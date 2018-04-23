import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *

########################################################################
# Test Numbers: M13F-005
# Author:       CContaxis
# Description:  Verify bump test
########################################################################

class M13F005:
    def Run(self, m1m3, sim):
        testForce = 222.0
        Header("Verify Bump Test")
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
                xForces[x] = testForce
                m1m3.Flush(m1m3.GetEventAppliedForces)
                m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
                time.sleep(0.1)
                primaryCylinderForce = -testForce
                secondaryCylinderForce = testForce * math.sqrt(2)
                if orientation == '-X':
                    secondaryCylinderForce = -secondaryCylinderForce
                    primaryCylinderForce = -primaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], testForce, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], testForce, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
                time.sleep(1)
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.Flush(m1m3.GetEventAppliedForces)
                m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
                m1m3.ClearOffsetForces()
                m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
                time.sleep(0.1)
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
                yForces[y] = testForce
                m1m3.Flush(m1m3.GetEventAppliedForces)
                m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
                time.sleep(0.1)
                primaryCylinderForce = -testForce
                secondaryCylinderForce = testForce * math.sqrt(2)
                if orientation == '-Y':
                    secondaryCylinderForce = -secondaryCylinderForce
                    primaryCylinderForce = -primaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], testForce, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], testForce, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
                time.sleep(1)
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                m1m3.Flush(m1m3.GetEventAppliedForces)
                m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
                m1m3.ClearOffsetForces()
                m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
                time.sleep(0.1)
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
            m1m3.Flush(m1m3.GetEventAppliedForces)
            m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)
            m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
            time.sleep(0.1)
            primaryCylinderForce = testForce
            secondaryCylinderForce = 0.0
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            result, data = m1m3.GetEventAppliedForces()
            if x != -1:
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], testForce, 0.1)
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            if y != -1:
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], testForce, 0.1)
            result, data = m1m3.GetEventAppliedCylinderForces()
            if x != -1 or y != -1:
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
            InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
            time.sleep(1)
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            m1m3.Flush(m1m3.GetEventAppliedForces)
            m1m3.Flush(m1m3.GetEventAppliedOffsetForces)
            m1m3.ClearOffsetForces()
            m1m3.Flush(m1m3.GetEventAppliedCylinderForces)
            time.sleep(0.1)
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
        