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
import click
import astropy.units as u
from datetime import datetime

__all__ = ["MTM1M3Movements", "offset"]

ZERO_M = 0 * u.m
ZERO_DEG = 0 * u.deg


def offset(x=ZERO_M, y=ZERO_M, z=ZERO_M, rx=ZERO_DEG, ry=ZERO_DEG, rz=ZERO_DEG):
    """Generate offset vector for MTM1M3Movements.do_movements method.

    Note
    ----
    Input parameters are astropy quantities. Those need to be prepared. As in
    this code:

    import astropy.units as u

    offsets = [
       offset(x=1 * u.mm, z=-0.23 * u.mm),
       offset(rx=0.45 * u.arcsec, z=-0.23 * u.mm),
    ]

    Parameters
    ----------
    x : `float`, units.m, optional
        Translation along x axis. Defaults to 0m.
    y : `float`, units.m, optional
        Translation along y axis. Defaults to 0m.
    z : `float`, units.m, optional
        Translation along z axis. Defaults to 0m.
    rx : `float`, units.deg, optional
        Rotation along x axis. Defaults to 0deg.
    ry : `float`, units.deg, optional
        Rotation along y axis. Defaults to 0deg.
    rz : `float`, units.deg, optional
        Rotation along z axis. Defaults to 0deg.

    Returns
    -------
    offset : array[6] of `float`
        Offset vector. Translation
    """
    return [x, y, z, rx, ry, rz]


class MTM1M3Movements(MTM1M3Test):

    POS_DATA_UNIT = u.m
    ROT_DATA_UNIT = u.deg

    POS_IMS_UNIT = u.m
    ROT_IMS_UNIT = u.deg

    POS_TOL_UNIT = u.um
    ROT_TOL_UNIT = u.arcsec

    # edit the defined reference positions as needed.
    # XYZ in um, R[XYZ] in arcsec
    REFERENCE = [0.0 * u.um] * 3 + [0.0 * u.arcsec] * 3

    POSITION_TOLERANCE = 8 * POS_TOL_UNIT
    ROTATION_TOLERANCE = 1.45 * ROT_TOL_UNIT
    LOAD_PATH_FORCE = 0.0
    LOAD_PATH_TOLERANCE = 100.0
    POS_IMS_TOLERANCE = 5 * POSITION_TOLERANCE
    ROT_IMS_TOLERANCE = 5 * ROTATION_TOLERANCE

    LOG_FILE = None
    LOG_MOVEMENT = None

    IMS_OFFSETS = [0] * 6

    async def tearDown(self):
        if self.LOG_FILE is not None:
            self.close_log_file()
        await super().tearDown()

    async def _check_position(
        self,
        position,
        position_tolerance=POSITION_TOLERANCE,
        rotation_tolerance=ROTATION_TOLERANCE,
        pos_ims_tolerance=POS_IMS_TOLERANCE,
        rot_ims_tolerance=ROT_IMS_TOLERANCE,
        check_forces: bool = False,
        check_IMS: bool = True,
        reference_IMS: bool = False,
    ) -> None:
        data = self.m1m3.tel_hardpointActuatorData.get()
        imsData = self.m1m3.tel_imsData.get()

        if self.moved_callback is not None:
            await self.moved_callback(position, data, imsData)

        self.assertAlmostEqual(
            (data.xPosition * self.POS_DATA_UNIT).to(self.POS_TOL_UNIT),
            position[0].to(self.POS_TOL_UNIT),
            delta=position_tolerance,
            msg="HP xPosition out of limit",
        )
        self.assertAlmostEqual(
            (data.yPosition * self.POS_DATA_UNIT).to(self.POS_TOL_UNIT),
            position[1].to(self.POS_TOL_UNIT),
            delta=position_tolerance,
            msg="HP yPosition out of limit",
        )
        self.assertAlmostEqual(
            (data.zPosition * self.POS_DATA_UNIT).to(self.POS_TOL_UNIT),
            position[2].to(self.POS_TOL_UNIT),
            delta=position_tolerance,
            msg="HP zPosition out of limit",
        )
        self.assertAlmostEqual(
            (data.xRotation * self.ROT_DATA_UNIT).to(self.ROT_TOL_UNIT),
            position[3].to(self.ROT_TOL_UNIT),
            delta=rotation_tolerance,
            msg="HP xRotation out of limit",
        )
        self.assertAlmostEqual(
            (data.yRotation * self.ROT_DATA_UNIT).to(self.ROT_TOL_UNIT),
            position[4].to(self.ROT_TOL_UNIT),
            delta=rotation_tolerance,
            msg="HP yRotation out of limit",
        )
        self.assertAlmostEqual(
            (data.zRotation * self.ROT_DATA_UNIT).to(self.ROT_TOL_UNIT),
            position[5].to(self.ROT_TOL_UNIT),
            delta=rotation_tolerance,
            msg="HP zRotation out of limit",
        )
        if check_forces:
            # Verify there are no unintended load paths.
            self.assertAlmostEqual(
                data.fx,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="FX out of limit",
            )
            self.assertAlmostEqual(
                data.fy,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="FY out of limit",
            )
            self.assertAlmostEqual(
                data.fz,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="FZ out of limit",
            )
            self.assertAlmostEqual(
                data.mx,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="MX out of limit",
            )
            self.assertAlmostEqual(
                data.my,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="MY out of limit",
            )
            self.assertAlmostEqual(
                data.mz,
                self.LOAD_PATH_FORCE,
                delta=self.LOAD_PATH_TOLERANCE,
                msg="MZ out of limit",
            )

        if reference_IMS is True:
            self.IMS_OFFSETS = [
                imsData.xPosition,
                imsData.yPosition,
                imsData.zPosition,
                imsData.xRotation,
                imsData.yRotation,
                imsData.zRotation,
            ]

            pos_unit = u.mm
            rot_unit = u.arcsec

            pos_fac = self.POS_IMS_UNIT.to(pos_unit)
            rot_fac = self.ROT_IMS_UNIT.to(rot_unit)

            click.echo(
                click.style(
                    f"IMS referenced at: "
                    f"X {self.IMS_OFFSETS[0]*pos_fac:.04f} {pos_unit.to_string()} "
                    f"Y {self.IMS_OFFSETS[1]*pos_fac:.04f} {pos_unit.to_string()} "
                    f"Z {self.IMS_OFFSETS[2]*pos_fac:.04f} {pos_unit.to_string()} "
                    f"rX {self.IMS_OFFSETS[3]*rot_fac:.04f} {rot_unit.to_string()} "
                    f"rY {self.IMS_OFFSETS[4]*rot_fac:.04f} {rot_unit.to_string()} "
                    f"rZ {self.IMS_OFFSETS[5]*rot_fac:.04f} {rot_unit.to_string()}",
                    fg="red",
                )
            )

        if check_IMS is False:
            return

        def ims_check(kind, value, target, ims_tol, normal_tol):
            self.assertAlmostEqual(
                value,
                target,
                delta=ims_tol,
                msg=f"IMS {kind} out of limit, CHECK IMS calibration (DisplacementSensorSettings.yaml)",
            )
            if abs(value - target) > normal_tol:
                click.echo(
                    click.style(
                        f"IMS out of normal limits - {kind} target {target:.04f} is {value:.04f}, "
                        f"difference {target-value:.04f}",
                        fg="red",
                    )
                )

        ims_check(
            "position X",
            ((imsData.xPosition - self.IMS_OFFSETS[0]) * self.POS_IMS_UNIT).to(
                self.POS_TOL_UNIT
            ),
            position[0].to(self.POS_TOL_UNIT),
            pos_ims_tolerance,
            position_tolerance,
        )

        ims_check(
            "position Y",
            ((imsData.yPosition - self.IMS_OFFSETS[1]) * self.POS_IMS_UNIT).to(
                self.POS_TOL_UNIT
            ),
            position[1].to(self.POS_TOL_UNIT),
            pos_ims_tolerance,
            position_tolerance,
        )

        ims_check(
            "position Z",
            ((imsData.zPosition - self.IMS_OFFSETS[2]) * self.POS_IMS_UNIT).to(
                self.POS_TOL_UNIT
            ),
            position[2].to(self.POS_TOL_UNIT),
            pos_ims_tolerance,
            position_tolerance,
        )

        ims_check(
            "rotation X",
            ((imsData.xRotation - self.IMS_OFFSETS[3]) * self.ROT_IMS_UNIT).to(
                self.ROT_TOL_UNIT
            ),
            position[3].to(self.ROT_TOL_UNIT),
            rot_ims_tolerance,
            rotation_tolerance,
        )

        ims_check(
            "rotation Y",
            ((imsData.yRotation - self.IMS_OFFSETS[4]) * self.ROT_IMS_UNIT).to(
                self.ROT_TOL_UNIT
            ),
            position[4].to(self.ROT_TOL_UNIT),
            rot_ims_tolerance,
            rotation_tolerance,
        )

        ims_check(
            "rotation Z",
            ((imsData.zRotation - self.IMS_OFFSETS[5]) * self.ROT_IMS_UNIT).to(
                self.ROT_TOL_UNIT
            ),
            position[5].to(self.ROT_TOL_UNIT),
            rot_ims_tolerance,
            rotation_tolerance,
        )

    async def waitHP(self):
        """Wait for HP to go through Moving to Idle states."""

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
        header,
        start_state=MTM1M3.DetailedState.ACTIVEENGINEERING,
        end_state=MTM1M3.DetailedState.PARKED,
        check_forces: bool = True,
        moved_callback: bool = None,
        wait: float = 4.0,
    ) -> None:
        """Run tests movements.

        Parameters
        ----------
        offsets : array of 6 members float tuples
            Movements (from 0 position) as X, Y, Z and Rx, Ry and Rz (rotation). Position shall be specified in u.m or similar, rotation as u.deg or similar.
        header : `str`
            Test header. Echoed at test startup.
        start_state : `int`, MTM1M3.DetailedState, optional
            Starts tests at this state. Defaults to ACTIVEENGINEERING. None =
            no transition.
        end_state : `int`, MTM1M3.DetailedState, optional
            When tests are successfully finished, transition mirror to this
            state. None = no transition. Defaults to
            MTM1M3.DetailedState.PARKED
        moved_callback : `function`, optional
            If not None, called after mirror moved to new position. Its three
            arguments are target position, hardpoint data and IMS data.
        wait : `float`, optional
            Wait for given number of seconds to settled down after movement is
            completed before checking it.
        """

        self.moved_callback = moved_callback

        self.printHeader(header)

        if start_state is not None:
            await self.startup(start_state)

        # make sure the HardpointCorrection is disabled.
        if check_forces is True:
            await self.m1m3.cmd_enableHardpointCorrections.start()
        else:
            await self.m1m3.cmd_disableHardpointCorrections.start()
        await asyncio.sleep(wait)

        click.echo(
            click.style(
                f"Moving to reference",
                fg="green",
            )
        )

        # confirm mirror at reference position.
        self.LOG_MOVEMENT = "startup reference"
        await self.m1m3.cmd_positionM1M3.set_start(
            xPosition=self.REFERENCE[0].to(u.m).value,
            yPosition=self.REFERENCE[1].to(u.m).value,
            zPosition=self.REFERENCE[2].to(u.m).value,
            xRotation=self.REFERENCE[3].to(u.deg).value,
            yRotation=self.REFERENCE[4].to(u.deg).value,
            zRotation=self.REFERENCE[5].to(u.deg).value,
        )
        await self.waitHP()

        await asyncio.sleep(wait)

        await self._check_position(
            self.REFERENCE, check_forces=check_forces, reference_IMS=True
        )

        for row in offsets:
            self.LOG_MOVEMENT = f"X {row[0].to(u.mm):.02f} Y {row[1].to(u.mm):.02f} Z {row[2].to(u.mm):.02f} RX {row[3].to(u.arcsec):.02f} RY {row[4].to(u.arcsec):.02f} RZ {row[5].to(u.arcsec):.02f}"
            click.echo(
                click.style(
                    f"Moving {self.LOG_MOVEMENT}",
                    fg="bright_blue",
                )
            )

            position = [row[i] + self.REFERENCE[i] for i in range(len(self.REFERENCE))]
            await self.m1m3.cmd_positionM1M3.set_start(
                xPosition=row[0].to(u.m).value,
                yPosition=row[1].to(u.m).value,
                zPosition=row[2].to(u.m).value,
                xRotation=row[3].to(u.deg).value,
                yRotation=row[4].to(u.deg).value,
                zRotation=row[5].to(u.deg).value,
            )
            await self.waitHP()

            await asyncio.sleep(wait)

            await self._check_position(position, check_forces=False)

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror if requested
        if end_state is not None:
            await self.shutdown(end_state)

        self.moved_callback = None

    def openCSV(self, name):
        """Opens CVS log file.

        Parameters
        ----------
        name : `str`
            File start name. Filename is contructed using this and timestamp.

        Returns
        -------
        cvsfile : `file`
            File descriptor opened for writing.
        """
        f = open(f'{name}-{datetime.now().strftime("%Y-%m-%dT%T")}.csv', "w")
        if self.LOG_FILE is None:
            self.LOG_FILE = f
        elif isinstance(self.LOG_FILE, list):
            self.LOG_FILE.append(f)
        else:
            self.LOG_FILE = [self.LOG_FILE, f]

        return f

    def close_log_file(self):
        self.moved_callback = None
        if isinstance(self.LOG_FILE, list):
            for f in self.LOG_FILE:
                f.close()
        else:
            self.LOG_FILE.close()
        self.LOG_FILE = None
