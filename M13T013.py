#!/usr/bin/env python3.8

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
# Test Numbers: M13T-013
# Author:       CContaxis
# Description:  Determination of X, Y, Z Zero Coordinate
# Steps:
# - Transition from standby to active engineering state
# - Disable hardpoint corrections
# - Determine +X position range
# - Determine -X position range
# - Determine +Y position range
# - Determine -Y position range
# - Determine +Z position range
# - Determine -Z position range
# - Determine +Z rotation range
# - Determine -Z rotation range
# - Determine +X rotation range
# - Determine -X rotation range
# - Determine +Y rotation range
# - Determine -Y rotation range
# - Write result file out
# - Transition from active engineering state to standby
########################################################################

import asyncio
import asynctest
import astropy.units as u

from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import *


class M13T013(MTM1M3Movements):
    TRANSLATION_STEP = 1 * u.mm.to(u.m)
    ROTATION_STEP = 5 * u.arcsec.to(u.deg)

    SETTLE_TIME = 3.0
    SAMPLE_TIME = 1.0

    detailsFile = None

    HARDPOINT_TOPICS = [
        "fx",
        "fy",
        "fz",
        "mx",
        "my",
        "mz",
        "xPosition",
        "yPosition",
        "zPosition",
        "xRotation",
        "yRotation",
        "zRotation",
    ]

    HARDPOINT_POSITIONS = HARDPOINT_TOPICS[6:]
    HARDPOINT_FORCES = HARDPOINT_TOPICS[:6]

    async def test_zero_coordinates_determination(self):
        self.printHeader("M13T-013: Determination of X, Y, Z, Zero Coordinate")

        await self.startup(MTM1M3.DetailedState.ACTIVEENGINEERING)

        # Disable hardpoint corrections
        await self.m1m3.cmd_disableHardpointCorrections.start()

        # Wait for corrections to go away
        await asyncio.sleep(SETTLE_TIME)

        testTable = [
            [
                TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1200,
                1200,
                1200,
                800,
                800,
                800,
            ],
            [
                -TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1200,
                1200,
                1200,
                800,
                800,
                800,
            ],
            [
                0.0,
                TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                0.0,
                1200,
                1200,
                1200,
                800,
                800,
                800,
            ],
            [
                0.0,
                -TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                0.0,
                1200,
                1200,
                1200,
                800,
                800,
                800,
            ],
            [
                0.0,
                0.0,
                TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                1000,
                1000,
                1000,
                800,
                800,
                800,
            ],
            [
                0.0,
                0.0,
                -TRANSLATION_STEP,
                0.0,
                0.0,
                0.0,
                1000,
                1000,
                1000,
                800,
                800,
                800,
            ],
            [
                0.0,
                0.0,
                0.0,
                ROTATION_STEP,
                0.0,
                0.0,
                1000,
                1000,
                1000,
                1200,
                1200,
                1200,
            ],
            [
                0.0,
                0.0,
                0.0,
                -ROTATION_STEP,
                0.0,
                0.0,
                1000,
                1000,
                1000,
                1200,
                1200,
                1200,
            ],
            [
                0.0,
                0.0,
                0.0,
                0.0,
                ROTATION_STEP,
                0.0,
                1000,
                1000,
                1000,
                1200,
                1200,
                1200,
            ],
            [
                0.0,
                0.0,
                0.0,
                0.0,
                -ROTATION_STEP,
                0.0,
                1000,
                1000,
                1000,
                1200,
                1200,
                1200,
            ],
            [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                ROTATION_STEP,
                1000,
                1000,
                1000,
                1500,
                1500,
                1500,
            ],
            [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                -ROTATION_STEP,
                1000,
                1000,
                1000,
                1500,
                1500,
                1500,
            ],
        ]

        resultFile = await self.openCSV("M13T013")
        print(
            "Test,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation,HP1Encoder,HP2Encoder,HP3Encoder,HP4Encoder,HP5Encoder,HP6Encoder",
            file=resultFile,
        )

        detailsFile = await self.openSCV("M13T013-details")
        print(
            "Test,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation,Fx,Fy,Fz,Mx,My,Mz",
            file=detailsFile,
        )

        for row in testTable:
            # Settle for a bit before taking a baseline
            await asyncio.sleep(SETTLE_TIME)

            # Get baseline data
            data = await self.sampleData(
                "tel_hardpointActuatorData", SAMPLE_TIME, False
            )
            baseline = self.average(data, self.HARDPOINT_TOPICS)

            diffs = {n: 0 for n in self.HARDPOINT_FORCES}

            def triggers_hit(diffs, triggers):
                i = 0
                for n in self.HARDPOINT_FORCES:
                    if diffs[n] >= triggers[i]:
                        return True
                    i += 1
                return False

            # Loop until force / moment triggers are hit
            while triggers_hit(diffs, row[7:]) is False:
                # Clear HP states
                data = self.m1m3.evt_hardpointActuatorState.get()

                # Make a step
                await self.m1m3.cmd_translateM1M3.set_start(
                    xPosition=row[0],
                    yPosition=row[1],
                    zPosition=row[2],
                    xRotation=row[3],
                    yRotation=row[4],
                    zRotation=row[5],
                )
                await self.waitHP()

                # Wait for motion to complete
                await asyncio.sleep(SETTLE_TIME)

                # Get step data
                data = await self.sampleData(
                    "tel_hardpointActuatorData", SAMPLE_TIME, False
                )
                averages = self.average(
                    data, self.HARDPOINT_POSITIONS + HARDPOINT_FORCES
                )
                diffs = {n: averages[n] - baseline[n] for n in HARDPOINT_FORCES}

                print(
                    ",".join(map(str, averages.values())), file=detailsFile,
                )

            # Get position data
            data = await self.sampleData(
                "tel_hardpointActuatorData", SAMPLE_TIME, False
            )
            averages = self.average(data, HARDPOINT_POSITIONS + ["encoder"])
            averages_encoders = self.average(data, ["encoder"])

            # Add position data to results
            print(
                ",".join(map(str, averages.values())),
                ",",
                ",".join(map(str, averages_encodersi["encoder"])),
                file=resultFile,
            )

            # Reset position
            await self.m1m3.cmd_positionM1M3(
                xPosition=0,
                yPosition=0,
                zPosition=0,
                xRotation=0,
                yRotation=0,
                zRotation=0,
            )
            await self.waitHP()

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
