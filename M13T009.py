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
# Test Numbers: M13T-009
# Author:       AClements
# Description:  Mirror Support System Active Motion Range
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where +X = 6.13mm, -X = 6.13mm, +Y = 6.13mm, -Y = -6.13mm, +Z = 4.07mm  & -Z = -5.57mm
#   +X, 0, 0
#   -X, 0, 0
#   0,+Y, 0
#   0, -Y, 0
#   0, 0, +Z
#   0, 0, -Z
#   +X, +Y, 0
#   +X, -Y, 0
#   -X, +Y, 0
#   -X, -Y, 0
#   +X, 0, +Z
#   +X, 0, -Z
#   -X, 0, +Z
#   -X, 0, -Z
#   0, +Y, +Z
#   0, +Y, -Z
#   0, -Y, +Z
#   0, -Y, -Z
# - Repeat Matrix 2 more times
# - Transition back to standby
########################################################################

import astropy.units as u
import asynctest

from MTM1M3Movements import *


TRAVEL_POSITION = 6.13 * u.mm
POS_Z_TRAVEL_POSITION = 4.07 * u.mm
NEG_Z_TRAVEL_POSITION = 5.57 * u.mm

ZERO_M = 0 * u.m
ZERO_DEG = 0 * u.deg

class M13T009(MTM1M3Movements):
    async def test_movements(self):
        offsets = [
            [TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG, ],
            [ZERO_M, ZERO_M, +POS_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, -NEG_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, ZERO_M, +POS_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, ZERO_M, -NEG_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, +POS_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, -NEG_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, +TRAVEL_POSITION, +POS_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, +TRAVEL_POSITION, -NEG_Z_TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
        ]

        await self.do_movements(offsets)


if __name__ == "__main__":
    asynctest.main()
