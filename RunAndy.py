import M13T010
import M13T011
import time
from SetupAndy import *

m1m3, sim = SetupAndy()
efd = 0

#M13T010.M13T010().Run(m1m3, sim, efd)
M13T011.M13T011().Run(m1m3, sim, efd)

Shutdown(m1m3, sim)
