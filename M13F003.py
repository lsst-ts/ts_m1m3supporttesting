import math
import time

from SALPY_m1m3 import *

from ForceActuatorTable import *
from HardpointActuatorTable import *
from Utilities import *

########################################################################
# Test Numbers: M13F-003
# Author:       CContaxis
# Description:  Verify ILC communications
########################################################################


class M13F003:
    def Run(self, m1m3, sim):
        Header("M13F-003: Communications Tests")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_DisabledState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal(
            "SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState
        )
        result, data = m1m3.GetEventForceActuatorInfo()
        forceActuatorInfo = data
        for index in range(156):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("FA ILC %d UniqueId Not 0" % refId, uniqueId, 0)
        result, data = m1m3.GetEventHardpointActuatorInfo()
        for index in range(6):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("HP ILC %d UniqueId Not 0" % refId, uniqueId, 0)
        result, data = m1m3.GetEventHardpointMonitorInfo()
        for index in range(6):
            refId = data.ReferenceId[index]
            uniqueId = data.ILCUniqueId[index]
            NotEqual("HM ILC %d UniqueId Not 0" % refId, uniqueId, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
