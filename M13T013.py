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
# Test Numbers: M13T-013 
# Author:       CContaxis
# Description:  Determination of X, Y, Z Zero Coordinate
# Steps:
# - Transition from standby to active engineering state
# - Disable hardpoint corrections
# - Determine +Z rotation range
# - Determine -Z rotation range
# - Determine +X rotation range
# - Determine -X rotation range
# - Determine +Y rotation range
# - Determine -Y rotation range
# - Determine +X position range
# - Determine -X position range
# - Determine +Y position range
# - Determine -Y position range
# - Determine +Z position range
# - Determine -Z position range
# - Write result file out
# - Transition from active engineering state to standby
########################################################################

import asyncio
import asynctest

from lsst.ts.idl.enum import MTM1M3

TRANSLATION_STEP = 0.0001
ROTATION_STEP = 0.000024435

class M13T013(MTM1M3Movements):
    SETTLE_TIME = 3.0
    SAMPLE_TIME = 1.0

    async def test_zero_coordinates_determination(self):
        self.printHeader("M13T-013: Determination of X, Y, Z, Zero Coordinate")

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)
        
        # Disable hardpoint corrections
        await self.m1m3.cmd_disableHardpointCorrections.start()
        
        # Get start timestamp
        startTimestamp = self.m1m3.tel_hardpointActuatorData.get().timestamp
        
        # Wait for corrections to go away
        await asyncio.sleep(SETTLE_TIME)
        
        testTable = [
            ["X Pos Position", TRANSLATION_STEP, 0.0, 0.0, 0.0, 0.0, 0.0, 1200, 1200, 1200, 800, 800, 800],
            ["X Neg Position", -TRANSLATION_STEP, 0.0, 0.0, 0.0, 0.0, 0.0, 1200, 1200, 1200, 800, 800, 800],
            ["Y Pos Position", 0.0, TRANSLATION_STEP, 0.0, 0.0, 0.0, 0.0, 1200, 1200, 1200, 800, 800, 800],
            ["Y Neg Position", 0.0, -TRANSLATION_STEP, 0.0, 0.0, 0.0, 0.0, 1200, 1200, 1200, 800, 800, 800],
            ["Z Pos Position", 0.0, 0.0, TRANSLATION_STEP, 0.0, 0.0, 0.0, 1000, 1000, 1000, 800, 800, 800],
            ["Z Neg Position", 0.0, 0.0, -TRANSLATION_STEP, 0.0, 0.0, 0.0, 1000, 1000, 1000, 800, 800, 800],
            ["X Pos Rotation", 0.0, 0.0, 0.0, ROTATION_STEP, 0.0, 0.0, 1000, 1000, 1000, 1200, 1200, 1200],
            ["X Neg Rotation", 0.0, 0.0, 0.0, -ROTATION_STEP, 0.0, 0.0, 1000, 1000, 1000, 1200, 1200, 1200],
            ["Y Pos Rotation", 0.0, 0.0, 0.0, 0.0, ROTATION_STEP, 0.0, 1000, 1000, 1000, 1200, 1200, 1200],
            ["Y Neg Rotation", 0.0, 0.0, 0.0, 0.0, -ROTATION_STEP, 0.0, 1000, 1000, 1000, 1200, 1200, 1200],
            ["Z Pos Rotation", 0.0, 0.0, 0.0, 0.0, 0.0, ROTATION_STEP, 1000, 1000, 1000, 1500, 1500, 1500],
            ["Z Neg Rotation", 0.0, 0.0, 0.0, 0.0, 0.0, -ROTATION_STEP, 1000, 1000, 1000, 1500, 1500, 1500],
        ]
        resultTable = []
        detailTable = []
        for row in testTable:
            # Settle for a bit before taking a baseline
            await asyncio.sleep(SETTLE_TIME)
            
            # Get baseline data
            datas = self.sampleHP(m1m3)
            bFx = Average(datas, lambda data: data.Fx)
            bFy = Average(datas, lambda data: data.Fy)
            bFz = Average(datas, lambda data: data.Fz)
            bMx = Average(datas, lambda data: data.Mx)
            bMy = Average(datas, lambda data: data.My)
            bMz = Average(datas, lambda data: data.Mz)
            dFx = 0
            dFy = 0
            dFz = 0
            dMx = 0
            dMy = 0
            dMz = 0
            
            # Loop until force / moment triggers are hit
            while abs(dFx) < row[7] and abs(dFy) < row[8] and abs(dFz) < row[9] and abs(dMx) < row[10] and abs(dMy) < row[11] and abs(dMz) < row[12]:
                # Clear HP states
                rtn, data = self.m1m3.GetEventHardpointActuatorState()
                
                # Make a step
                await self.m1m3.cmd_translateM1M3.set_start(
                        xPosition=row[1], 
                        yPosition=row[2],
                        zPosition=row[3],
                        xRotation=row[4],
                        yRotation=row[5],
                        zRotation=row[6]
                )
                await self.waitHP()
                
                # Wait for motion to complete
                await asyncio.sleep(SETTLE_TIME)
                
                # Get step data
                datas = self.sampleHP(m1m3)
                Fx = Average(datas, lambda data: data.Fx)
                Fy = Average(datas, lambda data: data.Fy)
                Fz = Average(datas, lambda data: data.Fz)
                Mx = Average(datas, lambda data: data.Mx)
                My = Average(datas, lambda data: data.My)
                Mz = Average(datas, lambda data: data.Mz)
                xPos = Average(datas, lambda data: data.XPosition)
                yPos = Average(datas, lambda data: data.YPosition)
                zPos = Average(datas, lambda data: data.ZPosition)
                xRot = Average(datas, lambda data: data.XRotation)
                yRot = Average(datas, lambda data: data.YRotation)
                zRot = Average(datas, lambda data: data.ZRotation)                
                dFx = Fx - bFx
                dFy = Fy - bFy
                dFz = Fz - bFz
                dMx = Mx - bMx
                dMy = My - bMy
                dMz = Mz - bMz
                detailTable.append([row[0], xPos, yPos, zPos, xRot, yRot, zRot, Fx, Fy, Fz, Mx, My, Mz])
                
            # Get position data
            datas = self.sampleHP(m1m3)
            xPos = Average(datas, lambda data: data.XPosition)
            yPos = Average(datas, lambda data: data.YPosition)
            zPos = Average(datas, lambda data: data.ZPosition)
            xRot = Average(datas, lambda data: data.XRotation)
            yRot = Average(datas, lambda data: data.YRotation)
            zRot = Average(datas, lambda data: data.ZRotation)
            hp1Enc = Average(datas, lambda data: data.Encoder[0])
            hp2Enc = Average(datas, lambda data: data.Encoder[1])
            hp3Enc = Average(datas, lambda data: data.Encoder[2])
            hp4Enc = Average(datas, lambda data: data.Encoder[3])
            hp5Enc = Average(datas, lambda data: data.Encoder[4])
            hp6Enc = Average(datas, lambda data: data.Encoder[5])
            
            # Add position data to results
            resultTable.append([row[0], xPos, yPos, zPos, xRot, yRot, zRot, hp1Enc, hp2Enc, hp3Enc, hp4Enc, hp5Enc, hp6Enc])
                
            # Reset position
            m1m3.PositionM1M3(0, 0, 0, 0, 0, 0)
            WaitUntil("SAL %s m1m3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
            WaitUntil("SAL %s m1m3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))
            
        # Write output file
        path = GetFilePath("%d-M13T013-Positions.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write("Test,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation,HP1Encoder,HP2Encoder,HP3Encoder,HP4Encoder,HP5Encoder,HP6Encoder\r\n")
        for row in resultTable:
            file.write("%s,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%d,%d,%d,%d,%d,%d\r\n" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
        file.close()
        
        # Write output file
        path = GetFilePath("%d-M13T013-Details.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write("Test,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation,Fx,Fy,Fz,Mx,My,Mz\r\n")
        for row in detailTable:
            file.write("%s,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
        file.close()
            
 #       # Transition to lowering engineering state
 #       m1m3.LowerM1M3()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
 #       
 #       # Wait until parked engineering state
 #       WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)
 #           
 #       # Transition to disabled state
 #       m1m3.Disable()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
 #       
 #       # Transition to standby state
 #       m1m3.Standby()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def sampleHP(self, m1m3):
        datas = []
        rtn, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        datas.append(data)
        while (data.Timestamp - startTime) <= SAMPLE_TIME:
            rtn, data = m1m3.GetNextSampleHardpointActuatorData()
            if rtn >= 0:
                datas.append(data)
        return datas
        
    def checkMotionStateEquals(self, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False
        
        
if __name__ == "__main__":
    asynctest.main()
