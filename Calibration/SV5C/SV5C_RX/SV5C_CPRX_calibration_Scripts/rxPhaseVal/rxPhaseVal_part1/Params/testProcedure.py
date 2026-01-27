# SVT Test
# SVT version 25.3.rc0
# Test saved 2025-07-28_1149
# Form factor: SV5C_CPTX_CPRX
# PY3
# Checksum: 422802103520067472cd117b0a6f5adc
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


initializeBert = _create('initializeBert', 'SvtFunction', iespName=None)
runBertscan = _create('runBertscan', 'SvtFunction', iespName=None)
runFirstBertscan = _create('runFirstBertscan', 'SvtFunction', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
setDataRate = _create('setDataRate', 'SvtFunction', iespName=None)
valOptions = _create('valOptions', 'SvtDataRecord', iespName=None)
writeValReport = _create('writeValReport', 'SvtFunction', iespName=None)

bertScan1 = _create('bertScan1', 'SvtMipiCphyBertScan', iespName='iespRx')
iespRx_mipiClockConfig1 = _create('iespRx_mipiClockConfig1', 'SvtMipiClockConfig', iespName='iespRx')
iespRx_mipiProtocol = _create('iespRx_mipiProtocol', 'SvtMipiProtocol', iespName='iespRx')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList', iespName='iespRx')
mipiCphyExpectedPattern1 = _create('mipiCphyExpectedPattern1', 'SvtMipiCphyExpectedPattern', iespName='iespRx')
patternSync1 = _create('patternSync1', 'SvtMipiCphyPatternSync', iespName='iespRx')
refClocksConfig2 = _create('refClocksConfig2', 'SvtRefClocksConfig', iespName='iespRx')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator', iespName='iespRx')

csiImagePattern1 = _create('csiImagePattern1', 'SvtMipiCphyCsiImagePattern', iespName='iespTx')
iespTx_mipiClockConfig1 = _create('iespTx_mipiClockConfig1', 'SvtMipiClockConfig', iespName='iespTx')
iespTx_mipiProtocol = _create('iespTx_mipiProtocol', 'SvtMipiProtocol', iespName='iespTx')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiCphyGenerator', iespName='iespTx')
params1 = _create('params1', 'SvtMipiCphyParams', iespName='iespTx')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig', iespName='iespTx')

initializeBert.args = ''
initializeBert.code = r'''#freeze cdr
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
iespRx.writeSubPartRegister(0x66A2, 0x00, 0x01)

iespRx.waitForCommandProcessors()
'''
initializeBert.wantAllVarsGlobal = False

runBertscan.args = 'lane,wire,wireSubChannel,bertDurationInBits'
runBertscan.code = r'''laneList1.lanes = [lane]
laneList1.setup()
bertScan1.wires = [wire]

#set pre bert
if wire == 'wireAB':
    wireIndex = 0
elif wire == 'wireBC':
    wireIndex = 1
elif wire == 'wireCA':
    wireIndex = 2
if wireSubChannel == '0' :
    subChannelIndex = 0
elif wireSubChannel == '1' :
    subChannelIndex = 1
preBert = (lane-1)*6 + wireIndex*2 + subChannelIndex

iespRx.writeSubPartRegister(0x66A4, 0x00, preBert)
print("PreBert Number is ", preBert)

laneMask = 0x01 << (lane-1)

print("Trying to sync at even phase...")
# First search for the threshold yielding the widest eye

bestThreshold = 0
bertScan1.bertDurationInBits = 1e4
bertScan1.saveResults = False

currThreshold = valOptions.defaultSyncThreshold
#Eye width must measure at least 85% of UI
minEyeWidth_ps = (1000000 / valOptions.dataRate) * 0.85
print(minEyeWidth_ps)
eyeWidth = 0

while((eyeWidth < minEyeWidth_ps) and (currThreshold < valOptions.maxSyncThreshold)):
    print("Setting threshold to %d mV..." % currThreshold)
    laneList1.hsThresholdVoltage = currThreshold
    laneList1.update()

    bertScan1.setup()
    tempResult = bertScan1.run()
    eyeWidth = tempResult._getAnalysis(lane, 'wireState')['jitter']['widthZeroErrs']
    print("Current eye width is %f ps..." % eyeWidth)
    if eyeWidth > minEyeWidth_ps :
        bestThreshold = currThreshold
    else :
        currThreshold = currThreshold + 10

#check that appropriate threshold was found
if(bestThreshold == 0):
    print("Failed to find appropriate sync threhsold. Stopping.")
    exit()

print("Eye width was %f ps at %d mV..." % (eyeWidth,bestThreshold))

# set the threshold to the best value
print("Setting best threshold to %d mV..." % bestThreshold)
iespRx.setMipiHsThresholdVoltage(bestThreshold, wire, [lane])
# now run the real scan without doing a bert sync
print("Running bertscan...")
bertScan1.saveResults = True
bertScan1.bertDurationInBits = bertDurationInBits
resultNameString = 'bertScan_%d_'%lane + wire[4:6] + '_' + wireSubChannel + '_' + 'even'
print(resultNameString)
bertScan1.resultName = resultNameString
bertScan1.setup()
resultEven = bertScan1.run()
print('--> bertScan Result: ', resultEven.getResultFolderPath().split('\\')[-1])
edges = resultEven._getAnalysis(lane, 'wireState')['edges']
fallingEdgeEven = edges[0]['location']
print("Falling Edge Location for Even Phase: %f" % fallingEdgeEven)
risingEdgeEven = edges[1]['location']
print("Rising Edge Location for Even Phase: %f" % risingEdgeEven)
syncOffsetEven = dftUtil.byteListToUIntValue(iespRx.readSubPartRegister(0x6643, laneMask))
print("SyncOffset for Even Phase: %d" % syncOffsetEven)

# Toggle clock phase (must be within a single clock commit)
print("Toggling clock phase...")
iespRx.writeSubPartRegister(0xFEEC, 0x00, 0x00) # Toggles even/odd state
iespRx.waitForCommandProcessors()

# must do a bert sync again after toggling even state
print("Trying to sync at odd phase...")

# First search for the threshold yielding the widest eye
bestThreshold = 0
bertScan1.bertDurationInBits = 1e4
bertScan1.saveResults = False

#first scan performed at 45mV
currThreshold = valOptions.defaultSyncThreshold
maxThreshold = 250
#Eye width must measure at least 85% of UI
minEyeWidth_ps = (1000000 / valOptions.dataRate) * 0.85
eyeWidth = 0

while((eyeWidth < minEyeWidth_ps) and (currThreshold < valOptions.maxSyncThreshold)):
    print("Setting threshold to %d mV..." % currThreshold)
    laneList1.hsThresholdVoltage = currThreshold
    laneList1.update()

    bertScan1.setup()
    tempResult = bertScan1.run()
    eyeWidth = tempResult._getAnalysis(lane, 'wireState')['jitter']['widthZeroErrs']
    print("Current eye width is %f ps..." % eyeWidth)
    if eyeWidth > minEyeWidth_ps :
        bestThreshold = currThreshold
    else :
        currThreshold = currThreshold + 10

#check that appropriate threshold was found
if(bestThreshold == 0):
    print("Failed to find appropriate sync threhsold. Stopping.")
    exit()

print("Eye width was %f ps at %d mV..." % (eyeWidth,bestThreshold))

# set the threshold to the best value
print("Setting best threshold to %d mV..." % bestThreshold)
iespRx.setMipiHsThresholdVoltage(bestThreshold, wire, [lane])
print("Running bertscan...")
bertScan1.saveResults = True
bertScan1.bertDurationInBits = bertDurationInBits
resultNameString = 'bertScan_%d_'%lane + wire[4:6] + '_' + wireSubChannel + '_' + 'odd'
print(resultNameString)
bertScan1.resultName = resultNameString
bertScan1.setup()
resultOdd = bertScan1.run()

print('--> bertScan Result: ', resultOdd.getResultFolderPath().split('\\')[-1])
edges = resultOdd._getAnalysis(lane, 'wireState')['edges']
fallingEdgeOdd = edges[0]['location']
print("Falling Edge Location for Odd Phase: %f" % fallingEdgeOdd)
risingEdgeOdd = edges[1]['location']
print("Rising Edge Location for Odd Phase: %f" % risingEdgeOdd)
syncOffsetOdd = dftUtil.byteListToUIntValue(iespRx.readSubPartRegister(0x6643, laneMask))
print("SyncOffset for Odd Phase: %d" % syncOffsetOdd)

# Toggle clock phase back so that we're always starting at the same phase (must be within a single clock commit)
iespRx.writeSubPartRegister(0xFEEC, 0x00, 0x00) # Toggles even/odd state
iespRx.waitForCommandProcessors()


return (resultEven, resultOdd,syncOffsetEven,syncOffsetOdd)
'''
runBertscan.wantAllVarsGlobal = False

runFirstBertscan.args = ''
runFirstBertscan.code = r'''laneList1.lanes = valOptions.lanes[0]
laneList1.setup()
lane = valOptions.lanes[0]
bertScan1.wires = valOptions.wires[0]
wire = valOptions.wires[0]
wireSubChannel = valOptions.wireSubChannels[0]
phase = 'even'


#set pre bert
if wire == 'wireAB':
    wireIndex = 0
elif wire == 'wireBC':
    wireIndex = 1
elif wire == 'wireCA':
    wireIndex = 2
if wireSubChannel == '0' :
    subChannelIndex = 0
elif wireSubChannel == '1' :
    subChannelIndex = 1
preBert = (lane-1)*6 + wireIndex*2 + subChannelIndex

iespRx.writeSubPartRegister(0x66A4, 0x00, preBert)
print("PreBert Number is ", preBert)
bertScan1.saveResults = False
bertScan1.bertDurationInBits = 1e7
resultNameString = 'bertScan_%d_'%lane + wire[4:6] + '_' + wireSubChannel + '_' + phase
print(resultNameString)
bertScan1.resultName = resultNameString
laneMask = 0x01 << (lane-1)

print("Running dummy bertscan to select the initial wire state for expected patterns...")
#clear force wire init state
iespRx.writeSubPartRegister(0x66A8, laneMask, 0x00)
# run first scan
bertScan1.run()

print("Forcing the initial wire state for all subsequent runs...")
# set force wire init state
iespRx.writeSubPartRegister(0x66A8, laneMask, 0x01)
'''
runFirstBertscan.wantAllVarsGlobal = False

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

setDataRate.args = 'dataRate'
setDataRate.code = r'''#enable alignment cal mode in the analyzer: remove the .5 sub ui offset
iespRx.writeSubPartRegister(0x0930, 0x00, 0x01)

iespTx_mipiClockConfig1.dataRate = dataRate
iespTx_mipiClockConfig1.setup()

# Start generator with a 200 mV amplitude hs222 pattern
mipiGenerator1.hsVoltageAmplitudesABC = [(100,100,100)]
mipiGenerator1.hsCommonVoltagesABC = [(200,200,200)]

mipiGenerator1.pattern = valOptions.Pattern
mipiGenerator1.setup()

mipiCphyExpectedPattern1.hsMode = 'data'
mipiCphyExpectedPattern1.hsData = [21844]

laneList1.expectedPattern = mipiCphyExpectedPattern1

iespRx_mipiClockConfig1.dataRate = dataRate
iespRx_mipiClockConfig1.setup()
'''
setDataRate.wantAllVarsGlobal = False

valOptions.addField('dataRate', descrip='''calibration dataRate''', attrType=float, iespInstanceName='any', defaultVal=4500.0, displayOrder=(0, 1.0))
valOptions.addField('depth', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=100000000.0, displayOrder=(0, 2.0))
valOptions.addField('lanes', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
valOptions.addField('wires', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['wireAB', 'wireBC', 'wireCA'], displayOrder=(0, 4.0))
valOptions.addField('wireSubChannels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['0', '1'], displayOrder=(0, 5.0))
valOptions.addField('defaultSyncThreshold', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=45.0, displayOrder=(0, 6.0))
valOptions.addField('maxSyncThreshold', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=300.0, displayOrder=(0, 7.0))
valOptions.addField('serialNumber', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='89-xxxx', displayOrder=(0, 8.0))
valOptions.addField('Pattern', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='CPHY_hsOnly222', displayOrder=(0, 9.0))
valOptions.addField('errAcceptance_ps', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=30.0, displayOrder=(0, 10.0))
valOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
valOptions.dataRate = 4000.0
valOptions.depth = 100000000.0
valOptions.lanes = [1, 2, 3, 4]
valOptions.wires = ['wireAB', 'wireBC', 'wireCA']
valOptions.wireSubChannels = ['0', '1']
valOptions.defaultSyncThreshold = 45.0
valOptions.maxSyncThreshold = 300.0
valOptions.serialNumber = '89-xxxx'
valOptions.Pattern = 'CPHY_hsOnly222'
valOptions.errAcceptance_ps = 30.0
valOptions.callCustomInitMethod()
writeValReport.args = 'listDiff,passFail,failFlag'
writeValReport.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d %02d %02d" % (now.year, now.month, now.day)
resultFolderCreator1.folderName = "valReport_" + valOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "rxPhase_valReport_" + valOptions.serialNumber + ".csv"
filePath = os.path.join(folderPath, FilePathString)
with open(filePath, "w") as outFile:
    outFile.write("SvtVersion, %s\n"%getSvtVersion())
    outFile.write("DUT serialNumber,%s\n"%valOptions.serialNumber)
    outFile.write("DUT firmware,%s_%s\n"%(iespRx.getFirmwareIdsFromConnection()[0],iespRx.getFirmwareRevisions()))
    outFile.write("Tx serialNumber, %s\n" % iespTx.getModuleSerialNums())
    outFile.write("Tx firmware,%s_%s\n"%(iespTx.getFirmwareIdsFromConnection()[0],iespTx.getFirmwareRevisions()))
    outFile.write("Date (YYYY MM DD),"+date + "\n")
    outFile.write("Datarate (Mbps),%s\n"%valOptions.dataRate)
    outFile.write("Pattern,%s \n"%valOptions.Pattern)
    outFile.write("Acceptance Error (ps),%s\n"%valOptions.errAcceptance_ps)
    outFile.write("Criteria,RxPhase offset lower than acceptance error.\n")
    if failFlag:
        outFile.write("Test Status,FAIL\n")
    else:
        outFile.write("Test Status,PASS\n")

    outFile.write(" \n")
    outFile.write("Wire, Measured Delay (ps),Acceptance Limit High (ps), Acceptance Limit Low (ps),Pass_Fail\n")
    wires = ['AB1_0', 'AB1_1', 'BC1_0', 'BC1_1', 'CA1_0', 'CA1_1','AB2_0', 'AB2_1', 'BC2_0', 'BC2_1', 'CA2_0', 'CA2_1','AB3_0', 'AB3_1', 'BC3_0', 'BC3_1', 'CA3_0', 'CA3_1','AB4_0', 'AB4_1', 'BC4_0', 'BC4_1', 'CA4_0', 'CA4_1']
    for i in range(len(listDiff)):
        outFile.write("%s,%s,+%s,-%s,%s\n"%(wires[i],listDiff[i],valOptions.errAcceptance_ps,valOptions.errAcceptance_ps,passFail[i]))
'''
writeValReport.wantAllVarsGlobal = False


bertScan1.bertDurationInBits = 1000000
bertScan1.endPhase = 1.5
bertScan1.laneList = laneList1
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = True
bertScan1.patternSync = patternSync1
bertScan1.phaseOffsets = [0.0]
bertScan1.saveResults = True
bertScan1.startPhase = -1.5
bertScan1.timeUnits = 'unitWidth'
bertScan1.wantResultImages = False
bertScan1.wires = ['wireAB', 'wireBC', 'wireCA']

iespRx_mipiClockConfig1.autoDetectDataRate = False
iespRx_mipiClockConfig1.autoDetectTimeout = 2.0
iespRx_mipiClockConfig1.dataRate = 1500.0
iespRx_mipiClockConfig1.referenceClocks = refClocksConfig2

iespRx_mipiProtocol.csiScramble = False
iespRx_mipiProtocol.csiVersion = 'Csi2_v2_0_and_later'
iespRx_mipiProtocol.protocol = 'CSI'

laneList1.expectedPattern = mipiCphyExpectedPattern1
laneList1.hsThresholdVoltage = 0.0
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 450.0

mipiCphyExpectedPattern1.hsData = [42, 0]
mipiCphyExpectedPattern1.hsMode = 'data'
mipiCphyExpectedPattern1.prbsOrder = 'PRBS_9'
mipiCphyExpectedPattern1.prbsSeed = '0x9980789A'

patternSync1.durationInBits = 100000
patternSync1.errorIfSyncFails = True
patternSync1.errorTolerance = 0.0003
patternSync1.laneList = laneList1
patternSync1.syncMethod = 'strobeSync'
patternSync1.syncMode = 'standard'
patternSync1.targetPhases = [0.0]
patternSync1.targetVoltages = [0.0]
patternSync1.voltageScanHeight = 500.0
patternSync1.wantRestoreVoltagesAfterSync = True

refClocksConfig2.externRefClockFreq = 100.0
refClocksConfig2.outputClockAFormat = 'LVDS'
refClocksConfig2.outputClockAFreq = 100.0
refClocksConfig2.systemRefClockSource = 'external'

resultFolderCreator1.channelProvider = laneList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'


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

iespTx_mipiClockConfig1.autoDetectTimeout = 2.0
iespTx_mipiClockConfig1.dataRate = 1500.0
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
mipiGenerator1.pattern = iespTx_CPHY_hsOnly222
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

iespRx.enableVeryPatientMode()

printMsg("Tx Serial Number: %s" % iespTx.getModuleSerialNums(), 'magenta', None, True)
printMsg('Tx Firmware Id: %s' % iespTx.getFirmwareIdsFromConnection()[0], 'magenta', None, True)
printMsg("Tx Firmware revision: %s" % iespTx.getFirmwareRevisions(), 'magenta', None, True)
printMsg("Tx Hardware revision: %s" % iespTx.getHardwareRevisions(), 'magenta', None, True)


printMsg("Rx Serial Number: %s" % iespRx.getModuleSerialNums(), 'magenta', None, True)
printMsg('Rx Firmware Id: %s' % iespRx.getFirmwareIdsFromConnection()[0], 'magenta', None, True)
printMsg("Rx Firmware revision: %s" % iespRx.getFirmwareRevisions(), 'magenta', None, True)
printMsg("Rx Hardware revision: %s" % iespRx.getHardwareRevisions(), 'magenta', None, True)

# Start generator at the selected data rate
uiInPs = 1/valOptions.dataRate*1000000
setDataRate(valOptions.dataRate)

# Put the DDR Memory of the analyzer in reset
iespRx.writeSubPartRegister(0xFEF0,0x00,0x01)
iespRx.waitForCommandProcessors()

# initialize BERT
initializeBert()

# run first bertscan to select initial wire state
runFirstBertscan()

# wait for DUT temperature to stabilize at the current data rate
lastTemperature = 0
for i in range(120) :
    temperatures = iespRx.getModuleTemperatures()
    currentTemperature = float(temperatures[1:5])
    print("Current temperature is %f degC..." % currentTemperature)
    if ( abs(currentTemperature - lastTemperature) > 0.5 ):
        sleepMillis(5000)
        lastTemperature = currentTemperature
    else:
        break

# construct result container for edge locations
resultDict = dict()
phases = ['even','odd']
for lane in valOptions.lanes :
    resultDict[lane] = dict()
    for wire in valOptions.wires:
            resultDict[lane][wire] = dict()
            for wireSubChannel in valOptions.wireSubChannels:
                resultDict[lane][wire][wireSubChannel] = dict()
                for phase in phases:
                    resultDict[lane][wire][wireSubChannel][phase] = []

# construct result container for sync offsets
syncOffsetDict = dict()
for lane in valOptions.lanes :
    syncOffsetDict[lane] = dict()
    for wire in valOptions.wires:
            syncOffsetDict[lane][wire] = dict()
            for wireSubChannel in valOptions.wireSubChannels:
                syncOffsetDict[lane][wire][wireSubChannel] = dict()
                for phase in phases:
                    syncOffsetDict[lane][wire][wireSubChannel][phase] = []


# Run data collection loop
depth = valOptions.depth
lanes = valOptions.lanes
wires = valOptions.wires
wireSubChannels = valOptions.wireSubChannels

for lane in lanes :
    lastSyncOffset = 0
    for wire in wires :
        for wireSubChannel in wireSubChannels :
            print(lane, wire, wireSubChannel)
            (resultEven, resultOdd, syncOffsetEven,syncOffsetOdd) = runBertscan(lane,wire,wireSubChannel,depth)
            resultDict[lane][wire][wireSubChannel][phases[0]] = resultEven
            syncOffsetDict[lane][wire][wireSubChannel][phases[0]] = syncOffsetEven
            resultDict[lane][wire][wireSubChannel][phases[1]] = resultOdd
            syncOffsetDict[lane][wire][wireSubChannel][phases[1]] = syncOffsetOdd


print("Final sync offsets are...")
for lane in valOptions.lanes:
    for wire in valOptions.wires:
        for wireSubChannel in valOptions.wireSubChannels:
            for phase in phases:
                string1 = 'syncOffset_%d_'%lane + wire[4:6] + '_' + wireSubChannel+ '_' + phase + ": "
                string2 = '%d'%syncOffsetDict[lane][wire][wireSubChannel][phase]
                print(string1,string2)

print("\n")
print("\n")

# Print skews
finalSkewList = list()
print("Final even/odd skews are...")
for lane in valOptions.lanes:
    referenceResultEven = resultDict[lane][valOptions.wires[0]][valOptions.wireSubChannels[0]][phases[0]]
    referenceEdgesEven = referenceResultEven._getAnalysis(lane, 'wireState')['edges']
    referenceFallingEdgeEven = referenceEdgesEven[0]['location']
    referenceRisingEdgeEven = referenceEdgesEven[1]['location']
    referenceResultOdd = resultDict[lane][valOptions.wires[0]][valOptions.wireSubChannels[0]][phases[1]]
    referenceEdgesOdd = referenceResultOdd._getAnalysis(lane, 'wireState')['edges']
    referenceFallingEdgeOdd = referenceEdgesOdd[0]['location']
    referenceRisingEdgeOdd = referenceEdgesOdd[1]['location']
    referenceFallingEdge = (referenceFallingEdgeEven + referenceFallingEdgeOdd) / 2
    referenceRisingEdge = (referenceRisingEdgeEven + referenceRisingEdgeOdd) / 2
    for wire in valOptions.wires:
        for wireSubChannel in valOptions.wireSubChannels:
            resultEven = resultDict[lane][wire][wireSubChannel][phases[0]]
            edgesEven = resultEven._getAnalysis(lane, 'wireState')['edges']
            fallingEdgeEven = edgesEven[0]['location']
            risingEdgeEven = edgesEven[1]['location']
            #string1 = 'skew_%d_'%lane + wire[4:6] + '_' + wireSubChannel+ '_' + phases[0] + ": "
            #string2 = '%f'%fallingEdgeEven
            #print(string1,string2)
            resultOdd = resultDict[lane][wire][wireSubChannel][phases[1]]
            edgesOdd = resultOdd._getAnalysis(lane, 'wireState')['edges']
            fallingEdgeOdd = edgesOdd[0]['location']
            risingEdgeOdd = edgesOdd[1]['location']
            #string1 = 'skew_%d_'%lane + wire[4:6] + '_' + wireSubChannel+ '_' + phases[1] + ": "
            #string2 = '%f'%fallingEdgeOdd
            #print(string1,string2)
            # detect rare case where the even bathtub is one UI away from the odd bathtub
            if abs(fallingEdgeEven-fallingEdgeOdd) > 0.5*uiInPs :
                fallingEdgeOdd = fallingEdgeEven
                print("**** Detected rare case where the even eye sync location was one UI off from the odd eye ****")
            if abs(risingEdgeEven-risingEdgeOdd) > 0.5*uiInPs :
                risingEdgeOdd = risingEdgeEven
                print("**** Detected rare case where the even eye sync location was one UI off from the odd eye ****")
            averageFallingEdge = (fallingEdgeEven + fallingEdgeOdd) / 2
            averageRisingEdge = (risingEdgeEven + risingEdgeOdd) / 2
            falling2FallingSkew = (averageFallingEdge-referenceFallingEdge)
            falling2RisingSkew = (averageFallingEdge-referenceRisingEdge)
            rising2FallingSkew = (averageRisingEdge-referenceFallingEdge)
            if (falling2FallingSkew > 0.5*uiInPs) :
                measuredSkew = falling2RisingSkew
                print("Using the falling edge of %s against the rising edge of the reference wire..."%wire)
            elif (falling2FallingSkew < -0.5*uiInPs) :
                measuredSkew = rising2FallingSkew
                print("Using the rising edge of %s against the rising edge of the reference wire..."%wire)
            else :
                measuredSkew = falling2FallingSkew
            finalSkewList.append(measuredSkew)

print("\n")
print("\n")
print("Data rate is %d Msps..." % valOptions.dataRate)
print("Final skew list for cal file is:")
print(finalSkewList)

failFlag = 0
pass_fail = []
if len(finalSkewList) == 24:
    for finalSkew in finalSkewList:
        if abs(finalSkew)>valOptions.errAcceptance_ps:
            failFlag = 1
            pass_fail.append("FAIL")  
        else:
            pass_fail.append("PASS")
            

    writeValReport(finalSkewList,pass_fail,failFlag)
else:
    printMsg('FAIL: Could not find the offsets for all the lanes.', 'red', None, True)

if failFlag:
    printMsg('FAIL', 'red', None, True)
    writeNoteForTestRun("Fail")
else:
    printMsg('PASS', 'green', None, True)
    writeNoteForTestRun("Pass")
