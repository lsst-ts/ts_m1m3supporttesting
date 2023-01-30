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
# This test requires you to switch M1M3 SS CsC configuration - disable fault on
# NearNeighborCheck and FarNeighborCheck and remove limits for applied forces
# (so offset wouldn't be pre-clipped).
#
# To do that, edit SafetyControllerSettings.yaml in actually
# used set, switch:
#
#        FaultOnNearNeighborCheck: On
#        FaultOnFarNeighborCheck: On
#
# to
#
#        FaultOnNearNeighborCheck: Off
#        FaultOnFarNeighborCheck: Off
#
# ForceLimit[XYZ]Table.csv needs to be replaced with
# ForceLimit[XYZ]TableNone.csv. Best is to edit on cRIO / simulator
# ForceActuatorSetting.yaml and change:
#
#   ForceLimitXTablePath: Tables/ForceLimitXTable.csv
#   ForceLimitYTablePath: Tables/ForceLimitYTable.csv
#   ForceLimitZTablePath: Tables/ForceLimitZTable.csv
#
# to
#
#   ForceLimitXTablePath: Tables/ForceLimitXTableNone.csv
#   ForceLimitYTablePath: Tables/ForceLimitYTableNone.csv
#   ForceLimitZTablePath: Tables/ForceLimitZTableNone.csv
#
#
# and restart CsC before running the test.

########################################################################
# Test Numbers: M13T-028
# Author:       CContaxis
# Description:  Actuator to Actuator Force Delta for 6 nearest neighbors
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - Apply a Z force
#   - Verify Z force induces a near neighbor warning
#   - Clear offset forces
#   - Verify near neighbor warning is removed
#   - Apply a negative Z force
#   - Verify Z force induces a near neighbor warning
#   - Clear offset forces
#   - Verify near neighbor warning is removed
#   - Apply a Z force to the near neighbors
#   - Verify neighbor force induces a near neighbor warning
#   - Clear offset forces
#   - Verify near neighbor warning is removed
#   - Apply a negative Z force to th enear neighbors
#   - Verify neighbor force induces a near neighbor warning
#   - Clear offset forces
#   - Verify near neighbor warning is removed
# - Transition from parked engineering state to standby
########################################################################

from MTM1M3Test import *
from ForceActuatorTable import *

from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest

MIRROR_WEIGHT = 170000.0
TEST_FORCE = (MIRROR_WEIGHT / 156) + 50
TEST_SETTLE_TIME = 1.0

NEIGHBOR_TABLE = [
    [101, 102, 408, 407, 107, 108],
    [102, 103, 409, 408, 101, 108, 109],
    [103, 104, 410, 409, 102, 109, 110],
    [104, 105, 411, 410, 103, 110, 111],
    [105, 106, 412, 411, 104, 111, 112],
    [106, 412, 105, 112],
    [107, 108, 101, 113, 114],
    [108, 109, 102, 101, 107, 114, 115],
    [109, 110, 103, 102, 108, 115, 116],
    [110, 111, 104, 103, 109, 116, 117],
    [111, 112, 105, 104, 110, 117, 118],
    [112, 106, 105, 111, 118, 125, 119],
    [113, 114, 107, 207, 214, 220, 120],
    [114, 115, 108, 107, 113, 120, 121],
    [115, 116, 109, 108, 114, 121, 122],
    [116, 117, 110, 109, 115, 122, 123],
    [117, 118, 111, 110, 116, 123, 124],
    [118, 119, 112, 111, 117, 124, 125],
    [119, 112, 111, 118, 125],
    [120, 121, 114, 113, 220, 125, 127],
    [121, 122, 115, 114, 120, 127, 128],
    [122, 123, 116, 115, 121, 128, 129],
    [123, 124, 117, 116, 122, 129, 130],
    [124, 125, 118, 117, 123, 130, 131],
    [125, 119, 118, 124, 131],
    [126, 127, 120, 220, 227, 232, 132],
    [127, 128, 121, 120, 126, 132, 133],
    [128, 129, 122, 121, 127, 133, 134],
    [129, 130, 123, 122, 128, 134, 135],
    [130, 131, 124, 123, 129, 135, 136],
    [131, 125, 124, 130, 136],
    [132, 133, 127, 126, 232, 237, 137, 138],
    [133, 134, 128, 127, 132, 138, 139],
    [134, 135, 129, 128, 133, 139, 140],
    [135, 136, 130, 129, 134, 140],
    [136, 131, 130, 129, 135],
    [137, 138, 132, 232, 237, 241, 141],
    [138, 139, 133, 132, 137, 141, 142, 143],
    [139, 134, 133, 138, 142, 143, 140],
    [140, 135, 134, 139, 143],
    [141, 142, 138, 137, 237, 241],
    [142, 143, 139, 138, 141],
    [143, 140, 139, 134, 133, 138, 142],
    [207, 107, 301, 208, 214, 113],
    [208, 207, 301, 302, 209, 215, 214],
    [209, 208, 302, 303, 210, 216, 215],
    [210, 209, 303, 304, 211, 217, 216],
    [211, 210, 304, 305, 212, 219, 218, 217],
    [212, 211, 305, 306, 219, 225, 218],
    [214, 113, 207, 208, 215, 221, 220],
    [215, 214, 208, 209, 216, 222, 221],
    [216, 215, 209, 210, 217, 223, 222],
    [217, 216, 210, 211, 218, 224, 223],
    [218, 217, 211, 212, 219, 225, 224],
    [219, 211, 212, 225, 218],
    [220, 120, 113, 214, 221, 227, 126],
    [221, 220, 214, 215, 222, 228, 227],
    [222, 221, 215, 216, 223, 229, 228],
    [223, 222, 216, 217, 224, 230, 229],
    [224, 223, 217, 218, 225, 231, 230],
    [225, 218, 219, 231, 224],
    [227, 126, 220, 221, 228, 233, 232],
    [228, 227, 221, 222, 229, 234, 233],
    [229, 228, 222, 223, 230, 236, 235, 234],
    [230, 229, 223, 224, 231, 236, 235],
    [231, 230, 224, 225, 236],
    [232, 132, 126, 227, 233, 238, 237, 137],
    [233, 232, 227, 228, 234, 239, 238],
    [234, 233, 228, 229, 235, 240, 243, 239],
    [235, 234, 229, 230, 236, 240],
    [236, 235, 229, 230, 231],
    [237, 137, 132, 232, 238, 241, 141],
    [238, 237, 232, 233, 239, 243, 242, 241],
    [239, 233, 234, 240, 243, 242, 238],
    [240, 239, 234, 235, 243],
    [241, 141, 137, 237, 238, 242],
    [242, 241, 238, 239, 243],
    [243, 238, 239, 234, 240, 242],
    [301, 307, 308, 302, 208, 207],
    [302, 301, 308, 309, 303, 209, 208],
    [303, 302, 309, 310, 304, 210, 209],
    [304, 303, 310, 311, 305, 211, 210],
    [305, 304, 311, 312, 306, 212, 211],
    [306, 305, 312, 212],
    [307, 407, 313, 314, 308, 301],
    [308, 307, 314, 315, 309, 302, 301],
    [309, 308, 315, 316, 310, 303, 302],
    [310, 309, 316, 317, 311, 304, 303],
    [311, 310, 317, 318, 319, 312, 305, 304],
    [312, 311, 318, 319, 306, 305, 325],
    [313, 414, 420, 320, 314, 307, 407],
    [314, 313, 320, 321, 315, 308, 307],
    [315, 314, 321, 322, 316, 309, 308],
    [316, 315, 322, 323, 317, 310, 309],
    [317, 316, 323, 324, 318, 311, 310],
    [318, 317, 324, 325, 319, 312, 311],
    [319, 318, 325, 312, 311],
    [320, 420, 326, 327, 321, 314, 313],
    [321, 320, 327, 328, 322, 315, 314],
    [322, 321, 328, 329, 323, 316, 315],
    [323, 322, 329, 330, 324, 317, 316],
    [324, 323, 330, 331, 325, 318, 317],
    [325, 324, 331, 319, 318, 312],
    [326, 427, 432, 332, 327, 320, 420],
    [327, 326, 332, 333, 328, 321, 320],
    [328, 327, 333, 334, 329, 322, 321],
    [329, 328, 334, 335, 330, 323, 322],
    [330, 329, 335, 336, 331, 324, 323],
    [331, 330, 336, 325, 324],
    [332, 432, 437, 337, 338, 333, 327, 326],
    [333, 332, 338, 339, 334, 328, 327],
    [334, 333, 339, 343, 340, 335, 329, 328],
    [335, 334, 340, 336, 330, 329],
    [336, 335, 331, 330, 329],
    [337, 437, 441, 341, 342, 338, 332, 432],
    [338, 337, 341, 342, 343, 339, 333, 332],
    [339, 338, 342, 343, 340, 335, 334, 333],
    [340, 343, 335, 334, 339],
    [341, 441, 342, 338, 337, 437],
    [342, 341, 343, 339, 333, 338, 337],
    [343, 342, 340, 339, 334, 333, 338],
    [407, 408, 414, 313, 307, 101],
    [408, 409, 415, 414, 407, 101, 102],
    [409, 410, 416, 415, 408, 102, 103],
    [410, 411, 417, 416, 409, 103, 104],
    [411, 412, 419, 418, 417, 410, 104, 105],
    [412, 419, 425, 418, 411, 105, 106],
    [414, 415, 421, 420, 313, 407, 408],
    [415, 416, 422, 421, 414, 408, 409],
    [416, 417, 423, 422, 415, 409, 410],
    [417, 418, 424, 423, 416, 410, 411],
    [418, 419, 425, 424, 417, 411, 412],
    [419, 425, 418, 411, 412],
    [420, 421, 427, 326, 320, 313, 414],
    [421, 422, 428, 427, 420, 414, 415],
    [422, 423, 429, 428, 421, 415, 416],
    [423, 424, 430, 429, 422, 416, 417],
    [424, 431, 430, 423, 417, 418, 425],
    [425, 431, 424, 418, 412, 419],
    [427, 428, 433, 432, 326, 420, 421],
    [428, 429, 434, 433, 427, 421, 422],
    [429, 430, 436, 435, 434, 428, 422, 423],
    [430, 431, 436, 435, 429, 423, 424],
    [431, 436, 430, 424, 425],
    [432, 433, 438, 437, 337, 332, 326, 427],
    [433, 434, 439, 438, 432, 427, 428],
    [434, 435, 440, 439, 433, 428, 429],
    [435, 440, 434, 429, 430, 436],
    [436, 435, 429, 430, 431],
    [437, 438, 441, 341, 337, 332, 432],
    [438, 439, 443, 442, 441, 437, 432, 433],
    [439, 440, 443, 442, 438, 433, 434],
    [440, 443, 439, 434, 435],
    [441, 442, 341, 337, 437, 438],
    [442, 441, 437, 438, 439, 443],
    [443, 442, 438, 439, 434, 440],
]


class M13T028(MTM1M3Test):
    async def test_nearest_neighbors(self):
        self.printHeader(
            "M13T-028: Actuator to Actuator Force Delta for 6 nearest neighbors"
        )

        self.printError(
            "This test should be run only in simulator or with surrogate mirror. DON'T RUN THIS TEST WITH GLASS MIRROR!"
        )

        self.printWarning(
            "This tests will run only with FaultOnNearNeighborCheck and FaultOnFarNeighborCheck disabled. And Limit table set to None Please see test source code for instructions."
        )

        await self.startup(MTM1M3.DetailedState.PARKEDENGINEERING)

        data = await self.m1m3.evt_forceSetpointWarning.next(
            flush=False, timeout=TEST_SETTLE_TIME
        )
        for i in range(len(forceActuatorTable)):
            self.assertEqual(
                data.nearNeighborWarning[i],
                False,
                msg=f"Near neighbor warning for index {i} is True. Was the previous test reseted?",
            )

        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            z = row[
                forceActuatorTableIndexIndex
            ]  # Z index for data access, all force actuators have Z data
            id = row[forceActuatorTableIDIndex]

            async def apply_z_offset(force, z_ids):
                # Prepare force data
                xForces = [0] * 12
                yForces = [0] * 100
                zForces = [0] * 156

                z_indices = list(map(actuatorIDToIndex, z_ids))

                self.printTest(
                    f"Verify Force Actuator {id} with {force:.02f}N applied to Z {str(z_indices)} FA IDs {str(z_ids)}"
                )
                # Apply the force offset
                for i in z_indices:
                    zForces[i] = force

                await self.m1m3.cmd_applyOffsetForces.set_start(
                    xForces=xForces, yForces=yForces, zForces=zForces
                )

                await asyncio.sleep(TEST_SETTLE_TIME)

                # Check for near neighbor warning
                data = self.m1m3.evt_forceSetpointWarning.get()

                self.assertEqual(
                    data.nearNeighborWarning[z],
                    True,
                    msg=f"Near neighbor warning for ID {id} ({z}) is False with force applied. Was ForceLimit[XYZ]TablePath pointed to *None?",
                )

                self.assertNotEqual(
                    self.m1m3.evt_detailedState.get().detailedState,
                    MTM1M3.DetailedState.FAULT,
                    msg=f"Mirror faulted when force applied for {id}. Most probably configuration error - were FaultOnNearNeighborCheck and FaultOnFarNeighborCheck set to 0?",
                )

                # Clear the force offset
                for i in z_indices:
                    zForces[i] = 0.0
                await self.m1m3.cmd_clearOffsetForces.start()

                await asyncio.sleep(TEST_SETTLE_TIME)

                # Check for near neighbor warning
                data = await self.m1m3.evt_forceSetpointWarning.get()
                self.assertEqual(
                    data.nearNeighborWarning[z],
                    False,
                    msg=f"Near neighbor warning for ID {id} is still True with no force applied",
                )

            await apply_z_offset(TEST_FORCE, [id])
            await apply_z_offset(-TEST_FORCE, [id])

            await apply_z_offset(TEST_FORCE, NEIGHBOR_TABLE[z][1:])
            await apply_z_offset(-TEST_FORCE, NEIGHBOR_TABLE[z][1:])

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
