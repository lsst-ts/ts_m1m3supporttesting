########################################################################
# Test Numbers: M13T-004
# Author:       CContaxis
# Description:  Individual hardpoint breakaway test
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each hardpoint actuator
#   - Perform the following steps for full extension and full retraction
#     - Issue hardpoint step command
#     - Verify hardpoint is moving
#     - Wait for hardpoint motion to complete or a limit switch is operated
#     - Issue stop hardpoint motion command
#     - Verify hardpoint is stopped
#     - Query EFD for hardpoint monitor data for test duration
#     - Query EFD for hardpoint actuator data for test duration
# - Transition from parked engineering to standby state
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

class M13T004:
    def Run(self, m1m3, sim, efd, header):
        Header(header)
        
        # Transition to disabled state
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to parked state state
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
        
        # Iterate through the 6 hardpoint actuators
        for index in range(6):
            actId = index + 1
            SubHeader("Hardpoint Actuator #%d" % (actId))
            
            # Issue through a number of steps for each actuator
            for step in [-999999999, 999999999]:
                # Give time for a sample
                time.sleep(1)
            
                # Get the start timestamp for collecting data from the EFD
                result, data = m1m3.GetSampleHardpointActuatorData()
                startTimestamp = data.Timestamp
                
                # Setup the simulator response (ignored if running at CAID)
                sim.setHPForceAndStatus(actId, 0, 100 + index, 0)
                sim.setILCStatus(actId, 0, 0x0000, 0)
                                
                # Wait a bit
                time.sleep(1)

                # Command the steps
                tmp = [0] * 6
                tmp[index] = step
                m1m3.MoveHardpointActuators(tmp)
                
                # Verify the commanded actuator is moving
                result, data = m1m3.GetEventHardpointActuatorState()
                Equal("Actuator %d moving" % (actId), data.MotionState[index], 2)
                
                # Wait for moving to complete or a limit switch is hit
                loopCount = 0
                while True:
                    # Check if moving is complete
                    result, data = m1m3.GetEventHardpointActuatorState()
                    if result >= 0 and data.MotionState[index] == 0:
                        break
                    # Check if limit switch is hit
                    result, data = m1m3.GetEventHardpointActuatorWarning()
                    if result >= 0 and (data.LimitSwitch1Operated[index] or data.LimitSwitch2Operated[index]):
                        break
                    status = 0
                    # For simulation testing toggle a limit switch after 10 seconds
                    result, data = m1m3.GetSampleHardpointActuatorData()
                    currentTimestamp = data.Timestamp
                    status1 = 0
                    status2 = 0
                    if abs(currentTimestamp - startTimestamp) >= 10.0:
                        status1 = 0x04 + 0x08
                        status2 = 0x0100 + 0x0200
                    sim.setHPForceAndStatus(actId, status1, loopCount, loopCount * 2)
                    sim.setILCStatus(actId, 0, status2, 0)
                    loopCount += 1
                    time.sleep(0.5)
                    
                # Stop hardpoint motion
                m1m3.StopHardpointMotion()
                
                # Verify hardpoint motion has stopped
                result, data = m1m3.GetEventHardpointActuatorState()
                Equal("Actuator %d stopped" % (actId), data.MotionState[index], 0)
                
                # Give a little buffer room before completing this part of the test
                time.sleep(1)
                
                # Get the stop timestamp for collecting data from the EFD
                result, data = m1m3.GetSampleHardpointActuatorData()
                stopTimestamp = data.Timestamp
                
                # Report the start and stop timestamps to the log
                Log("Start Timestamp: %0.6f" % startTimestamp)
                Log("Stop Timestamp:  %0.6f" % stopTimestamp)

                # Generate the hardpoint monitor data file
                rows = efd.QueryAll("SELECT Timestamp, BreakawayLVDT_%d, DisplacementLVDT_%d, BreakawayPressure_%d FROM m1m3_HardpointMonitorData WHERE Timestamp >= %0.3f AND Timestamp <= %0.3f ORDER BY Timestamp ASC" % (actId, actId, actId, startTimestamp, stopTimestamp))
                Log("Got %d rows" % len(rows))
                path = GetFilePath("%d-Hardpoint%d-MonitorData.csv" % (int(startTimestamp), actId))
                Log("File path: %s" % path)
                file = open(path, "w+")
                file.write("Timestamp,BreakawayLVDT,DisplacementLVDT,BreakawayPressure")
                for row in rows:
                    file.write("%0.3f,%0.9f,%0.9f,%0.3f" % (row[0], row[1], row[2], row[3]))
                file.close()
                
                # Generate the hardpoint actuator data file
                rows = efd.QueryAll("SELECT Timestamp, MeasuredForce_%d, Encoder_%d, Displacement_%d FROM m1m3_HardpointActuatorData WHERE Timestamp >= %0.3f AND Timestamp <= %0.3f ORDER BY Timestamp ASC" % (actId, actId, actId, startTimestamp, stopTimestamp))
                Log("Got %d rows" % len(rows))
                path = GetFilePath("%d-Hardpoint%d-ActuatorData.csv" % (int(startTimestamp), actId))
                Log("File path: %s" % path)
                file = open(path, "w+")
                file.write("Timestamp,MeasuredForce,Encoder,Displacement")
                for row in rows:
                    file.write("%0.3f,%0.9f,%d,%0.9f" % (row[0], row[1], row[2], row[3]))
                file.close()
       
        # Transition to the disabled state
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Transition to the standby state
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T004().Run(m1m3, sim, efd, "M13T-004: Individual Hardpoint Breakaway Test")       