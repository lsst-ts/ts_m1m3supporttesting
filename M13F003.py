import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *

########################################################################
# Test Numbers: M13F-003
# Author:       CContaxis
# Description:  Verify ILC communications
########################################################################

class M13F003:
    def Run(self, m1m3, sim):
        Header("Verify ILC Communications")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        result, data = m1m3.GetEventForceActuatorInfo()
        forceActuatorInfo = data
        for index in range(156):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("FA ILC %d UniqueId Not 0" % refId, uniqueId, 0)
        result, data = m1m3.GetEventHardpointActuatorInfo()
        for index in range(6):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("HP ILC %d UniqueId Not 0" % refId, uniqueId, 0)
        result, data = m1m3.GetEventHardpointMonitorInfo()
        for index in range(6):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("HM ILC %d UniqueId Not 0" % refId, uniqueId, 0)
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
        
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156
        for row in forceActuatorTable:
            index = row[forceActuatorTableIndexIndex]
            id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]
            Header("Verify Force Actuator %d Commands and Telemetry" % id)
            x = self.GetIndex(forceActuatorInfo.XDataReferenceId, id)
            y = self.GetIndex(forceActuatorInfo.YDataReferenceId, id)
            z = index

            if x != -1:
                xForces[x] = 10.0
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                primaryCylinderForce = -10.0
                secondaryCylinderForce = 10.0 * math.sqrt(2)
                if orientation == '-X':
                    secondaryCylinderForce = -secondaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                time.sleep(1)
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.ClearOffsetForces()
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                time.sleep(1)
                xForces[x] = 0
                SubHeader("Force Actuator %d X Force Removed" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                
            if y != -1:
                yForces[y] = 10
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                primaryCylinderForce = -10.0
                secondaryCylinderForce = 10.0 * math.sqrt(2)
                if orientation == '-Y':
                    secondaryCylinderForce = -secondaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                time.sleep(1)
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.ClearOffsetForces()
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                time.sleep(1)
                yForces[y] = 0
                SubHeader("Force Actuator %d Y Force Removed" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
            zForces[z] = 10
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)
            primaryCylinderForce = 10.0
            secondaryCylinderForce = 0.0
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            time.sleep(1)
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            m1m3.ClearOffsetForces()
            sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
            time.sleep(1)
            zForces[z] = 0            
            SubHeader("Force Actuator %d Z Force Removed" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)

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
        
    def VerifyForceActuators(self, m1m3, sim, xForces, yForces, zForces):
        result, data = m1m3.GetSampleForceActuatorData()
        for i in range(12):
            InTolerance("ForceActuatorData.XForce[%d]" % i, data.XForce[i], xForces[i], 0.1)
        for i in range(100):
            InTolerance("ForceActuatorData.YForce[%d]" % i, data.YForce[i], yForces[i], 0.1)
        for i in range(156):
            InTolerance("ForceActuatorData.ZForce[%d]" % i, data.ZForce[i], zForces[i], 0.1)
            
    def GetIndex(self, data, item):
        index = 0
        for value in data:
            if value == item:
                return index
            index += 1
        return -1
        