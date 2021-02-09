########################################################################
# Test Numbers: M13T-010
# Author:       AClements
# Description:  Position System Requirements
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm and ΘX, ΘY, & ΘZ are 50.4 arcsec:
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

import astopy.units as u

import asynctest

from MTM1M3Movements import MTM1M3Movements

TRAVEL_POSITION = 1 * u.mm
TRAVEL_ROTATION = 50.4 * u.arcsec

ZERO_M = 0 * u.m
ZERO_DEG = 0 * u.deg


class M13T010(MTM1M3Movements):
    async def test_movements(self):
        offsets = [
            [+TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [+TRAVEL_POSITION, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [-TRAVEL_POSITION, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, +TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, +TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, -TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, +TRAVEL_ROTATION, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, -TRAVEL_ROTATION, ZERO_DEG, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, +TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, -TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, +TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, -TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, +TRAVEL_ROTATION, +TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, -TRAVEL_ROTATION, +TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, +TRAVEL_ROTATION, -TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, -TRAVEL_ROTATION, -TRAVEL_ROTATION, ZERO_DEG,],
            [ZERO_M, ZERO_M, ZERO_M, +TRAVEL_ROTATION, ZERO_DEG, +TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, -TRAVEL_ROTATION, ZERO_DEG, +TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, +TRAVEL_ROTATION, ZERO_DEG, -TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, -TRAVEL_ROTATION, ZERO_DEG, -TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, +TRAVEL_ROTATION, +TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, +TRAVEL_ROTATION, -TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, -TRAVEL_ROTATION, +TRAVEL_ROTATION,],
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, -TRAVEL_ROTATION, -TRAVEL_ROTATION,],
        ]

        await self.do_movements(offsets)


if __name__ == "__main__":
    asynctest.main()
