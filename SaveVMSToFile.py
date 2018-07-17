from SALPY_vms import *

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

def SaveVMSToFile(file):
    print("Initializing SAL")
    vms = SAL_vms()
    vms.salTelemetrySub("vms_M1M3")
    print("Flushing SAL samples")
    data = vms_M1M3C()
    vms.getSample_M1M3(data)
    print("Logging to file")
    f = open(file, "w+")
    f.write("Timestamp (s),X1 (m/s^2),Y1 (m/s^2),Z1 (m/s^2),X2 (m/s^2),Y2 (m/s^2),Z2 (m/s^2),X3 (m/s^2),Y3 (m/s^2),Z3 (m/s^2)\r\n")
    startTime = -1
    while True:
        rtn = vms.getNextSample_M1M3(data)
        if rtn >= 0:
            timestamp = data.Timestamp
            if startTime == -1:
                startTime = timestamp
            for i in range(50):
                f.write("%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f,%0.6f\r\n" % (
                    timestamp, 
                    convert(data.Sensor1XAcceleration[i], X1Sensitivity),
                    convert(data.Sensor1YAcceleration[i], Y1Sensitivity),
                    convert(data.Sensor1ZAcceleration[i], Z1Sensitivity),
                    convert(data.Sensor2XAcceleration[i], X2Sensitivity),
                    convert(data.Sensor2YAcceleration[i], Y2Sensitivity),
                    convert(data.Sensor2ZAcceleration[i], Z2Sensitivity),
                    convert(data.Sensor3XAcceleration[i], X3Sensitivity),
                    convert(data.Sensor3YAcceleration[i], Y3Sensitivity),
                    convert(data.Sensor3ZAcceleration[i], Z3Sensitivity)))
                timestamp += 0.001
            print("Time: %0.1f" % (timestamp - startTime))

