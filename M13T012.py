#!/usr/bin/env python3.8

# This file is part of ts_salobj.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https: //www.lsst.org).
# See the COPYRIGHT file at the top - level directory of this distribution
# for details of code ownership.
#
# This program is free software : you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.If not, see < https:  // www.gnu.org/licenses/>.

########################################################################
# Test Numbers : M13T - 012
# Author : AClements
# Description : Position Repeatability After Parking
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Wait 5 seconds for everything to settle
# - Confirm Mirror in Reference Position
# - Park the miror, confirmed it has parked.
# - Take IMS measurements
# - return mirror to parked position.
# - repeat above process 5 times.
# - repeat the process for the matrix below
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm
# + X, 0, 0
# - X, 0, 0
# 0, + Y, 0
# 0, - Y, 0
# 0, 0, + Z
# 0, 0, - Z
# - Transition back to standby
########################################################################

import astropy.units as u
import asynctest

from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import *

TRAVEL_POSITION = 1 * u.mm
TRAVEL_ROTATION = 50.4 * u.arcsec
POSITION_TOLERANCE = 40 * u.um.to(u.m)
ROTATION_TOLERANCE = 0.4 * u.arcsec.to(u.deg)


class M13T012(MTM1M3Movements):
    async def _log_data_ims(self, data, imsData):
        print(
            self.LOG_MOVEMENT,
            ",",
            data.xPosition,
            ",",
            data.yPosition,
            ",",
            data.zPosition,
            ",",
            data.xRotation,
            ",",
            data.yRotation,
            ",",
            data.zRotation,
            ",",
            imsData.xPosition,
            ",",
            imsData.yPosition,
            ",",
            imsData.zPosition,
            ",",
            imsData.xRotation,
            ",",
            imsData.yRotation,
            ",",
            imsData.zRotation,
            file=self.LOG_FILE,
        )
        self.LOG_FILE.flush()

    async def test_repeatibility(self):
        offsets = [
            offset(),
            offset(x=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION),
            offset(z=+TRAVEL_POSITION),
            offset(z=-TRAVEL_POSITION),
        ]

        self.POSITION_TOLERANCE = POSITION_TOLERANCE
        self.ROTATION_TOLERANCE = ROTATION_TOLERANCE

        self.openCSV("M13T012")

        print(
            "Movement,HP xPosition, HP yPostion, HP zPosition, HP xRotation, HP yRotation, HP zRotation, IMS xPosition, IMS yPosition, IMS zPosition, IMS xRotation, IMS yRotation, IMS zRotation",
            file=self.LOG_FILE,
        )

        for i in range(7):
            await self.do_movements(
                offsets,
                "M13T-012: Position Repeatability After Parking",
                end_state=MTM1M3.DetailedState.PARKED,
                moved_callback=self._log_data_ims,
            )

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
