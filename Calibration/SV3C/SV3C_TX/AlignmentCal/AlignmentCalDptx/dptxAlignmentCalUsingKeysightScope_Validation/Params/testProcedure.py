# SVT Test
# SVT version 21.4.0
# Test saved 2023-06-07_1744
# Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: 3239acbee8c0235b94dd27bb1952a51b
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.

autoscaleScope = SvtFunction()
autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(validationOptions.scopeAutoScaleDelay)

# Make sure all skew are at 0. This is not reset by default
osci.write(":CALibrate:SKEW CHANnel1,0")
osci.write(":CALibrate:SKEW CHANnel2,0")
osci.write(":CALibrate:SKEW CHANnel3,0")
osci.write(":CALibrate:SKEW CHANnel4,0")

# Display the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")

# Autoscale the channels
osci.write(":AUToscale:VERTical CHANnel1")
sleepMillis(validationOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(validationOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(validationOptions.scopeAutoScaleDelay)


# Clear display
osci.write(":CDISplay")

# Make sure we're getting mean values
osci.write(":MEASure:STATistics MEAN")


# Measure average voltage of channel 1 to set trigger level
osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
sleepMillis(validationOptions.scopeAutoScaleDelay)
varAverage = osci.query_ascii_values(":MEASure:VAVerage? DISPlay,CHANnel1")
currentValue = varAverage[0]

triggerValue = currentValue

# Set trigger level to be just below the mid-point of the 3-level waveform
myString = ":TRIGger:LEVel CHANNEL1, %f" % triggerValue
osci.write(myString)

# Clear display
osci.write(":CDISplay")
sleepMillis(100)

# Set timebase to proper value
osci.write(":TIMebase:SCALe 100e-012")

# Turn averaging on
osci.write(":ACQuire:AVERage:COUNt 16")
osci.write(":ACQuire:AVERage 1")

# Define delta-time measurement parameters
osci.write(":MEASure:DELTatime:DEFine RISing,1,MIDDle,RISing,1,MIDDle")
'''
autoscaleScope.wantAllVarsGlobal = False
autoscaleScope._showInList = False

initScope = SvtFunction()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa as visa
#connect to scope
rm = visa.ResourceManager()
osci = rm.open_resource(scopeIpAddress)

#print "Setting Read Termination..."
osci.read_termination = '\n'
#print "Setting Write Termination..."
osci.write_termination = '\n'
#print "Setting connection timeout..."
osci.timeout = validationOptions.scopeConnectionTimeout


return osci
'''
initScope.wantAllVarsGlobal = False
initScope._showInList = False

measureDeltaTime = SvtFunction()
measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
channelString = "CHANNEL%d" % channel
commandString = ":MEASure:DELTatime CHANnel1,"+channelString
osci.write(commandString)

sleepMillis(validationOptions.scopeMeasurementDelay)

currentDeltaTime = 0
commandString = ":MEASure:DELTatime? CHANnel1,"+channelString
for i in range(validationOptions.numAverages) :
    varAmp = osci.query_ascii_values(commandString)
    currentDeltaTime += varAmp[0]
currentDeltaTime = currentDeltaTime / validationOptions.numAverages

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False
measureDeltaTime._showInList = False

performScopeMeasurement = SvtFunction()
performScopeMeasurement.args = 'lane, dataRate'
performScopeMeasurement.code = r'''if lane == 1 :
    currentDelayPos = 0
    currentDelayNeg = measureDeltaTime(2)

    delayList = [currentDelayPos, currentDelayNeg]

elif lane == 5:
    currentDelayPos = measureDeltaTime(2)
    currentDelayNeg = measureDeltaTime(3)

    delayList = [currentDelayPos, currentDelayNeg]

else:
    currentDelayPos = measureDeltaTime(2)
    currentDelayNeg = measureDeltaTime(3)

    delayList = [currentDelayPos, currentDelayNeg]

return delayList
'''
performScopeMeasurement.wantAllVarsGlobal = False
performScopeMeasurement._showInList = False

performValidationOnCollectedData = SvtFunction()
performValidationOnCollectedData.args = 'fineDelayDict'
performValidationOnCollectedData.code = r'''print("Checking measured data...")
for rate in validationOptions.calRates :
    for lane in validationOptions.calLanes :
        for wire in range(2) :
            measuredError = abs( fineDelayDict[lane][rate][wire])
            if measuredError > validationOptions.deltaTimeThreshold :
                print("Found a failing condition on Lane %d..." % lane)
                print("Measured error is %g s..." % measuredError)
                return False

return True
'''
performValidationOnCollectedData.wantAllVarsGlobal = False
performValidationOnCollectedData._showInList = False

writeRawData = SvtFunction()
writeRawData.args = 'delayDict'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = validationOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = validationOptions.serialNumber + "_DptxAlignmentValidationData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("DPTX Alignment Validation Data", file=outFile)
    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print("Lane, Data Rate, Skew Pos, Skew Neg", file=outFile)
    for lane in validationOptions.calLanes :
        for dataRate in validationOptions.calRates :
            print("%d, %f, %g, %g, " % (lane, dataRate, delayDict[lane][dataRate][0], delayDict[lane][dataRate][1]), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False
writeRawData._showInList = False



dphyColorBarPattern1 = SvtMipiDphyCsiColorBarPattern()
dphyColorBarPattern1.enableCsiEpd = False
dphyColorBarPattern1.errorInsertion = None
dphyColorBarPattern1.frameBlankingMode = 'frameRate'
dphyColorBarPattern1.frameRate = 4.0
dphyColorBarPattern1.gaussianBlurRadius = 0
dphyColorBarPattern1.horizLineTime = 65800.0
dphyColorBarPattern1.imageFormat = 'CSI_RGB888'
dphyColorBarPattern1.imageHeight = 480
dphyColorBarPattern1.imageWidth = 640
dphyColorBarPattern1.lineNumbering = 'disabled'
dphyColorBarPattern1.lineTimeMode = 'lineTimeTotal'
dphyColorBarPattern1.preBuiltColorBar = ColorBar_ctsHsTestPattern
dphyColorBarPattern1.timeUnits = 'nanosecond'
dphyColorBarPattern1.usePreBuiltColorBar = True
dphyColorBarPattern1.virtualChannel = 0
dphyColorBarPattern1.wantFrameNumbering = False
dphyColorBarPattern1._showInList = False

dphyParameters1 = SvtMipiDphyParameters()
dphyParameters1.clockTrailBits = ''
dphyParameters1.clockZeroBits = '0000'
dphyParameters1.hsTrailBits = ''
dphyParameters1.hsZeroBits = '0000'
dphyParameters1.sotBits = '00011101'
dphyParameters1.tAlpClk01Duration = (0.0, 20.0)
dphyParameters1.tAlpClk10Duration = (0.0, 40.0)
dphyParameters1.tAlpHs01Duration = (0.0, 20.0)
dphyParameters1.tAlpHs10Duration = (0.0, 40.0)
dphyParameters1.tAlpxDuration = 120.0
dphyParameters1.tClockLpx01Duration = (0.0, 80.0)
dphyParameters1.tClockPostDuration = (60.0, 60.0)
dphyParameters1.tClockPreDuration = (32.0, 0.0)
dphyParameters1.tClockPrepareDuration = (0.0, 80.0)
dphyParameters1.tClockTrailDuration = (0.0, 80.0)
dphyParameters1.tClockZeroDuration = (0.0, 300.0)
dphyParameters1.tHsExitDuration = 240.0
dphyParameters1.tHsIdleClkHs0Duration = (0.0, 60.0)
dphyParameters1.tHsIdlePostDuration = 8
dphyParameters1.tHsIdlePreDuration = 8
dphyParameters1.tHsLpx01Duration = (0.0, 80.0)
dphyParameters1.tHsPrepareDuration = (5.0, 60.0)
dphyParameters1.tHsTrailDuration = (8.0, 60.0)
dphyParameters1.tHsZeroDuration = (10.0, 145.0)
dphyParameters1.tTaGetDuration = 5
dphyParameters1.tTaGoDuration = 4.0
dphyParameters1.tTaSureDuration = 1.5
dphyParameters1.tlpxDuration = 80.0
dphyParameters1.useAlp = False
dphyParameters1.usePreambleSequence = False
dphyParameters1._showInList = False

mipiProtocol = SvtMipiProtocol()
mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig = SvtRefClocksConfig()
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

mipiClockConfig1 = SvtMipiClockConfig()
mipiClockConfig1.dataRate = 800.0
mipiClockConfig1.referenceClocks = refClocksConfig
mipiClockConfig1.sscEnabled = False

mipiDphyGenerator1 = SvtMipiDphyGenerator()
mipiDphyGenerator1.clockConfig = mipiClockConfig1
mipiDphyGenerator1.clockSkew = 0.0
mipiDphyGenerator1.continuousClock = False
mipiDphyGenerator1.dataLanes = [1, 2, 3, 4]
mipiDphyGenerator1.dataSkews = [0.0]
mipiDphyGenerator1.hsClockCommonVoltage = 200.0
mipiDphyGenerator1.hsClockPostTap = 0
mipiDphyGenerator1.hsClockPreTap = 0
mipiDphyGenerator1.hsClockVoltageAmplitude = 200.0
mipiDphyGenerator1.hsDataCommonVoltages = [200.0]
mipiDphyGenerator1.hsDataPostTaps = [0]
mipiDphyGenerator1.hsDataPreTaps = [0]
mipiDphyGenerator1.hsDataVoltageAmplitudes = [200.0]
mipiDphyGenerator1.jitterInjection = None
mipiDphyGenerator1.lpClockHighVoltage = 1200.0
mipiDphyGenerator1.lpClockLowVoltage = 0.0
mipiDphyGenerator1.lpDataHighVoltages = [1200.0]
mipiDphyGenerator1.lpDataLowVoltages = [0.0]
mipiDphyGenerator1.params = dphyParameters1
mipiDphyGenerator1.pattern = dphyColorBarPattern1
mipiDphyGenerator1.resetPatternMemory = True
mipiDphyGenerator1.splitDataAcrossLanes = True
mipiDphyGenerator1._showInList = False

resultFolderCreator1 = SvtResultFolderCreator()
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'
resultFolderCreator1._showInList = False

validationOptions = SvtDataRecord()
validationOptions.addField('serialNumber', descrip='''Serial number for device under test''', attrType=str, defaultVal='1234', displayOrder=(0, 1))
validationOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2))
validationOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds''', attrType=float, defaultVal=1000.0, displayOrder=(0, 3))
validationOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after the scope auto scale funtion.''', attrType=float, defaultVal=2000.0, displayOrder=(0, 4))
validationOptions.addField('numAverages', descrip='''Number of times the measurement is queried from the scope.''', attrType=int, defaultVal=100, displayOrder=(0, 5))
validationOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6))
validationOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, attrSubType=float, defaultVal=[80.0, 125.0, 187.5, 6500.0], displayOrder=(0, 7))
validationOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence''', attrType=float, defaultVal=1e-11, displayOrder=(0, 8))
validationOptions.addField('scopeConnectionTimeout', descrip='''Scope connection timeout.''', attrType=float, defaultVal=10000.0, displayOrder=(0, 9))
validationOptions.addField('minVersion', descrip='''Minimum Introspect ESP software version that is supported by this script.''', attrType=str, defaultVal='3.5.55', displayOrder=(0, 10))
validationOptions.addMethod('_customInit',
	'',
	r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
	False)
validationOptions.serialNumber = '1234'
validationOptions.scopeIPAddress = 'TCPIP0::10.20.20.200::inst0::INSTR'
validationOptions.scopeMeasurementDelay = 1000.0
validationOptions.scopeAutoScaleDelay = 2000.0
validationOptions.numAverages = 100
validationOptions.calLanes = [1, 2, 3, 4]
validationOptions.calRates = [80.0, 125.0, 187.5, 6500.0]
validationOptions.deltaTimeThreshold = 1e-11
validationOptions.scopeConnectionTimeout = 10000.0
validationOptions.minVersion = '3.5.55'
validationOptions.callCustomInitMethod()

testAsComponent1 = SvtTestAsComponent()
testAsComponent1.componentClassName = 'dptxAlignmentValUsingKeysight'
testAsComponent1.dataRecord = validationOptions
testAsComponent1.description = 'Regression script for validating timing alignment on the SV3C D-PHY Generator'
testAsComponent1.excludeGlobalClockConfig = True
testAsComponent1.excludedComponents = []
testAsComponent1.mainMethodName = 'run'
testAsComponent1.resultType = 'CsvData'
testAsComponent1.returnValue = r'''

'''
testAsComponent1.showMessages = True
testAsComponent1.usesIespHardware = True
testAsComponent1.viewSubComponents = []
testAsComponent1._showInList = False



#! TEST PROCEDURE
# Check Version
svtVersion = getSvtVersion()
if svtVersion < validationOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))

iesp = getIespInstance()
maxDataRate = iesp.getLimitMaximum("dataRate")

if maxDataRate != 6500:
    validationOptions.calRates = [80.0, 125.0, 187.5]


# Connect to scope
osci = initScope(validationOptions.scopeIPAddress)

# Initialize generator
fileName = "GeneratedDphyPattern_compiled.csv"
mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
mipiDphyGenerator1.dataLanes = validationOptions.calLanes
mipiDphyGenerator1.setup()

# Define results dictionary
measuredCoarseDelayDict = dict()
measuredFineDelayDict = dict()

# Start main loop
for lane in validationOptions.calLanes:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring D-PHY Lane %d..." % lane)
    if lane == 1 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch1, Wire Neg to Ch2' % lane
    elif lane == 5:
        myString = 'Please connect clock signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1'
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1' % lane
    waitForGuiOkDialog(myString)

    measuredFineDelayDict[lane] = dict()
    autoScale = True

    for dataRate in validationOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        measuredFineDelayDict[lane][dataRate] = list()

        iesp.writeSubPartRegister(0x0930, 0x00, 0x00) # clear cal mode
        fileName = "GeneratedDphyPattern_compiled.csv"
        mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
        mipiClockConfig1.dataRate = dataRate
        mipiDphyGenerator1.setup()
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern

        # Prepare scope for measurement
        autoscaleScope()

        # Use scope to measure values
        delayList = performScopeMeasurement(lane,dataRate)

        # Assmeble into dictionaries
        measuredFineDelayDict[lane][dataRate] = delayList

# Write all collected data points to file
writeRawData(measuredFineDelayDict)

# Disable alignment pattern
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
mipiDphyGenerator1.setup()

if performValidationOnCollectedData(measuredFineDelayDict) :
    writeNoteForTestRun("Pass")
else :
    writeNoteForTestRun("Fail")
