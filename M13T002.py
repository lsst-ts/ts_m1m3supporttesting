#!/usr/bin/env python3

# This file is part of ts_salobj.
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
# Test Numbers: M13T-002
# Description:  Bump test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator and each of its force
# component (X or Y and Z)
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
# - Transition from parked engineering state to standby
########################################################################

import asyncio
import asynctest
import click
import time

from MTM1M3Test import MTM1M3Test
from lsst.ts.cRIOpy.M1M3FATable import (
    FATABLE,
    FATABLE_ID,
    FATABLE_INDEX,
    FATABLE_SINDEX,
)
from lsst.ts.idl.enums import MTM1M3


class M13T002(MTM1M3Test):
    # max time for cylinder bump test; it's 5 seconds per block, 4 block
    # 20 sec nominal
    TIMEOUT = 40

    async def setUp(self):
        await super().setUp()
        self.failed = {"primary": [], "secondary": []}
        self.emptyFailed = self.failed

    async def _test_cylinder(self, actuator_id: int, index: int, primary: bool) -> None:
        start_time = time.monotonic()
        primary_str = "Primary" if primary else "Secondary"

        def get_bump_test_state(bump_test_status):
            if primary:
                return bump_test_status.primaryTest[index]
            return bump_test_status.secondaryTest[index]

        # last_test_state becomes None once a change in test status is detected
        last_test_state = get_bump_test_state(
            self.m1m3.evt_forceActuatorBumpTestStatus.get()
        )

        await self.m1m3.cmd_forceActuatorBumpTest.set_start(
            actuatorId=actuator_id,
            testPrimary=primary,
            testSecondary=not primary,
        )

        def get_test_state_str(state):
            return [
                "Not tested/Unknown",
                "Testing start zero",
                "Testing positive",
                "Positive wait zero",
                "Testing negative",
                "Negative wait zero",
                click.style("Passed", fg="green"),
                click.style("Failed", fg="red"),
            ][min(state, 7)]

        test_state = 0

        while True:
            if time.monotonic() - start_time > self.TIMEOUT:
                self.printTest(f"{primary_str} FA {actuator_id} timeouted.")
                break

            try:
                test_state = get_bump_test_state(
                    await self.m1m3.evt_forceActuatorBumpTestStatus.next(
                        flush=False, timeout=1
                    )
                )
                if last_test_state is not None and last_test_state != test_state:
                    last_test_state = None
                if test_state in (MTM1M3.BumpTest.PASSED, MTM1M3.BumpTest.FAILED):
                    if last_test_state is None:
                        break

            except asyncio.TimeoutError:
                pass

            applied = self.m1m3.tel_appliedCylinderForces.get()
            measured = self.m1m3.tel_forceActuatorData.get()
            # applied forces are in mN
            if primary:
                applied_force = applied.primaryCylinderForces[index] / 1000.0
                measured_force = measured.primaryCylinderForce[index]
            else:
                applied_force = applied.secondaryCylinderForces[index] / 1000.0
                measured_force = measured.secondaryCylinderForce[index]
            self.print_progress(
                f"{primary_str} FA {actuator_id}  ({index}) test: {test_state} ({get_test_state_str(test_state)}) {applied_force:.02f} {measured_force:.02f} {abs(applied_force - measured_force):.02f}"
            )

        if test_state == MTM1M3.BumpTest.PASSED and last_test_state is None:
            self.printTest(f"{primary_str} FA {actuator_id} passed.")
            return

        self.failed["primary" if primary else "secondary"].append(actuator_id)

    async def _test_actuator(self, actuator):
        actuator_index = actuator[FATABLE_INDEX]
        actuator_id = actuator[FATABLE_ID]
        secondary_index = actuator[FATABLE_SINDEX]

        self.printHeader(
            f"Testing {'SAA' if secondary_index is None else 'DAA'} actuator {actuator_id} ({actuator_index})"
        )

        await self._test_cylinder(actuator_id, actuator_index, True)
        if secondary_index is not None:
            await self._test_cylinder(actuator_id, secondary_index, False)

    async def test_bump_test(self):
        await self.startup(MTM1M3.DetailedState.PARKEDENGINEERING)

        with click.progressbar(range(200), label="Waiting for mirror", width=0) as bar:
            for b in bar:
                await asyncio.sleep(0.1)

        click.echo(
            click.style(
                f"Tests progressbars total is time allocated for completion ({self.TIMEOUT / 10:.1f} sec)!!",
                bold=True,
                fg="cyan",
            )
        )

        enabled = self.get_enabled_force_actuators()

        for actuator in FATABLE:
            if enabled[actuator[FATABLE_INDEX]] is False:
                self.printWarning(f"Skipping FA {actuator[FATABLE_ID]} ({actuator[FATABLE_INDEX]}).")
                continue

            await self._test_actuator(actuator)

        self.assertEqual(self.failed, self.emptyFailed)


if __name__ == "__main__":
    asynctest.main()
