########################################################################
# Test Numbers: M13T-015
# Author:       CContaxis
# Description:  Active Optic Force Offsets
# Steps:
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *
import CalculateBendingModeForces

TEST_FORCE = 222.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 0.1
TEST_SAMPLES_TO_AVERAGE = 10
WAIT_UNTIL_TIMEOUT = 300

class M13T014:
    def Run(self, m1m3, sim, efd):
        Header("M13T-014: Active Optic Force Offsets")
        
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

        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)

        # Wait a bit
        time.sleep(2.0)

        # Enable hardpoint corrections
        m1m3.EnableHardpointCorrections()

        # Wait a bit more
        time.sleep(2.0)
        
        # Prepare force data
        bm = [0] * 22
        xIndex = 0
        yIndex = 0
        sIndex = 0
        
        bmTests = [
            [5.00, 3.00, 1.50, 0.50, 0.10, 0.20, 0.05, 0.60, 0.10, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [1.00, 2.00, 3.00, 0.50, 0.10, 1.00, 0.20, 0.60, 0.05, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10, 0.00, 0.00, 0.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00]
        ]

        # Iterate through all 156 force actuators
        for bm in bmTests:
            # Calculate expected forces
            targetForces = CalculateBendingModeForces.CalculateBendingModeForces(bm)

            Header("Bending Mode %s" % bm)

            # Apply bending mode
            m1m3.ApplyActiveOpticForces(targetForces)

            # Wait for bending mode forces
            time.sleep(TEST_SETTLE_TIME)

            # I hate this script
            rtn, data = m1m3.GetEventAppliedActiveOpticForces()

            # Verify forces
            for i in range(156):
                InTolerance("m1m3_logevent_AppliedActiveOpticForces.ZForces[%d]" % i, data.ZForces[i], targetForces[i], TEST_TOLERANCE)

        Header("Clear Bending Mode")

        # Clear bending mode forces
        bm = [0] * 22
        targetForces = CalculateBendingModeForces.CalculateBendingModeForces(bm)

        # Clear bending mode
        m1m3.ClearActiveOpticForces()

        # Wait for bending mode forces
        time.sleep(TEST_SETTLE_TIME)

        # I hate this script
        rtn, data = m1m3.GetEventAppliedActiveOpticForces()

        # Verify forces
        for i in range(156):
            InTolerance("m1m3_logevent_AppliedActiveOpticForces.ZForces[%d]" % i, data.ZForces[i], targetForces[i], TEST_TOLERANCE)

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)
            
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
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T014().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)