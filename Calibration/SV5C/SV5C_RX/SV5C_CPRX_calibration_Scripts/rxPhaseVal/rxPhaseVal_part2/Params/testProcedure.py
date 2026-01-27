# SVT Test
# SVT version 25.3.rc0
# Test saved 2025-08-01_1559
# Form factor: SV5C_CPTX_CPRX
# PY3
# Checksum: df8f7876771325b121f095c862be4758
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName=None)
runCombinedEyeScan = _create('runCombinedEyeScan', 'SvtFunction', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
valParams = _create('valParams', 'SvtDataRecord', iespName=None)

bertScan1 = _create('bertScan1', 'SvtMipiCphyBertScan', iespName='iespRx')
eyeScan1 = _create('eyeScan1', 'SvtMipiCphyEyeScan', iespName='iespRx')
iespRx_mipiClockConfig1 = _create('iespRx_mipiClockConfig1', 'SvtMipiClockConfig', iespName='iespRx')
iespRx_mipiProtocol = _create('iespRx_mipiProtocol', 'SvtMipiProtocol', iespName='iespRx')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList', iespName='iespRx')
mipiCphyExpectedPattern1 = _create('mipiCphyExpectedPattern1', 'SvtMipiCphyExpectedPattern', iespName='iespRx')
refClocksConfig2 = _create('refClocksConfig2', 'SvtRefClocksConfig', iespName='iespRx')

csiImagePattern1 = _create('csiImagePattern1', 'SvtMipiCphyCsiImagePattern', iespName='iespTx')
customPattern1 = _create('customPattern1', 'SvtMipiCphyCustomPattern', iespName='iespTx')
iespTx_mipiClockConfig1 = _create('iespTx_mipiClockConfig1', 'SvtMipiClockConfig', iespName='iespTx')
iespTx_mipiProtocol = _create('iespTx_mipiProtocol', 'SvtMipiProtocol', iespName='iespTx')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiCphyGenerator', iespName='iespTx')
params1 = _create('params1', 'SvtMipiCphyParams', iespName='iespTx')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig', iespName='iespTx')

SetupFunction.args = 'rate'
SetupFunction.code = r'''iespTx_mipiClockConfig1.dataRate = rate
mipiGenerator1.setup()

iespRx_mipiClockConfig1.dataRate = rate
refClocksConfig2.externRefClockFreq = 100.0
iespRx_mipiClockConfig1.setup()


#freeze cdr
iespRx.writeSubPartRegister(0x66B0,0x00,0x01)

#set bert pattern trigger period. PRBS9 (511*16)bits
iespRx.writeSubPartRegister(0x66A0, 0x00, 8177)

#override termination
iespRx.writeSubPartRegister(0x0D40, 0x00, 0x01)

#force term on A
iespRx.writeSubPartRegister(0xD13, 0x0F, 0x01)

#force term on B
iespRx.writeSubPartRegister(0xD14, 0x0F, 0x01)

#force term on C
iespRx.writeSubPartRegister(0xD15, 0x0F, 0x01)

#set pre cdr bert enable
#iesp.writeSubPartRegister(0x66A2, 0x00, 0x01)

# !! Special command when doing combined eye scans
#force filtering disabled
iespRx.writeSubPartRegister(0xD22, 0x0F, 0x01)
#set pre cdr bert enable
iespRx.writeSubPartRegister(0x66A2, 0x00, 0x00)

# set expected pattern

laneList1.expectedPattern = mipiCphyExpectedPattern1
'''
SetupFunction.wantAllVarsGlobal = False

runCombinedEyeScan.args = ''
runCombinedEyeScan.code = r'''# --------------------------------------------------------------------
printMsg('Doing eye scans at %.1fMsps: AB/BC/CA combined...' % valParams.dataRate, 'magenta', None, True)
numberOfMaxTrials = 5

#perform clock commit and set termination
SetupFunction(valParams.dataRate)

sleepMillis(3000)

#loop through the wires: AB1_0, AB1_1...
for lane in valParams.lanes:
    #set active lane
    laneMask = 0x01 << (lane-1)
    laneList1.lanes = [lane]
    laneList1.setup()

    eyeScan1.wires = valParams.wires
    eyeScan1.resultName = 'lane_%s'%lane
    for trial in range(numberOfMaxTrials):
        print('==Trial #%d for lane%d' % (trial, lane))
        results = eyeScan1.run()
        print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
        print(results.getAnalysis(lane, 'wireState'))
        eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
        print(eyeCenterY)
        if eyeCenterY == None:
            warningMsg("Found a failing condition on Lane %d... eyeCenterY=None! Repeat..." % lane)
            # set the clock again
            SetupFunction(valParams.dataRate)
        else:
            break

#unfreeze cdr
iespRx.writeSubPartRegister(0x66B0,0x00,0x00)
# --------------------------------------------------------------------
'''
runCombinedEyeScan.wantAllVarsGlobal = False

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

valParams.addField('wires', descrip='''Wires for each lane to validate''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['wireAB', 'wireBC', 'wireCA'], displayOrder=(0, 1.0))
valParams.addField('dataRate', descrip='''dataRate for validation''', attrType=float, iespInstanceName='any', defaultVal=4500.0, displayOrder=(0, 2.0))
valParams.addField('lanes', descrip='''lanes to validate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
valParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
valParams.wires = ['wireAB', 'wireBC', 'wireCA']
valParams.dataRate = 4500.0
valParams.lanes = [1, 2, 3, 4]
valParams.callCustomInitMethod()

bertScan1.bertDurationInBits = 1000000
bertScan1.endPhase = 1.5
bertScan1.laneList = laneList1
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = False
bertScan1.patternSync = iespRx_PATSYNC_strobeSync
bertScan1.phaseOffsets = [0.0]
bertScan1.saveResults = True
bertScan1.startPhase = -1.5
bertScan1.timeUnits = 'unitWidth'
bertScan1.wantResultImages = False
bertScan1.wires = ['wireAB', 'wireBC', 'wireCA']

eyeScan1.berThreshold = 1e-12
eyeScan1.bertDurationInBits = 1000000
eyeScan1.endPhase = 1.0
eyeScan1.endVoltage = 630.0
eyeScan1.eyeMask = None
eyeScan1.laneList = laneList1
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.patternSync = iespRx_PATSYNC_strobeSync
eyeScan1.saveResults = True
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -1.0
eyeScan1.startVoltage = -630.0
eyeScan1.timeUnits = 'unitWidth'
eyeScan1.voltageStep = 20.0
eyeScan1.wantResultImages = False
eyeScan1.wires = ['wireAB', 'wireBC', 'wireCA']

iespRx_mipiClockConfig1.autoDetectDataRate = False
iespRx_mipiClockConfig1.autoDetectTimeout = 2.0
iespRx_mipiClockConfig1.dataRate = 5000.0
iespRx_mipiClockConfig1.referenceClocks = refClocksConfig2

iespRx_mipiProtocol.csiScramble = False
iespRx_mipiProtocol.csiVersion = 'Csi2_v2_0_and_later'
iespRx_mipiProtocol.protocol = 'CSI'

laneList1.expectedPattern = mipiCphyExpectedPattern1
laneList1.hsThresholdVoltage = 0.0
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 450.0

mipiCphyExpectedPattern1.hsData = [42, 0]
mipiCphyExpectedPattern1.hsMode = 'prbs'
mipiCphyExpectedPattern1.prbsOrder = 'PRBS_9'
mipiCphyExpectedPattern1.prbsSeed = '0x9980789A'

refClocksConfig2.externRefClockFreq = 100.0
refClocksConfig2.outputClockAFormat = 'LVDS'
refClocksConfig2.outputClockAFreq = 100.0
refClocksConfig2.systemRefClockSource = 'external'


csiImagePattern1.blankingDuration = 3000.0
csiImagePattern1.calibrationPreamble = 'disabled'
csiImagePattern1.cseParams = None
csiImagePattern1.csiCompressionParams = None
csiImagePattern1.enableCsiEpd = False
csiImagePattern1.errorInsertion = None
csiImagePattern1.frameBlankingDuration = 30000.0
csiImagePattern1.frameBlankingMode = 'frameRate'
csiImagePattern1.frameRate = 30.0
csiImagePattern1.gaussianBlurRadius = 0
csiImagePattern1.horizLineTime = 30000.0
csiImagePattern1.imageFiles = ['IntrospectLogo.png']
csiImagePattern1.imageFormat = 'CSI_RGB888'
csiImagePattern1.lineNumbering = 'disabled'
csiImagePattern1.lineTimeMode = 'lineTimeTotal'
csiImagePattern1.mediaSource = 'image'
csiImagePattern1.numLongPacketEpdSpacers = 0
csiImagePattern1.numShortPacketEpdSpacers = 0
csiImagePattern1.numVideoFrames = None
csiImagePattern1.rawFormatBayerCell = 'BGGR'
csiImagePattern1.regionsOfInterest = []
csiImagePattern1.sendRoiInfo = False
csiImagePattern1.timeUnits = 'nanosecond'
csiImagePattern1.useRoi = False
csiImagePattern1.useVideoFps = False
csiImagePattern1.videoFile = ''
csiImagePattern1.virtualChannel = 0
csiImagePattern1.wantFrameNumbering = False

customPattern1.hsData = [42, 0]
customPattern1.hsDataMode = 'prbs'
customPattern1.hsPrbsOrder = 9
customPattern1.hsPrbsSeed = None
customPattern1.hsSymbols = '22200000000000'
customPattern1.lpBits = ''
customPattern1.packetSize = 1000
customPattern1.patternType = 'hsOnly'
customPattern1.sameDataInEachPacket = True
customPattern1.stopDuration = 0

iespTx_mipiClockConfig1.autoDetectTimeout = 2.0
iespTx_mipiClockConfig1.dataRate = 5000.0
iespTx_mipiClockConfig1.referenceClocks = refClocksConfig1

iespTx_mipiProtocol.csiScramble = False
iespTx_mipiProtocol.csiScrambleNumSeeds = 'one'
iespTx_mipiProtocol.csiVersion = 'Csi2_v2_0_and_later'
iespTx_mipiProtocol.protocol = 'CSI'

mipiGenerator1.clockConfig = iespTx_mipiClockConfig1
mipiGenerator1.commonNoise = None
mipiGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.hsPostTaps = [0]
mipiGenerator1.hsPreTaps = [0]
mipiGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lanes = [1, 2, 3, 4]
mipiGenerator1.lpHighVoltages = [1200.0]
mipiGenerator1.lpLowVoltages = [0.0]
mipiGenerator1.params = params1
mipiGenerator1.pattern = customPattern1
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = False
mipiGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

params1.calAlternateSeqNumPrbs = 8
params1.calPreambleNumUI = 21
params1.calUserSequence = [0x5555, 0xAAAA]
params1.calibrationPreambleFormat = 'format_1'
params1.enableProgSeq = True
params1.lp000Duration = 65.0
params1.lp001Duration = 100.0
params1.opticalLink = 'disabled'
params1.post2NumUI = 112
params1.postNumUI = 112
params1.postSymbols = '4444444'
params1.preBeginNumUI = 196
params1.preBeginSymbols = '3333333'
params1.preEndSymbols = '3333333'
params1.progSeqSymbols = '33333333333333'
params1.syncWord = '3444443'
params1.t3AlpPauseMin = 50
params1.t3AlpPauseWake = 50
params1.tHsExitDuration = 300.0
params1.tTaGetDuration = 5
params1.tTaGoDuration = 4.0
params1.tTaSureDuration = 1.0
params1.tWaitOptical = 150000.0
params1.tlpxDuration = 100.0
params1.useAlp = False

refClocksConfig1.externRefClockFreq = 250.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.systemRefClockSource = 'internal'

#! TEST PROCEDURE
iespRx, iespTx = getAllIespInstances()

from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder

svtVersion = requireSvtVersionInRange("24.3", None)

# check the serial number
serialNumberFailFlag = 1
for trial in range(5):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    serialNumber = getTextDialog("Please enter the serial number of the RX unit (89-xxxx):")
    if serialNumber[:3] == '89-':
        serialNumberFailFlag = 0
        break

if serialNumberFailFlag == 0:

    # print HW, SW and FW info
    printMsg("Tx Serial Number: %s" % iespTx.getModuleSerialNums(), 'magenta', None, True)
    printMsg('Tx Firmware Id: %s' % iespTx.getFirmwareIdsFromConnection()[0], 'magenta', None, True)
    printMsg("Tx Firmware revision: %s" % iespTx.getFirmwareRevisions(), 'magenta', None, True)
    printMsg("Tx Hardware revision: %s" % iespTx.getHardwareRevisions(), 'magenta', None, True)

    printMsg("Serial Number: %s" % iespRx.getModuleSerialNums(), 'magenta', None, True)
    printMsg('Firmware Id: %s' % iespRx.getFirmwareIdsFromConnection()[0], 'magenta', None, True)
    printMsg("Firmware revision: %s" % iespRx.getFirmwareRevisions(), 'magenta', None, True)
    printMsg("Hardware revision: %s" % iespRx.getHardwareRevisions(), 'magenta', None, True)

    # rename the result folder
    renameFolderFailFlag = 0
    try:
        context = getCurrentTest()
        RunNotesFolderPath = context.getCurrRunResultFolderPath()
        # create a new folder named as the serial number of the RX unit
        resultFolderPath = context.createRunResultFolder(serialNumber)
    except:
        renameFolderFailFlag = 1
        printMsg("Fail: There is already a folder called (%s) in Results" % serialNumber, 'red', None, True)
        writeNoteForTestRun("Fail: There is already a folder called (%s) in Results" % serialNumber)

    if renameFolderFailFlag == 0:
        runCombinedEyeScan()

        sleepMillis(20000)

    # copy runNotes folder to the result folder
    runNotes1.makeCopyOfTestLogFile()
    copyContentsOfFolder(RunNotesFolderPath, resultFolderPath)

# serial number not as expected
else:
    printMsg("Fail: The serial number provided of the RX unit (%s) is not as expected!" % serialNumber, 'red', None, True)
    writeNoteForTestRun("Fail: The serial number provided of the RX unit (%s) is not as expected!" % serialNumber)
