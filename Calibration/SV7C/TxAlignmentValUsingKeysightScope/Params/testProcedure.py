# SVT Test
# SVT version 23.4.b7
# Test saved 2023-08-18_1022
# Form factor: SV7C_16C17G
# PY3
# Checksum: 23365fb6996bb6e772b7a494d9e9f18f
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName='None')
calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
initScope = _create('initScope', 'SvtFunction', iespName='None')
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName='None')
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName='None')
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName='None')
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName='None')

div256 = _create('div256', 'SvtUserPattern')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

# Make sure all skew are at 0. This is not reset by default
osci.write(":CALibrate:SKEW CHANnel1,0")
osci.write(":CALibrate:SKEW CHANnel2,0")
osci.write(":CALibrate:SKEW CHANnel3,0")
osci.write(":CALibrate:SKEW CHANnel4,0")

# Display the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")
osci.write(":CHANnel4:DISPlay 1")

# Autoscale the channels
osci.write(":AUToscale:VERTical CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel2")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel3")
sleepMillis(calOptions.scopeAutoScaleDelay)
osci.write(":AUToscale:VERTical CHANnel4")
sleepMillis(calOptions.scopeAutoScaleDelay)
# Clear display
osci.write(":CDISplay")

# Make sure we're getting mean values
osci.write(":MEASure:STATistics MEAN")


# Measure average voltage of channel 1 to set trigger level
osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
sleepMillis(calOptions.scopeAutoScaleDelay)
varAverage = osci.query_ascii_values(":MEASure:VAVerage? DISPlay,CHANnel1")
currentValue = varAverage[0]

triggerValue = currentValue

# Set trigger level to be just below the mid-point of the 3-level waveform
myString = ":TRIGger:LEVel CHANNEL1, %f" % triggerValue
osci.write(myString)

# Clear display
osci.write(":CDISplay")
sleepMillis(100)

# Set timebase to proper value
osci.write(":TIMebase:SCALe 100e-012")

# Turn averaging on
osci.write(":ACQuire:AVERage:COUNt 16")
osci.write(":ACQuire:AVERage 1")

# Define delta-time measurement parameters
osci.write(":MEASure:DELTatime:DEFine RISing,1,MIDDle,RISing,1,MIDDle")
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calChannels', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8850.0, 12850.0, 14250.0, 17250.0], displayOrder=(0, 7.0))
calOptions.addField('max_std_ps', descrip='''Minimum standard deviation required for scope measurement of delay.''', attrType=float, iespInstanceName='any', defaultVal=0.5, displayOrder=(0, 8.0))
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
calOptions.calRates = [8850.0, 12850.0, 14250.0, 17250.0]
calOptions.max_std_ps = 1.0
calOptions.callCustomInitMethod()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa as visa
#connect to scope
rm = visa.ResourceManager()
osci = rm.open_resource(scopeIpAddress)
#print(osci.lock_state)
#osci.lock_excl()
# Set to center by going to default
osci.write(":SYSTem:PRESet DEFault")
sleepMillis(calOptions.scopeAutoScaleDelay)

# Display/Enable the channels
osci.write(":CHANnel1:DISPlay 1")
osci.write(":CHANnel2:DISPlay 1")
osci.write(":CHANnel3:DISPlay 1")
osci.write(":CHANnel4:DISPlay 1")
osci.timeout = 10000

return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1

sleepMillis(calOptions.scopeAutoScaleDelay)

channelString = "CHANNEL%d" % channel
commandString = ":MEASure:DELTatime CHANnel1,"+channelString
osci.write(commandString)
osci.write(":MEASure:SENDvalid ON")
osci.write(":MEASure:STATistics ON")

max_meas_iterations = 15 # Maximum number of queries to the scope.

currentDeltaTime = 0
DeltaTime_std = 0

for i in range(max_meas_iterations):
    stats = osci.query(":MEASure:RESults?") # Get the delay measurement statistics from the scope
    stats = stats.split(',') # Format: measurement label,current,result state, min,max,mean,std dev,# of meas
    #print(stats)
    assert stats[0] == "Time(1-%d)"% channel, "Unexpected measurement config."
    if float(stats[7]) > calOptions.numAverages and float(stats[6])*1e12 < calOptions.max_std_ps: # Makes sure numAverages,max_std_ps parameters in calOptions are satisfied
        currentDeltaTime = float(stats[5])
        DeltaTime_std = float(stats[6])
        break
    elif float(stats[7]) > calOptions.numAverages and float(stats[6])*1e12 > calOptions.max_std_ps:
        channelString = "CHANNEL%d" % channel
        commandString = ":MEASure:DELTatime CHANnel1,"+channelString # This will start the measurement again
        osci.write(commandString)
    else:
        sleepMillis(500) # Sleep as to not overwhelm scope with queries

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

writeCalFile.args = 'measuredCoarseDelayDict, failCoarseDelayDict'
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "valReport_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "valReport_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for channel in range(1,17,1):
            print("%g," %channel, end=' ', file=outFile)
        print("", file=outFile)
        for channel in range(1,17,1):
            print("%g," % measuredCoarseDelayDict[channel][rate], end=' ', file=outFile)
        print("", file=outFile)
        for channel in range(1,17,1):
            print("%g," % failCoarseDelayDict[channel][rate], end=' ', file=outFile)
        print("", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False

writeCalFileTemp.args = 'measuredCoarseDelayDict, failCoarseDelayDict'
writeCalFileTemp.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "valReportTemp_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "valReportTemp_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for channel in range(1,17,1):
            print("%g," %channel, end=' ', file=outFile)
        print("", file=outFile)
        for channel in range(1,17,1):
            print("%g," % measuredCoarseDelayDict[channel][rate], end=' ', file=outFile)
        print("", file=outFile)
        for channel in range(1,17,1):
            print("%g," % failCoarseDelayDict[channel][rate], end=' ', file=outFile)
        print("", file=outFile)
'''
writeCalFileTemp.wantAllVarsGlobal = False


div256.bits = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
div256.notes = ''

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
txChannelList1.patterns = [div256]
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
fail = 0
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)
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

failCoarseDelayDict = dict()
for channel in range(1,17,1):
    failCoarseDelayDict[channel] = dict()
    for dataRate in calOptions.calRates :
        failCoarseDelayDict[channel][dataRate] = int()
        failCoarseDelayDict[channel][dataRate] = 0

for (i, group) in enumerate(groups) :
    print(group)
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
        if (abs(coarseDelay0) > halfUi/2):
            failCoarseDelayDict[group[0]][dataRate] = coarseDelay0
            print("fail on channel %d get %f" % (group[0], failCoarseDelayDict[group[0]][dataRate]))
            fail = 1

        coarseDelay1 = performScopeCal(group[1],3,dataRate)
        measureCoarseDelayDict[group[1]][dataRate] = coarseDelay1 * 1e12
        if (abs(coarseDelay1) > halfUi/2):
            failCoarseDelayDict[group[1]][dataRate] = coarseDelay1
            print("fail on channel %d get %g" % (group[1], failCoarseDelayDict[group[1]][dataRate]))
            fail = 1

        coarseDelay2 = performScopeCal(group[2],4,dataRate)
        measureCoarseDelayDict[group[2]][dataRate] = coarseDelay2 * 1e12
        if (abs(coarseDelay2) > halfUi/2):
            failCoarseDelayDict[group[1]][dataRate] = coarseDelay2
            print("fail on channel %d get %g" % (group[2], failCoarseDelayDict[group[2]][dataRate]))
            fail = 1

    writeCalFileTemp(measureCoarseDelayDict, failCoarseDelayDict)
writeCalFile(measureCoarseDelayDict, failCoarseDelayDict)

if fail == 1 :
    writeNoteForTestRun("Fail")
else :
    writeNoteForTestRun("Pass")
