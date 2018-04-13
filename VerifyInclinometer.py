import time
from Utilities import *
from SALPY_m1m3 import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify inclinometer data available in all states 
#               excluding StandbyState
########################################################################

class VerifyInclinometer:
    def Run(self, m1m3, sim):
        Header("Verify Inclinometer")
        self.CheckNoInclinometer(m1m3, sim, "Standby")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        self.CheckInclinometer(m1m3, sim, "Disabled")
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "Parked")
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "Raising")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "Active")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "Lowering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "ParkedEngineering")
        m1m3.RaiseM1M3(True)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "RaisingEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "ActiveEngineering")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckInclinometer(m1m3, sim, "LoweringEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def CheckInclinometer(self, m1m3, sim, state):
        SubHeader("Verify Inclinometer: %s State Validation" % (state))
        for angle in [355, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0]:
            sim.setInclinometer(angle)
            time.sleep(0.5)
            result, data = GetSampleInclinometerData()
            InTolerance("InclinometerData.InclinometerAngle", data.InclinometerAngle, angle, 0.001)
            
    def CheckNoInclinometer(self, m1m3, sim, state):
        SubHeader("Verify No Inclinometer: %s State Validation" % (state))
        # Clear any existing sample in the queue
        result, data = m1m3.GetSampleInclinometerData() 
        time.sleep(1)
        # See if new data came in
        result, data = m1m3.GetSampleInclinometerData()
        Equal("No InclinometerData", result, -100)
        time.sleep(1)
        # Check one last time to see if new data came in
        result, data = m1m3.GetSampleInclinometerData()
        Equal("Still No InclinometerData", result, -100)
        