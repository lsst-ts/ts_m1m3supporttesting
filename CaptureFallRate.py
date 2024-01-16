########################################################################
# Test Numbers: M13T-DPV
# Author:       CContaxis
# Description:  Force actuator DP valve test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an axial push limit
#     - Apply axial push forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an axial pull limit
#     - Apply axial pull forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an lateral push limit
#     - Apply lateral push forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
#   - If the force actuator has an lateral pull limit
#     - Apply lateral pull forces 15% higher
#     - Verify the limited force is being measured
#     - Clear offset forces
# - Transition from parked engineering state to standby
########################################################################

import math
import time

from SALPY_m1m3 import *

from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *
from Utilities import *

TEST_PRE_FALL_WAIT = 10.0


class CaptureFallRate:
    def Run(self, m1m3, sim, efd):
        Header("Capture Fall Rate")

        # Transition to disabled state
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

        # Transition to parked state
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)

        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_ParkedEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)

        # Transition to raising engineering state
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState",
            data.DetailedState,
            m1m3_shared_DetailedStates_RaisingEngineeringState,
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)

        # Wait until active engineering state
        WaitUntil(
            "DetailedState",
            600,
            lambda: m1m3.GetEventDetailedState()[1].DetailedState
            == m1m3_shared_DetailedStates_ActiveEngineeringState,
        )

        # Header
        outputText = "Timestamp"
        for i in range(8):
            outputText = outputText + ",IMS%d" % (i + 1)
        for i in range(12):
            outputText = outputText + ",FAx%d" % (i + 1)
        for i in range(100):
            outputText = outputText + ",FAy%d" % (i + 1)
        for i in range(156):
            outputText = outputText + ",FAz%d" % (i + 1)
        outputText = outputText + "\r\n"

        # Get start timestamp
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTimestamp = data.Timestamp

        Log("Pull GIS when ready")
        samples = 0
        while samples < 1000:
            rtn, ims = m1m3.GetSampleIMSData()
            if rtn >= 0:
                rtn, fa = m1m3.GetSampleForceActuatorData()
                if rtn >= 0:
                    outputText = outputText + "%0.3f" % ims.Timestamp
                    for i in range(8):
                        outputText = outputText + ",%0.6f" % ims.RawSensorData[i]
                    for i in range(12):
                        outputText = outputText + ",%0.6f" % fa.XForce[i]
                    for i in range(100):
                        outputText = outputText + ",%0.6f" % fa.YForce[i]
                    for i in range(156):
                        outputText = outputText + ",%0.6f" % fa.ZForce[i]
                    outputText = outputText + "\r\n"
                    samples += 1

        # Write the file
        path = GetFilePath("%d-CaptureFallRate.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write(outputText)
        file.close()

        # Transition to standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal(
            "DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState
        )
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)

    def SampleForceActuators(self, m1m3):
        # Get force actuator data
        datas = []
        while len(datas) < TEST_SAMPLES_TO_AVERAGE:
            result, data = m1m3.GetSampleForceActuatorData()
            if result >= 0:
                datas.append(data)
        return datas


if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    CaptureFallRate().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
