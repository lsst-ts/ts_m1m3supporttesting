import time
import binascii
import struct
from SALPY_MTM1M3 import *
from Utilities import *

COMMAND_TIME = 0.5
COMMAND_TIMEOUT = 10

class M1M3:
    def __init__(self):
        Log("M1M3: Initializing SAL")
        self.sal = SAL_MTM1M3()
        self.sal.setDebugLevel(0)
        self.sal.salCommand("MTM1M3_command_abortRaiseM1M3")
        self.sal.salCommand("MTM1M3_command_applyAberrationForces")
        self.sal.salCommand("MTM1M3_command_applyAberrationForcesByBendingModes")
        self.sal.salCommand("MTM1M3_command_applyActiveOpticForces")
        self.sal.salCommand("MTM1M3_command_applyActiveOpticForcesByBendingModes")
        self.sal.salCommand("MTM1M3_command_applyOffsetForces")
        self.sal.salCommand("MTM1M3_command_applyOffsetForcesByMirrorForce")
        self.sal.salCommand("MTM1M3_command_clearAberrationForces")
        self.sal.salCommand("MTM1M3_command_clearActiveOpticForces")
        self.sal.salCommand("MTM1M3_command_clearOffsetForces")
        self.sal.salCommand("MTM1M3_command_disable")
        self.sal.salCommand("MTM1M3_command_disableHardpointCorrections")
        self.sal.salCommand("MTM1M3_command_enable")
        self.sal.salCommand("MTM1M3_command_enableHardpointCorrections")
        self.sal.salCommand("MTM1M3_command_enterEngineering")
        self.sal.salCommand("MTM1M3_command_exitEngineering")
        self.sal.salCommand("MTM1M3_command_lowerM1M3")
        self.sal.salCommand("MTM1M3_command_moveHardpointActuators")
        self.sal.salCommand("MTM1M3_command_positionM1M3")
        self.sal.salCommand("MTM1M3_command_raiseM1M3")
        self.sal.salCommand("MTM1M3_command_shutdown")
        self.sal.salCommand("MTM1M3_command_standby")
        self.sal.salCommand("MTM1M3_command_start")
        self.sal.salCommand("MTM1M3_command_stopHardpointMotion")
        self.sal.salCommand("MTM1M3_command_modbusTransmit")
        self.sal.salCommand("MTM1M3_command_translateM1M3")
        self.sal.salEvent("MTM1M3_logevent_appliedAberrationForces")
        self.sal.salEvent("MTM1M3_logevent_appliedAccelerationForces")
        self.sal.salEvent("MTM1M3_logevent_appliedActiveOpticForces")
        self.sal.salEvent("MTM1M3_logevent_appliedAzimuthForces")
        self.sal.salEvent("MTM1M3_logevent_appliedBalanceForces")
        self.sal.salEvent("MTM1M3_logevent_appliedCylinderForces")
        self.sal.salEvent("MTM1M3_logevent_appliedElevationForces")
        self.sal.salEvent("MTM1M3_logevent_appliedForces")
        self.sal.salEvent("MTM1M3_logevent_appliedOffsetForces")
        self.sal.salEvent("MTM1M3_logevent_appliedSettingsMatchStart")
        self.sal.salEvent("MTM1M3_logevent_appliedStaticForces")
        self.sal.salEvent("MTM1M3_logevent_appliedThermalForces")
        self.sal.salEvent("MTM1M3_logevent_appliedVelocityForces")
        self.sal.salEvent("MTM1M3_logevent_commandRejectionWarning")
        self.sal.salEvent("MTM1M3_logevent_detailedState")
        self.sal.salEvent("MTM1M3_logevent_forceActuatorState")
        self.sal.salEvent("MTM1M3_logevent_forceActuatorInfo")
        self.sal.salEvent("MTM1M3_logevent_forceSetpointWarning")
        self.sal.salEvent("MTM1M3_logevent_hardpointActuatorInfo")
        self.sal.salEvent("MTM1M3_logevent_hardpointActuatorState")
        self.sal.salEvent("MTM1M3_logevent_hardpointActuatorWarning")
        self.sal.salEvent("MTM1M3_logevent_hardpointMonitorInfo")
        self.sal.salEvent("MTM1M3_logevent_modbusResponse")
        self.sal.salEvent("MTM1M3_logevent_rejectedAberrationForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedAccelerationForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedActiveOpticForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedAzimuthForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedBalanceForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedCylinderForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedElevationForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedOffsetForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedSettingsMatchStart")
        self.sal.salEvent("MTM1M3_logevent_rejectedStaticForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedThermalForces")
        self.sal.salEvent("MTM1M3_logevent_rejectedVelocityForces")
        self.sal.salEvent("MTM1M3_logevent_summaryState")
        self.sal.salTelemetrySub("MTM1M3_accelerometerData")
        self.sal.salTelemetrySub("MTM1M3_forceActuatorData")
        self.sal.salTelemetrySub("MTM1M3_hardpointActuatorData")
        self.sal.salTelemetrySub("MTM1M3_hardpointMonitorData")
        self.sal.salTelemetrySub("MTM1M3_imsData")
        self.sal.salTelemetrySub("MTM1M3_inclinometerData")
        
    def Close(self):
        Log("M1M3: Shutting down SAL")
        time.sleep(1)
        self.sal.salShutdown();

    def Time(self):
            return self.sal.getCurrentTime()
        
    def Flush(self, item):
        result, data = item()
        while result >= 0:
            result, data = item()           

    def AbortRaiseM1M3(self, run = True):
        Log("M1M3: AbortRaiseM1M3(%s)" % (run))
        data = MTM1M3_command_abortRaiseM1M3C()
        data.abortRaiseM1M3 = run
        cmdId = self.sal.issueCommand_abortRaiseM1M3(data)
        self.sal.waitForCompletion_abortRaiseM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyAberrationForces(self, zForces):
        Log("M1M3: ApplyAberrationForces([%s])" % (','.join(map(str, zForces))))
        data = MTM1M3_command_applyAberrationForcesC()
        for i in range(156):
            data.zForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_applyAberrationForces(data)
        self.sal.waitForCompletion_applyAberrationForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyAberrationForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyAberrationForcesByBendingModes([%s])" % (','.join(map(str, coefficients))))
        data = MTM1M3_command_applyAberrationForcesByBendingModesC()
        for i in range(22):
            data.coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_applyAberrationForcesByBendingModes(data)
        self.sal.waitForCompletion_applyAberrationForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyActiveOpticForces(self, zForces):
        Log("M1M3: ApplyActiveOpticForces([%s])" % (','.join(map(str, zForces))))
        data = MTM1M3_command_applyActiveOpticForcesC()
        for i in range(156):
            data.zForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_applyActiveOpticForces(data)
        self.sal.waitForCompletion_applyActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyActiveOpticForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyActiveOpticForcesByBendingModes([%s])" % (','.join(map(str, coefficients))))
        data = MTM1M3_command_applyActiveOpticForcesByBendingModesC()
        for i in range(22):
            data.coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_applyActiveOpticForcesByBendingModes(data)
        self.sal.waitForCompletion_applyActiveOpticForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyOffsetForces(self, xForces, yForces, zForces, waitForCompletion = True):
        Log("M1M3: ApplyOffsetForces([%s], [%s], [%s])" % (','.join(map(str, xForces)), ','.join(map(str, yForces)), ','.join(map(str, zForces))))
        data = MTM1M3_command_applyOffsetForcesC()
        for i in range(12):
            data.xForces[i] = xForces[i]
        for i in range(100):
            data.yForces[i] = yForces[i]
        for i in range(156):
            data.zForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_applyOffsetForces(data)
        if waitForCompletion:
            self.sal.waitForCompletion_applyOffsetForces(cmdId, COMMAND_TIMEOUT)
            time.sleep(COMMAND_TIME)
        
    def ApplyOffsetForcesByMirrorForce(self, fx, fy, fz, mx, my, mz, waitForCompletion = True):
        Log("M1M3: ApplyOffsetForcesByMirrorForce(%s, %s, %s, %s, %s, %s)" % (fx, fy, fz, mx, my, mz))
        data = MTM1M3_command_applyOffsetForcesByMirrorForceC()
        data.xForce = fx
        data.yForce = fy
        data.zForce = fz
        data.xMoment = mx
        data.yMoment = my
        data.zMoment = mz
        cmdId = self.sal.issueCommand_applyOffsetForcesByMirrorForce(data)
        if waitForCompletion:
            self.sal.waitForCompletion_applyOffsetForcesByMirrorForce(cmdId, COMMAND_TIMEOUT)
            time.sleep(COMMAND_TIME)
        
    def ClearAberrationForces(self, run = True):
        Log("M1M3: ClearAberrationForces(%s)" % (run))
        data = MTM1M3_command_clearAberrationForcesC()
        data.clearAberrationForces = run
        cmdId = self.sal.issueCommand_clearAberrationForces(data)
        self.sal.waitForCompletion_clearAberrationForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ClearActiveOpticForces(self, run = True):
        Log("M1M3: ClearActiveOpticForces(%s)" % (run))
        data = MTM1M3_command_clearActiveOpticForcesC()
        data.clearActiveOpticForces = run
        cmdId = self.sal.issueCommand_clearActiveOpticForces(data)
        self.sal.waitForCompletion_clearActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ClearOffsetForces(self, run = True):
        Log("M1M3: ClearOffsetForces(%s)" % (run))
        data = MTM1M3_command_clearOffsetForcesC()
        data.clearOffsetForces = run
        cmdId = self.sal.issueCommand_clearOffsetForces(data)
        self.sal.waitForCompletion_clearOffsetForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Disable(self, run = True):
        Log("M1M3: Disable(%s)" % (run))
        data = MTM1M3_command_disableC()
        data.value = run
        cmdId = self.sal.issueCommand_disable(data)
        self.sal.waitForCompletion_disable(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def DisableHardpointCorrections(self, run = True):
        Log("M1M3: DisableHardpointCorrections(%s)" % (run))
        data = MTM1M3_command_disableHardpointCorrectionsC()
        data.disableHardpointCorrections = run
        cmdId = self.sal.issueCommand_disableHardpointCorrections(data)
        self.sal.waitForCompletion_disableHardpointCorrections(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Enable(self, run = True):
        Log("M1M3: Enable(%s)" % (run))
        data = MTM1M3_command_enableC()
        data.value = run
        cmdId = self.sal.issueCommand_enable(data)
        self.sal.waitForCompletion_enable(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def EnableHardpointCorrections(self, run = True):
        Log("M1M3: EnableHardpointCorrections(%s)" % (run))
        data = MTM1M3_command_enableHardpointCorrectionsC()
        data.enableHardpointCorrections = run
        cmdId = self.sal.issueCommand_enableHardpointCorrections(data)
        self.sal.waitForCompletion_enableHardpointCorrections(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def EnterEngineering(self, run = True):
        Log("M1M3: EnterEngineering(%s)" % (run))
        data = MTM1M3_command_enterEngineeringC()
        data.enterEngineering = run
        cmdId = self.sal.issueCommand_enterEngineering(data)
        self.sal.waitForCompletion_enterEngineering(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ExitEngineering(self, run = True):
        Log("M1M3: ExitEngineering(%s)" % (run))
        data = MTM1M3_command_exitEngineeringC()
        data.exitEngineering = run
        cmdId = self.sal.issueCommand_exitEngineering(data)
        self.sal.waitForCompletion_exitEngineering(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def LowerM1M3(self, run = True):
        Log("M1M3: LowerM1M3(%s)" % (run))
        data = MTM1M3_command_LowerM1M3C()
        data.lowerM1M3 = run
        cmdId = self.sal.issueCommand_lowerM1M3(data)
        self.sal.waitForCompletion_lowerM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def MoveHardpointActuators(self, steps):
        Log("M1M3: MoveHardpointActuators(%s)" % (','.join(map(str, steps))))
        data = MTM1M3_command_moveHardpointActuatorsC()
        for i in range(6):
            data.steps[i] = steps[i]
        cmdId = self.sal.issueCommand_moveHardpointActuators(data)
        self.sal.waitForCompletion_moveHardpointActuators(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def PositionM1M3(self, xPosition = 0.0, yPosition = 0.0, zPosition = 0.0,
                     xRotation = 0.0, yRotation = 0.0, zRotation = 0.0):
        Log("M1M3: PositionM1M3(%s, %s, %s, %s, %s, %s)" % (xPosition, yPosition, zPosition, xRotation, yRotation,zRotation))
        data = MTM1M3_command_positionM1M3C()
        data.xPosition = xPosition
        data.yPosition = yPosition
        data.zPosition = zPosition
        data.xRotation = xRotation
        data.yRotation = yRotation
        data.zRotation = zRotation
        cmdId = self.sal.issueCommand_positionM1M3(data)
        self.sal.waitForCompletion_positionM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def RaiseM1M3(self, bypassReferencePosition, run = True):
        Log("M1M3: RaiseM1M3(%s, %s)" % (run, bypassReferencePosition))
        data = MTM1M3_command_raiseM1M3C()
        data.raiseM1M3 = run
        data.bypassReferencePosition = bypassReferencePosition
        cmdId = self.sal.issueCommand_raiseM1M3(data)
        self.sal.waitForCompletion_raiseM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Shutdown(self, run = True):
        Log("M1M3: Shutdown(%s)" % (run))
        data = MTM1M3_command_shutdownC()
        data.shutdown = run
        cmdId = self.sal.issueCommand_shutdown(data)
        self.sal.waitForCompletion_shutdown(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
    
    def Standby(self, run = True):
        Log("M1M3: Standby(%s)" % (run))
        data = MTM1M3_command_standbyC()
        data.value = run
        cmdId = self.sal.issueCommand_standby(data)
        self.sal.waitForCompletion_standby(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Start(self, settingsToApply, run = True):
        Log("M1M3: Start(%s, %s)" % (run, settingsToApply))
        data = MTM1M3_command_startC()
        data.settingsToApply = settingsToApply
        cmdId = self.sal.issueCommand_start(data)
        self.sal.waitForCompletion_start(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def StopHardpointMotion(self, run = True):
        Log("M1M3: StopHardpointMotion(%s)" % (run))
        data = MTM1M3_command_stopHardpointMotionC()
        data.stopHardpointMotion = run
        cmdId = self.sal.issueCommand_stopHardpointMotion(data)
        self.sal.waitForCompletion_stopHardpointMotion(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def TranslateM1M3(self, xTranslation = 0.0, yTranslation = 0.0, zTranslation = 0.0, xRotation = 0.0, yRotation = 0.0, zRotation = 0.0):
        Log("M1M3: TranslateM1M3(%s, %s, %s, %s, %s, %s)" % (xTranslation, yTranslation, zTranslation, xRotation, yRotation,zRotation))
        data = MTM1M3_command_translateM1M3C()
        data.xTranslation = xTranslation
        data.yTranslation = yTranslation
        data.zTranslation = zTranslation
        data.xRotation = xRotation
        data.yRotation = yRotation
        data.zRotation = zRotation
        cmdId = self.sal.issueCommand_translateM1M3(data)
        self.sal.waitForCompletion_translateM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ModbusTransmit(self, actuatorId, functionCode, rawData):
        Log("M1M3: ModbusTransmit(%d, %d, %d)" % (actuatorId, functionCode, len(rawData)))
        data = MTM1M3_command_modbusTransmitC()
        data.actuatorId = actuatorId
        data.functionCode = functionCode
        for i in range(len(rawData)):
            data.data[i] = rawData[i]
        data.dataLength = len(rawData)
        cmdId = self.sal.issueCommand_modbusTransmit(data)
        self.sal.waitForCompletion_modbusTransmit(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Modbus_SetADCOffsetSensitivity(self, actuatorId, channel, offset, sensitivity):
        Log("M1M3: Modbus SetADCOffsetSensitivity(%d, %d, %f, %f)" % (actuatorId, channel, offset, sensitivity))
        offsetBytes = self._floatToBytes(offset, "offset", 4)
        sensitivityBytes = self._floatToBytes(sensitivity, "sensitivity", 4)
        data = []
        data.append(bytes([channel]))
        data.append(offsetBytes[0])
        data.append(offsetBytes[1])
        data.append(offsetBytes[2])
        data.append(offsetBytes[3])
        data.append(sensitivityBytes[0])
        data.append(sensitivityBytes[1])
        data.append(sensitivityBytes[2])
        data.append(sensitivityBytes[3])
        self.ModbusTransmit(actuatorId, 81, data)
        self.PrintModbusResponse()
        
    def PrintModbusResponse(self):
        rtn, data = self.GetEventModbusResponse()
        if rtn == 0:
            Log("Modbus Response")
            Log("     Valid:         %s" % data.ResponseValid)
            Log("     Address:       %d" % data.Address)
            Log("     Function Code: %d" % data.FunctionCode)
            Log("     Data:          %s" % data.Data)
            Log("     CRC:           %d" % data.CRC)
   
    # This function is used to get the most recently published event
    # action: () -> result:int, data:<SAL_DATA>
    def GetEvent(self, action):
        lastResult, lastData = action()
        while lastResult >= 0:
            result, data = action()
            if result >= 0:
                lastResult = result
                lastData = data
            elif result < 0:
                break
        return lastResult, lastData
        
    # This function is used to search the queued events for data matching the predicate
    # action: () -> result:int, data:<SAL_DATA>
    # predicate: data:<SAL_DATA> -> boolean
    def SearchEvent(self, action, predicate):
        while True:
            result, data = action()
            if result >= 0 and predicate(data):
                return result, data
            elif result < 0:
                return result, data

    def GetNextEventAppliedAberrationForces(self):
        data = MTM1M3_logevent_appliedAberrationForcesC()
        result = self.sal.getEvent_appliedAberrationForces(data)
        return result, data
        
    def GetEventAppliedAberrationForces(self):
        return self.GetEvent(self.GetNextEventAppliedAberrationForces)
        
    def SearchEventAppliedAberrationForces(self, predicate):
        return self.SearchEvent(self.GetNextEventAppliedAberrationForces, predicate)

    def GetNextEventAppliedAccelerationForces(self):
        data = MTM1M3_logevent_appliedAccelerationForcesC()
        result = self.sal.getEvent_appliedAccelerationForces(data)
        return result, data
        
    def GetEventAppliedAccelerationForces(self):
        return self.GetEvent(self.GetNextEventAppliedAccelerationForces)

    def GetNextEventAppliedActiveOpticForces(self):
        data = MTM1M3_logevent_appliedActiveOpticForcesC()
        result = self.sal.getEvent_appliedActiveOpticForces(data)
        return result, data
        
    def GetEventAppliedActiveOpticForces(self):
        return self.GetEvent(self.GetNextEventAppliedActiveOpticForces)
    
    def GetNextEventAppliedAzimuthForces(self):
        data = MTM1M3_logevent_appliedAzimuthForcesC()
        result = self.sal.getEvent_appliedAzimuthForces(data)
        return result, data

    def GetEventAppliedAzimuthForces(self):
        return self.GetEvent(self.GetNextEventAppliedAzimuthForces)
    
    def GetNextEventAppliedBalanceForces(self):
        data = MTM1M3_logevent_appliedBalanceForcesC()
        result = self.sal.getEvent_appliedBalanceForces(data)
        return result, data
        
    def GetEventAppliedBalanceForces(self):
        return self.GetEvent(self.GetNextEventAppliedBalanceForces)
    
    def GetNextEventAppliedCylinderForces(self):
        data = MTM1M3_logevent_appliedCylinderForcesC()
        result = self.sal.getEvent_appliedCylinderForces(data)
        return result, data
        
    def GetEventAppliedCylinderForces(self):
        return self.GetEvent(self.GetNextEventAppliedCylinderForces)
    
    def GetNextEventAppliedElevationForces(self):
        data = MTM1M3_logevent_appliedElevationForcesC()
        result = self.sal.getEvent_appliedElevationForces(data)
        return result, data
        
    def GetEventAppliedElevationForces(self):
        return self.GetEvent(self.GetNextEventAppliedElevationForces)
    
    def GetNextEventAppliedForces(self):
        data = MTM1M3_logevent_appliedForcesC()
        result = self.sal.getEvent_appliedForces(data)
        return result, data
        
    def GetEventAppliedForces(self):
        return self.GetEvent(self.GetNextEventAppliedForces)
        
    def GetNextEventAppliedOffsetForces(self):
        data = MTM1M3_logevent_appliedOffsetForcesC()
        result = self.sal.getEvent_appliedOffsetForces(data)
        return result, data
        
    def GetEventAppliedOffsetForces(self):
        return self.GetEvent(self.GetNextEventAppliedOffsetForces)
    
    def GetNextEventAppliedStaticForces(self):
        data = MTM1M3_logevent_appliedStaticForcesC()
        result = self.sal.getEvent_appliedStaticForces(data)
        return result, data
        
    def GetEventAppliedStaticForces(self):
        return self.GetEvent(self.GetNextEventAppliedStaticForces)
    
    def GetNextEventAppliedThermalForces(self):
        data = MTM1M3_logevent_appliedThermalForcesC()
        result = self.sal.getEvent_appliedThermalForces(data)
        return result, data
        
    def GetEventAppliedThermalForces(self):
        return self.GetEvent(self.GetNextEventAppliedThermalForces)
    
    def GetNextEventAppliedVelocityForces(self):
        data = MTM1M3_logevent_appliedVelocityForcesC()
        result = self.sal.getEvent_appliedVelocityForces(data)
        return result, data
        
    def GetEventAppliedVelocityForces(self):
        return self.GetEvent(self.GetNextEventAppliedVelocityForces)
            
    def GetNextEventCommandRejectionWarning(self):
        data = MTM1M3_logevent_commandRejectionWarningC()
        result = self.sal.getEvent_commandRejectionWarning(data)
        return result, data
        
    def GetEventCommandRejectionWarning(self):
        return self.GetEvent(self.GetNextEventCommandRejectionWarning)
       
    def GetNextEventDetailedState(self):
        data = MTM1M3_logevent_detailedStateC()
        result = self.sal.getEvent_detailedState(data)
        return result, data
        
    def GetEventDetailedState(self):
        return self.GetEvent(self.GetNextEventDetailedState)
        
    def GetNextEventForceActuatorState(self):
        data = MTM1M3_logevent_forceActuatorStateC()
        result = self.sal.getEvent_forceActuatorState(data)
        return result, data
        
    def GetEventForceActuatorState(self):
        return self.GetEvent(self.GetNextEventForceActuatorState)
        
    def GetNextEventForceActuatorInfo(self):
        data = MTM1M3_logevent_forceActuatorInfoC()
        result = self.sal.getEvent_forceActuatorInfo(data)
        return result, data
        
    def GetEventForceActuatorInfo(self):
        return self.GetEvent(self.GetNextEventForceActuatorInfo)

    def GetNextEventForceSetpointWarning(self):
        data = MTM1M3_logevent_forceSetpointWarningC()
        result = self.sal.getEvent_forceSetpointWarning(data)
        return result, data

    def GetEventForceSetpointWarning(self):
        return self.GetEvent(self.GetNextEventForceSetpointWarning)
        
    def GetNextEventHardpointActuatorInfo(self):
        data = MTM1M3_logevent_hardpointActuatorInfoC()
        result = self.sal.getEvent_hardpointActuatorInfo(data)
        return result, data
        
    def GetEventHardpointActuatorInfo(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorInfo)
    
    def GetNextEventHardpointActuatorState(self):
        data = MTM1M3_logevent_hardpointActuatorStateC()
        result = self.sal.getEvent_hardpointActuatorState(data)
        return result, data
        
    def GetEventHardpointActuatorState(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorState)
    
    def GetNextEventHardpointActuatorWarning(self):
        data = MTM1M3_logevent_hardpointActuatorWarningC()
        result = self.sal.getEvent_hardpointActuatorWarning(data)
        return result, data
        
    def GetEventHardpointActuatorWarning(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorWarning)
        
    def GetNextEventHardpointMonitorInfo(self):
        data = MTM1M3_logevent_hardpointMonitorInfoC()
        result = self.sal.getEvent_hardpointMonitorInfo(data)
        return result, data
        
    def GetEventHardpointMonitorInfo(self):
        return self.GetEvent(self.GetNextEventHardpointMonitorInfo)
        
    def GetNextEventModbusResponse(self):
        data = MTM1M3_logevent_modbusResponseC()
        result = self.sal.getEvent_modbusResponseC(data)
        return result, data
        
    def GetEventModbusResponse(self):
        return self.GetEvent(self.GetNextEventModbusResponse)
        
    def GetNextEventRejectedAberrationForces(self):
        data = MTM1M3_logevent_rejectedAberrationForcesC()
        result = self.sal.getEvent_rejectedAberrationForces(data)
        return result, data
        
    def GetEventRejectedAberrationForces(self):
        return self.GetEvent(self.GetNextEventRejectedAberrationForces)

    def GetNextEventRejectedAccelerationForces(self):
        data = MTM1M3_logevent_rejectedAccelerationForcesC()
        result = self.sal.getEvent_rejectedAccelerationForces(data)
        return result, data
        
    def GetEventRejectedAccelerationForces(self):
        return self.GetEvent(self.GetNextEventRejectedAccelerationForces)

    def GetNextEventRejectedActiveOpticForces(self):
        data = MTM1M3_logevent_rejectedActiveOpticForcesC()
        result = self.sal.getEvent_rejectedActiveOpticForces(data)
        return result, data
        
    def GetEventRejectedActiveOpticForces(self):
        return self.GetEvent(self.GetNextEventRejectedActiveOpticForces)
    
    def GetNextEventRejectedAzimuthForces(self):
        data = MTM1M3_logevent_rejectedAzimuthForcesC()
        result = self.sal.getEvent_rejectedAzimuthForces(data)
        return result, data
        
    def GetEventRejectedAzimuthForces(self):
        return self.GetEvent(self.GetNextEventRejectedAzimuthForces)
    
    def GetNextEventRejectedBalanceForces(self):
        data = MTM1M3_logevent_rejectedBalanceForcesC()
        result = self.sal.getEvent_rejectedBalanceForces(data)
        return result, data
        
    def GetEventRejectedBalanceForces(self):
        return self.GetEvent(self.GetNextEventRejectedBalanceForces)
    
    def GetNextEventRejectedCylinderForces(self):
        data = MTM1M3_logevent_rejectedCylinderForcesC()
        result = self.sal.getEvent_rejectedCylinderForces(data)
        return result, data
        
    def GetEventRejectedCylinderForces(self):
        return self.GetEvent(self.GetNextEventRejectedCylinderForces)
    
    def GetNextEventRejectedElevationForces(self):
        data = MTM1M3_logevent_rejectedElevationForcesC()
        result = self.sal.getEvent_rejectedElevationForces(data)
        return result, data
        
    def GetEventRejectedElevationForces(self):
        return self.GetEvent(self.GetNextEventRejectedElevationForces)
    
    def GetNextEventRejectedForces(self):
        data = MTM1M3_logevent_rejectedForcesC()
        result = self.sal.getEvent_rejectedForces(data)
        return result, data
        
    def GetEventRejectedForces(self):
        return self.GetEvent(self.GetNextEventRejectedForces)
    
    def GetNextEventRejectedOffsetForces(self):
        data = MTM1M3_logevent_rejectedOffsetForcesC()
        result = self.sal.getEvent_rejectedOffsetForces(data)
        return result, data
        
    def GetEventRejectedOffsetForces(self):
        return self.GetEvent(self.GetNextEventRejectedOffsetForces)
    
    def GetNextEventRejectedStaticForces(self):
        data = MTM1M3_logevent_rejectedStaticForcesC()
        result = self.sal.getEvent_rejectedStaticForces(data)
        return result, data
        
    def GetEventRejectedStaticForces(self):
        return self.GetEvent(self.GetNextEventRejectedStaticForces)
    
    def GetNextEventRejectedThermalForces(self):
        data = MTM1M3_logevent_rejectedThermalForcesC()
        result = self.sal.getEvent_rejectedThermalForces(data)
        return result, data
        
    def GetEventRejectedThermalForces(self):
        return self.GetEvent(self.GetNextEventRejectedThermalForces)
    
    def GetNextEventRejectedVelocityForces(self):
        data = MTM1M3_logevent_rejectedVelocityForcesC()
        result = self.sal.getEvent_rejectedVelocityForces(data)
        return result, data
        
    def GetEventRejectedVelocityForces(self):
        return self.GetEvent(self.GetNextEventRejectedVelocityForces)
        
    def GetNextEventSummaryState(self):
        data = MTM1M3_logevent_summaryStateC()
        result = self.sal.getEvent_summaryState(data)
        return result, data
        
    def GetEventSummaryState(self):
        return self.GetEvent(self.GetNextEventSummaryState)
        
    def GetSampleAccelerometerData(self):
        data = MTM1M3_accelerometerDataC()
        result = self.sal.getSample_accelerometerData(data)
        return result, data
        
    def GetSampleForceActuatorData(self):
        data = MTM1M3_forceActuatorDataC()
        result = self.sal.getSample_forceActuatorData(data)
        return result, data

    def GetNextSampleForceActuatorData(self):
        data = MTM1M3_forceActuatorDataC()
        result = self.sal.getNextSample_forceActuatorData(data)
        return result, data
        
    def GetSampleHardpointActuatorData(self):
        data = MTM1M3_hardpointActuatorDataC()
        result = self.sal.getSample_hardpointActuatorData(data)
        return result, data
    
    def GetNextSampleHardpointActuatorData(self):
        data = MTM1M3_hardpointActuatorDataC()
        result = self.sal.getNextSample_hardpointActuatorData(data)
        return result, data

    def GetSampleHardpointMonitorData(self):
        data = MTM1M3_hardpointMonitorDataC()
        result = self.sal.getSample_hardpointMonitorData(data)
        return result, data
    
    def GetNextSampleHardpointMonitorData(self):
        data = MTM1M3_hardpointMonitorDataC()
        result = self.sal.getNextSample_hardpointMonitorData(data)
        return result, data
        
    def GetSampleIMSData(self):
        data = MTM1M3_imsDataC()
        result = self.sal.getSample_imsData(data)
        return result, data

    def GetNextSampleIMSData(self):
        data = MTM1M3_imsDataC()
        result = self.sal.getNextSample_imsData(data)
        return result, data
                
    def GetSampleInclinometerData(self):
        data = MTM1M3_inclinometerDataC()
        result = self.sal.getSample_inclinometerData(data)
        return result, data
        
    def _floatToBytes(self, someData:float, parameterName:str, byteSize:int):
        floatBytes = struct.pack(">f", someData)
        if (len(floatBytes) != byteSize):
            raise Exception(parameterName + " size does not match the byte size("
                            + str(byteSize) + ") specified.")
        return floatBytes
        
        
