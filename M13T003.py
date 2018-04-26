########################################################################
# Test Numbers: M13T-003
# Author:       CContaxis
# Description:  Individual hardpoint displacement test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each hardpoint actuator
#   - Perform the following steps for full extension and full retraction
#     - Issue hardpoint step command
#     - Verify hardpoint is moving
#     - Wait for hardpoint motion to complete or a limit switch is operated
#     - Issue stop hardpoint motion command
#     - Verify hardpoint is stopped
#     - Query EFD for hardpoint monitor data for test duration
#     - Query EFD for hardpoint actuator data for test duration
# - Transition from parked engineering to standby state
########################################################################

from Setup import *
from M13T004 import *
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T004().Run(m1m3, sim, efd, "M13T-003: Individual Hardpoint Displacement Test")       