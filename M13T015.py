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

import asyncio
import asynctest
import random

from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements, offset


class M13T015(MTM1M3Movements):
    async def test_force_combination_test(self):
        offsets = [
            {
                "xForces": [random.random() * 12.0 for x in range(12)],
                "yForces": [random.random() * -32 for y in range(100)],
                "zForces": [random.random() * 85 for z in range(156)],
            },
            {"xForces": [1] * 12, "yForces": [-1] * 100, "zForces": [1] * 156},
            {"xForces": [100] * 12, "yForces": [-100] * 100, "zForces": [100] * 156},
            {"xForces": [35] * 12, "yForces": [-75] * 100, "zForces": [85] * 156},
            {
                "xForces": [random.random() * 10.11 - 5 for x in range(12)],
                "yForces": [random.random() * -25.3 for y in range(100)],
                "zForces": [random.random() * 85 for z in range(156)],
            },
            {
                "xForces": [random.random() * 12.0 for x in range(12)],
                "yForces": [random.random() * -32 for y in range(100)],
                "zForces": [random.random() * 85 for z in range(156)],
            },
            {
                "xForces": [random.random() * 12.0 for x in range(12)],
                "yForces": [random.random() * -32 for y in range(100)],
                "zForces": [random.random() * 85 for z in range(156)],
            },
            {
                "xForces": [random.random() * 12.0 - 6 for x in range(12)],
                "yForces": [random.random() * -32 + 16 for y in range(100)],
                "zForces": [random.random() * 85 - 42.5 for z in range(156)],
            },
            {"xForces": [-12.45] * 12, "yForces": [12.34] * 100, "zForces": [-74.56] * 156},
        ]

        await self.applyOffsetForces(
            offsets,
            "M13T-015: Force Combination Test",
            end_state=MTM1M3.DetailedState.ACTIVEENGINEERING,
        )


if __name__ == "__main__":
    asynctest.main()
