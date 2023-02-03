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

from ForceActuatorTable import *
from MTM1M3Test import *

from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest
import click
import time
import numpy as np

TEST_FORCE = 222.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10


class M13T018(MTM1M3Test):
    async def _test_actuator(self, fa_type, fa_id):
        # Prepare force data
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156

        with click.progressbar(
            length=9,
            label=f"Bump testing {self.id} ({fa_type}{fa_id})",
            width=0,
            item_show_func=lambda i: "Starting"
            if i is None
            else [
                "Collecting baseline",
                "Push",
                "Checking push",
                "Zero after push",
                "Checking baseline",
                "Pull",
                "Checking after pull",
                "Zero after push",
                "Checking baseline",
            ][i],
        ) as bar:
            bar.update(1)

            # Get pre application force
            data = await self.sampleData(
                "tel_forceActuatorData", None, TEST_SAMPLES_TO_AVERAGE
            )
            baseline = self.average(data, ("xForce", "yForce", "zForce"))

            def setForce(force):
                if fa_type == "X":
                    xForces[fa_id] = force
                elif fa_type == "Y":
                    yForces[fa_id] = force
                elif fa_type == "Z":
                    zForces[fa_id] = force
                else:
                    raise RuntimeError(
                        f"Invalid FA type (only XYZ accepted): {fa_type}"
                    )

            async def applyAndVerify(force):
                setForce(force)

                if force == 0:
                    await self.m1m3.cmd_clearOffsetForces.start()
                else:
                    # Apply the offset forces
                    await self.m1m3.cmd_applyOffsetForces.set_start(
                        xForces=xForces, yForces=yForces, zForces=zForces
                    )

                await asyncio.sleep(0.3)

                bar.update(1)

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

                bar.update(1)

            async def verifyMeasured():
                test_started = time.monotonic()
                duration = 0
                failed = 0

                while duration < TEST_SETTLE_TIME * 4:
                    data = await self.sampleData(
                        "tel_forceActuatorData", None, TEST_SAMPLES_TO_AVERAGE
                    )
                    duration = time.monotonic() - test_started
                    averages = self.average(data, ("xForce", "yForce", "zForce"))

                    if (
                        np.allclose(
                            np.array(averages["xForce"]) - np.array(baseline["xForce"]),
                            xForces,
                            atol=TEST_TOLERANCE,
                        )
                        and np.allclose(
                            np.array(averages["yForce"]) - np.array(baseline["yForce"]),
                            yForces,
                            atol=TEST_TOLERANCE,
                        )
                        and np.allclose(
                            np.array(averages["zForce"]) - np.array(baseline["zForce"]),
                            zForces,
                            atol=TEST_TOLERANCE,
                        )
                    ):
                        if duration > TEST_SETTLE_TIME:
                            break
                    else:
                        failed += 1

                self.assertLessEqual(
                    duration,
                    TEST_SETTLE_TIME * 4,
                    msg=f"Actuator {self.id} ({fa_type}{fa_id}) tooks {duration:.02f}s and wasn't settled, failed {failed} times",
                )

                if duration > TEST_SETTLE_TIME + 1:
                    self.printWarning(
                        f"Actuator {self.id} ({fa_type}{fa_id}) tooks {duration:.02f}s to settled down, failed {failed} times"
                    )
                elif failed > 0:
                    self.printTest(
                        f"Actuator {self.id} ({fa_type}{fa_id}) failed {failed} times before settling down"
                    )

            await applyAndVerify(0)
            await verifyMeasured()

            await applyAndVerify(TEST_FORCE)
            await verifyMeasured()

            await applyAndVerify(0)
            await verifyMeasured()

            await applyAndVerify(-TEST_FORCE)
            await verifyMeasured()

            await applyAndVerify(0)
            await verifyMeasured()

    async def test_bump_raised(self):
        self.printHeader("M13T-018: Bump Test Raised")

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # Disable hardpoint corrections to keep forces good
        await self.m1m3.cmd_disableHardpointCorrections.start()

        await self.runActuators(self._test_actuator)

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
