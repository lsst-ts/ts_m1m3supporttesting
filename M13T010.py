########################################################################
# Test Numbers: M13T-010  
# Author:       AClements
# Description:  Position System Requirements
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm and ΘX, ΘY, & ΘZ are 0.014 degrees:
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
#   +ΘX, 0, 0
#   -ΘX, 0, 0
#   0, +ΘY, 0
#   0, -ΘY, 0
#   0, 0, +ΘZ
#   0, 0, -ΘZ
#   +ΘX, +ΘY, 0
#   -ΘX, +ΘY, 0
#   +ΘX, -ΘY, 0
#   -ΘX, -ΘY, 0
#   +ΘX, 0, +ΘZ
#   -ΘX, 0, +ΘZ
#   +ΘX, 0, -ΘZ
#   -ΘX, 0, -ΘZ
#   0, +ΘY, +ΘZ
#   0, +ΘY, -ΘZ
#   0, -ΘY, +ΘZ
#   0, -ΘY, -ΘZ
# - Repeat Matrix 2 more times
# - Transition back to standby
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb
import time

# edit the defined reference positions as needed.
REFERENCE_X_POSITION = -0.000667375
REFERENCE_Y_POSITION = 0.00133325
REFERENCE_Z_POSITION = 0.0143788
REFERENCE_X_ROTATION = -0.0000395131
REFERENCE_Y_ROTATION = -0.000000892629
REFERENCE_Z_ROTATION = 0.000351054

TRAVEL_POSITION = 0.001
TRAVEL_ROTATION = 0.014
POSITION_TOLERANCE = 0.001221
ROTATION_TOLERANCE = 0.01
WAIT_UNTIL_TIMEOUT = 600

class M13T010:
    def TestHardpointsMotion(self, m1m3):
        MotionStateArray = m1m3.GetEventHardpointActuatorState()[1].MotionState
        for i in range(0, 6):
            if MotionStateArray[i] != 2 and MotionStateArray[i] != 3:
                return False;
        return True

    def TestHardpointsAtRest(self, m1m3):
        MotionStateArray = m1m3.GetEventHardpointActuatorState()[1].MotionState
        for i in range(0, 6):
            if MotionStateArray[i] != 0:
                return False;
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
        Header("M13T-010: Position System Requirements")
        
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
        
        # The martix need to be tested 3 times
        for i in range(0,3):
            ##########################################################
            # Check that mirror is in nominal/reference/0,0,0 position

            # make sure the hardpoints have stopped moving.
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            # Not sure of the best way how to check when it is settled into reference position...
            # currently checking each direction, one at a time.
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
            
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
            
            ##########################################################
            # Command the mirror to the matrix positions.  Check to make sure it reaches those positions.

            #########################
            # (X, 0, 0) to (-X, 0, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            # wait for hardpoint movement.
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            # wait for hardpoints to stop moving.
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            
            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            #########################
            # (0, Y, 0) to (0, Y, 0)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            #########################
            # (0, 0, Z) to (0, 0, Z)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZPosition(0, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
           
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZPosition(0, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
                    
            #########################
            # (X, Y, 0) to (-X, -Y, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(-X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(-X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(-X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(-X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            #########################
            # (X, 0, Z) to (-X, 0, -Z) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(-X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(-X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            #########################
            # (0, Y, Z) to (0, -Y, -Z) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, -Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, -Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, -Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, -Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, -Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, -Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            #########################
            # (ΘX, 0, 0) to (-ΘX, 0, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION + TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(ΘX, 0, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION - TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(-ΘX, 0, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            
            #########################
            # (0, ΘY, 0) to (0, ΘY, 0)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            
            #########################
            # (0, 0, ΘZ) to (0, 0, ΘZ)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION + TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZRotation(0, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION - TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZRotation(0, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            
            #########################
            # (ΘX, ΘY, 0) to (-ΘX, -ΘY, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION + TRAVEL_ROTATION, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(ΘX, ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(ΘX, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(ΘX, ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YRotation(ΘX, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION + TRAVEL_ROTATION, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(ΘX, -ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(ΘX, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(ΘX, -ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YRotation(ΘX, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION - TRAVEL_ROTATION, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(-ΘX, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(-ΘX, ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YRotation(-ΘX, ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION - TRAVEL_ROTATION, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, REFERENCE_Z_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, -ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(-ΘX, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(-ΘX, -ΘY, 0)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YRotation(-ΘX, -ΘY, 0)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            
            #########################
            # (ΘX, 0, ΘZ) to (-ΘX, 0, -ΘZ) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION + TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION + TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, ΘZ)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(ΘX, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(ΘX, 0, ΘZ)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(ΘX, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION + TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION - TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, -ΘZ)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(ΘX, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(ΘX, 0, -ΘZ)", data.XRotation, REFERENCE_X_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(ΘX, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION - TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION + TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, ΘZ)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(-ΘX, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(-ΘX, 0, ΘZ)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(-ΘX, 0, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION - TRAVEL_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION - TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, -ΘZ)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(-ΘX, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XRotation(-ΘX, 0, -ΘZ)", data.XRotation, REFERENCE_X_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(-ΘX, 0, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            
            #########################
            # (0, ΘY, ΘZ) to (0, -ΘY, -ΘZ) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, REFERENCE_Z_ROTATION + TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, ΘZ)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, ΘY, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, ΘY, ΘZ)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(0, ΘY, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, REFERENCE_Z_ROTATION - TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, -ΘZ)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, ΘY, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, ΘY, -ΘZ)", data.YRotation, REFERENCE_Y_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(0, ΘY, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, REFERENCE_Z_ROTATION + TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, ΘZ)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, -ΘY, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, -ΘY, ΘZ)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(0, -ΘY, ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION + TRAVEL_ROTATION, ROTATION_TOLERANCE)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, REFERENCE_Z_ROTATION - TRAVEL_ROTATION)
            self.WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            self.WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, -ΘZ)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZRotation(0, -ΘY, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YRotation(0, -ΘY, -ΘZ)", data.YRotation, REFERENCE_Y_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZRotation(0, -ΘY, -ΘZ)", data.ZRotation, REFERENCE_Z_ROTATION - TRAVEL_ROTATION, ROTATION_TOLERANCE)

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
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T010().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
