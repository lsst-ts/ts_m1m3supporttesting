import binascii
import struct
from Simulator import Simulator

'''
This class simulates responses from the ILC.  Returns a byte array for each
response possible.
This will return different data then the actually ILC response.   There will 
be no CRC at the end of the byte array and a byte count of all bytes after 
the function will occur after the function code.

AWC 29 August 2017
'''
class ILCSimulator(Simulator):

    def __init__(self):
        pass
        
    ##########################################################################################################
    # Finalize the response by prepending the overall length (for UDP completeness), address, function, and length (for FPGA)
    def finalizeResponse(self, address, function, response):
        length = len(response)
        response[:0] = bytes([len(response)])
        response[:0] = bytes([function])
        response[:0] = bytes([address])
        response[:0] = bytes([len(response)])
        return response
    

    ##########################################################################################################
    # Code 17(0x11) Report Server Id
    def reportServerId(self, serverAddr, uniqueId, ilcAppType, networkNodeType,
                       ilcSelectedOptions, networkNodeOptions, majorRev, minorRev,
                       firmwareName):
        response = bytearray()
        
        firmwareNameBytes = firmwareName.encode('ascii')
        # 12 bytes comes from uniqueId (6 bytes), ilcAppType (1 byte),
        # networkNodeType (1 byte), ilcSelectedOptions (1 byte),
        # networkNodeOptions (1 byte), majorRev (1 byte), minorRev (1 byte)
        byteCount = 12 + len(firmwareNameBytes)
        self.dataCheck(byteCount, 'Byte Count', response)

        self.dataCheck(uniqueId, 'Unique Id', response, 6)
        self.dataCheck(ilcAppType, 'ILC App Type', response)
        self.dataCheck(networkNodeType, 'Network Node Type', response)
        self.dataCheck(ilcSelectedOptions, 'ILC App Type', response)
        self.dataCheck(networkNodeOptions, 'Network Node Options', response)
        self.dataCheck(majorRev, 'Major Revision', response)
        self.dataCheck(minorRev, 'Minor Revision', response)
        response.extend(firmwareNameBytes)
                
        return self.finalizeResponse(serverAddr, 17, response)

    ##########################################################################################################
    # Code 18(0x12) Report Server Status
    def reportServerStatus(self, serverAddr, mode, status, faults):
        response = bytearray()

        self.dataCheck(mode, 'Mode', response)
        self.dataCheck(status, 'Status', response, 2)
        self.dataCheck(faults, 'Faults', response, 2)
                
        return self.finalizeResponse(serverAddr, 18, response)

    ##########################################################################################################
    # Code 65(0x41) ILC Mode
    def ilcMode(self, serverAddr, ilcMode):
        response = bytearray()
        
        self.dataCheck(ilcMode, 'ILCMode', response, 2)
 
        return self.finalizeResponse(serverAddr, 65, response)

    ##########################################################################################################
    # Code 66(0x42) Step Motor Command (unicast)
    def stepMotorCommand(self, serverAddr, statusByte, ssiEncoderValue, loadCellForce):
        response = bytearray()
        
        self.dataCheck(statusByte, 'Status Byte', response)
        self.dataCheck(ssiEncoderValue, 'SSI Encoder Value', response, 4)
        self.dataCheck(loadCellForce, 'Load Cell Force', response, 4)
        
        return self.finalizeResponse(serverAddr, 66, response)

    ##########################################################################################################
    # Code 67(0x43) Force(N) and Status Request
    def forceAndStatusRequest(self, serverAddr, statusByte, ssiEncoderValue, loadCellForce):
        response = bytearray()

        self.dataCheck(statusByte, 'Status Byte', response)
        self.dataCheck(ssiEncoderValue, 'SSI Encoder Value', response, 4)
        self.dataCheck(loadCellForce, 'Load Cell Force', response, 4)
   
        return self.finalizeResponse(serverAddr, 67, response)

    ##########################################################################################################
    # Code 72(0x48) Set ILC Temporary Address
    def setIlcTemporaryAddress(self, serverAddr, temporaryAddress):
        response = bytearray()
        
        self.dataCheck(temporaryAddress, 'Temporary Address', response)
        
        return self.finalizeResponse(serverAddr, 72, response)

    ##########################################################################################################
    # Code 73(0x49) Set Boost Valve DCA Gains
    def setBoostValueDcaGains(self, serverAddr):
        response = bytearray()
        
        return self.finalizeResponse(serverAddr, 73, response)

    ##########################################################################################################
    # Code 74(0x4A) Read Boost Valve DCA Gains
    def readBoostValueDcaGains(self, serverAddr, axialBoostValveGain, lateralBoostValveGain):
        response = bytearray()
        
        self.dataCheck(axialBoostValveGain, 'Axial Boost Valve Gain', response, 4)
        self.dataCheck(lateralBoostValveGain, 'Lateral Boost Valve Gain', response, 4)
        
        return self.finalizeResponse(serverAddr, 74, response)

    ##########################################################################################################
    # Code 75(0x4B) Pneumatic Axis Force Demand Command (Single)
    def singlePneumaticAxisForce(self, statusByte, serverAddr, loadCellForce):
        response = bytearray()
        
        self.dataCheck(statusByte, 'Status Byte', response)
        self.dataCheck(loadCellForce, 'Load Cell Force', response, 4)
        
        return self.finalizeResponse(serverAddr, 75, response)

    ##########################################################################################################
    # Code 75(0x4B) Pneumatic Axis Force Demand Command (Dual)
    def dualPneumaticAxisForce(self, serverAddr, statusByte, axialLoadCellForce, lateralLoadCellForce):
        response = bytearray()
        
        self.dataCheck(statusByte, 'Status Byte', response)
        self.dataCheck(axialLoadCellForce, 'Axial Load Cell Force', response, 4)
        self.dataCheck(lateralLoadCellForce, 'Lateral Load Cell Force', response, 4)
        
        return self.finalizeResponse(serverAddr, 75, response)

    ##########################################################################################################
    # Code 76(0x4C) Pneumatic Force and Status (Single)
    def singlePneumaticForceAndStatus(self, statusByte, serverAddr, loadCellForce):
        response = bytearray()
        
        self.dataCheck(statusByte, 'Status Byte', response, 1, False)
        self.dataCheck(loadCellForce, 'Load Cell Force', response, 4)
        
        return self.finalizeResponse(serverAddr, 76, response)

    ##########################################################################################################
    # Code 76(0x4C) Pneumatic Force and Status (Dual)
    def dualPneumaticForceAndStatus(self, serverAddr, statusByte, axialLoadCellForce, lateralLoadCellForce):
        response = bytearray()
        
        self.dataCheck(statusByte, 'Status Byte', response, 1, False)
        self.dataCheck(axialLoadCellForce, 'Axial Load Cell Force', response, 4)
        self.dataCheck(lateralLoadCellForce, 'Lateral Load Cell Force', response, 4)
        
        return self.finalizeResponse(serverAddr, 76, response)

    ##########################################################################################################
    # Code 80(0x50) Set ADC Sample Rate
    def setAdcSampleRate(self, serverAddr, scanRateCode):
        response = bytearray()
        
        self.dataCheck(scanRateCode, 'Scan Rate Code', response, 1)
        
        return self.finalizeResponse(serverAddr, 80, response)

    ##########################################################################################################
    # Code 81(0x51) Set ADC Channel Offset and Sensitivity
    def setAdcChannelOffsetAndSensitivity(self, serverAddr):
        response = bytearray()
        
        return self.finalizeResponse(serverAddr, 81, response)

    ##########################################################################################################
    # Code 82(0x52) Read DAC Values
    def readDacValues(self, serverAddr, dac1ValueAxialPush, dac2ValueAxialPush,
                      dac3ValueLateralPush, dac4ValueLateralPush):
        response = bytearray()
        
        self.dataCheck(dac1ValueAxialPush, 'DAC 1 Axial Push', response, 2)
        self.dataCheck(dac2ValueAxialPush, 'DAC 2 Axial Push', response, 2)
        self.dataCheck(dac3ValueLateralPush, 'DAC 3 Lateral Push', response, 2)
        self.dataCheck(dac4ValueLateralPush, 'DAC 4 Lateral Push', response, 2)

        return self.finalizeResponse(serverAddr, 82, response)

    ##########################################################################################################
    # Code 107(0x6B) Reset
    def reset(self, serverAddr):
        response = bytearray()
                
        return self.finalizeResponse(serverAddr, 107, response)

    ##########################################################################################################
    # Code 110(0x6E) Read Calibration Data
    def readCalibrationData(self, serverAddr,
                            mainAdcCalibration1, mainAdcCalibration2, mainAdcCalibration3, mainAdcCalibration4,
                            mainSensorOffset1, mainSensorOffset2, mainSensorOffset3, mainSensorOffset4,
                            mainSensorSensitivity1, mainSensorSensitivity2, mainSensorSensitivity3, mainSensorSensitivity4,
                            backupAdcCalibration1, backupAdcCalibration2, backupAdcCalibration3, backupAdcCalibration4,
                            backupSensorOffset1, backupSensorOffset2, backupSensorOffset3, backupSensorOffset4,
                            backupSensorSensitivity1, backupSensorSensitivity2, backupSensorSensitivity3, backupSensorSensitivity4):
        response = bytearray()
        
        self.dataCheck(mainAdcCalibration1, 'Main ADC Calibration1', response, 4)
        self.dataCheck(mainAdcCalibration2, 'Main ADC Calibration2', response, 4)
        self.dataCheck(mainAdcCalibration3, 'Main ADC Calibration3', response, 4)
        self.dataCheck(mainAdcCalibration4, 'Main ADC Calibration4', response, 4)
        self.dataCheck(mainSensorOffset1, 'Main Sensor Offset1', response, 4)
        self.dataCheck(mainSensorOffset2, 'Main Sensor Offset2', response, 4)
        self.dataCheck(mainSensorOffset3, 'Main Sensor Offset3', response, 4)
        self.dataCheck(mainSensorOffset4, 'Main Sensor Offset4', response, 4)
        self.dataCheck(mainSensorSensitivity1, 'Main Sensor Sensitivity1', response, 4)
        self.dataCheck(mainSensorSensitivity2, 'Main Sensor Sensitivity2', response, 4)
        self.dataCheck(mainSensorSensitivity3, 'Main Sensor Sensitivity3', response, 4)
        self.dataCheck(mainSensorSensitivity4, 'Main Sensor Sensitivity4', response, 4)
        self.dataCheck(backupAdcCalibration1, 'Backup ADC Calibration1', response, 4)
        self.dataCheck(backupAdcCalibration2, 'Backup ADC Calibration2', response, 4)
        self.dataCheck(backupAdcCalibration3, 'Backup ADC Calibration3', response, 4)
        self.dataCheck(backupAdcCalibration4, 'Backup ADC Calibration4', response, 4)
        self.dataCheck(backupSensorOffset1, 'Backup Sensor Offset1', response, 4)
        self.dataCheck(backupSensorOffset2, 'Backup Sensor Offset2', response, 4)
        self.dataCheck(backupSensorOffset3, 'Backup Sensor Offset3', response, 4)
        self.dataCheck(backupSensorOffset4, 'Backup Sensor Offset4', response, 4)
        self.dataCheck(backupSensorSensitivity1, 'Backup Sensor Sensitivity1', response, 4)
        self.dataCheck(backupSensorSensitivity2, 'Backup Sensor Sensitivity2', response, 4)
        self.dataCheck(backupSensorSensitivity3, 'Backup Sensor Sensitivity3', response, 4)
        self.dataCheck(backupSensorSensitivity4, 'Backup Sensor Sensitivity4', response, 4)
        
        return self.finalizeResponse(serverAddr, 110, response)

    ##########################################################################################################
    # Code 119(0x77) Read DCA Pressure Values
    def readDcaPressureValues(self, serverAddr,
                            pressure1AxialPush, pressure2AxialPull, pressure3LateralPull, pressure4LateralPush):
        response = bytearray()
        
        self.dataCheck(pressure1AxialPush, 'Pressure 1 Axial Push', response, 4)
        self.dataCheck(pressure2AxialPull, 'Pressure 2 Axial Pull', response, 4)
        self.dataCheck(pressure3LateralPull, 'Pressure 3 Lateral Pull', response, 4)
        self.dataCheck(pressure4LateralPush, 'Pressure 4 Lateral Push', response, 4)
        
        return self.finalizeResponse(serverAddr, 119, response)

    ##########################################################################################################
    # Code 120(0x78) Report DCA Id
    def reportDcaId(self, serverAddr, dcaUniqueId, firmwareType, firmwareVersion):

        response = bytearray()
        
        self.dataCheck(dcaUniqueId, 'DCA Unique ID', response, 6)
        self.dataCheck(firmwareType, 'Firmware Type', response)
        self.dataCheck(firmwareVersion, 'Firmware Version', response, 2)
        
        return self.finalizeResponse(serverAddr, 120, response)

    ##########################################################################################################
    # Code 121(0x79) Report DCA Status
    def reportDcaStatus(self, serverAddr, dcaStatus):

        response = bytearray()
        
        self.dataCheck(dcaStatus, 'DCA Status', response, 2)
        
        return self.finalizeResponse(serverAddr, 121, response)
        
    ##########################################################################################################
    # Code 122(0x7A) Read LVDT
    def readLVDT(self, serverAddr, lvdt1, lvdt2):

        response = bytearray()
        
        self.dataCheck(lvdt1, 'LVDT1', response, 4)
        self.dataCheck(lvdt2, 'LVDT2', response, 4)
        
        return self.finalizeResponse(serverAddr, 122, response)

##########################################################################################################
# For Testing
def main():
    ilcs = ILCSimulator()

    # test CRC
    ba = bytearray()
    ba.append(0)
    ba.append(1)
    ba.append(2)
    print("Array [0,1,2] should be hex 91F1: " + hex(ilcs.calculateCRC(ba)))

    # test Report Server Id (17)
    response = ilcs.reportServerId(1, 'ABCDEF', 1, 4, 1, 2, 1, 0, 'Firmware Name')
    # We no longer use the CRC for the ILC responses
    # and have added a byte count as the 3rd entry.
    # assert (bytes([1, 17, 25, 65, 66, 67, 68, 69, 70, 1, 4, 1, 2, 1, 0, 70, 105, 114, 109, 119, 97, 114, 101, 32, 78, 97, 109, 101, 117, 185]) == response)
    assert (bytes([29, 1, 17, 26, 25, 65, 66, 67, 68, 69, 70, 1, 4, 1, 2, 1, 0, 70, 105, 114, 109, 119, 97, 114, 101, 32, 78, 97, 109, 101]) == response)
    print("Report Server Id (17): " + str(binascii.hexlify(response)))

    # test Report Server Status (18)
    response = ilcs.reportServerStatus(1, 2, 512, 256)
    # assert(bytes([1, 18, 2, 2, 0, 1, 0, 90, 113]) == response)
    assert(bytes([8, 1, 18, 5, 2, 2, 0, 1, 0]) == response)
    print("Report Server Status (18): " + str(binascii.hexlify(response)))

    # test ILC Mode (65)
    response = ilcs.ilcMode(1, 2)
    # assert(bytes([1, 65, 0, 2, 13, 208]) == response)
    assert(bytes([5, 1, 65, 2, 0, 2]) == response)
    print("ILC Mode(65): " + str(binascii.hexlify(response)))
    
    # test Step Motor Command (66)
    response = ilcs.stepMotorCommand(1, 0, 4096, 3203.46)
    # assert(bytes([1, 66, 0, 0, 0, 16, 0, 69, 72, 55, 92, 133, 32]) == response)
    assert(bytes([12, 1, 66, 9, 0, 0, 0, 16, 0, 69, 72, 55, 92]) == response)
    print("Step Motor Command (66): " + str(binascii.hexlify(response)))
    
    # test Force And Status Request (67)
    response = ilcs.forceAndStatusRequest(1, 0, -32, 3.4601)
    #assert(bytes([1, 67, 0, 255, 255, 255, 224, 64, 93, 114, 71, 145, 197]) == response)
    assert(bytes([12, 1, 67, 9, 0, 255, 255, 255, 224, 64, 93, 114, 71]) == response)
    print("Force And Status Request (67): " + str(binascii.hexlify(response)))

    # test Set ILC Temporary Address (72)
    response = ilcs.setIlcTemporaryAddress(1, 72)
    # assert(bytes([1, 72, 72, 54, 22]) == response)
    assert(bytes([4, 1, 72, 1, 72]) == response)
    print("Set ILC Temporary Address (72): " + str(binascii.hexlify(response)))

    # test Set ADC Sample Rate (80)
    response = ilcs.setAdcSampleRate(1, 11)
    # assert(bytes([1, 80, 0, 11, 14, 64]) == response)
    assert(bytes([5, 1, 80, 2, 0, 11]) == response)
    print("Set ADC Sample Rate (80): " + str(binascii.hexlify(response)))

    # test Read Calibration Data (110)
    response = ilcs.readCalibrationData(1,123.45, 234.56, 345.67, 456.78, 567.89, 0, 0, 0,
                                        678.91, 0, 0, 0, 789.21, 891.23, 912.34, -123.45,
                                        -234.56, 0, 0, 0, -345.67, 0, 0, 0)
#    assert(bytes([1, 110, 66, 246, 230, 102, 67, 106, 143, 92, 67, 172, 213, 195, 67, 228, 99, 215, 68, 13, 248, 246, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 41, 186, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 69, 77, 113, 68, 94, 206, 184, 68, 100, 21, 195, 194, 246, 230, 102, 195, 106, 143, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 172, 213, 195, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 228, 144]) == response)
    assert(bytes([99, 1, 110, 24*4, 66, 246, 230, 102, 67, 106, 143, 92, 67, 172, 213, 195, 67, 228, 99, 215, 68, 13, 248, 246, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 41, 186, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 69, 77, 113, 68, 94, 206, 184, 68, 100, 21, 195, 194, 246, 230, 102, 195, 106, 143, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 172, 213, 195, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == response)
    print("Read Calibration Data (110): " + str(binascii.hexlify(response)))
    
    # test Read LVDT (122)
    response = ilcs.readLVDT(1, 1.2, 2.3)
    print("Read LVDT (122): " + str(binascii.hexlify(response)))
    assert(bytes([11, 1, 122, 8, 0x3F, 0x99, 0x99, 0x9A, 0x40, 0x13, 0x33, 0x33]) == response)
    

    print("Succesfully end testing.")
##########################################################################################################
#main()
