from SALPY_m1m3 import *

from Utilities import *


class VerifyStateChanges:
    def Run(self, m1m3, sim):
        Header("Verify State Changes")
        self.CheckParameterValidation(m1m3, sim)
        self.CheckStandbyState(m1m3, sim)
        self.CheckDisabledState(m1m3, sim)
        self.CheckParkState(m1m3, sim)  # Passes
        self.CheckRaisingState(m1m3, sim)
        self.CheckActiveState(m1m3, sim)
        self.CheckLoweringState(m1m3, sim)
        self.CheckParkEngineeringState(m1m3, sim)
        self.CheckRaisingEngineeringState(m1m3, sim)
        self.CheckActiveEngineeringState(m1m3, sim)
        self.CheckLoweringEngineeringState(m1m3, sim)

    def CheckParameterValidation(self, m1m3, sim):
        SubHeader("Verify State Changes: State Command Parameter Validation")
        m1m3.Start("Default", False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enable Rejected", result, 0)
        m1m3.RaiseM1M3(False, False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Standby Rejected", result, 0)
        m1m3.Shutdown(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)

    def CheckStandbyState(self, m1m3, sim):
        SubHeader("Verify State Changes: Standby State Validation")
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
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enable Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Standby Rejected", result, 0)
        # Ignore because this will shutdown the software
        # m1m3.Shutdown()
        # result, data = m1m3.GetEventCommandRejectionWarning()
        # Equal("Shutdown Rejected", result, 0)

    def CheckDisabledState(self, m1m3, sim):
        SubHeader("Verify State Changes: Disabled State Validation")
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
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
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
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)

    def CheckParkState(self, m1m3, sim):
        SubHeader("Verify State Changes: Parked State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
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

    def CheckRaisingState(self, m1m3, sim):
        SubHeader("Verify State Changes: Raising State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
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

    def CheckActiveState(self, m1m3, sim):
        SubHeader("Verify State Changes: Active State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ActiveState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
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

    def CheckLoweringState(self, m1m3, sim):
        SubHeader("Verify State Changes: Lowering State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedState,
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

    def CheckParkEngineeringState(self, m1m3, sim):
        SubHeader("Verify State Changes: Parked Engineering State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
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

    def CheckRaisingEngineeringState(self, m1m3, sim):
        SubHeader("Verify State Changes: Raising Engineering State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
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

    def CheckActiveEngineeringState(self, m1m3, sim):
        SubHeader("Verify State Changes: Active Engineering State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ActiveState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
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

    def CheckLoweringEngineeringState(self, m1m3, sim):
        SubHeader("Verify State Changes: Lowering Engineering State Validation")
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
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
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
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil(
            "DetailedState",
            300,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_LoweringEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.Start("Default")
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Enable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Raise M1M3 Rejected", result, 0)
        m1m3.AbortRaiseM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Abort RaiseM1M3 Rejected", result, 0)
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Lower M1M3 Rejected", result, 0)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Enter Engineering Rejected", result, 0)
        m1m3.ExitEngineering()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Exit Engineering Rejected", result, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Disable Rejected", result, 0)
        m1m3.Standby()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Start Rejected", result, 0)
        m1m3.Shutdown()
        result, data = m1m3.GetEventCommandRejectionWarning()
        Equal("Shutdown Rejected", result, 0)
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
