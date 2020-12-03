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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

import asynctest
import asyncio
import logging
from Utilities import *
from ForceActuatorTable import *
from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3


class M13T002(asynctest.TestCase):
    async def setUp(self):
        self.domain = salobj.Domain()
        self.m1m3 = salobj.Remote(self.domain, "MTM1M3")
        self.failedPrimary = []
        self.failedSecondary = []

    async def assertM1M3State(self, state, wait=2):
        await asyncio.sleep(wait)
        self.assertEqual(self.m1m3.evt_detailedState.get().detailedState, state)

    async def wait_bump_test(self):
        TIMEOUT = 26
        count = 0
        while True:
            data = await self.m1m3.evt_forceActuatorBumpTestStatus.aget()
            primary = data.primaryTest[self._actuator_index]
            if primary > 5 or count > TIMEOUT:
                break

            await asyncio.sleep(1)
            count += 1
            print(
                f"{count} M1M3 primary actuator {self._actuator_index} ID {self._actuator_id} ends in {primary}"
            )

        if primary != 6:
            self.failedPrimary.append(self._actuator_id)

        if self._secondary_index is None:
            return

        count = 0
        while True:
            secondary = self.m1m3.evt_forceActuatorBumpTestStatus.get().secondaryTest[
                self._secondary_index
            ]
            if secondary > 5 or count > TIMEOUT:
                break

            await asyncio.sleep(1)
            count += 1
            print(
                f"{count} M1M3 secondary actuator {self._secondary_index} ID {self._actuator_id} ends in {secondary}"
            )

        if secondary != 6:
            self.failedSecondary.append(self._actuator_id)

    async def test_bump_test(self):
        await self.m1m3.start_task
        #await self.assertM1M3State(MTM1M3.DetailedState.STANDBY)

        await self.m1m3.cmd_start.set_start(settingsToApply="Default", timeout=60)
        await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)

        await self.m1m3.cmd_enable.start()
        await self.assertM1M3State(MTM1M3.DetailedState.PARKED)

        await self.m1m3.cmd_enterEngineering.start()
        await self.assertM1M3State(MTM1M3.DetailedState.PARKEDENGINEERING)

        print('Sleeping..')
        await asyncio.sleep(20)

        secondary = 0

        for actuator in forceActuatorTable[:3]:
            self._actuator_index = actuator[0]
            self._actuator_id = actuator[1]
            if actuator[5] == "DAA":
                self._secondary_index = secondary
                secondary += 1
            else:
                self._secondary_index = None

            print(
                f"Testing actuator ID {self._actuator_id} primary {self._actuator_index}, secondary {self._secondary_index}"
            )
            await self.m1m3.cmd_forceActuatorBumpTest.set_start(
                actuatorId=self._actuator_id,
                testPrimary=True,
                testSecondary=self._secondary_index is not None,
            )
            await self.wait_bump_test()

        self.assertEqual(self.failedPrimary, [])
        self.assertEqual(self.failedSecondary, [])

if __name__ == "__main__":
    asynctest.main()
