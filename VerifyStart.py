import time
from Utilities import *
from SALPY_m1m3 import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify start command many times
########################################################################

class VerifyForceActuators:
    def Run(self, m1m3, sim):
        Header("Verify Start")
        bad = False
        while not bad:
            m1m3.Start("Default")
            result, data = m1m3.GetEventDetailedState()
            bad = bad || Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
            result, data = m1m3.GetEventSummaryState()
            bad = bad || Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
            time.sleep(1)
            if bad:
                Log("Start Transition")
            m1m3.Standby()
            result, data = m1m3.GetEventDetailedState()
            bad = bad || Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
            result, data = m1m3.GetEventSummaryState()
            bad = bad || Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
            time.sleep(1)
            if bad:
                Log("Standby Transition")