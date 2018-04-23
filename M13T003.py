import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *

########################################################################
# Test Numbers: M13T-003
# Author:       CContaxis
# Description:  Individual hardpoint displacement test
########################################################################

class M13T003:
    def Run(self, m1m3, sim):
        Header("M13T-002: Individual Hardpoint Displacement Test")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        encoders = []
        commanded = False
        steps = 1000
        for index in range(6):
            status = 0x04
            if steps < 0:
                status = 0x08
            sim.setHPForceAndStatus(index + 1, 0, steps + index, 0)
            while True:
                result, data = m1m3.GetEventHardpointActuatorState()
                if result < 0:
                    break
            while True:
                tmp = [0] * 6
                tmp[index] = steps
                m1m3.MoveHardpointActuators(tmp)
                result, data = m1m3.GetEventHardpointActuatorState()
                Equal("Actuator %d moving" % index, data.MotionState[index], 2)
                while True:
                    result, data = m1m3.GetEventHardpointActuatorState()
                    if result == 0 and data.MotionState[index] == 0:
                        break
                sim.setHPForceAndStatus(index + 1, status, steps + index, 0)
                time.sleep(1)
                result, data = m1m3.GetEventHardpointActuatorWarning()
                if result == 0 and (data.LimitSwitch1Operated[index] or data.LimitSwitch2Operated[index]):
                    result, data = m1m3.GetSampleHardpointActuatorData()
                    encoders.append(data.Encoder[index])
                    steps = -steps
                    break
                    
        Log("Actuator 1 Encoder Limit 1: %d" % encoders[0])
        Log("Actuator 1 Encoder Limit 2: %d" % encoders[1])
        Log("Actuator 2 Encoder Limit 1: %d" % encoders[2])
        Log("Actuator 2 Encoder Limit 2: %d" % encoders[3])
        Log("Actuator 3 Encoder Limit 1: %d" % encoders[4])
        Log("Actuator 3 Encoder Limit 2: %d" % encoders[5])
        Log("Actuator 4 Encoder Limit 1: %d" % encoders[6])
        Log("Actuator 4 Encoder Limit 2: %d" % encoders[7])
        Log("Actuator 5 Encoder Limit 1: %d" % encoders[8])
        Log("Actuator 5 Encoder Limit 2: %d" % encoders[9])
        Log("Actuator 6 Encoder Limit 1: %d" % encoders[10])
        Log("Actuator 6 Encoder Limit 2: %d" % encoders[11])
        
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
        