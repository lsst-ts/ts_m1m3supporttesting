########################################################################
# Test Numbers: M13T-021  
# Author:       CContaxis
# Description:  Mirror Support Lifting and Parking
# Steps:
# - Transition from standby to parked engineering state
# - Raise Mirror
# - Verify raise time is < 300s
# - Verify HP shows mirror at the reference position
# - Verify IMS shows mirror at the reference position
# - Lower Mirror
# - Verify lower time is < 300s
# - Verify lower rate is < 15mm/s
# - Transition to parked state
# - Raise Mirror
# - Verify raise time is < 300s
# - Verify HP shows mirror at the reference position
# - Verify IMS shows mirror at the reference position
# - Lower Mirror
# - Verify lower time is < 300s
# - Verify lower rate is < 15mm/s
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

TRAVEL_POSITION = 0.001
TRAVEL_ROTATION = 0.00024435
POSITION_TOLERANCE = 0.0001
ROTATION_TOLERANCE = 0.0001
WAIT_UNTIL_TIMEOUT = 600

class M13T021:
    def Run(self, m1m3, sim, efd):
        Header("M13T-021: Mirror Support Lifting and Parking")
        
        # Transition to disabled state
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to parked state
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Get start time and start position
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        startHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        startIMSZ = data.ZPosition
        
        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)
        
        # Get stop time
        result, data = m1m3.GetSampleHardpointActuatorData()
        stopTime = data.Timestamp
        stopHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        stopIMSZ = data.ZPosition
        
        time.sleep(5.0)
        
        # Verify HP at reference position
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL m1m3_HardpointActuatorData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        # Verify IMS at reference position
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL m1m3_IMSData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        # Verify raise time
        LessThanEqual("Raise Time", (stopTime - startTime), 300)         
        
        time.sleep(5.0)
        
        # Get start time and start position
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        startHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        startIMSZ = data.ZPosition
        
        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)
        
        # Get stop time
        result, data = m1m3.GetSampleHardpointActuatorData()
        stopTime = data.Timestamp
        stopHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        stopIMSZ = data.ZPosition
        
        # Verify lower time
        LessThanEqual("Lower Time", (stopTime - startTime), 300)     
        
        # Verify fall rate
        LessThanEqual("Lower Rate", -(stopIMSZ - startIMSZ) / (stopTime - startTime), 0.015)
            
        # Transition to parked state
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
       
        # Get start time and start position
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        startHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        startIMSZ = data.ZPosition
        
        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveState)
        
        # Get stop time
        result, data = m1m3.GetSampleHardpointActuatorData()
        stopTime = data.Timestamp
        stopHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        stopIMSZ = data.ZPosition
        
        time.sleep(5.0)
        
        # Verify HP at reference position
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL m1m3_HardpointActuatorData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_HardpointActuatorData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        # Verify IMS at reference position
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL m1m3_IMSData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL m1m3_IMSData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        # Verify raise time
        LessThanEqual("Raise Time", (stopTime - startTime), 300)         
        
        time.sleep(5.0)
        
        # Get start time and start position
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTime = data.Timestamp
        startHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        startIMSZ = data.ZPosition
        
        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedState)
        
        # Get stop time
        result, data = m1m3.GetSampleHardpointActuatorData()
        stopTime = data.Timestamp
        stopHPZ = data.ZPosition
        result, data = m1m3.GetSampleIMSData()
        stopIMSZ = data.ZPosition
        
        # Verify lower time
        LessThanEqual("Lower Time", (stopTime - startTime), 300)     
        
        # Verify fall rate
        LessThanEqual("Lower Rate", -(stopIMSZ - startIMSZ) / (stopTime - startTime), 0.015)
        
        # Transition to disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def checkMotionStateEquals(self, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False
        
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T021().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
