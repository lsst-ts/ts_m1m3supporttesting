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

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

TEST_SETTLE_TIME = 2.0
TEST_SAMPLES_TO_AVERAGE = 50

class M13TDPV:
    def Run(self, m1m3, sim, efd):
        Header("M13T-DPV: Actuator Force DP Valve Limits")
        
        # Transition to disabled state
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to parked state
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Transition to parked engineering state
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Prepare force data
        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156
        xIndex = 0
        yIndex = 0
        sIndex = 0

        # Get start time
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTimestamp = data.Timestamp

        # Get output file path
        path = GetFilePath("%d-ForceActuator-DPValve.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        
        # Write output file
        file = open(path, "w+")
        file.write("ActId,AxialCylinderSetpoint,LateralCylinderSetpoint,AxialCylinderForce,LateralCylinderForce\r\n")        
        
        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            index = row[forceActuatorTableIndexIndex]
            id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]
            x = -1        # X index for data access, if -1 no X data available
            y = -1        # Y index for data access, if -1 no Y data available
            s = -1        # S (Secondary Cylinder) index for data access, if -1 no S data available
            z = index     # Z index for data access, all force actuators have Z data
            
            # Set the X and S index if applicable
            if orientation in ['+X', '-X']:
                x = xIndex
                s = sIndex
                xIndex += 1
                sIndex += 1

            # Set the Y and S index if applicable
            if orientation in ['+Y', '-Y']:
                y = yIndex
                s = sIndex
                yIndex += 1
                sIndex += 1

            # Setup test forces
            if orientation in ['+X']:
                tests = [
                    [4243, 0.0, 10243],
                    [4243, 0.0, -1757],
                    [-4243, 0.0, -10243],
                    [-4243, 0.0, 1757],
                ]
            elif orientation in ['-X']:
                tests = [
                    [-4243, 0.0, 10243],
                    [-4243, 0.0, -1757],
                    [4243, 0.0, -10243],
                    [4243, 0.0, 1757],
                ]
            elif orientation in ['+Y']:
                tests = [
                    [0.0, 4243, 10243],
                    [0.0, 4243, -1757],
                    [0.0, -4243, -10243],
                    [0.0, -4243, 1757],
                ]
            elif orientation in ['-Y']:
                tests = [
                    [0.0, -4243, 10243],
                    [0.0, -4243, -1757],
                    [0.0, 4243, -10243],
                    [0.0, 4243, 1757],
                ]
            else:
                tests = [
                    [0.0, 0.0, 6000.0],
                    [0.0, 0.0, -6000.0]
                ]
                
            Header("Verify Force Actuator %d" % id)

            # Run each test
            for testRow in tests:
                xSetpoint = testRow[0]
                ySetpoint = testRow[1]
                zSetpoint = testRow[2]

                # Flush applied cylinder forces
                rtn, data = m1m3.GetEventAppliedCylinderForces()

                # Apply the force
                if x != -1:
                    xForces[x] = xSetpoint
                if y != -1:
                    yForces[y] = ySetpoint
                zForces[z] = zSetpoint
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                
                # Wait for the forces to settle
                time.sleep(TEST_SETTLE_TIME)

                # Capture applied cylinder forces
                rtn, data = m1m3.GetEventAppliedCylinderForces()
                pSetpoint = data.PrimaryCylinderForces[z]
                sSetpoint = 0.0
                if s != -1:
                    sSetpoint = data.SecondaryCylinderForces[s]

                # Capture measured cylinder forces
                datas = self.SampleForceActuators(m1m3)
                pForce = Average(datas, lambda d: d.PrimaryCylinderForce[z])
                sForce = 0.0
                if s != -1:
                    sForce = Average(datas, lambda d: d.SecondaryCylinderForce[s])

                # Log data to output file
                file.write("%d,%0.1f,%0.1f,%0.1f,%0.1f\r\n" % (id, pSetpoint / 1000.0, sSetpoint / 1000.0, pForce, sForce))
                    
                # Clear test forces
                if x != -1:
                    xForces[x] = 0.0
                if y != -1:
                    yForces[y] = 0.0
                zForces[z] = 0.0
                m1m3.ClearOffsetForces()
                    
                # Wait a bit before continuing
                time.sleep(TEST_SETTLE_TIME)
                    
                    
        # Close output file
        file.close()
            
        # Transition to disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
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
    M13TDPV().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)