import binascii
import struct
from Simulator import Simulator

'''
This class simulates commands issued to the various Digital Inputs.  Returns a byte array 
for each response possible.

AWC 8 November 2017
'''
class DigitalInputSimulator(Simulator):

    
    def __init__(self):
        pass

    ###############################################################################
    # powerNetworkShutDown
    def powerNetworkShutDown(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Power Network Shut Down can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(0, 'Power Network Shut Down Number', response)
        self.dataCheck(command, 'Power Network Shut Down Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # fansHeatersPumpPoweredOff
    def fansHeatersPumpPoweredOff(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Fan Coils/Heaters/Pump Powered Off can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(1, 'Fan Coils/Heaters/Pump Powered Off Number', response)
        self.dataCheck(command, 'Fan Coils/Heaters/Pump Powered Off Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # laserTrackerOff
    def laserTrackerOff(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Laser Tracker Off can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(2, 'Laser Tracker Off Number', response)
        self.dataCheck(command, 'Laser Tracker Off Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # airSupplyClosedAirReliefOpen
    def airSupplyClosedAirReliefOpen(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Air Supply Closed can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(3, 'Air Supply Closed Number', response)
        self.dataCheck(command, 'Air Supply Closed Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # gisEarthquakeSignal
    def gisEarthquakeSignal(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the GIS Earthquake Signal can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(4, 'GIS Earthquake Signal Number', response)
        self.dataCheck(command, 'GIS Earthquake Signal Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # gisEStop
    def gisEStop(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the GIS E Stop can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(5, 'GIS E Stop Number', response)
        self.dataCheck(command, 'GIS E StopCommand', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # tmaMotionStop
    def tmaMotionStop(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the TMA Motion Stop can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(6, 'TMA Motion Stop Number', response)
        self.dataCheck(command, 'TMA Motion Stop Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # gisHeartbeatLost
    def gisHeartbeatLost(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the GIS Heartbeat Lost can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(7, 'GIS Heartbeat Lost Number', response)
        self.dataCheck(command, 'GIS Heartbeat Lost Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # airSupplyValveStatusOpen
    def airSupplyValveStatusOpen(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Air Supply Valve Status Open can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(8, 'Air Supply Valve Status Open Number', response)
        self.dataCheck(command, 'Air Supply Valve Status Open Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # airSupplyValveStatusClosed
    def airSupplyValveStatusClosed(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Air Supply Valve Status Closed can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(9, 'Air Supply Valve Status Closed Number', response)
        self.dataCheck(command, 'Air Supply Valve Status Closed Command', response)
        response[:0] = bytes([len(response)])
        return response

    ###############################################################################
    # mirrorCellLightsOn
    def mirrorCellLightsOn(self, command:int):
        if (command != 0 and command != 1):
            raise Exception('The command for the Mirror Cell Lights On can only be 0 (false) or 1 (true).  The value is currently' + str(command))
        response = bytearray()
        self.dataCheck(10, 'Mirror Cell Lights On Number', response)
        self.dataCheck(command, 'Mirror Cell Lights On Command', response)
        response[:0] = bytes([len(response)])
        return response

###############################################################################
# main - for testing
def main():
    DISim = DigitalInputSimulator()
    response = DISim.powerNetworkShutDown(1)

    assert(bytes([2, 0, 1]) == response)
    print("Digital Input, Power Network Shut Down Command: " + str(binascii.hexlify(response)))

    response = DISim.fansHeatersPumpPoweredOff(1)
    assert(bytes([2, 1, 1]) == response)
    print("Digital Input, Fan Coils/Heaters/Pump Powered Off Command: " + str(binascii.hexlify(response)))

    response = DISim.laserTrackerOff(1)
    assert(bytes([2, 2, 1]) == response)
    print("Digital Input, Laser Tracker Off Command: " + str(binascii.hexlify(response)))

    response = DISim.airSupplyClosedAirReliefOpen(1)
    assert(bytes([2, 3, 1]) == response)
    print("Digital Input, Air Supply Closed Command: " + str(binascii.hexlify(response)))

    response = DISim.gisEarthquakeSignal(1)
    assert(bytes([2, 4, 1]) == response)
    print("Digital Input, GIS Earthquake Signal Command: " + str(binascii.hexlify(response)))

    response = DISim.gisEStop(1)
    assert(bytes([2, 5, 1]) == response)
    print("Digital Input, GIS E Stop Command: " + str(binascii.hexlify(response)))

    response = DISim.tmaMotionStop(1)
    assert(bytes([2, 6, 1]) == response)
    print("Digital Input, TMA Motion Stop Command: " + str(binascii.hexlify(response)))

    response = DISim.gisHeartbeatLost(1)
    assert(bytes([2, 7, 1]) == response)
    print("Digital Input, GIS Heartbeat Lost Command: " + str(binascii.hexlify(response)))

    response= DISim.airSupplyValveStatusOpen(1)
    assert(bytes([2, 8, 1]) == response)
    print("Digital Input, Air Supply Valve Status Open Command: " + str(binascii.hexlify(response)))

    response= DISim.airSupplyValveStatusClosed(1)
    assert(bytes([2, 9, 1]) == response)
    print("Digital Input, Air Supply Valve Status Closed Command: " + str(binascii.hexlify(response)))

    response = DISim.mirrorCellLightsOn(1)
#    ordArray = [c for c in response]
#    print(ordArray)
    assert(bytes([2, 10, 1]) == response)
    print("Digital Input, Mirror Cell Lights On Command: " + str(binascii.hexlify(response)))

###############################################################################
#main()
