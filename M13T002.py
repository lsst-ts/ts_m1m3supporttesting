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
#     - Apply a pure -X force offset
#     - Verify the pure -X force is being applied
#     - Verify the pure -X force is being measured
#     - Clear offset forces
#     - Verify the pure -X force is no longer being applied
#     - Verify the pure -X force is no longer being measured
#   - If the force actuator has an Y component
#     - Apply a pure Y force offset
#     - Verify the pure Y force is being applied
#     - Verify the pure Y force is being measured
#     - Clear offset forces
#     - Verify the pure Y force is no longer being applied
#     - Verify the pure Y force is no longer being measured
#     - Apply a pure -Y force offset
#     - Verify the pure -Y force is being applied
#     - Verify the pure -Y force is being measured
#     - Clear offset forces
#     - Verify the pure -Y force is no longer being applied
#     - Verify the pure -Y force is no longer being measured
#   - Apply a pure Z force offset
#   - Verify the pure Z force is being applied
#   - Verify the pure Z force is being measured
#   - Clear offset forces
#   - Verify the pure Z force is no longer being applied
#   - Verify the pure Z force is no longer being measured
#   - Apply a pure -Z force offset
#   - Verify the pure -Z force is being applied
#   - Verify the pure -Z force is being measured
#   - Clear offset forces
#   - Verify the pure -Z force is no longer being applied
#   - Verify the pure -Z force is no longer being measured
# - Transition from parked engineering state to standby
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

TEST_FORCE = 222.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10

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
                xForces[x] = TEST_FORCE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, TEST_FORCE, 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +X AppliedForces.XForces[%d]" % (id, x), data.XForces[x], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +X AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +X AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +X AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d +X AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), TEST_TOLERANCE)
                InTolerance("FA%03d +X AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators("FA%03d +X" % id, m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()
                
                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +X0 AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +X0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +X0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +X0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d +X0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +X0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                xForces[x] = 0
                SubHeader("Force Actuator %d X Force Removed" % id)
                self.VerifyForceActuators("FA%03d +X0" % id, m1m3, sim, xForces, yForces, zForces)
                
                # Set the commanded X force
                xForces[x] = -TEST_FORCE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, -TEST_FORCE, 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d -X AppliedForces.XForces[%d]" % (id, x), data.XForces[x], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -X AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -X AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -X AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d -X AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), TEST_TOLERANCE)
                InTolerance("FA%03d -X AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                SubHeader("Force Actuator %d X Force Added" % id)
                self.VerifyForceActuators("FA%03d -X" % id, m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()
                
                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d -X0 AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -X0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -X0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -X0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d -X0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -X0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                xForces[x] = 0
                SubHeader("Force Actuator %d X Force Removed" % id)
                self.VerifyForceActuators("FA%03d -X0" % id, m1m3, sim, xForces, yForces, zForces)
                
            # If the current actuator has Y data available, test it
            if y != -1:
                # Set the commanded Y force
                yForces[y] = TEST_FORCE
                
                # Apply offset forces
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulated force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, TEST_FORCE, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +Y AppliedForces.YForces[%d]" % (id, y), data.YForces[y], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +Y AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d +Y AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators("FA%03d +Y" % id, m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()

                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +Y0 AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +Y0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +Y0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +Y0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d +Y0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +Y0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                yForces[y] = 0
                SubHeader("Force Actuator %d Y Force Removed" % id)
                self.VerifyForceActuators("FA%03d +Y0" % id, m1m3, sim, xForces, yForces, zForces)
                
                # Set the commanded Y force
                yForces[y] = -TEST_FORCE
                
                # Apply offset forces
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulated force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, -TEST_FORCE, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d -Y AppliedForces.YForces[%d]" % (id, y), data.YForces[y], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -Y AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -Y AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -Y AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d -Y AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], int(secondaryCylinderForce * 1000), TEST_TOLERANCE)
                InTolerance("FA%03d -Y AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                SubHeader("Force Actuator %d Y Force Added" % id)
                self.VerifyForceActuators("FA%03d -Y" % id, m1m3, sim, xForces, yForces, zForces)

                # Clear offset forces
                m1m3.ClearOffsetForces()

                # Set the simulated force actuator's load cells to the correct value
                sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d -Y0 AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -Y0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -Y0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -Y0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied cylinder forces match the expected value
                result, data = m1m3.GetEventAppliedCylinderForces()
                InTolerance("FA%03d -Y0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -Y0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
                
                # Wait a bit before checking all force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check all force actuators
                yForces[y] = 0
                SubHeader("Force Actuator %d Y Force Removed" % id)
                self.VerifyForceActuators("FA%03d -Y0" % id, m1m3, sim, xForces, yForces, zForces)
            
            # Set the commanded Z force
            zForces[z] = TEST_FORCE
            
            # Apply offset forces
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)
            
            # Set the simulated force actuator's load cells to the correct value
            primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, 0, TEST_FORCE)
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d +Z AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d +Z AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], TEST_FORCE, TEST_TOLERANCE)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d +Z AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d +Z AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], TEST_FORCE, TEST_TOLERANCE)
            
            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("FA%03d +Z AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
            
            # Wait a bit before checking all force actuator forces (positive and negative testing) 
            time.sleep(TEST_SETTLE_TIME)
            
            # Check all force actuators
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators("FA%03d +Z" % id, m1m3, sim, xForces, yForces, zForces)
            
            # Clear offset forces
            m1m3.ClearOffsetForces()
            
            # Set the simulated force actuator's load cells to the correct value
            sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d +Z0 AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d +Z0 AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d +Z0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d +Z0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)

            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("FA%03d +Z0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
            
            # Wait a bit before checking all force actuator forces (positive and negative)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check all force actuators
            zForces[z] = 0            
            SubHeader("Force Actuator %d Z Force Removed" % id)
            self.VerifyForceActuators("FA%03d +Z0" % id, m1m3, sim, xForces, yForces, zForces)
            
            # Set the commanded Z force
            zForces[z] = -TEST_FORCE
            
            # Apply offset forces
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)
            
            # Set the simulated force actuator's load cells to the correct value
            primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, 0, -TEST_FORCE)
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d -Z AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d -Z AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], -TEST_FORCE, TEST_TOLERANCE)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d -Z AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d -Z AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], -TEST_FORCE, TEST_TOLERANCE)
            
            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("FA%03d -Z AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], int(primaryCylinderForce * 1000), TEST_TOLERANCE)
            
            # Wait a bit before checking all force actuator forces (positive and negative testing) 
            time.sleep(TEST_SETTLE_TIME)
            
            # Check all force actuators
            SubHeader("Force Actuator %d Z Force Added" % id)
            self.VerifyForceActuators("FA%03d -Z" % id, m1m3, sim, xForces, yForces, zForces)
            
            # Clear offset forces
            m1m3.ClearOffsetForces()
            
            # Set the simulated force actuator's load cells to the correct value
            sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d -Z0 AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d -Z0 AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z0 AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            # If this actuator has a X force, verify it
            if x != -1:
                InTolerance("FA%03d -Z0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            # If this actuator has a Y force, verify it
            if y != -1:
                InTolerance("FA%03d -Z0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)

            # Verify the applied cylinder forces match the expected value
            result, data = m1m3.GetEventAppliedCylinderForces()
            # If this actuator has a X or Y force, verify it
            if x != -1 or y != -1:
                InTolerance("FA%03d -Z0 AppliedCylinderForces.SecondaryCylinderForces[%d]" % (id, s), data.SecondaryCylinderForces[s], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z0 AppliedCylinderForces.PrimaryCylinderForces[%d]" % (id, z), data.PrimaryCylinderForces[z], 0.0, TEST_TOLERANCE)
            
            # Wait a bit before checking all force actuator forces (positive and negative)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check all force actuators
            zForces[z] = 0            
            SubHeader("Force Actuator %d Z Force Removed" % id)
            self.VerifyForceActuators("FA%03d -Z0" % id, m1m3, sim, xForces, yForces, zForces)
            
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
        
    def VerifyForceActuators(self, preText, m1m3, sim, xForces, yForces, zForces):
        # Get force actuator data
        datas = []
        while len(datas) < TEST_SAMPLES_TO_AVERAGE:
            result, data = m1m3.GetSampleForceActuatorData()
            if result >= 0:
                datas.append(data)
        # Validate all X data
        for i in range(12):
            InTolerance("%s ForceActuatorData.XForce[%d]" % (preText, i), Average(datas, lambda x: x.XForce[i]), xForces[i], TEST_TOLERANCE)
        # Validate all Y data
        for i in range(100):
            InTolerance("%s ForceActuatorData.YForce[%d]" % (preText, i), Average(datas, lambda x: x.YForce[i]), yForces[i], TEST_TOLERANCE)
        # Validate all Z data
        for i in range(156):
            InTolerance("%s ForceActuatorData.ZForce[%d]" % (preText, i), Average(datas, lambda x: x.ZForce[i]), zForces[i], TEST_TOLERANCE)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T002().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)