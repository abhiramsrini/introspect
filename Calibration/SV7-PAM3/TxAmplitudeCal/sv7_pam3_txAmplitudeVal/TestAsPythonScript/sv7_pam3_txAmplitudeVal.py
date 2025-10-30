
# Generated via TestAsPythonScript from Test 'sv7_pam3_txAmplitudeVal'
# 2024-08-05_1439


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
svtContextFolderName = 'sv7_pam3_txAmplitudeValFolder'
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
globalClockConfig = svtContext.createComponent('SvtGlobalClockConfig', suggestedName='globalClockConfig')
pam3Protocol = svtContext.createComponent('SvtPam3Protocol', suggestedName='pam3Protocol')
resultFolderCreator1 = svtContext.createComponent('SvtResultFolderCreator', suggestedName='resultFolderCreator1')
txChannelList1 = svtContext.createComponent('SvtTxChannelList', suggestedName='txChannelList1')
userPattern1 = svtContext.createComponent('SvtUserPattern', suggestedName='userPattern1')
valOptions = svtContext.createComponent('SvtDataRecord', suggestedName='valOptions')




txChannelList1.commonModeVoltages = [600.0]

userPattern1.bits = '0000000000000000000000000000000011111111111111111111111111111111'



#-------------------------------------------------------------------------------

def beepOkDialog(msg):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    waitForOkDialog(msg)

#-------------------------------------------------------------------------------

def createRawDataResult():
    import os
    rawDataFolderName = f"rawData_{valOptions.serialNumber}"
    rawDataFileName = rawDataFolderName + '.json'
    resultFolderCreator1.resultType = 'Generic'
    resultFolderCreator1.folderName = rawDataFolderName
    rawDataFolderPath = resultFolderCreator1.run()
    rawDataFilePath = os.path.join(rawDataFolderPath, rawDataFileName)
    return rawDataFilePath

#-------------------------------------------------------------------------------

def getBestVertScalesAndOffsets(ch):
    txChannelList1.voltageSwings = [valOptions.amplitudeValues[0]]
    txChannelList1.update()
    
    scope.write(f":AUToscale:VERTical CHANnel{valOptions.scopeChannels[0]}")
    
    sleepMillis(1000)
    while not '1' in scope.query('*OPC?'):
        sleepMillis(1000)
    
    resultStr = scope.query(f":CHANnel{valOptions.scopeChannels[0]}:SCAle?")
    vScale1 = float(resultStr)
    resultStr = scope.query(f":CHANnel{valOptions.scopeChannels[0]}:OFFSet?")
    offset1 = float(resultStr)
    
    txChannelList1.voltageSwings = [valOptions.amplitudeValues[-1]]
    txChannelList1.update()
    
    scope.write(f":AUToscale:VERTical CHANnel{valOptions.scopeChannels[0]}")
    
    sleepMillis(1000)
    while not '1' in scope.query('*OPC?'):
        sleepMillis(1000)
    
    resultStr = scope.query(f":CHANnel{valOptions.scopeChannels[0]}:SCAle?")
    vScale2 = float(resultStr)
    resultStr = scope.query(f":CHANnel{valOptions.scopeChannels[0]}:OFFSet?")
    offset2 = float(resultStr)
    
    numPoints = len(valOptions.amplitudeValues)
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
    globalClockConfig.dataRate = valOptions.dataRate
    globalClockConfig.setup()
    
    txChannelList1.channels = [1,2,3,4,5,6,7,8,9,10,11,12]
    txChannelList1.patterns = [userPattern1]
    txChannelList1.commonModeVoltages = [valOptions.commonModeVoltage]
    txChannelList1.setup()

#-------------------------------------------------------------------------------

def initScope():
    import pyvisa
    
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
    
    return scope

#-------------------------------------------------------------------------------

def measure(amp, vScale):
    numChannels = len(valOptions.scopeChannels)
    amplitudeResults = [0] * numChannels
    
    if vScale is not None:
        for ch in valOptions.scopeChannels:
            scope.write(f":CHANnel{ch}:SCALe {vScale}")
    
    for ch in valOptions.scopeChannels:
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
    while count < valOptions.numMeasurements:
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
    channels = valOptions.channels.copy()
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
    
        msg = f'Measuring channels {chA}, {chB}, {chC}, {chD}. '
        msg += (f'Please connect these channels to the scope: CH_{chA}->SCOPE_CH1, '
                f'CH_{chB}->SCOPE_2, CH_{chC}->SCOPE_3, CH_{chD}->SCOPE_4')
        beepOkDialog(msg)
    
        for ampIdx, amp in enumerate(valOptions.amplitudeValues):
            vScale = vScales[ampIdx]
            print(f'Measuring at {amp:.2f} mV amplitude...')
    
            txChannelList1.voltageSwings = [amp]
            txChannelList1.update()
    
            amplitudeResults = measure(amp, vScale)
            while not isMeasureSuccess():
                for ch in valOptions.scopeChannels:
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
                measuredValue = amplitudeResults[scopeChanIdx]
                rawData[chIdx][ampIdx] = validateMeasurement(measuredValue, amp, channel)

#-------------------------------------------------------------------------------

def validateMeasurement(measuredValue, expectedValue, channel):
    from pprint import pformat
    
    absoluteError = abs(measuredValue - expectedValue)
    percentError = (absoluteError / expectedValue) * 100 if expectedValue != 0 else 0
    
    result = {'channel': f'{channel}',
              'expectedValue': expectedValue,
              'measuredValue': measuredValue,
              'absoluteError': absoluteError,
              'percentError': percentError,
              'fail': False}
    
    if absoluteError > valOptions.absoluteErrorThresh:
        result['fail'] = True
        warningMsg(f'Failed on channel {channel}')
        msg = pformat(result)
        warningMsg(msg)
    
    return result

#-------------------------------------------------------------------------------

def writeRawData():
    import time
    import os
    import json
    ## dd/mm/yyyy format
    dateToday = time.strftime("%d/%m/%Y")
    timeNow = time.strftime("%H:%M:%S")
    
    jsonDict = {}
    jsonDict['description'] = 'TX Amplitude Validation Data'
    jsonDict['serialNumber'] = f'{valOptions.serialNumber}'
    jsonDict['date'] = f'{dateToday}'
    jsonDict['time'] = f'{timeNow}'
    jsonDict['rawData'] = rawData
    
    with open(rawDataFilePath, 'w') as f:
        json.dump(jsonDict, f, indent=4)

#-------------------------------------------------------------------------------

valOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
valOptions.addField('scopeIpAddress', descrip='''Keysight scope's IP address''', attrType=str, iespInstanceName='any', defaultVal='TCPIP::10.30.30.215::INSTR', displayOrder=(0, 2.0))
valOptions.addField('scopeChannels', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
valOptions.addField('scopeTimeScale', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=2e-09, displayOrder=(0, 4.0))
valOptions.addField('channels', descrip='''Channels to validate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], displayOrder=(0, 5.0))
valOptions.addField('absoluteErrorThresh', descrip='''Allowable absolute value of error to pass validation''', attrType=float, iespInstanceName='any', defaultVal=35.0, displayOrder=(0, 6.0))
valOptions.addField('dataRate', descrip='''Data rate to validate with''', attrType=float, iespInstanceName='any', defaultVal=16000.0, displayOrder=(0, 7.0))
valOptions.addField('commonModeVoltage', descrip='''Common mode voltage to use during validation''', attrType=str, iespInstanceName='any', defaultVal='100.0', displayOrder=(0, 8.0))
valOptions.addField('amplitudeValues', descrip='''Values to test''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[50.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0], displayOrder=(0, 9.0))
valOptions.addField('numMeasurements', descrip='''''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 10.0))
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
valOptions.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
valOptions.absoluteErrorThresh = 35.0
valOptions.dataRate = 16000.0
valOptions.commonModeVoltage = '100.0'
valOptions.amplitudeValues = [50.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
valOptions.numMeasurements = 100
valOptions.callCustomInitMethod()
#-------------------------------------------------------------------------------

def testProcedure():
    global absoluteErrors, failures, iesp, numAmpVals, numCh, numFailures, rawData, rawDataFilePath, scope
    svtContext.createRunResultFolder() # create a dated sub-folder for results
    svtContext.initForRun() # re-init components for this run
    namesDict = svtContext.getNamesDict()
    namesDict.update(globalsDict)
    from dftm.errMsg import setFileLogLevel
    setFileLogLevel('txChannelList', 31, printInfo=False) # Suppress logging
    
    iesp = getIespInstance()
    
    beepOkDialog(f'Please connect the first 4 channels to the scope ({valOptions.channels[:4]})')
    
    
    # ----- Initialization -----
    increaseLimits()
    initModule()
    scope = initScope()
    beepOkDialog('Please ensure a cal file with tx '
                 'calibration data has been loaded '
                 'on the module.')
    
    rawDataFilePath = createRawDataResult()
    
    numCh = 12
    numAmpVals = len(valOptions.amplitudeValues)
    
    rawData = [[{} for y in range(numAmpVals)] for x in range(numCh)]
    
    
    # ----- Validation -----
    performMeasurements()
    writeRawData()
    
    
    # ----- Pass/Fail -----
    failures = [True for x in rawData for y in x if y.get('fail', False)]
    numFailures = len(failures)
    print(f'Number of failures: {numFailures}')
    absoluteErrors = [y.get('absoluteError', 0) for x in rawData for y in x]
    print(f'Max error: {max(absoluteErrors)}')
    if numFailures > 0:
        writeNoteForTestRun("Fail")
    else:
        writeNoteForTestRun("Pass")
    svtContext.runEnding()
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    testProcedure()
#-------------------------------------------------------------------------------
