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
# - Transition from parked engineering state to standby
########################################################################

from MTM1M3Test import *
from ForceActuatorTable import *
from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest
import click


class M13T002(MTM1M3Test):
    TIMEOUT = 260

    async def setUp(self):
        await super().setUp()
        self.failed = {"primary": [], "secondary": []}
        self.emptyFailed = self.failed

    async def wait_bump_test(self):
        def test_state(state):
            return [
                "Not tested",
                "Testing start zero",
                "Testing positive",
                "Positive wait zero",
                "Testing negative",
                "Negative wait zero",
                click.style("Passed", fg="green"),
                click.style("Failed", fg="red"),
            ][min(state, 7)]

        primary = -1
        with click.progressbar(
            range(self.TIMEOUT),
            label=click.style(f"Primary {self._actuator_id:03d}", bold=True)
            + click.style(" (% of timeout time)"),
            item_show_func=lambda i: test_state(primary),
            width=0,
        ) as bar:
            for b in bar:
                data = await self.m1m3.evt_forceActuatorBumpTestStatus.aget()
                primary = data.primaryTest[self._actuator_index]
                if primary > 5:
                    bar.update(0)
                    break

                await asyncio.sleep(0.1)

        if primary != 6:
            click.echo(
                click.style(f"Failed primary {self._actuator_id}", bg="red", bold=True)
            )
            self.failed["primary"].append(self._actuator_id)

        if self._secondary_index is None:
            return

        count = 0

        secondary = -1
        with click.progressbar(
            range(self.TIMEOUT),
            label=click.style(f"Secondary {self._actuator_id:03d}", bold=True)
            + click.style(" (% of timeout time)"),
            item_show_func=lambda i: test_state(secondary),
            width=0,
        ) as bar:
            for b in bar:
                secondary = (
                    self.m1m3.evt_forceActuatorBumpTestStatus.get().secondaryTest[
                        self._secondary_index
                    ]
                )
                if secondary > 5:
                    bar.update(0)
                    break

                await asyncio.sleep(0.1)

        if secondary != 6:
            click.echo(
                click.style(
                    f"Failed secondary {self._actuator_id}", bg="red", bold=True
                )
            )
            self.failed["secondary"].append(self._actuator_id)

    async def test_bump_test(self):
        await self.startup(MTM1M3.DetailedState.PARKEDENGINEERING)

        with click.progressbar(range(200), label="Waiting for mirror", width=0) as bar:
            for b in bar:
                await asyncio.sleep(0.1)

        secondary = 0

        click.echo(
            click.style(
                f"Tests progressbars total is time allocated for completion ({self.TIMEOUT / 10:.1f} sec)!!",
                bold=True,
                fg="cyan",
            )
        )

        try:

            with click.progressbar(
                forceActuatorTable,
                label=click.style("Actuators", fg="green"),
                item_show_func=lambda a: "XXX" if a is None else str(a[1]),
                show_pos=True,
                width=0,
            ) as bar:
            
                for actuator in bar:
                    self._actuator_index = actuator[0]
                    self._actuator_id = actuator[1]
                    if actuator[5] == "DAA":
                        self._secondary_index = secondary
                        secondary += 1
                    else:
                        self._secondary_index = None
                    click.echo(
                        click.style(
                            f"Testing actuator ID {self._actuator_id} primary {self._actuator_index}, secondary {self._secondary_index}",
                            fg="blue",
                        )
                    )
                    await self.m1m3.cmd_forceActuatorBumpTest.set_start(
                        actuatorId=self._actuator_id,
                        testPrimary=True,
                        testSecondary=self._secondary_index is not None,
                    )
                    await self.wait_bump_test()
                
        except KeyboardInterrupt:

            click.echo(
                click.style(f"Actuator bump test killed while testing actuator ID {self._actuator_id} primary {self._actuator_index} " 
                    f"secondary {self._secondary_index}", fg="red", bold=True))

            await self.m1m3.cmd_killForceActuatorBumpTest.start()

        self.assertEqual(self.failed, self.emptyFailed)


if __name__ == "__main__":
    asynctest.main()
