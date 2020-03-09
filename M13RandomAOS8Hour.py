########################################################################
# Test Numbers: M13RandomAOS8Hour
# Author:       AClements
# Description:  Suppose to mimic a night of viewing as much as we can at CAID
# Steps:
# - Raise Mirror in Active Mode
# - Confirm Mirror in Reference Position
# - Disable Hardpoint Corrections
# - wait 5 seconds
# - Enable Hardpoint Corrections
# - Apply a Randomly selected (1 through 9) Active Optic Force by Bending mode
# - Wait 30 seconds
# - Clear Active Optic Forces by Bending Mode
# - repeat sequence for 8 hours
# - Lower mirror
########################################################################

from Utilities import *
from SALPY_m1m3 import *
from Setup import *
import MySQLdb
import time
import random

# edit the defined reference positions as needed.
REFERENCE_X_POSITION = 0.0
REFERENCE_Y_POSITION = 0.0
REFERENCE_Z_POSITION = 0.0
REFERENCE_X_ROTATION = 0.0
REFERENCE_Y_ROTATION = 0.0
REFERENCE_Z_ROTATION = 0.0

POSITION_TOLERANCE = 0.000008
ROTATION_TOLERANCE = 0.00000209
WAIT_UNTIL_TIMEOUT = 120
RUN_TIME = 28800 # number of seconds in 8 hours

class M13RandomAOS8Hour:

    def Run(self, m1m3, sim, efd):
        Header("M13RandomAOS8Hour: Position System Requirements")
        
        # Raise mirror (therefore entering the Raised Engineering State).
        m1m3.RaiseM1M3(False)
        result, data = m1m3.GetEventDetailedState()
        Equal("SAL MTM1M3_logevent_DetailedState.DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until active engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ActiveEngineeringState)
        
        time.sleep(5.0)
        
        result, data = m1m3.GetSampleHardpointActuatorData()
        InTolerance("SAL MTM1M3_HardpointActuatorData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_HardpointActuatorData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)
        
        result, data = m1m3.GetSampleIMSData()
        InTolerance("SAL MTM1M3_IMSData.XPosition", data.XPosition, REFERENCE_X_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.YPosition", data.YPosition, REFERENCE_Y_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.ZPosition", data.ZPosition, REFERENCE_Z_POSITION, POSITION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.XRotation", data.XRotation, REFERENCE_X_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.YRotation", data.YRotation, REFERENCE_Y_ROTATION, ROTATION_TOLERANCE)
        InTolerance("SAL MTM1M3_IMSData.ZRotation", data.ZRotation, REFERENCE_Z_ROTATION, ROTATION_TOLERANCE)

        displacementResults = []
        faResults = []

        startTime = time.time()
        counter = 0
        
        while(True):
            counter = counter + 1
            Log("Starting to run loop # %d" % counter)
            loopStartTime = time.time()
            # Disable Hardpoint Corrections
            m1m3.DisableHardpointCorrections(True)

            time.sleep(5.0)

            # Enable Hardpoint Corrections
            m1m3.EnableHardpointCorrections(True)
            
            # Select a random bending mode, change it to 1.0
            bendingModes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            randomMode = random.randint(1, 10)
            bendingModes[randomMode] = 1.0

            # Apply Bending Mode, sleep for 30 seconds
            m1m3.ApplyActiveOpticForcesByBendingModes(bendingModes)
            time.sleep(15.0)
            result, hpData = m1m3.GetSampleHardpointActuatorData()
            result, imsData = m1m3.GetSampleIMSData()
            result, faData = m1m3.GetSampleForceActuatorData()
            time.sleep(15.0)

            m1m3.ClearActiveOpticForces(True)
            
            displacementResults.append([counter, hpData.XPosition, hpData.YPosition, hpData.ZPosition, hpData.XRotation, hpData.YRotation, hpData.ZRotation, imsData.XPosition, imsData.YPosition, imsData.ZPosition, imsData.XRotation, imsData.YRotation, imsData.ZRotation])
            faResults.append([counter, faData.PrimaryCylinderForce, faData.SecondaryCylinderForce, faData.XForce, faData.YForce, faData.ZForce, faData.Fx, faData.Fy, faData.Fz, faData.Mx, faData.My, faData.Mz, faData.ForceMagnitude])

            if (startTime + RUN_TIME < time.time()):
                Log("Test complete.  Ending script")
                break
            else:
                Log("Loop complete. Running Time: %f" % (time.time() - loopStartTime))

        path = GetFilePath("M13RandomAOS8Hour-Positions.csv")
        Log("File path: %s" % path)
        f = open(path, "w+")
        f.write("LoopCounter,HP-XPosition,HP-YPosition,HP-ZPosition,HP-XRotation,HP-YRotation,HP-ZRotation,IMS-XPosition,IMS-YPosition,IMS-ZPosition,IMS-XRotation,IMS-YRotation,IMS-ZRotation\r\n")
        for r in displacementResults:
            f.write("%s,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f\r\n" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]))
        f.close()

        path = GetFilePath("M13RandomAOS8Hour-ForceActuators.csv")
        Log("File path: %s" % path)
        f = open(path, "w+")
        f.write("LoopCounter,")
        for i in range(156):
            f.write("PrimaryCylinderForce %d," % i)
        for i in range(112):
            f.write("SecondaryCylinderForce %d," % i)
        for i in range(12):
            f.write("XForce %d," % i)
        for i in range(100):
            f.write("YForce %d," % i)
        for i in range(156):
            f.write("ZForce %d," % i)
        f.write("Fx,Fy,Fz,Mx,My,Mz,ForceMagnitude\r\n")
        for r in faResults:
            f.write("%s," % (r[0]))
            for i in range(156):
                f.write("%0.9f," % (r[1][i]))
            for i in range(112):
                f.write("%0.9f," % (r[2][i]))
            for i in range(12):
                f.write("%0.9f," % (r[3][i]))
            for i in range(100):
                f.write("%0.9f," % (r[4][i]))
            for i in range(156):
                f.write("%0.9f," % (r[5][i]))
            f.write("%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f,%0.9f\r\n" % (r[6], r[7], r[8], r[9], r[10], r[11], r[12]))
        f.close()

        #######################
        # Lower the mirror

        # Lower mirror.
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.detailedState, MTM1M3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.summaryState, MTM1M3_shared_SummaryStates_EnabledState)
        
        # Wait until parked engineering state
        WaitUntil("DetailedState", WAIT_UNTIL_TIMEOUT, lambda: m1m3.GetEventDetailedState()[1].DetailedState == MTM1M3_shared_DetailedStates_ParkedEngineeringState)
        
    def checkMotionStateEquals(self, eval):
        rtn, data = m1m3.GetNextEventHardpointActuatorState()
        if rtn >= 0:
            return eval(sum(data.MotionState))
        return False
        
        
if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    M13RandomAOS8Hour().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
