import binascii
import struct
from Simulator import Simulator

'''
This class simulates responses from four Accelerometer.  Returns a byte array 
for each response possible.

AWC 6 October 2017
'''
class AccelSimulator(Simulator):

    
    def __init__(self):
        pass

    ###############################################################################
    # accelerometerResponse
    def accelerometerResponse(self, accelerometerNumber, elevationVoltage, azimuthVoltage):
        response = bytearray()
        if (1 > accelerometerNumber or 4 < accelerometerNumber):
            raise Exception("There are only 4 accelerometers (1-4), you chose number: " + str(accelerometerNumber))
        self.dataCheck(accelerometerNumber, 'Accelrometer Number', response)
        self.dataCheck(elevationVoltage, 'Elevation Voltage', response, 4)
        self.dataCheck(azimuthVoltage, 'Azimuth Voltage', response, 4)
        response[:0] = bytes([len(response)])
        return response

###############################################################################
# main - for testing
def main():
    accelSim = AccelSimulator()
    response = accelSim.accelerometerResponse(1, 2.3)

#    ordArray = [c for c in response]
#    print(ordArray)
    assert(bytes([1, 64, 19, 51, 51]) == response)
    print("Accelerometer Response: " + str(binascii.hexlify(response)))
    

###############################################################################
#main()
