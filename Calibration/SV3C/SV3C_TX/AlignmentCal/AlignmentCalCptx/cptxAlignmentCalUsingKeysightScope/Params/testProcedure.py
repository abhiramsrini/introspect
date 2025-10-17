# SVT Test
# SVT version 24.1.0
# Test saved 2024-03-08_1355
# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 3e1b8092a19c3401d5a0553819b159ab
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
cphyPattern1 = _create('cphyPattern1', 'SvtMipiCphyCustomPattern')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

# skew = 0
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
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel4")
sleepMillis(calOptions.scopeAutoScaleDelay)


# Clear display
osci.write(":CDISplay")

# Make sure we're getting mean values
osci.write(":MEASure:STATistics MEAN")


# Measure average voltage of channel 1 to set trigger level
osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
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

calOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.30.30.00::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=1000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5], displayOrder=(0, 7.0))
calOptions.addField('scopeSetupFile', descrip='''This is a placeholder in case we store a scope setup file as part of the script.''', attrType=str, iespInstanceName='any', defaultVal='Placeholder', displayOrder=(0, 8.0))
calOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence.''', attrType=float, iespInstanceName='any', defaultVal=3e-12, displayOrder=(0, 9.0))
calOptions.addField('scopeConnectionTimeout', descrip='''Connection timeout''', attrType=float, iespInstanceName='any', defaultVal=5000.0, displayOrder=(0, 10.0))
calOptions.addField('minVersion', descrip='''Minimum IntrospectESP version supported by this script''', attrType=str, iespInstanceName='any', defaultVal='22.2.1', displayOrder=(0, 11.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.scopeIPAddress = 'TCPIP0::10.30.30.00::inst0::INSTR'
calOptions.scopeMeasurementDelay = 1000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4]
calOptions.calRates = [80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5]
calOptions.scopeSetupFile = 'Placeholder'
calOptions.deltaTimeThreshold = 3e-12
calOptions.scopeConnectionTimeout = 5000.0
calOptions.minVersion = '24.1.0'
calOptions.callCustomInitMethod()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa
#connect to scope
rm = pyvisa.ResourceManager()
osci = rm.open_resource(scopeIpAddress)
osci.lock_excl()

osci.read_termination = '\n'
osci.write_termination = '\n'
osci.timeout = calOptions.scopeConnectionTimeout


return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
channelString = "CHANNEL%d" % channel
commandString = ":MEASure:DELTatime CHANnel1,"+channelString
osci.write(commandString)

sleepMillis(calOptions.scopeMeasurementDelay)

currentDeltaTime = 0
commandString = ":MEASure:DELTatime? CHANnel1,"+channelString
for i in range(calOptions.numAverages) :
    varAmp = osci.query_ascii_values(commandString)
    currentDeltaTime += varAmp[0]
currentDeltaTime = currentDeltaTime / calOptions.numAverages

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False

performScopeCal.args = 'lane, dataRate'
performScopeCal.code = r'''if dataRate >= 3125.0000001:
    osRatio = 2
elif dataRate >= 1500.0000001:
    osRatio = 4
elif dataRate >= 781.2500001:
    osRatio = 8
elif dataRate >= 390.6250001:
    osRatio = 16
elif dataRate >= 195.3125001:
    osRatio = 32
else:
    osRatio = 64

halfUi = 1000000 / (dataRate * osRatio) / 2 * 1e-12
halfUi = halfUi + 3e-12

if lane == 1 :
    print("Performing coarse loop...")
    coarseA = 0
    fineA = 0

    done = 0
    accumulatedCoarseB = 0
    accumulatedCoarseC = 0
    iesp.setMipiCoarseSkews(coarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])
    while not done:
        currentDelayB = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayB)
        if abs(currentDelayB) < halfUi :
            done=1
            break
        numSlipsB = round(currentDelayB/(2*halfUi))
        accumulatedCoarseB += numSlipsB
        iesp.setMipiCoarseSkews(coarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayC = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayC)
        if abs(currentDelayC) < halfUi :
            done=1
            break
        numSlipsC = round(currentDelayC/(2*halfUi))
        accumulatedCoarseC += numSlipsC
        iesp.setMipiCoarseSkews(coarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])

    print("Coarse B is %d..." % accumulatedCoarseB)
    print("Coarse C is %d..." % accumulatedCoarseC)

    coarseDelayList = [coarseA, accumulatedCoarseB, accumulatedCoarseC]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFineB = 0
    accumulatedFineC = 0
    iesp.setMipiFineSkews(fineA, accumulatedFineB, accumulatedFineC, [lane])
    while not done:
        currentDelayB = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayB)
        if abs(currentDelayB) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineB += -1*currentDelayB
        iesp.setMipiFineSkews(fineA, accumulatedFineB*1e12, accumulatedFineC*1e12, [lane])

    done = 0
    while not done:
        currentDelayC = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayC)
        if abs(currentDelayC) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineC += -1*currentDelayC
        iesp.setMipiFineSkews(fineA, accumulatedFineB*1e12, accumulatedFineC*1e12, [lane])

    print("Fine B is %f ps..." % (accumulatedFineB*1e12))
    print("Fine C is %f ps..." % (accumulatedFineC*1e12))

    #mult by 1e15 for fs
    fineDelayList = [fineA, accumulatedFineB*1e15, accumulatedFineC*1e15]

else:
    print("Performing coarse loop...")
    done = 0
    accumulatedCoarseA = 0
    accumulatedCoarseB = 0
    accumulatedCoarseC = 0
    iesp.setMipiCoarseSkews(accumulatedCoarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])
    while not done:
        currentDelayA = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayA)
        if abs(currentDelayA) < halfUi :
            done=1
            break
        numSlipsA = round(currentDelayA/(2*halfUi))
        accumulatedCoarseA += numSlipsA
        iesp.setMipiCoarseSkews(accumulatedCoarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayB = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayB)
        if abs(currentDelayB) < halfUi :
            done=1
            break
        numSlipsB = round(currentDelayB/(2*halfUi))
        accumulatedCoarseB += numSlipsB
        iesp.setMipiCoarseSkews(accumulatedCoarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])
    # Now repeat for Channel 4
    done = 0
    while not done:
        currentDelayC = measureDeltaTime(4)
        print("Detected delay on channel 4 is %e..." % currentDelayC)
        if abs(currentDelayC) < halfUi :
            done=1
            break
        numSlipsC = round(currentDelayC/(2*halfUi))
        accumulatedCoarseC += numSlipsC
        iesp.setMipiCoarseSkews(accumulatedCoarseA, accumulatedCoarseB, accumulatedCoarseC, [lane])

    print("Coarse A is %d..." % accumulatedCoarseA)
    print("Coarse B is %d..." % accumulatedCoarseB)
    print("Coarse C is %d..." % accumulatedCoarseC)

    coarseDelayList = [accumulatedCoarseA, accumulatedCoarseB, accumulatedCoarseC]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFineA = 0
    accumulatedFineB = 0
    accumulatedFineC = 0
    iesp.setMipiFineSkews(accumulatedFineA, accumulatedFineB, accumulatedFineC, [lane])
    while not done:
        currentDelayA = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayA)
        if abs(currentDelayA) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineA += -1*currentDelayA
        iesp.setMipiFineSkews(accumulatedFineA*1e12, accumulatedFineB*1e12, accumulatedFineC*1e12, [lane])
    # Now do channel 3
    done = 0
    while not done:
        currentDelayB = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayB)
        if abs(currentDelayB) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineB += -1*currentDelayB
        iesp.setMipiFineSkews(accumulatedFineA*1e12, accumulatedFineB*1e12, accumulatedFineC*1e12, [lane])
    # Now do channel 4
    done = 0
    while not done:
        currentDelayC = measureDeltaTime(4)
        print("Detected delay on channel 4 is %e..." % currentDelayC)
        if abs(currentDelayC) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineC += -1*currentDelayC
        iesp.setMipiFineSkews(accumulatedFineA*1e12, accumulatedFineB*1e12, accumulatedFineC*1e12, [lane])

    print("Fine A is %f ps..." % (accumulatedFineA*1e12))
    print("Fine B is %f ps..." % (accumulatedFineB*1e12))
    print("Fine C is %f ps..." % (accumulatedFineC*1e12))

    #multiply by 1e15 to store as fs
    fineDelayList = [accumulatedFineA*1e15, accumulatedFineB*1e15, accumulatedFineC*1e15]


return (coarseDelayList, fineDelayList)
'''
performScopeCal.wantAllVarsGlobal = False

writeCalFile.args = 'measuredCoarseDelayDict, measuredFineDelayDict'
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
    print("section type : tx_skew_calibration_data_cphy", file=outFile)
    print("num lanes : 4", file=outFile)
    print("num data rates : %d" % len(calOptions.calRates), file=outFile)

    for rate in calOptions.calRates:
        print("#Data Rate = %f XcvrRate = %d" % (rate, rate*64), file=outFile)
        print("%f " % rate, file=outFile)
        for wire in [0,1,2]:
            for lane in [1, 2, 3, 4]:
                print("%d," % measuredCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
            print("", file=outFile)
        for wire in [0,1,2]:
            for lane in [1, 2, 3, 4]:
                print("%d," % measuredFineDelayDict[lane][rate][wire], end=' ', file=outFile)
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
cphyParams1.tTaSureDuration = 1.5
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


autoscaleScope._showInList = False
autoscaleScope._showInTabs = False
initScope._showInList = False
measureDeltaTime._showInList = False
performScopeCal._showInList = False
writeCalFile._showInList = False
writeCalFile._showInTabs = False
writeRawData._showInList = False
writeRawData._showInTabs = False

cphyParams1._showInList = False
cphyPattern1._showInList = False
mipiCphyGenerator1._showInList = False
resultFolderCreator1._showInList = False
#! TEST PROCEDURE
# Check Version
svtVersion = getSvtVersion()
if svtVersion < calOptions.minVersion:
    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, calOptions.minVersion))


iesp = getIespInstance()
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

# Initialize generator
mipiCphyGenerator1.lanes = calOptions.calLanes
mipiCphyGenerator1.setup()

# Define results dictionary
measuredCoarseDelayDict = dict()
measuredFineDelayDict = dict()
for lane in [1, 2, 3, 4] :
   measuredCoarseDelayDict[lane] = dict()
   measuredFineDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      measuredCoarseDelayDict[lane][dataRate] = dict()
      measuredFineDelayDict[lane][dataRate] = dict()
      for wire in [0,1,2]:
          measuredCoarseDelayDict[lane][dataRate][wire] = 0
          measuredFineDelayDict[lane][dataRate][wire] = 0

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

for lane in mipiCphyGenerator1.lanes :
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)
    if lane==1 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch2, Wire B to Ch3, and Wire C to Ch4. IMPORTANT: Keep Lane 1A connected to Ch1' % lane
    waitForGuiOkDialog(myString)

    measuredCoarseDelayDict[lane] = dict()
    measuredFineDelayDict[lane] = dict()

    #auto scale once per lane
    autoScale = True

    for dataRate in calOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        measuredCoarseDelayDict[lane][dataRate] = list()
        measuredFineDelayDict[lane][dataRate] = list()

        iesp.writeSubPartRegister(0x0930, 0x00, 0x01) # enable cal mode
        mipiClockConfig1.dataRate = dataRate
        mipiCphyGenerator1.setup()
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern

        # Prepare scope for measurement
        if(autoScale):
            autoscaleScope()
            autoScale = False

        # Use scope to measure values
        (coarseDelayList, fineDelayList) = performScopeCal(lane,dataRate)

        # Assemble into dictionaries
        measuredCoarseDelayDict[lane][dataRate] = coarseDelayList
        measuredFineDelayDict[lane][dataRate] = fineDelayList

writeCalFile(measuredCoarseDelayDict, measuredFineDelayDict)

# Disable alignment pattern
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
mipiCphyGenerator1.setup()
