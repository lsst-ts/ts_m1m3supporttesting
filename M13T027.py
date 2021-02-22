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

# !!!! PLEASE NOTE !!!!
#
# This test requires you to switch M1M3 SS CsC configuration -
# ForceLimit[XYZ]Table.csv needs to be replaced with
# ForceLimit[XYZ]TableSmall.csv. Best is to edit on cRIO / simulator
# ForceActuatorSetting.xml and change:
#
#   <ForceLimitXTablePath>Tables/ForceLimitXTable.csv</ForceLimitXTablePath>
#   <ForceLimitYTablePath>Tables/ForceLimitYTable.csv</ForceLimitYTablePath>
#   <ForceLimitZTablePath>Tables/ForceLimitZTable.csv</ForceLimitZTablePath>
#
# to
#
#   <ForceLimitXTablePath>Tables/ForceLimitXTableSmall.csv</ForceLimitXTablePath>
#   <ForceLimitYTablePath>Tables/ForceLimitYTableSmall.csv</ForceLimitYTablePath>
#   <ForceLimitZTablePath>Tables/ForceLimitZTableSmall.csv</ForceLimitZTablePath>
#
# and restart CsC before running the test.

########################################################################
# Test Numbers: M13T-027
# Author:       CContaxis
# Description:  Force actuator limits
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an X component
#     - Apply a X force offset 15% higher than the max X limit
#     - Verify the X force is clipped
#     - Verify the limited X force is applied
#     - Verify the limited X force is being measured
#     - Apply a X force offset 15% lower than the min X limit
#     - Verify the X force is clipped
#     - Verify the limited X force is applied
#     - Verify the limited X force is being measured
#     - Clear offset forces
#   - If the force actuator has an Y component
#     - Apply a Y force offset 15% higher than the max Y limit
#     - Verify the Y force is clipped
#     - Verify the limited Y force is applied
#     - Verify the limited Y force is being measured
#     - Apply a Y force offset 15% lower than the min Y limit
#     - Verify the Y force is clipped
#     - Verify the limited Y force is applied
#     - Verify the limited Y force is being measured
#     - Clear offset forces
#   - Apply a Z force offset 15% higher than the max Z limit
#   - Verify the Z force is clipped
#   - Verify the limited Z force is applied
#   - Verify the limited Z force is being measured
#   - Apply a Z force offset 15% lower than the min Z limit
#   - Verify the Z force is clipped
#   - Verify the limited Z force is applied
#   - Verify the limited Z force is being measured
#   - Clear offset forces
# - Transition from parked engineering state to standby
########################################################################

from MTM1M3Test import *
from ForceActuatorTable import *

from lsst.ts.idl.enums import MTM1M3

import asynctest
import asyncio
import numpy as np
import time

TEST_PERCENTAGE = 1.15
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10

forceActuatorXLimitTable = [
    [112, -75, 0, 0, 75],
    [128, -75, 0, 0, 75],
    [135, -75, 0, 0, 75],
    [212, -75, 0, 0, 75],
    [228, -75, 0, 0, 75],
    [235, -75, 0, 0, 75],
    [312, -75, 0, 0, 75],
    [328, -75, 0, 0, 75],
    [335, -75, 0, 0, 75],
    [412, -75, 0, 0, 75],
    [428, -75, 0, 0, 75],
    [435, -75, 0, 0, 75],
]
forceActuatorYLimitTable = [
    [102, -70, 0, 0, 190],
    [103, -110.6, 0, 0, 265.3],
    [104, -110.6, 0, 0, 265.3],
    [105, -110.6, 0, 0, 265.3],
    [108, -110.6, 0, 0, 265.3],
    [109, -110.6, 0, 0, 265.3],
    [110, -110.6, 0, 0, 265.3],
    [111, -110.6, 0, 0, 265.3],
    [113, -50, 0, 0, 200],
    [114, -110.6, 0, 0, 265.3],
    [115, -110.6, 0, 0, 265.3],
    [116, -110.6, 0, 0, 265.3],
    [117, -110.6, 0, 0, 265.3],
    [118, -47.5, 0, 0, 190],
    [120, -110.6, 0, 0, 265.3],
    [121, -110.6, 0, 0, 265.3],
    [122, -110.6, 0, 0, 265.3],
    [123, -110.6, 0, 0, 265.3],
    [124, -55, 0, 0, 180],
    [126, -50, 0, 0, 200],
    [127, -110.6, 0, 0, 265.3],
    [129, -110.6, 0, 0, 265.3],
    [130, -40, 0, 0, 153],
    [132, -110.6, 0, 0, 265.3],
    [133, -110.6, 0, 0, 265.3],
    [134, -110.6, 0, 0, 265.3],
    [137, -110.6, 0, 0, 265.3],
    [138, -23, 0, 0, 177],
    [208, -110.6, 0, 0, 265.3],
    [209, -110.6, 0, 0, 265.3],
    [210, -110.6, 0, 0, 265.3],
    [211, -110.6, 0, 0, 265.3],
    [214, -110.6, 0, 0, 265.3],
    [215, -110.6, 0, 0, 265.3],
    [216, -110.6, 0, 0, 265.3],
    [217, -110.6, 0, 0, 265.3],
    [218, -47.5, 0, 0, 190],
    [220, -110.6, 0, 0, 265.3],
    [221, -110.6, 0, 0, 265.3],
    [222, -110.6, 0, 0, 265.3],
    [223, -110.6, 0, 0, 265.3],
    [224, -55, 0, 0, 180],
    [227, -110.6, 0, 0, 265.3],
    [229, -110.6, 0, 0, 265.3],
    [230, -40, 0, 0, 153],
    [232, -110.6, 0, 0, 265.3],
    [233, -110.6, 0, 0, 265.3],
    [234, -110.6, 0, 0, 265.3],
    [237, -110.6, 0, 0, 265.3],
    [238, -23, 0, 0, 177],
    [302, -110.6, 0, 0, 265.3],
    [303, -110.6, 0, 0, 265.3],
    [304, -110.6, 0, 0, 265.3],
    [305, -110.6, 0, 0, 265.3],
    [308, -110.6, 0, 0, 265.3],
    [309, -110.6, 0, 0, 265.3],
    [310, -110.6, 0, 0, 265.3],
    [311, -75, 0, 0, 180],
    [313, -50, 0, 0, 200],
    [314, -110.6, 0, 0, 265.3],
    [315, -110.6, 0, 0, 265.3],
    [316, -110.6, 0, 0, 265.3],
    [317, -110.6, 0, 0, 265.3],
    [318, -47.5, 0, 0, 190],
    [320, -110.6, 0, 0, 265.3],
    [321, -110.6, 0, 0, 265.3],
    [322, -110.6, 0, 0, 265.3],
    [323, -110.6, 0, 0, 265.3],
    [324, -55, 0, 0, 180],
    [326, -50, 0, 0, 200],
    [327, -110.6, 0, 0, 265.3],
    [329, -110.6, 0, 0, 265.3],
    [330, -40, 0, 0, 153],
    [332, -110.6, 0, 0, 265.3],
    [333, -110.6, 0, 0, 265.3],
    [334, -75, 0, 0, 180],
    [337, -110.6, 0, 0, 265.3],
    [338, -23, 0, 0, 177],
    [408, -110.6, 0, 0, 265.3],
    [409, -110.6, 0, 0, 265.3],
    [410, -110.6, 0, 0, 265.3],
    [411, -75, 0, 0, 180],
    [414, -110.6, 0, 0, 265.3],
    [415, -110.6, 0, 0, 265.3],
    [416, -110.6, 0, 0, 265.3],
    [417, -110.6, 0, 0, 265.3],
    [418, -47.5, 0, 0, 190],
    [420, -110.6, 0, 0, 265.3],
    [421, -110.6, 0, 0, 265.3],
    [422, -110.6, 0, 0, 265.3],
    [423, -110.6, 0, 0, 265.3],
    [424, -55, 0, 0, 180],
    [427, -110.6, 0, 0, 265.3],
    [429, -110.6, 0, 0, 265.3],
    [430, -40, 0, 0, 153],
    [432, -110.6, 0, 0, 265.3],
    [433, -110.6, 0, 0, 265.3],
    [434, -75, 0, 0, 180],
    [437, -110.6, 0, 0, 265.3],
    [438, -23, 0, 0, 177],
]
forceActuatorZLimitTable = [
    [101, -226.1, 0, 0, 226.1],
    [102, -100, 0, 0, 200],
    [103, -100, 0, 0, 200],
    [104, -100, 0, 0, 200],
    [105, -100, 0, 0, 200],
    [106, -226.1, 0, 0, 226.1],
    [107, -226.1, 0, 0, 226.1],
    [108, -100, 0, 0, 200],
    [109, -100, 0, 0, 200],
    [110, -100, 0, 0, 200],
    [111, -100, 0, 0, 200],
    [112, -125, 0, 0, 220],
    [113, -120, 0, 0, 200],
    [114, -100, 0, 0, 200],
    [115, -100, 0, 0, 200],
    [116, -100, 0, 0, 200],
    [117, -100, 0, 0, 200],
    [118, -75, 0, 0, 200],
    [119, -133, 0, 0, 133],
    [120, -100, 0, 0, 200],
    [121, -100, 0, 0, 200],
    [122, -100, 0, 0, 200],
    [123, -100, 0, 0, 200],
    [124, -80, 0, 0, 200],
    [125, -226.1, 0, 0, 226.1],
    [126, -120, 0, 0, 200],
    [127, -100, 0, 0, 200],
    [128, -125, 0, 0, 220],
    [129, -100, 0, 0, 200],
    [130, -110, 0, 0, 180],
    [131, -226.1, 0, 0, 226.1],
    [132, -100, 0, 0, 200],
    [133, -100, 0, 0, 200],
    [134, -100, 0, 0, 200],
    [135, -125, 0, 0, 220],
    [136, -226.1, 0, 0, 226.1],
    [137, -100, 0, 0, 200],
    [138, -95, 0, 0, 200],
    [139, -226.1, 0, 0, 226.1],
    [140, -226.1, 0, 0, 226.1],
    [141, -226.1, 0, 0, 226.1],
    [142, -226.1, 0, 0, 226.1],
    [143, -133, 0, 0, 133],
    [207, -226.1, 0, 0, 226.1],
    [208, -100, 0, 0, 200],
    [209, -100, 0, 0, 200],
    [210, -100, 0, 0, 200],
    [211, -100, 0, 0, 200],
    [212, -125, 0, 0, 220],
    [214, -100, 0, 0, 200],
    [215, -100, 0, 0, 200],
    [216, -100, 0, 0, 200],
    [217, -100, 0, 0, 200],
    [218, -75, 0, 0, 200],
    [219, -133, 0, 0, 133],
    [220, -100, 0, 0, 200],
    [221, -100, 0, 0, 200],
    [222, -100, 0, 0, 200],
    [223, -100, 0, 0, 200],
    [224, -80, 0, 0, 200],
    [225, -226.1, 0, 0, 226.1],
    [227, -100, 0, 0, 200],
    [228, -125, 0, 0, 220],
    [229, -100, 0, 0, 200],
    [230, -110, 0, 0, 180],
    [231, -226.1, 0, 0, 226.1],
    [232, -100, 0, 0, 200],
    [233, -100, 0, 0, 200],
    [234, -100, 0, 0, 200],
    [235, -125, 0, 0, 220],
    [236, -226.1, 0, 0, 226.1],
    [237, -100, 0, 0, 200],
    [238, -95, 0, 0, 200],
    [239, -226.1, 0, 0, 226.1],
    [240, -226.1, 0, 0, 226.1],
    [241, -226.1, 0, 0, 226.1],
    [242, -226.1, 0, 0, 226.1],
    [243, -133, 0, 0, 133],
    [301, -226.1, 0, 0, 226.1],
    [302, -100, 0, 0, 200],
    [303, -100, 0, 0, 200],
    [304, -100, 0, 0, 200],
    [305, -100, 0, 0, 200],
    [306, -226.1, 0, 0, 226.1],
    [307, -226.1, 0, 0, 226.1],
    [308, -100, 0, 0, 200],
    [309, -100, 0, 0, 200],
    [310, -100, 0, 0, 200],
    [311, -80, 0, 0, 180],
    [312, -125, 0, 0, 220],
    [313, -120, 0, 0, 200],
    [314, -100, 0, 0, 200],
    [315, -100, 0, 0, 200],
    [316, -100, 0, 0, 200],
    [317, -100, 0, 0, 200],
    [318, -75, 0, 0, 200],
    [319, -133, 0, 0, 133],
    [320, -100, 0, 0, 200],
    [321, -100, 0, 0, 200],
    [322, -100, 0, 0, 200],
    [323, -100, 0, 0, 200],
    [324, -80, 0, 0, 200],
    [325, -226.1, 0, 0, 226.1],
    [326, -120, 0, 0, 200],
    [327, -100, 0, 0, 200],
    [328, -125, 0, 0, 220],
    [329, -100, 0, 0, 200],
    [330, -110, 0, 0, 180],
    [331, -226.1, 0, 0, 226.1],
    [332, -100, 0, 0, 200],
    [333, -100, 0, 0, 200],
    [334, -80, 0, 0, 180],
    [335, -125, 0, 0, 220],
    [336, -226.1, 0, 0, 226.1],
    [337, -100, 0, 0, 200],
    [338, -95, 0, 0, 200],
    [339, -226.1, 0, 0, 226.1],
    [340, -226.1, 0, 0, 226.1],
    [341, -226.1, 0, 0, 226.1],
    [342, -226.1, 0, 0, 226.1],
    [343, -133, 0, 0, 133],
    [407, -226.1, 0, 0, 226.1],
    [408, -100, 0, 0, 200],
    [409, -100, 0, 0, 200],
    [410, -100, 0, 0, 200],
    [411, -80, 0, 0, 180],
    [412, -125, 0, 0, 220],
    [414, -100, 0, 0, 200],
    [415, -100, 0, 0, 200],
    [416, -100, 0, 0, 200],
    [417, -100, 0, 0, 200],
    [418, -75, 0, 0, 200],
    [419, -133, 0, 0, 133],
    [420, -100, 0, 0, 200],
    [421, -100, 0, 0, 200],
    [422, -100, 0, 0, 200],
    [423, -100, 0, 0, 200],
    [424, -80, 0, 0, 200],
    [425, -226.1, 0, 0, 226.1],
    [427, -100, 0, 0, 200],
    [428, -125, 0, 0, 220],
    [429, -100, 0, 0, 200],
    [430, -110, 0, 0, 180],
    [431, -226.1, 0, 0, 226.1],
    [432, -100, 0, 0, 200],
    [433, -100, 0, 0, 200],
    [434, -80, 0, 0, 180],
    [435, -125, 0, 0, 220],
    [436, -226.1, 0, 0, 226.1],
    [437, -100, 0, 0, 200],
    [438, -95, 0, 0, 200],
    [439, -226.1, 0, 0, 226.1],
    [440, -226.1, 0, 0, 226.1],
    [441, -226.1, 0, 0, 226.1],
    [442, -226.1, 0, 0, 226.1],
    [443, -133, 0, 0, 133],
]

forceActuatorLimitActuatorId = 0
forceActuatorLimitMin = 1
forceActuatorLimitMax = 4


class M13T027(MTM1M3Test):
    async def _test_actuator(self, fa_type, fa_id):
        self.printTest(f"Testing {fa_type} {fa_id}")
        # Prepare force data
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156

        xApplied = [0] * 12
        yApplied = [0] * 100
        zApplied = [0] * 156

        async def verify(preclipped=True):
            await asyncio.sleep(0.5)

            if preclipped:
                # Verify the preclipped forces match the commanded values
                data = self.m1m3.evt_preclippedForces.get()

                if data is None:
                    self.fail(
                        "Cannot retrieve preclipped data. Most likely you forgot to change Limit tables to *Small?"
                    )

                self.assertListAlmostEqual(
                    data.xForces,
                    xForces,
                    delta=TEST_TOLERANCE,
                    msg="X preclipped forces don't match",
                )
                self.assertListAlmostEqual(
                    data.yForces,
                    yForces,
                    delta=TEST_TOLERANCE,
                    msg="Y preclipped forces don't match",
                )
                self.assertListAlmostEqual(
                    data.zForces,
                    zForces,
                    delta=TEST_TOLERANCE,
                    msg="Z preclipped forces don't match",
                )

            # Verify the applied mirror forces match the expected value
            data = self.m1m3.evt_appliedForces.get()

            self.assertListAlmostEqual(
                data.xForces,
                xApplied,
                delta=TEST_TOLERANCE,
                msg="X applied forces don't match",
            )
            self.assertListAlmostEqual(
                data.yForces,
                yApplied,
                delta=TEST_TOLERANCE,
                msg="Y applied forces don't match",
            )
            self.assertListAlmostEqual(
                data.zForces,
                zApplied,
                delta=TEST_TOLERANCE,
                msg="Z applied forces don't match",
            )

            test_start = time.monotonic()
            duration = 0
            failed_count = 0

            while duration < TEST_SETTLE_TIME * 4:
                # Check force actuator force
                data = await self.sampleData(
                    "tel_forceActuatorData", None, TEST_SAMPLES_TO_AVERAGE
                )
                averages = self.average(data, ["xForce", "yForce", "zForce"])

                duration = time.monotonic() - test_start
                if (
                    np.allclose(averages["xForce"], xApplied, atol=TEST_TOLERANCE)
                    and np.allclose(averages["yForce"], yApplied, atol=TEST_TOLERANCE)
                    and np.allclose(averages["zForce"], zApplied, atol=TEST_TOLERANCE)
                ):
                    if duration > TEST_SETTLE_TIME:
                        break
                else:
                    failed_count += 1

            self.assertLessEqual(
                duration,
                TEST_SETTLE_TIME * 4,
                msg=f"Actuator {self.id} ({fa_type}{fa_id}) doesn't settle within 4 times {TEST_SETTLE_TIME}",
            )

            if duration > TEST_SETTLE_TIME + 1:
                self.printWarning(
                    f"Testing {self.id} ({fa_type}{fa_id}) took {duration:.02f}s to settle down"
                )
            else:
                self.printTest(f"Testing {self.id} ({fa_type}{fa_id}) took {duration:.02f}s with {failed_count} fails")

        async def set_scaled(scale, run_test=True):
            """Sets [xyz]Forces and [xyz]Applied.

            Parameters
            ----------
            scale : `int`
                Scale. 1 for maximum force, -1 for minimum force, 0 for no force.
            """
            minMax = forceActuatorLimitMax if scale > 0 else forceActuatorLimitMin
            use = abs(scale)

            if fa_type == "X":
                xApplied[fa_id] = use * forceActuatorXLimitTable[fa_id][minMax]
                xForces[fa_id] = xApplied[fa_id] * TEST_PERCENTAGE
                self.printTest(
                    f"FA {self.id} X {fa_id}: will apply {xForces[fa_id]:.02f}N, expect to see {xApplied[fa_id]:.02f}N"
                )
            elif fa_type == "Y":
                yApplied[fa_id] = use * forceActuatorYLimitTable[fa_id][minMax]
                yForces[fa_id] = yApplied[fa_id] * TEST_PERCENTAGE
                self.printTest(
                    f"FA {self.id} Y {fa_id}: will apply {yForces[fa_id]:.02f}N, expect to see {yApplied[fa_id]:.02f}N"
                )
            elif fa_type == "Z":
                zApplied[fa_id] = use * forceActuatorZLimitTable[fa_id][minMax]
                zForces[fa_id] = zApplied[fa_id] * TEST_PERCENTAGE
                self.printTest(
                    f"FA {self.id} Z {fa_id}: will apply {zForces[fa_id]:.02f}N, expect to see {zApplied[fa_id]:.02f}N"
                )
            else:
                raise RuntimeError(f"Invalid FA type (only XYZ accepted): {fa_type}")

            if run_test is False:
                return

            # Apply the offset force
            await self.m1m3.cmd_applyOffsetForces.set_start(
                xForces=xForces, yForces=yForces, zForces=zForces
            )

            # This is for run with SW simulator. Modify if SW simulator is needed.
            # Set the simulatored force actuator's load cells to the correct value
            # primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, xForces[x], 0, 0)
            # sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)

            await verify()

        await set_scaled(1)
        await set_scaled(-1)

        # Clear force setpoint for this actuator
        await set_scaled(0, False)
        # Clear offset forces
        await self.m1m3.cmd_clearOffsetForces.start()
        await verify(False)

    async def test_actuator_force_limits(self):
        self.printHeader("M13T-027: Actuator Force Limits")
        self.printWarning(
            "This test requires you to switch M1M3 SS CsC configuration - ForceLimit[XYZ]Table.csv needs to be replaced with ForceLimit[XYZ]TableSmall.csv. Best is to edit on cRIO ForceActuatorSetting.xml"
        )

        await self.startup(MTM1M3.DetailedState.PARKEDENGINEERING)

        x = 0  # X index for data access
        y = 0  # Y index for data access

        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            z = row[forceActuatorTableIndexIndex]
            self.id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]

            self.printTest(f"Verify Force Actuator {self.id} Commands and Telemetry")

            # Run X tests for DDA X
            if orientation in ["+X", "-X"]:
                await self._test_actuator("X", x)
                x += 1
            # Run Y tests for DDA Y
            elif orientation in ["+Y", "-Y"]:
                await self._test_actuator("Y", y)
                y += 1

            await self._test_actuator("Z", z)

        # Transition to standby state
        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
