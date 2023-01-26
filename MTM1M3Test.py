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
import numpy as np
import time

from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3

from ForceActuatorTable import *

__all__ = ["MTM1M3Test"]


class MTM1M3Test(asynctest.TestCase):
    """Common parent of M1M3 tests.

    Provides setUp and tearDown methods to create connection to M1M3. `startup`
    and `shutdown` methods can be used to progress mirror to a given state.
    Also contains functions to collect measurements during tests, and prints tests
    progress.
    """

    def printHeader(self, header):
        """Prints header text.

        Parameters
        ----------
        header : `str`
            String to print as header.
        """
        click.echo(click.style(header, bold=True, fg="cyan"))

    def printTest(self, test):
        """Prints test progress.

        Parameters
        ----------
        test : `str`
            String to print with test header style.
        """
        click.echo(click.style(test, fg="blue"))

    def printWarning(self, warn):
        """Prints test warning.

        Parameters
        ----------
        warn : `str`
            String to print with warning style.
        """
        click.echo(click.style(warn, fg="yellow", bg="black"))

    def printError(self, err):
        """Prints test error or another important message.

        Parameters
        ----------
        err : `str`
            String to print with error style.
        """
        click.echo(click.style(err, fg="black", bg="red"))

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

    async def switchM1M3State(self, command, state, wait=2, **kwargs):
        """Switch M1M3 state by executing a command and make sure M1M3 reaches
        given state.

        Parameters
        ----------
        command : `str`
            M1M3 command (as string, without cmd_ or any other prefix).
        state : `int`, MTM1M3.DetailedState
            Expected M1M3 state after command is performed.
        wait : `float`, optional
            Wait for given number of seconds for state switch. Defaults to 2.
        **kwargs : dict
            Arguments passed to the command.
        """

        self.m1m3.evt_detailedState.flush()
        stateAfter = asyncio.create_task(
            self.m1m3.evt_detailedState.next(flush=False, timeout=wait)
        )

        await getattr(self.m1m3, "cmd_" + command).set_start(**kwargs)

        self.assertEqual(
            (await stateAfter).detailedState,
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
        with click.progressbar(range(4), label="Starting up..", width=0) as bar:
            await self.m1m3.start_task
            bar.update(1)
            if target == MTM1M3.DetailedState.STANDBY:
                return

            # see our state..
            try:
                startState = self.m1m3.evt_detailedState.get().detailedState
                if startState == target:
                    return
            except AttributeError:
                click.echo(
                    click.style(
                        "State not received. Assuming it's not started.", fg="red"
                    )
                )
                startState = MTM1M3.DetailedState.STANDBY

            if startState == MTM1M3.DetailedState.STANDBY:
                await self.switchM1M3State(
                    "start",
                    MTM1M3.DetailedState.DISABLED,
                    wait=10,
                    timeout=60,
                )
                bar.update(1)
                startState = MTM1M3.DetailedState.DISABLED

            if startState == MTM1M3.DetailedState.DISABLED:
                if target == MTM1M3.DetailedState.DISABLED:
                    return
                await self.switchM1M3State("enable", MTM1M3.DetailedState.PARKED)
                bar.update(1)
                startState = MTM1M3.DetailedState.PARKED

            if startState == MTM1M3.DetailedState.PARKED:
                if target == MTM1M3.DetailedState.PARKED:
                    return
                if target in (
                    MTM1M3.DetailedState.PARKEDENGINEERING,
                    MTM1M3.DetailedState.ACTIVEENGINEERING,
                ):
                    await self.switchM1M3State(
                        "enterEngineering", MTM1M3.DetailedState.PARKEDENGINEERING
                    )
                    bar.update(1)
                    if target == MTM1M3.DetailedState.PARKEDENGINEERING:
                        return
                    startState = MTM1M3.DetailedState.PARKEDENGINEERING

        if target in (
            MTM1M3.DetailedState.ACTIVE,
            MTM1M3.DetailedState.ACTIVEENGINEERING,
        ):
            if (
                startState == MTM1M3.DetailedState.ACTIVEENGINEERING
                and target == MTM1M3.DetailedState.ACTIVE
            ):
                await self.switchM1M3State("exitEngineering", target)
                return

            if (
                startState == MTM1M3.DetailedState.ACTIVE
                and target == MTM1M3.DetailedState.ACTIVEENGINEERING
            ):
                await self.switchM1M3State("enterEngineering", target)
                return

            click.echo(
                click.style("Waiting for mirror to be raised", bold=True, fg="green")
            )

            raisingState = (
                MTM1M3.DetailedState.RAISING
                if target == MTM1M3.DetailedState.ACTIVE
                else MTM1M3.DetailedState.RAISINGENGINEERING
            )

            await self.switchM1M3State(
                "raiseM1M3",
                raisingState,
                wait=2,
                bypassReferencePosition=False,
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
                startTime = time.monotonic()
                while time.monotonic() - startTime < 300:
                    await asyncio.sleep(0.1)
                    pct = self.m1m3.evt_forceActuatorState.get().supportPercentage
                    diff = pct - lastPercents
                    if diff > 0.1:
                        bar.update(diff)
                        lastPercents = pct
                    if not (
                        self.m1m3.evt_detailedState.get().detailedState == raisingState
                    ):
                        break

            self.assertEqual(
                self.m1m3.evt_detailedState.get().detailedState,
                target,
                msg="Mirror raise didn't finish in time",
            )
            return

        if target in (
            MTM1M3.DetailedState.PARKED,
            MTM1M3.DetailedState.PARKEDENGINEERING,
        ):
            if (
                startState == MTM1M3.DetailedState.PARKEDENGINEERING
                and target == MTM1M3.DetailedState.PARKED
            ):
                await self.switchM1M3State("exitEngineering", target)
                return

            if (
                startState == MTM1M3.DetailedState.PARKED
                and target == MTM1M3.DetailedState.PARKEDENGINEERING
            ):
                await self.switchM1M3State("enterEngineering", target)
                return

            click.echo(
                click.style("Waiting for mirror to be lowered", bold=True, fg="green")
            )

            loweringState = (
                MTM1M3.DetailedState.LOWERING
                if target == MTM1M3.DetailedState.PARKED
                else MTM1M3.DetailedState.LOWERINGENGINEERING
            )

            await self.switchM1M3State(
                "lowerM1M3",
                loweringState,
                wait=2,
            )
            pct = 100
            lastPercents = 100
            with click.progressbar(
                range(100),
                label="Lowering",
                width=0,
                item_show_func=lambda i: f"{pct:.01f}%"
                if pct < 100
                else click.style("chasing HP", fg="blue"),
                show_percent=False,
            ) as bar:
                startTime = time.monotonic()
                while time.monotonic() - startTime < 300:
                    await asyncio.sleep(0.1)
                    pct = self.m1m3.evt_forceActuatorState.get().supportPercentage
                    diff = lastPercents - pct
                    if diff > 0.1:
                        bar.update(diff)
                        lastPercents = pct
                    if not (
                        self.m1m3.evt_detailedState.get().detailedState == loweringState
                    ):
                        break

            self.assertEqual(
                self.m1m3.evt_detailedState.get().detailedState,
                target,
                msg="Mirror lowering didn't finish in time",
            )
            return

        self.fail(f"Unknown/unsupported target startup state: {target}")

    async def shutdown(self, target=MTM1M3.DetailedState.STANDBY):
        """Closes mirror test cycle, commands its state to the given state.

        Parameters
        ----------
        target : `int`, MTM1M3.DetailedState
            Transition to this state.
        """
        currentState = self.m1m3.evt_detailedState.get().detailedState
        if currentState == target:
            return

        if currentState in (
            MTM1M3.DetailedState.ACTIVE,
            MTM1M3.DetailedState.ACTIVEENGINEERING,
        ):
            if currentState == MTM1M3.DetailedState.ACTIVE:
                loweringState = MTM1M3.DetailedState.LOWERING
                parkedState = MTM1M3.DetailedState.PARKED
            else:
                loweringState = MTM1M3.DetailedState.LOWERINGENGINEERING
                parkedState = MTM1M3.DetailedState.PARKEDENGINEERING

            await self.switchM1M3State("lowerM1M3", loweringState)
            pct = 100
            lastPercents = 100
            with click.progressbar(
                range(100),
                label="Lowering",
                width=0,
                item_show_func=lambda i: f"{pct:.01f}%"
                if pct > 0
                else click.style("chasing HP", fg="blue"),
                show_percent=False,
            ) as bar:
                startTime = time.monotonic()
                while time.monotonic() - startTime < 300:
                    await asyncio.sleep(0.1)
                    pct = self.m1m3.evt_forceActuatorState.get().supportPercentage
                    diff = lastPercents - pct
                    if diff > 0.1:
                        bar.update(diff)
                        lastPercents = pct
                    if not (
                        self.m1m3.evt_detailedState.get().detailedState == loweringState
                    ):
                        break

            self.assertEqual(
                self.m1m3.evt_detailedState.get().detailedState,
                parkedState,
                msg="Mirror doesn't lower to correct state",
            )
            currentState = parkedState

        with click.progressbar(range(4), label="Shutdown", width=0) as bar:

            if currentState == MTM1M3.DetailedState.PARKEDENGINEERING:
                if target == MTM1M3.DetailedState.PARKEDENGINEERING:
                    return
                await self.switchM1M3State(
                    "exitEngineering", MTM1M3.DetailedState.PARKED
                )
                bar.update(1)
                currentState = MTM1M3.DetailedState.PARKED

            if currentState == MTM1M3.DetailedState.PARKED:
                if target == MTM1M3.DetailedState.PARKED:
                    return
                await self.switchM1M3State("disable", MTM1M3.DetailedState.DISABLED)
                bar.update(1)
                currentState = MTM1M3.DetailedState.DISABLED

            if currentState == MTM1M3.DetailedState.DISABLED:
                if target == MTM1M3.DetailedState.DISABLED:
                    return
                await self.switchM1M3State("standby", MTM1M3.DetailedState.STANDBY)
                bar.update(1)
                currentState = MTM1M3.DetailedState.STANDBY

            if currentState == MTM1M3.DetailedState.STANDBY:
                if target == MTM1M3.DetailedState.STANDBY:
                    return
                await self.m1m3.cmd_exitControl.start()
                bar.update(1)
                return

            self.fail(f"Unknown shutdown target state {target} - {currentState}.")

    async def sampleData(
        self, topic_name, sampling_time, sampling_size=None, flush=True
    ):
        """Samples given M1M3 data for given seconds.

        Parameters
        ----------
        topic_name : `str`
           Event or telemetry topic name (e.g. tel_hardpointActuatorData, evt_detailedState).
        sampling_time : `float`
           Sample time (seconds).
        sampling_size : `float`, optional
           Size of collected samples. When
        flush : `bool`, optional
           Flush data before sampling. Defaults to True.

        Returns
        -------
        data : `array`
           Array of sampled data.

        Throws
        ------
        Runtime error if given number of samples cannot be collected.
        """

        topic = getattr(self.m1m3, topic_name)

        data = await topic.next(flush=flush)
        ret = [data]
        startTimestamp = data.timestamp

        while (
            sampling_time is not None
            and data.timestamp - startTimestamp < sampling_time
        ) or (sampling_size is not None and len(ret) < sampling_size):
            data = await topic.next(flush=False, timeout=sampling_time)
            ret.append(data)

        if sampling_size is not None and len(ret) < sampling_size:
            raise RuntimeError(
                f"Only {len(ret)} of requested {sampling_size} collected."
            )

        return ret

    def average(self, data, topics_names, axis=0):
        """Calculate averages from given data.

        Parameters
        ----------
        data : `array`
            Input values.
        topic_names : `array[str]`
            Names of members to use from data.
        axis : `int`, optional
            Axis for np.average. Defaults to 0.

        Returns
        -------
        ret : `dict`
            Dictionary with collected averages.
        """
        ret = {}
        for n in topics_names:
            ret[n] = np.average([getattr(d, n) for d in data], axis=axis)
        return ret

    def assertListAlmostEqual(self, l1, l2, msg=None, **kwargs):
        self.assertEqual(len(l1), len(l2), msg=msg)
        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], msg=msg, **kwargs)

    async def runActuators(self, function):
        """Runs function for all actuators and directions (XYZ).

        Parameters
        ----------
        function : `func('[XYZ]',int)`
            Run this function for all actuators and directions. The first
            argument is direction (either 'X', 'Y' or 'Z', the second is FA
            index (0 based, counted from the first actuator with given
            direction).
        """
        x = 0  # X index for data access
        y = 0  # Y index for data access

        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            z = row[forceActuatorTableIndexIndex]
            self.id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]

            self.printTest(f"Verify Force Actuator {self.id}")

            # Run X tests for DDA X
            if orientation in ["+X", "-X"]:
                await function("X", x)
                x += 1
            # Run Y tests for DDA Y
            elif orientation in ["+Y", "-Y"]:
                await function("Y", y)
                y += 1

            await function("Z", z)
