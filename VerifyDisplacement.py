import time

from SALPY_m1m3 import *

from Utilities import *

########################################################################
# Test Numbers:
# Author:       CContaxis
# Description:  Verify displacement data available in all states
#               excluding StandbyState
########################################################################


class VerifyDisplacement:
    def Run(self, m1m3, sim):
        Header("Verify Displacement")
        self.CheckNoDisplacement(m1m3, sim, "Standby")
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
        self.CheckDisplacement(m1m3, sim, "Disabled")
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "Parked")
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "Raising")
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "Active")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "Lowering")
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "ParkedEngineering")
        m1m3.RaiseM1M3(True)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "RaisingEngineering")
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "ActiveEngineering")
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        self.CheckDisplacement(m1m3, sim, "LoweringEngineering")
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Disable()
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
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)

    def CheckDisplacement(self, m1m3, sim, state):
        SubHeader("Verify Displacement: %s State Validation" % (state))
        displacements = [
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        ]
        for row in displacements:
            sim.setDisplacement(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            )
            time.sleep(1.0)
            result, data = m1m3.GetSampleIMSData()
            InTolerance(
                "IMSData.RawSensorData[0]", data.RawSensorData[0], row[0], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[1]", data.RawSensorData[1], row[1], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[2]", data.RawSensorData[2], row[2], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[3]", data.RawSensorData[3], row[3], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[4]", data.RawSensorData[4], row[4], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[5]", data.RawSensorData[5], row[5], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[6]", data.RawSensorData[6], row[6], 0.001
            )
            InTolerance(
                "IMSData.RawSensorData[7]", data.RawSensorData[7], row[7], 0.001
            )

    def CheckNoDisplacement(self, m1m3, sim, state):
        SubHeader("Verify No Displacement: %s State Validation" % (state))
        # Clear any existing sample in the queue
        result, data = m1m3.GetSampleIMSData()
        time.sleep(1)
        # See if new data came in
        result, data = m1m3.GetSampleIMSData()
        Equal("No IMSData", result, -100)
        time.sleep(1)
        # Check one last time to see if new data came in
        result, data = m1m3.GetSampleIMSData()
        Equal("Still No IMSData", result, -100)
