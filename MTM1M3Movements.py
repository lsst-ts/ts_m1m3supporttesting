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

import asyncio
import os
from datetime import datetime

import astropy.units as u
import click
from lsst.ts.idl.enums import MTM1M3

from AutoFlush import AutoFlush
from MTM1M3Test import MTM1M3Test

__all__ = ["MTM1M3Movements", "offset"]

ZERO_M = 0 * u.m
ZERO_DEG = 0 * u.deg


def offset(
    x=ZERO_M, y=ZERO_M, z=ZERO_M, rx=ZERO_DEG, ry=ZERO_DEG, rz=ZERO_DEG
):
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


class ForceOffsets:
    def __init__(
        self, xForces=None, yForces=None, zForces=None, zActiveForces=None
    ):
        self.xForces = xForces
        self.yForces = yForces
        self.zForces = zForces
        self.zActiveForces = zActiveForces

    def getOffsetForces(self):
        if (
            self.xForces is None
            and self.yForces is None
            and self.zForces is None
        ):
            return None
        return {
            "xForces": self.xForces,
            "yForces": self.yForces,
            "zForces": self.zForces,
        }

    def getActiveOffsets(self):
        if self.zActiveForces is None:
            return None
        return {"zForces": self.zActiveForces}

    def getXForce(self, xIndex, default=0):
        return default if self.xForces is None else self.xForces[xIndex]

    def getYForce(self, yIndex, default=0):
        return default if self.yForces is None else self.yForces[yIndex]

    def getZOffsetForce(self, zIndex, default=0):
        return default if self.zForces is None else self.zForces[zIndex]

    def getZActiveForce(self, zIndex, default=0):
        return (
            default
            if self.zActiveForces is None
            else self.zActiveForces[zIndex]
        )

    def __str__(self):
        ret = ""
        if not (
            self.xForces is None
            and self.yForces is None
            and self.zForces is None
        ):
            ret += "OffsetsForces:"
            if self.xForces is not None:
                ret += f" X {sum(self.xForces):.2f}"
            if self.yForces is not None:
                ret += f" Y {sum(self.yForces):.2f}"
            if self.zForces is not None:
                ret += f" Z {sum(self.zForces):.2f}"
            ret += " "

        if not (self.zActiveForces is None):
            ret += f"ActiveOffsets: Z {sum(self.zActiveForces):.2f}"

        return ret


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

    # Base force, moments and their tolerances were
    # measured on the mirror. Adjust as needed.
    LOAD_PATH_FORCE = [275, 55, 1950] * u.N
    LOAD_PATH_FORCE_TOLERANCE = [200, 200, 200] * u.N
    LOAD_PATH_MOMENTS = [1000, 232, 480] * u.N * u.m
    LOAD_PATH_MOMENTS_TOLERANCE = [200, 200, 200] * u.N * u.m

    MEASURED_FORCE_TOLERANCE = 5
    APPLIED_SUM_FORCES_TOLERANCE = 0.001

    POS_IMS_TOLERANCE = 50 * POSITION_TOLERANCE
    ROT_IMS_TOLERANCE = 50 * ROTATION_TOLERANCE

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
                data.fx * u.N,
                self.LOAD_PATH_FORCE[0],
                delta=self.LOAD_PATH_FORCE_TOLERANCE[0],
                msg="Force X out of limit",
            )
            self.assertAlmostEqual(
                data.fy * u.N,
                self.LOAD_PATH_FORCE[1],
                delta=self.LOAD_PATH_FORCE_TOLERANCE[1],
                msg="Force Y out of limit",
            )
            self.assertAlmostEqual(
                data.fz * u.N,
                self.LOAD_PATH_FORCE[2],
                delta=self.LOAD_PATH_FORCE_TOLERANCE[2],
                msg="Force Z out of limit",
            )
            self.assertAlmostEqual(
                data.mx * u.N * u.m,
                self.LOAD_PATH_MOMENTS[0],
                delta=self.LOAD_PATH_MOMENTS_TOLERANCE[0],
                msg="Moment X out of limit",
            )
            self.assertAlmostEqual(
                data.my * u.N * u.m,
                self.LOAD_PATH_MOMENTS[1],
                delta=self.LOAD_PATH_MOMENTS_TOLERANCE[1],
                msg="Moment Y out of limit",
            )
            self.assertAlmostEqual(
                data.mz * u.N * u.m,
                self.LOAD_PATH_MOMENTS[2],
                delta=self.LOAD_PATH_MOMENTS_TOLERANCE[2],
                msg="Moment Z out of limit",
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
                    f"X {self.IMS_OFFSETS[0]*pos_fac:.04f} "
                    f"{pos_unit.to_string()} "
                    f"Y {self.IMS_OFFSETS[1]*pos_fac:.04f} "
                    f"{pos_unit.to_string()} "
                    f"Z {self.IMS_OFFSETS[2]*pos_fac:.04f} "
                    f"{pos_unit.to_string()} "
                    f"rX {self.IMS_OFFSETS[3]*rot_fac:.04f} "
                    f"{rot_unit.to_string()} "
                    f"rY {self.IMS_OFFSETS[4]*rot_fac:.04f} "
                    f"{rot_unit.to_string()} "
                    f"rZ {self.IMS_OFFSETS[5]*rot_fac:.04f} "
                    f"{rot_unit.to_string()}",
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
                msg=f"IMS {kind} out of limit, CHECK IMS calibration "
                "(DisplacementSensorSettings.yaml)",
            )
            if abs(value - target) > normal_tol:
                click.echo(
                    click.style(
                        f"IMS out of normal limits - {kind} target "
                        f"{target:.04f} is {value:.04f}, "
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
            Movements (from 0 position) as X, Y, Z and Rx, Ry and Rz
            (rotation). Position shall be specified in u.m or similar, rotation
            as u.deg or similar.
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
        await self.m1m3.cmd_disableHardpointCorrections.start()

        await asyncio.sleep(wait)

        click.echo(
            click.style(
                "Moving to reference",
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
            self.LOG_MOVEMENT = (
                f"X {row[0].to(u.mm):.02f} "
                f"Y {row[1].to(u.mm):.02f} "
                f"Z {row[2].to(u.mm):.02f} "
                f"RX {row[3].to(u.arcsec):.02f} "
                f"RY {row[4].to(u.arcsec):.02f} "
                f"RZ {row[5].to(u.arcsec):.02f}"
            )

            click.echo(
                click.style(
                    f"Moving {self.LOG_MOVEMENT}",
                    fg="bright_blue",
                )
            )

            position = [
                row[i] + self.REFERENCE[i] for i in range(len(self.REFERENCE))
            ]
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

    async def hardpoint_move(self, step):
        self.hardpointActuatorDataFile = AutoFlush(self.openCSV(f"HP-{self.hp}-{step}"))

        self.hardpointMonitorDataFile = AutoFlush(
            self.openCSV(f"Monitor-{self.hp}-{step}")
        )
        click.echo(
            click.style(
                f"Saving data to {os.path.abspath(self.hardpointActuatorDataFile.name)} and {os.path.abspath(self.hardpointMonitorDataFile.name)}",
                fg="blue",
            )
        )
        self.hardpointActuatorDataFile.print(
            f"Timestamp,Steps Queued {self.hp},Measured Force {self.hp},Encoder {self.hp},Displacement {self.hp},Lower Limit Switch {self.hp},Upper Limit Switch {self.hp}",
        )
        self.m1m3.tel_hardpointActuatorData.callback = self.hardpointActuatorData

        self.hardpointMonitorDataFile.print(
            f"Timestamp,BreakawayLVDT {self.hp},DisplacementLVDT {self.hp},BreakawayPressure {self.hp}",
        )
        self.m1m3.tel_hardpointMonitorData.callback = self.hardpointMonitorData

        # Give time for a sample
        await asyncio.sleep(1)

        # Get the start timestamp for collecting data from the EFD
        startTimestamp = self.m1m3.tel_hardpointActuatorData.get().timestamp

        # Setup the simulator response (ignored if running at CAID)
        # sim.setHPForceAndStatus(actId, 0, 100 + index, 0)
        # sim.setILCStatus(actId, 0, 0x0000, 0)

        hpIndex = self.hp - 1

        # Command the steps
        tmp = [0] * 6
        tmp[hpIndex] = step
        await self.m1m3.cmd_moveHardpointActuators.set_start(steps=tmp)
        click.echo(click.style(f"Moving {self.hp} {step}", fg="green"))

        # Wait a bit
        await asyncio.sleep(1)

        # Verify the commanded actuator is moving
        self.assertEqual(
            self.m1m3.evt_hardpointActuatorState.get().motionState[hpIndex],
            MTM1M3.HardpointActuatorMotionStates.STEPPING,
        )

        # Wait for moving to complete or a limit switch is hit
        loopCount = 0
        while True:
            # Check if moving is complete
            if (
                self.m1m3.evt_hardpointActuatorState.get().motionState[hpIndex]
                == MTM1M3.HardpointActuatorMotionStates.STANDBY
            ):
                break

            # Check if limit switch is hit
            hpWarning = self.m1m3.evt_hardpointActuatorWarning.get()
            if (hpWarning.limitSwitch1Operated[hpIndex] and step > 0) or (
                hpWarning.limitSwitch2Operated[hpIndex] and step < 0
            ):
                click.echo(
                    click.style(
                        f"Limit switch on HP {self.hp} reached on {step} command - 1: {hpWarning.limitSwitch1Operated[hpIndex]} 2: {hpWarning.limitSwitch2Operated[hpIndex]}",
                        fg="yellow",
                    )
                )
                break

            status = 0

            # For simulation testing toggle a limit switch after 10 seconds
            # hpData = self.m1m3.tel_hardpointActuatorData.get()
            # currentTimestamp = hpData.timestamp
            # status1 = 0
            # status2 = 0
            # if abs(currentTimestamp - startTimestamp) >= 10.0:
            #    status1 = 0x04 + 0x08
            #    status2 = 0x0100 + 0x0200
            # sim.setHPForceAndStatus(actId, status1, loopCount, loopCount * 2)
            # sim.setILCStatus(actId, 0, status2, 0)
            # loopCount += 1

            await asyncio.sleep(0.5)

        # Stop hardpoint motion
        await self.m1m3.cmd_stopHardpointMotion.start()

        # Give a little buffer room before completing this part of the test
        await asyncio.sleep(1)

        # Verify hardpoint motion has stopped
        self.assertEqual(
            self.m1m3.evt_hardpointActuatorState.get().motionState[hpIndex],
            MTM1M3.HardpointActuatorMotionStates.STANDBY,
        )

        # Get the stop timestamp for collecting data from the EFD
        stopTimestamp = self.m1m3.tel_hardpointActuatorData.get().timestamp

        self.m1m3.tel_hardpointActuatorData.callback = None
        self.m1m3.tel_hardpointMonitorData.callback = None

        # Report the start and stop timestamps to the log
        click.echo(f"Start Timestamp: {startTimestamp:.0f}")
        click.echo(f"Stop Timestamp: {stopTimestamp:.0f}")

    async def hardpointActuatorData(self, data):
        hpIndex = self.hp - 1

        warnings = self.m1m3.evt_hardpointActuatorWarning.get()
        if warnings is None:
            s_high = "-"
            s_low = "-"
        else:
            s_low = warnings.limitSwitch2Operated[hpIndex]
            s_high = warnings.limitSwitch1Operated[hpIndex]

        self.hardpointActuatorDataFile.print(
            f"{data.timestamp:.03f},{data.stepsQueued[hpIndex]:.09f},{data.measuredForce[hpIndex]:.09f},{data.encoder[hpIndex]:d},{data.displacement[hpIndex]:.09f},{s_low},{s_high}",
        )

    async def hardpointMonitorData(self, data):
        hpIndex = self.hp - 1

        self.hardpointMonitorDataFile.print(
            f"{data.timestamp:.03f},{data.breakawayLVDT[hpIndex]:.09f},{data.displacementLVDT[hpIndex]:.09f},{data.breakawayPressure[hpIndex]:.03f}",
        )

    async def hardpoint_test(self, hp):
        self.hp = hp
        click.echo(click.style(f"Hardpoint Actuator {self.hp}", bold=True, fg="cyan"))

        # Issue through a number of steps for each actuator
        with click.progressbar(
            [-999999999, 999999999],
            label=click.style("Stepping HP", fg="green"),
            item_show_func=lambda a: str(a),
            show_pos=True,
            width=0,
        ) as bar:
            for step in bar:
                await self.hardpoint_move(step)

    async def _check_forces_sum(self, forces):
        elevationForces = self.m1m3.tel_appliedElevationForces.get()
        staticForces = self.m1m3.evt_appliedStaticForces.get()
        offsetForces = self.m1m3.evt_appliedOffsetForces.get()
        activeForces = self.m1m3.evt_appliedActiveOpticForces.get()
        appliedForces = self.m1m3.tel_appliedForces.get()
        measuredForces = self.m1m3.tel_forceActuatorData.get()
        if (
            elevationForces is None
            or staticForces is None
            or offsetForces is None
            or activeForces is None
            or appliedForces is None
            or measuredForces is None
        ):
            self.printError(
                "Something is wrong - "
                f"elevationForces {elevationForces} "
                f"appliedForces {appliedForces} "
                f"staticForces {staticForces} "
                f"offsetForces {offsetForces} "
                f"activeForces {activeForces} "
                f"measuredForces {measuredForces} "
            )
            return

        for xIndex in range(12):
            self.assertAlmostEqual(
                forces.getXForce(xIndex, self.lastXForces[xIndex]),
                offsetForces.xForces[xIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg=f"{xIndex} X Offset != appliedOffset",
            )

            self.assertAlmostEqual(
                sum(
                    [
                        elevationForces.xForces[xIndex],
                        staticForces.xForces[xIndex],
                        forces.getXForce(xIndex, self.lastXForces[xIndex]),
                    ]
                ),
                appliedForces.xForces[xIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg=f"Applied xForce for {xIndex} doesn't match sum of "
                f"{elevationForces.xForces[xIndex]}, "
                f"{staticForces.xForces[xIndex]}, and"
                f"{forces.getXForce(xIndex, self.lastXForces[xIndex])}",
            )

            self.assertAlmostEqual(
                appliedForces.xForces[xIndex],
                measuredForces.xForce[xIndex],
                delta=self.MEASURED_FORCE_TOLERANCE,
                msg=f"Applied xForce for {xIndex} doesn't match measured",
            )

        for yIndex in range(100):
            self.assertAlmostEqual(
                forces.getYForce(yIndex, self.lastYForces[yIndex]),
                offsetForces.yForces[yIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg=f"{yIndex} Y Offset != appliedOffset",
            )

            self.assertAlmostEqual(
                sum(
                    [
                        elevationForces.yForces[yIndex],
                        staticForces.yForces[yIndex],
                        forces.getYForce(yIndex, self.lastYForces[yIndex]),
                    ]
                ),
                appliedForces.yForces[yIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg=f"Applied yForce for {yIndex} doesn't match sum of "
                f"{elevationForces.yForces[yIndex]}, "
                f"{staticForces.yForces[yIndex]}, and "
                f"{forces.getYForce(yIndex,self.lastYForces[yIndex])}",
            )

            self.assertAlmostEqual(
                appliedForces.yForces[yIndex],
                measuredForces.yForce[yIndex],
                delta=self.MEASURED_FORCE_TOLERANCE,
                msg=f"Applied yForce for {yIndex} doesn't match measured",
            )

        for zIndex in range(156):
            zOffset = forces.getZOffsetForce(zIndex, self.lastZForces[zIndex])
            zActive = forces.getZActiveForce(
                zIndex, self.lastZActiveForces[zIndex]
            )

            self.assertAlmostEqual(
                zOffset,
                offsetForces.zForces[zIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg="{zIndex} Z Offset != appliedOffset",
            )
            self.assertAlmostEqual(
                zActive,
                activeForces.zForces[zIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg="{zIndex} Z Active force != appliedActiveOpticForces",
            )

            self.assertAlmostEqual(
                sum(
                    [
                        elevationForces.zForces[zIndex],
                        staticForces.zForces[zIndex],
                        zOffset,
                        zActive,
                    ]
                ),
                appliedForces.zForces[zIndex],
                delta=self.APPLIED_SUM_FORCES_TOLERANCE,
                msg=f"Applied zForce for {zIndex} doesn't match sum of "
                f"{elevationForces.zForces[zIndex]}, "
                f"{staticForces.zForces[zIndex]}, "
                f"{zOffset}, and {zActive}",
            )

            self.assertAlmostEqual(
                appliedForces.zForces[zIndex],
                measuredForces.zForce[zIndex],
                delta=self.MEASURED_FORCE_TOLERANCE,
                msg=f"Applied zForce for {zIndex} doesn't match measured",
            )

        click.echo(
            click.style(
                f"Offsets OK {forces}",
                fg="green",
            )
        )

    async def resetLastOffsetForces(self):
        self.lastXForces = [0] * 12
        self.lastYForces = [0] * 100
        self.lastZForces = [0] * 156
        self.lastZActiveForces = [0] * 156

        await self.m1m3.cmd_clearOffsetForces.start()
        await self.m1m3.cmd_clearActiveOpticForces.start()

        click.echo(click.style("Clear offsets", fg="bright_blue"))

    async def applyOffsetForces(
        self,
        offsets: hash,
        header: str,
        start_state=MTM1M3.DetailedState.ACTIVEENGINEERING,
        end_state=MTM1M3.DetailedState.PARKED,
        check_forces: bool = True,
        moved_callback: bool = None,
        wait: float = 8.0,
    ) -> None:
        """Run tests movements.

        Parameters
        ----------
        offsets : `map`
            Map of xForces, yForces and zForces offsets and zActiveForces for
            active optics forces.
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

        self.printHeader(header)

        if start_state is not None:
            await self.startup(start_state)

        # make sure the HardpointCorrection is disabled.
        await self.m1m3.cmd_disableHardpointCorrections.start()

        await self.resetLastOffsetForces()

        await asyncio.sleep(wait)

        for row in offsets:
            click.echo(
                click.style(
                    f"Offsets {str(row)}",
                    fg="bright_blue",
                )
            )

            offset = row.getOffsetForces()
            active = row.getActiveOffsets()

            if offset is not None:
                await self.m1m3.cmd_applyOffsetForces.set_start(**offset)

            if active is not None:
                await self.m1m3.cmd_applyActiveOpticForces.set_start(**active)

            await asyncio.sleep(wait)

            await self._check_forces_sum(row)

            if offset is not None:
                self.lastXForces = row.xForces
                self.lastYForces = row.yForces
                self.lastZForces = row.zForces

            if active is not None:
                self.lastZActiveForces = row.zActiveForces

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror if requested
        if end_state is not None:
            await self.shutdown(end_state)

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
