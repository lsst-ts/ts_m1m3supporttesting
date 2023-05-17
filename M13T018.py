#!/usr/bin/env python3

# This file is part of M1M3 SS test suite.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

########################################################################
# Test Numbers: M13T-018
# Author:       CContaxis
# Description:  Bump test raised
# Steps:
# - Transition from standby to active engineering state
# - Perform the following steps for each force actuator and each of its force component (X or Y and Z)
#   - Apply a pure force offset
#   - Verify the pure force is being applied
#   - Verify the pure force is being measured
#   - Clear offset forces
#   - Verify the pure force is no longer being applied
#   - Verify the pure force is no longer being measured
#   - Apply a pure -force offset
#   - Verify the pure -force is being applied
#   - Verify the pure -force is being measured
#   - Clear offset forces
#   - Verify the pure -force is no longer being applied
#   - Verify the pure -force is no longer being measured
# - Transition from active engineering state to standby
########################################################################

import asyncio
from datetime import datetime, timezone
import time

import asynctest
import click
import numpy as np
from lsst.ts.cRIOpy.M1M3FATable import (
    FATABLE,
    FATABLE_ID,
    FATABLE_INDEX,
    FATABLE_XFA,
    FATABLE_XINDEX,
    FATABLE_YFA,
    FATABLE_YINDEX,
    FATABLE_ZFA,
    FATABLE_ZINDEX,
)
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Test import MTM1M3Test

TEST_FORCE = 222.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10


class FATestAttempt:
    def __init__(self, measured, baseline, expected):
        self.measured = measured
        self.baseline = baseline
        self.error = measured - baseline
        self.expected = expected
        self.passed = abs(expected - self.error) < TEST_TOLERANCE

    def __str__(self) -> str:
        return f"measured: {self.measured:.02f} N baseline: {self.baseline:.02f} N error: {self.error:.02f} N expected: {self.expected:.02f} N"


class FATest:
    def __init__(self, index: int, actuator_id: int, orientation: str) -> None:
        self.index = index
        self.actuator_id = actuator_id
        self.orientation = orientation

        self.tries = []

    def add_test(self, test: FATestAttempt) -> None:
        self.tries.append(test)

    def print_failed(self) -> None:
        failed = [tried for tried in self.tries if tried.passed == False]
        for fail in failed:
            print(f"{self.actuator_id} ({self.orientation}{self.index}) : {fail}")

    def clear(self) -> None:
        self.tries = []


class M13T018(MTM1M3Test):
    async def _test_actuator(self, fa_type, fa_id):
        # Prepare force data
        xForces = [0] * FATABLE_XFA
        yForces = [0] * FATABLE_YFA
        zForces = [0] * FATABLE_ZFA

        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - collecting baseline"
        )

        await self.m1m3.cmd_clearOffsetForces.start()

        await asyncio.sleep(3)

        # Get pre application force
        data = await self.sampleData(
            "tel_forceActuatorData", None, TEST_SAMPLES_TO_AVERAGE
        )
        self.printCode(
            f"Baseline at {datetime.now(timezone.utc).isoformat()} timestamps: {data[0].timestamp} {data[-1].timestamp}"
        )
        baseline = self.average(data, ("xForce", "yForce", "zForce"))

        x_tests = [
            FATest(row[FATABLE_XINDEX], row[FATABLE_ID], "X")
            for row in FATABLE
            if row[FATABLE_XINDEX] is not None
        ]
        y_tests = [
            FATest(row[FATABLE_YINDEX], row[FATABLE_ID], "Y")
            for row in FATABLE
            if row[FATABLE_YINDEX] is not None
        ]
        z_tests = [
            FATest(row[FATABLE_ZINDEX], row[FATABLE_ID], "Z")
            for row in FATABLE
            if row[FATABLE_ZINDEX] is not None
        ]

        def print_failed():
            for test in x_tests:
                test.print_failed()
            for test in y_tests:
                test.print_failed()
            for test in z_tests:
                test.print_failed()

        def clear_tests():
            for test in x_tests:
                test.clear()
            for test in y_tests:
                test.clear()
            for test in z_tests:
                test.clear()

        def setForce(force):
            if fa_type == "X":
                xForces[fa_id] = force
            elif fa_type == "Y":
                yForces[fa_id] = force
            elif fa_type == "Z":
                zForces[fa_id] = force
            else:
                raise RuntimeError(f"Invalid FA type (only XYZ accepted): {fa_type}")

        async def applyAndVerify(force):
            setForce(force)

            if force == 0:
                await self.m1m3.cmd_clearOffsetForces.start()
            else:
                # Apply the offset forces
                await self.m1m3.cmd_applyOffsetForces.set_start(
                    xForces=xForces, yForces=yForces, zForces=zForces
                )

            await asyncio.sleep(0.7)

            data = self.m1m3.evt_appliedOffsetForces.get()

            self.assertFalse(
                data is None, msg="Cannot retrieve evt_appliedOffsetForces"
            )

            self.assertListAlmostEqual(
                data.xForces,
                xForces,
                delta=TEST_TOLERANCE,
                msg="Applied X offsets doesn't match.",
            )
            self.assertListAlmostEqual(
                data.yForces,
                yForces,
                delta=TEST_TOLERANCE,
                msg="Applied Y offsets doesn't match.",
            )
            self.assertListAlmostEqual(
                data.zForces,
                zForces,
                delta=TEST_TOLERANCE,
                msg="Applied Z offsets doesn't match.",
            )

        async def verifyMeasured():
            test_started = time.monotonic()
            failed = 0
            clear_tests()
            duration = 0

            while duration < TEST_SETTLE_TIME * 4:
                data = await self.sampleData(
                    "tel_forceActuatorData", None, TEST_SAMPLES_TO_AVERAGE
                )
                duration = time.monotonic() - test_started
                averages = self.average(data, ("xForce", "yForce", "zForce"))

                last_failed = failed

                for actuator in FATABLE:
                    x_index = actuator[FATABLE_XINDEX]
                    if x_index is not None:
                        attempt = FATestAttempt(
                            averages["xForce"][x_index],
                            baseline["xForce"][x_index],
                            xForces[x_index],
                        )
                        if not (attempt.passed):
                            failed += 1
                        x_tests[x_index].add_test(attempt)

                    y_index = actuator[FATABLE_YINDEX]
                    if y_index is not None:
                        attempt = FATestAttempt(
                            averages["yForce"][y_index],
                            baseline["yForce"][y_index],
                            yForces[y_index],
                        )
                        if not (attempt.passed):
                            failed += 1
                        y_tests[y_index].add_test(attempt)

                    z_index = actuator[FATABLE_ZINDEX]
                    if z_index is not None:
                        attempt = FATestAttempt(
                            averages["zForce"][z_index],
                            baseline["zForce"][z_index],
                            zForces[z_index],
                        )
                        if not (attempt.passed):
                            failed += 1
                        z_tests[z_index].add_test(attempt)

                if failed == last_failed:
                    break

            if duration > TEST_SETTLE_TIME * 4:
                self.printError(
                    f"When testing actuator {self.id} ({fa_type}{fa_id}), it tooks {duration:.02f}s and wasn't settled, noticed {failed} failures listed below:"
                )
                self.failedFAs.append(f"{fa_type}{fa_id} - {self.id}")
                print_failed()

            elif duration > TEST_SETTLE_TIME + 1:
                self.printWarning(
                    f"When testing actuator {self.id} ({fa_type}{fa_id}), it  tooks {duration:.02f}s to settled down, noticed {failed} failures listed below"
                )
                print_failed()
            elif failed > 0:
                self.printTest(
                    f"When testing actuator {self.id} ({fa_type}{fa_id}), noticed {failed} failures before settling down - they are listed below:"
                )
                print_failed()

        self.print_progress(f"Bump testing {self.id} ({fa_type}{fa_id}) - 1st zero")
        await applyAndVerify(0)
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - verify 1st zero"
        )
        await verifyMeasured()

        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - {TEST_FORCE} N"
        )
        await applyAndVerify(TEST_FORCE)
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - verify {TEST_FORCE} N"
        )
        await verifyMeasured()

        self.print_progress(f"Bump testing {self.id} ({fa_type}{fa_id}) - 2nd zero")
        await applyAndVerify(0)
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - verify 2nd zero"
        )
        await verifyMeasured()

        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - {-TEST_FORCE} N"
        )
        await applyAndVerify(-TEST_FORCE)
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - verify {-TEST_FORCE} N"
        )
        await verifyMeasured()

        self.print_progress(f"Bump testing {self.id} ({fa_type}{fa_id}) - final zero")
        await applyAndVerify(0)
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - verify final zero"
        )
        await verifyMeasured()
        self.print_progress(
            f"Bump testing {self.id} ({fa_type}{fa_id}) - finished", True
        )

    async def test_bump_raised(self):
        self.printHeader("M13T-018: Bump Test Raised")

        self.failedFAs = []

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # Disable hardpoint corrections to keep forces good
        await self.m1m3.cmd_disableHardpointCorrections.start()

        await asyncio.sleep(10)

        await self.run_actuators(self._test_actuator)

        await self.shutdown(MTM1M3.DetailedState.STANDBY)

        self.assertEqual(self.failedFAs, [])


if __name__ == "__main__":
    asynctest.main()
