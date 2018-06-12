import M1M3
import CellSimulator
import EFD
from HardpointActuatorTable import *
from HardpointMonitorTable import *
from ForceActuatorTable import *
import time

simulatorIP = "140.252.32.153"
runSimulator = False

def Setup():
    m1m3 = M1M3.M1M3()
    sim = CellSimulator.CellSimulator(simulatorIP, runSimulator)
    efd = EFD.EFD()

    sim.setInclinometer(0.0)
    sim.setDisplacement(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    sim.setAccelerometerVoltage(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    sim.setAngularVelocity(0.0, 0.0, 0.0, 7, 20)
        
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
    
    return m1m3, sim, efd
    
def Shutdown(m1m3, sim, efd):
    m1m3.Close()
    efd.Close()
    return 0