import time
import binascii
import struct
from SALPY_m1m3 import *
from Utilities import *

COMMAND_TIME = 0.5
COMMAND_TIMEOUT = 10

class M1M3:
    def __init__(self):
        Log("M1M3: Initializing SAL")
        self.sal = SAL_m1m3()
        self.sal.setDebugLevel(0)
        self.sal.salCommand("m1m3_command_AbortRaiseM1M3")
        self.sal.salCommand("m1m3_command_ApplyAberrationForces")
        self.sal.salCommand("m1m3_command_ApplyAberrationForcesByBendingModes")
        self.sal.salCommand("m1m3_command_ApplyActiveOpticForces")
        self.sal.salCommand("m1m3_command_ApplyActiveOpticForcesByBendingModes")
        self.sal.salCommand("m1m3_command_ApplyOffsetForces")
        self.sal.salCommand("m1m3_command_ApplyOffsetForcesByMirrorForce")
        self.sal.salCommand("m1m3_command_ClearAberrationForces")
        self.sal.salCommand("m1m3_command_ClearActiveOpticForces")
        self.sal.salCommand("m1m3_command_ClearOffsetForces")
        self.sal.salCommand("m1m3_command_Disable")
        self.sal.salCommand("m1m3_command_DisableHardpointCorrections")
        self.sal.salCommand("m1m3_command_Enable")
        self.sal.salCommand("m1m3_command_EnableHardpointCorrections")
        self.sal.salCommand("m1m3_command_EnterEngineering")
        self.sal.salCommand("m1m3_command_ExitEngineering")
        self.sal.salCommand("m1m3_command_LowerM1M3")
        self.sal.salCommand("m1m3_command_MoveHardpointActuators")
        self.sal.salCommand("m1m3_command_PositionM1M3")
        self.sal.salCommand("m1m3_command_RaiseM1M3")
        self.sal.salCommand("m1m3_command_Shutdown")
        self.sal.salCommand("m1m3_command_Standby")
        self.sal.salCommand("m1m3_command_Start")
        self.sal.salCommand("m1m3_command_StopHardpointMotion")
        self.sal.salCommand("m1m3_command_ModbusTransmit")
        self.sal.salCommand("m1m3_command_TranslateM1M3")
        self.sal.salEvent("m1m3_logevent_AppliedAberrationForces")
        self.sal.salEvent("m1m3_logevent_AppliedAccelerationForces")
        self.sal.salEvent("m1m3_logevent_AppliedActiveOpticForces")
        self.sal.salEvent("m1m3_logevent_AppliedAzimuthForces")
        self.sal.salEvent("m1m3_logevent_AppliedBalanceForces")
        self.sal.salEvent("m1m3_logevent_AppliedCylinderForces")
        self.sal.salEvent("m1m3_logevent_AppliedElevationForces")
        self.sal.salEvent("m1m3_logevent_AppliedForces")
        self.sal.salEvent("m1m3_logevent_AppliedOffsetForces")
        self.sal.salEvent("m1m3_logevent_AppliedSettingsMatchStart")
        self.sal.salEvent("m1m3_logevent_AppliedStaticForces")
        self.sal.salEvent("m1m3_logevent_AppliedThermalForces")
        self.sal.salEvent("m1m3_logevent_AppliedVelocityForces")
        self.sal.salEvent("m1m3_logevent_CommandRejectionWarning")
        self.sal.salEvent("m1m3_logevent_DetailedState")
        self.sal.salEvent("m1m3_logevent_ForceActuatorState")
        self.sal.salEvent("m1m3_logevent_ForceActuatorInfo")
        self.sal.salEvent("m1m3_logevent_ForceSetpointWarning")
        self.sal.salEvent("m1m3_logevent_HardpointActuatorInfo")
        self.sal.salEvent("m1m3_logevent_HardpointActuatorState")
        self.sal.salEvent("m1m3_logevent_HardpointActuatorWarning")
        self.sal.salEvent("m1m3_logevent_HardpointMonitorInfo")
        self.sal.salEvent("m1m3_logevent_ModbusResponse")
        self.sal.salEvent("m1m3_logevent_RejectedAberrationForces")
        self.sal.salEvent("m1m3_logevent_RejectedAccelerationForces")
        self.sal.salEvent("m1m3_logevent_RejectedActiveOpticForces")
        self.sal.salEvent("m1m3_logevent_RejectedAzimuthForces")
        self.sal.salEvent("m1m3_logevent_RejectedBalanceForces")
        self.sal.salEvent("m1m3_logevent_RejectedCylinderForces")
        self.sal.salEvent("m1m3_logevent_RejectedElevationForces")
        self.sal.salEvent("m1m3_logevent_RejectedForces")
        self.sal.salEvent("m1m3_logevent_RejectedOffsetForces")
        self.sal.salEvent("m1m3_logevent_RejectedSettingsMatchStart")
        self.sal.salEvent("m1m3_logevent_RejectedStaticForces")
        self.sal.salEvent("m1m3_logevent_RejectedThermalForces")
        self.sal.salEvent("m1m3_logevent_RejectedVelocityForces")
        self.sal.salEvent("m1m3_logevent_SummaryState")
        self.sal.salTelemetrySub("m1m3_AccelerometerData")
        self.sal.salTelemetrySub("m1m3_ForceActuatorData")
        self.sal.salTelemetrySub("m1m3_HardpointActuatorData")
        self.sal.salTelemetrySub("m1m3_IMSData")
        self.sal.salTelemetrySub("m1m3_InclinometerData")
        
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
        data = m1m3_command_AbortRaiseM1M3C()
        data.AbortRaiseM1M3 = run
        cmdId = self.sal.issueCommand_AbortRaiseM1M3(data)
        self.sal.waitForCompletion_AbortRaiseM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyAberrationForces(self, zForces):
        Log("M1M3: ApplyAberrationForces([%s])" % (','.join(map(str, zForces))))
        data = m1m3_command_ApplyAberrationForcesC()
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyAberrationForces(data)
        self.sal.waitForCompletion_ApplyAberrationForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyAberrationForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyAberrationForcesByBendingModes([%s])" % (','.join(map(str, coefficients))))
        data = m1m3_command_ApplyAberrationForcesByBendingModesC()
        for i in range(22):
            data.Coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_ApplyAberrationForcesByBendingModes(data)
        self.sal.waitForCompletion_ApplyAberrationForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyActiveOpticForces(self, zForces):
        Log("M1M3: ApplyActiveOpticForces([%s])" % (','.join(map(str, zForces))))
        data = m1m3_command_ApplyActiveOpticForcesC()
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyActiveOpticForces(data)
        self.sal.waitForCompletion_ApplyActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyActiveOpticForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyActiveOpticForcesByBendingModes([%s])" % (','.join(map(str, coefficients))))
        data = m1m3_command_ApplyActiveOpticForcesByBendingModesC()
        for i in range(22):
            data.Coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_ApplyActiveOpticForcesByBendingModes(data)
        self.sal.waitForCompletion_ApplyActiveOpticForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ApplyOffsetForces(self, xForces, yForces, zForces, waitForCompletion = True):
        Log("M1M3: ApplyOffsetForces([%s], [%s], [%s])" % (','.join(map(str, xForces)), ','.join(map(str, yForces)), ','.join(map(str, zForces))))
        data = m1m3_command_ApplyOffsetForcesC()
        for i in range(12):
            data.XForces[i] = xForces[i]
        for i in range(100):
            data.YForces[i] = yForces[i]
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyOffsetForces(data)
        if waitForCompletion:
            self.sal.waitForCompletion_ApplyOffsetForces(cmdId, COMMAND_TIMEOUT)
            time.sleep(COMMAND_TIME)
        
    def ApplyOffsetForcesByMirrorForce(self, fx, fy, fz, mx, my, mz, waitForCompletion = True):
        Log("M1M3: ApplyOffsetForcesByMirrorForce(%s, %s, %s, %s, %s, %s)" % (fx, fy, fz, mx, my, mz))
        data = m1m3_command_ApplyOffsetForcesByMirrorForceC()
        data.XForce = fx
        data.YForce = fy
        data.ZForce = fz
        data.XMoment = mx
        data.YMoment = my
        data.ZMoment = mz
        cmdId = self.sal.issueCommand_ApplyOffsetForcesByMirrorForce(data)
        if waitForCompletion:
            self.sal.waitForCompletion_ApplyOffsetForcesByMirrorForce(cmdId, COMMAND_TIMEOUT)
            time.sleep(COMMAND_TIME)
        
    def ClearAberrationForces(self, run = True):
        Log("M1M3: ClearAberrationForces(%s)" % (run))
        data = m1m3_command_ClearAberrationForcesC()
        data.ClearAberrationForces = run
        cmdId = self.sal.issueCommand_ClearAberrationForces(data)
        self.sal.waitForCompletion_ClearAberrationForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ClearActiveOpticForces(self, run = True):
        Log("M1M3: ClearActiveOpticForces(%s)" % (run))
        data = m1m3_command_ClearActiveOpticForcesC()
        data.ClearActiveOpticForces = run
        cmdId = self.sal.issueCommand_ClearActiveOpticForces(data)
        self.sal.waitForCompletion_ClearActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ClearOffsetForces(self, run = True):
        Log("M1M3: ClearOffsetForces(%s)" % (run))
        data = m1m3_command_ClearOffsetForcesC()
        data.ClearOffsetForces = run
        cmdId = self.sal.issueCommand_ClearOffsetForces(data)
        self.sal.waitForCompletion_ClearOffsetForces(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Disable(self, run = True):
        Log("M1M3: Disable(%s)" % (run))
        data = m1m3_command_DisableC()
        data.Disable = run
        cmdId = self.sal.issueCommand_Disable(data)
        self.sal.waitForCompletion_Disable(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def DisableHardpointCorrections(self, run = True):
        Log("M1M3: DisableHardpointCorrections(%s)" % (run))
        data = m1m3_command_DisableHardpointCorrectionsC()
        data.DisableHardpointCorrections = run
        cmdId = self.sal.issueCommand_DisableHardpointCorrections(data)
        self.sal.waitForCompletion_DisableHardpointCorrections(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Enable(self, run = True):
        Log("M1M3: Enable(%s)" % (run))
        data = m1m3_command_EnableC()
        data.Enable = run
        cmdId = self.sal.issueCommand_Enable(data)
        self.sal.waitForCompletion_Enable(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def EnableHardpointCorrections(self, run = True):
        Log("M1M3: EnableHardpointCorrections(%s)" % (run))
        data = m1m3_command_EnableHardpointCorrectionsC()
        data.EnableHardpointCorrections = run
        cmdId = self.sal.issueCommand_EnableHardpointCorrections(data)
        self.sal.waitForCompletion_EnableHardpointCorrections(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def EnterEngineering(self, run = True):
        Log("M1M3: EnterEngineering(%s)" % (run))
        data = m1m3_command_EnterEngineeringC()
        data.EnterEngineering = run
        cmdId = self.sal.issueCommand_EnterEngineering(data)
        self.sal.waitForCompletion_EnterEngineering(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ExitEngineering(self, run = True):
        Log("M1M3: ExitEngineering(%s)" % (run))
        data = m1m3_command_ExitEngineeringC()
        data.ExitEngineering = run
        cmdId = self.sal.issueCommand_ExitEngineering(data)
        self.sal.waitForCompletion_ExitEngineering(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def LowerM1M3(self, run = True):
        Log("M1M3: LowerM1M3(%s)" % (run))
        data = m1m3_command_LowerM1M3C()
        data.LowerM1M3 = run
        cmdId = self.sal.issueCommand_LowerM1M3(data)
        self.sal.waitForCompletion_LowerM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def MoveHardpointActuators(self, steps):
        Log("M1M3: MoveHardpointActuators(%s)" % (','.join(map(str, steps))))
        data = m1m3_command_MoveHardpointActuatorsC()
        for i in range(6):
            data.Steps[i] = steps[i]
        cmdId = self.sal.issueCommand_MoveHardpointActuators(data)
        self.sal.waitForCompletion_MoveHardpointActuators(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def PositionM1M3(self, xPosition = 0.0, yPosition = 0.0, zPosition = 0.0,
                     xRotation = 0.0, yRotation = 0.0, zRotation = 0.0):
        Log("M1M3: PositionM1M3(%s, %s, %s, %s, %s, %s)" % (xPosition, yPosition, zPosition, xRotation, yRotation,zRotation))
        data = m1m3_command_PositionM1M3C()
        data.XPosition = xPosition
        data.YPosition = yPosition
        data.ZPosition = zPosition
        data.XRotation = xRotation
        data.YRotation = yRotation
        data.ZRotation = zRotation
        cmdId = self.sal.issueCommand_PositionM1M3(data)
        self.sal.waitForCompletion_PositionM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def RaiseM1M3(self, bypassReferencePosition, run = True):
        Log("M1M3: RaiseM1M3(%s, %s)" % (run, bypassReferencePosition))
        data = m1m3_command_RaiseM1M3C()
        data.RaiseM1M3 = run
        data.BypassReferencePosition = bypassReferencePosition
        cmdId = self.sal.issueCommand_RaiseM1M3(data)
        self.sal.waitForCompletion_RaiseM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Shutdown(self, run = True):
        Log("M1M3: Shutdown(%s)" % (run))
        data = m1m3_command_ShutdownC()
        data.Shutdown = run
        cmdId = self.sal.issueCommand_Shutdown(data)
        self.sal.waitForCompletion_Shutdown(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
    
    def Standby(self, run = True):
        Log("M1M3: Standby(%s)" % (run))
        data = m1m3_command_StandbyC()
        data.Standby = run
        cmdId = self.sal.issueCommand_Standby(data)
        self.sal.waitForCompletion_Standby(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def Start(self, settingsToApply, run = True):
        Log("M1M3: Start(%s, %s)" % (run, settingsToApply))
        data = m1m3_command_StartC()
        data.Start = run
        data.SettingsToApply = settingsToApply
        cmdId = self.sal.issueCommand_Start(data)
        self.sal.waitForCompletion_Start(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def StopHardpointMotion(self, run = True):
        Log("M1M3: StopHardpointMotion(%s)" % (run))
        data = m1m3_command_StopHardpointMotionC()
        data.StopHardpointMotion = run
        cmdId = self.sal.issueCommand_StopHardpointMotion(data)
        self.sal.waitForCompletion_StopHardpointMotion(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def TranslateM1M3(self, xTranslation = 0.0, yTranslation = 0.0, zTranslation = 0.0, xRotation = 0.0, yRotation = 0.0, zRotation = 0.0):
        Log("M1M3: TranslateM1M3(%s, %s, %s, %s, %s, %s)" % (xTranslation, yTranslation, zTranslation, xRotation, yRotation,zRotation))
        data = m1m3_command_TranslateM1M3C()
        data.XTranslation = xTranslation
        data.YTranslation = yTranslation
        data.ZTranslation = zTranslation
        data.XRotation = xRotation
        data.YRotation = yRotation
        data.ZRotation = zRotation
        cmdId = self.sal.issueCommand_TranslateM1M3(data)
        self.sal.waitForCompletion_TranslateM1M3(cmdId, COMMAND_TIMEOUT)
        time.sleep(COMMAND_TIME)
        
    def ModbusTransmit(self, actuatorId, functionCode, rawData):
        Log("M1M3: ModbusTransmit(%d, %d, %d)" % (actuatorId, functionCode, len(rawData)))
        data = m1m3_command_ModbusTransmitC()
        data.ActuatorId = actuatorId
        data.FunctionCode = functionCode
        for i in range(len(rawData)):
            data.Data[i] = rawData[i]
        data.DataLength = len(rawData)
        cmdId = self.sal.issueCommand_ModbusTransmit(data)
        self.sal.waitForCompletion_ModbusTransmit(cmdId, COMMAND_TIMEOUT)
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
        data = m1m3_logevent_AppliedAberrationForcesC()
        result = self.sal.getEvent_AppliedAberrationForces(data)
        return result, data
        
    def GetEventAppliedAberrationForces(self):
        return self.GetEvent(self.GetNextEventAppliedAberrationForces)
        
    def SearchEventAppliedAberrationForces(self, predicate):
        return self.SearchEvent(self.GetNextEventAppliedAberrationForces, predicate)

    def GetNextEventAppliedAccelerationForces(self):
        data = m1m3_logevent_AppliedAccelerationForcesC()
        result = self.sal.getEvent_AppliedAccelerationForces(data)
        return result, data
        
    def GetEventAppliedAccelerationForces(self):
        return self.GetEvent(self.GetNextEventAppliedAccelerationForces)

    def GetNextEventAppliedActiveOpticForces(self):
        data = m1m3_logevent_AppliedActiveOpticForcesC()
        result = self.sal.getEvent_AppliedActiveOpticForces(data)
        return result, data
        
    def GetEventAppliedActiveOpticForces(self):
        return self.GetEvent(self.GetNextEventAppliedActiveOpticForces)
    
    def GetNextEventAppliedAzimuthForces(self):
        data = m1m3_logevent_AppliedAzimuthForcesC()
        result = self.sal.getEvent_AppliedAzimuthForces(data)
        return result, data

    def GetEventAppliedAzimuthForces(self):
        return self.GetEvent(self.GetNextEventAppliedAzimuthForces)
    
    def GetNextEventAppliedBalanceForces(self):
        data = m1m3_logevent_AppliedBalanceForcesC()
        result = self.sal.getEvent_AppliedBalanceForces(data)
        return result, data
        
    def GetEventAppliedBalanceForces(self):
        return self.GetEvent(self.GetNextEventAppliedBalanceForces)
    
    def GetNextEventAppliedCylinderForces(self):
        data = m1m3_logevent_AppliedCylinderForcesC()
        result = self.sal.getEvent_AppliedCylinderForces(data)
        return result, data
        
    def GetEventAppliedCylinderForces(self):
        return self.GetEvent(self.GetNextEventAppliedCylinderForces)
    
    def GetNextEventAppliedElevationForces(self):
        data = m1m3_logevent_AppliedElevationForcesC()
        result = self.sal.getEvent_AppliedElevationForces(data)
        return result, data
        
    def GetEventAppliedElevationForces(self):
        return self.GetEvent(self.GetNextEventAppliedElevationForces)
    
    def GetNextEventAppliedForces(self):
        data = m1m3_logevent_AppliedForcesC()
        result = self.sal.getEvent_AppliedForces(data)
        return result, data
        
    def GetEventAppliedForces(self):
        return self.GetEvent(self.GetNextEventAppliedForces)
        
    def GetNextEventAppliedOffsetForces(self):
        data = m1m3_logevent_AppliedOffsetForcesC()
        result = self.sal.getEvent_AppliedOffsetForces(data)
        return result, data
        
    def GetEventAppliedOffsetForces(self):
        return self.GetEvent(self.GetNextEventAppliedOffsetForces)
    
    def GetNextEventAppliedStaticForces(self):
        data = m1m3_logevent_AppliedStaticForcesC()
        result = self.sal.getEvent_AppliedStaticForces(data)
        return result, data
        
    def GetEventAppliedStaticForces(self):
        return self.GetEvent(self.GetNextEventAppliedStaticForces)
    
    def GetNextEventAppliedThermalForces(self):
        data = m1m3_logevent_AppliedThermalForcesC()
        result = self.sal.getEvent_AppliedThermalForces(data)
        return result, data
        
    def GetEventAppliedThermalForces(self):
        return self.GetEvent(self.GetNextEventAppliedThermalForces)
    
    def GetNextEventAppliedVelocityForces(self):
        data = m1m3_logevent_AppliedVelocityForcesC()
        result = self.sal.getEvent_AppliedVelocityForces(data)
        return result, data
        
    def GetEventAppliedVelocityForces(self):
        return self.GetEvent(self.GetNextEventAppliedVelocityForces)
            
    def GetNextEventCommandRejectionWarning(self):
        data = m1m3_logevent_CommandRejectionWarningC()
        result = self.sal.getEvent_CommandRejectionWarning(data)
        return result, data
        
    def GetEventCommandRejectionWarning(self):
        return self.GetEvent(self.GetNextEventCommandRejectionWarning)
       
    def GetNextEventDetailedState(self):
        data = m1m3_logevent_DetailedStateC()
        result = self.sal.getEvent_DetailedState(data)
        return result, data
        
    def GetEventDetailedState(self):
        return self.GetEvent(self.GetNextEventDetailedState)
        
    def GetNextEventForceActuatorState(self):
        data = m1m3_logevent_ForceActuatorStateC()
        result = self.sal.getEvent_ForceActuatorState(data)
        return result, data
        
    def GetEventForceActuatorState(self):
        return self.GetEvent(self.GetNextEventForceActuatorState)
        
    def GetNextEventForceActuatorInfo(self):
        data = m1m3_logevent_ForceActuatorInfoC()
        result = self.sal.getEvent_ForceActuatorInfo(data)
        return result, data
        
    def GetEventForceActuatorInfo(self):
        return self.GetEvent(self.GetNextEventForceActuatorInfo)

    def GetNextEventForceSetpointWarning(self):
        data = m1m3_logevent_ForceSetpointWarningC()
        result = self.sal.getEvent_ForceSetpointWarning(data)
        return result, data

    def GetEventForceSetpointWarning(self):
        return self.GetEvent(self.GetNextEventForceSetpointWarning)
        
    def GetNextEventHardpointActuatorInfo(self):
        data = m1m3_logevent_HardpointActuatorInfoC()
        result = self.sal.getEvent_HardpointActuatorInfo(data)
        return result, data
        
    def GetEventHardpointActuatorInfo(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorInfo)
    
    def GetNextEventHardpointActuatorState(self):
        data = m1m3_logevent_HardpointActuatorStateC()
        result = self.sal.getEvent_HardpointActuatorState(data)
        return result, data
        
    def GetEventHardpointActuatorState(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorState)
    
    def GetNextEventHardpointActuatorWarning(self):
        data = m1m3_logevent_HardpointActuatorWarningC()
        result = self.sal.getEvent_HardpointActuatorWarning(data)
        return result, data
        
    def GetEventHardpointActuatorWarning(self):
        return self.GetEvent(self.GetNextEventHardpointActuatorWarning)
        
    def GetNextEventHardpointMonitorInfo(self):
        data = m1m3_logevent_HardpointMonitorInfoC()
        result = self.sal.getEvent_HardpointMonitorInfo(data)
        return result, data
        
    def GetEventHardpointMonitorInfo(self):
        return self.GetEvent(self.GetNextEventHardpointMonitorInfo)
        
    def GetNextEventModbusResponse(self):
        data = m1m3_logevent_ModbusResponseC()
        result = self.sal.getEvent_ModbusResponseC(data)
        return result, data
        
    def GetEventModbusResponse(self):
        return self.GetEvent(self.GetNextEventModbusResponse)
        
    def GetNextEventRejectedAberrationForces(self):
        data = m1m3_logevent_RejectedAberrationForcesC()
        result = self.sal.getEvent_RejectedAberrationForces(data)
        return result, data
        
    def GetEventRejectedAberrationForces(self):
        return self.GetEvent(self.GetNextEventRejectedAberrationForces)

    def GetNextEventRejectedAccelerationForces(self):
        data = m1m3_logevent_RejectedAccelerationForcesC()
        result = self.sal.getEvent_RejectedAccelerationForces(data)
        return result, data
        
    def GetEventRejectedAccelerationForces(self):
        return self.GetEvent(self.GetNextEventRejectedAccelerationForces)

    def GetNextEventRejectedActiveOpticForces(self):
        data = m1m3_logevent_RejectedActiveOpticForcesC()
        result = self.sal.getEvent_RejectedActiveOpticForces(data)
        return result, data
        
    def GetEventRejectedActiveOpticForces(self):
        return self.GetEvent(self.GetNextEventRejectedActiveOpticForces)
    
    def GetNextEventRejectedAzimuthForces(self):
        data = m1m3_logevent_RejectedAzimuthForcesC()
        result = self.sal.getEvent_RejectedAzimuthForces(data)
        return result, data
        
    def GetEventRejectedAzimuthForces(self):
        return self.GetEvent(self.GetNextEventRejectedAzimuthForces)
    
    def GetNextEventRejectedBalanceForces(self):
        data = m1m3_logevent_RejectedBalanceForcesC()
        result = self.sal.getEvent_RejectedBalanceForces(data)
        return result, data
        
    def GetEventRejectedBalanceForces(self):
        return self.GetEvent(self.GetNextEventRejectedBalanceForces)
    
    def GetNextEventRejectedCylinderForces(self):
        data = m1m3_logevent_RejectedCylinderForcesC()
        result = self.sal.getEvent_RejectedCylinderForces(data)
        return result, data
        
    def GetEventRejectedCylinderForces(self):
        return self.GetEvent(self.GetNextEventRejectedCylinderForces)
    
    def GetNextEventRejectedElevationForces(self):
        data = m1m3_logevent_RejectedElevationForcesC()
        result = self.sal.getEvent_RejectedElevationForces(data)
        return result, data
        
    def GetEventRejectedElevationForces(self):
        return self.GetEvent(self.GetNextEventRejectedElevationForces)
    
    def GetNextEventRejectedForces(self):
        data = m1m3_logevent_RejectedForcesC()
        result = self.sal.getEvent_RejectedForces(data)
        return result, data
        
    def GetEventRejectedForces(self):
        return self.GetEvent(self.GetNextEventRejectedForces)
    
    def GetNextEventRejectedOffsetForces(self):
        data = m1m3_logevent_RejectedOffsetForcesC()
        result = self.sal.getEvent_RejectedOffsetForces(data)
        return result, data
        
    def GetEventRejectedOffsetForces(self):
        return self.GetEvent(self.GetNextEventRejectedOffsetForces)
    
    def GetNextEventRejectedStaticForces(self):
        data = m1m3_logevent_RejectedStaticForcesC()
        result = self.sal.getEvent_RejectedStaticForces(data)
        return result, data
        
    def GetEventRejectedStaticForces(self):
        return self.GetEvent(self.GetNextEventRejectedStaticForces)
    
    def GetNextEventRejectedThermalForces(self):
        data = m1m3_logevent_RejectedThermalForcesC()
        result = self.sal.getEvent_RejectedThermalForces(data)
        return result, data
        
    def GetEventRejectedThermalForces(self):
        return self.GetEvent(self.GetNextEventRejectedThermalForces)
    
    def GetNextEventRejectedVelocityForces(self):
        data = m1m3_logevent_RejectedVelocityForcesC()
        result = self.sal.getEvent_RejectedVelocityForces(data)
        return result, data
        
    def GetEventRejectedVelocityForces(self):
        return self.GetEvent(self.GetNextEventRejectedVelocityForces)
        
    def GetNextEventSummaryState(self):
        data = m1m3_logevent_SummaryStateC()
        result = self.sal.getEvent_SummaryState(data)
        return result, data
        
    def GetEventSummaryState(self):
        return self.GetEvent(self.GetNextEventSummaryState)
        
    def GetSampleAccelerometerData(self):
        data = m1m3_AccelerometerDataC()
        result = self.sal.getSample_AccelerometerData(data)
        return result, data
        
    def GetSampleForceActuatorData(self):
        data = m1m3_ForceActuatorDataC()
        result = self.sal.getSample_ForceActuatorData(data)
        return result, data

    def GetNextSampleForceActuatorData(self):
        data = m1m3_ForceActuatorDataC()
        result = self.sal.getNextSample_ForceActuatorData(data)
        return result, data
        
    def GetSampleHardpointActuatorData(self):
        data = m1m3_HardpointActuatorDataC()
        result = self.sal.getSample_HardpointActuatorData(data)
        return result, data
    
    def GetNextSampleHardpointActuatorData(self):
        data = m1m3_HardpointActuatorDataC()
        result = self.sal.getNextSample_HardpointActuatorData(data)
        return result, data
        
    def GetSampleIMSData(self):
        data = m1m3_IMSDataC()
        result = self.sal.getSample_IMSData(data)
        return result, data

    def GetNextSampleIMSData(self):
        data = m1m3_IMSDataC()
        result = self.sal.getNextSample_IMSData(data)
        return result, data
                
    def GetSampleInclinometerData(self):
        data = m1m3_InclinometerDataC()
        result = self.sal.getSample_InclinometerData(data)
        return result, data
        
    def _floatToBytes(self, someData:float, parameterName:str, byteSize:int):
        floatBytes = struct.pack(">f", someData)
        if (len(floatBytes) != byteSize):
            raise Exception(parameterName + " size does not match the byte size("
                            + str(byteSize) + ") specified.")
        return floatBytes
        
        
