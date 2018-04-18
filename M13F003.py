import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *

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
        xIndex = 0
        yIndex = 0
        sIndex = 0
        for row in forceActuatorTable:
            index = row[forceActuatorTableIndexIndex]
            id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]
            x = -1
            y = -1
            s = -1
            z = index
            if orientation in ['+X', '-X']:
                x = xIndex
                s = sIndex
                xIndex += 1
                sIndex += 1
            if orientation in ['+Y', '-Y']:
                y = yIndex
                s = sIndex
                yIndex += 1
                sIndex += 1

            Header("Verify Force Actuator %d Commands and Telemetry" % id)

            if x != -1:
                xForces[x] = 10.0
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                primaryCylinderForce = -10.0
                secondaryCylinderForce = 10.0 * math.sqrt(2)
                if orientation == '-X':
                    secondaryCylinderForce = -secondaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 10.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 10.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], secondaryCylinderForce, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], primaryCylinderForce, 0.1)
                time.sleep(1)
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.ClearOffsetForces()
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
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
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 10.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 10.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], secondaryCylinderForce, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], primaryCylinderForce, 0.1)
                time.sleep(1)
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.ClearOffsetForces()
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
                time.sleep(1)
                yForces[y] = 0
                SubHeader("Force Actuator %d Y Force Removed" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
            zForces[z] = 10
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)
            primaryCylinderForce = 10.0
            secondaryCylinderForce = 0.0
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            result, data = m1m3.GetEventAppliedForces()
            if x != -1:
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 10.0, 0.1)
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 10.0, 0.1)
            result, data = m1m3.GetEventAppliedCylinderForces()
            if x != -1 or y != -1:
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
            InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], primaryCylinderForce, 0.1)
            time.sleep(1)
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            m1m3.ClearOffsetForces()
            sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
            result, data = m1m3.GetEventAppliedForces()
            if x != -1:
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
            result, data = m1m3.GetEventAppliedCylinderForces()
            if x != -1 or y != -1:
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
            InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
            time.sleep(1)
            zForces[z] = 0            
            SubHeader("Force Actuator %d Z Force Removed" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
        for row in hardpointActuatorTable:
            index = row[hardpointActuatorTableIndexIndex]
            id = row[hardpointActuatorTableIDIndex]
            
            Header("Verify Hardpoint Actuator %d Commands and Telemetry" % id)
            
            sim.setHPForceAndStatus(id, 0, 0, 0)
            time.sleep(1)
            result, preStepData = m1m3.GetSampleHardpointActuatorData()
            steps = [0] * 6
            steps[index] = 8
            m1m3.MoveHardpointActuators(steps)
            sim.setHPForceAndStatus(id, 0, 10, 100)
            time.sleep(1)
            result, postStepData = m1m3.GetSampleHardpointActuatorData()
            NotEqual("Hardpoint Actuator %d Encoder Changed" % id, postStepData.Encoder[index], preStepData.Encoder[index])
            NotEqual("Hardpoint Actuator %d Force Changed" % id, postStepData.MeasuredForce[index], preStepData.MeasuredForce[index])
            sim.setHPForceAndStatus(id, 0, 0, 0)
            

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
        