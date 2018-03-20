import time
from SALPY_m1m3 import *
from Utilities import *

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
        self.sal.salCommand("m1m3_command_Enable")
        self.sal.salCommand("m1m3_command_EnterEngineering")
        self.sal.salCommand("m1m3_command_ExitEngineering")
        self.sal.salCommand("m1m3_command_LowerM1M3")
        self.sal.salCommand("m1m3_command_RaiseM1M3")
        self.sal.salCommand("m1m3_command_Shutdown")
        self.sal.salCommand("m1m3_command_Standby")
        self.sal.salCommand("m1m3_command_Start")
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
        self.sal.salTelemetrySub("m1m3_InclinometerData")
        
    def __del__(self):
        Log("M1M3: Shutting down SAL")
        time.sleep(1)
        self.sal.salShutdown();
        
    def AbortRaiseM1M3(self, run = True):
        Log("M1M3: AbortRaiseM1M3(%s)" % (run))
        data = m1m3_command_AbortRaiseM1M3C()
        data.AbortRaiseM1M3 = run
        cmdId = self.sal.issueCommand_AbortRaiseM1M3(data)
        self.sal.waitForCompletion_AbortRaiseM1M3(cmdId, COMMAND_TIMEOUT)
        
    def ApplyAberrationForces(self, zForces):
        Log("M1M3: ApplyAberrationForces([%s])" % (','.join(zForces)))
        data = m1m3_command_ApplyAberrationForcesC()
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyAberrationForces(data)
        self.sal.waitForCompletion_ApplyAberrationForces(cmdId, COMMAND_TIMEOUT)
        
    def ApplyAberrationForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyAberrationForcesByBendingModes([%s])" % (','.join(coefficients)))
        data = m1m3_command_ApplyAberrationForcesByBendingModesC()
        for i in range(22):
            data.Coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_ApplyAberrationForcesByBendingModes(data)
        self.sal.waitForCompletion_ApplyAberrationForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        
    def ApplyActiveOpticForces(self, zForces):
        Log("M1M3: ApplyActiveOpticForces([%s])" % (','.join(zForces)))
        data = m1m3_command_ApplyActiveOpticForcesC()
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyActiveOpticForces(data)
        self.sal.waitForCompletion_ApplyActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        
    def ApplyActiveOpticForcesByBendingModes(self, coefficients):
        Log("M1M3: ApplyActiveOpticForcesByBendingModes([%s])" % (','.join(coefficients)))
        data = m1m3_command_ApplyActiveOpticForcesByBendingModesC()
        for i in range(22):
            data.Coefficients[i] = coefficients[i]
        cmdId = self.sal.issueCommand_ApplyActiveOpticForcesByBendingModes(data)
        self.sal.waitForCompletion_ApplyActiveOpticForcesByBendingModes(cmdId, COMMAND_TIMEOUT)
        
    def ApplyOffsetForces(self, xForces, yForces, zForces):
        Log("M1M3: ApplyOffsetForces([%s], [%s], [%s])" % (','.join(xForces), ','.join(yForces), ','.join(zForces)))
        data = m1m3_command_ApplyOffsetForcesC()
        for i in range(12):
            data.XForces[i] = xForces[i]
        for i in range(100):
            data.YForces[i] = yForces[i]
        for i in range(156):
            data.ZForces[i] = zForces[i]
        cmdId = self.sal.issueCommand_ApplyOffsetForces(data)
        self.sal.waitForCompletion_ApplyOffsetForces(cmdId, COMMAND_TIMEOUT)
        
    def ApplyOffsetForcesByMirrorForce(self, fx, fy, fz, mx, my, mz):
        Log("M1M3: ApplyOffsetForcesByMirrorForce(%s, %s, %s, %s, %s, %s)" % (fx, fy, fz, mx, my, mz))
        data = m1m3_command_ApplyOffsetForcesByMirrorForceC()
        data.XForce = fx
        data.YForce = fy
        data.ZForce = fz
        data.XMoment = mx
        data.YMoment = my
        data.ZMoment = mz
        cmdId = self.sal.issueCommand_ApplyOffsetForcesByMirrorForce(data)
        self.sal.waitForCompletion_ApplyOffsetForcesByMirrorForce(cmdId, COMMAND_TIMEOUT)
        
    def ClearAberrationForces(self, run = True):
        Log("M1M3: ClearAberrationForces(%s)" % (run))
        data = m1m3_command_ClearAberrationForcesC()
        data.ClearAberrationForces = run
        cmdId = self.sal.issueCommand_ClearAberrationForces(data)
        self.sal.waitForCompletion_ClearAberrationForces(cmdId, COMMAND_TIMEOUT)
        
    def ClearActiveOpticForces(self, run = True):
        Log("M1M3: ClearActiveOpticForces(%s)" % (run))
        data = m1m3_command_ClearActiveOpticForcesC()
        data.ClearActiveOpticForces = run
        cmdId = self.sal.issueCommand_ClearActiveOpticForces(data)
        self.sal.waitForCompletion_ClearActiveOpticForces(cmdId, COMMAND_TIMEOUT)
        
    def ClearOffsetForces(self, run = True):
        Log("M1M3: ClearOffsetForces(%s)" % (run))
        data = m1m3_command_ClearOffsetForcesC()
        data.ClearOffsetForces = run
        cmdId = self.sal.issueCommand_ClearOffsetForces(data)
        self.sal.waitForCompletion_ClearOffsetForces(cmdId, COMMAND_TIMEOUT)
        
    def Disable(self, run = True):
        Log("M1M3: Disable(%s)" % (run))
        data = m1m3_command_DisableC()
        data.Disable = run
        cmdId = self.sal.issueCommand_Disable(data)
        self.sal.waitForCompletion_Disable(cmdId, COMMAND_TIMEOUT)
        
    def Enable(self, run = True):
        Log("M1M3: Enable(%s)" % (run))
        data = m1m3_command_EnableC()
        data.Enable = run
        cmdId = self.sal.issueCommand_Enable(data)
        self.sal.waitForCompletion_Enable(cmdId, COMMAND_TIMEOUT)
        
    def EnterEngineering(self, run = True):
        Log("M1M3: EnterEngineering(%s)" % (run))
        data = m1m3_command_EnterEngineeringC()
        data.EnterEngineering = run
        cmdId = self.sal.issueCommand_EnterEngineering(data)
        self.sal.waitForCompletion_EnterEngineering(cmdId, COMMAND_TIMEOUT)
        
    def ExitEngineering(self, run = True):
        Log("M1M3: ExitEngineering(%s)" % (run))
        data = m1m3_command_ExitEngineeringC()
        data.ExitEngineering = run
        cmdId = self.sal.issueCommand_ExitEngineering(data)
        self.sal.waitForCompletion_ExitEngineering(cmdId, COMMAND_TIMEOUT)
        
    def LowerM1M3(self, run = True):
        Log("M1M3: LowerM1M3(%s)" % (run))
        data = m1m3_command_LowerM1M3C()
        data.LowerM1M3 = run
        cmdId = self.sal.issueCommand_LowerM1M3(data)
        self.sal.waitForCompletion_LowerM1M3(cmdId, COMMAND_TIMEOUT)
        
    def RaiseM1M3(self, bypassReferencePosition, run = True):
        Log("M1M3: RaiseM1M3(%s, %s)" % (run, bypassReferencePosition))
        data = m1m3_command_RaiseM1M3C()
        data.RaiseM1M3 = run
        data.BypassReferencePosition = bypassReferencePosition
        cmdId = self.sal.issueCommand_RaiseM1M3(data)
        self.sal.waitForCompletion_RaiseM1M3(cmdId, COMMAND_TIMEOUT)
        
    def Shutdown(self, run = True):
        Log("M1M3: Shutdown(%s)" % (run))
        data = m1m3_command_ShutdownC()
        data.Shutdown = run
        cmdId = self.sal.issueCommand_Shutdown(data)
        self.sal.waitForCompletion_Shutdown(cmdId, COMMAND_TIMEOUT)
    
    def Standby(self, run = True):
        Log("M1M3: Standby(%s)" % (run))
        data = m1m3_command_StandbyC()
        data.Standby = run
        cmdId = self.sal.issueCommand_Standby(data)
        self.sal.waitForCompletion_Standby(cmdId, COMMAND_TIMEOUT)
        
    def Start(self, settingsToApply, run = True):
        Log("M1M3: Start(%s, %s)" % (run, settingsToApply))
        data = m1m3_command_StartC()
        data.Start = run
        data.SettingsToApply = settingsToApply
        cmdId = self.sal.issueCommand_Start(data)
        self.sal.waitForCompletion_Start(cmdId, COMMAND_TIMEOUT)

    def GetEventAppliedAberrationForces(self):
        data = m1m3_logevent_AppliedAberrationForcesC()
        result = self.sal.getEvent_AppliedAberrationForces(data)
        return result, data

    def GetEventAppliedAccelerationForces(self):
        data = m1m3_logevent_AppliedAccelerationForcesC()
        result = self.sal.getEvent_AppliedAccelerationForces(data)
        return result, data

    def GetEventAppliedActiveOpticForces(self):
        data = m1m3_logevent_AppliedActiveOpticForcesC()
        result = self.sal.getEvent_AppliedActiveOpticForces(data)
        return result, data
    
    def GetEventAppliedAzimuthForces(self):
        data = m1m3_logevent_AppliedAzimuthForcesC()
        result = self.sal.getEvent_AppliedAzimuthForces(data)
        return result, data
    
    def GetEventAppliedBalanceForces(self):
        data = m1m3_logevent_AppliedBalanceForcesC()
        result = self.sal.getEvent_AppliedBalanceForces(data)
        return result, data
    
    def GetEventAppliedCylinderForces(self):
        data = m1m3_logevent_AppliedCylinderForcesC()
        result = self.sal.getEvent_AppliedCylinderForces(data)
        return result, data
    
    def GetEventAppliedElevationForces(self):
        data = m1m3_logevent_AppliedElevationForcesC()
        result = self.sal.getEvent_AppliedElevationForces(data)
        return result, data
    
    def GetEventAppliedForces(self):
        data = m1m3_logevent_AppliedForcesC()
        result = self.sal.getEvent_AppliedForces(data)
        return result, data
    
    def GetEventAppliedOffsetForces(self):
        data = m1m3_logevent_AppliedOffsetForcesC()
        result = self.sal.getEvent_AppliedOffsetForces(data)
        return result, data
    
    def GetEventAppliedStaticForces(self):
        data = m1m3_logevent_AppliedStaticForcesC()
        result = self.sal.getEvent_AppliedStaticForces(data)
        return result, data
    
    def GetEventAppliedThermalForces(self):
        data = m1m3_logevent_AppliedThermalForcesC()
        result = self.sal.getEvent_AppliedThermalForces(data)
        return result, data
    
    def GetEventAppliedVelocityForces(self):
        data = m1m3_logevent_AppliedVelocityForcesC()
        result = self.sal.getEvent_AppliedVelocityForces(data)
        return result, data
            
    def GetEventCommandRejectionWarning(self):
        data = m1m3_logevent_CommandRejectionWarningC()
        result = self.sal.getEvent_CommandRejectionWarning(data)
        return result, data
       
    def GetEventDetailedState(self):
        data = m1m3_logevent_DetailedStateC()
        result = self.sal.getEvent_DetailedState(data)
        return result, data
        
    def GetEventForceActuatorState(self):
        data = m1m3_logevent_ForceActuatorStateC()
        result = self.sal.getEvent_ForceActuatorState(data)
        return result, data
        
    def GetEventRejectedAberrationForces(self):
        data = m1m3_logevent_RejectedAberrationForcesC()
        result = self.sal.getEvent_RejectedAberrationForces(data)
        return result, data

    def GetEventRejectedAccelerationForces(self):
        data = m1m3_logevent_RejectedAccelerationForcesC()
        result = self.sal.getEvent_RejectedAccelerationForces(data)
        return result, data

    def GetEventRejectedActiveOpticForces(self):
        data = m1m3_logevent_RejectedActiveOpticForcesC()
        result = self.sal.getEvent_RejectedActiveOpticForces(data)
        return result, data
    
    def GetEventRejectedAzimuthForces(self):
        data = m1m3_logevent_RejectedAzimuthForcesC()
        result = self.sal.getEvent_RejectedAzimuthForces(data)
        return result, data
    
    def GetEventRejectedBalanceForces(self):
        data = m1m3_logevent_RejectedBalanceForcesC()
        result = self.sal.getEvent_RejectedBalanceForces(data)
        return result, data
    
    def GetEventRejectedCylinderForces(self):
        data = m1m3_logevent_RejectedCylinderForcesC()
        result = self.sal.getEvent_RejectedCylinderForces(data)
        return result, data
    
    def GetEventRejectedElevationForces(self):
        data = m1m3_logevent_RejectedElevationForcesC()
        result = self.sal.getEvent_RejectedElevationForces(data)
        return result, data
    
    def GetEventRejectedForces(self):
        data = m1m3_logevent_RejectedForcesC()
        result = self.sal.getEvent_RejectedForces(data)
        return result, data
    
    def GetEventRejectedOffsetForces(self):
        data = m1m3_logevent_RejectedOffsetForcesC()
        result = self.sal.getEvent_RejectedOffsetForces(data)
        return result, data
    
    def GetEventRejectedStaticForces(self):
        data = m1m3_logevent_RejectedStaticForcesC()
        result = self.sal.getEvent_RejectedStaticForces(data)
        return result, data
    
    def GetEventRejectedThermalForces(self):
        data = m1m3_logevent_RejectedThermalForcesC()
        result = self.sal.getEvent_RejectedThermalForces(data)
        return result, data
    
    def GetEventRejectedVelocityForces(self):
        data = m1m3_logevent_RejectedVelocityForcesC()
        result = self.sal.getEvent_RejectedVelocityForces(data)
        return result, data
        
    def GetEventSummaryState(self):
        data = m1m3_logevent_SummaryStateC()
        result = self.sal.getEvent_SummaryState(data)
        return result, data
                
    def GetSampleInclinometerData(self):
        data = m1m3_InclinometerDataC()
        result = self.sal.getSample_InclinometerData(data)
        return result, data
        
        