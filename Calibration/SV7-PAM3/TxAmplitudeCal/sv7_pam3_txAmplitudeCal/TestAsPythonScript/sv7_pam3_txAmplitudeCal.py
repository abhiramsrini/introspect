
# Generated via TestAsPythonScript from Test 'sv7_pam3_txAmplitudeCal'
# 2024-08-05_1418


import sys
import os
import shutil
from types import FunctionType
if not ((3,7) <= sys.version_info):
    versionTuple = (sys.version_info.major, sys.version_info.minor)
    sys.exit('This script requires Python 3.7+, but you are using Python %s.%s' % versionTuple)

# change the following line to have the path to the SvtPython folder
svtPythonPath = r'C:\IntrospectRepo\DV1600\sw\Pinetree\trunk\SvtPython'
sys.path.append(svtPythonPath)

from dftm.svt import initFormFactor, createComponentContext, errorMsg
import dftm.fileUtil as fileUtil
import dftm.svt as svt

formFactorName = 'SV7C_12C40G_PAM3_DDR'
iesp = initFormFactor(formFactorName)

dir_path = os.path.dirname(os.path.realpath(__file__))
currentFolder = fileUtil.getCurrentFolder()
svtContextFolderName = 'sv7_pam3_txAmplitudeCalFolder'
svtContextFolderPath = fileUtil.joinPaths(currentFolder, svtContextFolderName)
pythonCodeFolder = os.path.join(dir_path, "..", "PythonCode")
newPythonCodeFolder = os.path.join(svtContextFolderPath, "PythonCode")
if os.path.isdir(pythonCodeFolder) and not os.path.isdir(newPythonCodeFolder):
    shutil.copytree(pythonCodeFolder, newPythonCodeFolder)
svtContext = createComponentContext(svtContextFolderPath)
svtNamesDict = svtContext.getNamesDict()
globalsDict = globals()
globalsDict.update(svtNamesDict)

ftdiSerialNumPats = {'FORMFACTOR': 'SV7C_12C40G_PAM3_DDR', 'SV7C_12C40G_PAM3_DDR': 'default'}
svt.updateFtdiSerials(inputSerials=ftdiSerialNumPats)
connected = svt.connectToHardware()

if not connected:
    errorMsg('Failed to connect to IESP hardware')

#-------------------------------------------------------------------------------
# Components:
#-------------------------------------------------------------------------------
# Note: the following only sets the values of properties whose values differ from the default
fullSwingPattern = svtContext.createComponent('SvtUserPattern', suggestedName='fullSwingPattern')
globalClockConfig1 = svtContext.createComponent('SvtGlobalClockConfig', suggestedName='globalClockConfig1')
options = svtContext.createComponent('SvtDataRecord', suggestedName='options')
pam3Protocol = svtContext.createComponent('SvtPam3Protocol', suggestedName='pam3Protocol')
resultFolderCreator1 = svtContext.createComponent('SvtResultFolderCreator', suggestedName='resultFolderCreator1')
txChannelList1 = svtContext.createComponent('SvtTxChannelList', suggestedName='txChannelList1')

fullSwingPattern.bits = '0000000000000000000000000000000011111111111111111111111111111111'





txChannelList1.commonModeVoltages = [600.0]


#-------------------------------------------------------------------------------

def beepOkDialog(msg):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    waitForOkDialog(msg)

#-------------------------------------------------------------------------------

def createCalFileResult():
    calFolderName = f"txAmplitude_{options.serialNumber}"
    calFileName = calFolderName + '.txt'
    resultFolderCreator1.resultType = 'TextReport'
    resultFolderCreator1.folderName = calFolderName
    calFolderPath = resultFolderCreator1.run()
    calFilePath = os.path.join(calFolderPath, calFileName)
    return calFilePath

#-------------------------------------------------------------------------------

def createRawDataResult():
    rawDataFolderName = f"rawData_{options.serialNumber}"
    rawDataFileName = rawDataFolderName + '.csv'
    resultFolderCreator1.resultType = 'CsvData'
    resultFolderCreator1.folderName = rawDataFolderName
    rawDataFolderPath = resultFolderCreator1.run()
    rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
    return rawDataFilePath

#-------------------------------------------------------------------------------

def getBestVertScalesAndOffsets(ch):
    amp = vodValues[0] * options.vodVoltageStep
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

#-------------------------------------------------------------------------------

def increaseLimits():
    iesp.setLimitMaximum("txCommonModeVoltage", 2500)
    iesp.setLimitMinimum("txCommonModeVoltage", 0)
    iesp.setLimitMaximum("voltageSwing", 1500)
    iesp.setLimitMinimum("voltageSwing", 0)
    
    # Common Mode Limits:   [100, 750]
    # Amplitude Limits:        [20, 1000]

#-------------------------------------------------------------------------------

def initModule():
    globalClockConfig1.dataRate = options.dataRate
    globalClockConfig1.setup()
    
    txChannelList1.channels = options.channels
    txChannelList1.patterns = [fullSwingPattern]
    txChannelList1.commonModeVoltages = [options.commonModeVoltage]
    txChannelList1.setup()

#-------------------------------------------------------------------------------

def initScope():
    import pyvisa
    
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

#-------------------------------------------------------------------------------

def measure(amp, vScale):
    numChannels = len(options.scopeChannels)
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

#-------------------------------------------------------------------------------

def performMeasurements():
    numChanPerGroup = 4
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

#-------------------------------------------------------------------------------

def plotCalResults():
    from dftm.matplotlibConfig import matplotlib
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

#-------------------------------------------------------------------------------

def writeCalFile():
    import datetime
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

#-------------------------------------------------------------------------------

def writeRawData():
    import time
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

#-------------------------------------------------------------------------------

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
#-------------------------------------------------------------------------------

def testProcedure():
    global arrayShape, calFilePath, iesp, numCh, numVodVals, numXcvrs, rawData, rawDataFilePath, scope, vodValues
    svtContext.createRunResultFolder() # create a dated sub-folder for results
    svtContext.initForRun() # re-init components for this run
    namesDict = svtContext.getNamesDict()
    namesDict.update(globalsDict)
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
    svtContext.runEnding()
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    testProcedure()
#-------------------------------------------------------------------------------
