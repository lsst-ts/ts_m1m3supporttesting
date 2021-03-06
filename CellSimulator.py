import ILCSimulator
import InclinometerSimulator
import DisplaceSimulator
import AccelSimulator
import DigitalInputSimulator
import DigitalOutputSimulator
import time
import UDP    
import socket
from Utilities import Log
    
class CellSimulator:
    AccelerometerVoltsToMetersPerSecondSqrd = 4.9035
    AccelerometerXDistance = 1.0
    AccelerometerYDistance = 1.0
    AccelerometerZDistance = 1.0
  
    def __init__(self, ipAddress, dbg = False):
        self.Print = dbg
        self._ilcSim = ILCSimulator.ILCSimulator()
        self._inclinSim = InclinometerSimulator.InclinometerSimulator()
        self._displaceSim = DisplaceSimulator.DisplacementSimulator()
        self._accelSim = AccelSimulator.AccelSimulator()
        self._diSim = DigitalInputSimulator.DigitalInputSimulator()
        self._doSim = DigitalOutputSimulator.DigitalOutputSimulator()

        self._udpClientSubnetA = UDP.UDP(ipAddress, 5006)
        self._udpClientSubnetB = UDP.UDP(ipAddress, 5007)
        self._udpClientSubnetC = UDP.UDP(ipAddress, 5008)
        self._udpClientSubnetD = UDP.UDP(ipAddress, 5009)
        self._udpClientSubnetE = UDP.UDP(ipAddress, 5005)
        self._udpClientInclin = UDP.UDP(ipAddress, 5010)
        self._udpClientDisplace = UDP.UDP(ipAddress, 5011)
        self._udpClientAccel = UDP.UDP(ipAddress, 5012)
        self._udpClientDI = UDP.UDP(ipAddress, 5013)
        self._udpClientDO = UDP.UDP(ipAddress, 5014)
        self._udpResponse = UDP.UDP(socket.gethostbyname(socket.gethostname()), 4999, True)
        
    def setDisplacement(self, d1:float, d2:float, d3:float, d4:float, d5:float, d6:float, d7:float, d8:float):
        if self.Print:
            Log("CellSimulator: Setting IMS displacements to (%0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f)" % (d1, d2, d3, d4, d5, d6, d7, d8))
        self._udpClientDisplace.send(self._displaceSim.displacementResponse(d1, d2, d3, d4, d5, d6, d7, d8))
        
    def setInclinometer(self, angle:float):
        if self.Print:
            Log("CellSimulator: Setting inclinometer angle to %0.3f" % (angle))
        self._udpClientInclin.send(self._inclinSim.inclinometerResponse(angle))
                
    def setAccelerometerVoltage(self, a1:float, a2:float, a3:float, a4:float, a5:float, a6:float, a7:float, a8:float):
        if self.Print:
            Log("CellSimulator: Setting accelerometer voltages to (%0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f)" % (a1, a2, a3, a4, a5, a6, a7, a8))
        self._udpClientAccel.send(self._accelSim.accelerometerResponse(accelerometerNumber = 1, elevationVoltage = a1, azimuthVoltage = a2))
        self._udpClientAccel.send(self._accelSim.accelerometerResponse(accelerometerNumber = 2, elevationVoltage = a3, azimuthVoltage = a4))
        self._udpClientAccel.send(self._accelSim.accelerometerResponse(accelerometerNumber = 3, elevationVoltage = a5, azimuthVoltage = a6))
        self._udpClientAccel.send(self._accelSim.accelerometerResponse(accelerometerNumber = 4, elevationVoltage = a7, azimuthVoltage = a8))
        
    def setAccelerometer(self, a1:float, a2:float, a3:float, a4:float, a5:float, a6:float, a7:float, a8:float):
        if self.Print:
            Log("CellSimulator: Setting accelerometer acceleration to (%0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f, %0.3f)" % (a1, a2, a3, a4, a5, a6, a7, a8))
        a1 = a1 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a2 = a2 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a3 = a3 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a4 = a4 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a5 = a5 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a6 = a6 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a7 = a7 / self.AccelerometerVoltsToMetersPerSecondSqrd
        a8 = a8 / self.AccelerometerVoltsToMetersPerSecondSqrd
        self.setAccelerometerVoltage(a1, a2, a3, a4, a5, a6, a7, a8)
        
    def setAngularAcceleration(self, ax:float, ay:float, az:float):
        if self.Print:
            Log("CellSimulator: Setting accelerometer angular acceleration to (%0.3f, %0.3f, %0.3f)" % (ax, ay, az))
        a8 = (ax / 2.0) * self.AccelerometerXDistance
        a6 = (-ax / 2.0) * self.AccelerometerXDistance
        a3 = (ay / 2.0) * self.AccelerometerYDistance
        a1 = (-ay / 2.0) * self.AccelerometerYDistance
        a5 = -az * self.AccelerometerZDistance
        a7 = -az * self.AccelerometerZDistance
        a2 = 0.0
        a4 = 0.0
        self.setAccelerometer(a1, a2, a3, a4, a5, a6, a7, a8)
        
    def setAngularVelocity(self, vx:float, vy:float, vz:float):
        if self.Print:
            Log("CellSimulator: Setting gyro angular velocity to (%0.3f, %0.3f, %0.3f)" % (vx, vy, vz))
            
        
    def setAUXPowerNetworksOff(self, off):
        if self.Print:
            Log("CellSimulator: Setting AUX power network off to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.powerNetworkShutDown(boolToInt(not on)))
        
    def setThermalEquipmentOff(self, off):
        if self.Print:
            Log("CellSimulator: Setting thermal equipment off to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.fansHeatersPumpPoweredOff(boolToInt(not on)))
    
    def setAirSupplyOff(self, off):
        if self.Print:
            Log("CellSimulator: Setting air supply off to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.airSupplyClosedAirReliefOpen(boolToInt(not on)))
    
    def setCabinetDoorOpen(self, open):
        if self.Print:
            Log("CellSimulator: Setting cabinet door open to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.gisEarthquakeSignal(boolToInt(not on)))
    
    def setTMAMotionStop(self, stop):
        if self.Print:
            Log("CellSimulator: Setting TMA motion stop to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.tmaMotionStop(boolToInt(not on)))
    
    def setGISHeartbeatLost(self, lost):
        if self.Print:
            Log("CellSimulator: Setting GIS heartbeat lost to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.gisHeartbeatLost(boolToInt(not on)))
        
    def setAirSupplyValveOpen(self, open):
        if self.Print:
            Log("CellSimulator: Setting air supply valve open to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.airSupplyValveStatusOpen(boolToInt(not on)))
    
    def setAirSupplyValveClosed(self, closed):
        if self.Print:
            Log("CellSimulator: Setting air supply valve closed to (%d)" % (boolToInt(on)))
        self._udpClientDI.send(self._diSim.airSupplyValveStatusClosed(boolToInt(not on)))
        
    def getHeartbeatToSafetyController(self):
        if self.Print:
            Log("CellSimulator: Getting heartbeat to safety controller")
        self._udpClientDO.send(self._doSim.requestHeartBeatSafetyController())
        return self.getDO()
        
    def getAirSupplyValve(self):
        if self.Print:
            Log("CellSimulator: Getting air supply valve")
        self._udpClientDO.send(self._doSim.requestAirSupplyControlValve())
        return self.getDO()
    
    def getCellLights(self):
        if self.Print:
            Log("CellSimulator: Getting cell lights")
        self._udpClientDO.send(self._doSim.requestMirrorCellLightsRemoteControl())
        return self.getDO()
        
    def getAUXPowerNetworkAOn(self):
        if self.Print:
            Log("CellSimulator: Getting AUX power network A on")
        self._udpClientDO.send(self._doSim.requestAuxPowerNetworkAOn())
        return self.getDO()
        
    def getAUXPowerNetworkBOn(self):
        if self.Print:
            Log("CellSimulator: Getting AUX power network B on")
        self._udpClientDO.send(self._doSim.requestAuxPowerNetworkBOn())
        return self.getDO()
        
    def getAUXPowerNetworkCOn(self):
        if self.Print:
            Log("CellSimulator: Getting AUX power network C on")
        self._udpClientDO.send(self._doSim.requestAuxPowerNetworkCOn())
        return self.getDO()
        
    def getAUXPowerNetworkDOn(self):
        if self.Print:
            Log("CellSimulator: Getting AUX power network D on")
        self._udpClientDO.send(self._doSim.requestAuxPowerNetworkDOn())
        return self.getDO()
    
    def getPowerNetworkAOn(self):
        if self.Print:
            Log("CellSimulator: Getting power network A on")
        self._udpClientDO.send(self._doSim.requestPowerNetworkAOn())
        return self.getDO()
        
    def getPowerNetworkBOn(self):
        if self.Print:
            Log("CellSimulator: Getting power network B on")
        self._udpClientDO.send(self._doSim.requestPowerNetworkBOn())
        return self.getDO()
        
    def getPowerNetworkCOn(self):
        if self.Print:
            Log("CellSimulator: Getting power network C on")
        self._udpClientDO.send(self._doSim.requestPowerNetworkCOn())
        return self.getDO()
        
    def getPowerNetworkDOn(self):
        if self.Print:
            Log("CellSimulator: Getting power network D on")
        self._udpClientDO.send(self._doSim.requestPowerNetworkDOn())
        return self.getDO()

    def setILCID(self, id:int, uniqueId:int, ilcAppType:int, networkNodeType:int, ilcSelectedOptions:int, networkNodeOptions:int, majorRev:int, minorRev:int, firmwareName:str):
        if self.Print:
            Log("CellSimulator: Setting ILC ID for %d to (%d, %d, %d, %d, %d, %d, %d, %s)" % (id, uniqueId, ilcAppType, networkNodeType, ilcSelectedOptions, networkNodeOptions, majorRev, minorRev, firmwareName))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.reportServerId(address, uniqueId, ilcAppType, networkNodeType, ilcSelectedOptions, networkNodeOptions, majorRev, minorRev, firmwareName))
        
    def setILCStatus(self, id:int, mode:int, status:int, faults:int):
        if self.Print:
            Log("CellSimulator: Setting ILC status for %d to (%d, %d, %d)" % (id, mode, status, faults))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.reportServerStatus(address, mode, status, faults))
        
    def setILCMode(self, id:int, ilcMode:int):
        if self.Print:
            Log("CellSimulator: Setting ILC mode for %d to (%d)" % (id, ilcMode))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.ilcMode(address, ilcMode))
        
    def setHPForceAndStatus(self, id:int, statusByte:int, ssiEncoderValue:int, loadCellForce:float):
        if self.Print:
            Log("CellSimulator: Setting HP force and status for %d to (%d, %d, %0.3f)" % (id, statusBy, ssiEncoderValue, loadCellForce))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.forceAndStatusRequest(address, statusByte, ssiEncoderValue, float(loadCellForce)))

    def setBoostValveGains(self, id:int, primaryCylinderGain:float, secondaryCylinderGain:float):
        if self.Print:
            Log("CellSimulator: Setting boost valve gains for %d to (%0.3f, %0.3f)" % (id, primaryCylinderGain, secondaryCylinderGain))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.readBoostValueDcaGains(address, float(primaryCylinderGain), float(secondaryCylinderGain)))
        
    def setFAForceAndStatus(self, id:int, statusByte:int, primaryCylinderForce:float, secondaryCylinderForce:float = 0):
        if self.Print:
            Log("CellSimulator: Setting FA force and status for %d to (%d, %0.3f, %0.3f)" % (id, statusByte, primaryCylinderForce, secondaryCylinderForce))
        subnet, address = getSubnetAndAddress(id)
        if address <= 16:
            subnet.send(self._ilcSim.singlePneumaticAxisForce(statusByte, address, float(primaryCylinderForce)))
            subnet.send(self._ilcSim.singlePneumaticForceAndStatus(statusByte, address, float(primaryCylinderForce)))
        else:
            subnet.send(self._ilcSim.dualPneumaticAxisForce(address, statusByte, float(primaryCylinderForce), float(secondaryCylinderForce)))
            subnet.send(self._ilcSim.singlePneumaticForceAndStatus(address, statusByte, float(primaryCylinderForce), float(secondaryCylinderForce)))
            
    def setADCSampleRate(self, id:int, scanRateCode:int):
        if self.Print:
            Log("CellSimulator: Setting ADC sample rate for %d to (%d)" % (id, scanRateCode))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.setAdcSampleRate(address, scanRateCode))
        
    def setCalibrationData(self, id:int, mainAdcCalibration1:float, mainAdcCalibration2:float, mainAdcCalibration3:float, mainAdcCalibration4:float, mainSensorOffset1:float, mainSensorOffset2:float, mainSensorOffset3:float, mainSensorOffset4:float, mainSensorSensitivity1:float, mainSensorSensitivity2:float, mainSensorSensitivity3:float, mainSensorSensitivity4:float, backupAdcCalibration1:float, backupAdcCalibration2:float, backupAdcCalibration3:float, backupAdcCalibration4:float, backupSensorOffset1:float, backupSensorOffset2:float, backupSensorOffset3:float, backupSensorOffset4:float, backupSensorSensitivity1:float, backupSensorSensitivity2:float, backupSensorSensitivity3:float, backupSensorSensitivity4:float):
        if self.Print:
            Log("CellSimulator: Setting calibration data for %d to ()" % (id))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.readCalibrationData(address, mainAdcCalibration1, mainAdcCalibration2, mainAdcCalibration3, mainAdcCalibration4, mainSensorOffset1, mainSensorOffset2, mainSensorOffset3, mainSensorOffset4, mainSensorSensitivity1, mainSensorSensitivity2, mainSensorSensitivity3, mainSensorSensitivity4, backupAdcCalibration1, backupAdcCalibration2, backupAdcCalibration3, backupAdcCalibration4, backupSensorOffset1, backupSensorOffset2, backupSensorOffset3, backupSensorOffset4, backupSensorSensitivity1, backupSensorSensitivity2, backupSensorSensitivity3, backupSensorSensitivity4))
        
    def setPressure(self, id:int, p1:float, p2:float, p3:float, p4:float):
        if self.Print:
            Log("CellSimulator: Setting pressure for %d to (%0.3f, %0.3f, %0.3f, %0.3f)" % (id, p1, p2, p3, p4))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.readDcaPressureValues(address, p1, p2, p3, p4))
        
    def setMezzanineID(self, id:int, uniqueId:int, firmwareType:int, firmwareVersion:int):
        if self.Print:
            Log("CellSimulator: Setting mezzanine ID for %d to (%d, %d, %d)" % (id, uniqueId, firmwareType, firmwareVersion))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.reportDcaId(address, uniqueId, firmwareType, firmwareVersion))
        
    def setMezzanineStatus(self, id:int, status:int):
        if self.Print:
            Log("CellSimulator: Setting mezzanine status for %d to (%d)" % (id, status))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.reportDcaStatus(address, status))
        
    def setLVDT(self, id:int, lvdt1:float, lvdt2:float):
        if self.Print:
            Log("CellSimulator: Setting LVDT for %d to (%0.3f, %0.3f)" % (id, lvdt1, lvdt2))
        subnet, address = getSubnetAndAddress(id)
        subnet.send(self._ilcSim.readLVDT(address, lvdt1, lvdt2))
                
    def getSubnetAndAddress(self, id:int):
        for row in hardpointActuatorTable:
            if row[hardpointActuatorTableIDIndex] == id:
                return getSubnet(row[hardpointActuatorTableSubnetIndex]), row[hardpointActuatorTableAddressIndex]
        for row in hardpointMonitorTable:
            if row[hardpointMonitorTableIDIndex] == id:
                return getSubnet(row[hardpointMonitorTableSubnetIndex]), row[hardpointMonitorTableAddressIndex]
        for row in forceActuatorTable:
            if row[forceActuatorTableIDIndex] == id:
                return getSubnet(row[forceActuatorTableSubnetIndex]), row[forceActuatorTableAddressIndex]
        
    def getSubnet(self, subnet:int):
        if subnet == 1:
            return self._udpClientSubnetA
        elif subnet == 2:
            return self._udpClientSubnetB
        elif subnet == 3:
            return self._udpClientSubnetC
        elif subnet == 4:
            return self._udpClientSubnetD
        elif subnet == 5:
            return self._udpClientSubnetE
        return 0
        
    def boolToInt(self, b):
        if b:
            return 1
        return 0
        
    def getDO(self):
        message = self._udpResponse.get()
        return not (message[1] == ord("0"))
        
        