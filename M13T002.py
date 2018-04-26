########################################################################
# Test Numbers: M13T-002
# Author:       CContaxis
# Description:  Bump test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an X component
#     - Apply a pure X force offset
#     - Verify the pure X force is being applied
#     - Verify the pure X force is being measured
#     - Clear offset forces
#     - Verify the pure X force is no longer being applied
#     - Verify the pure X force is no longer being measured
#   - If the force actuator has an Y component
#     - Apply a pure Y force offset
#     - Verify the pure Y force is being applied
#     - Verify the pure Y force is being measured
#     - Clear offset forces
#     - Verify the pure Y force is no longer being applied
#     - Verify the pure Y force is no longer being measured
#   - Apply a pure X force offset
#   - Verify the pure Z force is being applied
#   - Verify the pure Z force is being measured
#   - Clear offset forces
#   - Verify the pure Z force is no longer being applied
#   - Verify the pure Z force is no longer being measured
# - Transition from parked engineering state to standby
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

testForce = 222.0

class M13T002:
    def Run(self, m1m3, sim, efd):
        Header("M13T-002: Bump Test")
        
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
        
        # Prepare force data
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156
        xIndex = 0
        yIndex = 0
        sIndex = 0
        
        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            index = row[forceActuatorTableIndexIndex]
            id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]
            x = -1        # X index for data access, if -1 no X data available
            y = -1        # Y index for data access, if -1 no Y data available
            s = -1        # S (Secondary Cylinder) index for data access, if -1 no S data available
            z = index     # Z index for data access, all force actuators have Z data
            
            # Set the X and S index if applicable
            if orientation in ['+X', '-X']:
                x = xIndex
                s = sIndex
                xIndex += 1
                sIndex += 1
                
            # Set the Y and S index if applicable
            if orientation in ['+Y', '-Y']:
                y = yIndex
                s = sIndex
                yIndex += 1
                sIndex += 1

            Header("Verify Force Actuator %d Commands and Telemetry" % id)

            # If the current actuator has X data available, test it
            if x != -1:
                # Set the commanded X force
                xForces[x] = testForce

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Wait a bit before setting the simulator
                time.sleep(1.0)
                
                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce = -testForce
                secondaryCylinderForce = testForce * math.sqrt(2)
                if orientation == '-X':
                    secondaryCylinderForce = -secondaryCylinderForce
                    primaryCylinderForce = -primaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], testForce, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], testForce, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(1.0)
                
                # Check all force actuators
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()
                
                # Wait a bit before setting the simulator
                time.sleep(1)
                
                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(1)
                
                # Check all force actuators
                xForces[x] = 0
                SubHeader("Force Actuator %d X Force Removed" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
                
            # If the current actuator has Y data available, test it
            if y != -1:
                # Set the commanded Y force
                yForces[y] = testForce
                
                # Apply offset forces
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Wait a bit before setting the simulator
                time.sleep(0.1)
                
                # Set the simulated force actuator's load cells to the correct value
                primaryCylinderForce = -testForce
                secondaryCylinderForce = testForce * math.sqrt(2)
                if orientation == '-Y':
                    secondaryCylinderForce = -secondaryCylinderForce
                    primaryCylinderForce = -primaryCylinderForce
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], testForce, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], testForce, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(1)
                
                # Check all force actuators
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()

                # Wait a bit before setting the simulator
                time.sleep(0.1)
                
                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
                InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
                InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
                InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(1)
                
                # Check all force actuators
                yForces[y] = 0
                SubHeader("Force Actuator %d Y Force Removed" % id)
                self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
            # Set the commanded Z force
            zForces[z] = testForce
            
            # Apply offset forces
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)

            # Wait a bit before setting the simulator
            time.sleep(0.1)
            
            # Set the simulated force actuator's load cells to the correct value
            primaryCylinderForce = testForce
            secondaryCylinderForce = 0.0
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], testForce, 0.1)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], testForce, 0.1)
            
            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
            InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), 0.1)
            
            # Wait a bit before checking all force actuator forces (positive and negative testing) 
            time.sleep(1)
            
            # Check all force actuators
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
            # Clear offset forces
            m1m3.ClearOffsetForces()
            
            # Wait a bit before setting the simulator
            time.sleep(0.1)
            
            # Set the simulated force actuator's load cells to the correct value
            sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("AppliedForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("AppliedForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("AppliedOffsetForces.XForces[%d]" % x, data.XForces[x], 0.0, 0.1)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("AppliedOffsetForces.YForces[%d]" % y, data.YForces[y], 0.0, 0.1)
            InTolerance("AppliedOffsetForces.ZForces[%d]" % z, data.ZForces[z], 0.0, 0.1)

            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("AppliedCylinderForces.SecondaryCylinderForces[%d]" % s, data.SecondaryCylinderForces[s], 0.0, 0.1)
            InTolerance("AppliedCylinderForces.PrimaryCylinderForces[%d]" % z, data.PrimaryCylinderForces[z], 0.0, 0.1)
            
            # Wait a bit before checking all force actuator forces (positive and negative)
            time.sleep(1)
            
            # Check all force actuators
            zForces[z] = 0            
            SubHeader("Force Actuator %d Z Force Removed" % id)
            self.VerifyForceActuators(m1m3, sim, xForces, yForces, zForces)
            
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
        
    def VerifyForceActuators(self, m1m3, sim, xForces, yForces, zForces):
        # Get force actuator data
        result, data = m1m3.GetSampleForceActuatorData()
        # Validate all X data
        for i in range(12):
            InTolerance("ForceActuatorData.XForce[%d]" % i, data.XForce[i], xForces[i], 0.1)
        # Validate all Y data
        for i in range(100):
            InTolerance("ForceActuatorData.YForce[%d]" % i, data.YForce[i], yForces[i], 0.1)
        # Validate all Z data
        for i in range(156):
            InTolerance("ForceActuatorData.ZForce[%d]" % i, data.ZForce[i], zForces[i], 0.1)
            
    def GetIndex(self, data, item):
        index = 0
        for value in data:
            if value == item:
                return index
            index += 1
        return -1
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    Shutdown(m1m3, sim, efd)
    M13T002().Run(m1m3, sim, efd)