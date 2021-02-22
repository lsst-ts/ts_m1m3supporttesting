#!/usr/bin/env python3.8

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
# Test Numbers: M13T-017
# Author:       CContaxis
# Description:  Active Optics Actuator Force Updates
# Steps:
# - Transition from standby to active engineering state
# - Clear active optic forces
# - Apply a set of active optic forces
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied
# - Apply an active optic force by bending modes
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied
# - Apply an active optic force by bending modes
# - Verify the active optic forces are applied
# - Apply a set of active optic forces
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied
# - Transition from active engineering state to standby
########################################################################

from CalculateBendingModeForces import *
from MTM1M3Test import *

from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest

TEST_MODE = [
    0.0,
    0.0,
    0.0,
    0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
]
TEST_FORCE = [1.2] * 156
TEST_TOLERANCE = 0.1
WAIT_UNTIL_TIMEOUT = 600


class M13T017(MTM1M3Test):
    async def test_active_optics_updates(self):
        self.printHeader("M13T-017: Active Optic Actuator Force Updates")

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        await asyncio.sleep(5.0)

        def verifyForces(zForces):
            # Get active optic forces
            data = self.m1m3.evt_appliedActiveOpticForces.get()

            # Validate all Z data
            self.assertListAlmostEqual(
                data.zForces,
                zForces,
                delta=TEST_TOLERANCE,
                msg=f"Verifying applied active optics forces",
            )

        async def clear_and_verify():
            await self.m1m3.cmd_clearActiveOpticForces.start()
            await asyncio.sleep(1.0)
            verifyForces([0] * 156)
            await asyncio.sleep(1.0)

        # Clear active optic forces and verify
        await clear_and_verify()

        self.printTest("Apply test forces")

        # Apply active optic force and verify
        await self.m1m3.cmd_applyActiveOpticForces.set_start(zForces=TEST_FORCE)
        await asyncio.sleep(1.0)
        verifyForces(TEST_FORCE)
        await asyncio.sleep(1.0)

        for i in range(2):
            self.printTest(f"Active + zero step {i}")
            # Clear active optic forces and verify
            await clear_and_verify()

            # Apply active optic force by bending mode and verify
            await self.m1m3.cmd_applyActiveOpticForcesByBendingModes.set_start(
                coefficients=TEST_MODE
            )
            await asyncio.sleep(1.0)
            verifyForces(CalculateBendingModeForces(TEST_MODE))
            await asyncio.sleep(1.0)

        self.printTest("Shutting down")

        # Apply active optic force and verify
        await self.m1m3.cmd_applyActiveOpticForces.set_start(zForces=TEST_FORCE)
        await asyncio.sleep(1.0)
        verifyForces(TEST_FORCE)
        await asyncio.sleep(1.0)

        # Clear active optic forces and verify
        await clear_and_verify()

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
