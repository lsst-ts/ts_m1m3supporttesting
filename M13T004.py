#!/usr/bin/env python3.8

# This file is part of ts_salobj.
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
# Description:  Individual hardpoint breakaway test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each hardpoint actuator
#   - Perform the following steps for full extension and full retraction
#     - Issue hardpoint step command
#     - Verify hardpoint is moving
#     - Wait for hardpoint motion to complete or a limit switch is operated
#     - Issue stop hardpoint motion command
#     - Verify hardpoint is stopped
#     - Query EFD for hardpoint monitor data for test duration
#     - Query EFD for hardpoint actuator data for test duration
# - Transition from parked engineering to standby state
########################################################################

from MTM1M3Test import *
from lsst.ts.idl.enums import MTM1M3

import asyncio
import asynctest
import click
from datetime import datetime
import os


class M13T004(MTM1M3Test):
    async def hardpoint_move(self, step):
        self.recordFile = open(
            f'{datetime.now().strftime("%Y-%m-%dT%T")}-hardpoint{self.hp}-{step}.csv',
            "w",
        )
        self.recordCounter = 0
        click.echo(
            click.style(
                f"Saving data to {os.path.abspath(self.recordFile.name)}", fg="blue"
            )
        )
        self.recordFile.write(
            f"Timestamp,BreakawayLVDT {self.hp},DisplacementLVDT {self.hp},BreakawayPressure {self.hp}\n"
        )
        self.m1m3.tel_hardpointMonitorData.callback = self.record_data

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
            if (
                hpWarning.limitSwitch1Operated[hpIndex]
                or hpWarning.limitSwitch2Operated[hpIndex]
            ):
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
            # time.sleep(0.5)

        # Stop hardpoint motion
        await self.m1m3.cmd_stopHardpointMotion.start()

        # Verify hardpoint motion has stopped
        self.assertEqual(
            self.m1m3.evt_hardpointActuatorState.get().motionState[hpIndex],
            MTM1M3.HardpointActuatorMotionStates.STANDBY,
        )

        # Give a little buffer room before completing this part of the test
        await asyncio.sleep(1)

        # Get the stop timestamp for collecting data from the EFD
        stopTimestamp = self.m1m3.tel_hardpointActuatorData.get().timestamp

        self.m1m3.tel_hardpointMonitorData.callback = None
        self.recordFile.close()

        # Report the start and stop timestamps to the log
        click.echo(f"Start Timestamp: {startTimestamp:.0f}")
        click.echo(f"Stop Timestamp: {stopTimestamp:.0f}")

        # Generate the hardpoint monitor data file
        # rows = efd.QueryAll("SELECT Timestamp, BreakawayLVDT_%d, DisplacementLVDT_%d, BreakawayPressure_%d FROM m1m3_HardpointMonitorData WHERE Timestamp >= %0.3f AND Timestamp <= %0.3f ORDER BY Timestamp ASC" % (actId, actId, actId, startTimestamp, stopTimestamp))
        # path = GetFilePath("%d-Hardpoint%d-MonitorData.csv" % (int(startTimestamp), actId))
        # Log("File path: %s" % path)
        # file = open(path, "w+")
        # file.write("Timestamp,BreakawayLVDT,DisplacementLVDT,BreakawayPressure\r\n")
        # rowCount = 0
        # for row in rows:
        #    rowCount += 1
        #    file.write("%0.3f,%0.9f,%0.9f,%0.3f\r\n" % (row[0], row[1], row[2], row[3]))
        # file.close()
        # Log("Got %d rows" % rowCount)

        # Generate the hardpoint actuator data file
        # rows = efd.QueryAll("SELECT Timestamp, MeasuredForce_%d, Encoder_%d, Displacement_%d FROM m1m3_HardpointActuatorData WHERE Timestamp >= %0.3f AND Timestamp <= %0.3f ORDER BY Timestamp ASC" % (actId, actId, actId, startTimestamp, stopTimestamp))
        # path = GetFilePath("%d-Hardpoint%d-ActuatorData.csv" % (int(startTimestamp), actId))
        # Log("File path: %s" % path)
        # file = open(path, "w+")
        # file.write("Timestamp,MeasuredForce,Encoder,Displacement\r\n")
        # rowCount = 0
        # for row in rows:
        #    rowCount += 1
        #    file.write("%0.3f,%0.9f,%d,%0.9f\r\n" % (row[0], row[1], row[2], row[3]))
        # file.close()
        # Log("Got %d rows" % rowCount)

    async def record_data(self, data):
        hpIndex = self.hp - 1
        self.recordFile.write(
            f"{data.timestamp:.03f},{data.breakawayLVDT[hpIndex]:.09f},{data.displacementLVDT[hpIndex]:.09f},{data.breakawayPressure[hpIndex]:.03f}\n"
        )
        self.recordCounter += 1
        if self.recordCounter > 10:
            self.recordFile.flush()
            self.recordCounter = 0

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

    async def test_hardpoints(self):
        await self.startup(MTM1M3.DetailedState.PARKEDENGINEERING)

        # Iterate through the 6 hardpoint actuators
        for hp in range(1, 7):
            await self.hardpoint_test(hp)


if __name__ == "__main__":
    asynctest.main()
