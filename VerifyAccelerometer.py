import time
from Utilities import *
from SALPY_m1m3 import *

########################################################################
# Test Numbers: 
# Author:       CContaxis
# Description:  Verify accelerometer data available in all states 
#               excluding StandbyState
########################################################################

class VerifyAccelerometer:
    def Run(self, m1m3, sim):
        Header("Verify Accelerometer")
        self.CheckNoAccelerometer(m1m3, sim, "Standby")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        self.CheckAccelerometer(m1m3, sim, "Disabled")
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "Parked")
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "Raising")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "Active")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "Lowering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "ParkedEngineering")
        m1m3.RaiseM1M3(True)
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "RaisingEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "ActiveEngineering")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckAccelerometer(m1m3, sim, "LoweringEngineering")
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def CheckAccelerometer(self, m1m3, sim, state):
        SubHeader("Verify Accelerometer: %s State Validation" % (state))
        accelerometers = [
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0]
        ]
        for row in accelerometers:
            sim.setAccelerometerVoltage(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            time.sleep(1)
            result, data = m1m3.GetSampleAccelerometerData()
            InTolerance("AccelerometerData.RawAccelerometer[0]", data.RawAccelerometer[0], row[0], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[1]", data.RawAccelerometer[1], row[1], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[2]", data.RawAccelerometer[2], row[2], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[3]", data.RawAccelerometer[3], row[3], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[4]", data.RawAccelerometer[4], row[4], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[5]", data.RawAccelerometer[5], row[5], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[6]", data.RawAccelerometer[6], row[6], 0.001)
            InTolerance("AccelerometerData.RawAccelerometer[7]", data.RawAccelerometer[7], row[7], 0.001)
            
    def CheckNoAccelerometer(self, m1m3, sim, state):
        SubHeader("Verify No Accelerometer: %s State Validation" % (state))
        # Clear any existing sample in the queue
        result, data = m1m3.GetSampleAccelerometerData() 
        time.sleep(1)
        # See if new data came in
        result, data = m1m3.GetSampleAccelerometerData()
        Equal("No AccelerometerData", result, 0)
        time.sleep(1)
        # Check one last time to see if new data came in
        result, data = m1m3.GetSampleAccelerometerData()
        Equal("Still No AccelerometerData", result, 0)
        