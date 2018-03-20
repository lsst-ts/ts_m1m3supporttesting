import M1M3
import CellSimulator
import VerifyStateChanges
import VerifyEFD

m1m3 = M1M3.M1M3()
sim = CellSimulator.CellSimulator("140.252.32.151", True)

VerifyStateChanges.VerifyStateChanges().Run(m1m3, sim)
#VerifyEFD.VerifyEFD().Run(m1m3, sim)
