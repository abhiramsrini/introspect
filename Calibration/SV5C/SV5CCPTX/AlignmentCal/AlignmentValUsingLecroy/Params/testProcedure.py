# SVT Test
# SVT version 25.2.b1
# Test saved 2025-06-19_1529
# Form factor: SV5C_4L8G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: cc89414c596a64657ccfc323eb5c1c31
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName=None)
calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
initScope = _create('initScope', 'SvtFunction', iespName=None)
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName=None)
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName=None)
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName=None)
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName=None)

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
import time

print("Setting channels to autoscale")
osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("*OPC?", 1)


# Clear display
print("Clearing display")
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(100)

# Set timebase to proper value
print("Setting timebase to 100 ps")
osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 100e-012'", 1)
iesp.setMeasurementTimeout(60000)
osci.writestring("VBS 'app.Acquisition.Trigger.C1Slope = 0'", 1)

time.sleep(30)
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='any', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[4125.0, 5125.0, 6125.0, 7525.0], displayOrder=(0, 7.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '79-0057'
calOptions.scopeIPAddress = 'TCPIP0::169.254.197.102::inst0::INSTR'
calOptions.scopeMeasurementDelay = 2000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4]
calOptions.calRates = [4125.0, 5125.0, 6125.0, 7525.0]
calOptions.callCustomInitMethod()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa

#connect to scope
import win32com.client
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)
osci.WriteString("VBS 'app.SetToDefaultSetup'", 1)
osci.WriteString("*OPC?", 1)
sleepMillis(calOptions.scopeAutoScaleDelay)
iesp.setMeasurementTimeout(60000)

# Display/Enable the channels

print("Setting channels to display")
osci.WriteString("VBS 'app.Acquisition.C1.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.View = true'", 1)

# Make sure all skew are at 0. This is not reset by default
print("Setting skew to 0")
osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C4.Deskew = 0'", 1)

# Configure the Measurement Parameter
osci.WriteString("VBS 'app.Measure.P1.MeasurementType = 0'", 1)
osci.WriteString("VBS 'app.Measure.ShowMeasure = true",1)
osci.WriteString("VBS 'app.Measure.StatsOn = true",1)
osci.WriteString("VBS 'app.Measure.P1.View = true",1)
osci.WriteString("VBS 'app.Measure.P2.View = False",1)

# Turn averaging on
osci.writestring("VBS 'app.Acquisition.C1.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C2.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C3.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C4.AverageSweeps = 1'", 1)


# Define delta-time measurement parameters

print("Setting delta-time measurement parameters")
osci.WriteString("VBS 'app.Measure.P1.ParamEngine = \"DeltaTimeAtLevel\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel1 = 50'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope2 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel2 = 50'", 1)

return osci
'''
initScope.wantAllVarsGlobal = False

measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
import time
channelString = "C%d" % channel
print ("channel string is %s" % channelString)
osci.WriteString("VBS 'app.Measure.P1.Source1 = 0'" , 1)

commandString = "VBS 'app.Measure.P1.Source2 = \"%s\"'" % channelString
osci.WriteString(commandString, 1)
sleepMillis(calOptions.scopeAutoScaleDelay)
commandString = "VBS? 'return = app.Measure.P1.mean.Result.Value'"
osci.WriteString(commandString, 1)
currentDeltaTime = 0


for i in range(calOptions.numAverages) :

    varAmp = osci.WriteString(commandString, 1)
    sleepMillis(50)
    varAmp = osci.ReadString(100)
    osci.WriteString("VBS? 'return=app.WaitUntilIdle(20)'", 1)
    osci.WriteString("*OPC?", 1)
    currentDeltaTime += float(varAmp)

currentDeltaTime = currentDeltaTime / calOptions.numAverages

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False

performScopeCal.args = 'lane,wire,position,  dataRate'
performScopeCal.code = r'''if lane == 4 and wire == 2:
    print("Performing coarse loop...")
    coarse = 0
    coarseDelay = coarse
    print("delay is %d..." % coarseDelay)
    print(" ")

else: # channels 2-16
    print("Performing coarse loop...")
    print ("Position is %d" %position)
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
wires = ['A', 'B', 'C']
##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%d  %s," %(lane,wires[wire]), end=' ', file=outFile)
        print("", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%g," % measuredCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%g," % failCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
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
wires = ['A', 'B', 'C']

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    for rate in calOptions.calRates:
        print("#Data Rate = %f" % rate, file=outFile)
        print("#Tx Skew Coarse", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%d  %s," %(lane,wires[wire]), end=' ', file=outFile)
        print("", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%g," % measuredCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
        for lane in [1, 2, 3, 4]:
            for wire in [0,1,2]:
                print("%g," % failCoarseDelayDict[lane][rate][wire], end=' ', file=outFile)
        print("", file=outFile)
'''
writeCalFileTemp.wantAllVarsGlobal = False


cphyParams1.calAlternateSeqNumPrbs = 8
cphyParams1.calPreambleNumUI = 21
cphyParams1.calUserSequence = [0x5555, 0xAAAA]
cphyParams1.calibrationPreambleFormat = 'format_1'
cphyParams1.lp000Duration = 65.0
cphyParams1.lp001Duration = 100.0
cphyParams1.opticalLink = 'disabled'
cphyParams1.post2NumUI = 112
cphyParams1.postNumUI = 112
cphyParams1.postSymbols = '4444444'
cphyParams1.preBeginNumUI = 196
cphyParams1.preBeginSymbols = '3333333'
cphyParams1.preEndSymbols = '3333333'
cphyParams1.progSeqSymbols = '33333333333333'
cphyParams1.syncWord = '3444443'
cphyParams1.t3AlpPauseMin = 50
cphyParams1.t3AlpPauseWake = 50
cphyParams1.tHsExitDuration = 300.0
cphyParams1.tTaGetDuration = 5
cphyParams1.tTaGoDuration = 4.0
cphyParams1.tTaSureDuration = 1.0
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 100.0
cphyParams1.useAlp = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 5000.0
mipiClockConfig1.referenceClocks = None

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.commonNoise = None
mipiGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.hsPostTaps = [0]
mipiGenerator1.hsPreTaps = [0]
mipiGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lanes = [1, 2, 3, 4]
mipiGenerator1.lpHighVoltages = [1200.0]
mipiGenerator1.lpLowVoltages = [0.0]
mipiGenerator1.params = cphyParams1
mipiGenerator1.pattern = CPHY_hsOnly333
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = True
mipiGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

#! TEST PROCEDURE
svtVersion = requireSvtVersionInRange("24.3", None)

fail = 0

#svtVersion = requireSvtVersionInRange("23.1", None)
import numpy as np
iesp = getIespInstance()

# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

# Define results dictionary
measureCoarseDelayDict = dict()
for lane in [1, 2, 3, 4] :
   measureCoarseDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      measureCoarseDelayDict[lane][dataRate] = dict()
      for wire in [0,1,2]:
          measureCoarseDelayDict[lane][dataRate][wire] = 0

#initialize generator
mipiGenerator1.lanes = calOptions.calLanes
mipiGenerator1.setup()


failCoarseDelayDict = dict()
for lane in [1, 2, 3, 4] :
   failCoarseDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      failCoarseDelayDict[lane][dataRate] = dict()
      for wire in [0,1,2]:
          failCoarseDelayDict[lane][dataRate][wire] = 0

for lane in [4,3,2,1]:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring C-PHY Lane %d..." % lane)

    if lane==4 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire C to Ch1, Wire B, to Ch2, and Wire A to Ch3' % lane
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire C to Ch2, Wire B to Ch3, and Wire A to Ch4. IMPORTANT: Keep Lane 4C connected to Ch1' % lane

    waitForGuiOkDialog(myString)
    #auto scale once per lane
    autoScale = True

    for dataRate in calOptions.calRates :
        halfUi = 1000000 / dataRate / 2 * 1e-12
        halfUi = halfUi + 5e-12
       # print "HalfUi: %e" % halfUi
        print("Measuring at %f Mbps..." % dataRate)

        #do clock commit
        mipiClockConfig1.dataRate = dataRate
        #initialize generator after clock commit
        mipiGenerator1.setup()
        #enable alignment pattern
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01)
        # Prepare scope for measurement
        if(autoScale):
            autoscaleScope()
            autoScale = False
        if lane==4 :

            coarseDelay1 = performScopeCal(lane,1,2,dataRate)
            measureCoarseDelayDict[lane][dataRate][1] = coarseDelay1 * 1e12
            if (abs(coarseDelay1) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][1] = coarseDelay1
                print("fail on channel %d wire B get %g" % (lane, failCoarseDelayDict[lane][dataRate][1]))
                fail = 1

            coarseDelay2 = performScopeCal(lane,0,3,dataRate)
            measureCoarseDelayDict[lane][dataRate][0] = coarseDelay2 * 1e12
            if (abs(coarseDelay2) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][0] = coarseDelay2
                print("fail on channel %d wire A get %g" % (lane, failCoarseDelayDict[lane][dataRate][0]))
                fail = 1
        else:
            #use scope to measure values
            coarseDelay0 = performScopeCal(lane,2,2,dataRate)
            measureCoarseDelayDict[lane][dataRate][2] = coarseDelay0 * 1e12
            if (abs(coarseDelay0) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][2] = coarseDelay0
                print("fail on channel %d wire C get %f" % (lane, failCoarseDelayDict[lane][dataRate][2]))

            coarseDelay1 = performScopeCal(lane,1,3,dataRate)
            measureCoarseDelayDict[lane][dataRate][1] = coarseDelay1 * 1e12
            if (abs(coarseDelay1) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][1] = coarseDelay1
                print("fail on channel %d wire B get %g" % (lane, failCoarseDelayDict[lane][dataRate][1]))
                fail = 1

            coarseDelay2 = performScopeCal(lane,0,4,dataRate)
            measureCoarseDelayDict[lane][dataRate][0] = coarseDelay2 * 1e12
            if (abs(coarseDelay2) > halfUi/2):
                failCoarseDelayDict[lane][dataRate][0] = coarseDelay2
                print("fail on channel %d wire A get %g" % (lane, failCoarseDelayDict[lane][dataRate][0]))
                fail = 1

    writeCalFileTemp(measureCoarseDelayDict, failCoarseDelayDict)
writeCalFile(measureCoarseDelayDict, failCoarseDelayDict)
#iesp.writeSubPartRegister(0x0C80, 0x00, 0x00)

if fail == 1 :
    writeNoteForTestRun("Fail")
else :
    writeNoteForTestRun("Pass")


if fail == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
elif fail:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)

iesp.writeSubPartRegister(0x0972, 0x00, 0x00)