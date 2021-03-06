import time
from SALPY_m1m3 import *
from Utilities import Log

class M1M3:
    def __init__(self):
        Log("M1M3: Initializing SAL")
        self.sal = SAL_m1m3()
        self.sal.setDebugLevel(0)
        self.sal.salCommand("m1m3_command_Start")
        self.sal.salCommand("m1m3_command_Enable")
        self.sal.salCommand("m1m3_command_EnterEngineering")
        self.sal.salCommand("m1m3_command_RaiseM1M3")
        self.sal.salCommand("m1m3_command_AbortRaiseM1M3")
        self.sal.salCommand("m1m3_command_LowerM1M3")
        self.sal.salCommand("m1m3_command_ExitEngineering")
        self.sal.salCommand("m1m3_command_Disable")
        self.sal.salCommand("m1m3_command_Standby")
        self.sal.salCommand("m1m3_command_Shutdown")
        self.sal.salEvent("m1m3_logevent_DetailedState")
        
    def __del__(self):
        Log("M1M3: Shutting down SAL")
        time.sleep(1)
        self.sal.salShutdown();
        
    def Start(self, settingsToApply, run = True):
        Log("M1M3: Start(%s, %s)" % (run, settingsToApply))
        data = m1m3_command_StartC()
        data.Start = run
        data.SettingsToApply = settingsToApply
        cmdId = self.sal.issueCommand_Start(data)
        self.sal.waitForCompletion_Start(cmdId, 10)
        
    def Enable(self, run = True):
        Log("M1M3: Enable(%s)" % (run))
        data = m1m3_command_EnableC()
        data.Enable = run
        cmdId = self.sal.issueCommand_Enable(data)
        self.sal.waitForCompletion_Enable(cmdId, 10)
        
    def RaiseM1M3(self, bypassReferencePosition, run = True):
        Log("M1M3: RaiseM1M3(%s, %s)" % (run, bypassReferencePosition))
        data = m1m3_command_RaiseM1M3C()
        data.RaiseM1M3 = run
        data.BypassReferencePosition = bypassReferencePosition
        cmdId = self.sal.issueCommand_RaiseM1M3(data)
        self.sal.waitForCompletion_RaiseM1M3(cmdId, 10)
        
    def AbortRaiseM1M3(self, run = True):
        Log("M1M3: AbortRaiseM1M3(%s)" % (run))
        data = m1m3_command_AbortRaiseM1M3C()
        data.AbortRaiseM1M3 = run
        cmdId = self.sal.issueCommand_AbortRaiseM1M3(data)
        self.sal.waitForCompletion_AbortRaiseM1M3(cmdId, 10)
        
    def LowerM1M3(self, run = True):
        Log("M1M3: LowerM1M3(%s)" % (run))
        data = m1m3_command_LowerM1M3C()
        data.LowerM1M3 = run
        cmdId = self.sal.issueCommand_LowerM1M3(data)
        self.sal.waitForCompletion_LowerM1M3(cmdId, 10)
        
    def EnterEngineering(self, run = True):
        Log("M1M3: EnterEngineering(%s)" % (run))
        data = m1m3_command_EnterEngineeringC()
        data.EnterEngineering = run
        cmdId = self.sal.issueCommand_EnterEngineering(data)
        self.sal.waitForCompletion_EnterEngineering(cmdId, 10)
        
    def ExitEngineering(self, run = True):
        Log("M1M3: ExitEngineering(%s)" % (run))
        data = m1m3_command_ExitEngineeringC()
        data.ExitEngineering = run
        cmdId = self.sal.issueCommand_ExitEngineering(data)
        self.sal.waitForCompletion_ExitEngineering(cmdId, 10)
        
    def Disable(self, run = True):
        Log("M1M3: Disable(%s)" % (run))
        data = m1m3_command_DisableC()
        data.Disable = run
        cmdId = self.sal.issueCommand_Disable(data)
        self.sal.waitForCompletion_Disable(cmdId, 10)
        
    def Standby(self, run = True):
        Log("M1M3: Standby(%s)" % (run))
        data = m1m3_command_StandbyC()
        data.Standby = run
        cmdId = self.sal.issueCommand_Standby(data)
        self.sal.waitForCompletion_Standby(cmdId, 10)
        
    def Shutdown(self, run = True):
        Log("M1M3: Shutdown(%s)" % (run))
        data = m1m3_command_ShutdownC()
        data.Shutdown = run
        cmdId = self.sal.issueCommand_Shutdown(data)
        self.sal.waitForCompletion_Shutdown(cmdId, 10)
        
    def GetEventDetailedState(self):
        data = m1m3_logevent_DetailedStateC()
        result = self.sal.getEvent_DetailedState(data)
        return result, data

    