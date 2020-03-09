########################################################################
# Test Numbers: M13T-011  
# Author:       AClements
# Description:  Position Stability During Active Mode Operation
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Wait 5 seconds for everything to settle
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm
# - Wait 15 seconds between each movement to let control take measurements.
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
# - Pull data from EFD to generate RMS values specified by the test.
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from SALPY_vms import *
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

X1Sensitivity = 51.459
Y1Sensitivity = 52.061
Z1Sensitivity = 51.298

X2Sensitivity = 51.937
Y2Sensitivity = 52.239
Z2Sensitivity = 52.130

X3Sensitivity = 52.183
Y3Sensitivity = 52.015
Z3Sensitivity = 51.908

TRAVEL_POSITION = 0.001
TRAVEL_ROTATION = 0.00024435
POSITION_TOLERANCE = 0.000008
ROTATION_TOLERANCE = 0.00000209
WAIT_UNTIL_TIMEOUT = 600
SETTLE_TIME = 3.0
SAMPLE_TIME = 15.0

def convert(raw, sensitivity):
    return (raw * 1000.0) / sensitivity

class M13T011:
    def Run(self, m1m3, sim, efd):
        Header("M13T-011: Position Stability During Active Mode Operation")

        # Setup VMS
        vms = SAL_vms()
        vms.salTelemetrySub("vms_M1M3")
        
        ########################################
        # Enable the mirror, Raise it.

        # Bring mirror into Disabled state.
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Place mirror into Enabled state.
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_EnabledState)
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
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ActiveState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        
        # wait 5 seconds
        time.sleep(5)

        skipFirstMove = True

        # The martix need to be tested 3 times
        for i in range(0,3):
            testTable = [
                ["REF", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+X", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-X", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+Y", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-Y", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+X+Y", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+X-Y", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-X+Y", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-X-Y", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+X+Z", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+X-Z", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-X+Z", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-X-Z", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+Y+Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["+Y-Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-Y+Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["-Y-Z", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION]]

            for row in testTable:
                # Dont attempt to move to reference position unless we have moved previously
                if not skipFirstMove:
                    # Perform the requested motion
                    rtn, data = m1m3.GetEventHardpointActuatorState()
                    m1m3.PositionM1M3(row[1], row[2], row[3], row[4], row[5], row[6])

                    # Wait for the requested motion to complete
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x != 0))
                    WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x == 0))
                else:
                    skipFirstMove = False

                # Allow some settling time
                time.sleep(SETTLE_TIME)

                # Prepare to sample data
                imsDatas = []
                vmsDatas = []

                # Flush IMS data
                result, imsData = m1m3.GetSampleIMSData()

                # Flush VMS data
                vmsData = vms_M1M3C()
                result = vms.getNextSample_M1M3(vmsData)
                while result >= 0:
                    vmsData = vms_M1M3C()
                    result = vms.getNextSample_M1M3(vmsData)

                # Mark times
                startTimestamp = imsData.Timestamp
                timestamp = startTimestamp

                # Sample data for the configured sample time
                while (timestamp - startTimestamp) < SAMPLE_TIME:
                    result, imsData = m1m3.GetNextSampleIMSData()
                    if result >= 0:
                        timestamp = imsData.Timestamp
                        imsDatas.append(imsData)
                    vmsData = vms_M1M3C()
                    result = vms.getNextSample_M1M3(vmsData)
                    if result >= 0:
                        vmsDatas.append(vmsData)

                # Write the IMS data to a file
                path = GetFilePath("M13T011-%s-%d-IMS-%d.csv" % (row[0], (i+1), int(startTimestamp)))
                file = open(path, "w+")
                file.write("Timestamp,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation\r\n")
                for imsData in imsDatas:
                    file.write("%0.3f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f\r\n" % (imsData.Timestamp, imsData.XPosition, imsData.YPosition, imsData.ZPosition, imsData.XRotation, imsData.YRotation, imsData.ZRotation))
                file.close()

                # Write the VMS data to a file
                path = GetFilePath("M13T011-%s-%d-VMS-%d.csv" % (row[0], (i+1), int(startTimestamp)))
                file = open(path, "w+")
                file.write("Timestamp (s),X1 (m/s^2),Y1 (m/s^2),Z1 (m/s^2),X2 (m/s^2),Y2 (m/s^2),Z2 (m/s^2),X3 (m/s^2),Y3 (m/s^2),Z3 (m/s^2)\r\n")
                for vmsData in vmsDatas:
                    newTimestamp = vmsData.Timestamp
                    for j in range(50):
                        file.write("%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n" % (
                            newTimestamp, 
                            convert(vmsData.Sensor1XAcceleration[j], X1Sensitivity),
                            convert(vmsData.Sensor1YAcceleration[j], Y1Sensitivity),
                            convert(vmsData.Sensor1ZAcceleration[j], Z1Sensitivity),
                            convert(vmsData.Sensor2XAcceleration[j], X2Sensitivity),
                            convert(vmsData.Sensor2YAcceleration[j], Y2Sensitivity),
                            convert(vmsData.Sensor2ZAcceleration[j], Z2Sensitivity),
                            convert(vmsData.Sensor3XAcceleration[j], X3Sensitivity),
                            convert(vmsData.Sensor3YAcceleration[j], Y3Sensitivity),
                            convert(vmsData.Sensor3ZAcceleration[j], Z3Sensitivity)))
                        newTimestamp += 0.001
                file.close()               

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        
        # Bring mirror into Disabled state.
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL MTM1M3_logevent_SummaryState.SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
    def checkMotionStateEquals(self, m1m3, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False        
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T011().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
