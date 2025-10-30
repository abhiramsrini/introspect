# SVT Test
# SVT version 24.4.b0
# Test saved 2024-06-27_1132
# Form factor: SV7C_16C17G
# PY3
# Checksum: 2a57417a34227c1c27d8e88d21c5f3ba
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


digitalCapture1 = _create('digitalCapture1', 'SvtDigitalCapture')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
patternSync1 = _create('patternSync1', 'SvtPatternSync')
rawDataCapture1 = _create('rawDataCapture1', 'SvtDigitalCapture')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
rxChannelList1 = _create('rxChannelList1', 'SvtRxChannelList')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
userPattern1 = _create('userPattern1', 'SvtUserPattern')

digitalCapture1.errorToleranceForAnalysis = 0.0
digitalCapture1.numBytesDesired = 2048
digitalCapture1.rxChannelList = rxChannelList1
digitalCapture1.saveResults = True
digitalCapture1.startCondition = 'wordDetect'
digitalCapture1.startWord = '00001111'
digitalCapture1.timeout = 10
digitalCapture1.timeoutForAnalysis = 30
digitalCapture1.wantAnalysis = True

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 17400.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

patternSync1.autoDiagnoseSyncFailure = True
patternSync1.durationInBits = 100000
patternSync1.errorIfSyncFails = True
patternSync1.errorTolerance = 0.0003
patternSync1.rxChannelList = rxChannelList1
patternSync1.standAlone = False
patternSync1.syncMethod = 'syncWithCentering'
patternSync1.syncMode = 'standard'
patternSync1.targetPhases = [0.0]
patternSync1.targetVoltages = [0.0]
patternSync1.voltageScanHeight = 500.0
patternSync1.wantRestoreVoltagesAfterSync = True

rawDataCapture1.errorToleranceForAnalysis = 0.0
rawDataCapture1.numBytesDesired = 2048
rawDataCapture1.rxChannelList = rxChannelList1
rawDataCapture1.saveResults = True
rawDataCapture1.startCondition = 'signalDetect'
rawDataCapture1.startWord = '11110000'
rawDataCapture1.timeout = 10
rawDataCapture1.timeoutForAnalysis = 30
rawDataCapture1.wantAnalysis = True

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

rxChannelList1.channelLabeling = None
rxChannelList1.channels = [9, 10, 11, 12, 13, 14, 15, 16]
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
#from dftm.comm.commUtils import *
iesp = getIespInstance()
#SpiOps.beVeryPatient = True
iesp.enableVeryPatientMode()
fail = 0

channels = rxChannelList1.channels

globalClockConfig.setup()
uiWidthInPs = (1/iesp.getDataRate())*1000000
phaseStepInPs = uiWidthInPs/64

txChannelList1.setup()
rxChannelList1.setup()

result = patternSync1.run()
rxPhasesDict = result.getSyncedPhasesByChannel()

digitalCaptureResult = digitalCapture1.run()

coarseSkewsByChannel = dict()
for channel in rxChannelList1.channels :
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
        print(f"Calibration failed on channel {channel}")
        fail = 1

if fail == 1 :
    writeNoteForTestRun("Fail")
else :
    writeNoteForTestRun("Pass")
