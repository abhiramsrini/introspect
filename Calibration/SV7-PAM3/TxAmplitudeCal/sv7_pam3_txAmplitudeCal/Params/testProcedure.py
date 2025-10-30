# SVT Test
# SVT version 24.4.b5
# Test saved 2024-08-05_1418
# Form factor: SV7C_12C40G_PAM3_DDR
# PY3
# Checksum: ab88ddd058f67bcab0add79843601dce
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


beepOkDialog = _create('beepOkDialog', 'SvtFunction', iespName='None')
createCalFileResult = _create('createCalFileResult', 'SvtFunction', iespName='None')
createRawDataResult = _create('createRawDataResult', 'SvtFunction', iespName='None')
getBestVertScalesAndOffsets = _create('getBestVertScalesAndOffsets', 'SvtFunction', iespName='None')
increaseLimits = _create('increaseLimits', 'SvtFunction', iespName='None')
initModule = _create('initModule', 'SvtFunction', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measure = _create('measure', 'SvtFunction', iespName='None')
options = _create('options', 'SvtDataRecord', iespName='None')
performMeasurements = _create('performMeasurements', 'SvtFunction', iespName='None')
plotCalResults = _create('plotCalResults', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

fullSwingPattern = _create('fullSwingPattern', 'SvtUserPattern')
globalClockConfig1 = _create('globalClockConfig1', 'SvtGlobalClockConfig')
pam3Protocol = _create('pam3Protocol', 'SvtPam3Protocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')

beepOkDialog.args = 'msg'
beepOkDialog.code = r'''dftUtil.beep(554,250)
dftUtil.beep(554,320)
waitForOkDialog(msg)
'''
beepOkDialog.wantAllVarsGlobal = False

createCalFileResult.args = ''
createCalFileResult.code = r'''calFolderName = f"txAmplitude_{options.serialNumber}"
calFileName = calFolderName + '.txt'
resultFolderCreator1.resultType = 'TextReport'
resultFolderCreator1.folderName = calFolderName
calFolderPath = resultFolderCreator1.run()
calFilePath = os.path.join(calFolderPath, calFileName)
return calFilePath
'''
createCalFileResult.wantAllVarsGlobal = False

createRawDataResult.args = ''
createRawDataResult.code = r'''rawDataFolderName = f"rawData_{options.serialNumber}"
rawDataFileName = rawDataFolderName + '.csv'
resultFolderCreator1.resultType = 'CsvData'
resultFolderCreator1.folderName = rawDataFolderName
rawDataFolderPath = resultFolderCreator1.run()
rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
return rawDataFilePath
'''
createRawDataResult.wantAllVarsGlobal = False

getBestVertScalesAndOffsets.args = 'ch'
getBestVertScalesAndOffsets.code = r'''amp = vodValues[0] * options.vodVoltageStep
txChannelList1.voltageSwings = [amp]
txChannelList1.update()

scope.write(f":AUToscale:VERTical CHANnel{options.scopeChannels[0]}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

resultStr = scope.query(f":CHANnel{options.scopeChannels[0]}:SCAle?")
vScale1 = float(resultStr)
resultStr = scope.query(f":CHANnel{options.scopeChannels[0]}:OFFSet?")
offset1 = float(resultStr)

amp = vodValues[-1] * options.vodVoltageStep
txChannelList1.voltageSwings = [amp]
txChannelList1.update()

scope.write(f":AUToscale:VERTical CHANnel{options.scopeChannels[0]}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

resultStr = scope.query(f":CHANnel{options.scopeChannels[0]}:SCAle?")
vScale2 = float(resultStr)
resultStr = scope.query(f":CHANnel{options.scopeChannels[0]}:OFFSet?")
offset2 = float(resultStr)

numPoints = len(vodValues)
vScales = np.linspace(vScale1, vScale2, numPoints, endpoint=True)
offsets = np.linspace(offset1, offset2, numPoints, endpoint=True)
return vScales.tolist(), offsets.tolist()
'''
getBestVertScalesAndOffsets.wantAllVarsGlobal = False

increaseLimits.args = ''
increaseLimits.code = r'''iesp.setLimitMaximum("txCommonModeVoltage", 2500)
iesp.setLimitMinimum("txCommonModeVoltage", 0)
iesp.setLimitMaximum("voltageSwing", 1500)
iesp.setLimitMinimum("voltageSwing", 0)

# Common Mode Limits:   [100, 750]
# Amplitude Limits:        [20, 1000]
'''
increaseLimits.wantAllVarsGlobal = False

initModule.args = ''
initModule.code = r'''globalClockConfig1.dataRate = options.dataRate
globalClockConfig1.setup()

txChannelList1.channels = options.channels
txChannelList1.patterns = [fullSwingPattern]
txChannelList1.commonModeVoltages = [options.commonModeVoltage]
txChannelList1.setup()
'''
initModule.wantAllVarsGlobal = False

initScope.args = ''
initScope.code = r'''import pyvisa

rm = pyvisa.ResourceManager()
try:
    scope = rm.open_resource(options.scopeIpAddress, timeout=20000)
except Exception as e:
    availAddresses = rm.list_resources()
    print(f"Could not connect to scope. Available addresses: {availAddresses}")
    exit()

scope.write_termination = '\n'
scope.read_termination = '\n'

scope.write('*RST')
scope.write(f":TIMebase:SCALe {options.scopeTimeScale}")

for ch in options.scopeChannels:
    scope.write(f":CHANnel{ch}:DISPlay ON")
for ch in options.scopeChannels:
    scope.write(f":AUToscale:VERTical CHANnel{ch}")

sleepMillis(1000)
while not '1' in scope.query('*OPC?'):
    sleepMillis(1000)

for ch in options.scopeChannels:
    scope.write(f":CALibrate:SKEW CHANnel{ch},0")

scope.write("MEASure:STATistics ON")

return scope
'''
initScope.wantAllVarsGlobal = False

measure.args = 'amp, vScale'
measure.code = r'''numChannels = len(options.scopeChannels)
amplitudeResults = [0] * numChannels

if vScale is not None:
    for ch in options.scopeChannels:
        scope.write(f":CHANnel{ch}:SCALe {vScale}")

for ch in options.scopeChannels:
    scope.write(f":TRIGger:LEVel:FIFTy")
    scope.write(f":MEASure:VAMPlitude CHANnel{ch}")

count = 0
failCount = 0
while count < 20:
    checkIfRunCancelled()
    resultStr = scope.query(':MEASure:RESults?')
    resultList = resultStr.split(',')
    count = float(resultList[-1])
    if count > 9e37:
        count = 0
        failCount += 1
        if failCount > 10:
            return None
scope.write(":CDISplay")

count = 0
while count < options.numMeasurements:
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
    amplitudeResults[chIdx] = mean

return amplitudeResults
'''
measure.wantAllVarsGlobal = False

options.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
options.addField('hardwareRevision', descrip='''Hardware revision''', attrType=str, iespInstanceName='any', defaultVal='A', displayOrder=(0, 2.0))
options.addField('speedGrade', descrip='''Speed grade''', attrType=int, iespInstanceName='any', defaultVal=1, displayOrder=(0, 3.0))
options.addField('scopeIpAddress', descrip='''Visa string specifying location of the calibration scope''', attrType=str, iespInstanceName='any', defaultVal='TCPIP::10.30.30.215::INSTR', displayOrder=(0, 4.0))
options.addField('scopeChannels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 5.0))
options.addField('scopeTimeScale', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=2e-09, displayOrder=(0, 6.0))
options.addField('dataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='any', defaultVal=16000.0, displayOrder=(0, 7.0))
options.addField('channels', descrip='''List of channels to calibrate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], displayOrder=(0, 8.0))
options.addField('calHeader', descrip='''Header ID string for the amplitude calibration data''', attrType=str, iespInstanceName='any', defaultVal='tx_amplitude_calibration_data', displayOrder=(0, 9.0))
options.addField('plotResults', descrip='''Do you wish to plot the calibration results?''', attrType=bool, iespInstanceName='any', defaultVal=True, displayOrder=(0, 10.0))
options.addField('commonModeVoltage', descrip='''Common mode voltage used for calibration''', attrType=float, iespInstanceName='any', defaultVal=100.0, displayOrder=(0, 11.0))
options.addField('numMeasurements', descrip='''''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 12.0))
options.addField('numVodVals', descrip='''''', attrType=int, iespInstanceName='any', defaultVal=32, displayOrder=(0, 13.0))
options.addField('vodStart', descrip='''The actual start of VOD values. VOD 0 and 1 do not output anything.''', attrType=int, iespInstanceName='any', defaultVal=2, displayOrder=(0, 14.0))
options.addField('vodVoltageStep', descrip='''VOD voltage step in mV''', attrType=float, iespInstanceName='any', defaultVal=35.48387, displayOrder=(0, 15.0))
options.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
options.serialNumber = '1234'
options.hardwareRevision = 'A'
options.speedGrade = 1
options.scopeIpAddress = 'TCPIP::10.30.30.215::INSTR'
options.scopeChannels = [1, 2, 3, 4]
options.scopeTimeScale = 2e-09
options.dataRate = 16000.0
options.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
options.calHeader = 'tx_amplitude_calibration_data'
options.plotResults = True
options.commonModeVoltage = 100.0
options.numMeasurements = 100
options.numVodVals = 32
options.vodStart = 2
options.vodVoltageStep = 35.48387
options.callCustomInitMethod()
performMeasurements.args = ''
performMeasurements.code = r'''numChanPerGroup = 4
channels = options.channels.copy()
while len(channels) % numChanPerGroup != 0:
    channels.append(None)

numGroups = int(len(channels) / numChanPerGroup)
channelGroups = np.reshape(channels, (numGroups, numChanPerGroup))

# ---
def isMeasureSuccess():
    nonlocal amplitudeResults
    if amplitudeResults is None:
        return False
    return True
# ---

vScales, _ = getBestVertScalesAndOffsets(channelGroups[0][0])

for channelGroup in channelGroups:
    (chA, chB, chC, chD) = channelGroup

    msg = f'Measuring channels {chA}P, {chB}P, {chC}P, {chD}P. '
    msg += (f'Please connect these channels to the scope: CH_{chA}P->SCOPE_CH1, '
            f'CH_{chB}P->SCOPE_2, CH_{chC}P->SCOPE_3, CH_{chD}P->SCOPE_4')
    beepOkDialog(msg)

    for vodIdx, vod in enumerate(vodValues):
        vScale = vScales[vodIdx]

        amp = vod * options.vodVoltageStep
        print(f'Measuring at {amp:.2f} mV amplitude...')

        txChannelList1.voltageSwings = [amp]
        txChannelList1.update()

        amplitudeResults = measure(amp, vScale)
        while not isMeasureSuccess():
            for ch in options.scopeChannels:
                scope.write(f":AUToscale:VERTical CHANnel{ch}")

            sleepMillis(1000)
            while not '1' in scope.query('*OPC?'):
                checkIfRunCancelled()
                sleepMillis(1000)
            amplitudeResults = measure(amp, None)

        for scopeChanIdx, channel in enumerate(channelGroup):
            if channel is None:
                continue
            chIdx = channel - 1
            rawData[chIdx, vodIdx] = amplitudeResults[scopeChanIdx]
'''
performMeasurements.wantAllVarsGlobal = False

plotCalResults.args = ''
plotCalResults.code = r'''from dftm.matplotlibConfig import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate

plotFolderName = f"plots_{options.serialNumber}"
resultFolderCreator1.resultType = 'Generic'
resultFolderCreator1.folderName = plotFolderName
plotFolderPath = resultFolderCreator1.run()

# ---
def findNearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return array[idx]
# ---

for channel in options.channels:
    chIdx = channel - 1
    measuredVoltages = rawData[chIdx, :]
    rawFunc = interpolate.interp1d(vodValues, measuredVoltages, kind='nearest') # Step function

    plt.figure(figsize=(500,1000))
    fig, axis = plt.subplots(2, 1)

    axis[0].plot(vodValues, measuredVoltages, '.b', label='Raw')
    axis[0].plot(vodValues, rawFunc(vodValues), '-.b', label='Raw Fit')
    axis[0].set_xlabel("Vod Values")
    axis[0].set_ylabel("Measured Amplitudes")
    axis[0].legend(loc="upper left")
    axis[0].set_title(f"CH_{channel:02} Vod vs Measured Amplitude")

    startVoltage = int(round(options.vodStart*options.vodVoltageStep))
    maxVoltage = int(round(options.vodVoltageStep * options.numVodVals))
    desiredVoltages = np.asarray(list(range(startVoltage, maxVoltage)), dtype=np.float)
    theoreticalMeasuredVoltages = [findNearest(measuredVoltages, x) for x in desiredVoltages]
    error = np.abs(theoreticalMeasuredVoltages - desiredVoltages)
    axis[1].plot(desiredVoltages, theoreticalMeasuredVoltages, '.g', label='Expected Output')
    axis[1].plot(desiredVoltages, error, '-.y', label=f'Error (max={max(error):.2f})')
    axis[1].set_xlabel("Desired Voltage")
    axis[1].set_ylabel("Expected Output")
    axis[1].legend(loc="upper left")
    axis[1].set_title(f"CH_{channel:02} Desired vs Expected Output")

    plotFileName = f"ch{channel:02}_plot.png"
    plotFilePath = os.path.join(plotFolderPath, plotFileName)
    plt.savefig(plotFilePath)
    plt.close()
'''
plotCalResults.wantAllVarsGlobal = False

writeCalFile.args = ''
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

lines = []

lines.append("BEGIN SECTION")
lines.append("section type : header")
lines.append(f"serial number : {options.serialNumber}")
lines.append(f"hardware revision : {options.hardwareRevision}")
lines.append(f"date of manufacture(YYYYMMDD) : {date}")
lines.append(f"date of calibration(YYYYMMDD) : {date}")
lines.append(f"speed grade : {options.speedGrade}")
lines.append("END SECTION")

lines.append("")

lines.append("BEGIN SECTION")
lines.append(f"section type : {options.calHeader}")
lines.append(f"num lanes : {len(options.channels) * numXcvrs}")
lines.append(f"num vod values : {options.numVodVals}")
lines.append("#each line is a channel, each element is the voltage at the given VOD setting")

for vodIdx in range(options.numVodVals):
    lineStr = ""
    for chIdx in range(numCh):
        for xcvrIdx in range(numXcvrs):
            measuredVodIdx = vodIdx - options.vodStart
            if measuredVodIdx < 0:
                lineStr += f"{0:.16f} "
                continue
            measureVoltage_mV = rawData[chIdx, measuredVodIdx]
            lineStr += f"{measureVoltage_mV * 1000:.16f} " # Multiply mV to uV

    for chIdx in range(12-numCh):
        for xcvrIdx in range(numXcvrs):
            lineStr += f"{0:.16f} "

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
lines.append("ResultDescrip, TX Amplitude Calibration Data")
lines.append(f"SerialNumber, {options.serialNumber}")
lines.append(f"Date, {dateToday}")
lines.append(f"Time, {timeNow}")
lines.append("DATA")
lines.append("CHANNEL, VOD_VAL, MEAS_VAMP_FULL_MV")

for chIdx, channel in enumerate(options.channels):
    for vodIdx, vod in enumerate(vodValues):
        measuredAmplitude = rawData[chIdx, vodIdx]
        lines.append(f"{channel}, {vod}, {measuredAmplitude}")

with open(rawDataFilePath, 'w') as f:
    f.writelines('\n'.join(lines))
'''
writeRawData.wantAllVarsGlobal = False


fullSwingPattern.bits = '0000000000000000000000000000000011111111111111111111111111111111'
fullSwingPattern.notes = ''

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
txChannelList1.patterns = [PAT_DIV40]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')

beepOkDialog._showInList = False
createCalFileResult._showInList = False
createRawDataResult._showInList = False
getBestVertScalesAndOffsets._showInList = False
increaseLimits._showInList = False
initModule._showInList = False
initScope._showInList = False
measure._showInList = False
performMeasurements._showInList = False
plotCalResults._showInList = False
writeCalFile._showInList = False
writeRawData._showInList = False
#! TEST PROCEDURE
import numpy as np
import os

from dftm.errMsg import setFileLogLevel
setFileLogLevel('txChannelList', 31, printInfo=False) # Suppress logging

iesp = getIespInstance()

beepOkDialog(f'Please connect the first 4 channels to the scope ({options.channels[:4]})')


# ----- Initialization -----
increaseLimits()
initModule()
scope = initScope()
beepOkDialog('Please ensure a cal file with common mode '
             'IN and OUT calibration data has been loaded '
             'on the module.')

rawDataFilePath = createRawDataResult()
calFilePath = createCalFileResult()

vodValues = list(range(options.vodStart, options.numVodVals))

numCh = len(options.channels)
numXcvrs = 2 # per channel
numVodVals = len(vodValues)

arrayShape = (numCh, numVodVals)
rawData = np.zeros(arrayShape, dtype=np.double)
rawData.fill(np.nan)


# ----- Calibration -----
performMeasurements()
writeRawData()
writeCalFile()
if options.plotResults:
    plotCalResults()
