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
import astropy.units as u


__all__ = ["MTM1M3Movements"]


class MTM1M3Movements(MTM1M3Test):
    # edit the defined reference positions as needed.
    # XYZ in m, R[XYZ] in deg
    REFERENCE = np.array([0.0] * 6)

    POSITION_TOLERANCE = (8 * u.um).to(u.m).value
    ROTATION_TOLERANCE = 0.00000209
    LOAD_PATH_FORCE = 0.0
    LOAD_PATH_TOLERANCE = 0.0

    LOG_FILE = None
    LOG_MOVEMENT = None

    async def tearDown(self):
        if self.LOG_FILE is not None:
            self.close_log_file()
        await super().tearDown()

    def _check_position(
        self, position, tolerance=POSITION_TOLERANCE, checkForces=False
    ):
        data = self.m1m3.tel_hardpointActuatorData.get()
        imsData = self.m1m3.tel_imsData.get()

        if self.LOG_FILE:
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

        self.assertAlmostEqual(data.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(data.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(data.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(data.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(data.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(data.zRotation, position[5], delta=tolerance)
        if checkForces:
            # Verify there are no unintended load paths.
            self.assertAlmostEqual(
                data.fx, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )
            self.assertAlmostEqual(
                data.fy, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )
            self.assertAlmostEqual(
                data.fz, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )
            self.assertAlmostEqual(
                data.mx, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )
            self.assertAlmostEqual(
                data.my, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )
            self.assertAlmostEqual(
                data.mz, self.LOAD_PATH_FORCE, delta=self.LOAD_PATH_TOLERANCE
            )

        self.assertAlmostEqual(imsData.xPosition, position[0], delta=tolerance)
        self.assertAlmostEqual(imsData.yPosition, position[1], delta=tolerance)
        self.assertAlmostEqual(imsData.zPosition, position[2], delta=tolerance)
        self.assertAlmostEqual(imsData.xRotation, position[3], delta=tolerance)
        self.assertAlmostEqual(imsData.yRotation, position[4], delta=tolerance)
        self.assertAlmostEqual(imsData.zRotation, position[5], delta=tolerance)

    async def _wait_HP(self):
        async def wait_for(states, timeout=100):
            while True:
                data = self.m1m3.evt_hardpointActuatorState.get()
                not_met = 0
                for hp in range(6):
                    if data.motionState[hp] not in states:
                        not_met += 1
                if not_met == 0 or timeout < 0:
                    break
                await asyncio.sleep(0.1)
                timeout -= 0.1

        await wait_for(
            (
                MTM1M3.HardpointActuatorMotionStates.STEPPING,
                MTM1M3.HardpointActuatorMotionStates.CHASING,
                MTM1M3.HardpointActuatorMotionStates.QUICKPOSITIONING,
                MTM1M3.HardpointActuatorMotionStates.FINEPOSITIONING,
            ),
            1,
        )
        await wait_for((MTM1M3.HardpointActuatorMotionStates.STANDBY,))

    async def do_movements(
        self,
        offsets,
        start_state=MTM1M3.DetailedState.ACTIVEENGINEERING,
        end_state=MTM1M3.DetailedState.PARKED,
    ):
        """Run tests movements.

        Parameters
        ----------
        offsets : array of 6 members float tuples
            Movements (from 0 position) as X, Y, Z and Rx, Ry and Rz (rotation). Position shall be specified in u.m or similar, rotation as u.deg or similar.
        start_state : `int`, MTM1M3.DetailedState
            Starts tests at this state
        end_state : `int`, MTM1M3.DetailedState
            When tests are successfully finished, transition mirror to this state.
        """

        click.echo(
            click.style(
                "M13T-009: Mirror Support System Active Motion Range",
                bold=True,
                fg="cyan",
            )
        )

        await self.startup(start_state)

        # make sure the HardpointCorrection is disabled.
        await self.m1m3.cmd_disableHardpointCorrections.start()
        await asyncio.sleep(5.0)

        # confirm mirror at reference position.
        self.LOG_MOVEMENT = "startup reference"
        self._check_position(self.REFERENCE)

        for row in offsets:
            self.LOG_MOVEMENT = f"X {row[0].to(u.mm):.02f} Y {row[1].to(u.mm):.02f} Z {row[2].to(u.mm):.02f} RX {row[3].to(u.arcsec):.02f} RY {row[4].to(u.arcsec):.02f} RZ {row[5].to(u.arcsec):.02f}"
            click.echo(click.style(f"Moving {self.LOG_MOVEMENT}", fg="bright_blue",))

            position = (
                list(map(lambda x: x.to(u.m).value, row[:3]))
                + list(map(lambda y: y.to(u.deg).value, row[3:]))
            ) + self.REFERENCE
            await self.m1m3.cmd_positionM1M3.set_start(
                xPosition=row[0].to(u.m).value,
                yPosition=row[1].to(u.m).value,
                zPosition=row[2].to(u.m).value,
                xRotation=row[3].to(u.deg).value,
                yRotation=row[4].to(u.deg).value,
                zRotation=row[5].to(u.deg).value,
            )
            await self._wait_HP()

            await asyncio.sleep(3.0)

            self._check_position(position, checkForces=True)

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        await self.shutdown(end_state)

    def set_log_file(self, path):
        self.LOG_FILE = open(path, "w")
        print(
            "Movement,HP xPosition, HP yPostion, HP zPosition, HP xRotation, HP yRotation, HP zRotation, IMS xPosition, IMS yPosition, IMS zPosition, IMS xRotation, IMS yRotation, IMS zRotation",
            file=self.LOG_FILE,
        )

    def close_log_file(self):
        self.LOG_FILE.close()
        self.LOG_FILE = None
