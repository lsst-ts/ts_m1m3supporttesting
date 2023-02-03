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
# Test Numbers: M13T-032
# Author:       CContaxis
# Description:  Independent Measuring System (IMS)
# Steps:
# - Transition from standby to active engineering state
# - Repeat the following 3 times:
#   - Follow the motion matrix below:
#     - +X  0  0
#     - -X  0  0
#     -  0 +Y  0
#     -  0 -Y  0
#     -  0  0 +Z
#     -  0  0 -Z
# - Transition from active engineering state to standby
########################################################################

from MTM1M3Movements import *
from lsst.ts.idl.enums import MTM1M3

import astropy.units as u

import asyncio
import asynctest

TRAVEL_POSITION = 1 * u.mm
SAMPLE_TIME = 1


class M13T032(MTM1M3Movements):
    async def _log_data(self, position, data, imsData):
        names = [
            "xPosition",
            "yPosition",
            "zPosition",
            "xRotation",
            "yRotation",
            "zRotation",
        ]
        hpData = await self.sampleData("tel_hardpointActuatorData", SAMPLE_TIME)
        hpAverages = self.average(hpData, names)

        imsData = await self.sampleData("tel_imsData", SAMPLE_TIME)
        imsAverages = self.average(imsData, names)

        M2MM = u.m.to(u.mm)
        D2ARCSEC = u.deg.to(u.arcsec)

        def printAverage(a, n):
            if n[1:] == "Rotation":
                return str(a[n] * D2ARCSEC)
            return str(a[n] * M2MM)

        print(
            str(hpData[0].timestamp)
            + ", "
            + self.LOG_MOVEMENT
            + ", "
            + ", ".join(
                [printAverage(hpAverages, n) for n in names]
                + [printAverage(imsAverages, n) for n in names]
            ),
            file=self.LOG_FILE,
        )
        self.LOG_FILE.flush()

    async def test_ims(self):
        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        offsets = [
            offset(x=+TRAVEL_POSITION),
            offset(x=+TRAVEL_POSITION),
            offset(y=-TRAVEL_POSITION),
            offset(y=+TRAVEL_POSITION),
            offset(z=-TRAVEL_POSITION),
            offset(z=-TRAVEL_POSITION),
            offset(),
        ]

        self.openCSV("M13T032")

        print(
            "Timestamp, HP X(mm), HP Y(mm), HP Z(mm), HP RX(arcsec), HP RY(arcsec), HP RZ(arcsec), IMS X(mm), IMS Y(mm), IMS Z(mm), IMS RX(arcsec), IMS RY(arcsec), IMS RZ(arcsec)",
            file=self.LOG_FILE,
        )

        # Repeat 3 times
        for i in range(3):
            await self.do_movements(
                offsets,
                f"M13T032 - Test movements pass #{i}/3",
                start_state=None,
                end_state=None,
                moved_callback=self._log_data,
            )

        self.close_log_file()

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
