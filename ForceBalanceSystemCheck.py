########################################################################
# Test Numbers: N/A
# Author:       CContaxis
# Description:  Characterize the force balance system
# Steps:
# - Sample data before and after application of a mirror force
########################################################################

import math
import time

from SALPY_m1m3 import *

from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *
from Utilities import *

TEST_FORCE = 1000.0
TEST_MOMENT = 1000.0
TEST_HOLD_TIME = 5.0
TEST_SAMPLE_TIME = 20.0


class ForceBalanceSystemCheck:
    def Run(self, m1m3, sim, efd):
        Header("Force balance system check")

        testTable = [
            ["Fx", TEST_FORCE, 0, 0, 0, 0, 0],
            ["Fx", -TEST_FORCE, 0, 0, 0, 0, 0],
            ["Fy", 0, TEST_FORCE, 0, 0, 0, 0],
            ["Fy", 0, -TEST_FORCE, 0, 0, 0, 0],
            ["Fz", 0, 0, TEST_FORCE, 0, 0, 0],
            ["Fz", 0, 0, -TEST_FORCE, 0, 0, 0],
            ["Mx", 0, 0, 0, TEST_MOMENT, 0, 0],
            ["Mx", 0, 0, 0, -TEST_MOMENT, 0, 0],
            ["My", 0, 0, 0, 0, TEST_MOMENT, 0],
            ["My", 0, 0, 0, 0, -TEST_MOMENT, 0],
            ["Mz", 0, 0, 0, 0, 0, TEST_MOMENT],
            ["Mz", 0, 0, 0, 0, 0, -TEST_MOMENT],
        ]

        for test in testTable:
            # Get start time of this test
            result, data = m1m3.GetSampleHardpointActuatorData()
            startTimestamp = data.Timestamp

            # Write header
            output = "Timestamp,HP1,HP2,HP3,HP4,HP5,HP6,Fx,Fy,Fz,Mx,My,Mz\r\n"
            commanded = False

            # Repeat until sample time has passed
            while (data.Timestamp - startTimestamp) < TEST_SAMPLE_TIME:
                # Command mirror force after hold time
                if (data.Timestamp - startTimestamp) > TEST_HOLD_TIME and not commanded:
                    commanded = True
                    m1m3.ApplyOffsetForcesByMirrorForce(
                        test[1], test[2], test[3], test[4], test[5], test[6], False
                    )
                # Sample data
                rtn, data = m1m3.GetNextSampleHardpointActuatorData()
                if rtn >= 0:
                    output = output + (
                        "%0.6f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n"
                        % (
                            data.Timestamp,
                            data.MeasuredForce[0],
                            data.MeasuredForce[1],
                            data.MeasuredForce[2],
                            data.MeasuredForce[3],
                            data.MeasuredForce[4],
                            data.MeasuredForce[5],
                            data.Fx,
                            data.Fy,
                            data.Fz,
                            data.Mx,
                            data.My,
                            data.Mz,
                        )
                    )

            # Prepend force and timestamp information
            rtn, data = m1m3.GetEventAppliedOffsetForces()
            output = (
                "Applied %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f at %0.6f\r\n"
                % (data.Fx, data.Fy, data.Fz, data.Mx, data.My, data.Mz, data.Timestamp)
            ) + output

            # Write the output file
            path = GetFilePath(
                "%d-ForceBalanceSystemCheck-%s.csv" % (int(startTimestamp), test[0])
            )
            Log("File path: %s" % path)
            file = open(path, "w+")
            file.write(output)
            file.close()

            # Clear offset forces
            m1m3.ClearOffsetForces()
            time.sleep(5.0)


if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    ForceBalanceSystemCheck().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
