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
        Equal("SAL MTM1M3_logevent_SummaryState.SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_DisabledState)
        
        # Check SAL Event
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_DisabledState)
        
        # Check EFD Command
        row = efd.QueryOne("SELECT Start, SettingsToApply FROM MTM1M3_command_Start ORDER BY date_time DESC LIMIT 1")
        Equal("EFD MTM1M3_command_Start.Start", int(row[0]), 1)
        Equal("EFD MTM1M3_command_Start.SettingsToApply", row[1], "Default")
        
        # Check EFD Event
        row = efd.QueryOne("SELECT Timestamp, DetailedState FROM MTM1M3_logevent_DetailedState WHERE Timestamp <= %0.3f ORDER BY Timestamp DESC LIMIT 1" % (eventTimestamp + 0.001))
        InTolerance("EFD MTM1M3_logevent_DetailedState.Timestamp", float(row[0]), data.Timestamp, 0.001)
        Equal("EFD MTM1M3_logevent_DetailedState.DetailedState", int(row[1]), data.detailedState)
                
        # Check SAL Telemetry
        result, data = m1m3.GetSampleInclinometerData()
        telemetryTimestamp = data.Timestamp
        GreaterThan("SAL MTM1M3_InclinometerData.Timestamp", data.Timestamp, eventTimestamp)
        
        # Check EFD Telemetry
        row = efd.QueryOne("SELECT Timestamp, InclinometerAngle FROM MTM1M3_InclinometerData WHERE Timestamp <= %0.3f ORDER BY Timestamp DESC LIMIT 1" % (telemetryTimestamp + 0.001))
        InTolerance("EFD MTM1M3_InclinometerData.Timestamp", float(row[0]), data.Timestamp, 0.001)
        InTolerance("EFD MTM1M3_InclinometerData.InclinometerAngle", float(row[1]), data.InclinometerAngle, 0.001)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL MTM1M3_logevent_SummaryState.SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_StandbyState)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T001().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
