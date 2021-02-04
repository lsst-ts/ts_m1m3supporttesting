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
        self.domain = salobj.Domain()
        self.m1m3 = salobj.Remote(self.domain, "MTM1M3")
        self.failed = {"primary": [], "secondary": []}
        self.emptyFailed = self.failed

    async def tearDown(self):
        await self.m1m3.close()
        await self.domain.close()

    async def assertM1M3State(self, state, wait=2):
        await asyncio.sleep(wait)
        self.assertEqual(
            self.m1m3.evt_detailedState.get().detailedState,
            state,
            click.style("M1M3 SS is in wrong state", bold=True, bg="red"),
        )

    async def startup(self, target=MTM1M3.DetailedState.PARKED):
        with click.progressbar(range(7), label="Starting up..", width=0) as bar:
            await self.m1m3.start_task
            # await self.assertM1M3State(MTM1M3.DetailedState.STANDBY)
            bar.update(1)
            if target == MTM1M3.DetailedState.STANDBY:
                return

            await self.m1m3.cmd_start.set_start(settingsToApply="Default", timeout=60)
            bar.update(1)
            await self.assertM1M3State(MTM1M3.DetailedState.DISABLED)
            bar.update(1)
            if target == MTM1M3.DetailedState.DISABLED:
                return

            await self.m1m3.cmd_enable.start()
            bar.update(1)
            await self.assertM1M3State(MTM1M3.DetailedState.PARKED)
            bar.update(1)
            if target == MTM1M3.DetailedState.PARKED:
                return

            if target == MTM1M3.DetailedState.PARKEDENGINEERING:
                await self.m1m3.cmd_enterEngineering.start()
                bar.update(1)
                await self.assertM1M3State(MTM1M3.DetailedState.PARKEDENGINEERING)
                bar.update(1)
                return
