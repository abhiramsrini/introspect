# SVT Test
# SVT version 24.1.0
# Test saved 2024-03-08_1138
# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 69e2f03b0e5ee0e7fea20895617c92fb
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
performScopeMeasurement = _create('performScopeMeasurement', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
cphyPattern1 = _create('cphyPattern1', 'SvtMipiCphyCustomPattern')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

calOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.30.30.00::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=3000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='any', defaultVal=500.0, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
calOptions.addField('commonModeValues', descrip='''Range of common-mode voltages to be verified''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[-100.0, 100.0, 300.0], displayOrder=(0, 7.0))
calOptions.addField('amplitudeValues', descrip='''Range of differential voltages to be verified''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[120.0, 200.0, 400.0, 600.0], displayOrder=(0, 8.0))
calOptions.addField('scopeSetupFile', descrip='''This is a placeholder in case we store a scope setup file as part of the script.''', attrType=str, iespInstanceName='any', defaultVal='Placeholder', displayOrder=(0, 9.0))
calOptions.addField('scopeConnectionTimeout', descrip='''Timeout for connecting to scope''', attrType=float, iespInstanceName='any', defaultVal=10000.0, displayOrder=(0, 10.0))
calOptions.addField('minVersion', descrip='''Minimum IntrsopectESP version supported by this script''', attrType=str, iespInstanceName='any', defaultVal='22.2.1', displayOrder=(0, 11.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = 'SV3CPTX17120013'
calOptions.scopeIPAddress = 'TCPIP0::169.254.103.240::inst0::INSTR'
calOptions.scopeMeasurementDelay = 3000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.calDataRate = 500.0
calOptions.calLanes = [1, 2, 3, 4]
calOptions.commonModeValues = [-100.0, 100.0, 300.0]
calOptions.amplitudeValues = [120.0, 200.0, 400.0, 600.0]
calOptions.scopeSetupFile = 'Placeholder'
calOptions.scopeConnectionTimeout = 10000.0
calOptions.minVersion = '24.1.0'
calOptions.callCustomInitMethod()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa
#connect to scope
import win32com.client
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
import time
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)
osci.WriteString("VBS 'app.SetToDefaultSetup'", 1)
osci.WriteString("*OPC?", 1)

#osci.read_termination = '\n'
#osci.write_termination = '\n'
#osci.timeout = calOptions.scopeConnectionTimeout

# Converted Keysight-specific commands to Teledyne LeCroy equivalents

# osci.write(":CALibrate:SKEW CHANnel1,0")

osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.Deskew = 0'", 1)

osci.WriteString("VBS 'app.Acquisition.C1.View = 1'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = 1'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = 1'", 1)


osci.WriteString("VBS 'app.Acquisition.C1.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Coupling = 0'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("*OPC?", 1)

#time.sleep(10)

return osci
'''
initScope.wantAllVarsGlobal = False

performScopeMeasurement.args = ''
performScopeMeasurement.code = r'''# Set timebase to proper value
osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("*OPC?", 1)

# Clear display
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)

# Set timebase to proper value
osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 5e-8'", 1)
iesp.setMeasurementTimeout(60000)


# Measure average voltage of channel 1 to set trigger level
# osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
sleepMillis(100)

osci.WriteString("VBS 'app.Measure.P1.MeasurementType = 0'", 1)
osci.WriteString("VBS 'app.Measure.ShowMeasure = true",1)
osci.WriteString("VBS 'app.Measure.StatsOn = true",1)

sleepMillis(calOptions.scopeAutoScaleDelay)

# Configure the Measuremnet Parameter for VAVerage

osci.WriteString("VBS 'app.Measure.P1.Source1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.ParamEngine = \"Mean\"'", 1)
osci.WriteString("VBS? 'return = app.WaitUntilIdle(5)'", 1)
osci.WriteString("VBS app.sleep(1000)'", 1)
osci.WriteString("VBS? 'return = app.Measure.P1.mean.Result.Value'", 1)
varAverage = osci.ReadString(500)
#print (varAverage)
#currentValue = varAverage[0]
#currentValue = float(varAverage[0])

# Configure the Measuremnet Parameter for VAMPlitude

osci.WriteString("VBS 'app.Measure.P2.Source1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P2.ParamEngine = \"Amplitude\"'", 1)
osci.WriteString("VBS? 'return = app.WaitUntilIdle(5)'", 1)
osci.WriteString("VBS app.sleep(1000)'", 1)
osci.WriteString("VBS? 'return = app.Measure.P2.mean.Result.Value'", 1)
varAmp = osci.ReadString(500)
#print (varAmp)
#currentAmp = varAmp[0]
#currentAmp = float(varAmp[0])

# Clear display
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(100)

## Now perform measurements on all channels
commonModeReturnList = list()
amplitudeReturnList = list()


for channel in [1,2,3] :

    channelString = "C%d" % channel
    print(channelString)

    commonModeMeasurementString = "VBS 'app.Measure.P1.Source1 = \"%s\"'" % channelString
    osci.writestring(commonModeMeasurementString, 1)
    sleepMillis(calOptions.scopeMeasurementDelay)
    commonModeMeasurementString = "VBS? 'return = app.Measure.P1.mean.Result.Value'"
    varAverage = osci.WriteString(commonModeMeasurementString, 1)
    varAverage = osci.ReadString(500)
    try:
        varAverage = float(varAverage.strip()) * 1000  # Convert from V to mV
        print(varAverage)
        commonModeReturnList.append(varAverage)
    except ValueError:
        varAverage = 0.0  # Fallback in case of conversion error
        #commonModeReturnList.append(varAverage[0]*1000) #convert to mV

    amplitudeMeasurementString = "VBS app.Measure.P2.Source1 = \"%s\"'" % channelString
    osci.writestring(amplitudeMeasurementString, 1)
    sleepMillis(calOptions.scopeMeasurementDelay)
    amplitudeMeasurementString = "VBS? 'return = app.Measure.P2.mean.Result.Value'"
    varAmp = osci.WriteString(amplitudeMeasurementString, 1)
    varAmp = osci.ReadString(500)
    #amplitudeReturnList.append(varAmp[0]*1000) #convert to mV
    try:
        varAmp = float(varAmp.strip()) * 1000  # Convert from V to mV
        print(varAmp)
        amplitudeReturnList.append(varAmp)
    except ValueError:
        varAmp = 0.0  # Fallback in case of conversion error


print (commonModeReturnList)
print (amplitudeReturnList)
return(commonModeReturnList, amplitudeReturnList)
'''
performScopeMeasurement.wantAllVarsGlobal = False

writeCalFile.args = 'commonModeSlopeDict, commonModeOffsetDict, amplitudeSlopeDict, amplitudeOffsetDict'
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "calCoefficients_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "calCoefficients_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    print("BEGIN SECTION", file=outFile)
    print("section type : header", file=outFile)
    print("serial number : "+calOptions.serialNumber, file=outFile)
    print("hardware revision : RevB", file=outFile)
    print("date of manufacture(YYYYMMDD) : "+date, file=outFile)
    print("date of calibration(YYYYMMDD) : "+date, file=outFile)
    print("speed grade : 3", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type: jitter_calibration_data", file=outFile)
    print("ffffffffffffffffffffffffffffffff00000000000000000000000000000000", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : tx_common_mode_calibration_data_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("#common mode slope and offset. slope will be fixed point 16:16", file=outFile)

    for wire in [0,1,2]:
        print("%f," % commonModeSlopeDict[1][wire], end=' ', file=outFile) # lane 1 slope of wire
        print("%f," % commonModeSlopeDict[2][wire], end=' ', file=outFile) # lane 2 slope of wire
        print("%f," % commonModeSlopeDict[3][wire], end=' ', file=outFile) # lane 3 slope of wire
        print("%f," % commonModeSlopeDict[4][wire], end=' ', file=outFile) # lane 4 slope of wire
        print("", file=outFile)
    for wire in [0,1,2]:
        print("%d," % commonModeOffsetDict[1][wire], end=' ', file=outFile) # lane 1 offset of wire in uV
        print("%d," % commonModeOffsetDict[2][wire], end=' ', file=outFile) # lane 2 offset of wire in uV
        print("%d," % commonModeOffsetDict[3][wire], end=' ', file=outFile) # lane 3 offset of wire in uV
        print("%d," % commonModeOffsetDict[4][wire], end=' ', file=outFile) # lane 4 offset of wire in uV
        print("", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : tx_amplitude_calibration_data_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("#amplitude slope and offset. slope will be fixed point 16:16", file=outFile)
    for wire in [0,1,2]:
        print("%f," % amplitudeSlopeDict[1][wire], end=' ', file=outFile) # lane 1 slope of wire
        print("%f," % amplitudeSlopeDict[2][wire], end=' ', file=outFile) # lane 2 slope of wire
        print("%f," % amplitudeSlopeDict[3][wire], end=' ', file=outFile) # lane 3 slope of wire
        print("%f," % amplitudeSlopeDict[4][wire], end=' ', file=outFile) # lane 4 slope of wire
        print("", file=outFile)
    for wire in [0,1,2]:
        print("%d," % amplitudeOffsetDict[1][wire], end=' ', file=outFile) # lane 1 offset of wire in uV
        print("%d," % amplitudeOffsetDict[2][wire], end=' ', file=outFile) # lane 2 offset of wire in uV
        print("%d," % amplitudeOffsetDict[3][wire], end=' ', file=outFile) # lane 3 offset of wire in uV
        print("%d," % amplitudeOffsetDict[4][wire], end=' ', file=outFile) # lane 4 offset of wire in uV
        print("", file=outFile)
    print("END SECTION", file=outFile)

    #--Append CPTX common mode data for replica channels. No cal data is automatically gathered for this--
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : tx_common_mode_calibration_data_replica_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("1.0, 1.0, 1.0, 1.0,", file=outFile)
    print("0, 0, 0, 0,", file=outFile)
    print("END SECTION", file=outFile)

    #--Append DPTX data. Shares same data as CPTX but in a different format--
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_amplitude_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("%f," % amplitudeSlopeDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%f," % amplitudeSlopeDict[1][0], end=' ', file=outFile) # 1Pos
    print("%f," % amplitudeSlopeDict[1][2], end=' ', file=outFile) # 2Pos
    print("%f," % amplitudeSlopeDict[3][1], end=' ', file=outFile) # 3Pos
    print("%f," % amplitudeSlopeDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%f," % amplitudeSlopeDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%f," % amplitudeSlopeDict[1][1], end=' ', file=outFile) # 1Neg
    print("%f," % amplitudeSlopeDict[3][0], end=' ', file=outFile) # 2Neg
    print("%f," % amplitudeSlopeDict[3][2], end=' ', file=outFile) # 3Neg
    print("%f," % amplitudeSlopeDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("%d," % amplitudeOffsetDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%d," % amplitudeOffsetDict[1][0], end=' ', file=outFile) # 1Pos
    print("%d," % amplitudeOffsetDict[1][2], end=' ', file=outFile) # 2Pos
    print("%d," % amplitudeOffsetDict[3][1], end=' ', file=outFile) # 3Pos
    print("%d," % amplitudeOffsetDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%d," % amplitudeOffsetDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%d," % amplitudeOffsetDict[1][1], end=' ', file=outFile) # 1Neg
    print("%d," % amplitudeOffsetDict[3][0], end=' ', file=outFile) # 2Neg
    print("%d," % amplitudeOffsetDict[3][2], end=' ', file=outFile) # 3Neg
    print("%d," % amplitudeOffsetDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)

    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_common_mode_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("%f," % commonModeSlopeDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%f," % commonModeSlopeDict[1][0], end=' ', file=outFile) # 1Pos
    print("%f," % commonModeSlopeDict[1][2], end=' ', file=outFile) # 2Pos
    print("%f," % commonModeSlopeDict[3][1], end=' ', file=outFile) # 3Pos
    print("%f," % commonModeSlopeDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%f," % commonModeSlopeDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%f," % commonModeSlopeDict[1][1], end=' ', file=outFile) # 1Neg
    print("%f," % commonModeSlopeDict[3][0], end=' ', file=outFile) # 2Neg
    print("%f," % commonModeSlopeDict[3][2], end=' ', file=outFile) # 3Neg
    print("%f," % commonModeSlopeDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("%d," % commonModeOffsetDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%d," % commonModeOffsetDict[1][0], end=' ', file=outFile) # 1Pos
    print("%d," % commonModeOffsetDict[1][2], end=' ', file=outFile) # 2Pos
    print("%d," % commonModeOffsetDict[3][1], end=' ', file=outFile) # 3Pos
    print("%d," % commonModeOffsetDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%d," % commonModeOffsetDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%d," % commonModeOffsetDict[1][1], end=' ', file=outFile) # 1Neg
    print("%d," % commonModeOffsetDict[3][0], end=' ', file=outFile) # 2Neg
    print("%d," % commonModeOffsetDict[3][2], end=' ', file=outFile) # 3Neg
    print("%d," % commonModeOffsetDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("END SECTION", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False

writeRawData.args = 'commonData, ampData'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = calOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = calOptions.serialNumber + "_CptxVoltageCalData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("CPTX Voltage Calibration Data", file=outFile)
    print("Serial Number, %s" % calOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print("Lane, WireA Programmed CM, WireA Programmed Amp, WireA Measured CM, WireA Measured Amp, WireB Programmed CM, WireB Programmed Amp, WireB Measured CM, WireB Measured Amp, WireC Programmed CM, WireC Programmed Amp, WireC Measured CM, WireC Measured Amp,", file=outFile)
    for lane in calOptions.calLanes :
        for cm in calOptions.commonModeValues :
            for amp in calOptions.amplitudeValues :
                print("%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f," % (lane, cm, amp, commonData[lane][cm][amp][0], ampData[lane][cm][amp][0], cm, amp, commonData[lane][cm][amp][1], ampData[lane][cm][amp][1], cm, amp, commonData[lane][cm][amp][2], ampData[lane][cm][amp][2]), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False


cphyParams1.calAlternateSeqNumPrbs = 8
cphyParams1.calPreambleNumUI = 21
cphyParams1.calUserSequence = [0x5555, 0xAAAA]
cphyParams1.calibrationPreambleFormat = 'format_1'
cphyParams1.lp000Duration = 65.0
cphyParams1.lp001Duration = 100.0
cphyParams1.opticalLink = 'disabled'
cphyParams1.post2NumUI = 112
cphyParams1.postNumUI = 112
cphyParams1.postSymbols = '4444444'
cphyParams1.preBeginNumUI = 196
cphyParams1.preBeginSymbols = '3333333'
cphyParams1.preEndSymbols = '3333333'
cphyParams1.progSeqSymbols = '33333333333333'
cphyParams1.syncWord = '3444443'
cphyParams1.t3AlpPauseMin = 50
cphyParams1.t3AlpPauseWake = 50
cphyParams1.tHsExitDuration = 300.0
cphyParams1.tTaGetDuration = 5
cphyParams1.tTaGoDuration = 4.0
cphyParams1.tTaSureDuration = 1.0
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 50.0
cphyParams1.useAlp = False

cphyPattern1.hsData = [42, 0]
cphyPattern1.hsDataMode = 'prbs'
cphyPattern1.hsPrbsOrder = 9
cphyPattern1.hsPrbsSeed = None
cphyPattern1.hsSymbols = '22200000000000'
cphyPattern1.lpBits = ''
cphyPattern1.packetSize = 1000
cphyPattern1.patternType = 'packetLoop'
cphyPattern1.sameDataInEachPacket = True
cphyPattern1.stopDuration = 0

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 500.0
mipiClockConfig1.referenceClocks = refClocksConfig

mipiCphyGenerator1.clockConfig = mipiClockConfig1
mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.hsPostTaps = [0]
mipiCphyGenerator1.hsPreTaps = [0]
mipiCphyGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.jitterInjection = None
mipiCphyGenerator1.lanes = [1, 2, 3, 4]
mipiCphyGenerator1.lpHighVoltages = [1200.0]
mipiCphyGenerator1.lpLowVoltages = [0.0]
mipiCphyGenerator1.params = cphyParams1
mipiCphyGenerator1.pattern = CPHY_hsOnly333
mipiCphyGenerator1.resetPatternMemory = True
mipiCphyGenerator1.splitDataAcrossLanes = True
mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'


initScope._showInList = False
performScopeMeasurement._showInList = False
writeCalFile._showInList = False
writeRawData._showInList = False

cphyParams1._showInList = False
cphyPattern1._showInList = False
mipiCphyGenerator1._showInList = False
resultFolderCreator1._showInList = False
#! TEST PROCEDURE
# Check Version
import numpy as np

svtVersion = getSvtVersion()
if svtVersion < calOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, calOptions.minVersion))

res_correction = 1.05

# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

# Initialize generator
mipiCphyGenerator1.lanes = calOptions.calLanes
mipiClockConfig1.dataRate = calOptions.calDataRate
mipiCphyGenerator1.setup()

#Enable calibration mode. Ensures no previously stored cal data is being applied.
iesp = getIespInstance()
iesp.writeSubPartRegister(0x0930, 0x00, 0x01)   # calibration mode

# Define results dictionary
measuredCommonModeDict = dict()
measuredAmplitudeDict = dict()

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

for lane in mipiCphyGenerator1.lanes :
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)
    myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane
    waitForGuiOkDialog(myString)
    measuredCommonModeDict[lane] = dict()
    measuredAmplitudeDict[lane] = dict()

    for programmedCommonMode in calOptions.commonModeValues :
        print("Measuring at %f mV common-mode..." % programmedCommonMode)
        measuredCommonModeDict[lane][programmedCommonMode] = dict()
        measuredAmplitudeDict[lane][programmedCommonMode] = dict()

        for programmedAmplitude in calOptions.amplitudeValues :
            print("Measuring at %f mV amplitude..." % programmedAmplitude)
            measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude] = list()
            measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude] = list()

            # Update the generator
            mipiCphyGenerator1.hsCommonVoltagesABC = [(programmedCommonMode, programmedCommonMode, programmedCommonMode)]
            mipiCphyGenerator1.hsVoltageAmplitudesABC = [(programmedAmplitude, programmedAmplitude, programmedAmplitude)]
            mipiCphyGenerator1.update()

            # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane
            (measuredCommonMode, measuredAmplitude) = performScopeMeasurement()


            # Accumulate the list into the dictionaries
            for wire in range(0,3,1) :
                measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude].append(measuredCommonMode[wire]*res_correction)
                # Increase common mode measurement by 5% to account for impedance difference
                measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude].append(measuredAmplitude[wire])

            # Display information messages
            wires = ['A', 'B', 'C']
            for wire in range(0,3,1) :
                print("Wire %s: Programmed % f mV common-mode, and measured %f mV..." % (wires[wire],programmedCommonMode, measuredCommonMode[wire]))
                print("Wire %s: Programmed %f mV amplitude, and measured %f mV..." % (wires[wire], programmedAmplitude, measuredAmplitude[wire]))

# Dump the raw measurement values into a csv file
writeRawData(measuredCommonModeDict, measuredAmplitudeDict)

# Compute averages on a per-wire basis. Note the change in dictionary definition
averageCommonModeDict = dict()
for lane in mipiCphyGenerator1.lanes :
    averageCommonModeDict[lane] = dict()
    for wire in [0,1,2] :
        averageCommonModeDict[lane][wires[wire]] = list()
        for programmedCommonMode in calOptions.commonModeValues :
            currentAverageValue = 0
            for  programmedAmplitude in calOptions.amplitudeValues :
                currentAverageValue += measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude][wire]
            currentAverageValue = currentAverageValue / len(calOptions.amplitudeValues)
            averageCommonModeDict[lane][wires[wire]].append(currentAverageValue)

averageAmplitudeDict = dict()
for lane in mipiCphyGenerator1.lanes :
    averageAmplitudeDict[lane] = dict()
    for wire in [0,1,2] :
        averageAmplitudeDict[lane][wires[wire]] = list()
        for programmedAmplitude in calOptions.amplitudeValues :
            currentAverageValue = 0
            for programmedCommonMode in calOptions.commonModeValues :
                currentAverageValue += measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude][wire]
            currentAverageValue = currentAverageValue / len(calOptions.commonModeValues)
            averageAmplitudeDict[lane][wires[wire]].append(currentAverageValue)



# Compute slope and offset, then store to cal file
commonModeSlopeDict = dict()
commonModeOffsetDict = dict()
amplitudeSlopeDict = dict()
amplitudeOffsetDict = dict()

for lane in calOptions.calLanes :
    commonModeSlopeDict[lane] = list()
    commonModeOffsetDict[lane] = list()
    amplitudeSlopeDict[lane] = list()
    amplitudeOffsetDict[lane] = list()
    for wire in [0,1,2] :
        currentCommonModeList = averageCommonModeDict[lane][wires[wire]]
        polynomialValuesCommonMode = np.polyfit(currentCommonModeList, calOptions.commonModeValues, 1)
        commonModeSlopeDict[lane].append(polynomialValuesCommonMode[0])
        commonModeOffsetDict[lane].append(polynomialValuesCommonMode[1]*1000)   #convert to uV

        currentAmplitudeList = averageAmplitudeDict[lane][wires[wire]]
        polynomialValuesAmplitude = np.polyfit(currentAmplitudeList, calOptions.amplitudeValues, 1)
        amplitudeSlopeDict[lane].append(polynomialValuesAmplitude[0])
        amplitudeOffsetDict[lane].append(polynomialValuesAmplitude[1]*1000)     #convert to uV


writeCalFile(commonModeSlopeDict, commonModeOffsetDict, amplitudeSlopeDict, amplitudeOffsetDict)
