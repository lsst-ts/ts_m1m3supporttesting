import time
from Utilities import *
from SALPY_m1m3 import *
from HardpointActuatorTable import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify hardpoint actuator data available in all states 
#               excluding StandbyState
########################################################################

class VerifyHardpointActuators:
    def Run(self, m1m3, sim):
        Header("Verify Hardpoint Actuators")
        self.CheckNoHardpointActuators(m1m3, sim, "Standby")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        self.CheckHardpointActuators(m1m3, sim, "Disabled")
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "Parked")
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "Raising")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "Active")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "Lowering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "ParkedEngineering")
        m1m3.RaiseM1M3(True)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "RaisingEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "ActiveEngineering")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckHardpointActuators(m1m3, sim, "LoweringEngineering")
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
        
    def CheckHardpointActuators(self, m1m3, sim, state):
        SubHeader("Verify Hardpoint Actuators: %s State Validation" % (state))
        for row in hardpointActuatorTable:
            for otherRow in hardpointActuatorTable:
                sim.setHPForceAndStatus(otherRow[hardpointActuatorTableIDIndex], 0, 0, 0)
            sim.setHPForceAndStatus(otherRow[hardpointActuatorTableIDIndex], 0, -1, 1)
            time.sleep(1.0)
            result, data = m1m3.GetSampleHardpointActuatorData()
            for otherRow in hardpointActuatorTable:
                pIndex = otherRow[hardpointActuatorTableIndexIndex]
                expected = 0
                if otherRow[hardpointActuatorTableIDIndex] == row[hardpointActuatorTableIDIndex]:
                    expected = 1
                Equal("HardpointActuatorData.Encoder[%d]" % pIndex, data.Encoder[pIndex], -expected)
                InTolerance("HardpointActuatorData.MeasuredForce[%d]" % pIndex, data.MeasuredForce[pIndex], float(expected), 0.001)
            
    def CheckNoHardpointActuators(self, m1m3, sim, state):
        SubHeader("Verify No Hardpoint Actuators: %s State Validation" % (state))
        # Clear any existing sample in the queue
        result, data = m1m3.GetSampleHardpointActuatorData() 
        time.sleep(1)
        # See if new data came in
        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("No HardpointActuatorData", result, -100)
        time.sleep(1)
        # Check one last time to see if new data came in
        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("Still No HardpointActuatorData", result, -100)
        