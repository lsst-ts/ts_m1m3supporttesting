#!/usr/bin/env python3.8

# This file is part of M1M3 SS test suite.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

########################################################################
# Test Numbers: M13T-018
# Author:       CContaxis
# Description:  Bump test raised
# Steps:
# - Transition from standby to active engineering state
# - Perform the following steps for each force actuator and each of its force component (X or Y and Z)
#   - Apply a pure force offset
#   - Verify the pure force is being applied
#   - Verify the pure force is being measured
#   - Clear offset forces
#   - Verify the pure force is no longer being applied
#   - Verify the pure force is no longer being measured
#   - Apply a pure -force offset
#   - Verify the pure -force is being applied
#   - Verify the pure -force is being measured
#   - Clear offset forces
#   - Verify the pure -force is no longer being applied
#   - Verify the pure -force is no longer being measured
# - Transition from active engineering state to standby
########################################################################

from ForceActuatorTable import *
from MTM1M3Test import *

from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest

TEST_FORCE = 222.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10

class M13T018(MTM1M3Test):
    async def _test_actuator(self, fa_type, fa_id):
        # Prepare force data
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156

        self.printHeader(f"Verify Force Actuator {self.id} {fa_type}")

    async def test_bump_raised(self):
        self.printHeader("M13T-018: Bump Test Raised")

        await self.startup(MTM1M3Test.DetailedState.ACTIVEENGINEERING)
        
        # Disable hardpoint corrections to keep forces good
        await self.m1m3.cmd_disableHardpointCorrections.start()
        
        await self.runActuators(self._test_actuator)
        
        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            z = row[forceActuatorTableIndexIndex]
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

        await self.shutdown(MTM1M3.DetailedState.STANDBY)
        
if __name__ == "__main__":
    asynctest.main()
