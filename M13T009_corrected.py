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

TRAVEL_POSITION = 0.00613
POS_Z_TRAVEL_POSITION = 0.00407
NEG_Z_TRAVEL_POSITION = 0.00557
POSITION_TOLERANCE = 0.000008
ROTATION_TOLERANCE = 0.00000209
WAIT_UNTIL_TIMEOUT = 600
LOAD_PATH_FORCE = 0.0
LOAD_PATH_TOLERANCE = 0.0

class M13T009:

    def TestHardpointsMotion(self, m1m3):
        MotionStateArray = m1m3.GetEventHardpointActuatorState()[1].MotionState
        for i in range(0, 6):
            if MotionStateArray[i] != 2 and MotionStateArray[i] != 3:
                return False
        return True

    def TestHardpointsAtRest(self, m1m3):
        MotionStateArray = m1m3.GetEventHardpointActuatorState()[1].MotionState
        for i in range(0, 6):
            if MotionStateArray[i] != 0:
                return False
        return True
        
    def WaitUntilHardpointsMotion(self, topic, timeout, m1m3):
        start = time.time()
        timedout = False
        while not self.TestHardpointsMotion(m1m3):
            time.sleep(0.1)
            if time.time() - start >= timeout:
                timedout = True
                break
        message = "WaitUntil %s or %0.3f" % (topic, timeout)
        return Result(message, not timedout)

    def WaitUntilHardpointsAtRest(self, topic, timeout, m1m3):
        start = time.time()
        timedout = False
        while not self.TestHardpointsAtRest(m1m3):
            time.sleep(0.1)
            if time.time() - start >= timeout:
                timedout = True
                break
        message = "WaitUntil %s or %0.3f" % (topic, timeout)
        return Result(message, not timedout)

    def Run(self, m1m3, sim, efd):
        Header("M13T-009: Mirror Support System Active Motion Range")
        
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
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedState)
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
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)

        # make sure the HardpointCorrection is disabled.
        m1m3.DisableHardpointCorrections(True)
        
        time.sleep(5.0)
        
        # confirm mirror at reference position.
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL MTM1M3_HardpointActuatorData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL MTM1M3_IMSData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        ##########################################################
        # Command the mirror to the matrix positions.  Check to make sure it reaches those positions.
            
        testTable = [
            ["(+X, 0, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(-X, 0, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + POS_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION -NEG_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(+X, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(+X, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(-X, +Y, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(-X, -Y, 0, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(+X, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + POS_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(+X, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - NEG_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(-X, 0, +Z, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + POS_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(-X, 0, -Z, 0, 0, 0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - NEG_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, +Y, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION + POS_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, +Y, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION - NEG_Z_TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, -Y, +Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
            ["(0, -Y, -Z, 0, 0, 0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION],
        ]
            
        for row in testTable:
            rtn, data = m1m3.GetEventHardpointActuatorState()
            m1m3.PositionM1M3(row[1], row[2], row[3], row[4], row[5], row[6])
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Moving" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x != 0))
            WaitUntil("SAL %s MTM1M3_HardpointActuatorState.MotionState Standby" % row[0], WAIT_UNTIL_TIMEOUT, lambda: self.checkMotionStateEquals(m1m3, lambda x: x == 0))
            
            time.sleep(3.0)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.XPosition" % row[0], data.XPosition, row[1], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.YPosition" % row[0], data.YPosition, row[2], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.ZPosition" % row[0], data.ZPosition, row[3], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.XRotation" % row[0], data.XRotation, row[4], ROTATION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.YRotation" % row[0], data.YRotation, row[5], ROTATION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.ZRotation" % row[0], data.ZRotation, row[6], ROTATION_TOLERANCE)

            # Verify there are no unintended load paths.
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.XForce" % row[0], data.Fx, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.YForce" % row[0], data.Fy, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.ZForce" % row[0], data.Fz, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.XMoment" % row[0], data.Mx, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.YMoment" % row[0], data.My, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
            InTolerance("SAL %s MTM1M3_HardpointActuatorData.ZMoment" % row[0], data.Mz, LOAD_PATH_FORCE, LOAD_PATH_TOLERANCE)
                
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL %s MTM1M3_IMSData.XPosition" % row[0], data.XPosition, row[1], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_IMSData.YPosition" % row[0], data.YPosition, row[2], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_IMSData.ZPosition" % row[0], data.ZPosition, row[3], POSITION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_IMSData.XRotation" % row[0], data.XRotation, row[4], ROTATION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_IMSData.YRotation" % row[0], data.YRotation, row[5], ROTATION_TOLERANCE)
            InTolerance("SAL %s MTM1M3_IMSData.ZRotation" % row[0], data.ZRotation, row[6], ROTATION_TOLERANCE)

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
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
    M13T009().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
