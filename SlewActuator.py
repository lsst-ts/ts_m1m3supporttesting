########################################################################
# Test Numbers: N/A
# Author:       CContaxis
# Description:  Slew an actuator like the test stand
# Steps:
# - Sample data before and after application of a mirror force
########################################################################

import math
import time

from SALPY_m1m3 import *
from SALPY_vms import *

from ForceActuatorTable import *
from HardpointActuatorTable import *
from Setup import *
from Utilities import *

actuatorZIndex = 1
actuatorYIndex = 0

testTable = [
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 739, 984],
    [0, 787, 996],
    [0, 835, 1008],
    [0, 883, 1020],
    [0, 931, 1032],
    [0, 979, 1044],
    [0, 1027, 1056],
    [0, 1075, 1068],
    [0, 1123, 1080],
    [0, 1171, 1092],
    [0, 1219, 1104],
    [0, 1267, 1116],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1291, 1122],
    [0, 1243, 1110],
    [0, 1195, 1098],
    [0, 1147, 1086],
    [0, 1099, 1074],
    [0, 1051, 1062],
    [0, 1003, 1050],
    [0, 955, 1038],
    [0, 907, 1026],
    [0, 859, 1014],
    [0, 811, 1002],
    [0, 763, 990],
    [0, 715, 978],
    [0, 667, 966],
    [0, 619, 954],
    [0, 571, 942],
    [0, 523, 930],
    [0, 475, 918],
    [0, 427, 906],
    [0, 379, 894],
    [0, 331, 882],
    [0, 283, 870],
    [0, 235, 858],
    [0, 187, 846],
    [0, 139, 834],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 91, 822],
    [0, 139, 834],
    [0, 187, 846],
    [0, 235, 858],
    [0, 283, 870],
    [0, 331, 882],
    [0, 379, 894],
    [0, 427, 906],
    [0, 475, 918],
    [0, 523, 930],
    [0, 571, 942],
    [0, 619, 954],
    [0, 667, 966],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
    [0, 691, 972],
]

TEST_HOLD_TIME = 5.0
TEST_SCALER = 1.0

X1Sensitivity = 51.459
Y1Sensitivity = 52.061
Z1Sensitivity = 51.298

X2Sensitivity = 51.937
Y2Sensitivity = 52.239
Z2Sensitivity = 52.130

X3Sensitivity = 52.183
Y3Sensitivity = 52.015
Z3Sensitivity = 51.908


def convert(raw, sensitivity):
    return (raw * 1000.0) / sensitivity


class ForceBalanceSystemCheckProfile:
    def Run(self, m1m3, sim, efd):
        Header("Force balance system check profile")

        # Setup VMS
        vms = SAL_vms()
        vms.salTelemetrySub("vms_M1M3")

        # Get start time of this test
        result, data = m1m3.GetSampleHardpointActuatorData()
        startTimestamp = data.Timestamp
        realStart = startTimestamp
        result, data = m1m3.GetSampleIMSData()
        vmsData = vms_M1M3C()
        result = vms.getSample_M1M3(vmsData)
        result, data = m1m3.GetSampleForceActuatorData()

        # Write header
        hpOutput = "Timestamp,RelativeTimestamp,SFx,SFy,SFz,SMx,SMy,SMz,HP1,HP2,HP3,HP4,HP5,HP6,Fx,Fy,Fz,Mx,My,Mz\r\n"
        imsOutput = (
            "Timestamp,XPosition,YPosition,ZPosition,XRotation,YRotation,ZRotation\r\n"
        )
        vmsOutput = "Timestamp (s),X1 (m/s^2),Y1 (m/s^2),Z1 (m/s^2),X2 (m/s^2),Y2 (m/s^2),Z2 (m/s^2),X3 (m/s^2),Y3 (m/s^2),Z3 (m/s^2)\r\n"
        faOutput = "Timestamp,XSetpoint,YSetpoint,ZSetpoint,XActual,YActual,ZActual\r\n"

        # Wait hold time
        while (data.Timestamp - startTimestamp) < TEST_HOLD_TIME:
            # Sample data
            rtn, data = m1m3.GetNextSampleHardpointActuatorData()
            if rtn >= 0:
                hpOutput = hpOutput + (
                    "%0.6f,%0.6f,0.0,0.0,0.0,0.0,0.0,0.0,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n"
                    % (
                        data.Timestamp,
                        (data.Timestamp - realStart),
                        data.MeasuredForce[0],
                        data.MeasuredForce[1],
                        data.MeasuredForce[2],
                        data.MeasuredForce[3],
                        data.MeasuredForce[4],
                        data.MeasuredForce[5],
                        data.Fx,
                        data.Fy,
                        data.Fz,
                        data.Mx,
                        data.My,
                        data.Mz,
                    )
                )

            rtn, imsData = m1m3.GetNextSampleIMSData()
            if rtn >= 0:
                imsOutput = imsOutput + (
                    "%0.6f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f\r\n"
                    % (
                        imsData.Timestamp,
                        imsData.XPosition,
                        imsData.YPosition,
                        imsData.ZPosition,
                        imsData.XRotation,
                        imsData.YRotation,
                        imsData.ZRotation,
                    )
                )

            vmsData = vms_M1M3C()
            result = vms.getNextSample_M1M3(vmsData)
            if result >= 0:
                newTimestamp = vmsData.Timestamp
                for j in range(50):
                    vmsOutput = vmsOutput + (
                        "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n"
                        % (
                            newTimestamp,
                            convert(vmsData.Sensor1XAcceleration[j], X1Sensitivity),
                            convert(vmsData.Sensor1YAcceleration[j], Y1Sensitivity),
                            convert(vmsData.Sensor1ZAcceleration[j], Z1Sensitivity),
                            convert(vmsData.Sensor2XAcceleration[j], X2Sensitivity),
                            convert(vmsData.Sensor2YAcceleration[j], Y2Sensitivity),
                            convert(vmsData.Sensor2ZAcceleration[j], Z2Sensitivity),
                            convert(vmsData.Sensor3XAcceleration[j], X3Sensitivity),
                            convert(vmsData.Sensor3YAcceleration[j], Y3Sensitivity),
                            convert(vmsData.Sensor3ZAcceleration[j], Z3Sensitivity),
                        )
                    )
                    newTimestamp += 0.001

            rtn, faData = m1m3.GetNextSampleForceActuatorData()
            if rtn >= 0:
                faOutput = faOutput + (
                    "%0.6f,0,691,972,0,%0.3f,%0.3f\r\n"
                    % (
                        faData.Timestamp,
                        faData.YForce[actuatorYIndex],
                        faData.ZForce[actuatorZIndex],
                    )
                )

        xForces = [0] * 12
        yForces = [0] * 100
        zForces = [0] * 156
        zForces[0] = 972
        zForces[1] = 972
        zForces[2] = 972
        zForces[7] = 972
        zForces[8] = 972
        zForces[122] = 972
        zForces[123] = 972

        # Run profile
        for record in testTable:
            # Wait for sample
            while True:
                rtn, data = m1m3.GetNextSampleHardpointActuatorData()
                if rtn >= 0:
                    break

            yForces[actuatorYIndex] = record[1]
            zForces[actuatorZIndex] = record[2]

            # Command new offset
            m1m3.ApplyOffsetForces(xForces, yForces, zForces, False)

            # Append data to file
            hpOutput = hpOutput + (
                "%0.6f,%0.6f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n"
                % (
                    data.Timestamp,
                    (data.Timestamp - realStart),
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    data.MeasuredForce[0],
                    data.MeasuredForce[1],
                    data.MeasuredForce[2],
                    data.MeasuredForce[3],
                    data.MeasuredForce[4],
                    data.MeasuredForce[5],
                    data.Fx,
                    data.Fy,
                    data.Fz,
                    data.Mx,
                    data.My,
                    data.Mz,
                )
            )

            rtn, imsData = m1m3.GetNextSampleIMSData()
            if rtn >= 0:
                imsOutput = imsOutput + (
                    "%0.6f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f\r\n"
                    % (
                        imsData.Timestamp,
                        imsData.XPosition,
                        imsData.YPosition,
                        imsData.ZPosition,
                        imsData.XRotation,
                        imsData.YRotation,
                        imsData.ZRotation,
                    )
                )

            vmsData = vms_M1M3C()
            result = vms.getNextSample_M1M3(vmsData)
            if result >= 0:
                newTimestamp = vmsData.Timestamp
                for j in range(50):
                    vmsOutput = vmsOutput + (
                        "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n"
                        % (
                            newTimestamp,
                            convert(vmsData.Sensor1XAcceleration[j], X1Sensitivity),
                            convert(vmsData.Sensor1YAcceleration[j], Y1Sensitivity),
                            convert(vmsData.Sensor1ZAcceleration[j], Z1Sensitivity),
                            convert(vmsData.Sensor2XAcceleration[j], X2Sensitivity),
                            convert(vmsData.Sensor2YAcceleration[j], Y2Sensitivity),
                            convert(vmsData.Sensor2ZAcceleration[j], Z2Sensitivity),
                            convert(vmsData.Sensor3XAcceleration[j], X3Sensitivity),
                            convert(vmsData.Sensor3YAcceleration[j], Y3Sensitivity),
                            convert(vmsData.Sensor3ZAcceleration[j], Z3Sensitivity),
                        )
                    )
                    newTimestamp += 0.001

            rtn, faData = m1m3.GetNextSampleForceActuatorData()
            if rtn >= 0:
                faOutput = faOutput + (
                    "%0.6f,0,%0.3f,%0.3f,0,%0.3f,%0.3f\r\n"
                    % (
                        faData.Timestamp,
                        record[1],
                        record[2],
                        faData.YForce[actuatorYIndex],
                        faData.ZForce[actuatorZIndex],
                    )
                )

        # Wait hold time
        startTimestamp = data.Timestamp
        while (data.Timestamp - startTimestamp) < TEST_HOLD_TIME:
            # Sample data
            rtn, data = m1m3.GetNextSampleHardpointActuatorData()
            if rtn >= 0:
                hpOutput = hpOutput + (
                    "%0.6f,%0.6f,0.0,0.0,0.0,0.0,0.0,0.0,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f\r\n"
                    % (
                        data.Timestamp,
                        (data.Timestamp - realStart),
                        data.MeasuredForce[0],
                        data.MeasuredForce[1],
                        data.MeasuredForce[2],
                        data.MeasuredForce[3],
                        data.MeasuredForce[4],
                        data.MeasuredForce[5],
                        data.Fx,
                        data.Fy,
                        data.Fz,
                        data.Mx,
                        data.My,
                        data.Mz,
                    )
                )

            rtn, imsData = m1m3.GetNextSampleIMSData()
            if rtn >= 0:
                imsOutput = imsOutput + (
                    "%0.6f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f,%0.12f\r\n"
                    % (
                        imsData.Timestamp,
                        imsData.XPosition,
                        imsData.YPosition,
                        imsData.ZPosition,
                        imsData.XRotation,
                        imsData.YRotation,
                        imsData.ZRotation,
                    )
                )

            vmsData = vms_M1M3C()
            result = vms.getNextSample_M1M3(vmsData)
            if result >= 0:
                newTimestamp = vmsData.Timestamp
                for j in range(50):
                    vmsOutput = vmsOutput + (
                        "%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n"
                        % (
                            newTimestamp,
                            convert(vmsData.Sensor1XAcceleration[j], X1Sensitivity),
                            convert(vmsData.Sensor1YAcceleration[j], Y1Sensitivity),
                            convert(vmsData.Sensor1ZAcceleration[j], Z1Sensitivity),
                            convert(vmsData.Sensor2XAcceleration[j], X2Sensitivity),
                            convert(vmsData.Sensor2YAcceleration[j], Y2Sensitivity),
                            convert(vmsData.Sensor2ZAcceleration[j], Z2Sensitivity),
                            convert(vmsData.Sensor3XAcceleration[j], X3Sensitivity),
                            convert(vmsData.Sensor3YAcceleration[j], Y3Sensitivity),
                            convert(vmsData.Sensor3ZAcceleration[j], Z3Sensitivity),
                        )
                    )
                    newTimestamp += 0.001

            rtn, faData = m1m3.GetNextSampleForceActuatorData()
            if rtn >= 0:
                faOutput = faOutput + (
                    "%0.6f,0,692,972,0,%0.3f,%0.3f\r\n"
                    % (
                        faData.Timestamp,
                        faData.YForce[actuatorYIndex],
                        faData.ZForce[actuatorZIndex],
                    )
                )

        # Write the output file
        path = GetFilePath("%d-SlewActuator-HP.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write(hpOutput)
        file.close()

        path = GetFilePath("%d-SlewActuator-IMS.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write(imsOutput)
        file.close()

        path = GetFilePath("%d-SlewActuator-VMS.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write(vmsOutput)
        file.close()

        path = GetFilePath("%d-SlewActuator-FA.csv" % (int(startTimestamp)))
        Log("File path: %s" % path)
        file = open(path, "w+")
        file.write(faOutput)
        file.close()

        vms.salShutdown()


if __name__ == "__main__":
    m1m3, sim, efd = Setup()
    ForceBalanceSystemCheckProfile().Run(m1m3, sim, efd)
    Shutdown(m1m3, sim, efd)
