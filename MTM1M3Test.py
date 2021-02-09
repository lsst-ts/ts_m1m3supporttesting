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
        """Starts MTM1M3, up to given target state.

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

            if startState == -1 or startState == MTM1M3.DetailedState.STANDBY:
                await self.m1m3.cmd_start.set_start(
                    settingsToApply="Default", timeout=60
                )
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)
                bar.update(1)
                startState = MTM1M3.DetailedState.DISABLED

            if startState == MTM1M3.DetailedState.DISABLED:
                if target == MTM1M3.DetailedState.DISABLED:
                    return
                await self.m1m3.cmd_enable.start()
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.PARKED)
                bar.update(1)
                startState = MTM1M3.DetailedState.PARKED

            if startState == MTM1M3.DetailedState.PARKED:
                if target == MTM1M3.DetailedState.PARKED:
                    return
                if target in (
                    MTM1M3.DetailedState.PARKEDENGINEERING,
                    MTM1M3.DetailedState.ACTIVEENGINEERING,
                ):
                    await self.m1m3.cmd_enterEngineering.start()
                    bar.update(1)
                    await self.assertM1M3State(MTM1M3.DetailedState.PARKEDENGINEERING)
                    bar.update(1)
                    if target == MTM1M3.DetailedState.PARKEDENGINEERING:
                        return
                    startState = MTM1M3.DetailedState.PARKEDENGINEERING

        if (
            target == MTM1M3.DetailedState.ACTIVE
            and startState == MTM1M3.DetailedState.PARKED
        ) or (
            target == MTM1M3.DetailedState.ACTIVEENGINEERING
            and startState == MTM1M3.DetailedState.PARKEDENGINEERING
        ):
            click.echo(
                click.style("Waiting for mirror to be raised", bold=True, fg="green")
            )
            await self.m1m3.cmd_raiseM1M3.set_start(
                raiseM1M3=True, bypassReferencePosition=False
            )
            pct = 0
            lastPercents = 0
            with click.progressbar(
                range(100),
                label="Raising",
                width=0,
                item_show_func=lambda i: f"{pct:.01f}%"
                if pct < 100
                else click.style("chasing HP", fg="blue"),
                show_percent=False,
            ) as bar:
                while True:
                    await asyncio.sleep(0.1)
                    pct = (
                        self.m1m3.evt_forceActuatorState.get().supportPercentage * 100.0
                    )
                    diff = pct - lastPercents
                    if diff > 0.1:
                        bar.update(diff)
                        lastPercents = pct
                    if self.m1m3.evt_detailedState.get().detailedState not in (
                        MTM1M3.DetailedState.RAISING,
                        MTM1M3.DetailedState.RAISINGENGINEERING,
                    ):
                        break
            await self.assertM1M3State(target, 0)
            return

        self.fail("Unknown/unsupported target startup state: {target}")

    async def shutdown(self, target=MTM1M3.DetailedState.STANDBY):
        """Closes mirror test cycle, commands its state to the given position.

        Parameters
        ----------
        target : `int`, MTM1M3.DetailedState
            Changes mirror state to the given position.
        """
        currentState = self.m1m3.evt_detailedState.get().detailedState

        if currentState in (
            MTM1M3.DetailedState.ACTIVE,
            MTM1M3.DetailedState.ACTIVEENGINEERING,
        ):
            await self.m1m3.cmd_lowerM1M3.start()
            pct = 0
            lastPercents = 0
            with click.progressbar(
                range(100),
                label="Raising",
                width=0,
                item_show_func=lambda i: f"{pct:.01f}%"
                if pct < 100
                else click.style("chasing HP", fg="blue"),
                show_percent=False,
            ) as bar:
                while True:
                    await asyncio.sleep(0.1)
                    pct = (
                        self.m1m3.evt_forceActuatorState.get().supportPercentage * 100.0
                    )
                    diff = lastPercents - pct
                    if diff > 0.1:
                        bar.update(diff)
                        lastPercents = pct
                    if self.m1m3.evt_detailedState.get().detailedState not in (
                        MTM1M3.DetailedState.LOWERING,
                        MTM1M3.DetailedState.LOWERINGENGINEERING,
                    ):
                        break
            if currentState == MTM1M3.DetailedState.ACTIVE:
                currentState = MTM1M3.DetailedState.PARKED
            else:
                currentState = MTM1M3.DetailedState.PARKEDENGINEERING

            await self.assertM1M3State(currentState, 0)

        with click.progressbar(range(8), label="Shutdown", width=0) as bar:

            if currentState == MTM1M3.DetailedState.PARKEDENGINEERING:
                await self.m1m3.cmd_exitEngineering.start()
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)
                bar.update(1)
                currentState = MTM1M3.DetailedState.PARKED

            if currentState == MTM1M3.DetailedState.PARKED:
                if target == MTM1M3.DetailedState.PARKED:
                    return
                await self.m1m3.cmd_disable.start()
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)
                bar.update(1)
                currentState = MTM1M3.DetailedState.DISABLED

            if currentState == MTM1M3.DetailedState.DISABLED:
                if target == MTM1M3.DetailedState.DISABLED:
                    return
                await self.m1m3.cmd_standby.start()
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.STANDBY)
                bar.update(1)
                currentState = MTM1M3.DetailedState.STANDBY

            if currentState == MTM1M3.DetailedState.STANDBY:
                if target == MTM1M3.DetailedState.STANDBY:
                    return
                bar.update(1)
                await self.m1m3.cmd_exitControl.start()
                bar.update(1)
                return

            self.fail(f"Unknown shutdown target state {target}.")
