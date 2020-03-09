########################################################################
# Test Numbers: M13T-017
# Author:       CContaxis
# Description:  Active Optics Actuator Force Updates
# Steps:
# - Transition from standby to active engineering state
# - Clear active optic forces
# - Apply a set of active optic forces
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied 
# - Apply an active optic force by bending modes
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied
# - Apply an active optic force by bending modes
# - Verify the active optic forces are applied
# - Apply a set of active optic forces
# - Verify the active optic forces are applied
# - Clear active optic forces
# - Verify the active optic forces are no longer applied
# - Transition from active engineering state to standby
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *
from CalculateBendingModeForces import *

TEST_MODE = [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
TEST_FORCE = [1.2] * 156
TEST_TOLERANCE = 0.1
WAIT_UNTIL_TIMEOUT = 600

class M13T017:
    def Run(self, m1m3, sim, efd):
        Header("M13T-017: Active Optic Actuator Force Updates")
        
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
        
        time.sleep(5.0)
        
        # Clear active optic forces and verify
        m1m3.ClearActiveOpticForces()
        time.sleep(1.0)
        self.verifyForces("Clear AO Force", m1m3, [0] * 156)
        time.sleep(1.0)
        
        # Apply active optic force and verify
        m1m3.ApplyActiveOpticForces(TEST_FORCE)
        time.sleep(1.0)
        self.verifyForces("Apply AO Force by Forces", m1m3, TEST_FORCE)
        time.sleep(1.0)
        
        # Clear active optic forces and verify
        m1m3.ClearActiveOpticForces()
        time.sleep(1.0)
        self.verifyForces("Clear AO Force", m1m3, [0] * 156)
        time.sleep(1.0)
        
        # Apply active optic force by bending mode and verify
        m1m3.ApplyActiveOpticForcesByBendingModes(TEST_MODE)
        time.sleep(1.0)
        self.verifyForces("Apply AO Force by Forces", m1m3, CalculateBendingModeForces(TEST_MODE))
        time.sleep(1.0)
        
        # Clear active optic forces and verify
        m1m3.ClearActiveOpticForces()
        time.sleep(1.0)
        self.verifyForces("Clear AO Force", m1m3, [0] * 156)
        time.sleep(1.0)
        
        # Apply active optic force by bending mode and verify
        m1m3.ApplyActiveOpticForcesByBendingModes(TEST_MODE)
        time.sleep(1.0)
        self.verifyForces("Apply AO Force by Forces", m1m3, CalculateBendingModeForces(TEST_MODE))
        time.sleep(1.0)
        
        # Apply active optic force and verify
        m1m3.ApplyActiveOpticForces(TEST_FORCE)
        time.sleep(1.0)
        self.verifyForces("Apply AO Force by Forces", m1m3, TEST_FORCE)
        time.sleep(1.0)
        
        # Clear active optic forces and verify
        m1m3.ClearActiveOpticForces()
        time.sleep(1.0)
        self.verifyForces("Clear AO Force", m1m3, [0] * 156)
        time.sleep(1.0)
        
        # Transition to lowering engineering state
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
            
        # Transition to disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Transition to standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
    def verifyForces(self, preText, m1m3, zForces):
        # Get active optic forces
        result, data = m1m3.GetEventAppliedActiveOpticForces()
        
        # Validate all Z data
        for i in range(156):
            InTolerance("%s MTM1M3_logevent_AppliedActiveOpticForces.ZForces[%d]" % (preText, i), data.ZForces[i], zForces[i], TEST_TOLERANCE)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T017().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
