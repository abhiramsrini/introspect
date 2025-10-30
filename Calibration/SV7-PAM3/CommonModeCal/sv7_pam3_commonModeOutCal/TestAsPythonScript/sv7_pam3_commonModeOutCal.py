
# Generated via TestAsPythonScript from Test 'sv7_pam3_commonModeOutCal'
# 2024-08-05_1308


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
svtContextFolderName = 'sv7_pam3_commonModeOutCalFolder'
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
calOptions = svtContext.createComponent('SvtDataRecord', suggestedName='calOptions')
globalClockConfig1 = svtContext.createComponent('SvtGlobalClockConfig', suggestedName='globalClockConfig1')
pam3Protocol = svtContext.createComponent('SvtPam3Protocol', suggestedName='pam3Protocol')
resultFolderCreator1 = svtContext.createComponent('SvtResultFolderCreator', suggestedName='resultFolderCreator1')
txChannelList1 = svtContext.createComponent('SvtTxChannelList', suggestedName='txChannelList1')
userPattern1 = svtContext.createComponent('SvtUserPattern', suggestedName='userPattern1')





txChannelList1.commonModeVoltages = [600.0]
txChannelList1.patterns = [userPattern1]

userPattern1.bits = '0011'


#-------------------------------------------------------------------------------

def beepOkDialog(msg):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    waitForOkDialog(msg)

#-------------------------------------------------------------------------------

def createCalFileResult():
    calFolderName = f"commonModeOut_{calOptions.serialNumber}"
    calFileName = calFolderName + '.txt'
    resultFolderCreator1.resultType = 'TextReport'
    resultFolderCreator1.folderName = calFolderName
    calFolderPath = resultFolderCreator1.run()
    calFilePath = os.path.join(calFolderPath, calFileName)
    return calFilePath

#-------------------------------------------------------------------------------

def createRawDataResult():
    rawDataFolderName = f"rawData_{calOptions.serialNumber}"
    rawDataFileName = rawDataFolderName + '.csv'
    resultFolderCreator1.resultType = 'CsvData'
    resultFolderCreator1.folderName = rawDataFolderName
    rawDataFolderPath = resultFolderCreator1.run()
    rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
    return rawDataFilePath

#-------------------------------------------------------------------------------

def findVertScaleAndOffset(ch):
    txChannelList1.commonModeVoltages = [calOptions.commonModeValues[0]]
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

#-------------------------------------------------------------------------------

def increaseLimits():
    iesp.setLimitMaximum("txCommonModeVoltage", 2500)
    iesp.setLimitMinimum("txCommonModeVoltage", 0)
    iesp.setLimitMaximum("voltageSwing", 1100)
    iesp.setLimitMinimum("voltageSwing", 0)
    
    # Common Mode Limits:   [100, 750]
    # Amplitude Limits:        [20, 1000]

#-------------------------------------------------------------------------------

def initModule():
    globalClockConfig1.dataRate = calOptions.dataRate
    globalClockConfig1.setup()
    
    txChannelList1.channels = actualChannels
    
    if calOptions.pattern == 'idle':
        txChannelList1.patterns = ['PAT_DIV40']
    else:
        txChannelList1.patterns = [calOptions.pattern]
    
    txChannelList1.setup()
    
    if calOptions.pattern == 'idle':
        txChannelList1.stopPatterns()

#-------------------------------------------------------------------------------

def initScope():
    import pyvisa
    
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

#-------------------------------------------------------------------------------

def measure(cm, vScale, offset):
    numChannels = len(calOptions.scopeChannels)
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

#-------------------------------------------------------------------------------

def performMeasurements():
    numChanPerGroup = 4
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

#-------------------------------------------------------------------------------

def plotCalResults():
    from dftm.matplotlibConfig import matplotlib
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

#-------------------------------------------------------------------------------

def processRawData():
    arrayShape = (numCh, numWires, numCmVals)
    
    # Compute common mode polynomials
    for channelStr in calOptions.channels:
        chIdx = int(channelStr[:-1]) - 1
        wireIdx = 0 if 'P' in channelStr else 1
        poly = np.polyfit(rawData[chIdx, wireIdx, :], calOptions.commonModeValues, 4)
        commonModeCoeffs[chIdx, wireIdx, :] = poly

#-------------------------------------------------------------------------------

def writeCalFile():
    import datetime
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

#-------------------------------------------------------------------------------

def writeRawData():
    import time
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

#-------------------------------------------------------------------------------

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
#-------------------------------------------------------------------------------

def testProcedure():
    global actualChannels, arrayShape, calFilePath, commonModeCoeffs, iesp, numCh, numCmVals, numCoeffs, numWires, rawData, rawDataFilePath, scope
    svtContext.createRunResultFolder() # create a dated sub-folder for results
    svtContext.initForRun() # re-init components for this run
    namesDict = svtContext.getNamesDict()
    namesDict.update(globalsDict)
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
    svtContext.runEnding()
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    testProcedure()
#-------------------------------------------------------------------------------
