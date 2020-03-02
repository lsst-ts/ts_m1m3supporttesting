########################################################################
# Test Numbers: M13T-001
# Author:       CContaxis
# Description:  M1M3 & EFD Interface
# Steps:
# - Issue start command
# - Check EFD for the most recently sent start command
# - Check EFD for the most recently published detailed state event
# - Check EFD for the most recently published inclinometer telemetry
# - Transition back to standby
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb

class M13T001:
    def Run(self, m1m3, sim, efd):
        Header("M13T-001: M1M3 & EFD Interface")
        
        # Issue a command to generate a command, event, and telemetry
        m1m3.Start("Default")
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Check SAL Event
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        
        # Check EFD Command
        row = efd.QueryOne('SELECT "settingsToApply" FROM "efd"."autogen"."lsst.sal.MTM1M3.command_start" ORDER BY DESC LIMIT 1')
        Equal("EFD m1m3_command_start.settingsToApply", row[0], "default")
        
        # Check EFD Event
        row = efd.QueryOne('SELECT "timestamp", "detailedState" FROM "efd"."autogen"."lsst.sal.MTM1M3.logevent_detailedState" ORDER BY DESC LIMIT 1'
        InTolerance("EFD m1m3_logevent_detailedState.timestamp", float(row[0]), data.timestamp, 0.001)
        Equal("EFD m1m3_logevent_detailedState.detailedState", int(row[1]), data.detailedState)
                
        # Check SAL Telemetry
        result, data = m1m3.GetSampleInclinometerData()
        telemetryTimestamp = data.Timestamp
        GreaterThan("SAL m1m3_InclinometerData.Timestamp", data.Timestamp, eventTimestamp)
        
        # Check EFD Telemetry
        row = efd.QueryOne('SELECT "timestamp", "inclinometerAngle" FROM "efd"."autogen"."lsst.sal.MTM1M3.inclinometerData" ORDER BY DESC LIMIT 1')
        InTolerance("EFD m1m3_inclinometerData.timestamp", float(row[0]), data.timestamp, 0.001)
        InTolerance("EFD m1m3_inclinometerData.inclinometerAngle", float(row[1]), data.inclinometerAngle, 0.001)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T001().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)