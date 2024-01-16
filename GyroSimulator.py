import binascii
import struct

from Simulator import Simulator

"""
This class sends the user data to the cRIO which will load the data into the FPGA which will
simulate  responses from the Gyro. It returns a byte array for each response possible.

AWC 22 January 2018
"""


class GyroSimulator(Simulator):
    def __init__(self):
        pass

    def loadData(
        self,
        xValue: float,
        yValue: float,
        zValue: float,
        status: int,
        gyroTemperature: int,
    ):
        response = bytearray()

        self.dataCheck(0xFE81FF55, "Header", response, 4, False)
        self.dataCheck(float(xValue), "X Value", response, 4)
        self.dataCheck(float(yValue), "Y Value", response, 4)
        self.dataCheck(float(zValue), "Z Value", response, 4)
        self.dataCheck(0x80000000, "Reserved", response, 4, False)
        self.dataCheck(0x80000000, "Reserved", response, 4, False)
        self.dataCheck(0x80000000, "Reserved", response, 4, False)
        self.dataCheck(status, "Status", response, 1, False)
        self.dataCheck(0x00, "Sequence", response, 1, False)
        self.dataCheck(gyroTemperature, "Gyro Temperature", response, 2)

        response[:0] = bytes([len(response)])

        return response


##########################################################################################################
# For Testing
def main():
    gyros = GyroSimulator()

    # test loadData
    response = gyros.loadData(1, 2, 3, 4, 5)
    ordArray = [c for c in response]
    print(ordArray)
    assert (
        bytes(
            [
                32,
                255,
                129,
                255,
                85,
                63,
                128,
                0,
                0,
                64,
                0,
                0,
                0,
                64,
                64,
                0,
                0,
                128,
                0,
                0,
                0,
                128,
                0,
                0,
                0,
                128,
                0,
                0,
                0,
                4,
                0,
                0,
                5,
            ]
        )
        == response
    )
    print("loadData: " + str(binascii.hexlify(response)))


# main()
