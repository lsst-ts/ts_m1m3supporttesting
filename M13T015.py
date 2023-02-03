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
# Test Numbers: M13T-015
# Author:       CContaxis
# Description:  Active Optic Bending Mode Offsets
# Steps:
########################################################################

from MTM1M3Movements import *
from lsst.ts.idl.enums import MTM1M3
import CalculateBendingModeForces

import asyncio
import asynctest

TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 0.1


class M13T015(MTM1M3Movements):
    async def test_active_optic_bending_mode_offsets(self):
        self.printHeader("M13T-015: Active Optic Bending Mode Offsets")

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # Wait a bit
        await asyncio.sleep(2.0)

        # Enable hardpoint corrections
        await self.m1m3.cmd_enableHardpointCorrections.start()

        # Wait a bit more
        await asyncio.sleep(2.0)

        # Prepare force data
        bm = [0] * 22

        bmTests = [
            [
                5.00,
                3.00,
                1.50,
                0.50,
                0.10,
                0.20,
                0.05,
                0.60,
                0.10,
                0.05,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
            ],
            [
                1.00,
                2.00,
                3.00,
                0.50,
                0.10,
                1.00,
                0.20,
                0.60,
                0.05,
                0.05,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
            ],
            [
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.20,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.10,
                0.10,
                0.00,
                0.00,
                0.00,
                0.10,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
            ],
        ]

        # Iterate through all 156 force actuators
        for bm in bmTests:
            # Calculate expected forces
            targetForces = CalculateBendingModeForces.CalculateBendingModeForces(bm)

            self.printTest(f"Bending Mode {bm}")

            # Apply bending mode
            await self.m1m3.cmd_applyActiveOpticForcesByBendingModes.set_start(coefficients=bm)

            # Wait for bending mode forces
            await asyncio.sleep(TEST_SETTLE_TIME)

            data = self.m1m3.evt_appliedActiveOpticForces.get()
            self.assertListAlmostEqual(
                data.zForces,
                targetForces,
                delta=TEST_TOLERANCE,
                msg="Applied bending modes produces same forces as calculated",
            )

        self.printTest("Clear Bending Mode")

        # Clear bending mode forces
        targetForces = CalculateBendingModeForces.CalculateBendingModeForces([0] * 22)

        # Clear bending mode
        await self.m1m3.cmd_clearActiveOpticForces.start()

        # Wait for bending mode forces
        await asyncio.sleep(TEST_SETTLE_TIME)

        data = self.m1m3.evt_appliedActiveOpticForces.get()
        self.assertListAlmostEqual(
            data.zForces,
            targetForces,
            delta=TEST_TOLERANCE,
            msg="Cleared bending forces",
        )

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
