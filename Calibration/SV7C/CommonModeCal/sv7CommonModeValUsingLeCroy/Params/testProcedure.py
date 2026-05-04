# SVT Test
# SVT version 23.3.b11
# Test saved 2023-06-08_1229
# Form factor: SV7C_16C17G
# PY3
# Checksum: 3fdc5356fbd9996fb1f45fe3824abd69
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


initScope = _create('initScope', 'SvtFunction', iespName='None')
valOptions = _create('valOptions', 'SvtDataRecord', iespName='None')
validateTxAmp = _create('validateTxAmp', 'SvtFunction', iespName='None')
validateTxCommMode = _create('validateTxCommMode', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

div1200 = _create('div1200', 'SvtUserPattern')
globalClockConfig1 = _create('globalClockConfig1', 'SvtGlobalClockConfig')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
scope1 = _create('scope1', 'SvtKeysightInfiniiumScope')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
vAmpMeasurement = _create('vAmpMeasurement', 'SvtScopeMeasurement')
vCmMeasurement = _create('vCmMeasurement', 'SvtScopeMeasurement')

initScope.args = ''
initScope.code = r'''scope1.address = valOptions.scopeIPAddress
scope1.connect()
scope1.reset()
# Set timebase to proper value
scope1.setTimeScale(5e-8)

# Make sure all skew are at 0. This is not reset by default
scope1.sendCommand(":CALibrate:SKEW CHANnel1,0")
scope1.sendCommand(":CALibrate:SKEW CHANnel2,0")
scope1.sendCommand(":CALibrate:SKEW CHANnel3,0")
scope1.sendCommand(":CALibrate:SKEW CHANnel4,0")
'''
initScope.wantAllVarsGlobal = False

valOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='SV5C_16C12G', defaultVal='1234', displayOrder=(0, 1.0))
valOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='SV5C_16C12G', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
valOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='SV5C_16C12G', defaultVal=600.0, displayOrder=(0, 3.0))
valOptions.addField('calChannels', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='SV5C_16C12G', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 4.0))
valOptions.addField('commonModeValues', descrip='''Range of common-mode voltages to be verified''', attrType=list, iespInstanceName='SV5C_16C12G', attrSubType=float, defaultVal=[250.0, 390.0, 530.0], displayOrder=(0, 5.0))
valOptions.addField('amplitudeValues', descrip='''Range of differential voltages to be verified''', attrType=list, iespInstanceName='SV5C_16C12G', attrSubType=float, defaultVal=[625.0, 270.0, 40.0], displayOrder=(0, 6.0))
valOptions.addField('connectedToTerminationBoard', descrip='''Set to true if the measurement is performed using a termination board with high-impedance probes. If the measurement is done directly on the oscilloscope 50 Ohm inputs, set to False. If set to False, a compensation value for common mode measurements is applied''', attrType=bool, iespInstanceName='SV5C_16C12G', defaultVal=False, displayOrder=(0, 7.0))
valOptions.addField('absoluteErrorThreshold', descrip='''Pass/fail threshold for the absolute value of voltage error''', attrType=float, iespInstanceName='SV5C_16C12G', defaultVal=20.0, displayOrder=(0, 8.0))
valOptions.addField('percentErrorThreshold', descrip='''Pass/fail threshold for the percentage of voltage error''', attrType=float, iespInstanceName='SV5C_16C12G', defaultVal=10.0, displayOrder=(0, 9.0))
valOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
valOptions.serialNumber = 'SV7C23030007'
valOptions.scopeIPAddress = 'TCPIP0::169.254.103.240::inst0::INSTR'
valOptions.calDataRate = 600.0
valOptions.calChannels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
valOptions.commonModeValues = [250.0, 390.0, 530.0]
valOptions.amplitudeValues = [625.0, 270.0, 40.0]
valOptions.connectedToTerminationBoard = False
valOptions.absoluteErrorThreshold = 20.0
valOptions.percentErrorThreshold = 10.0
valOptions.callCustomInitMethod()
validateTxAmp.args = 'measValP, measValN, vAmp, chName'
validateTxAmp.code = r'''measVal = (measValP + measValN)
absError = abs( measVal - vAmp )
if vAmp == 0:
    prctError = 0
else:
    prctError = absError / vAmp * 100
resultDict = {'measValP': measValP,
                'measValN': measValN,
                'error': absError,
                'prctError': prctError,
                'result': True}
if (absError > valOptions.absoluteErrorThreshold) and (prctError > valOptions.percentErrorThreshold):
    warningMsg('Failed TX Amplitude on %s:' % chName)
    warningMsg('measValP: %f, measValN: %f, measVal: %f, expctVal: %f, error: %f, %% error: %0.1f'
                % (measValP, measValN, measVal, vAmp, absError, prctError))
    resultDict['result'] = False

return resultDict
'''
validateTxAmp.wantAllVarsGlobal = False

validateTxCommMode.args = 'measVal, vCm, chName'
validateTxCommMode.code = r'''measVal *= 2.2 # X2.2 for (50ohm+60ohm)/50ohm to GND
absError = abs( measVal - vCm )
if vCm == 0:
    prctError = 0
else:
    prctError = absError / vCm * 100
resultDict = {'measVal': measVal,
                'error': absError,
                'prctError': prctError,
                'result': True}
if (absError > valOptions.absoluteErrorThreshold) and (prctError > valOptions.percentErrorThreshold):
    warningMsg('Failed TX Common Mode on %s:' % chName)
    warningMsg('measVal: %0.1f, expctVal: %0.1f, error: %0.1f, %% error: %0.1f'
                % (measVal, vCm, absError, prctError))
    resultDict['result'] = False

return resultDict
'''
validateTxCommMode.wantAllVarsGlobal = False

writeRawData.args = 'commonData, ampData'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = valOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = valOptions.serialNumber + "_TxVoltageCalData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("TX Voltage Validation Data", file=outFile)
    print("Serial Number, %s" % valOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ,", file=outFile)
    print(("COND_CHANNEL, COND_VSWING_MV, COND_VCM_MV,"
                        + " MEAS_CHP_VAMP_MV, MEAS_CHN_VAMP_MV, MEAS_VAMP_ERROR_MV, MEAS_VAMP_PRCTERROR_MV, MEAS_VAMP_RESULT,"
                        + " MEAS_CHP_VCM_MV, MEAS_CHP_VCM_ERROR_MV, MEAS_CHP_VCM_PRCTERROR_MV, MEAS_CHP_VCM_RESULT,"
                        + " MEAS_CHN_VCM_MV, MEAS_CHN_VCM_ERROR_MV, MEAS_CHN_VCM_PRCTERROR_MV, MEAS_CHN_VCM_RESULT"), file=outFile)
    for ch in valOptions.calChannels:
        for cm in valOptions.commonModeValues:
            for amp in valOptions.amplitudeValues:
                dataLine = ''
                vAmpDict = ampData[ch][cm][amp]
                if vAmpDict:
                    vAmpChP = vAmpDict['measValP']
                    vAmpChN = vAmpDict['measValN']
                    vAmpError = vAmpDict['error']
                    vAmpPrct = vAmpDict['prctError']
                    vAmpResult = vAmpDict['result']
                    dataLine += ('%0.1f, %0.1f, %0.1f, %0.1f, %s, '
                                % (vAmpChP, vAmpChN, vAmpError, vAmpPrct, vAmpResult))
                else:
                    dataLine += 'nan, nan, nan, nan, False, '

                if 'P' in commonData[ch][cm][amp]:
                    vCmDict = commonData[ch][cm][amp]['P']
                    vCmChP = vCmDict['measVal']
                    vCmError = vCmDict['error']
                    vCmPrct = vCmDict['prctError']
                    vCmResult = vCmDict['result']
                    dataLine += ('%0.1f, %0.1f, %0.1f, %s, '
                                % (vCmChP, vCmError, vCmPrct, vCmResult))
                else:
                    dataLine += 'nan, nan, nan, False, '

                if 'N' in commonData[ch][cm][amp]:
                    vCmDict = commonData[ch][cm][amp]['N']
                    vCmChN = vCmDict['measVal']
                    vCmError = vCmDict['error']
                    vCmPrct = vCmDict['prctError']
                    vCmResult = vCmDict['result']
                    dataLine += ('%0.1f, %0.1f, %0.1f, %s, '
                                % (vCmChN, vCmError, vCmPrct, vCmResult))
                else:
                    dataLine += 'nan, nan, nan, False, '

                print("%d, %0.1f, %0.1f, %s" % (ch, amp, cm, dataLine), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False


div1200.bits = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
div1200.notes = ''

globalClockConfig1.clockRecoveryChannel = 8
globalClockConfig1.dataRate = 500.0
globalClockConfig1.refClockSyncMode = 'clockRecovery'
globalClockConfig1.referenceClocks = refClocksConfig
globalClockConfig1.sscEnabled = False
globalClockConfig1.sscFrequency = 50.0
globalClockConfig1.sscSpread = 1.0

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

resultFolderCreator1.channelProvider = None
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

scope1.address = 'TCPIP0::1.2.3.4::inst0::INSTR'
scope1.triggerMode = 'auto'
scope1.triggerSlope = 'rising'
scope1.triggerSource = 'CHAN1'

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [400.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [PAT_DIV40]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']

vAmpMeasurement.edgeDirsA = ['either']
vAmpMeasurement.edgeDirsB = ['either']
vAmpMeasurement.edgeIndicesA = ['1']
vAmpMeasurement.edgeIndicesB = ['1']
vAmpMeasurement.measType = 'vAmplitude'
vAmpMeasurement.minCount = 50
vAmpMeasurement.saveResults = False
vAmpMeasurement.scope = scope1
vAmpMeasurement.sources = ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4']
vAmpMeasurement.sourcesA = ['CHAN1']
vAmpMeasurement.sourcesB = ['CHAN2']

vCmMeasurement.edgeDirsA = ['either']
vCmMeasurement.edgeDirsB = ['either']
vCmMeasurement.edgeIndicesA = ['1']
vCmMeasurement.edgeIndicesB = ['1']
vCmMeasurement.measType = 'vAverage'
vCmMeasurement.minCount = 50
vCmMeasurement.saveResults = False
vCmMeasurement.scope = scope1
vCmMeasurement.sources = ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4']
vCmMeasurement.sourcesA = ['CHAN1']
vCmMeasurement.sourcesB = ['CHAN2']


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')

writeRawData._showInList = False

resultFolderCreator1._showInList = False
#! TEST PROCEDURE
## Check Version
iesp = getIespInstance()
# Connect to scope
initScope()
fail = 0
# Initialize TX Channel List
formFactor = iesp.__class__.__name__
if formFactor == 'SV7C_16C28G':
    valOptions.calDataRate=17500
    txChannelList1.patterns = [div1200]
else:
    txChannelList1.patterns = [PAT_DIV40]
    valOptions.calDataRate=600
txChannelList1.channels = valOptions.calChannels
globalClockConfig1.dataRate = valOptions.calDataRate
globalClockConfig1.setup()

# Define results dictionary
vCmResultsByCh = dict()
vAmpResultsByCh = dict()
numChannel = len(valOptions.calChannels)
chStart = valOptions.calChannels[0]
chEnd = valOptions.calChannels[numChannel-1]
formFactor = iesp.__class__.__name__
channelOrder = list()
for i in range(chStart, chEnd+1, 4):
    if (i < chEnd):
        channelOrder.append((i, i+1))
for i in range(chStart, chEnd+1, 4):
    if ((i+2) < chEnd):
        channelOrder.append((i+2, i+3))
print(channelOrder)

valResult = True
for (chA,chB) in channelOrder:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring channels %d and %d..." % (chA, chB))
    myString = ('Please connect channels %d and %d signals to the oscilloscope. Ch%dP to Ch1, Ch%dN to Ch2, Ch%dP to Ch3, Ch%dN to Ch4'
                % (chA, chB, chA, chA, chB, chB))
    waitForGuiOkDialog(myString)
    vCmResultsByCh[chA] = dict()
    vCmResultsByCh[chB] = dict()
    vAmpResultsByCh[chA] = dict()
    vAmpResultsByCh[chB] = dict()

    for vCm in valOptions.commonModeValues :
        print("Measuring at %f mV common-mode..." % vCm)
        vCmResultsByCh[chA][vCm] = dict()
        vCmResultsByCh[chB][vCm] = dict()
        vAmpResultsByCh[chA][vCm] = dict()
        vAmpResultsByCh[chB][vCm] = dict()

        for vAmp in valOptions.amplitudeValues :
            print("Measuring at %f mV amplitude..." % vAmp)

            # Update the generator
            txChannelList1.commonModeVoltages = [vCm]
            txChannelList1.voltageSwings = [vAmp]
            txChannelList1.update()

            vCmResults = vCmMeasurement.run()
            vAmpResults = vAmpMeasurement.run()
            scope1._resetAllMeasurements()

            vCmResultsByCh[chA][vCm][vAmp] = dict()
            vCmResultsByCh[chB][vCm][vAmp] = dict()
            if vCmResults is not None:
                if 'CHAN1' in vCmResults:
                    valDict = validateTxCommMode(vCmResults['CHAN1']['mean'] * 1000, vCm, 'CH%dP' % chA)
                    vCmResultsByCh[chA][vCm][vAmp]['P'] = valDict
                    if valDict['result'] == False:
                        fail = 1
                if 'CHAN2' in vCmResults:
                    valDict = validateTxCommMode(vCmResults['CHAN2']['mean'] * 1000, vCm, 'CH%dN' % chA)
                    vCmResultsByCh[chA][vCm][vAmp]['N'] = valDict
                    if valDict['result'] == False:
                        fail = 1
                if 'CHAN3' in vCmResults:
                    valDict = validateTxCommMode(vCmResults['CHAN3']['mean'] * 1000, vCm, 'CH%dP' % chB)
                    vCmResultsByCh[chB][vCm][vAmp]['P'] = valDict
                    if valDict['result'] == False:
                        fail = 1
                if 'CHAN4' in vCmResults:
                    valDict = validateTxCommMode(vCmResults['CHAN4']['mean'] * 1000, vCm, 'CH%dN' % chB)
                    vCmResultsByCh[chB][vCm][vAmp]['N'] = valDict
                    if valDict['result'] == False:
                        fail = 1
            vAmpResultsByCh[chA][vCm][vAmp] = None
            vAmpResultsByCh[chB][vCm][vAmp] = None
            if vAmpResults is not None:
                if 'CHAN1' in vAmpResults and 'CHAN2' in vAmpResults:
                    valDict = validateTxAmp(vAmpResults['CHAN1']['mean'] * 1000,
                                            vAmpResults['CHAN2']['mean'] * 1000,
                                            vAmp, 'CH%d' % chA)
                    vAmpResultsByCh[chA][vCm][vAmp] = valDict
                    if valDict['result'] == False:
                        fail = 1
                if 'CHAN3' in vAmpResults and 'CHAN4' in vAmpResults:
                    valDict = validateTxAmp(vAmpResults['CHAN3']['mean'] * 1000,
                                            vAmpResults['CHAN4']['mean'] * 1000,
                                            vAmp, 'CH%d' % chB)
                    vAmpResultsByCh[chB][vCm][vAmp] = valDict
                    if valDict['result'] == False:
                        fail = 1
# Dump the raw measurement values into a csv file
writeRawData(vCmResultsByCh, vAmpResultsByCh)
if fail == 1:
    writeNoteForTestRun("Fail")
else:
    writeNoteForTestRun("Pass")
