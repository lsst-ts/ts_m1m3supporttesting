#!/usr/bin/env python3

# This file is part of M1M3 test suite.
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
# Test Numbers: M13T-004
# Author:       CContaxis
# Description:  Mirror positioning repeatibility after hardpoint breakaways
# Steps:
# - Raise the mirror
# - Record the IMS positions right after the mirror was raised
# - Offset (XYZ) the mirror, record the offsets and IMS positions
# - Lower the mirror
# - Perform the HP breakway test - for each hardpoint actuator, do:
#   - Perform the following steps for full extension and full retraction
#     - Issue hardpoint step command
#     - Verify hardpoint is moving
#     - Wait for hardpoint motion to complete or a limit switch is operated
#     - Issue stop hardpoint motion command
#     - Verify hardpoint is stopped
# - Repeat 3x
########################################################################

from datetime import datetime

import astropy.units as u
import asynctest
import click
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements, offset

TRAVEL_POSITION = 1 * u.mm
TRAVEL_ROTATION = 5 * u.arcsec


class M13T004(MTM1M3Movements):
    async def setUp(self):
        await super().setUp()
        self.step = 1

        start = datetime.now()

        self.IMS_FILE = self.openCSV("M13T016")
        print(
            "# Message,HP.timestamp,HP.xPosition,HP.yPosition,HP.zPosition,"
            + "HP.xRotation,HP.yRotation,HP.zRotation,"
            + ",".join([f"HP.encoder{x}" for x in range(1, 7)])
            + ","
            + ",".join([f"HP.measuredForce{x}" for x in range(1, 7)])
            + ",IMS.timestamp,IMS.xPosition,IMS.yPosition,IMS.zPosition,"
            + "IMS.xRotation,IMS.yRotation,IMS.zRotation,"
            + ",".join([f"IMS.rawSensorData{x}" for x in range(1, 9)]),
            file=self.IMS_FILE,
        )

    def _logIMS(self, message, data, imsData):
        print(
            message,
            data.timestamp,
            data.xPosition,
            data.yPosition,
            data.zPosition,
            data.xRotation,
            data.yRotation,
            data.zRotation,
            ",".join(map(str, data.encoder)),
            ",".join(map(str, data.measuredForce)),
            imsData.timestamp,
            imsData.xPosition,
            imsData.zPosition,
            imsData.xRotation,
            imsData.yRotation,
            imsData.zRotation,
            imsData.zRotation,
            ",".join(map(str, imsData.rawSensorData)),
            file=self.IMS_FILE,
            sep=",",
        )
        self.IMS_FILE.flush()

    async def _after_movement(self, position, data, imsData):
        self._logIMS(f"Step {self.step}", data, imsData)
        self.step += 1

    async def _run(self):
        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        data = await self.m1m3.tel_hardpointActuatorData.next(flush=True)
        imsData = await self.m1m3.tel_imsData.next(flush=True)

        self._logIMS("Raised", data, imsData)

        offsets = [
            offset(x=+TRAVEL_POSITION, y=+TRAVEL_POSITION, z=+TRAVEL_POSITION),
            offset(x=-TRAVEL_POSITION, y=-TRAVEL_POSITION, z=-TRAVEL_POSITION),
            offset(rx=+TRAVEL_ROTATION, ry=+TRAVEL_ROTATION),
            offset(rx=-TRAVEL_ROTATION, ry=-TRAVEL_ROTATION),
            offset(
                z=+TRAVEL_POSITION, rx=-TRAVEL_ROTATION, ry=-TRAVEL_ROTATION
            ),
            offset(
                z=-TRAVEL_POSITION, rx=+TRAVEL_ROTATION, ry=+TRAVEL_ROTATION
            ),
        ]

        await self.do_movements(
            offsets,
            "M13T-016: Mirror positioning repeatibility after hardpoint "
            "breakaways",
            moved_callback=self._after_movement,
            end_state=MTM1M3.DetailedState.PARKEDENGINEERING,
        )

        await self.shutdown(MTM1M3.DetailedState.PARKEDENGINEERING)

        # Iterate through the 6 hardpoint actuators
        for hp in range(1, 7):
            await self.hardpoint_test(hp)

        click.echo(
            click.style(
                "Saved files can be plotted with PlotT004.py",
                fg="blue",
            )
        )

    async def test_hardpoints(self):
        for repeat in range(3):
            await self._run()


if __name__ == "__main__":
    asynctest.main()
