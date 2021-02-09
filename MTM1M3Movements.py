# This file is part of M1M3 Support System test suite.
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

from MTM1M3Test import MTM1M3Test

from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest
import time
import click
import numpy as np


__all__ = ["MTM1M3Movements"]


class MTM1M3Movements(MTM1M3Test):
    # edit the defined reference positions as needed.
    # XYZ in m, R[XYZ] in deg
    REFERENCE = np.array([0.0] * 6)

    POSITION_TOLERANCE = 0.000008
    ROTATION_TOLERANCE = 0.00000209
    LOAD_PATH_FORCE = 0.0
    LOAD_PATH_TOLERANCE = 0.0

    def _check_position(
        self, position, tolerance=POSITION_TOLERANCE, checkForces=False
    ):
        data = self.m1m3.tel_hardpointActuatorData.get()
        self.assertAlmostEqual(data.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(data.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(data.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(data.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(data.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(data.zRotation, position[5], delta=tolerance)
        if checkForces:
            # Verify there are no unintended load paths.
            self.assertAlmostEqual(data.fx, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.fy, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.fz, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.mx, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.my, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)
            self.assertAlmostEqual(data.mz, LOAD_PATH_FORCE, delta=LOAD_PATH_TOLERANCE)

        imsData = self.m1m3.tel_imsData.get()
        self.assertAlmostEqual(imsData.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(imsData.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(imsData.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(imsData.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(imsData.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(imsData.zRotation, position[5], delta=tolerance)

    async def _wait_HP(self):
        async def wait_for(state):
            while True:
                data = self.m1m3.tel_hardpointActuatorData.get()
                for hp in range(6):
                    if data.motionState[hp] != state:
                        await asyncio.sleep(0.1)
                        continue
                break

        wait_for(MTM1M3.HardpointActuatorMotionStates.STEPPING)
        wait_for(MTM1M3.HardpointActuatorMotionStates.STANDBY)

    async def do_movements(self, offsets):
        click.echo(
            click.style(
                "M13T-009: Mirror Support System Active Motion Range",
                bold=True,
                fg="cyan",
            )
        )

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # make sure the HardpointCorrection is disabled.
        await self.m1m3.cmd_disableHardpointCorrections.start()
        await asyncio.sleep(5.0)

        # confirm mirror at reference position.
        self._check_position(self.REFERENCE)

        for row in offsets:
            click.echo(
                click.style(
                    "Moving X {row[0].to(u.mm):.02f} Y {row[1].to(u.mm):.02f} Z {row[2].to(u.mm):.02f} RX {row[3].to(u.arcsec):.02f} RY {row[4].to(u.arcsec):.02f} RZ {row[5].to(u.arcsec):.02f}",
                    fg="navy",
                )
            )

            position = (
                list(map(lambda x: x.to(u.m).value, row[:3]))
                + list(map(lambda y: y.to(u.deg).value, row[3:]))
            ) + REFERENCE
            await self.m1m3.cmd_positionM1M3.set_start(
                xPosition=row[0],
                yPosition=row[1],
                zPosition=row[2],
                xRotation=row[3],
                yRotation=row[4],
                zRotation=row[5],
            )
            self._wait_HP()

            time.sleep(3.0)

            self._check_position(position, checkForces=True)

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        await self.m1m3.cmd_lowerM1M3.start()