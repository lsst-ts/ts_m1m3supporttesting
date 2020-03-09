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

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb
import time


TRANSLATION_STEP = 0.0002
ROTATION_STEP = 0.00004887
SETTLE_TIME = 5.0
SAMPLE_TIME = 1.0
LOOP_COUNT = 2

WAIT_UNTIL_TIMEOUT = 600

class M13T013:
    def Run(self, m1m3, sim, efd):
        Header("M13T-013: Determination of X, Y, Z, Zero Coordinate")
        
#        # Transition to disabled state
#        m1m3.Start("Default")
#        result, data = m1m3.GetEventDetailedState()
#        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
#        result, data = m1m3.GetEventSummaryState()
#        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
#        
#        # Transition to parked state
#        m1m3.Enable()
#        result, data = m1m3.GetEventDetailedState()
#        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedState)
#        result, data = m1m3.GetEventSummaryState()
#        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
#        
#        # Transition to parked engineering state
#        m1m3.EnterEngineering()
#        result, data = m1m3.GetEventDetailedState()
#        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedEngineeringState)
#        result, data = m1m3.GetEventSummaryState()
#        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
#        
#        # Raise mirror (therefore entering the Raised Engineering State).
#        m1m3.RaiseM1M3(False)
#        result, data = m1m3.GetEventDetailedState()
#        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_RaisingEngineeringState)
#        result, data = m1m3.GetEventSummaryState()
#        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
#        
#        # Wait until active engineering state
#        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        
        # Disable hardpoint corrections
        m1m3.DisableHardpointCorrections()
        
        # Get start timestamp
        rtn, data = m1m3.GetSampleHardpointActuatorData()
        startTimestamp = data.Timestamp
        
        # Wait for corrections to go away
        time.sleep(SETTLE_TIME)
        
        testTable = [
            ["X Position", -0.002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.002, 0.0, 0.0, 0.0, 0.0, 0.0, TRANSLATION_STEP, 0, 0, 0, 0, 0],
            ["Y Position", 0.0, -0.002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.002, 0.0, 0.0, 0.0, 0.0, 0, TRANSLATION_STEP, 0, 0, 0, 0],
            #["Z Position", 0.0, 0.0, -0.002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.002, 0.0, 0.0, 0.0, 0, 0, TRANSLATION_STEP, 0, 0, 0],
            #["X Rotation", 0.0, 0.0, 0.0, -0.0004887, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004887, 0.0, 0.0, 0, 0, 0, ROTATION_STEP, 0, 0],
            #["Y Rotation", 0.0, 0.0, 0.0, 0.0, -0.0004887, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004887, 0.0, 0, 0, 0, 0, ROTATION_STEP, 0],
            #["Z Rotation", 0.0, 0.0, 0.0, 0.0, 0.0, -0.0004887, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0004887, 0, 0, 0, 0, 0, ROTATION_STEP],
        ]
        detailTable = []
        for row in testTable:
            xPos = row[1]
            yPos = row[2]
            zPos = row[3]
            xRot = row[4]
            yRot = row[5]
            zRot = row[6]
            xPosStart = xPos
            yPosStart = yPos
            zPosStart = zPos
            xRotStart = xRot
            yRotStart = yRot
            zRotStart = zRot
            xPosEnd = row[7]
            yPosEnd = row[8]
            zPosEnd = row[9]
            xRotEnd = row[10]
            yRotEnd = row[11]
            zRotEnd = row[12]
            xPosStep = row[13]
            yPosStep = row[14]
            zPosStep = row[15]
            xRotStep = row[16]
            yRotStep = row[17]
            zRotStep = row[18]
            xPosSteps = 0
            if xPosStep != 0:
                xPosSteps = round((xPosEnd - xPosStart) / xPosStep)
            yPosSteps = 0
            if yPosStep != 0:
                yPosSteps = round((yPosEnd - yPosStart) / yPosStep)
            zPosSteps = 0
            if zPosStep != 0:
                zPosSteps = round((zPosEnd - zPosStart) / zPosStep)
            xRotSteps = 0
            if xRotStep != 0:
                xRotSteps = round((xRotEnd - xRotStart) / xRotStep)
            yRotSteps = 0
            if yRotStep != 0:
                yRotSteps = round((yRotEnd - yRotStart) / yRotStep)
            zRotSteps = 0
            if zRotStep != 0:
                zRotSteps = round((zRotEnd - zRotStart) / zRotStep)
            steps = int(max([xPosSteps, yPosSteps, zPosSteps, xRotSteps, yRotSteps, zRotSteps]))
            print("Steps: %d" % steps)
            for i in range(LOOP_COUNT):
                for j in range(steps):
                    # Clear HP states
                    rtn, data = m1m3.GetEventHardpointActuatorState()
                    
                    # Make a step
                    m1m3.PositionM1M3(xPos, yPos, zPos, xRot, yRot, zRot)
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))
                    
                    # Wait for motion to complete
                    time.sleep(SETTLE_TIME)
                    
                    # Get step data
                    datas = self.sampleHP(m1m3)
                    measuredFx = Average(datas, lambda data: data.Fx)
                    measuredFy = Average(datas, lambda data: data.Fy)
                    measuredFz = Average(datas, lambda data: data.Fz)
                    measuredMx = Average(datas, lambda data: data.Mx)
                    measuredMy = Average(datas, lambda data: data.My)
                    measuredMz = Average(datas, lambda data: data.Mz)
                    measuredXPos = Average(datas, lambda data: data.XPosition)
                    measuredYPos = Average(datas, lambda data: data.YPosition)
                    measuredZPos = Average(datas, lambda data: data.ZPosition)
                    measuredXRot = Average(datas, lambda data: data.XRotation)
                    measuredYRot = Average(datas, lambda data: data.YRotation)
                    measuredZRot = Average(datas, lambda data: data.ZRotation)                
                    detailTable.append([row[0], measuredXPos, measuredYPos, measuredZPos, measuredXRot, measuredYRot, measuredZRot, measuredFx, measuredFy, measuredFz, measuredMx, measuredMy, measuredMz])
                    
                    # Change position
                    xPos = round(xPos + xPosStep, 6)
                    yPos = round(yPos + yPosStep, 6)
                    zPos = round(zPos + zPosStep, 6)
                    xRot = round(xRot + xRotStep, 9)
                    yRot = round(yRot + yRotStep, 9)
                    zRot = round(zRot + zRotStep, 9)
                
                # Swap direction
                t1 = xPosEnd
                t2 = yPosEnd
                t3 = zPosEnd
                t4 = xRotEnd
                t5 = yRotEnd
                t6 = zRotEnd
                xPosEnd = xPosStart
                yPosEnd = yPosStart
                zPosEnd = zPosStart
                xRotEnd = xRotStart
                yRotEnd = yRotStart
                zRotEnd = zRotStart
                xPosStart = t1
                yPosStart = t2
                zPosStart = t3
                xRotStart = t4
                yRotStart = t5
                zRotStart = t6
                xPos = xPosStart
                yPos = yPosStart
                zPos = zPosStart
                xRot = xRotStart
                yRot = yRotStart
                zRot = zRotStart
                
                for j in range(steps):
                    # Clear HP states
                    rtn, data = m1m3.GetEventHardpointActuatorState()
                    
                    # Make a step
                    m1m3.PositionM1M3(xPos, yPos, zPos, xRot, yRot, zRot)
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))
                    
                    # Wait for motion to complete
                    time.sleep(SETTLE_TIME)
                    
                    # Get step data
                    datas = self.sampleHP(m1m3)
                    measuredFx = Average(datas, lambda data: data.Fx)
                    measuredFy = Average(datas, lambda data: data.Fy)
                    measuredFz = Average(datas, lambda data: data.Fz)
                    measuredMx = Average(datas, lambda data: data.Mx)
                    measuredMy = Average(datas, lambda data: data.My)
                    measuredMz = Average(datas, lambda data: data.Mz)
                    measuredXPos = Average(datas, lambda data: data.XPosition)
                    measuredYPos = Average(datas, lambda data: data.YPosition)
                    measuredZPos = Average(datas, lambda data: data.ZPosition)
                    measuredXRot = Average(datas, lambda data: data.XRotation)
                    measuredYRot = Average(datas, lambda data: data.YRotation)
                    measuredZRot = Average(datas, lambda data: data.ZRotation)                
                    detailTable.append([row[0], measuredXPos, measuredYPos, measuredZPos, measuredXRot, measuredYRot, measuredZRot, measuredFx, measuredFy, measuredFz, measuredMx, measuredMy, measuredMz])
                    
                    # Change position
                    xPos = round(xPos - xPosStep, 6)
                    yPos = round(yPos - yPosStep, 6)
                    zPos = round(zPos - zPosStep, 6)
                    xRot = round(xRot - xRotStep, 9)
                    yRot = round(yRot - yRotStep, 9)
                    zRot = round(zRot - zRotStep, 9)
                    
                # Swap direction
                t1 = xPosEnd
                t2 = yPosEnd
                t3 = zPosEnd
                t4 = xRotEnd
                t5 = yRotEnd
                t6 = zRotEnd
                xPosEnd = xPosStart
                yPosEnd = yPosStart
                zPosEnd = zPosStart
                xRotEnd = xRotStart
                yRotEnd = yRotStart
                zRotEnd = zRotStart
                xPosStart = t1
                yPosStart = t2
                zPosStart = t3
                xRotStart = t4
                yRotStart = t5
                zRotStart = t6
                xPos = xPosStart
                yPos = yPosStart
                zPos = zPosStart
                xRot = xRotStart
                yRot = yRotStart
                zRot = zRotStart
                
            # Reset position
            m1m3.PositionM1M3(0, 0, 0, 0, 0, 0)
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))
        
        # Write output file
        path = GetFilePath("%d-M13T013-2-Details.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write("Test,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation,Fx,Fy,Fz,Mx,My,Mz\r\n")
        for row in detailTable:
            file.write("%s,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
        file.close()
            
 #       # Transition to lowering engineering state
 #       m1m3.LowerM1M3()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
 #       
 #       # Wait until parked engineering state
 #       WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
 #           
 #       # Transition to disabled state
 #       m1m3.Disable()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
 #       
 #       # Transition to standby state
 #       m1m3.Standby()
 #       result, data = m1m3.GetEventDetailedState()
 #       Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
 #       result, data = m1m3.GetEventSummaryState()
 #       Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
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
    m1m3, sim, efd = Setup()
    M13T013().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
