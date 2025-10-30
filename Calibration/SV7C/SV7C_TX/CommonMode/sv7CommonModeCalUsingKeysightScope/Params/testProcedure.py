# SVT Test
# SVT version 23.3.b7
# Test saved 2023-05-12_1159
# Form factor: SV7C_16C17G
# PY3
# Checksum: 6ce3f995fe117fe5cbfe432066539cee
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')

div1200 = _create('div1200', 'SvtUserPattern')
globalClockConfig1 = _create('globalClockConfig1', 'SvtGlobalClockConfig')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
scope1 = _create('scope1', 'SvtKeysightInfiniiumScope')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
vAmpMeasurement = _create('vAmpMeasurement', 'SvtScopeMeasurement')
vCmMeasurement = _create('vCmMeasurement', 'SvtScopeMeasurement')

calOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='any', defaultVal=600.0, displayOrder=(0, 3.0))
calOptions.addField('calChannels', descrip='''List of channels to calibrate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 4.0))
calOptions.addField('commonModeValues', descrip='''Common-mode voltages to be calibrated''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0], displayOrder=(0, 5.0))
calOptions.addField('amplitudeValues', descrip='''Differential voltages to be calibrated''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[1100.0, 750.0, 500.0, 250.0, 100.0], displayOrder=(0, 6.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '1234'
calOptions.scopeIPAddress = 'TCPIP0::10.20.20.200::inst0::INSTR'
calOptions.calDataRate = 17500.0
calOptions.calChannels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
calOptions.commonModeValues = [0.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0]
calOptions.amplitudeValues = [1100.0, 750.0, 500.0, 250.0, 100.0]
calOptions.callCustomInitMethod()
initScope.args = ''
initScope.code = r'''import pyvisa as visa
#connect to scope
import win32com.client
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)

# Set timebase to proper value
#scope1.setTimeScale(5e-8)
osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 5e-8'", 1)


# Make sure all skew are at 0. This is not reset by default

osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.Deskew = 0'", 1)

osci.WriteString("VBS 'app.Acquisition.C1.View = 1'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = 1'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = 1'", 1)


osci.WriteString("VBS 'app.Acquisition.C1.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Coupling = 0'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("*OPC?", 1)

time.sleep(10)

return osci
#scope1.sendCommand(":CALibrate:SKEW CHANnel1,0")
#scope1.sendCommand(":CALibrate:SKEW CHANnel2,0")
#scope1.sendCommand(":CALibrate:SKEW CHANnel3,0")
#scope1.sendCommand(":CALibrate:SKEW CHANnel4,0")
'''
initScope.wantAllVarsGlobal = False

writeCalFile.args = 'commonModeDict, amplitudeDict, cmCoefList, ampCoefList'
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "calCoefficients_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "calCoefficients_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    print("BEGIN SECTION", file=outFile)
    print("section type : header", file=outFile)
    print("serial number : "+calOptions.serialNumber, file=outFile)
    print("hardware revision : B", file=outFile)
    print("date of manufacture(YYYYMMDD) : "+date, file=outFile)
    print("date of calibration(YYYYMMDD) : "+date, file=outFile)
    print("speed grade : 3", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)

    print("BEGIN SECTION", file=outFile)
    print("section type : tx_common_mode_calibration_data", file=outFile)
    print("num lanes : %d" % len(calOptions.calChannels), file=outFile)
    print("#common mode x^4, x^3, x^2, x^1, x^0 coefficients.", file=outFile)
    for coef in cmCoefList:
        for ch in range(1,17,1):
            outFile.write("%.16f, " % commonModeDict[coef]['P'][ch])
        outFile.write("\n")
        for ch in range(1,17,1):
            outFile.write("%.16f, " % commonModeDict[coef]['N'][ch])
        outFile.write("\n")
    print("END SECTION", file=outFile)
    print("", file=outFile)

    print("BEGIN SECTION", file=outFile)
    print("section type : tx_amplitude_calibration_data", file=outFile)
    print("num lanes : %d" % len(calOptions.calChannels), file=outFile)
    print("#amplitude slope and offset.", file=outFile)
    for coef in ampCoefList:
        for ch in range(1,17,1):
            outFile.write("%.16f, " % amplitudeDict[coef][ch])
        outFile.write("\n")
    print("END SECTION", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False

writeRawData.args = 'commonData, ampData'
writeRawData.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

resultFolderCreator1.folderName = calOptions.serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".csv"
filePathString = calOptions.serialNumber + "_TxVoltageCalData" + stringAppendix
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:
    print("ResultDescrip, TX Voltage Calibration Data", file=outFile)
    print("SerialNumber, %s" % calOptions.serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print("", file=outFile)
    print("DATA", file=outFile)
    print("COND_CHANNEL, COND_VSWING_MV, COND_VCM_MV, MEAS_CHP_VAMP_MV, MEAS_CHN_VAMP_MV, MEAS_CHP_VCM_MV, MEAS_CHN_VCM_MV", file=outFile)
    for ch in calOptions.calChannels:
        for cm in calOptions.commonModeValues :
            for amp in calOptions.amplitudeValues:
                vAmpChP = ampData[ch][cm][amp].get('P', np.nan)
                vAmpChN = ampData[ch][cm][amp].get('N', np.nan)
                vCmChP = commonData[ch][cm][amp].get('P', np.nan)
                vCmChN = commonData[ch][cm][amp].get('N', np.nan)
                print("%d, %f, %f, %f, %f, %f, %f" % (ch, amp, cm, vAmpChP, vAmpChN, vCmChP, vCmChN), file=outFile)
'''
writeRawData.wantAllVarsGlobal = False


div1200.bits = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
div1200.notes = ''

globalClockConfig1.clockRecoveryChannel = 8
globalClockConfig1.dataRate = 12500.0
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
txChannelList1.commonModeVoltages = [600.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [PAT_DIV40]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [1000.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']

vAmpMeasurement.edgeDirsA = ['either']
vAmpMeasurement.edgeDirsB = ['either']
vAmpMeasurement.edgeIndicesA = ['1']
vAmpMeasurement.edgeIndicesB = ['1']
vAmpMeasurement.measType = 'vAmplitude'
vAmpMeasurement.minCount = 50
vAmpMeasurement.saveResults = True
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
vCmMeasurement.saveResults = True
vCmMeasurement.scope = scope1
vCmMeasurement.sources = ['CHAN1', 'CHAN2', 'CHAN3', 'CHAN4']
vCmMeasurement.sourcesA = ['CHAN1']
vCmMeasurement.sourcesB = ['CHAN2']


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')

initScope._showInList = False
writeCalFile._showInList = False
writeRawData._showInList = False

resultFolderCreator1._showInList = False
#! TEST PROCEDURE
import numpy as np

# Connect to scope
initScope()
iesp = getIespInstance()
iesp.setLimitMaximum("txCommonModeVoltage", 2500)
iesp.setLimitMinimum("txCommonModeVoltage", 0)
iesp.setLimitMaximum("voltageSwing", 1100)
iesp.setLimitMinimum("voltageSwing", 0)
formFactor = iesp.__class__.__name__

if formFactor == 'SV7C_16C28G':
    calOptions.calDataRate=17500
    txChannelList1.patterns = [div1200]
else:
    txChannelList1.patterns = [PAT_DIV40]
    calOptions.calDataRate=600

# Initialize TX Channel List
txChannelList1.channels = calOptions.calChannels
globalClockConfig1.dataRate = calOptions.calDataRate
globalClockConfig1.setup()

# Define results dictionary
vCmResultsByCh = dict()
vAmpResultsByCh = dict()

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

numChannel = len(calOptions.calChannels)
chStart = calOptions.calChannels[0]
chEnd = calOptions.calChannels[numChannel-1]

channelOrder = list()
"""
for i in range(numChannel)[::4]:
    channelOrder.append((i+1, i+2))
for i in range(numChannel)[2::4]:
    channelOrder.append((i+1, i+2))
"""
for i in range(chStart, chEnd+1, 4):
    if (i < chEnd):
        channelOrder.append((i, i+1))
for i in range(chStart, chEnd+1, 4):
    if ((i+2) < chEnd):
        channelOrder.append((i+2, i+3))
print(channelOrder)


cmCoefList = ['x4', 'x3', 'x2', 'x1', 'of']
ampCoefList = ['x1', 'of']

amplitudeDict = dict()
for coef in ampCoefList:
    amplitudeDict[coef] = dict()
for channel in range(1,17,1):
    amplitudeDict['x1'][channel] = 1.0
    amplitudeDict['of'][channel] = 0

commonModeDict = dict()
for coef in cmCoefList:
    commonModeDict[coef] = dict()
    commonModeDict[coef]['P'] = dict()
    commonModeDict[coef]['N'] = dict()
for wire in ['P', 'N']:
    for channel in range(1,17,1):
        commonModeDict['x4'][wire][channel] = 0
        commonModeDict['x3'][wire][channel] = 0
        commonModeDict['x2'][wire][channel] = 0
        commonModeDict['x1'][wire][channel] = 1.0
        commonModeDict['of'][wire][channel] = 0

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

    for progVCm in calOptions.commonModeValues :
        print("Measuring at %f mV common-mode..." % progVCm)
        vCmResultsByCh[chA][progVCm] = dict()
        vCmResultsByCh[chB][progVCm] = dict()
        vAmpResultsByCh[chA][progVCm] = dict()
        vAmpResultsByCh[chB][progVCm] = dict()

        for progVAmp in calOptions.amplitudeValues :
            print("Measuring at %f mV amplitude..." % progVAmp)

            # Update the generator
            txChannelList1.commonModeVoltages = [progVCm]
            txChannelList1.voltageSwings = [progVAmp]
            txChannelList1.update()

            vCmResults = vCmMeasurement.run()
            scope1._resetAllMeasurements()
            vAmpResults = vAmpMeasurement.run()
            scope1._resetAllMeasurements()

            vCmResultsByCh[chA][progVCm][progVAmp] = dict()
            vCmResultsByCh[chB][progVCm][progVAmp] = dict()
            if vCmResults is not None:
                if 'CHAN1' in vCmResults:
                    vCmResultsByCh[chA][progVCm][progVAmp]['P'] = vCmResults['CHAN1']['mean'] * 1000
                if 'CHAN2' in vCmResults:
                    vCmResultsByCh[chA][progVCm][progVAmp]['N'] = vCmResults['CHAN2']['mean'] * 1000
                if 'CHAN3' in vCmResults:
                    vCmResultsByCh[chB][progVCm][progVAmp]['P'] = vCmResults['CHAN3']['mean'] * 1000
                if 'CHAN4' in vCmResults:
                    vCmResultsByCh[chB][progVCm][progVAmp]['N'] = vCmResults['CHAN4']['mean'] * 1000

            vAmpResultsByCh[chA][progVCm][progVAmp] = dict()
            vAmpResultsByCh[chB][progVCm][progVAmp] = dict()
            if vAmpResults is not None:
                if 'CHAN1' in vAmpResults:
                    vAmpResultsByCh[chA][progVCm][progVAmp]['P'] = vAmpResults['CHAN1']['mean'] * 1000
                if 'CHAN2' in vAmpResults:
                    vAmpResultsByCh[chA][progVCm][progVAmp]['N'] = vAmpResults['CHAN2']['mean'] * 1000
                if 'CHAN3' in vAmpResults:
                    vAmpResultsByCh[chB][progVCm][progVAmp]['P'] = vAmpResults['CHAN3']['mean'] * 1000
                if 'CHAN4' in vAmpResults:
                    vAmpResultsByCh[chB][progVCm][progVAmp]['N'] = vAmpResults['CHAN4']['mean'] * 1000

# Dump the raw measurement values into a csv file
writeRawData(vCmResultsByCh, vAmpResultsByCh)

# Compute averages on a per-wire basis. Note the change in dictionary definition
avgVCmResultsByCh = dict()
numVAmps = len(calOptions.amplitudeValues)
for ch in calOptions.calChannels:
    avgVCmResultsByCh[ch] = dict()
    avgVCmResultsByCh[ch]['P'] = list()
    avgVCmResultsByCh[ch]['N'] = list()
    for vCm in calOptions.commonModeValues:
        vCmResultForChP = [vCmResultsByCh[ch][vCm][vAmp]['P'] for vAmp in calOptions.amplitudeValues if 'P' in vCmResultsByCh[ch][vCm][vAmp]]
        vCmResultForChN = [vCmResultsByCh[ch][vCm][vAmp]['N'] for vAmp in calOptions.amplitudeValues if 'N' in vCmResultsByCh[ch][vCm][vAmp]]
        avgVCmResultsByCh[ch]['P'].append(np.mean(vCmResultForChP) * 2.2) # X2.2 for (50ohm+60ohm)/50ohm to GND
        avgVCmResultsByCh[ch]['N'].append(np.mean(vCmResultForChN) * 2.2) # X2.2 for (50ohm+60ohm)/50ohm to GND

avgVAmpResultsByCh = dict()
numVCms = len(calOptions.commonModeValues)
for ch in calOptions.calChannels:
    avgVAmpResultsByCh[ch] = list()
    for vAmp in calOptions.amplitudeValues:
        # Addition of avg postive and avg negative voltage swings
        vAmpResultForChP = [vAmpResultsByCh[ch][vCm][vAmp]['P'] for vCm in calOptions.commonModeValues if 'P' in vAmpResultsByCh[ch][vCm][vAmp]]
        vAmpResultForChN = [vAmpResultsByCh[ch][vCm][vAmp]['N'] for vCm in calOptions.commonModeValues if 'N' in vAmpResultsByCh[ch][vCm][vAmp]]
        avgVAmp = np.mean(vAmpResultForChP) + np.mean(vAmpResultForChN)
        avgVAmpResultsByCh[ch].append(avgVAmp)

# Compute slope and offset, then store to cal file

for wire in ['P', 'N']:
    for ch in calOptions.calChannels:
        currentCommonModeList = avgVCmResultsByCh[ch][wire]
        polynomialValuesCommonMode = np.polyfit(currentCommonModeList, calOptions.commonModeValues, 4)
        commonModeDict['x4'][wire][ch] = polynomialValuesCommonMode[0]
        commonModeDict['x3'][wire][ch] = polynomialValuesCommonMode[1]
        commonModeDict['x2'][wire][ch] = polynomialValuesCommonMode[2]
        commonModeDict['x1'][wire][ch] = polynomialValuesCommonMode[3]
        commonModeDict['of'][wire][ch] = polynomialValuesCommonMode[4] * 1000 # X1000 to convert to uV

for ch in calOptions.calChannels:
    currentAmplitudeList = avgVAmpResultsByCh[ch]
    polynomialValuesAmplitude = np.polyfit(currentAmplitudeList, calOptions.amplitudeValues, 1)
    amplitudeDict['x1'][ch] = polynomialValuesAmplitude[0]
    amplitudeDict['of'][ch] = polynomialValuesAmplitude[1] * 1000     # X1000 to convert to uV

writeCalFile(commonModeDict, amplitudeDict, cmCoefList, ampCoefList)

iesp.setLimitMaximum("txCommonModeVoltage", 800)
iesp.setLimitMinimum("txCommonModeVoltageMin", 100)
iesp.setLimitMaximum("voltageSwing", 800)
iesp.setLimitMinimum("voltageSwing", 20)
