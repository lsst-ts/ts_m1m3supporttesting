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
# Test Numbers: M13T-011
# Author:       AClements
# Description:  Position Stability During Active Mode Operation
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Wait 5 seconds for everything to settle
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm
# - Wait 15 seconds between each movement to let control take measurements.
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
# - Pull data from EFD to generate RMS values specified by the test.
########################################################################

import asyncio
import unittest
from datetime import datetime

import astropy.units as u
from lsst.ts import salobj
from lsst.ts.criopy.VMS import Collector
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements, offset

TRAVEL_POSITION = 1 * u.mm
SETTLE_TIME = 3.0
SAMPLE_TIME = 15.0

M2MM = u.m.to(u.mm)


class M13T011(MTM1M3Movements):
    def _log_data(self, position, data, imsData):
        self.m1m3.tel_imsData.flush()
        self.vms.data.flush()

        startTimestamp = None

        while True:
            imsData = self.m1m3.tel_imsData.next()

            if startTimestamp is None:
                startTimestamp = imsData.timestamp
            elif (imsData.timestamp - startTimestamp) > SAMPLE_TIME:
                break

            print(
                imsData.timestamp,
                imsData.xPosition,
                imsData.zPosition,
                imsData.xRotation,
                imsData.yRotation,
                imsData.zRotation,
                ", ".join(imsData.rawSensorData),
                ", ".join(position),
                file=self.IMS_FILE,
                sep=",",
            )
            self.IMS_FILE.flush()

            def convert(raw, sensitivity):
                return (raw * M2MM) / sensitivity

    async def _run(self):
        offsets = [
            offset(),
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
        ]

        # Start collector
        self.tasks.append(asyncio.create_task(self.collector.collect_data(False)))

        # The matrix need to be tested 3 times
        for i in range(3):
            await self.do_movements(
                offsets,
                "M13T-011: Position Stability During Active Mode Operation",
                end_state=MTM1M3.DetailedStates.STANDBY,
                moved_callback=self._log_data,
            )

        for t in self.tasks:
            t.cancel()

    async def test_movements(self):
        # Setup VMS
        self.vms = salobj.Remote(self.domain, "MTVMS", index=1)

        start = datetime.now()

        self.IMS_FILE = self.openCSV("M13T012-IMS")

        print(
            "Timestamp,xPosition,yPosition,zPosition," "xRotation,yRotation,zRotation",
            file=self.IMS_FILE,
        )

        self.collector = Collector(
            1,
            "M13T012-VMS-" + datetime.now().strftime("%Y-%m-%dT%T") + ".${ext}",
        )

        self.tasks = []

        try:
            await self._run()
        finally:
            await asyncio.gather(*self.tasks)
            self.collector.close()


if __name__ == "__main__":
    unittest.main()
