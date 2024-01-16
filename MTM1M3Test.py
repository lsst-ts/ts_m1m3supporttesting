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
import shutil
import sys
import time
import unittest
from typing import Any, Callable, Coroutine

import astropy.units as u
import click
import numpy as np
from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3
from lsst.ts.salobj import BaseMsgType
from lsst.ts.xml.tables.m1m3 import FATable

__all__ = ["MTM1M3Test"]

M2UM = u.m.to(u.um)


class MTM1M3Test(unittest.IsolatedAsyncioTestCase):
    """Common parent of M1M3 tests.

    Provides asyncSetUp and asyncTearDown methods to create connection to M1M3.
    `startup` and `shutdown` methods can be used to progress mirror to a given
    state. Also contains functions to collect measurements during tests, and
    prints tests progress.
    """

    def printHeader(self, header:str) -> None:
        """Prints header text.

        Parameters
        ----------
        header : `str`
            String to print as header.
        """
        click.echo(click.style(header, bold=True, fg="cyan"))

    def printCode(self, text:str) -> None:
        click.echo(click.style(text, fg="blue"))

    def printTest(self, test: str, centerfill: str | None = None) -> None:
        """Prints test progress.

        Parameters
        ----------
        test : `str`
            String to print with test header style.
        centerfill: `str`
            If provided, put text to center and fill remaining space with
            repeating this string.
        """
        if centerfill:
            fw = int((shutil.get_terminal_size().columns - len(test)) / 2)
            click.echo(centerfill * fw + click.style(test, fg="blue") + centerfill * fw)
        else:
            click.echo(click.style(test, fg="blue"))

    def printWarning(self, warn:str) -> None:
        """Prints test warning.

        Parameters
        ----------
        warn : `str`
            String to print with warning style.
        """
        click.echo(click.style(warn, fg="yellow", bg="black"))

    def printError(self, err:str) -> None:
        """Prints test error or another important message.

        Parameters
        ----------
        err : `str`
            String to print with error style.
        """
        click.echo(click.style(err, fg="black", bg="red"))

    def print_progress(self, message: str, final: bool = False) -> None:
        """Prints tests progress. Ideal for printing data about test progres.
        Message isn't stored in any log. Only print if running in terminal.

        Parameters
        ----------
        message : `str`
            Message to print.
        final: `bool`
            True if that's a final message.
        """
        if sys.stdout.isatty():
            click.echo(message + "\033[0K\r", nl=final)

    def printValues(self, name: str, values: str) -> None:
        """Print values. Pretty format value name and value.

        Parameters
        ----------
        name : `str`
            Value name.
        values : `str`
            Value.
        """
        click.echo(click.style(name, fg="green") + values)

    async def asyncSetUp(self) -> None:
        """Setup tests. This methods is being called by unittest.TestCase
        before any test (test_XX) method is called. Creates connections to
        MTM1M3."""
        self.domain = salobj.Domain()
        self.m1m3 = salobj.Remote(self.domain, "MTM1M3")

        self.max_raising_rate = 0
        self.max_lowering_rate = 0

    async def asyncTearDown(self) -> None:
        """Called by unittest.TestCase after test is done. Correctly closes
        salobj objects."""
        await self.m1m3.close()
        await self.domain.close()

    async def switchM1M3State(self, command:str, state: MTM1M3.DetailedStates, wait:float=5, **kwargs:Any) -> None:
        """Switch M1M3 state by executing a command and make sure M1M3 reaches
        given state.

        Parameters
        ----------
        command : `str`
            M1M3 command (as string, without cmd_ or any other prefix).
        state : `int`, MTM1M3.DetailedStates
            Expected M1M3 state after command is performed.
        wait : `float`, optional
            Wait for given number of seconds for state switch. Defaults to 5.
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

    async def _raising(self) -> None:
        self.printTest("Waiting for mirror to be raised")

        currentState = self.m1m3.evt_detailedState.get().detailedState
        if currentState == MTM1M3.DetailedStates.PARKED:
            raisingState = MTM1M3.DetailedStates.RAISING
            activeState = MTM1M3.DetailedStates.ACTIVE
        else:
            raisingState = MTM1M3.DetailedStates.RAISINGENGINEERING
            activeState = MTM1M3.DetailedStates.ACTIVEENGINEERING

        last_raising_ims = await self.m1m3.tel_imsData.aget()

        await self.switchM1M3State(
            "raiseM1M3",
            raisingState,
            wait=5,
            bypassReferencePosition=False,
        )
        pct = 0
        lastPercents = 0
        raising_rate = 0
        with click.progressbar(
            range(100),
            label="Raising",
            width=0,
            item_show_func=lambda i: f"{pct:.01f}% {raising_rate:.01f} um/sec"
            if pct < 100
            else click.style("chasing HP", fg="blue"),
            show_percent=False,
        ) as bar:
            startTime = time.monotonic()
            while time.monotonic() - startTime < 360:
                if pct == 100:
                    await asyncio.sleep(0.5)
                else:
                    try:
                        sp = await self.m1m3.evt_raisingLoweringInfo.next(
                            flush=False, timeout=60
                        )
                    except asyncio.TimeoutError:
                        self.printError(
                            "Cannot retrieve raisingLowering message after mirror was commanded to raise"
                        )
                        continue
                ims = self.m1m3.tel_imsData.get()
                pct = sp.weightSupportedPercent
                if pct == 100.0:
                    bar.update(100)
                diff = pct - lastPercents
                if diff > 0.1:
                    bar.update(diff)
                    lastPercents = pct
                mdur = ims.timestamp - last_raising_ims.timestamp
                if mdur > 0:
                    raising_rate = (
                        abs(last_raising_ims.zPosition - ims.zPosition) * M2UM
                    ) / mdur
                    self.max_raising_rate = max(self.max_raising_rate, raising_rate)
                last_raising_ims = ims
                if not (
                    self.m1m3.evt_detailedState.get().detailedState == raisingState
                ):
                    break

        self.assertEqual(
            self.m1m3.evt_detailedState.get().detailedState,
            activeState,
            msg="Mirror raise didn't finish in time",
        )

    async def _lowering(self) -> int:
        currentState = self.m1m3.evt_detailedState.get().detailedState
        if currentState == MTM1M3.DetailedStates.ACTIVE:
            loweringState = MTM1M3.DetailedStates.LOWERING
            parkedState = MTM1M3.DetailedStates.PARKED
        else:
            loweringState = MTM1M3.DetailedStates.LOWERINGENGINEERING
            parkedState = MTM1M3.DetailedStates.PARKEDENGINEERING

        self.max_lowering_rate = 0
        last_lowering_ims = await self.m1m3.tel_imsData.aget()

        await self.switchM1M3State(
            "lowerM1M3",
            loweringState,
        )
        pct = 100
        lastPercents = 100
        lowering_rate = 0
        with click.progressbar(
            range(100),
            label="Lowering",
            width=0,
            item_show_func=lambda i: f"{pct:.01f}% {lowering_rate:.01f} um/sec"
            if pct < 100
            else click.style("chasing HP", fg="blue"),
            show_percent=False,
        ) as bar:
            startTime = time.monotonic()
            while time.monotonic() - startTime < 300:
                await asyncio.sleep(0.1)
                sp = self.m1m3.evt_raisingLoweringInfo.get()
                ims = self.m1m3.tel_imsData.get()
                pct = sp.weightSupportedPercent
                diff = lastPercents - pct
                if diff > 0.1:
                    bar.update(diff)
                    lastPercents = pct
                mdur = ims.timestamp - last_lowering_ims.timestamp
                if mdur > 0:
                    lowering_rate = (
                        abs(last_lowering_ims.zPosition - ims.zPosition) * M2UM
                    ) / mdur
                    self.max_lowering_rate = max(self.max_lowering_rate, lowering_rate)
                last_lowering_ims = ims
                if not (
                    self.m1m3.evt_detailedState.get().detailedState == loweringState
                ):
                    break

        self.assertEqual(
            self.m1m3.evt_detailedState.get().detailedState,
            parkedState,
            msg="Mirror lowering didn't finish in time",
        )

        return parkedState

    async def startup(self, target: MTM1M3.DetailedStates=MTM1M3.DetailedStates.PARKED) -> None:
        """Starts MTM1M3, up to given target state.

        Parameters
        ----------
        target : `int`, MTM1M3.DetailedStates
            Transition to this state.
        """
        with click.progressbar(range(4), label="Starting up..", width=0) as bar:
            await self.m1m3.start_task
            bar.update(1)
            if target == MTM1M3.DetailedStates.STANDBY:
                return

            # see our state..
            try:
                startState = self.m1m3.evt_detailedState.get().detailedState
                if startState == target:
                    return
            except AttributeError:
                self.printError("State not received. Assuming it's not started.")
                startState = MTM1M3.DetailedStates.STANDBY

            if startState == MTM1M3.DetailedStates.STANDBY:
                await self.switchM1M3State(
                    "start",
                    MTM1M3.DetailedStates.DISABLED,
                    wait=10,
                    timeout=60,
                )
                bar.update(1)
                startState = MTM1M3.DetailedStates.DISABLED

            if startState == MTM1M3.DetailedStates.DISABLED:
                if target == MTM1M3.DetailedStates.DISABLED:
                    return
                await self.switchM1M3State("enable", MTM1M3.DetailedStates.PARKED)
                bar.update(1)
                startState = MTM1M3.DetailedStates.PARKED

            if startState == MTM1M3.DetailedStates.PARKED:
                if target == MTM1M3.DetailedStates.PARKED:
                    return
                if target in (
                    MTM1M3.DetailedStates.PARKEDENGINEERING,
                    MTM1M3.DetailedStates.ACTIVEENGINEERING,
                ):
                    await self.switchM1M3State(
                        "enterEngineering",
                        MTM1M3.DetailedStates.PARKEDENGINEERING,
                    )
                    bar.update(1)
                    if target == MTM1M3.DetailedStates.PARKEDENGINEERING:
                        return
                    startState = MTM1M3.DetailedStates.PARKEDENGINEERING

        if target in (
            MTM1M3.DetailedStates.ACTIVE,
            MTM1M3.DetailedStates.ACTIVEENGINEERING,
        ):
            if (
                startState == MTM1M3.DetailedStates.ACTIVEENGINEERING
                and target == MTM1M3.DetailedStates.ACTIVE
            ):
                await self.switchM1M3State("exitEngineering", target)
                return

            if (
                startState == MTM1M3.DetailedStates.ACTIVE
                and target == MTM1M3.DetailedStates.ACTIVEENGINEERING
            ):
                await self.switchM1M3State("enterEngineering", target)
                return

            await self._raising()

            return

        if target in (
            MTM1M3.DetailedStates.PARKED,
            MTM1M3.DetailedStates.PARKEDENGINEERING,
        ):
            if (
                startState == MTM1M3.DetailedStates.PARKEDENGINEERING
                and target == MTM1M3.DetailedStates.PARKED
            ):
                await self.switchM1M3State("exitEngineering", target)
                return

            if (
                startState == MTM1M3.DetailedStates.PARKED
                and target == MTM1M3.DetailedStates.PARKEDENGINEERING
            ):
                await self.switchM1M3State("enterEngineering", target)
                return

            self.printTest("Waiting for mirror to be lowered")

            await self._lowering()

            return

        self.fail(f"Unknown/unsupported target startup state: {target}")

    async def shutdown(self, target:MTM1M3.DetailedStates=MTM1M3.DetailedStates.STANDBY) -> None:
        """Closes mirror test cycle, commands its state to the given state.

        Parameters
        ----------
        target : `int`, MTM1M3.DetailedStates
            Transition to this state.
        """
        currentState = self.m1m3.evt_detailedState.get().detailedState
        if target in (
            MTM1M3.DetailedStates.ACTIVE,
            MTM1M3.DetailedStates.ACTIVEENGINEERING,
        ):
            if (
                currentState == MTM1M3.DetailedStates.ACTIVE
                and target == MTM1M3.DetailedStates.ACTIVEENGINEERING
            ):
                await self.switchM1M3State("enterEngineering", target)
                return
            elif (
                currentState == MTM1M3.DetailedStates.ACTIVEENGINEERING
                and target == MTM1M3.DetailedStates.ACTIVE
            ):
                await self.switchM1M3State("exitEngineering", target)
                return
        if currentState == target:
            return

        if currentState in (
            MTM1M3.DetailedStates.ACTIVE,
            MTM1M3.DetailedStates.ACTIVEENGINEERING,
        ):
            currentState = await self._lowering()

        with click.progressbar(range(4), label="Shutdown", width=0) as bar:
            if currentState == MTM1M3.DetailedStates.PARKEDENGINEERING:
                if target == MTM1M3.DetailedStates.PARKEDENGINEERING:
                    return
                await self.switchM1M3State(
                    "exitEngineering", MTM1M3.DetailedStates.PARKED
                )
                bar.update(1)
                currentState = MTM1M3.DetailedStates.PARKED

            if currentState == MTM1M3.DetailedStates.PARKED:
                if target == MTM1M3.DetailedStates.PARKED:
                    return
                await self.switchM1M3State("disable", MTM1M3.DetailedStates.DISABLED)
                bar.update(1)
                currentState = MTM1M3.DetailedStates.DISABLED

            if currentState == MTM1M3.DetailedStates.DISABLED:
                if target == MTM1M3.DetailedStates.DISABLED:
                    return
                await self.switchM1M3State("standby", MTM1M3.DetailedStates.STANDBY)
                bar.update(1)
                currentState = MTM1M3.DetailedStates.STANDBY

            if currentState == MTM1M3.DetailedStates.STANDBY:
                if target == MTM1M3.DetailedStates.STANDBY:
                    return
                if target in (
                    MTM1M3.DetailedStates.PARKED,
                    MTM1M3.DetailedStates.PARKEDENGINEERING,
                ):
                    await self.switchM1M3State("enable", MTM1M3.DetailedStates.PARKED)
                    if target == MTM1M3.DetailedStates.PARKEDENGINEERING:
                        await self.switchM1M3State("enterEngineering", target)
                    return
                await self.switchM1M3State("exitControl", MTM1M3.DetailedStates.OFFLINE)
                bar.update(1)
                self.printWarning("Called exitControl command")
                return

            self.fail(f"Unknown shutdown target state {target} - {currentState}.")

    async def sampleData(
        self, topic_name:str, sampling_time:float, sampling_size:int | None=None, flush:bool=True
    ) -> list[BaseMsgType]:
        """Samples given M1M3 data for given seconds.

        Parameters
        ----------
        topic_name : `str`
           Event or telemetry topic name (e.g. tel_hardpointActuatorData,
           evt_detailedState).
        sampling_time : `float`
           Sample time (seconds).
        sampling_size : `int`, optional
           Size of collected samples. When None (the default), sampling size is
           unlimited.
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

    def average(self, data: BaseMsgType, topics_names: list[str], axis:int=0) -> dict[str, Any]:
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

    def assertListAlmostEqual(self, l1:list[Any], l2:list[Any], msg:str|None=None, **kwargs:Any) -> None:
        self.assertEqual(len(l1), len(l2), msg=msg)
        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], msg=msg, **kwargs)

    def get_enabled_force_actuators(self) -> list[bool]:
        """Returns 156-member array, where true means actuator is enabled.

        Returns
        -------
        enabled : `[bool]`
            Array where true means actuator is enabled.
        """
        enabled_FA = self.m1m3.evt_enabledForceActuators.get()
        if enabled_FA is None:
            self.printError("Cannot retrieve enabled actuator list!")
            raise RuntimeError("Cannot retrieve enabled actuator list!")
        enabled = enabled_FA.forceActuatorEnabled
        for index, e in enumerate(enabled):
            if e is False:
                self.printWarning(f"Actuator with index {index} is disabled.")
        return enabled

    async def run_actuators(self, function: Callable[[str, int], Coroutine[Any, Any, None]]) -> None:
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

        enabled = self.get_enabled_force_actuators()

        # Iterate through all 156 force actuators
        for row in FATable:
            z = row.z_index
            self.actuator_id = row.actuator_id
            if enabled[z] is False:
                self.printWarning(f"Skipping FA index {z} ID {self.actuator_id}")
                continue
            self.printTest(f"Verify Force Actuator {self.actuator_id}")

            # Run X tests for DDA X
            if row.x_index is not None:
                await function("X", x)
                x += 1
            # Run Y tests for DDA Y
            elif row.y_index is not None:
                await function("Y", y)
                y += 1

            await function("Z", z)
