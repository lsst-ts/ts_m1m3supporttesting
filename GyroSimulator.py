import binascii
import struct
from Simulator import Simulator

'''
This class sends the user data to the cRIO which will load the data into the FPGA which will
simulate  responses from the Gyro. It returns a byte array for each response possible.

AWC 22 January 2018
'''
class GyroSimulator(Simulator):

    def __init__(self):
        pass

    def loadData(self, xValue:float, yValue:float, zValue:float, isValid:bool, gyroTemperature:int):
        response = bytearray()

        self.dataCheck(xValue, 'X Value', response, 4)
        self.dataCheck(yValue, 'Y Value', response, 4)
        self.dataCheck(zValue, 'Z Value', response, 4)
        if isValid:
            # binary 00000111 - all valid, DSP 1760 manual, pg. 15 & Rev. B DSP 1760 External Electrical Signaling ICD pg.19
            self.dataCheck(7, 'Is Valid', response, 1, False) 
        else:
            self.dataCheck(0, 'Is Valid', response, 1, False) # binary 00000000 - all invalid, DSP 1760 manual, pg.15
        self.dataCheck(gyroTemperature, 'Gyro Temperature', response, 2)

        response[:0] = bytes([len(response)])
        
        return response


##########################################################################################################
# For Testing
def main():
    gyros = GyroSimulator()

    # test loadData
    response = gyros.loadData(12.34, 23.34, 34.45, 1, 24)
    ordArray = [c for c in response]
    print(ordArray)
    assert (bytes([15, 65, 69, 112, 164, 65, 186, 184, 82, 66, 9, 204, 205, 1, 0, 24]) == response)
    print("loadData: " + str(binascii.hexlify(response)))
#main()
