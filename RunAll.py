#import M1M3
import CellSimulator
import VerifyStateChanges
#import VerifyEFD
from HardpointActuatorTable import *
from HardpointMonitorTable import *
from ForceActuatorTable import *

m1m3 = M1M3.M1M3()
sim = CellSimulator.CellSimulator("140.252.32.153", True)

sim.setInclinometer(45.0)
sim.setDisplacement(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
sim.setAccelerometerVoltage(1.0, -1.0, 2.0, -2.0, 3.0, -3.0, 4.0, -4.0)
sim.setAngularVelocity(12.34, 56.78, 91.01, True, 20)
    
for row in hardpointActuatorTable:
    id = row[hardpointActuatorTableIDIndex]
    sim.setILCID(id, id, 1, 1, 0, 0, 8, 0, "Mock-HP")
    sim.setILCStatus(id, 48, 0, 0)
    sim.setILCMode(id, 0)
    sim.setHPForceAndStatus(id, 0, (id + 1000), (id + 0.5))
    #sim.setADCSampleRate(id, 8)
    #sim.setCalibrationData(id, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
   
for row in hardpointMonitorTable:
    id = row[hardpointMonitorTableIDIndex]
    sim.setILCID(id, id, 7, 7, 0, 0, 8, 0, "Mock-HM")
    sim.setILCStatus(id, 48, 0, 0)
    sim.setILCMode(id, 0)
    #sim.setMezzanineID(id, id + 1000, 52, 52)
    sim.setMezzanineStatus(id, 0)
    sim.setPressure(id, 0.0, 0.0, 0.0, 0.0)
    sim.setLVDT(id, 0.0, 0.0)
    
for row in forceActuatorTable:
    id = row[forceActuatorTableIDIndex]
    type = row[forceActuatorTableTypeIndex]
    if type == 'SAA':
        sim.setILCID(id, id, 2, 2, 0, 0, 8, 0, "Mock-FA")
    else:
        sim.setILCID(id, id, 2, 2, 2, 2, 8, 0, "Mock-FA")
    sim.setILCStatus(id, 48, 0, 0)
    sim.setILCMode(id, 0)
    sim.setBoostValveGains(id, 1.0, 1.0)
    sim.setFAForceAndStatus(id, 0, 0.0, 0.0)
    #sim.setADCSampleRate(id, 8)
    #sim.setCalibrationData(id, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    #sim.setMezzanineID(id, id + 1000, 52, 52)
    sim.setMezzanineStatus(id, 0)
    sim.setPressure(id, 0.0, 0.0, 0.0, 0.0)

VerifyStateChanges.VerifyStateChanges().Run(m1m3, sim)
#VerifyEFD.VerifyEFD().Run(m1m3, sim)
