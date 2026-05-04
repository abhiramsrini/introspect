# SVT Test
# SVT version 23.4.b7
# Test saved 2023-08-18_1020
# Form factor: SV7C_16C17G
# PY3
# Checksum: 161ecce6bfd58ec870367786edce4546
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName='None')

div512 = _create('div512', 'SvtUserPattern')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
import time 

# Autoscale the channels
osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("VBS? 'return=app.WaitUntiIdle(5)'", 1)
osci.WriteString("*OPC?", 1)
# Clear display
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(100)

#Set timebase to proper value

osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 5e-9'", 1)
osci.writestring("VBS 'app.Acquisition.Trigger.C1Slope = 0'", 1)

time.sleep(10)
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calChannels', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0], displayOrder=(0, 7.0))
calOptions.addField('max_std_ps', descrip='''Minimum standard deviation required for the scope to measure the delay.''', attrType=float, iespInstanceName='any', defaultVal=0.5, displayOrder=(0, 8.0))
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
calOptions.scopeMeasurementDelay = 2000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calChannels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
calOptions.calRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0]
calOptions.max_std_ps = 1.0
calOptions.callCustomInitMethod()
dataFile1.delimiter = ','
dataFile1.fileName = ''
dataFile1.numFields = 1
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'

initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa as visa
#connect to scope
import win32com.client #imports the pywin32 library
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)

# Set to center by going to default
osci.WriteString("VBS 'app.SetToDefaultSetup'", 1)
osci.WriteString("*OPC?", 1)
sleepMillis(calOptions.scopeAutoScaleDelay)

# Display/Enable the channels

osci.WriteString("VBS 'app.Acquisition.C1.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.View = true'", 1)


# Make sure all skew are at 0. This is not reset by default
osci.WriteString("VBS 'app.Acquisition.C1.DeSkew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.DeSkew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.DeSkew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.DeSkew = 0'", 1)

# Setting the channels 50 Ohm Coupling
osci.WriteString("VBS 'app.Acquisition.C1.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.Coupling = 0'", 1)

# Configuring the Measurement Parameter
osci.WriteString("VBS 'app.Measure.P1.MeasurementType = 0'", 1)
osci.WriteString("VBS 'app.Measure.ShowMeasure = true",1)
osci.WriteString("VBS 'app.Measure.StatsOn = true",1)
osci.WriteString("VBS 'app.Measure.P1.View = true",1)
osci.WriteString("VBS 'app.Measure.P2.View = False",1)

# Define delta-time measurement parameters
osci.WriteString("VBS 'app.Measure.P1.ParamEngine = \"DeltaTimeAtLevel\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel1 = 50'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope2 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel2 = 50'", 1)

# Turn averaging on
osci.writestring("VBS 'app.Acquisition.C1.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C2.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C3.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C4.AverageSweeps = 1'", 1)

# Autoscale the channels
osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("*OPC?", 1)

return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
channelSource = "C%d" % channel

# Update P1 sources for this channel pair
osci.WriteString("VBS 'app.Measure.P1.Source1 = \"C1\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Source2 = \"%s\"'" % channelSource, 1)

# Clear previous statistics before accumulating fresh ones
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(calOptions.scopeAutoScaleDelay)

max_meas_iterations = 15
currentDeltaTime = 0
DeltaTime_std = 0

for i in range(max_meas_iterations):
    sweeps = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Sweeps'", 1))
    std    = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Sdev'", 1))

    if sweeps > calOptions.numAverages and std * 1e12 < calOptions.max_std_ps:
        currentDeltaTime = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Mean'", 1))
        DeltaTime_std = std
        break
    elif sweeps > calOptions.numAverages and std * 1e12 > calOptions.max_std_ps:
        osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
    else:
        sleepMillis(500)

assert currentDeltaTime != 0, 'Unable to measure delay with std less than max_std_ps after the maximum number of iterations.'

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False

performScopeCal.args = 'channel,position,  dataRate'
performScopeCal.code = r'''if channel == 1:
    print("Performing coarse loop...")
    coarse = 0
    coarseDelay = coarse
    print("delay is %d..." % coarseDelay)
    print(" ")

else: # channels 2-16
    print("Performing coarse loop...")
    coarseDelay = measureDeltaTime(position)
    print("delay is %g..." % coarseDelay)


return coarseDelay
'''
performScopeCal.wantAllVarsGlobal = False

writeCalFile.args = 'polyCoefficients'
writeCalFile.code = r'''import datetime
import os

dataFile1.fileName = "calCoefficients_"+calOptions.serialNumber+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.serialNumber+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : tx_alignment_calibration_data\n")

    for c in range(4):
        for channel in range(1,17,1) :
            calFile.write("%0.15f," % polyCoefficients[channel][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficients_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFile.wantAllVarsGlobal = False

writeCalFileTemp.args = 'measuredCoarseDelayDict'
writeCalFileTemp.code = r'''import datetime
import os

dataFile1.fileName = "calCoefficientsTemp_"+calOptions.serialNumber+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.serialNumber+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : tx_alignment_calibration_data\n")

    for c in range(4):
        for channel in range(1,17,1) :
            calFile.write("%0.15f," % polyCoefficients[channel][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficientsTemp_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFileTemp.wantAllVarsGlobal = False


div512.bits = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
div512.notes = ''

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 8000.0
globalClockConfig.refClockSyncMode = 'clockRecovery'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

resultFolderCreator1.channelProvider = None
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [400.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [div512]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')
#! TEST PROCEDURE
iesp = getIespInstance()
calOptions.calChannels = sorted(calOptions.calChannels)

# Connect to scope
osci = initScope(calOptions.scopeIPAddress)
iesp.setMeasurementTimeout(60000)
groups = []
for (i,channel) in enumerate(calOptions.calChannels):
    if i==0:
        referenceChannel = channel
    elif(i in [1,4,7,10,13]):
        group = [channel]
    else:
        group.append(channel)

    if (channel==calOptions.calChannels[-1] or i in [3,6,9,12,15]):
       groups.append(group)

#define results dictionary
measureCoarseDelayDict = dict()
for channel in range(1,17,1):
    measureCoarseDelayDict[channel] = dict()
    for dataRate in calOptions.calRates :
        measureCoarseDelayDict[channel][dataRate] = int()
        measureCoarseDelayDict[channel][dataRate] = 0

polyCoefficients = dict()
for channel in range(1,17,1) :
    polyCoefficients[channel] = dict()
    for c in range(4):
        polyCoefficients[channel][c] = 0

for (i, group) in enumerate(groups) :

    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring channel %d, %d, %d" % (group[0], group[1],group[2]))
    myString = "Please connect channel %d, %d, %d, %d Positive to Input 1,2,3,4 of the oscilloscope." % (referenceChannel,group[0],group[1],group[2])
    waitForGuiOkDialog(myString)



    #initialize generator
    txChannelList1.channels = calOptions.calChannels
    txChannelList1.setup()


    if(i == 0):
        autoscaleScope()

    for dataRate in calOptions.calRates :
        halfUi = 1000000 / dataRate / 2 * 1e-12
        halfUi = halfUi + 5e-12
       # print "HalfUi: %e" % halfUi
        print("Measuring at %f Mbps..." % dataRate)

        #do clock commit
        globalClockConfig.dataRate = dataRate
        globalClockConfig.setup()
        #initialize generator after clock commit
        txChannelList1.setup()

        #use scope to measure values
        coarseDelay0 = performScopeCal(group[0],2,dataRate)
        measureCoarseDelayDict[group[0]][dataRate] = coarseDelay0 * 1e12
        coarseDelay1 = performScopeCal(group[1],3,dataRate)
        measureCoarseDelayDict[group[1]][dataRate] = coarseDelay1 * 1e12
        coarseDelay2 = performScopeCal(group[2],4,dataRate)
        measureCoarseDelayDict[group[2]][dataRate] = coarseDelay2 * 1e12


    for channel in group :
        xVals = list()
        yVals = list()
        for dataRate in sorted(calOptions.calRates) :
            xVals.append(dataRate)
            yVals.append(measureCoarseDelayDict[channel][dataRate])
        polyCoefficients[channel] = np.polyfit(xVals,yVals,3)
        print(polyCoefficients[channel])
    writeCalFileTemp(polyCoefficients)

writeCalFile(polyCoefficients)
