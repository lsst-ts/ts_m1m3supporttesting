import binascii
import struct

"""
This is the super class that simulates responses from the all the Simulators.

AWC 29 August 2017
"""


class Simulator:
    def __init__(self):
        pass

    ##########################################################################################################
    # This was pulled outside of dataCheck so it can be used by inclinometer simulator
    # as the inclinometer moves the bytes around.
    def floatToBytes(self, someData: float, parameterName: str, byteSize: int):
        floatBytes = struct.pack(">f", someData)
        if len(floatBytes) != byteSize:
            raise Exception(
                parameterName
                + " size does not match the byte size("
                + str(byteSize)
                + ") specified."
            )
        return floatBytes

    ##########################################################################################################
    # For each type of "someData", store it correctly in aBytesArray
    # parameterName is mainly for error message
    # byteSize is to make sure "someData" has the correct amount of bytes for the parameter
    def dataCheck(
        self,
        someData,
        parameterName: str,
        aByteArray: bytearray,
        byteSize: int = 1,
        intSigned: bool = True,
    ):
        # integer
        if isinstance(someData, int):
            aByteArray.extend(
                someData.to_bytes(byteSize, byteorder="big", signed=intSigned)
            )

        # string
        elif isinstance(someData, str):
            if len(someData) > byteSize:
                raise Exception(
                    parameterName
                    + " is too large: "
                    + str(len(someData))
                    + ", it can only be a maximum of "
                    + str(byteSize)
                )
            aByteArray.extend(someData.encode("ascii"))
            if len(someData) < byteSize:
                bufferArray = bytearray(byteSize - len(someData))
                aByteArray.extend(bufferArray)

        # float
        elif isinstance(someData, float):
            floatBytes = self.floatToBytes(someData, parameterName, byteSize)
            aByteArray.extend(floatBytes)

        # if we are here, we have recieved an unrecognized type
        else:
            raise Exception(
                parameterName
                + " has a type that we are unable to process.  Throwing exception"
            )

    ##########################################################################################################
    # Computing the 16-bit CRC value of data
    def calculateCRC(self, aByteArray):
        crc = int("FFFF", 16)
        for aByte in aByteArray:
            crc = crc ^ aByte  # XOR
            for i in range(1, 9):
                crcShift = crc >> 1
                if (crc & 1) != 0:
                    crc = crcShift ^ int("A001", 16)
                else:
                    crc = crcShift
        aByteArray.extend(crc.to_bytes(2, byteorder="little"))
        return crc
