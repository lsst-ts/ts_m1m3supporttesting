#!/usr/bin/env python3

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
# Test Numbers: M13T-015
# Author:       PKubanek
# Description:  Force Combination Test
# Steps:
# - Transition to active mode
# - Apply various forces (AOS - applyActiveOpticsForces, gravity)
# - Read back applied forces
# - Verify that applied forces are sum of force components
# - Repeat
# - Lower mirror
########################################################################

import unittest

from lsst.ts.idl.enums import MTM1M3
from numpy.random import normal, random

from MTM1M3Movements import ForceOffsets, MTM1M3Movements


class M13T015(MTM1M3Movements):
    async def test_force_combination_test(self):
        offsets = [
            ForceOffsets(
                xForces=normal(85, 58, 12),
                yForces=normal(122, 63, 100),
                zForces=normal(78, 42.5, 156),
            ),
            ForceOffsets(zActiveForces=normal(0.2, 7.3, 156)),
            ForceOffsets(
                xForces=random(12) * 35.2,
                yForces=random(100) * 78.2,
                zForces=random(156) * 167.78,
            ),
            ForceOffsets(xForces=[1] * 12, yForces=[-1] * 100, zForces=[1] * 156),
            ForceOffsets(xForces=[100] * 12, yForces=[-100] * 100, zForces=[100] * 156),
            ForceOffsets(xForces=[35] * 12, yForces=[-75] * 100, zForces=[85] * 156),
            ForceOffsets(
                xForces=normal(0, 80, 12),
                yForces=normal(0, 45, 100),
                zForces=normal(0, 42.5, 156),
            ),
            ForceOffsets(
                xForces=normal(-12, 30, 12),
                yForces=normal(11.5, 16, 100),
                zForces=normal(35, 42.5, 156),
            ),
            ForceOffsets(
                xForces=normal(85, 58, 12),
                yForces=normal(300, 63, 100),
                zForces=normal(200, 42.5, 156),
            ),
            ForceOffsets(
                xForces=normal(30, 69, 12),
                yForces=normal(256, 74, 100),
                zForces=normal(127, 47, 156),
            ),
            ForceOffsets(
                xForces=normal(0, 6, 12),
                yForces=normal(0, 16, 100),
                zForces=normal(0, 42.5, 156),
            ),
            ForceOffsets(
                xForces=[-12.45] * 12,
                yForces=[12.34] * 100,
                zForces=[-74.56] * 156,
            ),
        ]

        await self.applyOffsetForces(
            offsets,
            "M13T-015: Force Combination Test",
        )


if __name__ == "__main__":
    unittest.main()
