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

class M13T011:
    def Run(self, m1m3, sim, efd):
        Header("M13T-011: Position Stability During Active Mode Operation")
        
        ########################################
        # Enable the mirror, Raise it.

        # Bring mirror into Disabled state.
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Place mirror into Enabled state.
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_EnabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ActiveState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)
        
        # wait 5 seconds
        time.sleep(5)

        # The martix need to be tested 3 times
        for i in range(0,3):
           testTable = [
                ["(0, 0, 0, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(+X, 0, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(-X, 0, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(+X, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(+X, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(-X, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(-X, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(+X, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(+X, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(-X, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(-X, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, +Y, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, +Y, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, -Y, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
                ["(0, -Y, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION]*                
            ]
            
            for row in testTable:
                rtn, data = m1m3.GetEventHardpointActuatorState()
                m1m3.PositionM1M3(row[1], row[2], row[3], row[4], row[5], row[6])
                WaitUntil("SAL %s m1m3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x != 0))
                WaitUntil("SAL %s m1m3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x == 0))
                
                time.sleep(5.0)
                
                result, data = m1m3.GetSampleHardpointActuatorData()
                startTime = data.Timestamp
                InTolerance("SAL %s m1m3_HardpointActuatorData.XPosition" % row[0], data.XPosition, row[1], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_HardpointActuatorData.YPosition" % row[0], data.YPosition, row[2], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_HardpointActuatorData.ZPosition" % row[0], data.ZPosition, row[3], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_HardpointActuatorData.XRotation" % row[0], data.XRotation, row[4], ROTATION_TOLERANCE)
                InTolerance("SAL %s m1m3_HardpointActuatorData.YRotation" % row[0], data.YRotation, row[5], ROTATION_TOLERANCE)
                InTolerance("SAL %s m1m3_HardpointActuatorData.ZRotation" % row[0], data.ZRotation, row[6], ROTATION_TOLERANCE)
                
                result, data = m1m3.GetSampleIMSData()
                InTolerance("SAL %s m1m3_IMSData.XPosition" % row[0], data.XPosition, row[1], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_IMSData.YPosition" % row[0], data.YPosition, row[2], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_IMSData.ZPosition" % row[0], data.ZPosition, row[3], POSITION_TOLERANCE)
                InTolerance("SAL %s m1m3_IMSData.XRotation" % row[0], data.XRotation, row[4], ROTATION_TOLERANCE)
                InTolerance("SAL %s m1m3_IMSData.YRotation" % row[0], data.YRotation, row[5], ROTATION_TOLERANCE)
                InTolerance("SAL %s m1m3_IMSData.ZRotation" % row[0], data.ZRotation, row[6], ROTATION_TOLERANCE)
                
                time.sleep(15.0)
                
                result, data = m1m3.GetSampleHardpointActuatorData()
                Log("%s Start Timestamp: %0.3f" % (row[0], startTime))
                Log("%s Stop Timestamp: %0.3f" % (row[0], data.Timestamp))
                

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)
        
        # Bring mirror into Disabled state.
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def checkMotionStateEquals(self, m1m3, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False
        
    def getDatas(self, getter, time):
        result, data = getter()
        startTime = data.Timestamp
        datas = [data]
        while True:
            result, data = getter()
            if result > 0:
                if data.Timestamp - startTime > 15.0:
                    break
                else:
                    datas.append(data)
        return datas
        
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T011().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
