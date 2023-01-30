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

import astropy.units as u
import asynctest
import click
from datetime import datetime

from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import *


X1Sensitivity = 51.459
Y1Sensitivity = 52.061
Z1Sensitivity = 51.298

X2Sensitivity = 51.937
Y2Sensitivity = 52.239
Z2Sensitivity = 52.130

X3Sensitivity = 52.183
Y3Sensitivity = 52.015
Z3Sensitivity = 51.908

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
            vmsData = self.vms.tel_psd.next()

            if startTimestamp is None:
                startTimestamp = imsData.timestamp
            elif (imsData.timestamp - startTimestamp) > SAMPLE_TIME:
                break

            print(
                imsData.timestamp,
                ", ",
                imsData.xPosition,
                ", ",
                imsData.zPosition,
                ", ",
                imsData.xRotation,
                ", ",
                imsData.yRotation,
                ", ",
                imsData.zRotation,
                ", ",
                ", ".join(imsData.rawSensorData),
                ", ",
                ", ".join(position),
                file=self.LOG_FILE[0],
            )
            self.LOG_FILE[0].flush()

            def convert(raw, sensitivity):
                return (raw * M2MM) / sensitivity

            vmsTimestamp = vmsData.timestamp

            for j in range(50):
                print(
                    vmsTimestamp,
                    convert(vmsData.accelerationPSDX[j], X1Sensitivity),
                    ",",
                    convert(vmsData.accelerationPSDY[j], Y1Sensitivity),
                    ",",
                    convert(vmsData.sensor1ZAcceleration[j], Z1Sensitivity),
                    ",",
                    convert(vmsData.sensor2XAcceleration[j], X2Sensitivity),
                    ",",
                    convert(vmsData.sensor2YAcceleration[j], Y2Sensitivity),
                    ",",
                    convert(vmsData.sensor2ZAcceleration[j], Z2Sensitivity),
                    ",",
                    convert(vmsData.sensor3XAcceleration[j], X3Sensitivity),
                    ",",
                    convert(vmsData.sensor3YAcceleration[j], Y3Sensitivity),
                    ",",
                    convert(vmsData.sensor3ZAcceleration[j], Z3Sensitivity),
                    file=self.LOG_FILE[1],
                )
                vmsTimestamp += 0.001

            self.LOG_FILE[1].flush()

    async def test_movements(self):
        # Setup VMS
        self.vms = salobj.Remote(self.domain, "MTVMS", index=1)

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

        self.LOG_FILE = [
            open(f'M13T012-IMS-{datetime.now().strftime("%Y-%m-%dT%T")}.csv', "w"),
            open(f'M13T012-VMS-{datetime.now().strftime("%Y-%m-%dT%T")}.csv', "w"),
        ]

        print(
            "Timestamp,xPosition,yPosition,zPosition,xRotation,yRotation,zRotation",
            file=self.LOG_FILE[0],
        )
        print(
            "Timestamp (s),X1 (m/s^2),Y1 (m/s^2),Z1 (m/s^2),X2 (m/s^2),Y2 (m/s^2),Z2 (m/s^2),X3 (m/s^2),Y3 (m/s^2),Z3 (m/s^2)",
            file=self.LOG_FILE[1],
        )

        # The matrix need to be tested 3 times
        for i in range(3):
            await self.do_movements(
                offsets,
                "M13T-011: Position Stability During Active Mode Operation",
                end_state=MTM1M3.DetailedState.STANDBY,
                moved_callback=self._log_data,
            )


if __name__ == "__main__":
    asynctest.main()
