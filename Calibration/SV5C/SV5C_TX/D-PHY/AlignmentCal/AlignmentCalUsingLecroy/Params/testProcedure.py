# SVT Test
# SVT version 25.2.0
# Test saved 2025-07-01_1824
# Form factor: SV5C_4L8G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: 980a5b96c0a4ecce6696839b5940e176
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName=None)
calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
createPlots = _create('createPlots', 'SvtFunction', iespName=None)
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName=None)
initScope = _create('initScope', 'SvtFunction', iespName=None)
measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName=None)
performScopeCal = _create('performScopeCal', 'SvtFunction', iespName=None)
plotCreator1 = _create('plotCreator1', 'SvtPlotCreator', iespName=None)
writeCalFile = _create('writeCalFile', 'SvtFunction', iespName=None)
writeCalFileTemp = _create('writeCalFileTemp', 'SvtFunction', iespName=None)
writeMeasurements = _create('writeMeasurements', 'SvtFunction', iespName=None)

dphyParams1 = _create('dphyParams1', 'SvtMipiDphyParameters')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiDphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
import time

osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("*OPC?", 1)
time.sleep(5)

# Clear display
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(20)

# Set timebase to proper value

osci.WriteString("VBS 'app.Acquisition.Horizontal.HorScale = 5e-09'", 1)
osci.WriteString("VBS 'app.Acquisition.Trigger.Edge.Slope = \"Positive\"'", 1)
iesp.setMeasurementTimeout(60000)

# Turn averaging on

osci.writestring("VBS 'app.Acquisition.C1.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C2.AverageSweeps = 1'", 1)
osci.writestring("VBS 'app.Acquisition.C3.AverageSweeps = 1'", 1)

# Define delta-time measurement parameters

print("Setting delta-time measurement parameters")
osci.WriteString("VBS 'app.Measure.P1.ParamEngine = \"DeltaTimeAtLevel\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel1 = 50'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope2 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel2 = 50'", 1)

time.sleep(10)
'''
autoscaleScope.wantAllVarsGlobal = False

calOptions.addField('serialNumber', descrip='''Serial number of device under test.''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function.''', attrType=float, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is querried from the scope.''', attrType=int, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of channels to measure.''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', attrSubType=int, defaultVal=[1, 2, 3, 4, 5], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='SV5C_4L8G_MIPI_DPHY_GENERATOR', attrSubType=float, defaultVal=[3126.0, 3500.0, 3750.0, 4000.0, 4250.0, 4500.0, 4750.0, 5000.0, 5250.0, 5500.0, 5750.0, 6000.0, 6250.0], displayOrder=(0, 7.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.serialNumber = '79-0057'
calOptions.scopeIPAddress = 'TCPIP0::10.30.30.155::inst0::INSTR'
calOptions.scopeMeasurementDelay = 2000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4, 5]
calOptions.calRates = [3126.0, 3500.0, 3750.0, 4000.0, 4250.0, 4500.0, 4750.0, 5000.0, 5250.0, 5500.0, 5750.0, 6000.0, 6250.0]
calOptions.callCustomInitMethod()
createPlots.args = 'measureCoarseDelayDict,polyCoefficients'
createPlots.code = r'''for lane in calOptions.calLanes:
    for wire in [0,1]:
        xcvrRates = []
        delays = []
        for datarate in calOptions.calRates:
            xcvrRate = datarate*osRatio
            delays.append(measureCoarseDelayDict[lane][xcvrRate][wire])
            xcvrRates.append(xcvrRate)

        plotCreator1.fileName = "Lane%s_%s"%(lane,wire)
        plotCreator1.run(xcvrRates,delays,polyCoefficients[lane][wire],lane,wire)
'''
createPlots.wantAllVarsGlobal = False

dataFile1.delimiter = ','
dataFile1.fileName = ''
dataFile1.numFields = 1
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'

initScope.args = 'scopeIpAddress'
initScope.code = r'''import pyvisa
#connect to scope
import win32com.client #imports the pywin32 library
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)
osci.WriteString("VBS 'app.SetToDefaultSetup'", 1)
osci.WriteString("*OPC?", 1)
iesp.setMeasurementTimeout(60000)

# Make sure all skew are at 0. This is not reset by default
print("Setting skew to 0")
osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Deskew = 0'", 1)

# Display the channels
print("Setting channels to display")
osci.WriteString("VBS 'app.Acquisition.C1.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C1.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Coupling = 0'", 1)

# Clear display
print("Clearing display")
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(100)

# Make sure we're getting mean values

osci.WriteString("VBS 'app.Measure.P1.MeasurementType = 0'", 1)
osci.WriteString("VBS 'app.Measure.ShowMeasure = true",1)
osci.WriteString("VBS 'app.Measure.StatsOn = true",1)
osci.WriteString("VBS 'app.Measure.P1.View = true",1)
osci.WriteString("VBS 'app.Measure.P2.View = False",1)

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
osci.WriteString("VBS? 'return=app.WaitUntilIdle(10)'", 1)
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
performScopeCal.code = r'''if lane == 5 and wire == 1:
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

plotCreator1.codeToSetupPlots = r'''""" Example code:
xvals = arange(0, 10, 0.1)
yvals = sin(xvals)
dataSet1 = SvtPlotDataSet(xvals, yvals)
dataSet1.setColor('orange')
dataSet1.setLineStyle(':', 4)
plotA.addDataSet(dataSet1)
"""

xcvrRates = args[0]
delays = args[1]
coeffs = args[2]
lane = args[3]
wire = args[4]


fit_x = np.linspace(min(xcvrRates),max(xcvrRates),100)
fit_y = np.polyval(coeffs,fit_x)

dataSet1 = SvtPlotDataSet(xcvrRates, delays)
dataSet1.setColor('tab:blue')
dataSet1.setMarker('o')
dataSet1.setLabel('Data')

dataSet2 = SvtPlotDataSet(fit_x , fit_y)
dataSet2.setColor('tab:orange')
dataSet2.setLabel('Fit')

plotA.setTitle("Lane %s, Wire %s"%(lane,wire))
plotA.setXLabel('xcvrRate (Mbps)')
plotA.setYLabel('Delay (ps)')

plotA.addDataSet(dataSet1)
plotA.addDataSet(dataSet2)
plotA.setLegend(True)

error = delays-np.polyval(coeffs,xcvrRates)

dataSet3 = SvtPlotDataSet(xcvrRates, error)
dataSet3.setMarker('o')
dataSet3.setColor('tab:blue')
dataSet3.setLineStyle(' ', 4)

plotB.setXLabel('xcvrRate (Mbps)')
plotB.setYLabel('Data - Fit (ps)')


plotB.addDataSet(dataSet3)
'''
plotCreator1.fileName = 'image001'
plotCreator1.folderName = 'AlignmentTransferFunctions'
plotCreator1.grid = True
plotCreator1.layout = 'A;B'
plotCreator1.plotColors = ['Auto']
plotCreator1.plotType = 'line'
plotCreator1.projection = 'rectilinear'
plotCreator1.title = ''
plotCreator1.xAxisLabel = ''
plotCreator1.xAxisLimits = []
plotCreator1.xAxisScale = 'linear'
plotCreator1.xValues = r'''

'''
plotCreator1.yAxisLabel = ''
plotCreator1.yAxisLimits = []
plotCreator1.yAxisScale = 'linear'
plotCreator1.yValues = r'''

'''

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
    calFile.write("section type : dptx_alignment_calibration_data\n")

    for c in range(4):
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                calFile.write("%0.15f," % polyCoefficients[lane][wire][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficients_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFile.wantAllVarsGlobal = False

writeCalFileTemp.args = 'polyCoefficients'
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
    calFile.write("section type : dptx_alignment_calibration_data\n")

    for c in range(4):
        for lane in [5,1, 2, 3, 4]:
            for wire in [0,1]:
                calFile.write("%0.15f," % polyCoefficients[lane][wire][c])
        calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficientsTemp_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeCalFileTemp.wantAllVarsGlobal = False

writeMeasurements.args = 'measureCoarseDelayDict,polyCoefficients'
writeMeasurements.code = r'''dataFile1.fileName = "delayMeasurements_"+calOptions.serialNumber+".csv"
filePath = dataFile1.getFilePath()

with open(filePath, "w") as measFile:
    measFile.write("Fit Data:\n")

    measFile.write("xcvrRate,")
    for lane in calOptions.calLanes:
        for wire in [0,1]:
            measFile.write("Lane%s_%s,"%(lane,wire))
    measFile.write("\n")

    for datarate in calOptions.calRates:
        xcvrRate = datarate*osRatio
        measFile.write("%0.15f,"%xcvrRate)
        for lane in calOptions.calLanes:
            for wire in [0,1]:
                measFile.write("%0.15f,"%measureCoarseDelayDict[lane][xcvrRate][wire])
        measFile.write("\n")

    measFile.write("\n")
    measFile.write("Polyfit Coefficients:\n")

    measFile.write("Coeff,")
    for lane in calOptions.calLanes:
        for wire in [0,1]:
            measFile.write("Lane%s_%s,"%(lane,wire))


    measFile.write("\n")
    for coeff in range(4):
        measFile.write("%0.15f,"%coeff)
        for lane in calOptions.calLanes:
            for wire in [0,1]:
                measFile.write("%0.15f,"%polyCoefficients[lane][wire][coeff])
        measFile.write("\n")

    measFile.close()

dataFile1.saveAsResult("delayMeasurements_"+calOptions.serialNumber)
dataFile1.deleteFile()
'''
writeMeasurements.wantAllVarsGlobal = False


dphyParams1.clockTrailBits = ''
dphyParams1.clockZeroBits = '0000'
dphyParams1.hsTrailBits = ''
dphyParams1.hsZeroBits = '0000'
dphyParams1.sotBits = '00011101'
dphyParams1.tAlpClk01Duration = (0.0, 20.0)
dphyParams1.tAlpClk10Duration = (0.0, 40.0)
dphyParams1.tAlpHs01Duration = (0.0, 20.0)
dphyParams1.tAlpHs10Duration = (0.0, 40.0)
dphyParams1.tAlpxDuration = 120.0
dphyParams1.tClockLpx01Duration = (0.0, 80.0)
dphyParams1.tClockPostDuration = (60.0, 60.0)
dphyParams1.tClockPreDuration = (32.0, 0.0)
dphyParams1.tClockPrepareDuration = (0.0, 80.0)
dphyParams1.tClockTrailDuration = (0.0, 80.0)
dphyParams1.tClockZeroDuration = (0.0, 300.0)
dphyParams1.tHsExitDuration = 240.0
dphyParams1.tHsIdleClkHs0Duration = (0.0, 60.0)
dphyParams1.tHsIdlePostDuration = 8
dphyParams1.tHsIdlePreDuration = 8
dphyParams1.tHsLpx01Duration = (0.0, 80.0)
dphyParams1.tHsPrepareDuration = (5.0, 60.0)
dphyParams1.tHsTrailDuration = (8.0, 60.0)
dphyParams1.tHsZeroDuration = (10.0, 145.0)
dphyParams1.tPreamble = 32
dphyParams1.tTaGetDuration = 5
dphyParams1.tTaGoDuration = 4.0
dphyParams1.tTaSureDuration = 1.0
dphyParams1.tlpxDuration = 80.0
dphyParams1.useAlp = False
dphyParams1.usePreambleSequence = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 5000.0
mipiClockConfig1.referenceClocks = None
mipiClockConfig1.sscEnabled = False
mipiClockConfig1.sscFrequency = 50.0
mipiClockConfig1.sscSpread = 1.0

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.clockSkew = 0.0
mipiGenerator1.commonNoise = None
mipiGenerator1.continuousClock = False
mipiGenerator1.dataLanes = [1, 2, 3, 4]
mipiGenerator1.dataSkews = [0.0]
mipiGenerator1.hsClockCommonVoltage = 200.0
mipiGenerator1.hsClockPostTap = 0
mipiGenerator1.hsClockPreTap = 0
mipiGenerator1.hsClockVoltageAmplitude = 200.0
mipiGenerator1.hsDataCommonVoltages = [200.0]
mipiGenerator1.hsDataPostTaps = [0]
mipiGenerator1.hsDataPreTaps = [0]
mipiGenerator1.hsDataVoltageAmplitudes = [200.0]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lpClockHighVoltage = 1200.0
mipiGenerator1.lpClockLowVoltage = 0.0
mipiGenerator1.lpDataHighVoltages = [1200.0]
mipiGenerator1.lpDataLowVoltages = [0.0]
mipiGenerator1.params = dphyParams1
mipiGenerator1.pattern = DPHY_packetLoop1000_prbs9
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = True

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'

#! TEST PROCEDURE
svtVersion = requireSvtVersionInRange("25.1", None)
iesp = getIespInstance()
import numpy as np

# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

### All Rates are in OS=2 range ###
osRatio = 2

# Define results dictionary
measureCoarseDelayDict = dict()
for lane in range(1,6,1) :
   measureCoarseDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
        xcvrRate = dataRate * osRatio
        measureCoarseDelayDict[lane][xcvrRate] = dict()
        for wire in [0,1]:
            measureCoarseDelayDict[lane][xcvrRate][wire] = 0


polyCoefficients = dict()
for lane in [1, 2, 3, 4,5] :
    polyCoefficients[lane] = dict()
    for wire in [0,1]:
        polyCoefficients[lane][wire] = dict()
        for c in range(4):
            polyCoefficients[lane][wire][c] = 0

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

#initialize generator
mipiGenerator1.dataLanes = [1,2,3,4]

for lane in [5,4,3,2,1]:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring D-PHY Lane %d..." % lane)

    if lane == 5:
        myString = 'Please connect clock signals to the oscilloscope. Wire Neg to Ch1, Wire Pos to Ch2'
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Neg to Ch2, Wire Pos to Ch3. IMPORTANT: Keep CLOCK 1Neg connected to Ch1' % lane
    waitForGuiOkDialog(myString)

    #auto scale once per lane
    autoScale = True

    for dataRate in calOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        iesp.writeSubPartRegister(0x0934, 0x00, 0x01) #Disable the clock offset
        #do clock commit
        mipiClockConfig1.dataRate = dataRate
        #initialize generator after clock commit
        mipiGenerator1.setup()
        #enable alignment pattern
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01)

        #calculate xcvr rate
        xcvrRate = dataRate * osRatio

        # Prepare scope for measurement
        #if(autoScale):
        autoscaleScope()
        #    autoScale = False
        if lane==5 :
            #use scope to measure values
            coarseDelay1 = performScopeCal(lane,1,1,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][1] = coarseDelay1 * 1e12
            coarseDelay2 = performScopeCal(lane,0,2,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][0] = coarseDelay2 * 1e12
        else:
            #use scope to measure values
            coarseDelay1 = performScopeCal(lane,1,2,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][1] = coarseDelay1 * 1e12
            coarseDelay2 = performScopeCal(lane,0,3,xcvrRate)
            measureCoarseDelayDict[lane][xcvrRate][0] = coarseDelay2 * 1e12

    for wire in [0,1] :
        xVals = list()
        yVals = list()
        for dataRate in sorted(calOptions.calRates) :
            #calculate xcvr rate
            xcvrRate = dataRate * osRatio
            xVals.append(xcvrRate)
            yVals.append(measureCoarseDelayDict[lane][xcvrRate][wire])
        polyCoefficients[lane][wire] = np.polyfit(xVals,yVals,3)
        print(polyCoefficients[lane][wire])
    writeCalFileTemp(polyCoefficients)


writeCalFile(polyCoefficients)
writeMeasurements(measureCoarseDelayDict,polyCoefficients)
#createPlots(measureCoarseDelayDict,polyCoefficients)

iesp.writeSubPartRegister(0x0934, 0x00, 0x00) # disable the clock offset
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00)
