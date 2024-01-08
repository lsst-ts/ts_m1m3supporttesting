import binascii

from Simulator import Simulator

"""
This class simulates responses from four Accelerometer. Returns a byte array
for each response possible.

AWC 6 October 2017
"""


class AccelSimulator(Simulator):
    def __init__(self) -> None:
        pass

    def accelerometerResponse(
        self, accelerometerNumber: int, elevationVoltage: float, azimuthVoltage: float
    ) -> bytearray:
        response = bytearray()
        if 1 > accelerometerNumber or 4 < accelerometerNumber:
            raise Exception(
                "There are only 4 accelerometers (1-4), you chose number: "
                + str(accelerometerNumber)
            )
        self.dataCheck(accelerometerNumber, "Accelrometer Number", response)
        self.dataCheck(elevationVoltage, "Elevation Voltage", response, 4)
        self.dataCheck(azimuthVoltage, "Azimuth Voltage", response, 4)
        response[:0] = bytes([len(response)])
        return response


def main() -> None:
    accelSim = AccelSimulator()
    response = accelSim.accelerometerResponse(1, 2.3, 2.2)

    assert (
        bytearray([0x09, 0x01, 0x40, 0x13, 0x33, 0x33, 0x40, 0x0C, 0xCC, 0xCD])
        == response
    )
    print("Accelerometer Response: " + str(binascii.hexlify(response)))


if __name__ == "__main__":
    main()
