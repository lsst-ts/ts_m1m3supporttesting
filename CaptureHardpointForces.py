########################################################################
# Test Numbers: M13T-DPV
# Author:       CContaxis
# Description:  Force actuator DP valve test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an axial push limit
#     - Apply axial push forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an axial pull limit
#     - Apply axial pull forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an lateral push limit
#     - Apply lateral push forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an lateral pull limit
#     - Apply lateral pull forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
# - Transition from parked engineering state to standby
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

TEST_PRE_FALL_WAIT = 10.0

class CaptureHardpointForces:
    def Run(self, m1m3, sim, efd):
        Header("Capture Hardpoint Forces")
        
        # Get start timestamp
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTimestamp = data.Timestamp
        
        # Write the file
        path = GetFilePath("%d-CaptureHardpoint.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write("Timestamp,HP1,HP2,HP3,HP4,HP5,HP6,Fx,Fy,Fz,Mx,My,Mz\r\n")
        while True:
            rtn, data = m1m3.GetSampleHardpointActuatorData()
            if rtn >= 0:
                file.write("%0.6f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n" % (data.Timestamp, data.MeasuredForce[0], data.MeasuredForce[1], data.MeasuredForce[2], data.MeasuredForce[3], data.MeasuredForce[4], data.MeasuredForce[5], data.Fx, data.Fy, data.Fz, data.Mx, data.My, data.Mz))
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    CaptureHardpointForces().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)