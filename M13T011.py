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
REFERENCE_X_POSITION = -0.000667375
REFERENCE_Y_POSITION = 0.00133325
REFERENCE_Z_POSITION = 0.0143788
REFERENCE_X_ROTATION = -0.0000395131
REFERENCE_Y_ROTATION = -0.000000892629
REFERENCE_Z_ROTATION = 0.000351054

TRAVEL_POSITION = 0.001
POSITION_TOLERANCE = 0.001221
WAIT_UNTIL_TIMEOUT = 3 #TODO: should be 600 when done testing

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
            ##########################################################
            # Check that mirror is in nominal/reference/0,0,0 position
            
            # make sure the hardpoints have stopped moving.
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
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
            
            ##########################################################
            # Command the mirror to the matrix positions.  Check to make sure it reaches those positions.

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (X, 0, 0) to (-X, 0, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            # wait for hardpoint movement.
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            # wait for hardpoints to stop moving.
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (0, Y, 0) to (0, Y, 0)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (0, 0, Z) to (0, 0, Z)
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZPosition(0, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
           
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.ZPosition(0, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
                    
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (X, Y, 0) to (-X, -Y, 0) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(-X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(-X, Y, 0)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(-X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, -Y, 0)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.YPosition(-X, -Y, 0)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (X, 0, Z) to (-X, 0, -Z) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(-X, 0, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.XPosition(-X, 0, -Z)", data.XPosition, REFERENCE_X_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(-X, 0, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            #########################
            # (0, Y, Z) to (0, -Y, -Z) 
            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, Y, -Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, Y, -Z)", data.YPosition, REFERENCE_Y_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, -Y, Z)", data.ZPosition, REFERENCE_Z_POSITION + TRAVEL_POSITION, POSITION_TOLERANCE)

            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

            m1m3.PositionM1M3(REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
            WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
            result, data = m1m3.GetSampleHardpointActuatorData()
            InTolerance("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, -Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            result, data = m1m3.GetSampleIMSData()
            InTolerance("SAL m1m3_IMSData.YPosition(0, -Y, -Z)", data.YPosition, REFERENCE_Y_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            InTolerance("SAL m1m3_IMSData.ZPosition(0, -Y, -Z)", data.ZPosition, REFERENCE_Z_POSITION - TRAVEL_POSITION, POSITION_TOLERANCE)
            
            # wait 15 seconds so the control can record telemetry
            time.sleep(15)

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
    M13T011().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
