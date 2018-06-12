########################################################################
# Test Numbers: M13T-027
# Author:       CContaxis
# Description:  Force actuator limits
# Steps:
# - Transition from standby to parked engineering state
# - Perform the following steps for each force actuator
#   - If the force actuator has an X component
#     - Apply a X force offset 15% higher than the max X limit
#     - Verify the X force is rejected
#     - Verify the limited X force is applied
#     - Verify the limited X force is being measured
#     - Apply a X force offset 15% lower than the min X limit
#     - Verify the X force is rejected
#     - Verify the limited X force is applied
#     - Verify the limited X force is being measured
#     - Clear offset forces
#   - If the force actuator has an Y component
#     - Apply a Y force offset 15% higher than the max Y limit
#     - Verify the Y force is rejected
#     - Verify the limited Y force is applied
#     - Verify the limited Y force is being measured
#     - Apply a Y force offset 15% lower than the min Y limit
#     - Verify the Y force is rejected
#     - Verify the limited Y force is applied
#     - Verify the limited Y force is being measured
#     - Clear offset forces
#   - Apply a Z force offset 15% higher than the max Z limit
#   - Verify the Z force is rejected
#   - Verify the limited Z force is applied
#   - Verify the limited Z force is being measured
#   - Apply a Z force offset 15% lower than the min Z limit
#   - Verify the Z force is rejected
#   - Verify the limited Z force is applied
#   - Verify the limited Z force is being measured
#   - Clear offset forces
# - Transition from parked engineering state to standby
########################################################################

import time
import math
from Utilities import *
from SALPY_m1m3 import *
from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *

TEST_PERCENTAGE = 1.15
TEST_SETTLE_TIME = 3.0
TEST_TOLERANCE = 5.0
TEST_SAMPLES_TO_AVERAGE = 10

forceActuatorXLimitTable = [
    [112,-75,0,0,75],
    [128,-75,0,0,75],
    [135,-75,0,0,75],
    [212,-75,0,0,75],
    [228,-75,0,0,75],
    [235,-75,0,0,75],
    [312,-75,0,0,75],
    [328,-75,0,0,75],
    [335,-75,0,0,75],
    [412,-75,0,0,75],
    [428,-75,0,0,75],
    [435,-75,0,0,75],
]
forceActuatorYLimitTable = [
    [102,-70,0,0,190       ],
    [103,-110.6,0,0,265.3  ],
    [104,-110.6,0,0,265.3  ],
    [105,-110.6,0,0,265.3  ],
    [108,-110.6,0,0,265.3  ],
    [109,-110.6,0,0,265.3  ],
    [110,-110.6,0,0,265.3  ],
    [111,-110.6,0,0,265.3  ],
    [113,-50,0,0,200       ],
    [114,-110.6,0,0,265.3  ],
    [115,-110.6,0,0,265.3  ],
    [116,-110.6,0,0,265.3  ],
    [117,-110.6,0,0,265.3  ],
    [118,-47.5,0,0,190     ],
    [120,-110.6,0,0,265.3  ],
    [121,-110.6,0,0,265.3  ],
    [122,-110.6,0,0,265.3  ],
    [123,-110.6,0,0,265.3  ],
    [124,-55,0,0,180       ],
    [126,-50,0,0,200       ],
    [127,-110.6,0,0,265.3  ],
    [129,-110.6,0,0,265.3  ],
    [130,-40,0,0,153       ],
    [132,-110.6,0,0,265.3  ],
    [133,-110.6,0,0,265.3  ],
    [134,-110.6,0,0,265.3  ],
    [137,-110.6,0,0,265.3  ],
    [138,-23,0,0,177       ],
    [208,-110.6,0,0,265.3  ],
    [209,-110.6,0,0,265.3  ],
    [210,-110.6,0,0,265.3  ],
    [211,-110.6,0,0,265.3  ],
    [214,-110.6,0,0,265.3  ],
    [215,-110.6,0,0,265.3  ],
    [216,-110.6,0,0,265.3  ],
    [217,-110.6,0,0,265.3  ],
    [218,-47.5,0,0,190     ],
    [220,-110.6,0,0,265.3  ],
    [221,-110.6,0,0,265.3  ],
    [222,-110.6,0,0,265.3  ],
    [223,-110.6,0,0,265.3  ],
    [224,-55,0,0,180       ],
    [227,-110.6,0,0,265.3  ],
    [229,-110.6,0,0,265.3  ],
    [230,-40,0,0,153       ],
    [232,-110.6,0,0,265.3  ],
    [233,-110.6,0,0,265.3  ],
    [234,-110.6,0,0,265.3  ],
    [237,-110.6,0,0,265.3  ],
    [238,-23,0,0,177       ],
    [302,-110.6,0,0,265.3  ],
    [303,-110.6,0,0,265.3  ],
    [304,-110.6,0,0,265.3  ],
    [305,-110.6,0,0,265.3  ],
    [308,-110.6,0,0,265.3  ],
    [309,-110.6,0,0,265.3  ],
    [310,-110.6,0,0,265.3  ],
    [311,-75,0,0,180       ],
    [313,-50,0,0,200       ],
    [314,-110.6,0,0,265.3  ],
    [315,-110.6,0,0,265.3  ],
    [316,-110.6,0,0,265.3  ],
    [317,-110.6,0,0,265.3  ],
    [318,-47.5,0,0,190     ],
    [320,-110.6,0,0,265.3  ],
    [321,-110.6,0,0,265.3  ],
    [322,-110.6,0,0,265.3  ],
    [323,-110.6,0,0,265.3  ],
    [324,-55,0,0,180       ],
    [326,-50,0,0,200       ],
    [327,-110.6,0,0,265.3  ],
    [329,-110.6,0,0,265.3  ],
    [330,-40,0,0,153       ],
    [332,-110.6,0,0,265.3  ],
    [333,-110.6,0,0,265.3  ],
    [334,-75,0,0,180       ],
    [337,-110.6,0,0,265.3  ],
    [338,-23,0,0,177       ],
    [408,-110.6,0,0,265.3  ],
    [409,-110.6,0,0,265.3  ],
    [410,-110.6,0,0,265.3  ],
    [411,-75,0,0,180       ],
    [414,-110.6,0,0,265.3  ],
    [415,-110.6,0,0,265.3  ],
    [416,-110.6,0,0,265.3  ],
    [417,-110.6,0,0,265.3  ],
    [418,-47.5,0,0,190     ],
    [420,-110.6,0,0,265.3  ],
    [421,-110.6,0,0,265.3  ],
    [422,-110.6,0,0,265.3  ],
    [423,-110.6,0,0,265.3  ],
    [424,-55,0,0,180       ],
    [427,-110.6,0,0,265.3  ],
    [429,-110.6,0,0,265.3  ],
    [430,-40,0,0,153       ],
    [432,-110.6,0,0,265.3  ],
    [433,-110.6,0,0,265.3  ],
    [434,-75,0,0,180       ],
    [437,-110.6,0,0,265.3  ],
    [438,-23,0,0,177       ],
]
forceActuatorZLimitTable = [
    [101,-226.1,0,0,226.1   ],
    [102,-100,0,0,200       ],
    [103,-100,0,0,200       ],
    [104,-100,0,0,200       ],
    [105,-100,0,0,200       ],
    [106,226.1,0,0,226.1    ],
    [107,-226.1,0,0,226.1   ],
    [108,-100,0,0,200       ],
    [109,-100,0,0,200       ],
    [110,-100,0,0,200       ],
    [111,-100,0,0,200       ],
    [112,-125,0,0,220       ],
    [113,-120,0,0,200       ],
    [114,-100,0,0,200       ],
    [115,-100,0,0,200       ],
    [116,-100,0,0,200       ],
    [117,-100,0,0,200       ],
    [118,-75,0,0,200        ],
    [119,-133,0,0,133       ],
    [120,-100,0,0,200       ],
    [121,-100,0,0,200       ],
    [122,-100,0,0,200       ],
    [123,-100,0,0,200       ],
    [124,-80,0,0,200        ],
    [125,226.1,0,0,226.1    ],
    [126,-120,0,0,200       ],
    [127,-100,0,0,200       ],
    [128,-125,0,0,220       ],
    [129,-100,0,0,200       ],
    [130,-110,0,0,180       ],
    [131,226.1,0,0,226.1    ],
    [132,-100,0,0,200       ],
    [133,-100,0,0,200       ],
    [134,-100,0,0,200       ],
    [135,-125,0,0,220       ],
    [136,226.1,0,0,226.1    ],
    [137,-100,0,0,200       ],
    [138,-95,0,0,200        ],
    [139,226.1,0,0,226.1    ],
    [140,226.1,0,0,226.1    ],
    [141,226.1,0,0,226.1    ],
    [142,226.1,0,0,226.1    ],
    [143,-133,0,0,133       ],
    [207,-226.1,0,0,226.1   ],
    [208,-100,0,0,200       ],
    [209,-100,0,0,200       ],
    [210,-100,0,0,200       ],
    [211,-100,0,0,200       ],
    [212,-125,0,0,220       ],
    [214,-100,0,0,200       ],
    [215,-100,0,0,200       ],
    [216,-100,0,0,200       ],
    [217,-100,0,0,200       ],
    [218,-75,0,0,200        ],
    [219,-133,0,0,133       ],
    [220,-100,0,0,200       ],
    [221,-100,0,0,200       ],
    [222,-100,0,0,200       ],
    [223,-100,0,0,200       ],
    [224,-80,0,0,200        ],
    [225,226.1,0,0,226.1    ],
    [227,-100,0,0,200       ],
    [228,-125,0,0,220       ],
    [229,-100,0,0,200       ],
    [230,-110,0,0,180       ],
    [231,226.1,0,0,226.1    ],
    [232,-100,0,0,200       ],
    [233,-100,0,0,200       ],
    [234,-100,0,0,200       ],
    [235,-125,0,0,220       ],
    [236,226.1,0,0,226.1    ],
    [237,-100,0,0,200       ],
    [238,-95,0,0,200        ],
    [239,226.1,0,0,226.1    ],
    [240,226.1,0,0,226.1    ],
    [241,226.1,0,0,226.1    ],
    [242,226.1,0,0,226.1    ],
    [243,-133,0,0,133       ],
    [301,-226.1,0,0,226.1   ],
    [302,-100,0,0,200       ],
    [303,-100,0,0,200       ],
    [304,-100,0,0,200       ],
    [305,-100,0,0,200       ],
    [306,226.1,0,0,226.1    ],
    [307,-226.1,0,0,226.1   ],
    [308,-100,0,0,200       ],
    [309,-100,0,0,200       ],
    [310,-100,0,0,200       ],
    [311,-80,0,0,180        ],
    [312,-125,0,0,220       ],
    [313,-120,0,0,200       ],
    [314,-100,0,0,200       ],
    [315,-100,0,0,200       ],
    [316,-100,0,0,200       ],
    [317,-100,0,0,200       ],
    [318,-75,0,0,200        ],
    [319,-133,0,0,133       ],
    [320,-100,0,0,200       ],
    [321,-100,0,0,200       ],
    [322,-100,0,0,200       ],
    [323,-100,0,0,200       ],
    [324,-80,0,0,200        ],
    [325,226.1,0,0,226.1    ],
    [326,-120,0,0,200       ],
    [327,-100,0,0,200       ],
    [328,-125,0,0,220       ],
    [329,-100,0,0,200       ],
    [330,-110,0,0,180       ],
    [331,226.1,0,0,226.1    ],
    [332,-100,0,0,200       ],
    [333,-100,0,0,200       ],
    [334,-80,0,0,180        ],
    [335,-125,0,0,220       ],
    [336,226.1,0,0,226.1    ],
    [337,-100,0,0,200       ],
    [338,-95,0,0,200        ],
    [339,226.1,0,0,226.1    ],
    [340,226.1,0,0,226.1    ],
    [341,226.1,0,0,226.1    ],
    [342,226.1,0,0,226.1    ],
    [343,-133,0,0,133       ],
    [407,-226.1,0,0,226.1   ],
    [408,-100,0,0,200       ],
    [409,-100,0,0,200       ],
    [410,-100,0,0,200       ],
    [411,-80,0,0,180        ],
    [412,-125,0,0,220       ],
    [414,-100,0,0,200       ],
    [415,-100,0,0,200       ],
    [416,-100,0,0,200       ],
    [417,-100,0,0,200       ],
    [418,-75,0,0,200        ],
    [419,-133,0,0,133       ],
    [420,-100,0,0,200       ],
    [421,-100,0,0,200       ],
    [422,-100,0,0,200       ],
    [423,-100,0,0,200       ],
    [424,-80,0,0,200        ],
    [425,226.1,0,0,226.1    ],
    [427,-100,0,0,200       ],
    [428,-125,0,0,220       ],
    [429,-100,0,0,200       ],
    [430,-110,0,0,180       ],
    [431,226.1,0,0,226.1    ],
    [432,-100,0,0,200       ],
    [433,-100,0,0,200       ],
    [434,-80,0,0,180        ],
    [435,-125,0,0,220       ],
    [436,226.1,0,0,226.1    ],
    [437,-100,0,0,200       ],
    [438,-95,0,0,200        ],
    [439,226.1,0,0,226.1    ],
    [440,226.1,0,0,226.1    ],
    [441,226.1,0,0,226.1    ],
    [442,226.1,0,0,226.1    ],
    [443,-133,0,0,133       ],
]

forceActuatorLimitActuatorId = 0
forceActuatorLimitMin = 1
forceActuatorLimitMax = 4

class M13T027:
    def Run(self, m1m3, sim, efd):
        Header("M13T-027: Actuator Force Limits")
        
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

            Header("Verify Force Actuator %d Commands and Telemetry" % id)

            # If the current actuator has X data available, test it
            if x != -1:
                # Set the commanded X force
                xForces[x] = forceActuatorXLimitTable[x][forceActuatorLimitMax] * TEST_PERCENTAGE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, xForces[x], 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the rejected forces match the commanded values
                result, data = m1m3.GetEventRejectedForces()
                InTolerance("FA%03d +X RejectedForces.XForces[%d]" % (id, x), data.XForces[x], xForces[x], TEST_TOLERANCE)
                InTolerance("FA%03d +X RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +X AppliedForces.XForces[%d]" % (id, x), data.XForces[x], forceActuatorXLimitTable[x][forceActuatorLimitMax], TEST_TOLERANCE)
                InTolerance("FA%03d +X AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)               
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +X ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda x: x.XForce[x]), forceActuatorXLimitTable[x][forceActuatorLimitMax], TEST_TOLERANCE)
                InTolerance("FA%03d +X ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), 0.0, TEST_TOLERANCE)
                
                # Set the commanded X force
                xForces[x] = forceActuatorXLimitTable[x][forceActuatorLimitMin] * TEST_PERCENTAGE

                # Apply the X only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, xForces[x], 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the rejected forces match the commanded values
                result, data = m1m3.GetEventRejectedForces()
                InTolerance("FA%03d -X RejectedForces.XForces[%d]" % (id, x), data.XForces[x], xForces[x], TEST_TOLERANCE)
                InTolerance("FA%03d -X RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d -X AppliedForces.XForces[%d]" % (id, x), data.XForces[x], forceActuatorXLimitTable[x][forceActuatorLimitMin], TEST_TOLERANCE)
                InTolerance("FA%03d -X AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)               
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d -X ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda x: x.XForce[x]), forceActuatorXLimitTable[x][forceActuatorLimitMin], TEST_TOLERANCE)
                InTolerance("FA%03d -X ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), 0.0, TEST_TOLERANCE)               
                
                # Clear force setpoint for this actuator
                xForces[x] = 0
                
                # Clear offset forces
                m1m3.ClearOffsetForces()
                
                # Wait a bit before continuing
                time.sleep(TEST_SETTLE_TIME)
                
            # If the current actuator has Y data available, test it
            if y != -1:
                # Set the commanded Y force
                yForces[y] = forceActuatorYLimitTable[y][forceActuatorLimitMax] * TEST_PERCENTAGE

                # Apply the Y only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, yForces[y], 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the rejected forces match the commanded values
                result, data = m1m3.GetEventRejectedForces()
                InTolerance("FA%03d +Y RejectedForces.YForces[%d]" % (id, y), data.YForces[y], yForces[y], TEST_TOLERANCE)
                InTolerance("FA%03d +Y RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +Y AppliedForces.YForces[%d]" % (id, y), data.YForces[y], forceActuatorYLimitTable[y][forceActuatorLimitMax], TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)               
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +Y ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda x: x.YForce[y]), forceActuatorYLimitTable[y][forceActuatorLimitMax], TEST_TOLERANCE)
                InTolerance("FA%03d +Y ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), 0.0, TEST_TOLERANCE)
                
                # Set the commanded Y force
                yForces[y] = forceActuatorYLimitTable[y][forceActuatorLimitMin] * TEST_PERCENTAGE

                # Apply the Y only offset force
                m1m3.ApplyOffsetForces(xForces, yForces, zForces)

                # Set the simulatored force actuator's load cells to the correct value
                primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, yForces[y], 0, 0)
                sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
                
                # Verify the rejected forces match the commanded values
                result, data = m1m3.GetEventRejectedForces()
                InTolerance("FA%03d +Y RejectedForces.YForces[%d]" % (id, y), data.YForces[y], yForces[y], TEST_TOLERANCE)
                InTolerance("FA%03d +Y RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)
                
                # Verify the applied mirror forces match the expected value
                result, data = m1m3.GetEventAppliedForces()
                InTolerance("FA%03d +Y AppliedForces.YForces[%d]" % (id, y), data.YForces[y], forceActuatorYLimitTable[y][forceActuatorLimitMin], TEST_TOLERANCE)
                InTolerance("FA%03d +Y AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], 0.0, TEST_TOLERANCE)               
                
                # Wait a bit before checking all of the force actuator forces (positive and negative testing)
                time.sleep(TEST_SETTLE_TIME)
                
                # Check force actuator force
                datas = self.SampleForceActuators(m1m3)
                InTolerance("FA%03d +Y ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda x: x.YForce[y]), forceActuatorYLimitTable[y][forceActuatorLimitMin], TEST_TOLERANCE)
                InTolerance("FA%03d +Y ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), 0.0, TEST_TOLERANCE)
                
                # Clear force setpoint for this actuator
                yForces[y] = 0
                
                # Clear offset forces
                m1m3.ClearOffsetForces()
                
                # Wait a bit before continuing
                time.sleep(TEST_SETTLE_TIME)
            
            # Set the commanded Z force
            zForces[z] = forceActuatorZLimitTable[z][forceActuatorLimitMax] * TEST_PERCENTAGE

            # Apply the Z only offset force
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)

            # Set the simulatored force actuator's load cells to the correct value
            primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, 0, zForces[z])
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            
            # Verify the rejected forces match the commanded values
            result, data = m1m3.GetEventRejectedForces()
            if x != -1:
                InTolerance("FA%03d +Z RejectedForces.XForces[%d]" % (id, y), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z RejectedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], zForces[z], TEST_TOLERANCE)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            if x != -1:
                InTolerance("FA%03d +Z AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], forceActuatorZLimitTable[z][forceActuatorLimitMax], TEST_TOLERANCE)               
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d +Z ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda x: x.XForce[x]), 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d +Z ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda x: x.YForce[y]), 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d +Z ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), forceActuatorZLimitTable[z][forceActuatorLimitMax], TEST_TOLERANCE)
            
            # Set the commanded Z force
            zForces[z] = forceActuatorZLimitTable[z][forceActuatorLimitMin] * TEST_PERCENTAGE

            # Apply the Z only offset force
            m1m3.ApplyOffsetForces(xForces, yForces, zForces)

            # Set the simulatored force actuator's load cells to the correct value
            primaryCylinderForce, secondaryCylinderForce = ActuatorToCylinderSpace(orientation, 0, 0, zForces[z])
            sim.setFAForceAndStatus(id, 0, primaryCylinderForce, secondaryCylinderForce)
            
            # Verify the rejected forces match the commanded values
            result, data = m1m3.GetEventRejectedForces()
            if x != -1:
                InTolerance("FA%03d -Z RejectedForces.XForces[%d]" % (id, y), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z RejectedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z RejectedForces.ZForces[%d]" % (id, z), data.ZForces[z], zForces[z], TEST_TOLERANCE)
            
            # Verify the applied mirror forces match the expected value
            result, data = m1m3.GetEventAppliedForces()
            if x != -1:
                InTolerance("FA%03d -Z AppliedForces.XForces[%d]" % (id, x), data.XForces[x], 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z AppliedForces.YForces[%d]" % (id, y), data.YForces[y], 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z AppliedForces.ZForces[%d]" % (id, z), data.ZForces[z], forceActuatorZLimitTable[z][forceActuatorLimitMin], TEST_TOLERANCE)               
            
            # Wait a bit before checking all of the force actuator forces (positive and negative testing)
            time.sleep(TEST_SETTLE_TIME)
            
            # Check force actuator force
            datas = self.SampleForceActuators(m1m3)
            if x != -1:
                InTolerance("FA%03d -Z ForceActuatorData.XForce[%d]" % (id, x), Average(datas, lambda x: x.XForce[x]), 0.0, TEST_TOLERANCE)
            if y != -1:
                InTolerance("FA%03d -Z ForceActuatorData.YForce[%d]" % (id, y), Average(datas, lambda x: x.YForce[y]), 0.0, TEST_TOLERANCE)
            InTolerance("FA%03d -Z ForceActuatorData.ZForce[%d]" % (id, z), Average(datas, lambda x: x.ZForce[z]), forceActuatorZLimitTable[z][forceActuatorLimitMin], TEST_TOLERANCE)
            
            # Clear force setpoint for this actuator
            zForces[z] = 0
            
            # Clear offset forces
            m1m3.ClearOffsetForces()
            
            # Wait a bit before continuing
            time.sleep(TEST_SETTLE_TIME)
            
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
    M13T002().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)