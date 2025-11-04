# SVT Test
# SVT version 24.3.b14
# Test saved 2024-07-25_1411
# Form factor: SV7C_16C17G
# PY3
# Checksum: 743b8b7066b8a59094b5c3894cfd70ef
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName='None')

bertScan1 = _create('bertScan1', 'SvtBertScan')
digitalCapture1 = _create('digitalCapture1', 'SvtDigitalCapture')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
patternSync1 = _create('patternSync1', 'SvtPatternSync')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
rxChannelList1 = _create('rxChannelList1', 'SvtRxChannelList')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
userPattern1 = _create('userPattern1', 'SvtUserPattern')

calOptions.addField('dataRates', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[6500.0, 6700.0, 6900.0, 7100.0, 7300.0, 7500.0, 7700.0, 7900.0, 8100.0, 8300.0, 8500.0, 8700.0, 8900.0, 9100.0, 9300.0, 9500.0, 9700.0, 9900.0, 10100.0, 10300.0, 10500.0, 10700.0, 10900.0, 11100.0, 11300.0, 11500.0, 11700.0, 11900.0, 12100.0, 12300.0, 12500.0], displayOrder=(0, 1.0))
calOptions.addField('moduleName', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 2.0))
calOptions.addField('channels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 3.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.dataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0]
calOptions.moduleName = '1234'
calOptions.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
calOptions.callCustomInitMethod()
dataFile1.delimiter = ','
dataFile1.fileName = ''
dataFile1.numFields = 1
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'


bertScan1.bertDurationInBits = 1000000
bertScan1.endPhase = 120.0
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = False
bertScan1.patternSync = patternSync1
bertScan1.phaseOffsets = [0.0]
bertScan1.rxChannelList = rxChannelList1
bertScan1.saveResults = True
bertScan1.startPhase = -120.0
bertScan1.timeUnits = 'picosecond'
bertScan1.wantAnalysis = True
bertScan1.wantResultImages = False

digitalCapture1.errorToleranceForAnalysis = 0.0
digitalCapture1.numBytesDesired = 2048
digitalCapture1.rxChannelList = rxChannelList1
digitalCapture1.saveResults = False
digitalCapture1.startCondition = 'wordDetect'
digitalCapture1.startWord = '00001111'
digitalCapture1.timeout = 10
digitalCapture1.timeoutForAnalysis = 30
digitalCapture1.wantAnalysis = True

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 12500.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

patternSync1.autoDiagnoseSyncFailure = True
patternSync1.durationInBits = 1000000
patternSync1.errorIfSyncFails = True
patternSync1.errorTolerance = 0.0003
patternSync1.rxChannelList = rxChannelList1
patternSync1.standAlone = True
patternSync1.syncMethod = 'syncWithCentering'
patternSync1.syncMode = 'standard'
patternSync1.targetPhases = [0.0]
patternSync1.targetVoltages = [0.0]
patternSync1.voltageScanHeight = 500.0
patternSync1.wantRestoreVoltagesAfterSync = True

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

rxChannelList1.channelLabeling = None
rxChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
rxChannelList1.comparatorThresholds = [0.0]
rxChannelList1.equalizationAcGains = [0]
rxChannelList1.equalizationEqGains = [0]
rxChannelList1.expectedPatterns = [userPattern1]
rxChannelList1.polarities = ['normal']

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [400.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [userPattern1]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']

userPattern1.bits = '01010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010100001111'
userPattern1.notes = ''


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')
#! TEST PROCEDURE
from dftm.commandProcessor.spiOps import SpiOps
import datetime

iesp = getIespInstance()
iesp.enableVeryPatientMode()

SpiOps.setDelays(0,1,0)

phaseOffsetsByDataRate = dict()
minOffsetDiff = 0

polyCoefficients = dict()
for channel in range(1,17,1) :
    polyCoefficients[channel] = dict()
    for c in range(4):
        polyCoefficients[channel][c] = 0.0

channels = sorted(calOptions.channels)
rxChannelList1.channels = channels
txChannelList1.channels = channels

for dataRate in sorted(calOptions.dataRates) :
    globalClockConfig.dataRate = dataRate
    globalClockConfig.setup()
    dataRate = iesp.getDataRate()
    print(dataRate)
    uiWidthInPs = (1/dataRate)*1000000
    txChannelList1.setup()
    rxChannelList1.setup()

    phaseOffsetsByDataRate[dataRate] = dict()
    coarseSkewsByChannel = dict()
    bathtubCentersByChannel = dict()
    channelMask = 0

    for channel in channels :
        channelMask = channelMask | 0x00001<<(channel-1)

    bertScan1.wantDoubleMode = False
    bertScan1.startPhase = -uiWidthInPs
    bertScan1.endPhase = uiWidthInPs
    patternSync1.syncMethod = 'syncWithCentering'

    result = patternSync1.run()
    rxPhasesDict = result.getSyncedPhasesByChannel()
    rxPhases = []
    for channel in channels:
        rxPhases.append(rxPhasesDict[channel])

    digitalCaptureResult = digitalCapture1.run()

    bertScan1.phaseOffsets = rxPhases
    patternSync1.syncMethod = 'syncWithMeasurementPath'
    patternSync1.targetPhases = rxPhases
    bertScanResult = bertScan1.run()

    for channel in channels :
        # Get bathtub phase center
        edges = bertScanResult.getEdges(channel)
        eyeCenter = (edges[1]['location']+edges[0]['location'])/2
        bathtubCentersByChannel[channel] = eyeCenter

        # Calculate coarse skew from digital capture using first channel as reference
        bits = digitalCaptureResult.getBits(channel)
        index = bits.index(digitalCapture1.startWord)

        if channel == channels[0]:
            coarseSkewRefChannel = index
        else:
            if index > userPattern1.numBits/2:
                index = index-userPattern1.numBits
        coarseSkewsByChannel[channel] = index

        # Calculate total skew from coarse and fine
        totalSkew = bathtubCentersByChannel[channel]+uiWidthInPs*(coarseSkewsByChannel[channel]-coarseSkewRefChannel)
        phaseOffsetsByDataRate[dataRate][channel] = totalSkew

    # Override rx alignment data in the firmware with the calculated skew
    for channel in channels :
        success = iesp.writeSubPartRegister(0x0232, None, int(0x00001<<(channel-1)))
        if (success == True) :
            success = iesp.writeSubPartRegister(0x0441, None, int(phaseOffsetsByDataRate[dataRate][channel]*1000))
            iesp.waitForCommandProcessors()
    iesp.writeSubPartRegister(0x0232, None, channelMask)

    # Check if the skew correction worked
    patternSync1.syncMethod = 'syncWithCentering'
    result = patternSync1.run()
    rxPhasesDict = result.getSyncedPhasesByChannel()

    digitalCaptureResult = digitalCapture1.run()

    for channel in channels :
        # Calculate coarse skew from digital capture
        bits = digitalCaptureResult.getBits(channel)
        index = bits.index(digitalCapture1.startWord)

        if channel != channels[0]:
            if index > userPattern1.numBits/2:
                index = index-userPattern1.numBits
        coarseSkewsByChannel[channel] = index

        # Calculate total skew from coarse and fine
        totalSkew = rxPhasesDict[channel]+uiWidthInPs*coarseSkewsByChannel[channel]

        if channel == channels[0]:
            skewRefChannel = totalSkew
        elif abs(totalSkew-skewRefChannel) > uiWidthInPs:
            errorMsg(f"Calibration failed on channel {channel} at data rate {dataRate}")



for channel in channels :
    xVals = list()
    yVals = list()
    for dataRate in sorted(calOptions.dataRates) :
        xVals.append(dataRate)
        yVals.append(phaseOffsetsByDataRate[dataRate][channel])
    polyCoefficients[channel] = np.polyfit(xVals,yVals,3)
    print(polyCoefficients[channel])
dataFile1.fileName = "rxAlignCal_"+calOptions.moduleName+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.moduleName+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : rx_alignment_calibration_data\n")

    for c in range(4):
        for channel in range(1,17,1):
            calFile.write("%0.15f," % polyCoefficients[channel][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("rxAlignCal_"+calOptions.moduleName)
dataFile1.deleteFile()
