########################################################################
# Test Numbers: M13T-010  NOT READY
# Author:       AClements
# Description:  Position System Requirements
# Steps:
# - Issue start command
# - Raise Mirror in Active Mode
# - Confirm Mirror in Reference Position
# - Follow the motion matrix below, where X, Y & Z are 1.0 mm and ΘX, ΘY, & ΘZ are 0.014 degrees:
#   +X, 0, 0 
#   -X, 0, 0
#   0,+Y, 0
#   0, -Y, 0
#   0, 0, +Z
#   0, 0, -Z
#   +X, 0, +Z
#   +X, 0, -Z
#   - X, 0, +Z
#   - X, 0, -Z
#   0, +Y, +Z
#   0, +Y, -Z
#   0, -Y, +Z
#   0, -Y, -Z
#   +ΘX, 0, 0
#   - ΘX, 0, 0
#   0, +ΘY, 0
#   0, -ΘY, 0
#   0, 0, +ΘZ
#   0, 0, -ΘZ
#   +ΘX,+ΘY, 0
#   -ΘX,+ΘY, 0
#   +ΘX,-ΘY, 0
#   -ΘX,-ΘY, 0
# - Repeat Matrix 2 more times
# - Transition back to standby
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb

#TODO: add defined reference positions here when they are defined.
referenceXPosition = 0.0
referenceYPosition = 0.0
referenceZPosition = 0.0
referenceXRotation = 0.0
referenceYRotation = 0.0
referenceZRotation = 0.0

travelDistance = 0.001
travelRotation = 0.014

class M13T010:
# This test has some TODOs that need to be completed before it can be run.  Hence the short circuit.
    def Run(self, m1m3, sim, efd):
        Header("M13T-010: Position System Requirements")
        Log("M13T-010 is not ready for test, TODOs need to be completed.")
        return
        
        ########################################
        # Enable the mirror, Raise it.

        # Bring mirror into Disabled state.
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Place mirror into Enabled state.
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_EnabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Raise mirror.
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ActiveState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        ##########################################################
        # Check that mirror is in nominal/reference/0,0,0 position

        # Not sure of the best way how to check when it is settled into reference position...
        # currently checking each direction, one at a time.
        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.XPosition", data.XPosition, referenceXPosition)
        WaitUntil("XPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition)

        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.YPosition", data.YPosition, referenceYPosition)
        WaitUntil("YPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition)

        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.ZPosition", data.ZPosition, referenceZPosition)
        WaitUntil("ZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition)

        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.XRotation", data.XRotation, referenceXRotation)
        WaitUntil("XRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation)

        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.YRotation", data.YRotation, referenceYRotation)
        WaitUntil("YRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation)

        result, data = m1m3.GetSampleHardpointActuatorData()
        Equal("SAL m1m3_HardpointActuatorData.ZRotation", data.ZRotation, referenceZRotation)
        WaitUntil("ZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation)

        ##########################################################
        # Command the mirror to the matrix positions.  Check to make sure it reaches those positions.

        # The martix need to be tested 3 times
        for i in range(0,3):
            #########################
            # (X, 0, 0) to (-X, 0, 0) 
            m1m3.PositionM1M3(referenceXPosition + travelPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(X, 0, 0)", data.XPosition, referenceXPosition + travelPosition)
            WaitUntil("XPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition + travelPosition)
            
            m1m3.PositionM1M3(referenceXPosition - travelPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, 0)", data.XPosition, referenceXPosition - travelPosition)
            WaitUntil("XPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition - travelPosition)
            
            #########################
            # (0, Y, 0) to (0, Y, 0)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition + travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, Y, 0)", data.YPosition, referenceYPosition + travelPosition)
            WaitUntil("YPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition + travelPosition)
            
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition - travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, 0)", data.YPosition, referenceYPosition - travelPosition)
            WaitUntil("YPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition - travelPosition)
            
            #########################
            # (0, 0, Z) to (0, 0, Z)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, Z)", data.ZPosition, referenceZPosition + travelPosition)
            WaitUntil("ZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition + travelPosition)
            
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, 0, -Z)", data.ZPosition, referenceZPosition - travelPosition)
            WaitUntil("ZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition - travelPosition)
                    
            #########################
            # (X, Y, 0) to (-X, -Y, 0) 
            m1m3.PositionM1M3(referenceXPosition + travelPosition, referenceYPosition + travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(X, Y, 0)", data.XPosition, referenceXPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.YPosition(X, Y, 0)", data.YPosition, referenceYPosition + travelPosition)
            WaitUntil("XYPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition + travelPosition, referenceYPosition - travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(X, -Y, 0)", data.XPosition, referenceXPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.YPosition(X, -Y, 0)", data.YPosition, referenceYPosition - travelPosition)
            WaitUntil("XYPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition - travelPosition)
            m1m3.PositionM1M3(referenceXPosition - travelPosition, referenceYPosition + travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(-X, Y, 0)", data.XPosition, referenceXPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.YPosition(-X, Y, 0)", data.YPosition, referenceYPosition + travelPosition)
            WaitUntil("XYPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition - travelPosition, referenceYPosition - travelPosition, referenceZPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(-X, -Y, 0)", data.XPosition, referenceXPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.YPosition(-X, -Y, 0)", data.YPosition, referenceYPosition - travelPosition)
            WaitUntil("XYPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition - travelPosition)
            
            #########################
            # (X, 0, Z) to (-X, 0, -Z) 
            m1m3.PositionM1M3(referenceXPosition + travelPosition, referenceYPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(X, 0, Z)", data.XPosition, referenceXPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, Z)", data.ZPosition, referenceZPosition + travelPosition)
            WaitUntil("XZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition + travelPosition, referenceYPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(X, 0, -Z)", data.XPosition, referenceXPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(X, 0, -Z)", data.ZPosition, referenceZPosition - travelPosition)
            WaitUntil("XZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition - travelPosition)
            m1m3.PositionM1M3(referenceXPosition - travelPosition, referenceYPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, Z)", data.XPosition, referenceXPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, Z)", data.ZPosition, referenceZPosition + travelPosition)
            WaitUntil("XZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition - travelPosition, referenceYPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XPosition(-X, 0, -Z)", data.XPosition, referenceXPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(-X, 0, -Z)", data.ZPosition, referenceZPosition - travelPosition)
            WaitUntil("XZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XPosition == referenceXPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition - travelPosition)
            
            #########################
            # (0, Y, Z) to (0, -Y, -Z) 
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition + travelPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, Y, Z)", data.YPosition, referenceYPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, Z)", data.ZPosition, referenceZPosition + travelPosition)
            WaitUntil("YZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition + travelPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, Y, -Z)", data.YPosition, referenceYPosition + travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, Y, -Z)", data.ZPosition, referenceZPosition - travelPosition)
            WaitUntil("YZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition + travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition - travelPosition)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition - travelPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, Z)", data.YPosition, referenceYPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, Z)", data.ZPosition, referenceZPosition + travelPosition)
            WaitUntil("YZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition + travelPosition)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition - travelPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YPosition(0, -Y, -Z)", data.YPosition, referenceYPosition - travelPosition)
            Equal("SAL m1m3_HardpointActuatorData.ZPosition(0, -Y, -Z)", data.ZPosition, referenceZPosition - travelPosition)
            WaitUntil("YZPosition", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YPosition == referenceYPosition - travelPosition and m1m3.GetSampleHardpointActuatorData()[1].ZPosition == referenceZPosition - travelPosition)
            
            #########################
            # (ΘX, 0, 0) to (-ΘX, 0, 0) 
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation + travelRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, 0)", data.XRotation, referenceXRotation + travelRotation)
            WaitUntil("XRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation - travelRotation, referenceYRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, 0)", data.XRotation, referenceXRotation - travelRotation)
            WaitUntil("XRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation - travelRotation)
            
            #########################
            # (0, ΘY, 0) to (0, ΘY, 0)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition + travelPosition, referenceZPosition, referenceXRotation, referenceYRotation + travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, 0)", data.YRotation, referenceYRotation + travelRotation)
            WaitUntil("YRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition - travelPosition, referenceZPosition, referenceXRotation, referenceYRotation - travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, 0)", data.YRotation, referenceYRotation - travelRotation)
            WaitUntil("YRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation - travelRotation)
            
            #########################
            # (0, 0, ΘZ) to (0, 0, ΘZ)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition + travelPosition, referenceXRotation, referenceYRotation, referenceZRotation + travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, 0, ΘZ)", data.ZRotation, referenceZRotation + travelRotation)
            WaitUntil("ZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition - travelPosition, referenceXRotation, referenceYRotation, referenceZRotation - travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, 0, -ΘZ)", data.ZRotation, referenceZRotation - travelRotation)
            WaitUntil("ZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation - travelRotation)
            
            #########################
            # (ΘX, ΘY, 0) to (-ΘX, -ΘY, 0) 
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation + travelRotation, referenceYRotation + travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(ΘX, ΘY, 0)", data.XRotation, referenceXRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.YRotation(ΘX, ΘY, 0)", data.YRotation, referenceYRotation + travelRotation)
            WaitUntil("XYRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation + travelRotation, referenceYRotation - travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(ΘX, -ΘY, 0)", data.XRotation, referenceXRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.YRotation(ΘX, -ΘY, 0)", data.YRotation, referenceYRotation - travelRotation)
            WaitUntil("XYRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation - travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation - travelRotation, referenceYRotation + travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, ΘY, 0)", data.XRotation, referenceXRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.YRotation(-ΘX, ΘY, 0)", data.YRotation, referenceYRotation + travelRotation)
            WaitUntil("XYRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation - travelRotation, referenceYRotation - travelRotation, referenceZRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, -ΘY, 0)", data.XRotation, referenceXRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.YRotation(-ΘX, -ΘY, 0)", data.YRotation, referenceYRotation - travelRotation)
            WaitUntil("XYRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceYRotation - travelRotation)
            
            #########################
            # (ΘX, 0, ΘZ) to (-ΘX, 0, -ΘZ) 
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation + travelRotation, referenceYRotation, referenceZRotation + travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, ΘZ)", data.XRotation, referenceXRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(ΘX, 0, ΘZ)", data.ZRotation, referenceZRotation + travelRotation)
            WaitUntil("XZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation + travelRotation, referenceYRotation, referenceZRotation - travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(ΘX, 0, -ΘZ)", data.XRotation, referenceXRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(ΘX, 0, -ΘZ)", data.ZRotation, referenceZRotation - travelRotation)
            WaitUntil("XZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation - travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation - travelRotation, referenceYRotation, referenceZRotation + travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, ΘZ)", data.XRotation, referenceXRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(-ΘX, 0, ΘZ)", data.ZRotation, referenceZRotation + travelRotation)
            WaitUntil("XZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation - travelRotation, referenceYRotation, referenceZRotation - travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.XRotation(-ΘX, 0, -ΘZ)", data.XRotation, referenceXRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(-ΘX, 0, -ΘZ)", data.ZRotation, referenceZRotation - travelRotation)
            WaitUntil("XZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].XRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation - travelRotation)
            
            #########################
            # (0, ΘY, ΘZ) to (0, -ΘY, -ΘZ) 
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation + travelRotation, referenceZRotation + travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, ΘZ)", data.YRotation, referenceYRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, ΘY, ΘZ)", data.ZRotation, referenceZRotation + travelRotation)
            WaitUntil("YZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation + travelRotation, referenceZRotation - travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, ΘY, -ΘZ)", data.YRotation, referenceYRotation + travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, ΘY, -ΘZ)", data.ZRotation, referenceZRotation - travelRotation)
            WaitUntil("YZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceXRotation + travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation - travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation - travelRotation, referenceZRotation + travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, ΘZ)", data.YRotation, referenceYRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, -ΘY, ΘZ)", data.ZRotation, referenceZRotation + travelRotation)
            WaitUntil("YZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation + travelRotation)
            m1m3.PositionM1M3(referenceXPosition, referenceYPosition, referenceZPosition, referenceXRotation, referenceYRotation - travelRotation, referenceZRotation - travelRotation)
            result, data = m1m3.GetSampleHardpointActuatorData()
            Equal("SAL m1m3_HardpointActuatorData.YRotation(0, -ΘY, -ΘZ)", data.YRotation, referenceYRotation - travelRotation)
            Equal("SAL m1m3_HardpointActuatorData.ZRotation(0, -ΘY, -ΘZ)", data.ZRotation, referenceZRotation - travelRotation)
            WaitUntil("YZRotation", 300, lambda: m1m3.GetSampleHardpointActuatorData()[1].YRotation == referenceXRotation - travelRotation and m1m3.GetSampleHardpointActuatorData()[1].ZRotation == referenceZRotation - travelRotation)
            

        #######################
        # Lower the mirror, put back in standby state.

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_EnabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        
        # Bring mirror into Disabled state.
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        eventTimestamp = data.Timestamp
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        
        # Get back into StandbyState
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL m1m3_logevent_DetailedState.DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)   
        result, data = m1m3.GetEventSummaryState()
        Equal("SAL m1m3_logevent_SummaryState.SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13T010().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
