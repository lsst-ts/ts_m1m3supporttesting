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
# Test Numbers: M13T-009  
# Author:       AClements
# Description:  Mirror Support System Active Motion Range
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where +X = 6.13mm, -X = 6.13mm, +Y = 6.13mm, -Y = -6.13mm, +Z = 4.07mm  & -Z = -5.57mm
#   +X, 0, 0 
#   -X, 0, 0
#   0,+Y, 0
#   0, -Y, 0
#   0, 0, +Z
#   0, 0, -Z
#   +X, +Y, 0
#   +X, -Y, 0
#   -X, +Y, 0
#   -X, -Y, 0
#   +X, 0, +Z
#   +X, 0, -Z
#   -X, 0, +Z
#   -X, 0, -Z
#   0, +Y, +Z
#   0, +Y, -Z
#   0, -Y, +Z
#   0, -Y, -Z
# - Repeat Matrix 2 more times
# - Transition back to standby
########################################################################

from MTM1M3Test import *
from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest
import time
import click

# edit the defined reference positions as needed.
REFERENCE = [0.0] * 6

TRAVEL_POSITION = 0.00613
POS_Z_TRAVEL_POSITION = 0.00407
NEG_Z_TRAVEL_POSITION = 0.00557
POSITION_TOLERANCE = 0.000008
ROTATION_TOLERANCE = 0.00000209
LOAD_PATH_FORCE = 0.0
LOAD_PATH_TOLERANCE = 0.0

class M13T009(MTM1M3Test):
    def _check_position(self, position, tolerance=POSITION_TOLERANCE, checkForces=False):
        data = m1m3.tel_hardpointActuatorData.get()
        self.assertAlmostEqual(data.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(data.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(data.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(data.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(data.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(data.zRotation, position[5], delta=tolerance)
        if checkForces:
            # Verify there are no unintended load paths.
            self.assertAlmostEqual(data.fx, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.fy, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.fz, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.mx, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.my, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.mz, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)

        imsData = m1m3.tel_imsData.get()
        self.assertAlmostEqual(imsData.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(imsData.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(imsData.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(imsData.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(imsData.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(imsData.zRotation, position[5], delta=tolerance)

    async def _waitHP(self):
        async def waitFor(state):
            while True:
                data = self.m1m3.tel_hardpointActuatorData.get()
                for hp in range(6):
                    if data.motionState[hp] != state:
                        await asyncio.sleep(0.1)
                        continue
                break
        waitFor(MTM1M3.HardpointActuatorMotionStates.STEPPING)
        waitFor(MTM1M3.HardpointActuatorMotionStates.STANDBY)


    async def test_movements(self):
        click.echo(click.style("M13T-009: Mirror Support System Active Motion Range", bold=True, fg="cyan"))

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # make sure the HardpointCorrection is disabled.
        await self.m1m3.cmd_disableHardpointCorrections.start
        await asyncio.sleep(5.0)
        
        # confirm mirror at reference position.
        self._check_position(REFERENCE)
        
        ##########################################################
        # Command the mirror to the matrix positions.  Check to make sure it reaches those positions.
            
        testTable = [
            ["(+X, 0, 0, 0, 0, 0)", REFERENCE[0] + TRAVEL_POSITION, REFERENCE[1], REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(-X, 0, 0, 0, 0, 0)", REFERENCE[0] - TRAVEL_POSITION, REFERENCE[1], REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, +Y, 0, 0, 0, 0)", REFERENCE[0], REFERENCE[1] + TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, -Y, 0, 0, 0, 0)", REFERENCE[0], REFERENCE[1] - TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, 0, +Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1], REFERENCE[2] + POS_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, 0, -Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1], REFERENCE[2] -NEG_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(+X, +Y, 0, 0, 0, 0)", REFERENCE[0] + TRAVEL_POSITION, REFERENCE[1] + TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(+X, -Y, 0, 0, 0, 0)", REFERENCE[0] + TRAVEL_POSITION, REFERENCE[1] - TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(-X, +Y, 0, 0, 0, 0)", REFERENCE[0] - TRAVEL_POSITION, REFERENCE[1] + TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(-X, -Y, 0, 0, 0, 0)", REFERENCE[0] - TRAVEL_POSITION, REFERENCE[1] - TRAVEL_POSITION, REFERENCE[2], REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(+X, 0, +Z, 0, 0, 0)", REFERENCE[0] + TRAVEL_POSITION, REFERENCE[1], REFERENCE[2] + POS_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(+X, 0, -Z, 0, 0, 0)", REFERENCE[0] + TRAVEL_POSITION, REFERENCE[1], REFERENCE[2] - NEG_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(-X, 0, +Z, 0, 0, 0)", REFERENCE[0] - TRAVEL_POSITION, REFERENCE[1], REFERENCE[2] + POS_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(-X, 0, -Z, 0, 0, 0)", REFERENCE[0] - TRAVEL_POSITION, REFERENCE[1], REFERENCE[2] - NEG_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, +Y, +Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1] + TRAVEL_POSITION, REFERENCE[2] + POS_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, +Y, -Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1] + TRAVEL_POSITION, REFERENCE[2] - NEG_Z_TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, -Y, +Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1] - TRAVEL_POSITION, REFERENCE[2] + TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
            ["(0, -Y, -Z, 0, 0, 0)", REFERENCE[0], REFERENCE[1] - TRAVEL_POSITION, REFERENCE[2] - TRAVEL_POSITION, REFERENCE[3], REFERENCE[4], REFERENCE[5]],
        ]
            
        for row in testTable:
            await self.m1m3.cmd_positionM1M3xPosition.set_start(xPosition=row[1], yPosition=row[2], zPosition=row[3], xRotation=row[4], yRotation=row[5], zRotation=row[6])
            self._waitHP()
            
            time.sleep(3.0)

            self._check_position(row[1:7], checkForces=True)
            
        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        await self.m1m3.cmd_lowerM1M3.start
        
if __name__ == "__main__":
    asynctest.main()
