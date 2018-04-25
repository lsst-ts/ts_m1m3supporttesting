import M1M3
import CellSimulator
import EFD
import VerifyAccelerometer
import VerifyInclinometer
import VerifyDisplacement
import VerifyEFD
import VerifyStateChanges
import VerifyTiming
import VerifyForceActuators
import VerifyHardpointActuators
import VerifyStart
import M13F003
import M13T002
import M13T003
import M13T004
from HardpointActuatorTable import *
from HardpointMonitorTable import *
from ForceActuatorTable import *
import time

m1m3 = M1M3.M1M3()
sim = CellSimulator.CellSimulator("140.252.32.153", True)
efd = EFD.EFD()

sim.setInclinometer(45.0)
sim.setDisplacement(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
sim.setAccelerometerVoltage(1.0, -1.0, 2.0, -2.0, 3.0, -3.0, 4.0, -4.0)
sim.setAngularVelocity(12.34, 56.78, 91.01, 7, 20)
    
for row in hardpointActuatorTable:
    id = row[hardpointActuatorTableIDIndex]
    sim.setILCID(id, id, 1, 1, 0, 0, 8, 2, "Mock-HP")
    sim.setILCStatus(id, 0, 0, 0)
    sim.setILCMode(id, 0)
    sim.setHPForceAndStatus(id, 0, 0, 0.0)
    sim.setADCSampleRate(id, 8)
    #sim.setCalibrationData(id, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
   
for row in hardpointMonitorTable:
    id = row[hardpointMonitorTableIDIndex]
    sim.setILCID(id, id, 7, 7, 0, 0, 8, 2, "Mock-HM")
    sim.setILCStatus(id, 0, 0, 0)
    sim.setILCMode(id, 0)
    sim.setMezzanineID(id, id + 1000, 52, 0x3832)
    sim.setMezzanineStatus(id, 0)
    sim.setPressure(id, 0.0, 0.0, 0.0, 0.0)
    sim.setLVDT(id, 0.0, 0.0)
    
for row in forceActuatorTable:
    id = row[forceActuatorTableIDIndex]
    type = row[forceActuatorTableTypeIndex]
    if type == 'SAA':
        sim.setILCID(id, id, 2, 2, 0, 0, 8, 2, "Mock-FA")
    else:
        sim.setILCID(id, id, 2, 2, 2, 2, 8, 2, "Mock-FA")
    sim.setILCStatus(id, 0, 0, 0)
    sim.setILCMode(id, 0)
    sim.setBoostValveGains(id, 1.0, 1.0)
    sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
    sim.setADCSampleRate(id, 8)
    #sim.setCalibrationData(id, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    sim.setMezzanineID(id, id + 1000, 52, 0x0802)
    sim.setMezzanineStatus(id, 0)
    sim.setPressure(id, 0.0, 0.0, 0.0, 0.0)

#VerifyEFD.VerifyEFD().Run(m1m3, sim)
#VerifyStateChanges.VerifyStateChanges().Run(m1m3, sim)
#VerifyAccelerometer.VerifyAccelerometer().Run(m1m3, sim)
#VerifyInclinometer.VerifyInclinometer().Run(m1m3, sim)
#VerifyDisplacement.VerifyDisplacement().Run(m1m3, sim)
#VerifyForceActuators.VerifyForceActuators().Run(m1m3, sim)
#VerifyHardpointActuators.VerifyHardpointActuators().Run(m1m3, sim)
#M13F003.M13F003().Run(m1m3, sim)
#M13T002.M13T002().Run(m1m3, sim)
#M13T003.M13T003().Run(m1m3, sim)
M13T004.M13T004().Run(m1m3, sim, efd)
#VerifyTiming.VerifyTiming().Run(m1m3, sim)
#VerifyStart.VerifyStart().Run(m1m3, sim)