# SVT Test
# SVT version 24.4.b1
# Test saved 2024-07-04_1645
# Form factor: SV7C_12C40G_PAM3_DDR
# PY3
# Checksum: af9ad49443bd5c34c6624e51dc844cb7
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


beepOkDialog = _create('beepOkDialog', 'SvtFunction', iespName='None')
createRawDataResult = _create('createRawDataResult', 'SvtFunction', iespName='None')
increaseLimits = _create('increaseLimits', 'SvtFunction', iespName='None')
initModule = _create('initModule', 'SvtFunction', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measure = _create('measure', 'SvtFunction', iespName='None')
performMeasurements = _create('performMeasurements', 'SvtFunction', iespName='None')
valOptions = _create('valOptions', 'SvtDataRecord', iespName='None')
validateMeasurement = _create('validateMeasurement', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
pam3Protocol = _create('pam3Protocol', 'SvtPam3Protocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
testAsPythonScript1 = _create('testAsPythonScript1', 'SvtTestAsPythonScript')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
userPattern1 = _create('userPattern1', 'SvtUserPattern')

beepOkDialog.args = 'msg'
beepOkDialog.code = r'''dftUtil.beep(554,250)
dftUtil.beep(554,320)
waitForOkDialog(msg)
'''
beepOkDialog.wantAllVarsGlobal = False

createRawDataResult.args = ''
createRawDataResult.code = r'''import os
rawDataFolderName = f"rawData_{valOptions.serialNumber}"
rawDataFileName = rawDataFolderName + '.json'
resultFolderCreator1.resultType = 'Generic'
resultFolderCreator1.folderName = rawDataFolderName
rawDataFolderPath = resultFolderCreator1.run()
rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
return rawDataFilePath
'''
createRawDataResult.wantAllVarsGlobal = False

increaseLimits.args = ''
increaseLimits.code = r'''iesp.setLimitMaximum("txCommonModeVoltage", 2500)
iesp.setLimitMinimum("txCommonModeVoltage", 0)
iesp.setLimitMaximum("voltageSwing", 1100)
iesp.setLimitMinimum("voltageSwing", 0)

# Common Mode Limits:   [100, 750]
# Amplitude Limits:        [20, 1000]
'''
increaseLimits.wantAllVarsGlobal = False

initModule.args = ''
initModule.code = r'''globalClockConfig.dataRate = valOptions.dataRate
globalClockConfig.setup()

txChannelList1.channels = actualChannels

if valOptions.pattern == 'idle':
    txChannelList1.patterns = ['PAT_DIV40']
else:
    txChannelList1.patterns = [valOptions.pattern]

txChannelList1.setup()

if valOptions.pattern == 'idle':
    txChannelList1.stopPatterns()
'''
initModule.wantAllVarsGlobal = False

initScope.args = ''
initScope.code = r'''import pyvisa

rm = pyvisa.ResourceManager()
try:
    scope = rm.open_resource(valOptions.scopeIpAddress, timeout=20000)
except Exception as e:
    availAddresses = rm.list_resources()
    print(f"Could not connect to scope. Available addresses: {availAddresses}")
    exit()

scope.write_termination = '\n'
scope.read_termination = '\n'

scope.write('*RST')
scope.write(f":TIMebase:SCALe {valOptions.scopeTimeScale}")

for ch in valOptions.scopeChannels:
    scope.write(f":CHANnel{ch}:DISPlay ON")
for ch in valOptions.scopeChannels:
    scope.write(f":AUToscale:VERTical CHANnel{ch}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

for ch in valOptions.scopeChannels:
    scope.write(f":CALibrate:SKEW CHANnel{ch},0")

scope.write("MEASure:STATistics ON")

scope.write(":TRIGger:HYSTeresis HSENsitivity")

return scope
'''
initScope.wantAllVarsGlobal = False

measure.args = 'cm, channelGroup'
measure.code = r'''numChannels = len([x for x in channelGroup if x is not None])
commonModeResults = [0] * numChannels

vScale = 50e-3
if cm > 800:
    vScale *= 2

while not '1' in scope.query('*OPC?'):
    checkIfRunCancelled()
    sleepMillis(1000)

for scopeChIdx, ch in enumerate(valOptions.scopeChannels):
    if channelGroup[scopeChIdx] is None:
        continue
    scope.write(f":CHANnel{ch}:SCAle {vScale}")
    scope.write(f":CHANnel{ch}:OFFSet {cm/1000}")
    scope.write(f":MEASure:VAVerage DISPlay,CHANnel{ch}")

scope.write(f":TRIGger:LEVel:FIFTy")

count = 0
while count < 20:
    checkIfRunCancelled()
    resultStr = scope.query(':MEASure:RESults?')
    resultList = resultStr.split(',')
    count = float(resultList[-1])
    mean = float(resultList[(7*(numChannels - 1)) + 4])
    if count > 9e37:
        count = 0

for scopeChIdx, ch in enumerate(valOptions.scopeChannels):
    if channelGroup[scopeChIdx] is None:
        continue
    scope.write(f":CHANnel{ch}:OFFSet {mean}")

scope.write(":CDISplay")

count = 0
while count < 20:
    checkIfRunCancelled()
    resultStr = scope.query(':MEASure:RESults?')
    resultList = resultStr.split(',')
    count = float(resultList[-1])
    if count > 9e37:
        count = 0

for chIdx in range(numChannels):
    mean = float(resultList[(7*(numChannels - chIdx - 1)) + 4])
    if mean > 9e37:
        return None
    mean *= 1000 # Convert V to mV
    print(f"CH{chIdx+1}: {mean}")
    commonModeResults[chIdx] = mean

vScale = 1
for scopeChIdx, ch in enumerate(valOptions.scopeChannels):
    if channelGroup[scopeChIdx] is None:
        continue
    scope.write(f":CHANnel{ch}:SCAle {vScale}")

return commonModeResults
'''
measure.wantAllVarsGlobal = False

performMeasurements.args = ''
performMeasurements.code = r'''valResult = True

numChanPerGroup = 4
channels = valOptions.channels.copy()
while len(channels) % numChanPerGroup != 0:
    channels.append(None)

numGroups = int(len(channels) / numChanPerGroup)
channelGroups = np.reshape(channels, (numGroups, numChanPerGroup))

for channelGroup in channelGroups:
    (chA, chB, chC, chD) = channelGroup

    msg = f'Measuring channels {chA}, {chB}, {chC}, {chD}. '
    msg += (f'Please connect these channels to the scope: CH_{chA}->SCOPE_CH1, '
            f'CH_{chB}->SCOPE_2, CH_{chC}->SCOPE_3, CH_{chD}->SCOPE_4')
    beepOkDialog(msg)

    for cmIdx, cm in enumerate(valOptions.commonModeValues):
        print(f'Measuring at {cm:.2f} mV common-mode...')

        txChannelList1.commonModeVoltages = [cm]
        txChannelList1.update()
        if valOptions.pattern == 'idle':
            txChannelList1.stopPatterns()

        commonModeResults = measure(cm, channelGroup)

        for scopeChanIdx, channelStr in enumerate(channelGroup):
            if channelStr is None:
                continue
            chIdx = int(channelStr[:-1]) - 1
            wireIdx = 0 if 'P' in channelStr else 1
            measuredValue = commonModeResults[scopeChanIdx]
            rawData[chIdx][wireIdx][cmIdx] = validateMeasurement(measuredValue, cm, channelStr)
'''
performMeasurements.wantAllVarsGlobal = False

valOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
valOptions.addField('scopeIpAddress', descrip='''Keysight scope's IP address''', attrType=str, iespInstanceName='any', defaultVal='TCPIP::10.30.30.215::INSTR', displayOrder=(0, 2.0))
valOptions.addField('scopeChannels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
valOptions.addField('scopeTimeScale', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=2e-09, displayOrder=(0, 4.0))
valOptions.addField('channels', descrip='''Channels to validate''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['1P', '2P', '3P', '3N', '4P', '5P', '6P', '7P', '8P', '9P', '9N', '10P', '11P', '12P'], displayOrder=(0, 5.0))
valOptions.addField('commonModeValues', descrip='''Common mode values to validate''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0], displayOrder=(0, 6.0))
valOptions.addField('absoluteErrorThresh', descrip='''Allowable absolute value of error to pass validation''', attrType=float, iespInstanceName='any', defaultVal=20.0, displayOrder=(0, 7.0))
valOptions.addField('percentErrorThresh', descrip='''Allowable percentage of error to pass validation''', attrType=float, iespInstanceName='any', defaultVal=10.0, displayOrder=(0, 8.0))
valOptions.addField('dataRate', descrip='''Data rate to validate with''', attrType=float, iespInstanceName='any', defaultVal=16000.0, displayOrder=(0, 9.0))
valOptions.addField('pattern', descrip='''Pattern to play during validation''', attrType=str, iespInstanceName='any', defaultVal='idle', displayOrder=(0, 10.0))
valOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
valOptions.serialNumber = '1234'
valOptions.scopeIpAddress = 'TCPIP::10.30.30.215::INSTR'
valOptions.scopeChannels = [1, 2, 3, 4]
valOptions.scopeTimeScale = 2e-09
valOptions.channels = ['1P', '2P', '3P', '3N', '4P', '5P', '6P', '7P', '8P', '9P', '9N', '10P', '11P', '12P']
valOptions.commonModeValues = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
valOptions.absoluteErrorThresh = 20.0
valOptions.percentErrorThresh = 10.0
valOptions.dataRate = 16000.0
valOptions.pattern = 'idle'
valOptions.callCustomInitMethod()
validateMeasurement.args = 'measuredValue, expectedValue, channelStr'
validateMeasurement.code = r'''from pprint import pformat

absoluteError = abs(measuredValue - expectedValue)
percentError = (absoluteError / expectedValue) * 100 if expectedValue != 0 else 0

result = {'channel': channelStr,
          'expectedValue': expectedValue,
          'measuredValue': measuredValue,
          'absoluteError': absoluteError,
          'percentError': percentError,
          'fail': False}

if absoluteError > valOptions.absoluteErrorThresh or percentError > valOptions.percentErrorThresh:
    result['fail'] = True
    warningMsg(f'Failed on channel {channelStr}')
    msg = pformat(result)
    warningMsg(msg)

return result
'''
validateMeasurement.wantAllVarsGlobal = False

writeRawData.args = ''
writeRawData.code = r'''import time
import os
import json
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

jsonDict = {}
jsonDict['description'] = 'TX Common Mode Out Validation Data'
jsonDict['serialNumber'] = f'{valOptions.serialNumber}'
jsonDict['date'] = f'{dateToday}'
jsonDict['time'] = f'{timeNow}'
jsonDict['rawData'] = rawData

with open(rawDataFilePath, 'w') as f:
    json.dump(jsonDict, f, indent=4)
'''
writeRawData.wantAllVarsGlobal = False


globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 16000.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = None
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

pam3Protocol.protocol = 'pam3'

resultFolderCreator1.channelProvider = None
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

testAsPythonScript1.contextFolderType = 'thisTestFolder'
testAsPythonScript1.notes = r''''''
testAsPythonScript1.omitDefaultValues = True
testAsPythonScript1.scriptName = 'sv7_pam3_commonModeVal.py'
testAsPythonScript1.usesIespHardware = True
testAsPythonScript1.wantConnectionConfig = True

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [600.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [userPattern1]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']

userPattern1.bits = '0011'
userPattern1.notes = ''


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')

beepOkDialog._showInList = False
createRawDataResult._showInList = False
increaseLimits._showInList = False
initModule._showInList = False
initScope._showInList = False
measure._showInList = False
performMeasurements._showInList = False
validateMeasurement._showInList = False
writeRawData._showInList = False
#! TEST PROCEDURE
from dftm.errMsg import setFileLogLevel
setFileLogLevel('txChannelList', 31, printInfo=False) # Suppress logging

iesp = getIespInstance()

beepOkDialog(f'Please connect the first 4 channels to the scope ({valOptions.channels[:4]})')

# ----- Initialization -----
actualChannels = []
for channelStr in valOptions.channels:
    actualChannels.append(int(channelStr[:-1]))
actualChannels = sorted(list(set(actualChannels)))

increaseLimits()
initModule()
scope = initScope()
beepOkDialog('Please ensure a cal file with common mode '
             'IN and OUT calibration data has been loaded '
             'on the module.')

rawDataFilePath = createRawDataResult()

numCh = len(actualChannels)
numCmVals = len(valOptions.commonModeValues)
numWires = 2 # 2 wires: P and N

rawData = [[[{} for z in range(numCmVals)] for y in range(numWires)] for x in range(numCh)]


# ----- Validation -----
performMeasurements()
writeRawData()


# ----- Pass/Fail -----
failures = [True for x in rawData for y in x for z in y if z.get('fail', False)]
numFailures = len(failures)
print(f'Number of failures: {numFailures}')
if numFailures > 0:
    writeNoteForTestRun("Fail")
else:
    writeNoteForTestRun("Pass")
