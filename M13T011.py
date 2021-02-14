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
# Test Numbers: M13T-011  
# Author:       AClements
# Description:  Position Stability During Active Mode Operation
# Steps:
# - Issue start command
# - Raise Mirror in Active Engineering Mode
# - Wait 5 seconds for everything to settle
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm
# - Wait 15 seconds between each movement to let control take measurements.
#   +X, 0, 0 
#   -X, 0, 0
#   0,+Y, 0
#   0, -Y, 0
#   0, 0, +Z
#   0, 0, -Z
#   +X, +Y, 0
#   +X, -Y, 0
#   -X, +Y, 0
#   -X, -Y, 0
#   +X, 0, +Z
#   +X, 0, -Z
#   -X, 0, +Z
#   -X, 0, -Z
#   0, +Y, +Z
#   0, +Y, -Z
#   0, -Y, +Z
#   0, -Y, -Z
# - Repeat Matrix 2 more times
# - Transition back to standby
# - Pull data from EFD to generate RMS values specified by the test.
########################################################################

import astropy.units as u
import asynctest
import click

from lsst.ts import salobj
from lsst.ts.idl.enums import MTM1M3

from MTM1M3Movements import MTM1M3Movements


X1Sensitivity = 51.459
Y1Sensitivity = 52.061
Z1Sensitivity = 51.298

X2Sensitivity = 51.937
Y2Sensitivity = 52.239
Z2Sensitivity = 52.130

X3Sensitivity = 52.183
Y3Sensitivity = 52.015
Z3Sensitivity = 51.908

TRAVEL_POSITION = 1 * u.mm
SETTLE_TIME = 3.0
SAMPLE_TIME = 15.0

ZERO_M = 0 * u.m
ZERO_DEG = 0 * u.deg

def convert(raw, sensitivity):
    return (raw * 1000.0) / sensitivity

class M13T011(MTM1M3Movements):
    def _log_data(self, data, imsData):
        startTimestamp = imsData.Timestamp
        timestamp = startTimestamp

    def test_movements(self):
        # Setup VMS
        self.vms = salobj.Remote(self.domain, "MTVMS")
        
        offsets = [
            [ZERO_M, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],

            [+TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [-TRAVEL_POSITION, ZERO_M, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [+TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [+TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [-TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [-TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_M, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [+TRAVEL_POSITION, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [+TRAVEL_POSITION, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [-TRAVEL_POSITION, ZERO_M, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [-TRAVEL_POSITION, ZERO_M, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, +TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, +TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, -TRAVEL_POSITION, +TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
            [ZERO_M, -TRAVEL_POSITION, -TRAVEL_POSITION, ZERO_DEG, ZERO_DEG, ZERO_DEG],
        ]

        self.LOG_FILE = open(
            f'M13T012-{datetime.now().strftime("%Y-%m-%dT%T")}.csv', "w"
        )

        # The martix need to be tested 3 times
        await self.do_movements(offsets, "M13T-011: Position Stability During Active Mode Operation", end_state=MTM1M3.DetailedState.STANDBY, moved_callback = self._log_data)

                # Flush VMS data
                vmsData = vms_M1M3C()
                result = vms.getNextSample_M1M3(vmsData)
                while result >= 0:
                    vmsData = vms_M1M3C()
                    result = vms.getNextSample_M1M3(vmsData)

                # Mark times
                startTimestamp = imsData.Timestamp
                timestamp = startTimestamp

                # Sample data for the configured sample time
                while (timestamp - startTimestamp) < SAMPLE_TIME:
                    result, imsData = m1m3.GetNextSampleIMSData()
                    if result >= 0:
                        timestamp = imsData.Timestamp
                        imsDatas.append(imsData)
                    vmsData = vms_M1M3C()
                    result = vms.getNextSample_M1M3(vmsData)
                    if result >= 0:
                        vmsDatas.append(vmsData)

                # Write the IMS data to a file
                path = GetFilePath("M13T011-%s-%d-IMS-%d.csv" % (row[0], (i+1), int(startTimestamp)))
                file = open(path, "w+")
                file.write("Timestamp,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation\r\n")
                for imsData in imsDatas:
                    file.write("%0.3f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f\r\n" % (imsData.Timestamp, imsData.XPosition, imsData.YPosition, imsData.ZPosition, imsData.XRotation, imsData.YRotation, imsData.ZRotation))
                file.close()

                # Write the VMS data to a file
                path = GetFilePath("M13T011-%s-%d-VMS-%d.csv" % (row[0], (i+1), int(startTimestamp)))
                file = open(path, "w+")
                file.write("Timestamp (s),X1 (m/s^2),Y1 (m/s^2),Z1 (m/s^2),X2 (m/s^2),Y2 (m/s^2),Z2 (m/s^2),X3 (m/s^2),Y3 (m/s^2),Z3 (m/s^2)\r\n")
                for vmsData in vmsDatas:
                    newTimestamp = vmsData.Timestamp
                    for j in range(50):
                        file.write("%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n" % (
                            newTimestamp, 
                            convert(vmsData.Sensor1XAcceleration[j], X1Sensitivity),
                            convert(vmsData.Sensor1YAcceleration[j], Y1Sensitivity),
                            convert(vmsData.Sensor1ZAcceleration[j], Z1Sensitivity),
                            convert(vmsData.Sensor2XAcceleration[j], X2Sensitivity),
                            convert(vmsData.Sensor2YAcceleration[j], Y2Sensitivity),
                            convert(vmsData.Sensor2ZAcceleration[j], Z2Sensitivity),
                            convert(vmsData.Sensor3XAcceleration[j], X3Sensitivity),
                            convert(vmsData.Sensor3YAcceleration[j], Y3Sensitivity),
                            convert(vmsData.Sensor3ZAcceleration[j], Z3Sensitivity)))
                        newTimestamp += 0.001
                file.close()               
        
if __name__ == "__main__":
    asynctest.main()
