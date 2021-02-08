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

import asyncio
import asynctest
import click

from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3

__all__ = ["MTM1M3Test"]


class MTM1M3Test(asynctest.TestCase):
    """Common parent of M1M3 tests.

    Provides setUp and tearDown methods to create connection to M1M3.
    """

    async def setUp(self):
        """Setup tests. This methods is being called by asynctest.TestCase
        before any test (test_XX) method is called. Creates connections to
        MTM1M3."""
        self.domain = salobj.Domain()
        self.m1m3 = salobj.Remote(self.domain, "MTM1M3")

    async def tearDown(self):
        """Called by asynctest.TestCase after test is done. Correctly closes
        salobj objects."""
        await self.m1m3.close()
        await self.domain.close()

    async def assertM1M3State(self, state, wait=2):
        """Make sure M1M3 reaches given state.

        Parameters
        ----------
        state : `int`, MTM1M3.DetailedState
            Expected M1M3 state.

        wait : `float`
            Wait for given number of seconds before querying for state.
        """

        await asyncio.sleep(wait)
        self.assertEqual(
            self.m1m3.evt_detailedState.get().detailedState,
            state,
            click.style("M1M3 SS is in wrong state", bold=True, bg="red"),
        )

    async def startup(self, target=MTM1M3.DetailedState.PARKED):
        """Startsa MTM1M3, up to given target state.

        Parameters
        ----------
        target : `int`, MTM1M3.DetailedState
            Transition to this state.
        """
        with click.progressbar(range(7), label="Starting up..", width=0) as bar:
            await self.m1m3.start_task
            # await self.assertM1M3State(MTM1M3.DetailedState.STANDBY)
            bar.update(1)
            if target == MTM1M3.DetailedState.STANDBY:
                return

            # see our state..
            try:
                startState = self.m1m3.evt_detailedState.get().detailedState
            except AttributeError:
                startState = -1

            if startState == -1:
                await self.m1m3.cmd_start.set_start(settingsToApply="Default", timeout=60)
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)
                bar.update(1)
                if target == MTM1M3.DetailedState.DISABLED:
                    return
                startState = MTM1M3.DetailedState.DISABLED

            if startState == MTM1M3.DetailedState.DISABLED:
               await self.m1m3.cmd_enable.start()
               bar.update(1)
               await self.assertM1M3State(MTM1M3.DetailedState.PARKED)
               bar.update(1)
               if target == MTM1M3.DetailedState.PARKED:
                   return
               startState = MTM1M3.DetailedState.PARKED

            if startState == MTM1M3.DetailedState.PARKED:
               if target == MTM1M3.DetailedState.PARKEDENGINEERING or target == MTM1M3.DetailedState.ACTIVEENGINEERING:
                   await self.m1m3.cmd_enterEngineering.start()
                   bar.update(1)
                   await self.assertM1M3State(MTM1M3.DetailedState.PARKEDENGINEERING)
                   bar.update(1)
                   return

        if (target == MTM1M3.DetailedState.ACTIVE and startState == MTM1M3.DetailedState.PARKED) or (target == MTM1M3.DetailedState.ACTIVEENGINEERING and startState == MTM1M3.DetailedState.PARKEDENGINEERING):
            await self.m1m3.cmd_raiseM1M3.set_start(raiseM1M3=True, bypassReferencePosition=False)
            lastPercents = 0
            with click.progressbar(range(100), label="Raising", width=0) as bar:
                while True:
                   await asyncio.sleep(0.1)
                   pct = self.m1m3.evt_forceActuatorState.get().supportPercentage
                   if pct - lastPercents > 1:
                       bar.update(1)
                       lastPercents = pct
                   if self.m1m3.evt_detailedState.get().detailedState != MTM1M3.DetailedState.RAISING and self.m1m3.evt_detailedState.get().detailedState != MTM1M3.DetailedState.RAISINGENGINEERING:
                       break
            await self.assertM1M3State(target, 0)
