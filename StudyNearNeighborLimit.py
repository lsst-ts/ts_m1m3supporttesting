import math

from CalculateBendingModeForces import *
from CalculateElevationForces import *
from ForceActuatorTable import *

nearNeighbors = {
    101: [102, 107, 108, 407, 408],
    102: [101, 103, 108, 109, 408, 409],
    103: [102, 104, 109, 110, 409, 410],
    104: [103, 105, 110, 111, 410, 411],
    105: [104, 106, 111, 112, 411, 412],
    106: [105, 112, 412],
    107: [101, 102, 108, 113, 114, 207],
    108: [101, 102, 107, 109, 114, 115],
    109: [102, 103, 108, 110, 115, 116],
    110: [103, 104, 109, 111, 116, 117],
    111: [104, 105, 110, 112, 117, 118],
    112: [105, 106, 111, 118, 119],
    113: [107, 114, 120, 207, 214, 220],
    114: [107, 108, 113, 115, 120, 121],
    115: [108, 109, 114, 116, 121, 122],
    116: [109, 110, 115, 117, 122, 123],
    117: [110, 111, 116, 118, 123, 124],
    118: [111, 112, 119, 117, 124, 125],
    119: [112, 118, 125],
    120: [113, 114, 121, 126, 127, 220],
    121: [114, 115, 120, 122, 127, 128],
    122: [115, 116, 121, 123, 128, 129],
    123: [116, 117, 122, 124, 129, 130],
    124: [117, 118, 123, 125, 130, 131],
    125: [118, 119, 124, 131],
    126: [120, 127, 132, 220, 227, 232],
    127: [120, 121, 126, 128, 132, 133],
    128: [121, 122, 127, 129, 133, 134],
    129: [122, 123, 128, 130, 134, 135],
    130: [123, 124, 129, 131, 135, 136],
    131: [124, 125, 130, 136],
    132: [126, 127, 133, 137, 138, 232],
    133: [127, 128, 132, 134, 138, 139],
    134: [128, 129, 133, 135, 139, 140],
    135: [129, 130, 134, 136, 140],
    136: [130, 131, 135],
    137: [132, 138, 141, 232, 237, 241],
    138: [132, 133, 137, 138, 141, 142],
    139: [133, 134, 138, 140, 142, 143],
    140: [134, 135, 139, 143],
    141: [137, 138, 142, 241],
    142: [138, 139, 141, 143],
    143: [138, 139, 140, 142],
}


def FindIndex(id):
    for row in forceActuatorTable:
        if row[forceActuatorTableIDIndex] == id:
            return row[forceActuatorTableIndexIndex]
    return -1


def AvgGlobalForce(x, y, z):
    totalX = 0.0
    totalY = 0.0
    totalZ = 0.0
    for i in range(156):
        if i < 12:
            totalX += x[i]
        if i < 100:
            totalY += y[i]
        totalZ += z[i]
    totalF = math.sqrt(totalX * totalX + totalY * totalY + totalZ * totalZ)
    avgF = totalF / 156
    return avgF


def Add(a, b):
    y = []
    for i in range(len(a)):
        y.append(a[i] + b[i])
    return y


def CalculateNearNeighbor(id, x, y, z):
    neighbors = nearNeighbors[id]
    testI = FindIndex(id)
    testRow = forceActuatorTable[testI]
    testX = x[testI]
    testY = y[testI]
    testZ = z[testI]
    nX = 0.0
    nY = 0.0
    nZ = 0.0
    for n in neighbors:
        nI = FindIndex(n)
        nX += x[nI]
        nY += y[nI]
        nZ += z[nI]
    avgX = nX / len(neighbors)
    avgY = nY / len(neighbors)
    avgZ = nZ / len(neighbors)
    dX = testX - avgX
    dY = testY - avgY
    dZ = testZ - avgZ
    mag = math.sqrt(dX * dX + dY * dY + dZ * dZ)
    return mag


a = 60.0
s = 1.2
x, y, z = CalculateElevationForces(a)
c = [0.0] * 22
c[0] = 0.0
c[1] = 0.0
c[2] = 0.0
c[3] = 0.0
c[4] = 0.5
z = Add(z, CalculateBendingModeForces(c))
avg = AvgGlobalForce(x, y, z)
print("Elevation: %0.3f" % a)
print("BendingModes: %s" % c)
print("Scale: %0.3f" % s)
print("AvgGlobalForce: %0.4f" % (avg))
for key in nearNeighbors:
    v = CalculateNearNeighbor(key, x, y, z)
    print("%d\t%10.4f\t%s\t%10.4f" % (key, v, v > (avg * s), v - (avg * s)))
# actId = 102
# i = FindIndex(actId)
# x[i] = 0.0
# y[i] = 0.0
# z[i] = -80.0
#
# tX = x[i]
# tY = y[i]
# tZ = z[i]
# tM = math.sqrt(tX * tX + tY * tY + tZ * tZ)
# print("%d%15.4f%15.4f%15.4f%15.4f" % (actId, tX, tY, tZ, tM))
# nX = 0.0
# nY = 0.0
# nZ = 0.0
# for n in nearNeighbors[actId]:
#    i = FindIndex(n)
#    nX += x[i]
#    nY += y[i]
#    nZ += z[i]
#    print("%d%15.4f%15.4f%15.4f%15.4f" % (n, x[i], y[i], z[i], math.sqrt(x[i] * x[i] + y[i] * y[i] + z[i] * z[i])))
# print("%d%15.4f%15.4f%15.4f%15.4f" % (999, nX, nY, nZ, math.sqrt(nX * nX + nY * nY + nZ * nZ)))
# count = len(nearNeighbors[actId])
# print("%d%15.4f%15.4f%15.4f%15.4f" % (999, nX / count, nY / count, nZ / count, math.sqrt(nX * nX + nY * nY + nZ * nZ) / count))
