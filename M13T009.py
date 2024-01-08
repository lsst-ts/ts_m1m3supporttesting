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
#
# For surrogate:
# +X = 5.00mm, -X = -5.75mm
# +Y = 4.75mm, -Y = -6.50mm
# +Z = 4.50mm, -Z = -2.60mm
# Surrogate has different center of gravity, and different geometry. It cannot
# reach full motion range, as the mirror will touch static supports on sides
# before achieving the full motion range.


# - Follow the motion matrix below, where
# +X = 6.13mm, -X = 6.13mm,
# +Y = 6.13mm, -Y = -6.13mm,
# +Z = 4.07mm & -Z = -5.57mm:
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

import unittest

import astropy.units as u
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements, offset

TRAVEL_POSITION = 6.13 * u.mm
POS_X_TRAVEL_POSITION = TRAVEL_POSITION
NEG_X_TRAVEL_POSITION = -TRAVEL_POSITION
POS_Y_TRAVEL_POSITION = TRAVEL_POSITION
NEG_Y_TRAVEL_POSITION = -TRAVEL_POSITION
POS_Z_TRAVEL_POSITION = 4.07 * u.mm
NEG_Z_TRAVEL_POSITION = -5.57 * u.mm

# surrogate
POS_X_TRAVEL_POSITION = 5.00 * u.mm
NEG_X_TRAVEL_POSITION = -5.75 * u.mm
POS_Y_TRAVEL_POSITION = 4.75 * u.mm
NEG_Y_TRAVEL_POSITION = -6.50 * u.mm
POS_Z_TRAVEL_POSITION = 4.50 * u.mm
NEG_Z_TRAVEL_POSITION = -2.60 * u.mm


class M13T009(MTM1M3Movements):
    async def test_movements(self) -> None:
        offsets = [
            offset(x=POS_X_TRAVEL_POSITION),
            offset(x=NEG_X_TRAVEL_POSITION),
            offset(y=POS_Y_TRAVEL_POSITION),
            offset(y=NEG_Y_TRAVEL_POSITION),
            offset(z=POS_Z_TRAVEL_POSITION),
            offset(z=NEG_Z_TRAVEL_POSITION),
            offset(x=POS_X_TRAVEL_POSITION, y=POS_Y_TRAVEL_POSITION),
            offset(x=POS_X_TRAVEL_POSITION, y=NEG_Y_TRAVEL_POSITION),
            offset(x=NEG_X_TRAVEL_POSITION, y=POS_Y_TRAVEL_POSITION),
            offset(x=NEG_X_TRAVEL_POSITION, y=NEG_Y_TRAVEL_POSITION),
            offset(x=POS_X_TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(x=POS_X_TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(x=NEG_X_TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(x=NEG_X_TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(y=POS_Y_TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(y=POS_Y_TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
            offset(y=NEG_Y_TRAVEL_POSITION, z=POS_Z_TRAVEL_POSITION),
            offset(y=NEG_Y_TRAVEL_POSITION, z=NEG_Z_TRAVEL_POSITION),
        ]

        for m in range(3):
            await self.do_movements(
                offsets,
                "M13T-009: Mirror Support System Active Motion Range",
                end_state=MTM1M3.DetailedStates.PARKED
                if m == 3
                else MTM1M3.DetailedStates.ACTIVEENGINEERING,
            )


if __name__ == "__main__":
    unittest.main()
