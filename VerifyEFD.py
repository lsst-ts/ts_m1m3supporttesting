from Utilities import *
from SALPY_m1m3 import *
import MySQLdb

########################################################################
# Test Numbers: M13T-001
# Author:       CContaxis
# Description:  Verify commands, events, and telemetry are pushed into 
#               the EFD  
########################################################################

class VerifyEFD:
    def Run(self, m1m3, sim):
        Header("Verify EFD")
        
        db = MySQLdb.connect(host = "localhost",
                             user="efduser",
                             passwd="lssttest",
                             db="EFD")
        cur = db.cursor()
        
        # Issue a command to generate a command, event, and telemetry
        m1m3.Start("Default")
        
        # Check SAL Event
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        
        # Check EFD Command
        count = cur.execute("SELECT Start, SettingsToApply FROM m1m3_command_Start ORDER BY date_time DESC LIMIT 1")
        if (Equal("EFD m1m3_command_Start Count", count, 1)):
            row = cur.fetchone()
            Equal("EFD m1m3_command_Start.Start", int(row[0]), 1)
            Equal("EFD m1m3_command_Start.SettingsToApply", row[1], "Default")
        
        # Check EFD Event
        count = cur.execute("SELECT Timestamp, DetailedState FROM m1m3_logevent_DetailedState WHERE Timestamp <= %0.3f ORDER BY Timestamp DESC LIMIT 1" % (eventTimestamp + 0.001))
        if (Equal("EFD m1m3_logevent_DetailedState Count", count, 1)):
            row = cur.fetchone()
            InTolerance("EFD m1m3_logevent_DetailedState.Timestamp", float(row[0]), data.Timestamp, 0.001)
            Equal("EFD m1m3_logevent_DetailedState.DetailedState", int(row[1]), data.DetailedState)
                
        # Check SAL Telemetry
        result, data = m1m3.GetSampleInclinometerData()
        telemetryTimestamp = data.Timestamp
        GreaterThan("SAL m1m3_InclinometerData.Timestamp", data.Timestamp, eventTimestamp)
        
        # Check EFD Telemetry
        count = cur.execute("SELECT Timestamp, InclinometerAngle FROM m1m3_InclinometerData WHERE Timestamp <= %0.3f ORDER BY Timestamp DESC LIMIT 1" % (telemetryTimestamp + 0.001))
        if (Equal("EFD m1m3_InclinometerData Count", count, 1)):
            row = cur.fetchone()
            InTolerance("EFD m1m3_InclinometerData.Timestamp", float(row[0]), data.Timestamp, 0.001)
            InTolerance("EFD m1m3_InclinometerData.InclinometerAngle", float(row[1]), data.InclinometerAngle, 0.001)
        
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
        db.close()
        