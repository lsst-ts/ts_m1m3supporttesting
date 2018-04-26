import VerifyAccelerometer
import VerifyInclinometer
import VerifyDisplacement
import VerifyEFD
import VerifyStateChanges
import VerifyTiming
import VerifyForceActuators
import VerifyHardpointActuators
import VerifyStart
import M13F003
import M13T002
import M13T003
import M13T004
import time
from Setup import *

m1m3, sim, efd = Setup()

#VerifyEFD.VerifyEFD().Run(m1m3, sim)
#VerifyStateChanges.VerifyStateChanges().Run(m1m3, sim)
#VerifyAccelerometer.VerifyAccelerometer().Run(m1m3, sim)
#VerifyInclinometer.VerifyInclinometer().Run(m1m3, sim)
#VerifyDisplacement.VerifyDisplacement().Run(m1m3, sim)
#VerifyForceActuators.VerifyForceActuators().Run(m1m3, sim)
#VerifyHardpointActuators.VerifyHardpointActuators().Run(m1m3, sim)
#M13F003.M13F003().Run(m1m3, sim)
M13T001.M13T001().Run(m1m3, sim, efd)
M13T002.M13T002().Run(m1m3, sim, efd)
M13T004.M13T004().Run(m1m3, sim, efd, "M13T-003: Individual Hardpoint Displacement Test")
M13T004.M13T004().Run(m1m3, sim, efd, "M13T-004: Individual Hardpoint Breakaway Test")
#VerifyTiming.VerifyTiming().Run(m1m3, sim)
#VerifyStart.VerifyStart().Run(m1m3, sim)