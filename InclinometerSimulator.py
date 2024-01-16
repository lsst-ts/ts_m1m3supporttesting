import binascii
import struct

from Simulator import Simulator

"""
This class simulates responses from the Inclinometer.  Returns a byte array 
for each response possible.

AWC 4 October 2017
"""


class InclinometerSimulator(Simulator):
    # since there is only one response from the Inclinometer
    # these values are pretty much constant.
    SERVER_ADDRESS = 127
    FUNCTION_CODE = 3
    DATA_LENGTH = 4

    def __init__(self):
        pass

    ###############################################################################
    # inclinometerResponse
    def inclinometerResponse(self, degreesMeasured):
        if degreesMeasured < 0.0 or degreesMeasured >= 360.0:
            raise Exception(
                "degreesMeasured is outside the valid range of values [0.0, 360.0)"
            )

        response = bytearray()
        self.dataCheck(self.SERVER_ADDRESS, "Server Address", response)
        self.dataCheck(self.FUNCTION_CODE, "Function Code", response)
        self.dataCheck(self.DATA_LENGTH, "Response Byte Count", response)

        # the inclinometer switches the bytes around, such that the MSB is the 3rd one.
        millidegreesMeasured = int(degreesMeasured * 1000)
        degreeBytes = millidegreesMeasured.to_bytes(4, byteorder="big", signed=False)
        # degreeBytes = self.floatToBytes(millidegreesMeasured, 'Millidegrees Measured', 4)
        degreeBytes = [degreeBytes[2], degreeBytes[3], degreeBytes[0], degreeBytes[1]]
        response.extend(degreeBytes)

        self.calculateCRC(response)

        response[:0] = bytes([len(response)])

        return response


###############################################################################
# main - for testing
def main():
    inclinSim = InclinometerSimulator()

    response = inclinSim.inclinometerResponse(36.001)
    assert bytes([9, 127, 3, 4, 140, 161, 00, 00, 0x1F, 0x46]) == response
    print("Inclinometer Response: " + str(binascii.hexlify(response)))


###############################################################################
# main()
