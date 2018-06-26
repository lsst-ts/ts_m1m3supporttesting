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

TEST_PERCENTAGE = 2.0
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 200.0
TEST_SAMPLES_TO_AVERAGE = 10

DPValveLimitTable = [
    [101,0,0,0,0,0,0,0,0,0,0,0,0],
    [102,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [103,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [104,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [105,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [106,0,0,0,0,0,0,0,0,0,0,0,0],
    [107,0,0,0,0,0,0,0,0,0,0,0,0],
    [108,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [109,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [110,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [111,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [112,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [113,0,0,0,0,0,-3439.6384,0,0,0,0,-1547.758315,0],
    [114,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [115,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [116,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [117,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [118,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-663.324992,0],
    [119,0,0,0,0,0,0,0,0,0,0,0,0],
    [120,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [121,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [122,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [123,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [124,0,0,2501.5552,0,0,-2814.2496,0,1989.974976,0,0,-663.324992,0],
    [125,0,0,0,0,0,0,0,0,0,0,0,0],
    [126,0,0,0,0,0,-3439.6384,0,0,0,0,-1547.758315,0],
    [127,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [128,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [129,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [130,0,0,2814.2496,0,0,-3126.944,0,2211.083307,0,0,-663.324992,0],
    [131,0,0,0,0,0,0,0,0,0,0,0,0],
    [132,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [133,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [134,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [135,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [136,0,0,0,0,0,0,0,0,0,0,0,0],
    [137,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [138,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-442.2166614,0],
    [139,0,0,0,0,0,0,0,0,0,0,0,0],
    [140,0,0,0,0,0,0,0,0,0,0,0,0],
    [141,0,0,0,0,0,0,0,0,0,0,0,0],
    [142,0,0,0,0,0,0,0,0,0,0,0,0],
    [143,0,0,0,0,0,0,0,0,0,0,0,0],
    [207,0,0,0,0,0,0,0,0,0,0,0,0],
    [208,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [209,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [210,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [211,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [212,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [214,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [215,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [216,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [217,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [218,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-663.324992,0],
    [219,0,0,0,0,0,0,0,0,0,0,0,0],
    [220,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [221,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [222,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [223,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [224,0,0,2501.5552,0,0,-2814.2496,0,1989.974976,0,0,-663.324992,0],
    [225,0,0,0,0,0,0,0,0,0,0,0,0],
    [227,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [228,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [229,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [230,0,0,2814.2496,0,0,-3126.944,0,2211.083307,0,0,-663.324992,0],
    [231,0,0,0,0,0,0,0,0,0,0,0,0],
    [232,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [233,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [234,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [235,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [236,0,0,0,0,0,0,0,0,0,0,0,0],
    [237,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [238,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-442.2166614,0],
    [239,0,0,0,0,0,0,0,0,0,0,0,0],
    [240,0,0,0,0,0,0,0,0,0,0,0,0],
    [241,0,0,0,0,0,0,0,0,0,0,0,0],
    [242,0,0,0,0,0,0,0,0,0,0,0,0],
    [243,0,0,0,0,0,0,0,0,0,0,0,0],
    [301,0,0,0,0,0,0,0,0,0,0,0,0],
    [302,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [303,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [304,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [305,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [306,0,0,0,0,0,0,0,0,0,0,0,0],
    [307,0,0,0,0,0,0,0,0,0,0,0,0],
    [308,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [309,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [310,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [311,0,0,0,0,0,-1563.472,0,0,0,0,-2432.191637,0],
    [312,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [313,0,0,0,0,0,-3439.6384,0,0,0,0,-1547.758315,0],
    [314,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [315,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [316,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [317,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [318,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-663.324992,0],
    [319,0,0,0,0,0,0,0,0,0,0,0,0],
    [320,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [321,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [322,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [323,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [324,0,0,2501.5552,0,0,-2814.2496,0,1989.974976,0,0,-663.324992,0],
    [325,0,0,0,0,0,0,0,0,0,0,0,0],
    [326,0,0,0,0,0,-3439.6384,0,0,0,0,-1547.758315,0],
    [327,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [328,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [329,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [330,0,0,2814.2496,0,0,-3126.944,0,2211.083307,0,0,-663.324992,0],
    [331,0,0,0,0,0,0,0,0,0,0,0,0],
    [332,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [333,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [334,0,0,0,0,0,-1563.472,0,0,0,0,-2432.191637,0],
    [335,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [336,0,0,0,0,0,0,0,0,0,0,0,0],
    [337,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [338,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-442.2166614,0],
    [339,0,0,0,0,0,0,0,0,0,0,0,0],
    [340,0,0,0,0,0,0,0,0,0,0,0,0],
    [341,0,0,0,0,0,0,0,0,0,0,0,0],
    [342,0,0,0,0,0,0,0,0,0,0,0,0],
    [343,0,0,0,0,0,0,0,0,0,0,0,0],
    [407,0,0,0,0,0,0,0,0,0,0,0,0],
    [408,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [409,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [410,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [411,0,0,0,0,0,-1563.472,0,0,0,0,-2432.191637,0],
    [412,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [414,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [415,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [416,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [417,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [418,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-663.324992,0],
    [419,0,0,0,0,0,0,0,0,0,0,0,0],
    [420,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [421,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [422,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [423,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [424,0,0,2501.5552,0,0,-2814.2496,0,1989.974976,0,0,-663.324992,0],
    [425,0,0,0,0,0,0,0,0,0,0,0,0],
    [427,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [428,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [429,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [430,0,0,2814.2496,0,0,-3126.944,0,2211.083307,0,0,-663.324992,0],
    [431,0,0,0,0,0,0,0,0,0,0,0,0],
    [432,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [433,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [434,0,0,0,0,0,-1563.472,0,0,0,0,-2432.191637,0],
    [435,0,0,3439.6384,0,0,-2188.8608,1326.649984,0,0,-884.4333227,0,0],
    [436,0,0,0,0,0,0,0,0,0,0,0,0],
    [437,0,0,0,0,0,-3126.944,0,0,0,0,-1105.541653,0],
    [438,0,0,2501.5552,0,0,-2814.2496,0,2211.083307,0,0,-442.2166614,0],
    [439,0,0,0,0,0,0,0,0,0,0,0,0],
    [440,0,0,0,0,0,0,0,0,0,0,0,0],
    [441,0,0,0,0,0,0,0,0,0,0,0,0],
    [442,0,0,0,0,0,0,0,0,0,0,0,0],
    [443,0,0,0,0,0,0,0,0,0,0,0,0],
]

DPValveLimitTableActuatorId = 0
DPValveLimitTableAxialPushX = 1
DPValveLimitTableAxialPushY = 2
DPValveLimitTableAxialPushZ = 3
DPValveLimitTableAxialPullX = 4
DPValveLimitTableAxialPullY = 5
DPValveLimitTableAxialPullZ = 6
DPValveLimitTableLateralPushX = 7
DPValveLimitTableLateralPushY = 8
DPValveLimitTableLateralPushZ = 9
DPValveLimitTableLateralPullX = 10
DPValveLimitTableLateralPullY = 11
DPValveLimitTableLateralPullZ = 12

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
        outputFile = "ActId,XSetpoint,YSetpoint,ZSetpoint,XForce,YForce,ZForce\r\n"
        
        # Iterate through all 156 force actuators
        for row in forceActuatorTable:
            index = row[forceActuatorTableIndexIndex]
            id = row[forceActuatorTableIDIndex]
            orientation = row[forceActuatorTableOrientationIndex]
            x = -1        # X index for data access, if -1 no X data available
            y = -1        # Y index for data access, if -1 no Y data available
            s = -1        # S (Secondary Cylinder) index for data access, if -1 no S data available
            z = index     # Z index for data access, all force actuators have Z data
            dpRow = DPValveLimitTable[z]
            
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

            Header("Verify Force Actuator %d Commands and Telemetry" % id)
            
            # Get start time
            result, data = m1m3.GetSampleHardpointActuatorData()
            startTimestamp = data.Timestamp
            
            # Define the tests to potentially execute
            tests = [
                ["AxialPush", dpRow[DPValveLimitTableAxialPushX], dpRow[DPValveLimitTableAxialPushY], dpRow[DPValveLimitTableAxialPushZ]],
                ["AxialPull", dpRow[DPValveLimitTableAxialPullX], dpRow[DPValveLimitTableAxialPullY], dpRow[DPValveLimitTableAxialPullZ]],
                ["LateralPush", dpRow[DPValveLimitTableLateralPushX], dpRow[DPValveLimitTableLateralPushY], dpRow[DPValveLimitTableLateralPushZ]],
                ["LateralPull", dpRow[DPValveLimitTableLateralPullX], dpRow[DPValveLimitTableLateralPullY], dpRow[DPValveLimitTableLateralPullZ]],
            ]
            # Run each test
            for testRow in tests:
                name = testRow[0]
                xLimit = testRow[1]
                yLimit = testRow[2]
                zLimit = testRow[3]
                # If the current actuator has a limit, test it
                if xLimit != 0 or yLimit != 0 or zLimit != 0:
                    outputFile = outputFile + ("%d," % id)
                    # Set test forces to limit + a percentage
                    if x != -1:
                        xForces[x] = xLimit * TEST_PERCENTAGE
                        outputFile = outputFile + ("%0.3f,0.0," % xForces[x])
                    elif y != -1:
                        yForces[y] = yLimit * TEST_PERCENTAGE
                        outputFile = outputFile + ("0.0,%0.3f," % yForces[y])
                    else:
                        outputFile = outputFile + "0.0,0.0,"
                    zForces[z] = zLimit * TEST_PERCENTAGE
                    outputFile = outputFile + ("%0.3f," % zForces[z])
                    
                    # Apply the X only offset force
                    m1m3.ApplyOffsetForces(xForces, yForces, zForces)
                    
                    # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                    time.sleep(TEST_SETTLE_TIME)
                    
                    # Check force actuator force
                    datas = self.SampleForceActuators(m1m3)
                    if x != -1:
                        xActual = Average(datas, lambda d: d.XForce[x])
                        InTolerance("FA%03d %s ForceActuatorData.XForce[%d]" % (id, name, x), xActual, xLimit, TEST_TOLERANCE)
                        outputFile = outputFile + ("%0.3f,0.0," % xActual)
                    elif y != -1:
                        yActual = Average(datas, lambda d: d.YForce[y])
                        InTolerance("FA%03d %s ForceActuatorData.YForce[%d]" % (id, name, y), yActual, yLimit, TEST_TOLERANCE)
                        outputFile = outputFile + ("0.0,%0.3f," % yActual)
                    else:
                        outputFile = outputFile + "0.0,0.0,"
                    zActual = Average(datas, lambda d: d.ZForce[z])
                    InTolerance("FA%03d %s ForceActuatorData.ZForce[%d]" % (id, name, z), zActual, zLimit, TEST_TOLERANCE)
                    outputFile = outputFile + ("%0.3f\r\n" % zActual)
                    
                    # Clear test forces
                    if x != -1:
                        xForces[x] = 0
                    if y != -1:
                        yForces[y] = 0
                    zForces[z] = 0
                    
                    # Clear offset forces
                    m1m3.ClearOffsetForces()
                    
                    # Wait a bit before continuing
                    time.sleep(TEST_SETTLE_TIME)
                    
                    
        # Get output file path
        path = GetFilePath("%d-ForceActuator-DPValve.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        
        # Write output file
        file = open(path, "w+")
        file.write(outputFile)
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