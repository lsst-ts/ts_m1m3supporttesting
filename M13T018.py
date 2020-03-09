########################################################################
# Test Numbers: M13T-018
# Author:       CContaxis
# Description:  Bump test raised
# Steps:
# - Transition from standby to active engineering state
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
# - Transition from active engineering state to standby
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

class M13T018:
    def Run(self, m1m3, sim, efd):
        Header("M13T-018: Bump Test Raised")
        
        # Transition to disabled state
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Transition to parked state
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Transition to raising engineering state
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", 600, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        
        # Disable hardpoint corrections to keep forces good
        m1m3.DisableHardpointCorrections()
        
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
            
            # Get pre application force
            datas = self.SampleForceActuators(m1m3)
            preX = 0.0
            preY = 0.0
            if x != -1:
                preX = Average(datas, lambda d: d.XForce[x])
            if y != -1:
                preY = Average(datas, lambda d: d.YForce[y])
            preZ = Average(datas, lambda d: d.ZForce[z])

            # If the current actuator has X data available, test it
            if x != -1:
                # Set the commanded X force
                xForces[x] = TEST_FORCE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +X AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +X AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +X ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX + TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +X ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Clear offset forces
                xForces[x] = 0.0
                m1m3.ClearOffsetForces()
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +X0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +X0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +X0 ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
                InTolerance("FA%03d +X0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Set the commanded X force
                xForces[x] = -TEST_FORCE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -X AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -X AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d -X ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX - TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -X ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Clear offset forces
                xForces[x] = 0.0
                m1m3.ClearOffsetForces()
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -X0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -X0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d -X0 ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
                InTolerance("FA%03d -X0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)
                
            # If the current actuator has Y data available, test it
            if y != -1:
                # Set the commanded Y force
                yForces[y] = TEST_FORCE

                # Apply the Y only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +Y AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +Y ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY + TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d +Y ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Clear offset forces
                yForces[y] = 0.0
                m1m3.ClearOffsetForces()
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d +Y0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d +Y0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +Y0 ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
                InTolerance("FA%03d +Y0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Set the commanded Y force
                yForces[y] = -TEST_FORCE

                # Apply the Y only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -Y AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], -TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -Y AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d -Y ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY - TEST_FORCE, TEST_TOLERANCE)
                InTolerance("FA%03d -Y ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

                # Clear offset forces
                yForces[y] = 0.0
                m1m3.ClearOffsetForces()
                
                # Verify the applied offset forces match the expected value
                result, data = m1m3.GetEventAppliedOffsetForces()
                InTolerance("FA%03d -Y0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
                InTolerance("FA%03d -Y0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d -Y0 ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
                InTolerance("FA%03d -Y0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)
            
            # Set the commanded Z force
            zForces[z] = TEST_FORCE

            # Apply the Z only offset force
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)

            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("FA%03d +Z AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], TEST_FORCE, TEST_TOLERANCE)                
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d +Z ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
            InTolerance("FA%03d +Z ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ + TEST_FORCE, TEST_TOLERANCE)

            # Clear offset forces
            zForces[z] = 0.0
            m1m3.ClearOffsetForces()
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("FA%03d +Z0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d +Z0 ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z0 ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
            InTolerance("FA%03d +Z0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)

            # Set the commanded Z force
            zForces[z] = -TEST_FORCE

            # Apply the Z only offset force
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)

            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("FA%03d -Z AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], -TEST_FORCE, TEST_TOLERANCE)                
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d -Z ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
            InTolerance("FA%03d -Z ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ - TEST_FORCE, TEST_TOLERANCE)

            # Clear offset forces
            zForces[z] = 0.0
            m1m3.ClearOffsetForces()
            
            # Verify the applied offset forces match the expected value
            result, data = m1m3.GetEventAppliedOffsetForces()
            if x != -1:
                InTolerance("FA%03d -Z0 AppliedOffsetForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z0 AppliedOffsetForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z0 AppliedOffsetForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)                
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d -Z0 ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda d: d.XForce[x]), preX, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z0 ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda d: d.YForce[y]), preY, TEST_TOLERANCE)
            InTolerance("FA%03d -Z0 ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda d: d.ZForce[z]), preZ, TEST_TOLERANCE)
        
        # Transition to lowering engineering state
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", 600, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        
        # Transition to disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Transition to standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
    def SampleForceActuators(self, m1m3):
        # Get force actuator data
        datas = []
        while len(datas) < TEST_SAMPLES_TO_AVERAGE:
            result, data = m1m3.GetSampleForceActuatorData()
            if result >= 0:
                datas.append(data)
        return datas
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T018().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)