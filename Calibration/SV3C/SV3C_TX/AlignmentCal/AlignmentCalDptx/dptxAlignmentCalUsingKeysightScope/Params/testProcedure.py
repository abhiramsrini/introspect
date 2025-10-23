# SVT Test
# SVT version 23.1.0
# Test saved 2023-03-13_1412
# Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: a28bda9f0b63e094e8380ed22f2b48db
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
coarseClkSkewsToString = _create('coarseClkSkewsToString', 'SvtFunction', iespName='None')
coarseDataSkewsToString = _create('coarseDataSkewsToString', 'SvtFunction', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')

dphyColorBarPattern1 = _create('dphyColorBarPattern1', 'SvtMipiDphyCsiColorBarPattern')
dphyParameters1 = _create('dphyParameters1', 'SvtMipiDphyParameters')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiDphyGenerator1 = _create('mipiDphyGenerator1', 'SvtMipiDphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

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
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
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

calOptions.addField('serialNumber', descrip='''Serial number for device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.30.30.00::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds''', attrType=float, iespInstanceName='any', defaultVal=1000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after the scope auto scale funtion.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is queried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5, 6500.0], displayOrder=(0, 7.0))
calOptions.addField('scopeSetupFile', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='Placeholder', displayOrder=(0, 8.0))
calOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence''', attrType=float, iespInstanceName='any', defaultVal=3e-12, displayOrder=(0, 9.0))
calOptions.addField('scopeConnectionTimeout', descrip='''Timeout used by PyVisa''', attrType=float, iespInstanceName='any', defaultVal=10000.0, displayOrder=(0, 10.0))
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
calOptions.calLanes = [1, 2, 3, 4, 5]
calOptions.calRates = [80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5, 6500.0]
calOptions.scopeSetupFile = 'Placeholder'
calOptions.deltaTimeThreshold = 3e-12
calOptions.scopeConnectionTimeout = 10000.0
calOptions.callCustomInitMethod()
coarseClkSkewsToString.args = 'Pos, Neg'
coarseClkSkewsToString.code = r'''posCmd = ("00000000%s"%(hex(Pos&0xffffffff)[2:]))[-8:]
negCmd = ("00000000%s"%(hex(Neg&0xffffffff)[2:]))[-8:]

return "%s %s" % (posCmd, negCmd)
'''
coarseClkSkewsToString.wantAllVarsGlobal = False

coarseDataSkewsToString.args = 'Pos, Neg'
coarseDataSkewsToString.code = r'''posCmd = ("00000000%s"%(hex(Pos&0xffffffff)[2:]))[-8:]
negCmd = ("00000000%s"%(hex(Neg&0xffffffff)[2:]))[-8:]

return "%s %s %s %s %s %s %s %s" % (posCmd, negCmd, posCmd, negCmd, posCmd, negCmd, posCmd, negCmd)
'''
coarseDataSkewsToString.wantAllVarsGlobal = False

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
    coarsePos = 0
    finePos = 0

    done = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    laneMask = 0x01 << (lane-1)
    iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(coarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayNeg = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(coarsePos, int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [coarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFineNeg = 0
    iesp.setMipiDataFineSkew(accumulatedFineNeg, finePos, [lane])        #lane 1. neg. pos.
    while not done :
        currentDelayNeg = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, finePos, [lane])

    print("Fine Neg is %f ps..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 for fs
    fineDelayList = [finePos, accumulatedFineNeg*1e15]

elif lane == 5:
    print("Performing coarse loop...")
    done = 0
    accumulatedCoarsePos = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(accumulatedCoarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < halfUi :
            done = 1
            break
        numSlipsPos = round(currentDelayPos/(2*halfUi))
        accumulatedCoarsePos += numSlipsPos
        iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Pos is %d..." % accumulatedCoarsePos)
    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [accumulatedCoarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFinePos = 0
    accumulatedFineNeg = 0
    iesp.setMipiClockFineSkew(accumulatedFineNeg, accumulatedFinePos)
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFinePos += -1*currentDelayPos
        iesp.setMipiClockFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12)
    # Now do channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiClockFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12)
    print("Fine Pos is %f ps ..." % (accumulatedFinePos*1e12))
    print("Fine Neg is %f ps ..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 to store as fs
    fineDelayList = [accumulatedFinePos*1e15, accumulatedFineNeg*1e15]
else:
    print("Performing coarse loop...")
    done = 0
    accumulatedCoarsePos = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    laneMask = 0x01 << (lane-1)
    iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(accumulatedCoarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < halfUi :
            done = 1
            break
        numSlipsPos = round(currentDelayPos/(2*halfUi))
        accumulatedCoarsePos += numSlipsPos
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Pos is %d..." % accumulatedCoarsePos)
    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [accumulatedCoarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFinePos = 0
    accumulatedFineNeg = 0
    iesp.setMipiDataFineSkew(accumulatedFineNeg, accumulatedFinePos, [lane])
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFinePos += -1*currentDelayPos
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12, [lane])
    # Now do channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12, [lane])
    print("Fine Pos is %f ps ..." % (accumulatedFinePos*1e12))
    print("Fine Neg is %f ps ..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 to store as fs
    fineDelayList = [accumulatedFinePos*1e15, accumulatedFineNeg*1e15]

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
    print("speed grade : 1", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type: jitter_calibration_data", file=outFile)
    print("ffffffffffffffffffffffffffffffff00000000000000000000000000000000", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_skew_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("num data rates : %d" % (len(calOptions.calRates) + 1), file=outFile)

    #need to print an extra entry for 4000Mbps. No longer calibrated at this rate but req for backwards compatibility
    print("#Data Rate = 4000", file=outFile)
    print("#Tx Skew Coarse and Fine", file=outFile)
    print("4000", file=outFile)

    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)

    for rate in calOptions.calRates:
        if rate >= 3125.0000001:
            osRatio = 2
        elif rate >= 1500.0000001:
            osRatio = 4
        elif rate >= 781.2500001:
            osRatio = 8
        elif rate >= 390.6250001:
            osRatio = 16
        elif rate >= 195.3125001:
            osRatio = 32
        else:
            osRatio = 64
        print("#Data Rate = %f" % (rate*osRatio), file=outFile)
        print("#Tx Skew Coarse and Fine", file=outFile)
        print("%f " % (rate*osRatio), file=outFile)
        for wire in [0,1]:
            print("%d," % measuredCoarseDelayDict[5][rate][wire], end=' ', file=outFile)    #Clk Data
            print("%d," % measuredCoarseDelayDict[1][rate][wire], end=' ', file=outFile)    #Lane 1
            print("%d," % measuredCoarseDelayDict[2][rate][wire], end=' ', file=outFile)    #Lane 2
            print("%d," % measuredCoarseDelayDict[3][rate][wire], end=' ', file=outFile)    #Lane 3
            print("%d," % measuredCoarseDelayDict[4][rate][wire], end=' ', file=outFile)    #Lane 4
            print("", file=outFile)
        for wire in [0,1]:
            print("%d," % measuredFineDelayDict[5][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[1][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[2][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[3][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[4][rate][wire], end=' ', file=outFile)
            print("", file=outFile)
    print("END SECTION", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False


dphyColorBarPattern1.blankingDuration = 3000.0
dphyColorBarPattern1.enableCsiEpd = False
dphyColorBarPattern1.epdOption = 'option1'
dphyColorBarPattern1.errorInsertion = None
dphyColorBarPattern1.frameBlankingDuration = 30000.0
dphyColorBarPattern1.frameBlankingMode = 'frameRate'
dphyColorBarPattern1.frameRate = 4.0
dphyColorBarPattern1.gaussianBlurRadius = 0
dphyColorBarPattern1.horizLineTime = 65800.0
dphyColorBarPattern1.imageFormat = 'CSI_RGB888'
dphyColorBarPattern1.imageHeight = 480
dphyColorBarPattern1.imageWidth = 640
dphyColorBarPattern1.lineNumbering = 'disabled'
dphyColorBarPattern1.lineTimeMode = 'lineTimeTotal'
dphyColorBarPattern1.numCols = 8
dphyColorBarPattern1.numLongPacketEpdSpacers = 0
dphyColorBarPattern1.numRows = 2
dphyColorBarPattern1.numShortPacketEpdSpacers = 0
dphyColorBarPattern1.preBuiltColorBar = ColorBar_ctsHsTestPattern
dphyColorBarPattern1.rawFormatBayerCell = 'BGGR'
dphyColorBarPattern1.rawValues = None
dphyColorBarPattern1.rgbValues = None
dphyColorBarPattern1.timeUnits = 'nanosecond'
dphyColorBarPattern1.usePreBuiltColorBar = True
dphyColorBarPattern1.valuesMode = 'rgb'
dphyColorBarPattern1.virtualChannel = 0
dphyColorBarPattern1.wantFrameNumbering = False

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
dphyParameters1.tPreamble = 32
dphyParameters1.tTaGetDuration = 5
dphyParameters1.tTaGoDuration = 4.0
dphyParameters1.tTaSureDuration = 1.5
dphyParameters1.tlpxDuration = 80.0
dphyParameters1.useAlp = False
dphyParameters1.usePreambleSequence = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 800.0
mipiClockConfig1.referenceClocks = refClocksConfig
mipiClockConfig1.sscEnabled = False
mipiClockConfig1.sscFrequency = 31.5
mipiClockConfig1.sscSpread = 2.0

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

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'


autoscaleScope._showInList = False
coarseClkSkewsToString._showInList = False
coarseDataSkewsToString._showInList = False
initScope._showInList = False
measureDeltaTime._showInList = False
performScopeCal._showInList = False
writeCalFile._showInList = False

dphyColorBarPattern1._showInList = False
dphyParameters1._showInList = False
mipiDphyGenerator1._showInList = False
resultFolderCreator1._showInList = False
#! TEST PROCEDURE
iesp = getIespInstance()
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

maxDataRate = iesp.getLimitMaximum("dataRate")

if maxDataRate != 6500:
    calOptions.calRates = [80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5]


# Initialize generator
fileName = "GeneratedDphyPattern_compiled.csv"
mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
#mipiDphyGenerator1.usePatternsFile = True
mipiDphyGenerator1.dataLanes = calOptions.calLanes
mipiDphyGenerator1.setup()

# Define results dictionary
measuredCoarseDelayDict = dict()
measuredFineDelayDict = dict()

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

# Declare global dictionary
for lane in range(1,6,1) :
   measuredCoarseDelayDict[lane] = dict()
   measuredFineDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      measuredCoarseDelayDict[lane][dataRate] = dict()
      measuredFineDelayDict[lane][dataRate] = dict()
      for wire in [0,1]:
          measuredCoarseDelayDict[lane][dataRate][wire] = 0
          measuredFineDelayDict[lane][dataRate][wire] = 0

for lane in mipiDphyGenerator1.dataLanes:
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


    autoScale = True

    for dataRate in calOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        measuredCoarseDelayDict[lane][dataRate] = list()
        measuredFineDelayDict[lane][dataRate] = list()

        iesp.writeSubPartRegister(0x0930, 0x00, 0x01) # enable cal mode
        fileName = "GeneratedDphyPattern_compiled.csv"
        mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
       # mipiDphyGenerator1.usePatternsFile = True
        mipiClockConfig1.dataRate = dataRate
        mipiDphyGenerator1.setup()
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern

        # Prepare scope for measurement
        if(autoScale):
            autoscaleScope()
            autoScale = False

        # Use scope to measure values
        (coarseDelayList, fineDelayList) = performScopeCal(lane,dataRate)

        # Assmeble into dictionaries
        measuredCoarseDelayDict[lane][dataRate] = coarseDelayList
        measuredFineDelayDict[lane][dataRate] = fineDelayList

# Disable alignment pattern
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
mipiDphyGenerator1.setup()

writeCalFile(measuredCoarseDelayDict, measuredFineDelayDict)
