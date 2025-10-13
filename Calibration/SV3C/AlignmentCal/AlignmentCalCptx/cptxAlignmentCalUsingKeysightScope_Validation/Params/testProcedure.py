# SVT Test
# SVT version 24.1.0
# Test saved 2024-03-08_1355
# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 6dc0ab6ec71c962274dbf04b11ec9834
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeMeasurement = _create('performScopeMeasurement', 'SvtFunction', iespName='None')
performValidationOnCollectedData = _create('performValidationOnCollectedData', 'SvtFunction', iespName='None')
validationOptions = _create('validationOptions', 'SvtDataRecord', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

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
osci.write(":CHANnel4:DISPlay 1")

# Autoscale the channels
osci.write(":AUToscale:VERTical CHANnel1")
sleepMillis(validationOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(validationOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(validationOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel4")
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

initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa
#connect to scope
rm = pyvisa.ResourceManager()
osci = rm.open_resource(scopeIpAddress)

osci.read_termination = '\n'
osci.write_termination = '\n'
osci.timeout = validationOptions.scopeConnectionTimeout


return osci
'''
initScope.wantAllVarsGlobal = False

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

performScopeMeasurement.args = 'lane, dataRate'
performScopeMeasurement.code = r'''if lane == 1 :
    currentDelayA = 0
    currentDelayB = measureDeltaTime(2)
    currentDelayC = measureDeltaTime(3)


    delayList = [currentDelayA, currentDelayB, currentDelayC]

else:
    currentDelayA = measureDeltaTime(2)
    currentDelayB = measureDeltaTime(3)
    currentDelayC = measureDeltaTime(4)
    delayList = [currentDelayA, currentDelayB, currentDelayC]


return (delayList)
'''
performScopeMeasurement.wantAllVarsGlobal = False

performValidationOnCollectedData.args = 'fineDelayDict'
performValidationOnCollectedData.code = r'''print("Checking measured data...")
for rate in validationOptions.calRates :
    for lane in validationOptions.calLanes :
        for wire in range(3) :
            measuredError = abs( fineDelayDict[lane][rate][wire])
            if measuredError > validationOptions.deltaTimeThreshold :
                print("Found a failing condition on Lane %d..." % lane)
                print("Measured error is %g s..." % measuredError)
                return False

return True
'''
performValidationOnCollectedData.wantAllVarsGlobal = False

validationOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
validationOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.30.30.00::inst0::INSTR', displayOrder=(0, 2.0))
validationOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=1000.0, displayOrder=(0, 3.0))
validationOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
validationOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
validationOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
validationOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[80.0, 125.0, 187.0], displayOrder=(0, 7.0))
validationOptions.addField('scopeSetupFile', descrip='''This is a placeholder in case we store a scope setup file as part of the script.''', attrType=str, iespInstanceName='any', defaultVal='Placeholder', displayOrder=(0, 8.0))
validationOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence.''', attrType=float, iespInstanceName='any', defaultVal=2e-11, displayOrder=(0, 9.0))
validationOptions.addField('scopeConnectionTimeout', descrip='''Scope connection timeout in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=5000.0, displayOrder=(0, 10.0))
validationOptions.addField('minVersion', descrip='''Minimum Introspect ESP software version that is supported by this script.''', attrType=str, iespInstanceName='any', defaultVal='22.2.1', displayOrder=(0, 11.0))
validationOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
validationOptions.serialNumber = '1234'
validationOptions.scopeIPAddress = 'TCPIP0::10.30.30.00::inst0::INSTR'
validationOptions.scopeMeasurementDelay = 1000.0
validationOptions.scopeAutoScaleDelay = 2000.0
validationOptions.numAverages = 100
validationOptions.calLanes = [1, 2, 3, 4]
validationOptions.calRates = [80.0, 125.0, 187.0]
validationOptions.scopeSetupFile = 'Placeholder'
validationOptions.deltaTimeThreshold = 2e-11
validationOptions.scopeConnectionTimeout = 5000.0
validationOptions.minVersion = '24.1.0'
validationOptions.callCustomInitMethod()
writeRawData.args = 'delayDict'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = validationOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = validationOptions.serialNumber + "_CptxAlignmentValidationData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("CPTX Alignment Validation Data", file=outFile)
    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print("Lane, Data Rate, WireA, WireB, WireC", file=outFile)
    for lane in validationOptions.calLanes :
        for dataRate in validationOptions.calRates :
            print("%d, %f, %g, %g, %g," % (lane, dataRate, delayDict[lane][dataRate][0], delayDict[lane][dataRate][1], delayDict[lane][dataRate][2]), file=outFile)
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
cphyParams1.tTaSureDuration = 1.5
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 50.0
cphyParams1.useAlp = False

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


autoscaleScope._showInList = False
initScope._showInList = False
measureDeltaTime._showInList = False
performScopeMeasurement._showInList = False
performValidationOnCollectedData._showInList = False
writeRawData._showInList = False

cphyParams1._showInList = False
mipiCphyGenerator1._showInList = False
resultFolderCreator1._showInList = False
#! TEST PROCEDURE
# Check Version
svtVersion = getSvtVersion()
if svtVersion < validationOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))

iesp = getIespInstance()
# Connect to scope
osci = initScope(validationOptions.scopeIPAddress)

# Initialize generator
mipiCphyGenerator1.lanes = validationOptions.calLanes
mipiCphyGenerator1.setup()

# Define results dictionary
measuredCoarseDelayDict = dict()
measuredFineDelayDict = dict()

for lane in mipiCphyGenerator1.lanes :
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)
    if lane==1 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch2, Wire B to Ch3, and Wire C to Ch4. IMPORTANT: Keep Lane 1A connected to Ch1' % lane
    waitForGuiOkDialog(myString)

    #measuredCoarseDelayDict[lane] = dict()
    measuredFineDelayDict[lane] = dict()

    #auto scale once per lane
    autoScale = True

    for dataRate in validationOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        #measuredCoarseDelayDict[lane][dataRate] = list()
        measuredFineDelayDict[lane][dataRate] = list()

        iesp.writeSubPartRegister(0x0930, 0x00, 0x00) # enable cal mode
        mipiClockConfig1.dataRate = dataRate
        mipiCphyGenerator1.setup()
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern

        # Prepare scope for measurement
        autoscaleScope()

        # Use scope to measure values
        delayList = performScopeMeasurement(lane,dataRate)

        # Assemble into dictionaries
        measuredFineDelayDict[lane][dataRate] = delayList

writeRawData(measuredFineDelayDict)

# Disable alignment pattern
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
mipiCphyGenerator1.setup()

if performValidationOnCollectedData(measuredFineDelayDict) :
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
