import time
from Utilities import *
from SALPY_m1m3 import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify start command many times
########################################################################

class VerifyStart:
    def Run(self, m1m3, sim):
        Header("Verify Start")
        ok = True
        while ok:
            m1m3.Start("Default")
            result, data = m1m3.GetEventDetailedState()
            ok = ok and Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
            result, data = m1m3.GetEventSummaryState()
            ok = ok and Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
            time.sleep(1)
            if not ok:
                Log("Start Transition")
            m1m3.Standby()
            result, data = m1m3.GetEventDetailedState()
            ok = ok and Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)
            result, data = m1m3.GetEventSummaryState()
            ok = ok and Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
            time.sleep(1)
            if not ok:
                Log("Standby Transition")