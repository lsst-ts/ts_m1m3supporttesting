import binascii
import struct
from Simulator import Simulator

'''
This class simulates responses from the Inclinometer.  Returns a byte array 
for each response possible.

AWC 6 October 2017
'''
class DisplacementSimulator(Simulator):

    RESPONSE_BEGIN = "M0,"
    RESPONSE_END = "\r\n"
    DISPLACEMENT_FORMAT = "{num:+09.4f}"
    
    def __init__(self):
        pass

    ###############################################################################
    # displacementResponse
    def displacementResponse(self, displace1, displace2, displace3, displace4, displace5, displace6, displace7, displace8):
        if displace1 < -999.9999 or displace1 > 999.9999:
            raise Exception("displace1 is outside the valid range of values [-999.9999, +999.9999]")
        if displace2 < -999.9999 or displace2 > 999.9999:
            raise Exception("displace2 is outside the valid range of values [-999.9999, +999.9999]")
        if displace3 < -999.9999 or displace3 > 999.9999:
            raise Exception("displace3 is outside the valid range of values [-999.9999, +999.9999]")
        if displace4 < -999.9999 or displace4 > 999.9999:
            raise Exception("displace4 is outside the valid range of values [-999.9999, +999.9999]")
        if displace5 < -999.9999 or displace5 > 999.9999:
            raise Exception("displace5 is outside the valid range of values [-999.9999, +999.9999]")
        if displace6 < -999.9999 or displace6 > 999.9999:
            raise Exception("displace6 is outside the valid range of values [-999.9999, +999.9999]")
        if displace7 < -999.9999 or displace7 > 999.9999:
            raise Exception("displace7 is outside the valid range of values [-999.9999, +999.9999]")
        if displace8 < -999.9999 or displace8 > 999.9999:
            raise Exception("displace8 is outside the valid range of values [-999.9999, +999.9999]")

        displaceArray = [self.DISPLACEMENT_FORMAT.format(num=displace1),
                         self.DISPLACEMENT_FORMAT.format(num=displace2),
                         self.DISPLACEMENT_FORMAT.format(num=displace3),
                         self.DISPLACEMENT_FORMAT.format(num=displace4),
                         self.DISPLACEMENT_FORMAT.format(num=displace5),
                         self.DISPLACEMENT_FORMAT.format(num=displace6),
                         self.DISPLACEMENT_FORMAT.format(num=displace7),
                         self.DISPLACEMENT_FORMAT.format(num=displace8)]
        responseString = self.RESPONSE_BEGIN + ",".join(displaceArray) + self.RESPONSE_END
        responseLength = len(responseString)
        
        response = bytearray()
        self.dataCheck(responseString, 'Displacement Response', response, responseLength)
        
        response[:0] = bytes([len(response)])

        return response

###############################################################################
# main - for testing
def main():
    displaceSim = DisplacementSimulator()

    response = displaceSim.displacementResponse(-19.7297, 4.8019, 6.0861, 4.2432, 5.0091, 5.3213, 2.0120, 11.0113)
    ordArray = [c for c in response]
    print(ordArray)
    assert(bytes([76, 77, 48, 44, 45, 48, 49, 57, 46, 55, 51, 48, 44, 43, 48, 48, 52, 46, 56, 48, 50, 44, 43, 48, 48, 54, 46, 48, 56, 54, 44, 43, 48, 48, 52, 46, 50, 52, 51, 44, 43, 48, 48, 53, 46, 48, 48, 57, 44, 43, 48, 48, 53, 46, 51, 50, 49, 44, 43, 48, 48, 50, 46, 48, 49, 50, 44, 43, 48, 49, 49, 46, 48, 49, 49, 13, 10]) == response)
    print("Inclinometer Response: " + str(binascii.hexlify(response)))
    print(response)

###############################################################################
#main()

