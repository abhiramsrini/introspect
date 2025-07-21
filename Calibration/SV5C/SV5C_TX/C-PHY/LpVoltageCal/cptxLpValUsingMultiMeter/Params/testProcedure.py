# SVT Test
# SVT version 25.2.0
# Test saved 2025-07-14_2055
# Form factor: SV5C_4L8G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: bfa30a2a1d212579477e265ac72bc96a
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
getVoltage = _create('getVoltage', 'SvtFunction', iespName=None)
performValidationOnCollectedData = _create('performValidationOnCollectedData', 'SvtFunction', iespName=None)
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName=None)
writeRawData = _create('writeRawData', 'SvtFunction', iespName=None)

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
cphyPattern1 = _create('cphyPattern1', 'SvtMipiCphyCustomPattern')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
powerOffPattern = _create('powerOffPattern', 'SvtMipiCphyCustomPattern')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
visaInstrument1 = _create('visaInstrument1', 'SvtVisaInstrument')

calOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=500.0, displayOrder=(0, 2.0))
calOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
calOptions.addField('lpLowValues', descrip='''Range of LP low voltages to be verified''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=float, defaultVal=[-100.0, 100.0, 300.0], displayOrder=(0, 4.0))
calOptions.addField('lpHighValues', descrip='''Range of LP high voltages to be verified''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', attrSubType=float, defaultVal=[600.0, 900.0, 1100.0, 1200.0], displayOrder=(0, 5.0))
calOptions.addField('absoluteErrorThreshold', descrip='''''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=20.0, displayOrder=(0, 6.0))
calOptions.addField('percentErrorThreshold', descrip='''''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal=10.0, displayOrder=(0, 7.0))
calOptions.addField('minVersion', descrip='''Minimum IntrsopectESP version supported by this script''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_CPHY_GENERATOR', defaultVal='20.4', displayOrder=(0, 8.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.calDataRate = 500.0
calOptions.calLanes = [1, 2, 3, 4]
calOptions.lpLowValues = [-100.0, 100.0, 300.0]
calOptions.lpHighValues = [600.0, 900.0, 1100.0, 1200.0]
calOptions.absoluteErrorThreshold = 10.0
calOptions.percentErrorThreshold = 5.0
calOptions.minVersion = '20.4'
calOptions.callCustomInitMethod()
getVoltage.args = ''
getVoltage.code = r'''#vMeasuredV = visaInstrument1.queryValue("MEASure:VOLTage:DC?")
import time

#vMeasuredV = visaInstrument1.queryValue("FETC?")
vMeasuredV = float(visaInstrument1.queryValue("MEAS:VOLT:DC?"))
vMeasured = vMeasuredV * 1000
return(vMeasured)
'''
getVoltage.wantAllVarsGlobal = False

performValidationOnCollectedData.args = 'lpLowData, lpHighData'
performValidationOnCollectedData.code = r'''print("Checking measured data...")
fail = 0

for lane in calOptions.calLanes :
        for lpLow in calOptions.lpLowValues :
            for lpHigh in calOptions.lpHighValues :
                for wire in range(3) :
                    lpLowErrorValue = abs( lpLowData[lane][lpLow][wire] - lpLow)
                    lpLowErrorPercent = lpLowErrorValue / lpLow * 100
                    lpHighErrorValue = abs( lpHighData[lane][lpHigh][wire] - lpHigh )
                    lpHighErrorPercent = lpHighErrorValue /lpHigh * 100
                    if not ( lpLowErrorValue < calOptions.absoluteErrorThreshold or lpLowErrorPercent < calOptions.percentErrorThreshold ):
                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                        print("Target lpLow is %f mV" % lpLow)
                        print("Measured lpLow is %f mV" % lpLowData[lane][lpLow][wire])
                        print("Absolute Error is %f mV" % lpLowErrorValue)
                        print("Percent Error is %f percent" % lpLowErrorPercent)
                        fail = 1
                    if not ( lpHighErrorValue < calOptions.absoluteErrorThreshold or lpHighErrorPercent < calOptions.percentErrorThreshold ) :
                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                        print("Target lpHigh %f mV" % lpHigh)
                        print("Measured lpHigh is %f mV" % lpHighData[lane][lpHigh][wire])
                        print("Absolute Error is %f mV" % lpHighErrorValue)
                        print("Percent Error is %f percent" % lpHighErrorPercent)
                        fail = 1

if fail == 1:
    return False
else:
    return True
'''
performValidationOnCollectedData.wantAllVarsGlobal = False

writeCalFile.args = 'lpLowSlopeDict, lpLowOffsetDict, lpHighSlopeDict, lpHighOffsetDict'
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
    #commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : tx_lp_high_calibration_data_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("#LP High slope and offset. slope will be fixed point 16:16", file=outFile)

    for wire in [0,1,2]:
        for lane in calOptions.calLanes :
            print("%f," % lpHighSlopeDict[lane][wire], end=' ', file=outFile) # lane 1 slope of wire
        print("", file=outFile)
    for wire in [0,1,2]:
        for lane in calOptions.calLanes:
            print("%d," % lpHighOffsetDict[lane][wire], end=' ', file=outFile) # lane 1 offset of wire in uV
        print("", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : tx_lp_low_calibration_data_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("#LP Low slope and offset. slope will be fixed point 16:16", file=outFile)
    for wire in [0,1,2]:
        for lane in calOptions.calLanes:
            print("%f," % lpLowSlopeDict[lane][wire], end=' ', file=outFile) # lane 1 slope of wire
        print("", file=outFile)
    for wire in [0,1,2]:
        for lane in calOptions.calLanes:
            print("%d," % lpLowOffsetDict[lane][wire], end=' ', file=outFile) # lane 1 offset of wire in uV
        print("", file=outFile)
    print("END SECTION", file=outFile)


    #--Append DPTX data. Shares same data as CPTX but in a different format--
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_lp_high_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("%f," % lpHighSlopeDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%f," % lpHighSlopeDict[1][0], end=' ', file=outFile) # 1Pos
    print("%f," % lpHighSlopeDict[1][2], end=' ', file=outFile) # 2Pos
    print("%f," % lpHighSlopeDict[3][1], end=' ', file=outFile) # 3Pos
    print("%f," % lpHighSlopeDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%f," % lpHighSlopeDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%f," % lpHighSlopeDict[1][1], end=' ', file=outFile) # 1Neg
    print("%f," % lpHighSlopeDict[3][0], end=' ', file=outFile) # 2Neg
    print("%f," % lpHighSlopeDict[3][2], end=' ', file=outFile) # 3Neg
    print("%f," % lpHighSlopeDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("%d," % lpHighOffsetDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%d," % lpHighOffsetDict[1][0], end=' ', file=outFile) # 1Pos
    print("%d," % lpHighOffsetDict[1][2], end=' ', file=outFile) # 2Pos
    print("%d," % lpHighOffsetDict[3][1], end=' ', file=outFile) # 3Pos
    print("%d," % lpHighOffsetDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%d," % lpHighOffsetDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%d," % lpHighOffsetDict[1][1], end=' ', file=outFile) # 1Neg
    print("%d," % lpHighOffsetDict[3][0], end=' ', file=outFile) # 2Neg
    print("%d," % lpHighOffsetDict[3][2], end=' ', file=outFile) # 3Neg
    print("%d," % lpHighOffsetDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)

    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_lp_low_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("%f," % lpLowSlopeDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%f," % lpLowSlopeDict[1][0], end=' ', file=outFile) # 1Pos
    print("%f," % lpLowSlopeDict[1][2], end=' ', file=outFile) # 2Pos
    print("%f," % lpLowSlopeDict[3][1], end=' ', file=outFile) # 3Pos
    print("%f," % lpLowSlopeDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%f," % lpLowSlopeDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%f," % lpLowSlopeDict[1][1], end=' ', file=outFile) # 1Neg
    print("%f," % lpLowSlopeDict[3][0], end=' ', file=outFile) # 2Neg
    print("%f," % lpLowSlopeDict[3][2], end=' ', file=outFile) # 3Neg
    print("%f," % lpLowSlopeDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("%d," % lpLowOffsetDict[4][1], end=' ', file=outFile) # Clk Pos
    print("%d," % lpLowOffsetDict[1][0], end=' ', file=outFile) # 1Pos
    print("%d," % lpLowOffsetDict[1][2], end=' ', file=outFile) # 2Pos
    print("%d," % lpLowOffsetDict[3][1], end=' ', file=outFile) # 3Pos
    print("%d," % lpLowOffsetDict[2][0], end=' ', file=outFile) # 4Pos
    print("", file=outFile)
    print("%d," % lpLowOffsetDict[4][2], end=' ', file=outFile) # Clk Neg
    print("%d," % lpLowOffsetDict[1][1], end=' ', file=outFile) # 1Neg
    print("%d," % lpLowOffsetDict[3][0], end=' ', file=outFile) # 2Neg
    print("%d," % lpLowOffsetDict[3][2], end=' ', file=outFile) # 3Neg
    print("%d," % lpLowOffsetDict[2][1], end=' ', file=outFile) # 4Neg
    print("", file=outFile)
    print("END SECTION", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False

writeRawData.args = 'lpLowData, lpHighData'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = calOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = calOptions.serialNumber + "_CptxLpVoltageCalData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("CPTX LP Voltage Calibration Data", file=outFile)
    print("Serial Number, %s" % calOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print("Lane, WireA Programmed LP Low, WireA Programmed LP High, WireA Measured LP Low, WireA Measured LP High, WireB Programmed LP Low, WireB Programmed LP High, WireB Measured LP Low, WireB Measured LP High, WireC Programmed LP Low, WireC Programmed LP High, WireC Measured LP Low, WireC Measured LP High,", file=outFile)
    for lane in calOptions.calLanes :
        for low in calOptions.lpLowValues :
            for high in calOptions.lpHighValues :
                print("%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f," % (lane, low, high, lpLowData[lane][low][0], lpHighData[lane][high][0], low, high, lpLowData[lane][low][1], lpHighData[lane][high][1], low, high, lpLowData[lane][low][2], lpHighData[lane][high][2]), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False


cphyParams1.calAlternateSeqNumPrbs = 8
cphyParams1.calPreambleNumUI = 21
cphyParams1.calUserSequence = [0x5555, 0xAAAA]
cphyParams1.calibrationPreambleFormat = 'format_1'
cphyParams1.enableProgSeq = True
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
cphyParams1.tlpxDuration = 500.0
cphyParams1.useAlp = False

cphyPattern1.hsData = [42, 0]
cphyPattern1.hsDataMode = 'prbs'
cphyPattern1.hsPrbsOrder = 9
cphyPattern1.hsPrbsSeed = None
cphyPattern1.hsSymbols = '22200000000000'
cphyPattern1.lpBits = '11'
cphyPattern1.packetSize = 1000
cphyPattern1.patternType = 'lpOnly'
cphyPattern1.sameDataInEachPacket = True
cphyPattern1.stopDuration = 0

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 500.0
mipiClockConfig1.referenceClocks = None

mipiCphyGenerator1.clockConfig = mipiClockConfig1
mipiCphyGenerator1.commonNoise = None
mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.hsPostTaps = [0]
mipiCphyGenerator1.hsPreTaps = [0]
mipiCphyGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.jitterInjection = None
mipiCphyGenerator1.lanes = [1, 2, 3, 4]
mipiCphyGenerator1.lpHighVoltages = [1200.0]
mipiCphyGenerator1.lpLowVoltages = [0.0]
mipiCphyGenerator1.params = cphyParams1
mipiCphyGenerator1.pattern = cphyPattern1
mipiCphyGenerator1.resetPatternMemory = True
mipiCphyGenerator1.splitDataAcrossLanes = False
mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

powerOffPattern.hsData = [42, 0]
powerOffPattern.hsDataMode = 'prbs'
powerOffPattern.hsPrbsOrder = 9
powerOffPattern.hsPrbsSeed = None
powerOffPattern.hsSymbols = '22200000000000'
powerOffPattern.lpBits = '00000000000000000000000000000000'
powerOffPattern.packetSize = 1000
powerOffPattern.patternType = 'lpOnly'
powerOffPattern.sameDataInEachPacket = True
powerOffPattern.stopDuration = 0

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

visaInstrument1.address = 'TCPIP0::169.254.197.103::inst0::INSTR'

#! TEST PROCEDURE
# Check Version
visaInstrument1.connect()

svtVersion = getSvtVersion()
if svtVersion < calOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, calOptions.minVersion))


iesp = getIespInstance()
lanes = mipiCphyGenerator1.lanes

# Initialize generator
mipiCphyGenerator1.lanes = calOptions.calLanes
mipiCphyGenerator1.lpLanes = calOptions.calLanes
mipiClockConfig1.dataRate = calOptions.calDataRate
mipiCphyGenerator1.setup()

#Enable calibration mode. Ensures no previously stored cal data is being applied.
iesp = getIespInstance()
iesp.writeSubPartRegister(0x0930, 0x00, 0x00)   # calibration mode

# Define results dictionary
measuredLpLowDict = dict()
measuredLpHighDict = dict()

for lane in range(1,5,1) :
    measuredLpLowDict[lane] = dict()
    measuredLpHighDict[lane] = dict()
    for programmedLpLow in calOptions.lpLowValues :
        measuredLpLowDict[lane][programmedLpLow] = list()
    for programmedLpHigh in calOptions.lpHighValues :
        measuredLpHighDict[lane][programmedLpHigh] = list()

wires = ['A', 'B', 'C']

for lane in mipiCphyGenerator1.lanes :
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)
    for wire in range(0,3,1):
        waitForOkDialog("Connect Data Lane=%s, Wire=%s to Multimeter" % (lane,wires[wire]))

        for programmedLpLow in calOptions.lpLowValues :
            print("Measuring at %f mV LP Low..." % programmedLpLow)

            # Update the generator
            mipiCphyGenerator1.lpLowVoltages = [programmedLpLow]
            mipiCphyGenerator1.cphyPattern = powerOffPattern
            mipiCphyGenerator1.update()
            iesp.setMipiLpStateWhenDisabled('000', lanes)

            # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane
            (measuredLpLow) = getVoltage()

            # Accumulate the list into the dictionaries
            measuredLpLowDict[lane][programmedLpLow].append( measuredLpLow)

            # Display information messages
            print("Wire %s: Programmed % f mV LP Low, and measured %f mV..." % (wires[wire],programmedLpLow, measuredLpLow))

        # Restore the generator
        mipiCphyGenerator1.lpLowVoltages = [0.0]
        mipiCphyGenerator1.update()

        # Now do LP High
        for programmedLpHigh in calOptions.lpHighValues :
            print("Measuring at %f mV LP High..." % programmedLpHigh)

            # Update the generator
            mipiCphyGenerator1.lpHighVoltages = [programmedLpHigh]
            mipiCphyGenerator1.cphyPattern = cphyPattern1
            mipiCphyGenerator1.update()


            # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane
            (measuredLpHigh) = getVoltage()


            # Accumulate the list into the dictionaries
            measuredLpHighDict[lane][programmedLpHigh].append( measuredLpHigh )

            # Display information messages
            print("Wire %s: Programmed % f mV LP High, and measured %f mV..." % (wires[wire],programmedLpHigh, measuredLpHigh))


# Dump the raw measurement values into a csv file
writeRawData(measuredLpLowDict, measuredLpHighDict)

if performValidationOnCollectedData(measuredLpLowDict, measuredLpHighDict) :
    writeNoteForTestRun("Pass")
    failFlag = 0
else :
    writeNoteForTestRun("Fail")
    failFlag = 1

if failFlag == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
elif failFlag:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
