from Utilities import *
from SALPY_m1m3 import *
import CalculateBendingModeForces
import CalculateDistributionForces
import ForceActuatorTable

########################################################################
# Test Numbers: M13T-025, M13T-026, M13T-017
# Author:       CContaxis
# Description:  Verify the various force components are applied properly
#               the Active and ActiveEngineering states
#               Verify force components are overwritten when applied, not
#               accumulated
########################################################################

class VerifyControlSystemLUT:
    def Run(self, m1m3, sim):
        Header("Verify Control System LUT")
        m1m3.Start("Default")
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        m1m3.Enable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.EnterEngineering()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_ParkedEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        m1m3.RaiseM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_RaisingEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("StaticForcesApplied", data.StaticForcesApplied, 0)
        Equal("ElevationForcesApplied", data.ElevationForcesApplied, 1)
        Equal("AzimuthForcesApplied", data.AzimuthForcesApplied, 0)
        Equal("ThermalForcesApplied", data.ThermalForcesApplied, 0)
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 0)
        Equal("AccelerationForcesApplied", data.AccelerationForcesApplied, 0)
        Equal("VelocityForcesApplied", data.VelocityForcesApplied, 0)
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 0)
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 0)
        Equal("BalanceForcesApplied", data.BalanceForcesApplied, 0)
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ActiveEngineeringState)        
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)    
        result, data = m1m3.GetEventForceActuatorState()
        Equal("StaticForcesApplied", data.StaticForcesApplied, 1)
        Equal("ElevationForcesApplied", data.ElevationForcesApplied, 1)
        Equal("AzimuthForcesApplied", data.AzimuthForcesApplied, 1)
        Equal("ThermalForcesApplied", data.ThermalForcesApplied, 1)
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 0)
        Equal("AccelerationForcesApplied", data.AccelerationForcesApplied, 1)
        Equal("VelocityForcesApplied", data.VelocityForcesApplied, 1)
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 0)
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 0)
        Equal("BalanceForcesApplied", data.BalanceForcesApplied, 1)        
        
        self.CheckAberrationForces(m1m3, sim)
        self.CheckAccelerationForces(m1m3, sim)
        self.CheckActiveOpticForces(m1m3, sim)
        self.CheckBalanceForces(m1m3, sim)
        self.CheckElevationForces(m1m3, sim)
        self.CheckOffsetForces(m1m3, sim)
        self.CheckStaticForces(m1m3, sim)
        self.CheckThermalForces(m1m3, sim)
        self.CheckVelocityForces(m1m3, sim)
        
        m1m3.LowerM1M3()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_LoweringEngineeringState)
        result, data = m1m3.GetEventSummaryState()
        result, data = m1m3.GetEventForceActuatorState()
        Equal("StaticForcesApplied", data.StaticForcesApplied, 0)
        Equal("ElevationForcesApplied", data.ElevationForcesApplied, 1)
        Equal("AzimuthForcesApplied", data.AzimuthForcesApplied, 0)
        Equal("ThermalForcesApplied", data.ThermalForcesApplied, 0)
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 0)
        Equal("AccelerationForcesApplied", data.AccelerationForcesApplied, 0)
        Equal("VelocityForcesApplied", data.VelocityForcesApplied, 0)
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 0)
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 0)
        Equal("BalanceForcesApplied", data.BalanceForcesApplied, 0)
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        WaitUntil("DetailedState", 300, lambda: m1m3.GetEventDetailedState()[1].DetailedState == m1m3_shared_DetailedStates_ParkedEngineeringState)  
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_EnabledState)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("StaticForcesApplied", data.StaticForcesApplied, 0)
        Equal("ElevationForcesApplied", data.ElevationForcesApplied, 0)
        Equal("AzimuthForcesApplied", data.AzimuthForcesApplied, 0)
        Equal("ThermalForcesApplied", data.ThermalForcesApplied, 0)
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 0)
        Equal("AccelerationForcesApplied", data.AccelerationForcesApplied, 0)
        Equal("VelocityForcesApplied", data.VelocityForcesApplied, 0)
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 0)
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 0)
        Equal("BalanceForcesApplied", data.BalanceForcesApplied, 0)
        m1m3.Disable()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_DisabledState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_DisabledState)
        m1m3.Standby()
        result, data = m1m3.GetEventDetailedState()
        Equal("DetailedState", data.DetailedState, m1m3_shared_DetailedStates_StandbyState)
        result, data = m1m3.GetEventSummaryState()
        Equal("SummaryState", data.SummaryState, m1m3_shared_SummaryStates_StandbyState)
        
    def CheckAberrationForces(self, m1m3, sim):
        SubHeader("Aberration Forces")
        zForces = []
        for i in range(156):
            zForces.append(i)
        m1m3.ApplyAberrationForces(zForces)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 1)
        result, data = m1m3.GetEventAppliedAberrationForces()
        for i in range(156):
            InTolerance("AppliedAberrationForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        coefficients = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        m1m3.ApplyAberrationForcesByBendingModes(coefficients)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 1)
        result, data = m1m3.GetEventAppliedAberrationForces()
        zForces = CalculateBendingModeForces(coefficients)
        for i in range(156):
            InTolerance("AppliedAberrationForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        coefficients = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        m1m3.ApplyAberrationForcesByBendingModes(coefficients)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 1)
        result, data = m1m3.GetEventAppliedAberrationForces()
        zForces = CalculateBendingModeForces(coefficients)
        for i in range(156):
            InTolerance("AppliedAberrationForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        m1m3.ClearAberrationForces()
        result, data = m1m3.GetEventForceActuatorState()
        Equal("AberrationForcesApplied", data.AberrationForcesApplied, 0)
        result, data = m1m3.GetEventAppliedAberrationForces()
        for i in range(156):
            InTolerance("AppliedAberrationForce.ZForces[%d]" % (i), data.ZForces[i], 0.0, 0.001)
        
    def CheckAccelerationForces(self, m1m3, sim):
        SubHeader("Acceleration Forces")
        
    def CheckActiveOpticForces(self, m1m3, sim):
        SubHeader("Active Optic Forces")
        zForces = []
        for i in range(156):
            zForces.append(i)
        m1m3.ApplyActiveOpticForces(zForces)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 1)
        result, data = m1m3.GetEventAppliedActiveOpticForces()
        for i in range(156):
            InTolerance("AppliedActiveOpticForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        coefficients = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        m1m3.ApplyActiveOpticForcesByBendingModes(coefficients)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 1)
        result, data = m1m3.GetEventAppliedActiveOpticForces()
        zForces = CalculateBendingModeForces(coefficients)
        for i in range(156):
            InTolerance("AppliedActiveOpticForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        coefficients = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        m1m3.ApplyActiveOpticForcesByBendingModes(coefficients)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 1)
        result, data = m1m3.GetEventAppliedActiveOpticForces()
        zForces = CalculateBendingModeForces(coefficients)
        for i in range(156):
            InTolerance("AppliedActiveOpticForce.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        m1m3.ClearActiveOpticForces()
        result, data = m1m3.GetEventForceActuatorState()
        Equal("ActiveOpticForcesApplied", data.ActiveOpticForcesApplied, 0)
        result, data = m1m3.GetEventAppliedActiveOpticForces()
        for i in range(156):
            InTolerance("AppliedActiveOpticForce.ZForces[%d]" % (i), data.ZForces[i], 0.0, 0.001)
        
    def CheckAzimuthForces(self, m1m3, sim):
        SubHeader("Azimuth Forces")
        
    def CheckBalanceForces(self, m1m3, sim):
        SubHeader("Balance Forces")
        
    def CheckElevationForces(self, m1m3, sim):
        SubHeader("Elevation Forces")
        
    def CheckOffsetForces(self, m1m3, sim):
        SubHeader("Offset Forces")
        xForces = []
        for i in range(12):
            xForces.append(float("1.%d" % i))
        yForces = []
        for i in range(100):
            yForces.append(float("2.%d" % i))
        zForces = []
        for i in range(156):
            zForces.append(float("3.%d" % i))
        m1m3.ApplyOffsetForces(xForces, yForces, zForces)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 1)
        result, data = m1m3.GetEventAppliedOffsetForces()
        for i in range(12):
            InTolerance("AppliedOffsetForces.XForces[%d]" % (i), data.XForces[i], xForces[i], 0.001)
        for i in range(100):
            InTolerance("AppliedOffsetForces.YForces[%d]" % (i), data.YForces[i], yForces[i], 0.001)
        for i in range(156):
            InTolerance("AppliedOffsetForces.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        fx = 10.0
        fy = 20.0
        fz = 30.0
        mx = 40.0
        my = 50.0
        mz = 60.0        
        m1m3.ApplyOffsetForcesByMirrorForce(fx, fy, fz, mx, my, mz)
        result, data = m1m3.GetEventForceActuatorState()
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 1)
        result, data = m1m3.GetEventAppliedOffsetForces()
        xForces, yForces, zForces = CalculateDistributionForces(fx, fy, fz, mx, my, mz)
        for i in range(12):
            InTolerance("AppliedOffsetForces.XForces[%d]" % (i), data.XForces[i], xForces[forceActuatorZIndexFromXIndex[i]], 0.001)
        for i in range(100):
            InTolerance("AppliedOffsetForces.YForces[%d]" % (i), data.YForces[i], yForces[forceActuatorZIndexFromYIndex[i]], 0.001)
        for i in range(156):
            InTolerance("AppliedOffsetForces.ZForces[%d]" % (i), data.ZForces[i], zForces[i], 0.001)
        m1m3.ClearOffsetForces()
        result, data = m1m3.GetEventForceActuatorState()
        Equal("OffsetForcesApplied", data.OffsetForcesApplied, 0)
        result, data = m1m3.GetEventAppliedOffsetForces()
        for i in range(12):
            InTolerance("AppliedOffsetForces.XForces[%d]" % (i), data.XForces[i], 0, 0.001)
        for i in range(100):
            InTolerance("AppliedOffsetForces.YForces[%d]" % (i), data.YForces[i], 0, 0.001)
        for i in range(156):
            InTolerance("AppliedOffsetForces.ZForces[%d]" % (i), data.ZForces[i], 0, 0.001)
        
    def CheckStaticForces(self, m1m3, sim):
        SubHeader("Static Forces")
        
    def CheckThermalForces(self, m1m3, sim):
        SubHeader("Thermal Forces")
        
    def CheckVelocityForces(self, m1m3, sim):
        SubHeader("Velocity Forces")