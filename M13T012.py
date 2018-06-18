########################################################################
# Test Numbers: M13T-012  
# Author:       AClements
# Description:  Position Repeatability After Parking
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Wait 5 seconds for everything to settle
# - Confirm Mirror in Reference Position
# - Park the miror, confirmed it has parked.
# - Take IMS measurements
# - return mirror to parked position.
# - repeat above process 5 times.
# - repeat the process for the matrix below
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm
#   +X, 0, 0 
#   -X, 0, 0
#   0,+Y, 0
#   0, -Y, 0
#   0, 0, +Z
#   0, 0, -Z
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
POSITION_TOLERANCE = 0.001221
WAIT_UNTIL_TIMEOUT = 3 #TODO: should be 600 when done testing

class M13T012:
    def RaiseM1M3(self, m1m3):
        # Raise mirror (therefore entering the Active Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ActiveEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)

    def TakeIMSMeasurements(self, m1m3, positionString, xPosition, yPosition, zPosition):
        # make sure the hardpoints have stopped moving.
        WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
        #TODO: confirm mirror is at whatever position when all IMS online
        # Not sure of the best way how to check when it is settled into reference position...
        # currently checking each direction, one at a time.
        SubHeader("Mirror at %s, taking IMS & Hardpoint measurements." % positionString)
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL m1m3_HardpointActuatorData.XPosition", data.XPosition, xPosition, POSITION_TOLERANCE)
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL m1m3_IMSData.XPosition", data.XPosition, xPosition, POSITION_TOLERANCE)
        
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL m1m3_HardpointActuatorData.YPosition", data.YPosition, yPosition, POSITION_TOLERANCE)
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL m1m3_IMSData.YPosition", data.YPosition, yPosition, POSITION_TOLERANCE)
        
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL m1m3_HardpointActuatorData.ZPosition", data.ZPosition, zPosition, POSITION_TOLERANCE)
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL m1m3_IMSData.ZPosition", data.ZPosition, zPosition, POSITION_TOLERANCE)

        Log("IMS measurements - %s " % (m1m3.GetSampleIMSData()[1]))
        SubHeader("Finished taking measurements.")

    def PositionM1M3(self, m1m3, xPosition, yPosition, zPosition):
        m1m3.PositionM1M3(xPosition, yPosition, zPosition, REFERENCE_X_ROTATION, REFERENCE_Y_ROTATION, REFERENCE_Z_ROTATION)
        # wait for hardpoint movement.
        WaitUntilHardpointsMotion("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)
        # wait for hardpoints to stop moving.
        WaitUntilHardpointsAtRest("SAL m1m3_HardpointActuatorState.MotionState", WAIT_UNTIL_TIMEOUT, m1m3)

    def LowerM1M3(self, m1m3):
        # Lower mirror, placing Control into Parked Engineering State.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)        
        
    def Run(self, m1m3, sim, efd):
        Header("M13T-012: Position Repeatability After Parking")
        
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
        
        # The steps need to be tested 5 times
        ##########################################################
        # nominal/reference/0,0,0 position
        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.TakeIMSMeasurements(m1m3, "reference position", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION)
            self.LowerM1M3(m1m3)

        #########################
        # (X, 0, 0) to (-X, 0, 0) 
        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (1.0, 0.0, 0.0)", REFERENCE_X_POSITION + TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION)
            self.LowerM1M3(m1m3)
            
        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (-1.0, 0.0, 0.0)", REFERENCE_X_POSITION - TRAVEL_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION)
            self.LowerM1M3(m1m3)
            
        #########################
        # (0, Y, 0) to (0, Y, 0)
        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (0.0, 1.0, 0.0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION + TRAVEL_POSITION, REFERENCE_Z_POSITION)
            self.LowerM1M3(m1m3)

        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (0.0, -1.0, 0.0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION - TRAVEL_POSITION, REFERENCE_Z_POSITION)
            self.LowerM1M3(m1m3)

        #########################
        # (0, 0, Z) to (0, 0, Z)
        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (0.0, 0.0, 1.0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION + TRAVEL_POSITION)
            self.LowerM1M3(m1m3)

        for i in range(0,5):
            self.RaiseM1M3(m1m3)
            self.PositionM1M3(m1m3, REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION)
            self.TakeIMSMeasurements(m1m3, "reference position + (0.0, 0.0, -1.0)", REFERENCE_X_POSITION, REFERENCE_Y_POSITION, REFERENCE_Z_POSITION - TRAVEL_POSITION)
            self.LowerM1M3(m1m3)

        #######################
        # Lower the mirror, put back in standby state.

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
    M13T012().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
