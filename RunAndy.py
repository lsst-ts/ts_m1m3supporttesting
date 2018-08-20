import M13T012A
import M13T010A
import time
from SetupAndy import *

m1m3, sim = SetupAndy()
efd = 0

M13T012A.M13T012A().Run(m1m3, sim, efd)
#M13T010A.M13T010A().Run(m1m3, sim, efd)

Shutdown(m1m3, sim)
