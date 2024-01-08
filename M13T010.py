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
# Test Numbers: M13T-010
# Author:       AClements
# Description:  Position System Requirements
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm and ΘX, ΘY, & ΘZ
# are 50.4 arcsec: +X, 0, 0
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
#   +ΘX, 0, 0
#   -ΘX, 0, 0
#   0, +ΘY, 0
#   0, -ΘY, 0
#   0, 0, +ΘZ
#   0, 0, -ΘZ
#   +ΘX, +ΘY, 0
#   -ΘX, +ΘY, 0
#   +ΘX, -ΘY, 0
#   -ΘX, -ΘY, 0
#   +ΘX, 0, +ΘZ
#   -ΘX, 0, +ΘZ
#   +ΘX, 0, -ΘZ
#   -ΘX, 0, -ΘZ
#   0, +ΘY, +ΘZ
#   0, +ΘY, -ΘZ
#   0, -ΘY, +ΘZ
#   0, -ΘY, -ΘZ
# - Repeat Matrix 2 more times
# - Transition back to standby
########################################################################

import unittest

import astropy.units as u
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements, offset

TRAVEL_POSITION = 1 * u.mm
TRAVEL_ROTATION = 50.4 * u.arcsec


class M13T010(MTM1M3Movements):
    async def test_movements(self) -> None:
        offsets = [
            offset(x=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION),
            offset(z=+TRAVEL_POSITION),
            offset(z=-TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, y=+TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, y=-TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, y=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, y=-TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, z=+TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION, z=-TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, z=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, z=-TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION, z=+TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION, z=-TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION, z=+TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION, z=-TRAVEL_POSITION),
            offset(rx=+TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION),
            offset(ry=+TRAVEL_ROTATION),
            offset(ry=-TRAVEL_ROTATION),
            offset(rz=+TRAVEL_ROTATION),
            offset(rz=-TRAVEL_ROTATION),
            offset(rx=+TRAVEL_ROTATION, ry=+TRAVEL_ROTATION),
            offset(rx=+TRAVEL_ROTATION, ry=-TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION, ry=+TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION, ry=-TRAVEL_ROTATION),
            offset(rx=+TRAVEL_ROTATION, rz=+TRAVEL_ROTATION),
            offset(rx=+TRAVEL_ROTATION, rz=-TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION, rz=+TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION, rz=-TRAVEL_ROTATION),
            offset(ry=+TRAVEL_ROTATION, rz=+TRAVEL_ROTATION),
            offset(ry=+TRAVEL_ROTATION, rz=-TRAVEL_ROTATION),
            offset(ry=-TRAVEL_ROTATION, rz=+TRAVEL_ROTATION),
            offset(ry=-TRAVEL_ROTATION, rz=-TRAVEL_ROTATION),
        ]

        for m in range(3):
            await self.do_movements(
                offsets,
                "M13T-010: Position System Requirements",
                end_state=MTM1M3.DetailedStates.ACTIVEENGINEERING,
                check_forces=False,
            )


if __name__ == "__main__":
    unittest.main()
