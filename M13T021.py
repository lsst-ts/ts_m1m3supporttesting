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
# Test Numbers: M13T-021
# Author:       CContaxis
# Description:  Mirror Support Lifting and Parking
# Steps:
# - Transition from standby to parked engineering state
# - Raise Mirror
# - Verify raise time is < 300s
# - Verify HP shows mirror at the reference position
# - Verify IMS shows mirror at the reference position
# - Lower Mirror
# - Verify lower time is < 300s
# - Verify lower rate is < 15mm/s
# - Exit engineering - transition to parked state (non engineering)
# - Raise Mirror
# - Verify raise time is < 300s
# - Verify HP shows mirror at the reference position
# - Verify IMS shows mirror at the reference position
# - Lower Mirror
# - Verify lower time is < 300s
# - Verify lower rate is < 15mm/s
# - Transition back to standby
########################################################################

from MTM1M3Movements import *

from lsst.ts.salobj import State
from lsst.ts.idl.enums import MTM1M3

import astropy.units as u
import asynctest
import asyncio

TRAVEL_POSITION = 1 * u.mm
TRAVEL_ROTATION = 50.4 * u.arcsec
#POSITION_TOLERANCE = 0.81 * u.mm
#ROTATION_TOLERANCE = 20 * u.arcsec
POSITION_TOLERANCE = 81 * u.mm.to(u.m)
ROTATION_TOLERANCE = 2000 * u.arcsec.to(u.deg)


M2UM = u.m.to(u.um)


class M13T021(MTM1M3Movements):
    async def _raise_lower(self, engmode):
        if engmode is True:
            state_parked = MTM1M3.DetailedState.PARKEDENGINEERING
            state_active = MTM1M3.DetailedState.ACTIVEENGINEERING
        else:
            state_parked = MTM1M3.DetailedState.PARKED
            state_active = MTM1M3.DetailedState.ACTIVE

        await self.startup(state_parked)

        await asyncio.sleep(2.0)

        # Get start time and start position
        startTime = self.m1m3.tel_hardpointActuatorData.get().timestamp

        # Raise mirror (therefore entering the Raised Engineering State).
        await self.startup(state_active)
        self.assertEqual(self.m1m3.evt_summaryState.get().summaryState, State.ENABLED)

        # Get stop time
        duration = self.m1m3.tel_hardpointActuatorData.get().timestamp - startTime

        await asyncio.sleep(5.0)

        await self.do_movements(
            [offset()],
            "Check position after movement",
            check_forces=False,
            end_state=state_active,
        )

        # Verify raise time
        self.assertLessEqual(
            duration,
            300,
            msg=f"Raising for more than 300 seconds! Measured raise time: {duration:.1f}s",
        )

        await asyncio.sleep(5.0)

        # Get start time and start position
        startTime = self.m1m3.tel_hardpointActuatorData.get().timestamp
        startIMSZ = self.m1m3.tel_imsData.get().zPosition * M2UM

        # Lower mirror.
        await self.shutdown(state_parked)

        duration = self.m1m3.tel_hardpointActuatorData.get().timestamp - startTime
        stopIMSZ = self.m1m3.tel_imsData.get().zPosition * M2UM

        # Verify lower time
        self.assertLessEqual(
            duration,
            300,
            msg=f"Lowering for more than 300 seconds! Measured llower time: {duration:.1f}s",
        )

        # Verify fall rate
        lower_rate = (startIMSZ - stopIMSZ) / duration
        self.assertLessEqual(
            (startIMSZ - stopIMSZ) / duration,
            150,
            msg="Lowering rate higher than 150 um/second, measured as {lower_rate:.02f}um/second",
        )

    async def test_mirror_support_lifting_and_parking(self):
        self.printHeader("M13T-021: Mirror Support Lifting and Parking")

        self.POSITION_TOLERANCE = POSITION_TOLERANCE
        self.ROTATION_TOLERANCE = ROTATION_TOLERANCE

        for engmode in [True, False]:
            self.printTest(('Engineering' if engmode else 'Automatic') + " pass")
            await self._raise_lower(engmode)

        await self.shutdown(MTM1M3.DetailedState.STANDBY)


if __name__ == "__main__":
    asynctest.main()
