from Utilities import *
from SALPY_m1m3 import *
import MySQLdb

class VerifyEFD:
    def Run(self, m1m3, sim):
        Header("Verify EFD")
        
        db = MySQLdb.connect(host = "",
                             user="",
                             passwd="",
                             db="")
        cur = db.cursor()
        
        m1m3.Start("Default", False)
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        
        # Check EFD Command
        cur.execute("SELECT * FROM m1m3_command_Start ORDER BY date_Time DESC LIMIT 1")
        row = cur.fetchone()
        print(row)
        actual = 0
        Equal("EFD m1m3_command_Start.Start", actual, 1)
        Equal("EFD m1m3_command_Start.SettingsToApply", actual, "Default")
        
        # Check EFD Event
        cur.execute("SELECT * FROM m1m3_logevent_DetailedState WHERE Timestamp <= eventTimestamp ORDER BY Timestamp DESC LIMT 1")
        row = cur.fetchone()
        print(row)
        actual = 0
        InTolerance("EFD m1m3_logevent_DetailedState.Timestamp", actual, data.Timestamp, 0.001)
        Equal("EFD m1m3_logevent_DetailedState.DetailedState", actual, data.DetailedState)
                
        # Check EFD Telemetry
        result, data = m1m3.GetSampleInclinometerData()
        telemetryTimestamp = data.Timestamp
        GreaterThan("SAL m1m3_InclinometerData.Timestamp", data.Timestamp, eventTimestamp)
                cur.execute("SELECT * FROM m1m3_InclinometerData WHERE Timestamp <= telemetryTimestamp ORDER BY Timestamp DESC LIMIT 1")
        row = cur.fetchone()
        print(row)
        actual = 0
        InTolerance("EFD m1m3_InclinometerData.Timestamp", actual, data.Timestamp, 0.001)
        InTolerance("EFD m1m3_InclinometerData.InclinometerAngle", actual, data.InclinometerAngle, 0.001)
        
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)   
        
        db.close()
        