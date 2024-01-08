#!/usr/bin/env python3

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
# Test Numbers: M13T-001
# Author:       CContaxis
# Description:  M1M3 & EFD Interface
# Steps:
# - Issue start command
# - Check EFD for the most recently sent start command
# - Check EFD for the most recently published detailed state event
# - Check EFD for the most recently published inclinometer telemetry
# - Transition back to standby
########################################################################

from MTM1M3Test import *
from lsst.ts.idl.enums import MTM1M3

import asynctest


class M13T001(MTM1M3Test):
    async def test_M1M3(self):
        await self.startup(MTM1M3.DetailedStates.STANDBY)

        await self.switchM1M3State(
            "start",
            MTM1M3.DetailedStates.DISABLED,
            settingsToApply="Default",
            timeout=60,
        )

        self.assertNotEqual(self.m1m3.evt_summaryState.get(), None)
        self.assertNotEqual(self.m1m3.evt_detailedState.get(), None)

        await self.switchM1M3State("enable", MTM1M3.DetailedStates.PARKED)

        await self.switchM1M3State("disable", MTM1M3.DetailedStates.DISABLED)

        await self.switchM1M3State("standby", MTM1M3.DetailedStates.STANDBY)

        # Check SAL Event
        # result, data = m1m3.GetEventDetailedState()
        # eventTimestamp = data.Timestamp
        # Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedS

        # Check EFD Command
        # row = efd.QueryOne("SELECT Start, SettingsToApply FROM m1m3_command_Start ORDER BY date_time DES
        # Equal("EFD m1m3_command_Start.Start", int(row[0]), 1)
        # Equal("EFD m1m3_command_Start.SettingsToApply", row[1], "Default")

        # Check EFD Event
        # row = efd.QueryOne("SELECT Timestamp, DetailedState FROM m1m3_logevent_DetailedState WHERE Times
        # InTolerance("EFD m1m3_logevent_DetailedState.Timestamp", float(row[0]), data.Timestamp, 0.001)
        # Equal("EFD m1m3_logevent_DetailedState.DetailedState", int(row[1]), data.DetailedState)

        # Check SAL Telemetry
        # result, data = m1m3.GetSampleInclinometerData()
        # telemetryTimestamp = data.Timestamp
        # GreaterThan("SAL m1m3_InclinometerData.Timestamp", data.Timestamp, eventTimestamp)

        # Check EFD Telemetry
        # row = efd.QueryOne("SELECT Timestamp, InclinometerAngle FROM m1m3_InclinometerData WHERE Timesta
        # InTolerance("EFD m1m3_InclinometerData.Timestamp", float(row[0]), data.Timestamp, 0.001)
        # InTolerance("EFD m1m3_InclinometerData.InclinometerAngle", float(row[1]), data.InclinometerAngle


if __name__ == "__main__":
    asynctest.main()
