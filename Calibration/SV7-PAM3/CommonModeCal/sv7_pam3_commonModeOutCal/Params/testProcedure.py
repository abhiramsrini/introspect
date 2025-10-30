# SVT Test
# SVT version 24.4.b5
# Test saved 2024-08-05_1308
# Form factor: SV7C_12C40G_PAM3_DDR
# PY3
# Checksum: 9ef5e1f6fc4646e5a8bd8ace47d2085c
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


beepOkDialog = _create('beepOkDialog', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
createCalFileResult = _create('createCalFileResult', 'SvtFunction', iespName='None')
createRawDataResult = _create('createRawDataResult', 'SvtFunction', iespName='None')
findVertScaleAndOffset = _create('findVertScaleAndOffset', 'SvtFunction', iespName='None')
increaseLimits = _create('increaseLimits', 'SvtFunction', iespName='None')
initModule = _create('initModule', 'SvtFunction', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measure = _create('measure', 'SvtFunction', iespName='None')
performMeasurements = _create('performMeasurements', 'SvtFunction', iespName='None')
plotCalResults = _create('plotCalResults', 'SvtFunction', iespName='None')
processRawData = _create('processRawData', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

globalClockConfig1 = _create('globalClockConfig1', 'SvtGlobalClockConfig')
pam3Protocol = _create('pam3Protocol', 'SvtPam3Protocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
userPattern1 = _create('userPattern1', 'SvtUserPattern')

beepOkDialog.args = 'msg'
beepOkDialog.code = r'''dftUtil.beep(554,250)
dftUtil.beep(554,320)
waitForOkDialog(msg)
'''
beepOkDialog.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('hardwareRevision', descrip='''Hardware revision''', attrType=str, iespInstanceName='any', defaultVal='A', displayOrder=(0, 2.0))
calOptions.addField('speedGrade', descrip='''Speed grade''', attrType=int, iespInstanceName='any', defaultVal=1, displayOrder=(0, 3.0))
calOptions.addField('scopeIpAddress', descrip='''Visa string specifying location of the calibration scope''', attrType=str, iespInstanceName='any', defaultVal='TCPIP::10.30.30.215::INSTR', displayOrder=(0, 4.0))
calOptions.addField('scopeChannels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 5.0))
calOptions.addField('scopeTimeScale', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=2e-09, displayOrder=(0, 6.0))
calOptions.addField('dataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='any', defaultVal=16000.0, displayOrder=(0, 7.0))
calOptions.addField('channels', descrip='''List of channels to calibrate''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['1P', '2P', '3P', '3N', '4P', '5P', '6P', '7P', '8P', '9P', '9N', '10P', '11P', '12P'], displayOrder=(0, 8.0))
calOptions.addField('calHeader', descrip='''Header ID string for the common mode calibration data''', attrType=str, iespInstanceName='any', defaultVal='tx_common_mode_calibration_data', displayOrder=(0, 9.0))
calOptions.addField('commonModeValues', descrip='''Common-mode voltages to be calibrated''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[0.0, 250.0, 500.0, 750.0, 1000.0, 1250.0, 1500.0], displayOrder=(0, 10.0))
calOptions.addField('plotResults', descrip='''Do you wish to plot the calibration results?''', attrType=bool, iespInstanceName='any', defaultVal=True, displayOrder=(0, 11.0))
calOptions.addField('pattern', descrip='''Pattern to play during calibration''', attrType=str, iespInstanceName='any', defaultVal='idle', displayOrder=(0, 12.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.hardwareRevision = 'A'
calOptions.speedGrade = 1
calOptions.scopeIpAddress = 'TCPIP::10.30.30.215::INSTR'
calOptions.scopeChannels = [1, 2, 3, 4]
calOptions.scopeTimeScale = 2e-09
calOptions.dataRate = 16000.0
calOptions.channels = ['1P', '2P', '3P', '3N', '4P', '5P', '6P', '7P', '8P', '9P', '9N', '10P', '11P', '12P']
calOptions.calHeader = 'tx_common_mode_calibration_data'
calOptions.commonModeValues = [0.0, 250.0, 500.0, 750.0, 1000.0, 1250.0, 1500.0]
calOptions.plotResults = True
calOptions.pattern = 'idle'
calOptions.callCustomInitMethod()
createCalFileResult.args = ''
createCalFileResult.code = r'''calFolderName = f"commonModeOut_{calOptions.serialNumber}"
calFileName = calFolderName + '.txt'
resultFolderCreator1.resultType = 'TextReport'
resultFolderCreator1.folderName = calFolderName
calFolderPath = resultFolderCreator1.run()
calFilePath = os.path.join(calFolderPath, calFileName)
return calFilePath
'''
createCalFileResult.wantAllVarsGlobal = False

createRawDataResult.args = ''
createRawDataResult.code = r'''rawDataFolderName = f"rawData_{calOptions.serialNumber}"
rawDataFileName = rawDataFolderName + '.csv'
resultFolderCreator1.resultType = 'CsvData'
resultFolderCreator1.folderName = rawDataFolderName
rawDataFolderPath = resultFolderCreator1.run()
rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
return rawDataFilePath
'''
createRawDataResult.wantAllVarsGlobal = False

findVertScaleAndOffset.args = 'ch'
findVertScaleAndOffset.code = r'''txChannelList1.commonModeVoltages = [calOptions.commonModeValues[0]]
txChannelList1.update()
if calOptions.pattern == 'idle':
    txChannelList1.stopPatterns()

scope.write(f":AUToscale:VERTical CHANnel{calOptions.scopeChannels[0]}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

resultStr = scope.query(f":CHANnel{calOptions.scopeChannels[0]}:SCAle?")
vScale1 = float(resultStr)
resultStr = scope.query(f":CHANnel{calOptions.scopeChannels[0]}:OFFSet?")
offset1 = float(resultStr)

txChannelList1.commonModeVoltages = [calOptions.commonModeValues[-1]]
txChannelList1.update()
if calOptions.pattern == 'idle':
    txChannelList1.stopPatterns()

scope.write(f":AUToscale:VERTical CHANnel{calOptions.scopeChannels[0]}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

resultStr = scope.query(f":CHANnel{calOptions.scopeChannels[0]}:SCAle?")
vScale2 = float(resultStr)
resultStr = scope.query(f":CHANnel{calOptions.scopeChannels[0]}:OFFSet?")
offset2 = float(resultStr)

numPoints = len(calOptions.commonModeValues)
vScales = np.linspace(vScale1, vScale2, numPoints, endpoint=True)
offsets = np.linspace(offset1, offset2, numPoints, endpoint=True)
return vScales.tolist(), offsets.tolist()
'''
findVertScaleAndOffset.wantAllVarsGlobal = False

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
initModule.code = r'''globalClockConfig1.dataRate = calOptions.dataRate
globalClockConfig1.setup()

txChannelList1.channels = actualChannels

if calOptions.pattern == 'idle':
    txChannelList1.patterns = ['PAT_DIV40']
else:
    txChannelList1.patterns = [calOptions.pattern]

txChannelList1.setup()

if calOptions.pattern == 'idle':
    txChannelList1.stopPatterns()
'''
initModule.wantAllVarsGlobal = False

initScope.args = ''
initScope.code = r'''import pyvisa

rm = pyvisa.ResourceManager()
try:
    scope = rm.open_resource(calOptions.scopeIpAddress, timeout=20000)
except Exception as e:
    availAddresses = rm.list_resources()
    print(f"Could not connect to scope. Available addresses: {availAddresses}")
    exit()

scope.write_termination = '\n'
scope.read_termination = '\n'

scope.write('*RST')
scope.write(f":TIMebase:SCALe {calOptions.scopeTimeScale}")

for ch in calOptions.scopeChannels:
    scope.write(f":CHANnel{ch}:DISPlay ON")
for ch in calOptions.scopeChannels:
    scope.write(f":AUToscale:VERTical CHANnel{ch}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

for ch in calOptions.scopeChannels:
    scope.write(f":CALibrate:SKEW CHANnel{ch},0")

scope.write("MEASure:STATistics ON")

scope.write(":TRIGger:HYSTeresis HSENsitivity")

return scope
'''
initScope.wantAllVarsGlobal = False

measure.args = 'cm, vScale, offset'
measure.code = r'''numChannels = len(calOptions.scopeChannels)
commonModeResults = [0] * numChannels

if cm > 1000:
    vScale *= 2
while not '1' in scope.query('*OPC?'):
    checkIfRunCancelled()
    sleepMillis(1000)

for ch in calOptions.scopeChannels:
    scope.write(f":CHANnel{ch}:SCAle {vScale}")
    scope.write(f":CHANnel{ch}:OFFSet {offset}")
    scope.write(f":MEASure:VAVerage DISPlay,CHANnel{ch}")

scope.write(f":TRIGger:LEVel:FIFTy")

count = 0
failCount = 0
while count < 20:
    checkIfRunCancelled()
    resultStr = scope.query(':MEASure:RESults?')
    resultList = resultStr.split(',')
    count = float(resultList[-1])
    mean = float(resultList[(7*(numChannels - 1)) + 4])
    if count > 9e37:
        if failCount > 10:
            return None
        count = 0
        failCount += 1

for ch in calOptions.scopeChannels:
      scope.write(f":CHANnel{ch}:OFFSet {mean}")

scope.write(":CDISplay")

count = 0
while count < 100:
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
for ch in calOptions.scopeChannels:
    scope.write(f":CHANnel{ch}:SCAle {vScale}")

return commonModeResults
'''
measure.wantAllVarsGlobal = False

performMeasurements.args = ''
performMeasurements.code = r'''numChanPerGroup = 4
channels = calOptions.channels.copy()
while len(channels) % numChanPerGroup != 0:
    channels.append(None)

numGroups = int(len(channels) / numChanPerGroup)
channelGroups = np.reshape(channels, (numGroups, numChanPerGroup))

# ---
def isMeasureSuccess():
    nonlocal commonModeResults
    if commonModeResults is None:
        return False
    return True
# ---

vScales, offsets = findVertScaleAndOffset(channelGroups[0][0])

for channelGroup in channelGroups:
    (chA, chB, chC, chD) = channelGroup

    msg = f'Measuring channels {chA}, {chB}, {chC}, {chD}. '
    msg += (f'Please connect these channels to the scope: CH_{chA}->SCOPE_CH1, '
            f'CH_{chB}->SCOPE_2, CH_{chC}->SCOPE_3, CH_{chD}->SCOPE_4')
    beepOkDialog(msg)

    for cmIdx, cm in enumerate(calOptions.commonModeValues):
        vScale = vScales[cmIdx]
        offset = offsets[cmIdx]

        print(f'Measuring at {cm:.2f} mV common-mode...')

        txChannelList1.commonModeVoltages = [cm]
        txChannelList1.update()
        if calOptions.pattern == 'idle':
            txChannelList1.stopPatterns()

        commonModeResults = None
        while not isMeasureSuccess():
            commonModeResults = measure(cm, vScale, offset)
            vScale *= 2

        for scopeChanIdx, channelStr in enumerate(channelGroup):
            if channelStr is None:
                continue
            chIdx = int(channelStr[:-1]) - 1
            wireIdx = 0 if 'P' in channelStr else 1
            rawData[chIdx, wireIdx, cmIdx] = commonModeResults[scopeChanIdx]
'''
performMeasurements.wantAllVarsGlobal = False

plotCalResults.args = ''
plotCalResults.code = r'''from dftm.matplotlibConfig import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate

plotFolderName = f"plots_{calOptions.serialNumber}"
resultFolderCreator1.resultType = 'Generic'
resultFolderCreator1.folderName = plotFolderName
plotFolderPath = resultFolderCreator1.run()

# Common Mode
commonModeValues = calOptions.commonModeValues
for channelStr in calOptions.channels:
    chIdx = int(channelStr[:-1]) - 1
    wireIdx = 0 if 'P' in channelStr else 1
    rawFunc = interpolate.interp1d(commonModeValues, rawData[chIdx, wireIdx, :], fill_value='extrapolate')

    calPoly = commonModeCoeffs[chIdx, wireIdx, :]
    calFunc = np.poly1d(calPoly)

    plt.figure()
    plt.plot(commonModeValues, rawData[chIdx, wireIdx, :], '.b', label='Raw')
    plt.plot(commonModeValues, rawFunc(commonModeValues), '-.b', label='Raw Fit')
    plt.plot(commonModeValues, calFunc(commonModeValues), '.r', label='Polynomial')
    plt.plot(commonModeValues, commonModeValues, '.g', label='Goal')

    start = int(np.ceil(min(commonModeValues)))
    end = int(np.floor(max(commonModeValues)))
    x = np.linspace(start, end, end - start + 1)
    calibratedData = rawFunc(calFunc(x))
    plt.plot(x, calibratedData, '-.r', label='Calibrated')

    error = x - calibratedData
    plt.plot(x, error, '-.y', label=f'Error (max={max(error):.2f})')

    plt.legend(loc="upper left")

    plt.xlabel("Common Mode Values")
    plt.ylabel("Measured and Calibrated Values")
    plt.title(f"CH_{int(channelStr[:-1]):02}{channelStr[-1]} Common Mode")

    plotFileName = f"{int(channelStr[:-1]):02}{channelStr[-1]}_cm_plot.png"
    plotFilePath = os.path.join(plotFolderPath, plotFileName)
    plt.savefig(plotFilePath)
    plt.close()
'''
plotCalResults.wantAllVarsGlobal = False

processRawData.args = ''
processRawData.code = r'''arrayShape = (numCh, numWires, numCmVals)

# Compute common mode polynomials
for channelStr in calOptions.channels:
    chIdx = int(channelStr[:-1]) - 1
    wireIdx = 0 if 'P' in channelStr else 1
    poly = np.polyfit(rawData[chIdx, wireIdx, :], calOptions.commonModeValues, 4)
    commonModeCoeffs[chIdx, wireIdx, :] = poly
'''
processRawData.wantAllVarsGlobal = False

writeCalFile.args = ''
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

lines = []

lines.append("BEGIN SECTION")
lines.append("section type : header")
lines.append(f"serial number : {calOptions.serialNumber}")
lines.append(f"hardware revision : {calOptions.hardwareRevision}")
lines.append(f"date of manufacture(YYYYMMDD) : {date}")
lines.append(f"date of calibration(YYYYMMDD) : {date}")
lines.append(f"speed grade : {calOptions.speedGrade}")
lines.append("END SECTION")

lines.append("")

lines.append("BEGIN SECTION")
lines.append(f"section type : {calOptions.calHeader}")
lines.append(f"num lanes : {len(actualChannels)}")
lines.append("#common mode x^4, x^3, x^2, x^1, x^0 coefficients.")

(numCh, numWires, numCoeffs) = commonModeCoeffs.shape
for coeffIdx in range(numCoeffs):
    for wireIdx in range(numWires):
        lineStr = ""
        for chIdx in range(numCh):
            value = commonModeCoeffs[chIdx, wireIdx, coeffIdx]
            if coeffIdx == numCoeffs - 1:
                value *= 1000 # Multiply mV to uV for the offset

            if not lineStr:
                lineStr += f"{value:.16f}"
            else:
                lineStr += f" {value:.16f}"

        for chIdx in range(12-numCh):
            value = 0
            if not lineStr:
                lineStr += f"{value:.16f}"
            else:
                lineStr += f" {value:.16f}"

        lines.append(lineStr)

lines.append("END SECTION")

with open(calFilePath, 'w') as f:
    f.writelines('\n'.join(lines))
'''
writeCalFile.wantAllVarsGlobal = False

writeRawData.args = ''
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

lines = []
lines.append("ResultDescrip, TX Common Mode Out Calibration Data")
lines.append(f"SerialNumber, {calOptions.serialNumber}")
lines.append(f"Date, {dateToday}")
lines.append(f"Time, {timeNow}")
lines.append("CHANNEL, EXPECTED_VCM_MV, MEAS_CHP_VCM_MV, MEAS_CHN_VCM_MV")

for chIdx, channel in enumerate(actualChannels):
    for cmIdx, cm in enumerate(calOptions.commonModeValues):
        measuredCommonMode = rawData[chIdx, :, cmIdx]
        lines.append(f"{channel}, {cm:.6f}, {measuredCommonMode[0]}, {measuredCommonMode[1]}")

with open(rawDataFilePath, 'w') as f:
    f.writelines('\n'.join(lines))
'''
writeRawData.wantAllVarsGlobal = False


globalClockConfig1.clockRecoveryChannel = 8
globalClockConfig1.dataRate = 16000.0
globalClockConfig1.refClockSyncMode = 'synchronous'
globalClockConfig1.referenceClocks = None
globalClockConfig1.sscEnabled = False
globalClockConfig1.sscFrequency = 50.0
globalClockConfig1.sscSpread = 1.0

pam3Protocol.protocol = 'pam3'

resultFolderCreator1.channelProvider = None
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

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
createCalFileResult._showInList = False
createRawDataResult._showInList = False
increaseLimits._showInList = False
initModule._showInList = False
initScope._showInList = False
measure._showInList = False
performMeasurements._showInList = False
plotCalResults._showInList = False
processRawData._showInList = False
writeCalFile._showInList = False
writeRawData._showInList = False
#! TEST PROCEDURE
import numpy as np
import os

from dftm.errMsg import setFileLogLevel
setFileLogLevel('txChannelList', 31, printInfo=False) # Suppress logging

iesp = getIespInstance()

beepOkDialog(f'Please connect the first 4 channels to the scope ({calOptions.channels[:4]})')


# ----- Initialization -----
actualChannels = []
for channelStr in calOptions.channels:
    actualChannels.append(int(channelStr[:-1]))
actualChannels = sorted(list(set(actualChannels)))

increaseLimits()
initModule()
scope = initScope()
beepOkDialog('Please ensure a cal file with ONLY common mode '
             'IN calibration data has been loaded on the module.')

rawDataFilePath = createRawDataResult()
calFilePath = createCalFileResult()

numCh = len(actualChannels)
numCmVals = len(calOptions.commonModeValues)
numWires = 2 # 2 wires: P and N

arrayShape = (numCh, numWires, numCmVals)
rawData = np.zeros(arrayShape, dtype=np.double)
rawData.fill(np.nan)

numCoeffs = 5
arrayShape = (numCh, numWires, numCoeffs)
commonModeCoeffs = np.zeros(arrayShape, dtype=np.double)
commonModeCoeffs[:, :, 1] = 1 # Default: y = x


# ----- Calibration -----
performMeasurements()
writeRawData()
processRawData()
writeCalFile()
if calOptions.plotResults:
    plotCalResults()
