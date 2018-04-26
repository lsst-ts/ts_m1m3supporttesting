########################################################################
# Test Numbers: M13T-028
# Author:       CContaxis
# Description:  Actuator to Actuator Force Delta for 6 nearest neighbors
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an X component
#     - Perform the following steps for each test point (min / max limit)
#       - Apply a pure X force offset above the limit
#       - Verify the pure X force is being applied but at the limit
#       - Verify the pure X force above the limit is rejected
#       - Clear offset forces
#       - Verify the pure X force is no longer being applied
#   - If the force actuator has an Y component
#     - Perform the following steps for each test point (min / max limit)
#       - Apply a pure Y force offset
#       - Verify the pure Y force is being applied but at the limit
#       - Verify the pure Y force above the limit is rejected
#       - Clear offset forces
#       - Verify the pure Y force is no longer being applied
#   - Perform the following steps for each test point (min / max limit)
#     - Apply a pure X force offset
#     - Verify the pure Z force is being applied but at the limit
#     - Verify the pure Z force above the limit is rejected
#     - Clear offset forces
#     - Verify the pure Z force is no longer being applied
# - Transition from parked engineering state to standby
########################################################################

from Setup import *
from M13T027 import *
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T027().Run(m1m3, sim, efd, "M13T-028: Actuator to Actuator Force Delta for 6 nearest neighbors")
    Shutdown(m1m3, sim, efd)