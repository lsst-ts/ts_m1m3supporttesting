import time
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify force actuator data available in all states 
#               excluding StandbyState
########################################################################

class VerifyForceActuators:
    def Run(self, m1m3, sim):
        Header("Verify Force Actuators")
        self.CheckNoForceActuators(m1m3, sim, "Standby")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        self.CheckForceActuators(m1m3, sim, "Disabled")
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "Parked")
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_RaisingState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "Raising")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "Active")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "Lowering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "ParkedEngineering")
        m1m3.RaiseM1M3(True)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "RaisingEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "ActiveEngineering")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        self.CheckForceActuators(m1m3, sim, "LoweringEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
    def CheckForceActuators(self, m1m3, sim, state):
        SubHeader("Verify Force Actuators: %s State Validation" % (state))
        for row in forceActuatorTable:
            for otherRow in forceActuatorTable:
                sim.setFAForceAndStatus(otherRow[forceActuatorTableIDIndex], 0, 0, 0)
            sim.setFAForceAndStatus(row[forceActuatorTableIDIndex], 0, 1, -1)
            time.sleep(1.0)
            result, data = m1m3.GetSampleForceActuatorData()
            for otherRow in forceActuatorTable:
                pIndex = otherRow[forceActuatorTableIndexIndex]
                sIndex = forceActuatorSIndexFromZIndex[pIndex]
                expected = 0.0
                if otherRow[forceActuatorTableIDIndex] == row[forceActuatorTableIDIndex]:
                    expected = 1.0
                InTolerance("ForceActuatorData.PrimaryCylinderForce[%d]" % pIndex, data.PrimaryCylinderForce[pIndex], expected, 0.001)
                if sIndex != -1:
                    InTolerance("ForceActuatorData.SecondaryCylinderForce[%d]" % sIndex, data.SecondaryCylinderForce[sIndex], -expected, 0.001)
            
    def CheckNoForceActuators(self, m1m3, sim, state):
        SubHeader("Verify No Force Actuators: %s State Validation" % (state))
        # Clear any existing sample in the queue
        result, data = m1m3.GetSampleForceActuatorData() 
        time.sleep(1)
        # See if new data came in
        result, data = m1m3.GetSampleForceActuatorData()
        Equal("No ForceActuatorData", result, -100)
        time.sleep(1)
        # Check one last time to see if new data came in
        result, data = m1m3.GetSampleForceActuatorData()
        Equal("Still No ForceActuatorData", result, -100)
        