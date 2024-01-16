import binascii
import struct

from Simulator import Simulator

"""
This class simulates commands issued from the various Digital Outputs.  
Prints output for each command

AWC 8 November 2017
"""


class DigitalOutputSimulator(Simulator):
    def __init__(self):
        pass

    def createResponse(self, cRioPortNum: int, stringRepresentation: str):
        response = bytearray()
        self.dataCheck(cRioPortNum, stringRepresentation, response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # heartBeatSafetyController
    def requestHeartBeatSafetyController(self):
        return self.createResponse(60, "Request Heart Beat Safety Controller")

    def heartBeatSafetyController(self, messageOutput):
        print("The Heart Beat Safety Controller states " + messageOutput)

    ###############################################################################
    # criticalFaultSafetyController
    def requestCriticalFaultSafetyController(self):
        return self.createResponse(61, "Request Critical Fault Safety Controller")

    def criticalFaultSafetyController(self, messageOutput: str):
        print("The Critical Fault Safety Controller states " + messageOutput)

    ###############################################################################
    # mirrorLowerRaisingToSafetyController
    def requestMirrorLowerRaisingToSafetyController(self):
        return self.createResponse(
            62, "Request Mirror Lower Raising To Safety Controller"
        )

    def mirrorLowerRaisingToSafetyController(self, messageOutput: str):
        print("The Mirror Lower Rasigin To Safety Controller states " + messageOutput)

    ###############################################################################
    # mirrorParkedToSafetyController
    def requestMirrorParkedToSafetyController(self):
        return self.createResponse(63, "Request Mirror Parked To Safety Controller")

    def mirrorParkedToSafetyController(self, messageOutput: str):
        print("The Mirror Parked To Safety Controller states " + messageOutput)

    ###############################################################################
    # airSupplyControlValve
    def requestAirSupplyControlValve(self):
        return self.createResponse(64, "Request Air Supply Control Valve")

    def airSupplyControlValve(self, messageOutput: str):
        print("The Air Supply Control Valve states " + messageOutput)

    ###############################################################################
    # mirrorCellLightsRemoteControl
    def requestMirrorCellLightsRemoteControl(self):
        return self.createResponse(65, "Request Mirror Cell Light Remote Control")

    def mirrorCellLightsRemoteControl(self, messageOutput: str):
        print("The Mirror Cell Lights Remote Control states " + messageOutput)

    ###############################################################################
    # auxPowerNetworkAOn
    def requestAuxPowerNetworkAOn(self):
        return self.createResponse(70, "Request Auxiliary Power Network A On")

    def auxPowerNetworkAOn(self, messageOutput: str):
        print("The Auxiliary Power Network A On states " + messageOutput)

    ###############################################################################
    # auxPowerNetworkBOn
    def requestAuxPowerNetworkBOn(self):
        return self.createResponse(71, "Request Auxiliary Power Network B On")

    def auxPowerNetworkBOn(self, messageOutput: str):
        print("The Auxiliary Power Network B On states " + messageOutput)

    ###############################################################################
    # auxPowerNetworkCOn
    def requestAuxPowerNetworkCOn(self):
        return self.createResponse(72, "Request Auxiliary Power Network C On")

    def auxPowerNetworkCOn(self, messageOutput: str):
        print("The Auxiliary Power Network C On states " + messageOutput)

    ###############################################################################
    # auxPowerNetworkDOn
    def requestAuxPowerNetworkDOn(self):
        return self.createResponse(73, "Request Auxiliary Power Network D On")

    def auxPowerNetworkDOn(self, messageOutput: str):
        print("The Auxiliary Power Network D On states " + messageOutput)

    ###############################################################################
    # powerNetworkAOn
    def requestPowerNetworkAOn(self):
        return self.createResponse(74, "Request Power Network A On")

    def powerNetworkAOn(self, messageOutput: str):
        print("The Power Network A On states " + messageOutput)

    ###############################################################################
    # powerNetworkBOn
    def requestPowerNetworkBOn(self):
        return self.createResponse(75, "Request Power Network B On")

    def powerNetworkBOn(self, messageOutput: str):
        print("The Power Network B On states " + messageOutput)

    ###############################################################################
    # powerNetworkCOn
    def requestPowerNetworkCOn(self):
        return self.createResponse(76, "Request Power Network C On")

    def powerNetworkCOn(self, messageOutput: str):
        print("The Power Network C On states " + messageOutput)

    ###############################################################################
    # powerNetworkDOn
    def requestPowerNetworkDOn(self):
        return self.createResponse(77, "Request Power Network D On")

    def powerNetworkDOn(self, messageOutput: str):
        print("The Power Network D On states " + messageOutput)

    ###############################################################################
    # function calls for return data
    functionCalls = {
        "60": heartBeatSafetyController,
        "61": criticalFaultSafetyController,
        "62": mirrorLowerRaisingToSafetyController,
        "63": mirrorParkedToSafetyController,
        "64": airSupplyControlValve,
        "65": mirrorCellLightsRemoteControl,
        "70": auxPowerNetworkAOn,
        "71": auxPowerNetworkBOn,
        "72": auxPowerNetworkCOn,
        "73": auxPowerNetworkDOn,
        "74": powerNetworkAOn,
        "75": powerNetworkBOn,
        "76": powerNetworkCOn,
        "77": powerNetworkDOn,
    }

    ###############################################################################
    # This is where we receive and parse the response from labview.
    def receiveOutput(self, message: str):
        messageType = message[0:2]
        messageValue = message[2:]
        print(
            "receive output: "
            + message
            + " type: "
            + messageType
            + " data: "
            + messageValue
        )
        self.functionCalls[messageType](self, messageValue)


###############################################################################
# main
def main():
    DOSim = DigitalOutputSimulator()


main()
