import M13T009
import M13T011
import time
from SetupAndy import *

m1m3, sim = SetupAndy()
efd = 0

#M13T011.M13T011().Run(m1m3, sim, efd)
M13T009.M13T009().Run(m1m3, sim, efd)

Shutdown(m1m3, sim)
