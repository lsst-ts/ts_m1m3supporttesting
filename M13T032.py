########################################################################
# Test Numbers: M13T-032  
# Author:       CContaxis
# Description:  Independent Measuring System (IMS)
# Steps:
# - Transition from standby to active engineering state
# - Repeat the following 3 times:
#   - Follow the motion matrix below:
#     - +X  0  0
#     - -X  0  0
#     -  0 +Y  0
#     -  0 -Y  0
#     -  0  0 +Z
#     -  0  0 -Z
# - Transition from active engineering state to standby
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb
import time

# edit the defined reference positions as needed.
REFERENCE_X_POSITION = 0.0
REFERENCE_Y_POSITION = 0.0
REFERENCE_Z_POSITION = 0.0
REFERENCE_X_ROTATION = 0.0
REFERENCE_Y_ROTATION = 0.0
REFERENCE_Z_ROTATION = 0.0

TRAVEL_POSITION = 0.001
TRAVEL_ROTATION = 0.00024435
POSITION_TOLERANCE = 0.000008
ROTATION_TOLERANCE = 0.00000209
WAIT_UNTIL_TIMEOUT = 600
SETTLE_TIME = 3
SAMPLE_TIME = 1

testTable = [
    ["X Positive", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
    ["X Negative", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
    ["Y Positive", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
    ["Y Negative", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
    ["Z Positive", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
    ["Z Negative", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION]
]

class M13T032:
    def Run(self, m1m3, sim, efd):
        Header("M13T-032: Independent Measuring System (IMS)")

        testID = int(m1m3.Time())

        # Transition to disabled state
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Transition to parked state
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
          
        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        
        # Prepare log file
        path = GetFilePath("M13T032-%d-HP-IMS.csv" % (testID))
        log = open(path, "w+")
        log.write("Timestamp,Name,HP-X,HP-Y,HP-Z,HP-Rx,HP-Ry,HP-Rz,IMS-X,IMS-Y,IMS-Z,IMS-Rx,IMS-Ry,IMS-Rz\r\n")

        # Repeat 3 times
        for i in range(3):
            # Settle down son
            time.sleep(5.0)

            # Collect a IMS baseline to adjust the data for temperature variations
            hpdatas, imsdatas = self.sampleHPIMS(m1m3)
            xPosOffset = -Average(imsdatas, lambda data: data.XPosition)
            yPosOffset = -Average(imsdatas, lambda data: data.YPosition)
            zPosOffset = -Average(imsdatas, lambda data: data.ZPosition)
            xRotOffset = -Average(imsdatas, lambda data: data.XRotation)
            yRotOffset = -Average(imsdatas, lambda data: data.YRotation)
            zRotOffset = -Average(imsdatas, lambda data: data.ZRotation)

            # Iterate through test table
            for row in testTable:
                # Move to the test location
                rtn, data = m1m3.GetEventHardpointActuatorState()
                m1m3.PositionM1M3(row[1], row[2], row[3], row[4], row[5], row[6])
                WaitUntil("%s - MTM1M3_HardpointActuatorState.MotionState = Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
                WaitUntil("%s - MTM1M3_HardpointActuatorState.MotionState = Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))

                # Settle for a bit
                time.sleep(SETTLE_TIME)

                # Collect position data
                hpdatas, imsdatas = self.sampleHPIMS(m1m3)
                xPosHP = Average(hpdatas, lambda data: data.XPosition)
                yPosHP = Average(hpdatas, lambda data: data.YPosition)
                zPosHP = Average(hpdatas, lambda data: data.ZPosition)
                xRotHP = Average(hpdatas, lambda data: data.XRotation)
                yRotHP = Average(hpdatas, lambda data: data.YRotation)
                zRotHP = Average(hpdatas, lambda data: data.ZRotation)
                xPosIMS = Average(imsdatas, lambda data: data.XPosition) + xPosOffset
                yPosIMS = Average(imsdatas, lambda data: data.YPosition) + yPosOffset
                zPosIMS = Average(imsdatas, lambda data: data.ZPosition) + zPosOffset
                xRotIMS = Average(imsdatas, lambda data: data.XRotation) + xRotOffset
                yRotIMS = Average(imsdatas, lambda data: data.YRotation) + yRotOffset
                zRotIMS = Average(imsdatas, lambda data: data.ZRotation) + zRotOffset

                # Verify HP
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.XPosition" % (row[0], i + 1), xPosHP, row[1], POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.YPosition" % (row[0], i + 1), yPosHP, row[2], POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.ZPosition" % (row[0], i + 1), zPosHP, row[3], POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.XRotation" % (row[0], i + 1), xRotHP, row[4], ROTATION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.YRotation" % (row[0], i + 1), yRotHP, row[5], ROTATION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_HardpointActuatorData.ZRotation" % (row[0], i + 1), zRotHP, row[6], ROTATION_TOLERANCE)

                # Verify IMS vs HP
                InTolerance("%s - %d - MTM1M3_IMSData.XPosition" % (row[0], i + 1), xPosIMS, xPosHP, POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_IMSData.YPosition" % (row[0], i + 1), yPosIMS, yPosHP, POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_IMSData.ZPosition" % (row[0], i + 1), zPosIMS, zPosHP, POSITION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_IMSData.XRotation" % (row[0], i + 1), xRotIMS, xRotHP, ROTATION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_IMSData.YRotation" % (row[0], i + 1), yRotIMS, yRotHP, ROTATION_TOLERANCE)
                InTolerance("%s - %d - MTM1M3_IMSData.ZRotation" % (row[0], i + 1), zRotIMS, zRotHP, ROTATION_TOLERANCE)

                # Write record
                log.write("%0.3f,%s,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f\r\n" % (hpdatas[0].Timestamp, "%s - %d" % (row[0], i + 1), xPosHP, yPosHP, zPosHP, xRotHP, yRotHP, zRotHP, xPosIMS, yPosIMS, zPosIMS, xRotIMS, yRotIMS, zRotIMS))


            # Return to the reference position
            rtn, data = m1m3.GetEventHardpointActuatorState()
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x != 0))
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(lambda x: x == 0))

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        
        # Transition to the disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Transition to the standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)

    def sampleHPIMS(self, m1m3):
        hpdatas = []
        imsdatas = []
        rtn, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        hpdatas.append(data)
        rtn, data = m1m3.GetSampleIMSData()
        imsdatas.append(data)
        while (data.Timestamp - startTime) <= SAMPLE_TIME:
            rtn, data = m1m3.GetNextSampleHardpointActuatorData()
            if rtn >= 0:
                hpdatas.append(data)
            rtn, data = m1m3.GetNextSampleIMSData()
            if rtn >= 0:
                imsdatas.append(data)
        return hpdatas, imsdatas
        
    def checkMotionStateEquals(self, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False
        
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T032().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
