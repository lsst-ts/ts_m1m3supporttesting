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

from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import *


TRAVEL_POSITION = 6.13 * u.mm
POS_Z_TRAVEL_POSITION = 4.07 * u.mm
NEG_Z_TRAVEL_POSITION = 5.57 * u.mm


class M13T009(MTM1M3Movements):
    async def test_movements(self):
        offsets = [
            offset(x=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION),
            offset(z=POS_Z_TRAVEL_POSITION),
            offset(z=NEG_Z_TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, y=+TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, y=-TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, y=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, y=-TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
        ]

        for m in range(3):
            await self.do_movements(
                offsets,
                "M13T-009: Mirror Support System Active Motion Range",
                end_state=MTM1M3.DetailedState.PARKED
                if m == 3
                else MTM1M3.DetailedState.ACTIVEENGINEERING,
            )


if __name__ == "__main__":
    asynctest.main()
