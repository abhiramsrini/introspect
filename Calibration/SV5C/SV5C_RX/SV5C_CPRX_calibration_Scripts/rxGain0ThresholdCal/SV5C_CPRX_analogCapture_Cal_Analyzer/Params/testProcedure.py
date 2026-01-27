# SVT Test
# SVT version 25.3.rc0
# Test saved 2025-08-04_1050
# Form factor: SV5C_4L8G_MIPI_CPHY_ANALYZER
# PY3
# Checksum: 5afedce0dd75c2d1c95adb9a385e86e0
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
computeHighVoltage = _create('computeHighVoltage', 'SvtFunction', iespName=None)
computeLeftEdgeLocation = _create('computeLeftEdgeLocation', 'SvtFunction', iespName=None)
computeLowVoltage = _create('computeLowVoltage', 'SvtFunction', iespName=None)
computeRightEdgeLocation = _create('computeRightEdgeLocation', 'SvtFunction', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
generatePlots = _create('generatePlots', 'SvtFunction', iespName=None)
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName=None)
plotCreator3 = _create('plotCreator3', 'SvtPlotCreator', iespName=None)
plotCreator4 = _create('plotCreator4', 'SvtPlotCreator', iespName=None)
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName=None)
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName=None)

analogCapture1 = _create('analogCapture1', 'SvtMipiCphyAnalogCapture')
globalClockConfig = _create('globalClockConfig', 'SvtMipiClockConfig')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

calOptions.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[250.0], displayOrder=(0, 1.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 150.0, 200.0, 250.0], displayOrder=(0, 2.0))
calOptions.addField('saveVscans', descrip='''''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 3.0))
calOptions.addField('wireSubChannels', descrip='''Sub-receivers to calibrate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[0, 1], displayOrder=(0, 4.0))
calOptions.addField('clockPhases', descrip='''phases to calibrate''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['even', 'odd'], displayOrder=(0, 5.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.dataRates = [200.0]
calOptions.targetLevels = [100.0, 125.0, 150.0, 175.0, 210.0]
calOptions.saveVscans = False
calOptions.wireSubChannels = [0, 1]
calOptions.clockPhases = ['even', 'odd']
calOptions.callCustomInitMethod()
computeHighVoltage.args = 'voltages'
computeHighVoltage.code = r'''dig = dftList.digitizeData(voltages, 25)
edgeLocation = dftList.findDigitalTransitions(dig)[0]

startLow = edgeLocation[0] + 1200
endLow = edgeLocation[0] + 1800
i = 0
while voltages[startLow] < 0 :
    i += 1
    startLow = edgeLocation[i] + 1200
    endLow = edgeLocation[i] + 1800
    #print "try to find the next rising edge"

#print voltages[startLow:endLow]

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)


print("HIGH", meanLocation)
return meanLocation
'''
computeHighVoltage.wantAllVarsGlobal = False

computeLeftEdgeLocation.args = 'phases, errCounts'
computeLeftEdgeLocation.code = r'''a = array(errCounts)
zeroRange = np.nonzero(a==0)
targetIndex = np.min(zeroRange[0]) + 10

phaseStep = phases[1]-phases[0]
divisionFactor = 66688
meanLocation = 0.0
for i in range(targetIndex) :
    errorCount1 = errCounts[i+1]
    errorCount2 = errCounts[i]
    if i == (targetIndex-1) :
        errCount1 = divisionFactor
    f_x = -1.0*(errorCount1-errorCount2) / (phases[i+1]-phases[i])
    meanLocation = meanLocation + phases[i]*f_x
meanLocation = phaseStep*(meanLocation/divisionFactor) + phaseStep / 2

return meanLocation
'''
computeLeftEdgeLocation.wantAllVarsGlobal = False

computeLowVoltage.args = 'voltages'
computeLowVoltage.code = r'''dig = dftList.digitizeData(voltages, 25)
up = dftList.findDigitalTransitions(dig)[0]
#print up
edgeLocation = dftList.findDigitalTransitions(dig)[1]
#print edgeLocation
i = 0
startLow = edgeLocation[0] + 1200
endLow = edgeLocation[0] + 1800

while voltages[startLow] > 0 :
    i += 1
    startLow = edgeLocation[i] + 1200
    endLow = edgeLocation[i] + 1800
   # print "try to find the next faling edge"

#print voltages[startLow:endLow]

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)


print("LOW", meanLocation)
return meanLocation
'''
computeLowVoltage.wantAllVarsGlobal = False

computeRightEdgeLocation.args = 'phases, errCounts'
computeRightEdgeLocation.code = r'''a = array(errCounts)
zeroRange = np.nonzero(a==0)
targetIndex = np.max(zeroRange[0]) - 10

phaseStep = phases[1]-phases[0]
divisionFactor = 66688
meanLocation = 0.0
for i in range(targetIndex, len(phases)-1, 1) :
    errorCount1 = errCounts[i+1]
    errorCount2 = errCounts[i]
    if i == (targetIndex-1) :
        errCount1 = divisionFactor
    f_x = 1.0*(errorCount1-errorCount2) / (phases[i+1]-phases[i])
    meanLocation = meanLocation + phases[i]*f_x
meanLocation = phaseStep*(meanLocation/divisionFactor) + phaseStep / 2

return meanLocation
'''
computeRightEdgeLocation.wantAllVarsGlobal = False

coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = '127.0.0.1'
coordinator1.serverPort = 12013

generatePlots.args = ''
generatePlots.code = r'''# generate average transfer functions
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                for phase in calOptions.clockPhases:
                    titleString = 'Transfer Function at %0.0f MHz, Lane %d\n%s, subChannel = %s, phase = %s' % (dataRate,lane, wire,wireSubChannel,phase)
                    xValues = sorted(levels)
                    yValues = list()
                    for targetLevel in sorted(levels) :
                        yValues.append(averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][targetLevel])
                    plotCreatorBasic1.xAxisLabel = "Input Voltage"
                    plotCreatorBasic1.yAxisLabel = "Output Voltage"
                    plotCreatorBasic1.yAxisLimits = [-800.0,800.0]
                    plotCreatorBasic1.title = titleString
                    plotCreatorBasic1.folderName = 'TransferFunctionPlots'
                    plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                for phase in calOptions.clockPhases:
                    titleString = 'Transfer Function vs Fit, DR = %0.0f, Lane %d\n%s, subChannel = %s, phase = %s' % (dataRate,lane, wire,wireSubChannel,phase)
                    plotCreator3.run(lane, dataRate, wire,wireSubChannel,phase, averageVoltageDict, PolynomialDict, titleString)

for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                titleString = 'Transfer Function vs Fit, DR = %0.0f, Lane %d\n%s, subChannel = %s, phase = average' % (dataRate,lane, wire,wireSubChannel)
                plotCreator4.run(lane, dataRate, wire,wireSubChannel, averageVoltageDict, averagePolynomialDict, titleString)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude,wireSubChannel,phase'
getMeasurementsAtAmplitude.code = r'''# Set generator Amplitude
myString = "mipiCphyGenerator1.hsVoltageAmplitudesABC = [(%d, %d, %d)]" % ((abs(amplitude)),(abs(amplitude)),(abs(amplitude)))

coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiCphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(1000)
analogCapture1.resultName = "Lane_data_"+str(amplitude)+"mV_"+str(wireSubChannel)+"_"+phase
result = analogCapture1.run()
lowVoltageForWire = dict()
highVoltageForWire = dict()
for lane in sorted(laneList1.lanes) :
    lowVoltageForWire[lane] = dict()
    highVoltageForWire[lane] = dict()
    for targetWire in ['wireAB', 'wireBC', 'wireCA'] :
        #voltages = result.getAnalysis(lane, targetWire)['digitizedLevels']

        src = HwTarget(lane, targetWire)
        voltages = result.analysisByChannel[src]['digitizedLevels']

        lowVoltageForWire[lane][targetWire] = voltages[0]
        highVoltageForWire[lane][targetWire] = voltages[3]

averageVoltageForLaneHigh = dict()
averageVoltageForLaneLow = dict()
for lane in sorted(laneList1.lanes) :
    averageVoltageForLaneHigh[lane] = dict()
    averageVoltageForLaneLow[lane] = dict()
    for targetWire in ['wireAB', 'wireBC', 'wireCA'] :
        averageVoltageForLaneHigh[lane][targetWire] = highVoltageForWire[lane][targetWire]
        averageVoltageForLaneLow[lane][targetWire] = lowVoltageForWire[lane][targetWire]


return (averageVoltageForLaneHigh, averageVoltageForLaneLow)
'''
getMeasurementsAtAmplitude.wantAllVarsGlobal = False

writeAverageVoltages.args = ''
writeAverageVoltages.code = r'''import os

# create csv file output
stringAppendix = ".csv"
filePathString = "AverageVoltageMeasurements" + stringAppendix
resultFolderCreator1.folderName = "AverageVoltageMeasurements"
folderPath = resultFolderCreator1.run()
filePath = os.path.join(folderPath, filePathString)

with open(filePath, "w") as outFile:

    # Fill header section
    print( "dataRates," ,file=outFile)
    for dataRate in sorted(calOptions.dataRates) :
        print( "%0.1f," % dataRate,file=outFile)
    print( "",file=outFile)

    print( "lanes," ,file=outFile)
    for lane in sorted(laneList1.lanes) :
        print( "%d," % lane,file=outFile)
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            print( "%s, " % wire,file=outFile)
    print( "",file=outFile)

    # End the header section with the keyword Voltages
    print( "Voltages",file=outFile)

    # now fill in the arrays
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                for wireSubChannel in sorted(calOptions.wireSubChannels):
                    for phase in calOptions.clockPhases:
                        commentString = "# Data Rate = %0.0f, Lane = %d, Wire = %s, subChannel = %s, phase = %s" % (dataRate, lane, wire,wireSubChannel,phase)
                        print( commentString,file=outFile)

                        # Output target levels
                        print( "Target,",file=outFile)
                        for level in sorted(levels) :
                            print( "%0.0f," % level,file=outFile)
                        print( "",file=outFile)

                        # Output measured levels
                        print( "Measured,",file=outFile)
                        for level in sorted(levels) :
                            print( "%0.4g," % averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][level],file=outFile)
                        print( "",file=outFile)
'''
writeAverageVoltages.wantAllVarsGlobal = False

writeTransferFunctions.args = ''
writeTransferFunctions.code = r'''import os
import datetime

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)
resultFolderCreator1.folderName = "calCoefficients_" + serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".txt"
filePathString = "calCoefficients_" + serialNumber + stringAppendix
filePath = os.path.join(folderPath, filePathString)

with open(filePath, "w") as outFile:
    commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : header\n")
    outFile.write("serial number : \n"+serialNumber)
    outFile.write("hardware revision : RevB\n")
    outFile.write("date of manufacture(YYYYMMDD) : \n"+date)
    outFile.write("date of calibration(YYYYMMDD) : \n"+date)
    outFile.write("speed grade : 0\n")
    outFile.write("END SECTION\n")
    outFile.write("\n")
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : cprx_rx_threshold_volt_gain0_calibration_data\n")
    outFile.write("# Each data rate block has 6 rows for offset, slope M1, slope M2, slope M3, slope M4, slope M5 respectively.\n")
    outFile.write("# Each row has 3*<number of lanes> columns (i.e. 1 column per wire). So for 4 lanes, the column labels are: AB1, BC1, CA1, AB2, BC2, CA2, AB3, BC3, CA3, AB4, BC4, CA4\n")
    numRates = 1 # 43
    ratesMeasured = 0
    for dataRate in sorted(calOptions.dataRates) :
        ratesMeasured = ratesMeasured + 1
        for i in range(5,-1,-1) :
            outFile.write(commentArray[i]+"\n")
            for lane in range(1,5,1):
                for wire in ['wireAB', 'wireBC', 'wireCA'] :
                    if i == 5:
                        value_0 =  PolynomialDict[dataRate][lane][wire][0]["even"][i] * 1000
                        value_1 =  PolynomialDict[dataRate][lane][wire][1]["even"][i] * 1000
                    else:
                        value_0 = PolynomialDict[dataRate][lane][wire][0]["even"][i]
                        value_1 = PolynomialDict[dataRate][lane][wire][1]["even"][i]
                    outFile.write("%0.10g,%0.10g," % (value_0, value_1))
            outFile.write("\n")

        for i in range(5,-1,-1) :
            outFile.write(commentArray[i]+"\n")
            for lane in range(1,5,1):
                for wire in ['wireAB', 'wireBC', 'wireCA'] :
                    if i == 5:
                        value_0 =  PolynomialDict[dataRate][lane][wire][0]["odd"][i] * 1000
                        value_1 =  PolynomialDict[dataRate][lane][wire][1]["odd"][i] * 1000
                    else:
                        value_0 = PolynomialDict[dataRate][lane][wire][0]["odd"][i]
                        value_1 = PolynomialDict[dataRate][lane][wire][1]["odd"][i]
                    outFile.write("%0.10g,%0.10g," % (value_0, value_1))
            outFile.write("\n")

        for i in range(5,-1,-1) :
            outFile.write(commentArray[i]+"\n")
            for lane in range(1,5,1):
                for wire in ['wireAB', 'wireBC', 'wireCA'] :
                    if i == 5:
                        value_0 =  averagePolynomialDict[dataRate][lane][wire][0][i] * 1000
                        value_1 =  averagePolynomialDict[dataRate][lane][wire][1][i] * 1000
                    else:
                        value_0 = averagePolynomialDict[dataRate][lane][wire][0][i]
                        value_1 = averagePolynomialDict[dataRate][lane][wire][1][i]
                    outFile.write("%0.10g,%0.10g," % (value_0, value_1))
            outFile.write("\n")
    outFile.write("END SECTION\n")
'''
writeTransferFunctions.wantAllVarsGlobal = False

plotCreator3.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
wire = args[2]
wireSubChannel = args[3]
phase = args[4]
dataDict = args[5]
polyDict = args[6]
plotTitle = args[7]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()
yVals1 = list()
yVals2 = list()
for targetLevel in sorted( dataDict[dataRate][lane][wire][wireSubChannel][phase].keys() ) :
    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][wire][wireSubChannel][phase][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane][wire][wireSubChannel][phase],targetLevel)
    yVals2.append(polyFitResult)
dataSet1 = SvtPlotDataSet(xVals, yVals1)
dataSet1.setColor(colors[0])
dataSet1.setLineStyle(':')
dataSet1.setMarker('o',2)
plotA.addDataSet(dataSet1)

dataSet2 = SvtPlotDataSet(xVals, yVals2)
dataSet2.setColor(colors[2])
dataSet2.setLineStyle(':')
dataSet2.setMarker('o',2)
plotA.addDataSet(dataSet2)

plotA.setTitle(plotTitle)
plotA.setYLim([-630.0, 630.0])
'''
plotCreator3.fileName = 'image001'
plotCreator3.folderName = 'DataVersusPolyFit'
plotCreator3.grid = True
plotCreator3.layout = 'A'
plotCreator3.plotColors = ['blue']
plotCreator3.plotType = 'line'
plotCreator3.projection = 'rectilinear'
plotCreator3.title = ''
plotCreator3.xAxisLabel = ''
plotCreator3.xAxisLimits = []
plotCreator3.xAxisScale = 'linear'
plotCreator3.xValues = r'''

'''
plotCreator3.yAxisLabel = ''
plotCreator3.yAxisLimits = []
plotCreator3.yAxisScale = 'linear'
plotCreator3.yValues = r'''

'''

plotCreator4.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
wire = args[2]
wireSubChannel = args[3]
dataDict = args[4]
polyDict = args[5]
plotTitle = args[6]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()

yVals1 = list()
yVals2 = list()
yVals3 = list()
for targetLevel in sorted( dataDict[dataRate][lane][wire][wireSubChannel][phase].keys() ) :

    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][wire][wireSubChannel]['even'][targetLevel])

    yVals2.append(dataDict[dataRate][lane][wire][wireSubChannel]['odd'][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane][wire][wireSubChannel],targetLevel)
    yVals3.append(polyFitResult)

dataSet1 = SvtPlotDataSet(xVals, yVals1)
dataSet1.setColor(colors[0])
dataSet1.setLineStyle(':')
dataSet1.setLabel('Data (Even Phase)')
dataSet1.setMarker('o',2)
plotA.addDataSet(dataSet1)

dataSet2 = SvtPlotDataSet(xVals, yVals2)
dataSet2.setColor(colors[2])
dataSet2.setLineStyle(':')
dataSet2.setLabel('Data (Odd Phase)')
dataSet2.setMarker('o',2)
plotA.addDataSet(dataSet2)

dataSet3 = SvtPlotDataSet(xVals, yVals3)
dataSet3.setColor(colors[3])
dataSet3.setLineStyle('-')
dataSet3.setLabel('Average Polynomial Fit')
dataSet3.setMarker('o',2)
plotA.addDataSet(dataSet3)

plotA.setTitle(plotTitle)
plotA.setLegend(True)
plotA.setYLim([-630.0, 630.0])
'''
plotCreator4.fileName = 'image001'
plotCreator4.folderName = 'DataVersusPolyFit_average'
plotCreator4.grid = True
plotCreator4.layout = 'A'
plotCreator4.plotColors = ['blue']
plotCreator4.plotType = 'line'
plotCreator4.projection = 'rectilinear'
plotCreator4.title = ''
plotCreator4.xAxisLabel = ''
plotCreator4.xAxisLimits = []
plotCreator4.xAxisScale = 'linear'
plotCreator4.xValues = r'''

'''
plotCreator4.yAxisLabel = ''
plotCreator4.yAxisLimits = []
plotCreator4.yAxisScale = 'linear'
plotCreator4.yValues = r'''

'''

plotCreatorBasic1.plotColors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black', 'blue', 'green']
plotCreatorBasic1.plotType = 'scatter'
plotCreatorBasic1.title = ''
plotCreatorBasic1.xAxisLabel = ''
plotCreatorBasic1.xAxisScale = 'linear'
plotCreatorBasic1.xValues = r'''
args[0]
'''
plotCreatorBasic1.yAxisLabel = ''
plotCreatorBasic1.yAxisScale = 'linear'
plotCreatorBasic1.yValues = r'''
args[1]
'''

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 350.0
analogCapture1.forceFramePeriod = False
analogCapture1.forcedFramePeriodDuration = 1
analogCapture1.framePeriodType = 'numberOfBursts'
analogCapture1.laneList = laneList1
analogCapture1.lineRateSource = 'fromClockConfig'
analogCapture1.measurementMode = 'differential'
analogCapture1.nthBurst = 1
analogCapture1.numBitsDesired = 512
analogCapture1.patternLenSymbols = 8
analogCapture1.refLane = 1
analogCapture1.saveResults = True
analogCapture1.startVoltage = -350.0
analogCapture1.timeout = 240
analogCapture1.triggerType = 'frame'
analogCapture1.wantAnalysis = True
analogCapture1.wantEyeDiagrams = False
analogCapture1.wantResultImages = False
analogCapture1.wires = ['wireAB', 'wireBC', 'wireCA']

globalClockConfig.autoDetectDataRate = False
globalClockConfig.autoDetectTimeout = 2.0
globalClockConfig.dataRate = 200.0
globalClockConfig.referenceClocks = refClocksConfig1

laneList1.expectedPattern = None
laneList1.hsThresholdVoltage = 0.0
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 600.0

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig1.externRefClockFreq = 100.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.systemRefClockSource = 'external'

resultFolderCreator1.channelProvider = laneList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

#! TEST PROCEDURE
import math
import numpy as np
from dftm.fileUtil import copyContentsOfFolder
from dftm.miscTypes import HwTarget

coordinator1.setState("running")
iesp = IESP.getInstance()

failFlag = 0

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("25.1", None)
iesp.enableVeryPatientMode()

# check the serial number
serialNumberFailFlag = 1
for trial in range(5):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    serialNumber = getTextDialog("Please enter the serial number of the RX unit (89-xxxx):")
    if serialNumber[:3] == '89-':
        serialNumberFailFlag = 0
        break

context = getCurrentTest()
RunNotesFolderPath = context.getCurrRunResultFolderPath()
resultFolderPath = context.createRunResultFolder(serialNumber)


dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

iesp.disableValidation()
# Set the analog capture scan limits to the maximum
analogCapture1.startVoltage = -630
analogCapture1.endVoltage = 630


# Declare global dictionary of measured values
averageVoltageDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    globalClockConfig.dataRate = dataRate
    globalClockConfig.setup()
    averageVoltageDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averageVoltageDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averageVoltageDict[dataRate][lane][wire] = dict()
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                averageVoltageDict[dataRate][lane][wire][wireSubChannel] = dict()
                for phase in calOptions.clockPhases:
                    averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase] = dict()
                    for targetLevel in sorted(calOptions.targetLevels) :
                        averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
PolynomialDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    PolynomialDict[dataRate] = dict()
    for lane in range(1,5,1) :
        PolynomialDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            PolynomialDict[dataRate][lane][wire] = dict()
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                PolynomialDict[dataRate][lane][wire][wireSubChannel] = dict()
                for phase in calOptions.clockPhases:
                    PolynomialDict[dataRate][lane][wire][wireSubChannel][phase] = [0.0,0.0,0.0,0.0,0.0,0.0]

# Loop over calibration variables
averagePolynomialDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averagePolynomialDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averagePolynomialDict[dataRate][lane][wire] = dict()
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                averagePolynomialDict[dataRate][lane][wire][wireSubChannel] = [0.0,0.0,0.0,0.0,0.0,0.0]

    # start generator
    myString = "mipiCphyGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(5000)

    for wireSubChannel in sorted(calOptions.wireSubChannels):
        # Placing clock commit here to ensure that the even/odd states toggle correctly
        globalClockConfig.setup()
        # Set appropriate subreceiver state
        # Firmware mapping:
        #0 - Default. SubChan0 = 0, SubChan1 = 1
        #1 - Flipped. SubChan0 = 1, SubChan1 = 0
        #2 - Dual Receiver 0. SubChan0 = 0, SubChan1 = 0
        #3 - Dual Receiver 1. SubChan0 = 1, SubChan1 = 1
        if wireSubChannel == 0:
            print("Selecting sub-receiver 0")
            # Select Dual Receiver 0
            subRecOption = 0x02
            iesp.writeSubPartRegister(0xFEDD, 0x00, subRecOption)
            iesp.waitForCommandProcessors()
        elif wireSubChannel == 1:
            print("Selecting sub-receiver 1")
            # Select Dual Receiver 1
            subRecOption = 0x03
            iesp.writeSubPartRegister(0xFEDD, 0x00, subRecOption)
            iesp.waitForCommandProcessors()
        for phase in calOptions.clockPhases:
            if phase == "odd":
                # This assumes that the even state has been tested first!
                print("Toggling odd phase state.")
                iesp.writeSubPartRegister(0xFEEC, 0x00, 0x00) # Toggles even/odd state
                iesp.waitForCommandProcessors()
            # now measure
            for targetLevel in sorted(calOptions.targetLevels) :
                (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel,wireSubChannel,phase)
                print("Measuring level "+str(targetLevel)+"mV")
                print(averageVoltagePerLaneHigh, averageVoltagePerLaneLow)
                for lane in sorted(laneList1.lanes) :
                    for wire in ['wireAB', 'wireBC', 'wireCA'] :
                        averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][targetLevel] = averageVoltagePerLaneHigh[lane][wire]
                        averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][-targetLevel] = averageVoltagePerLaneLow[lane][wire]
                        if ((averageVoltagePerLaneHigh[lane][wire] - averageVoltagePerLaneLow[lane][wire]) < 100) or math.isnan(averageVoltagePerLaneHigh[lane][wire]) or math.isnan(averageVoltagePerLaneLow[lane][wire]):
                            failFlag = 1
                            warningMsg("Bad Value on Lane %d wire %s..." % (lane, wire))

#print(averageVoltageDict)

# This is some dummy data that can be used for debug purposes

#averageVoltageDict = {200.0: {1: {'wireAB': {0: {'even': {100.0: 219.40374, 125.0: 264.47186, 150.0: 306.90436, 175.0: 349.13347, 210.0: 399.15669, -100.0: -186.22131, -125.0: -231.23423, -150.0: -269.45066, -175.0: -306.23916, -210.0: -350.94548}, 'odd': {100.0: 181.17251, 125.0: 218.40164, 150.0: 256.73586, 175.0: 283.7861, 210.0: 325.71056, -100.0: -196.54205, -125.0: -238.31847, -150.0: -278.33346, -175.0: -314.17117, -210.0: -355.89965}}, 1: {'even': {100.0: 218.00282, 125.0: 260.05475, 150.0: 304.81795, 175.0: 343.72003, 210.0: 394.01468, -100.0: -214.85274, -125.0: -260.32224, -150.0: -303.65906, -175.0: -344.62009, -210.0: -389.26599}, 'odd': {100.0: 222.31079, 125.0: 270.08876, 150.0: 315.84912, 175.0: 355.1915, 210.0: 403.49113, -100.0: -215.66521, -125.0: -260.86312, -150.0: -307.63659, -175.0: -349.91723, -210.0: -403.52689}}}, 'wireBC': {0: {'even': {100.0: 251.14819, 125.0: 303.54344, 150.0: 355.0824, 175.0: 406.49189, 210.0: 467.02706, -100.0: -227.80396, -125.0: -280.48277, -150.0: -334.03682, -175.0: -387.72963, -210.0: -449.16994}, 'odd': {100.0: 259.64388, 125.0: 310.80085, 150.0: 361.23119, 175.0: 408.32333, 210.0: 464.285, -100.0: -190.53678, -125.0: -238.47107, -150.0: -281.45603, -175.0: -323.93852, -210.0: -374.7739}}, 1: {'even': {100.0: 208.58999, 125.0: 249.76348, 150.0: 287.26024, 175.0: 323.99986, 210.0: 367.95492, -100.0: -200.73406, -125.0: -243.94354, -150.0: -286.187, -175.0: -325.70058, -210.0: -370.9827}, 'odd': {100.0: 234.59634, 125.0: 282.44508, 150.0: 330.58794, 175.0: 374.5068, 210.0: 430.5289, -100.0: -205.373, -125.0: -253.20543, -150.0: -299.58507, -175.0: -343.98332, -210.0: -397.84317}}}, 'wireCA': {0: {'even': {100.0: 317.16941, 125.0: 389.58026, 150.0: 462.67871, 175.0: 538.05832, 210.0: 634.95312, -100.0: -194.91446, -125.0: -249.8123, -150.0: -303.22931, -175.0: -356.50035, -210.0: -419.44257}, 'odd': {100.0: 195.88595, 125.0: 244.4507, 150.0: 289.75075, 175.0: 331.44328, 210.0: 387.21755, -100.0: -248.63272, -125.0: -303.57891, -150.0: -353.02317, -175.0: -404.33015, -210.0: -464.41179}}, 1: {'even': {100.0: 234.15148, 125.0: 281.62626, 150.0: 325.67758, 175.0: 367.53183, 210.0: 420.18957, -100.0: -198.84557, -125.0: -243.73054, -150.0: -285.31405, -175.0: -325.1422, -210.0: -370.40524}, 'odd': {100.0: 302.96794, 125.0: 361.2592, 150.0: 421.9116, 175.0: 478.4701, 210.0: 550.66148, -100.0: -178.46756, -125.0: -224.54389, -150.0: -269.38034, -175.0: -312.50293, -210.0: -362.51378}}}}, 2: {'wireAB': {0: {'even': {100.0: 243.71855, 125.0: 292.31382, 150.0: 339.65303, 175.0: 382.226, 210.0: 435.72456, -100.0: -187.43791, -125.0: -232.35127, -150.0: -270.96334, -175.0: -309.5949, -210.0: -353.25643}, 'odd': {100.0: 282.10406, 125.0: 335.36669, 150.0: 381.82789, 175.0: 427.73525, 210.0: 483.41562, -100.0: -138.41534, -125.0: -178.8798, -150.0: -216.5119, -175.0: -243.93796, -210.0: -282.60449}}, 1: {'even': {100.0: 249.02051, 125.0: 299.82505, 150.0: 346.55398, 175.0: 395.07394, 210.0: 450.34692, -100.0: -190.7506, -125.0: -238.48559, -150.0: -281.6562, -175.0: -321.46195, -210.0: -374.59944}, 'odd': {100.0: 300.33223, 125.0: 357.00719, 150.0: 416.33762, 175.0: 468.7535, 210.0: 537.78249, -100.0: -180.90376, -125.0: -231.42459, -150.0: -278.14745, -175.0: -320.3293, -210.0: -373.24174}}}, 'wireBC': {0: {'even': {100.0: 253.99864, 125.0: 300.47384, 150.0: 347.93433, 175.0: 393.60738, 210.0: 450.38936, -100.0: -169.34108, -125.0: -213.84964, -150.0: -249.09192, -175.0: -284.53438, -210.0: -327.47396}, 'odd': {100.0: 206.11788, 125.0: 247.73539, 150.0: 283.90827, 175.0: 321.53049, 210.0: 365.23103, -100.0: -199.47509, -125.0: -240.72535, -150.0: -281.28629, -175.0: -320.96172, -210.0: -367.87002}}, 1: {'even': {100.0: 201.36534, 125.0: 246.8796, 150.0: 291.28935, 175.0: 331.34574, 210.0: 385.8719, -100.0: -220.45491, -125.0: -266.63859, -150.0: -312.60806, -175.0: -355.93989, -210.0: -410.10253}, 'odd': {100.0: 222.88172, 125.0: 271.72491, 150.0: 319.61533, 175.0: 365.11911, 210.0: 428.16685, -100.0: -207.21543, -125.0: -252.41722, -150.0: -298.39213, -175.0: -342.47611, -210.0: -400.13097}}}, 'wireCA': {0: {'even': {100.0: 220.18771, 125.0: 266.95954, 150.0: 311.57427, 175.0: 359.27372, 210.0: 408.58457, -100.0: -248.35843, -125.0: -303.39217, -150.0: -359.17667, -175.0: -413.20511, -210.0: -480.19968}, 'odd': {100.0: 216.36491, 125.0: 265.5349, 150.0: 307.74149, 175.0: 347.21021, 210.0: 397.67742, -100.0: -226.59143, -125.0: -269.68595, -150.0: -314.15126, -175.0: -354.66871, -210.0: -405.54563}}, 1: {'even': {100.0: 255.77415, 125.0: 311.95131, 150.0: 363.1592, 175.0: 415.3316, 210.0: 480.69462, -100.0: -244.25044, -125.0: -302.29733, -150.0: -356.52304, -175.0: -410.7343, -210.0: -481.87827}, 'odd': {100.0: 251.33944, 125.0: 301.29488, 150.0: 348.28726, 175.0: 393.08765, 210.0: 442.59275, -100.0: -221.582, -125.0: -274.34719, -150.0: -326.31653, -175.0: -372.81463, -210.0: -432.56621}}}}, 3: {'wireAB': {0: {'even': {100.0: 269.24186, 125.0: 317.36534, 150.0: 366.53746, 175.0: 417.40374, 210.0: 489.98414, -100.0: -148.81347, -125.0: -191.19066, -150.0: -234.50797, -175.0: -277.09293, -210.0: -332.54425}, 'odd': {100.0: 270.73573, 125.0: 320.9705, 150.0: 368.46636, 175.0: 423.60912, 210.0: 496.25347, -100.0: -148.54527, -125.0: -190.68336, -150.0: -231.46639, -175.0: -273.43337, -210.0: -327.61336}}, 1: {'even': {100.0: 229.58318, 125.0: 279.44316, 150.0: 328.79706, 175.0: 377.71399, 210.0: 439.20563, -100.0: -194.34946, -125.0: -243.6436, -150.0: -286.08501, -175.0: -331.31283, -210.0: -390.0958}, 'odd': {100.0: 219.39689, 125.0: 268.06033, 150.0: 318.07143, 175.0: 365.6889, 210.0: 431.47692, -100.0: -211.74461, -125.0: -262.05222, -150.0: -311.49712, -175.0: -358.4648, -210.0: -424.76693}}}, 'wireBC': {0: {'even': {100.0: 234.31822, 125.0: 279.90947, 150.0: 323.23294, 175.0: 365.68811, 210.0: 418.6169, -100.0: -170.1809, -125.0: -216.20672, -150.0: -257.63712, -175.0: -298.36618, -210.0: -347.83232}, 'odd': {100.0: 232.50923, 125.0: 278.12915, 150.0: 319.96198, 175.0: 361.29741, 210.0: 414.056, -100.0: -169.49691, -125.0: -213.87615, -150.0: -256.28214, -175.0: -296.25982, -210.0: -343.96202}}, 1: {'even': {100.0: 218.41856, 125.0: 257.84605, 150.0: 292.99052, 175.0: 328.78052, 210.0: 370.15557, -100.0: -172.67137, -125.0: -213.83884, -150.0: -248.35075, -175.0: -284.06133, -210.0: -327.90601}, 'odd': {100.0: 225.91736, 125.0: 271.62614, 150.0: 321.77159, 175.0: 363.24801, 210.0: 421.61103, -100.0: -194.62019, -125.0: -241.03566, -150.0: -286.09206, -175.0: -331.0077, -210.0: -389.91796}}}, 'wireCA': {0: {'even': {100.0: 245.93119, 125.0: 297.67035, 150.0: 348.58194, 175.0: 396.71533, 210.0: 465.7688, -100.0: -221.64069, -125.0: -270.54832, -150.0: -320.85532, -175.0: -364.45247, -210.0: -427.788}, 'odd': {100.0: 215.65847, 125.0: 267.23903, 150.0: 315.79812, 175.0: 360.08608, 210.0: 422.78917, -100.0: -274.87748, -125.0: -331.33076, -150.0: -388.39461, -175.0: -443.77171, -210.0: -518.31107}}, 1: {'even': {100.0: 283.01736, 125.0: 332.18594, 150.0: 381.10165, 175.0: 432.97711, 210.0: 503.53518, -100.0: -120.71268, -125.0: -160.78657, -150.0: -200.92389, -175.0: -238.66336, -210.0: -284.01649}, 'odd': {100.0: 236.05071, 125.0: 282.98096, 150.0: 328.23453, 175.0: 373.36034, 210.0: 437.51621, -100.0: -194.34317, -125.0: -242.61413, -150.0: -290.10559, -175.0: -336.58441, -210.0: -402.27891}}}}, 4: {'wireAB': {0: {'even': {100.0: 274.35362, 125.0: 323.24283, 150.0: 370.21236, 175.0: 415.72574, 210.0: 480.13986, -100.0: -138.8384, -125.0: -180.69868, -150.0: -219.89595, -175.0: -258.01301, -210.0: -306.63739}, 'odd': {100.0: 159.97837, 125.0: 199.70699, 150.0: 237.55982, 175.0: 269.18149, 210.0: 311.5794, -100.0: -221.34161, -125.0: -265.58998, -150.0: -306.30586, -175.0: -346.18924, -210.0: -400.39316}}, 1: {'even': {100.0: 249.12656, 125.0: 295.71823, 150.0: 341.73406, 175.0: 384.06966, 210.0: 440.20764, -100.0: -180.95861, -125.0: -232.01915, -150.0: -273.60059, -175.0: -314.79383, -210.0: -373.35224}, 'odd': {100.0: 242.67055, 125.0: 291.18667, 150.0: 335.32359, 175.0: 380.33314, 210.0: 439.58538, -100.0: -187.02441, -125.0: -237.51522, -150.0: -280.93904, -175.0: -323.28365, -210.0: -379.83248}}}, 'wireBC': {0: {'even': {100.0: 160.45273, 125.0: 200.1792, 150.0: 240.65154, 175.0: 280.45951, 210.0: 327.91705, -100.0: -199.60176, -125.0: -242.46716, -150.0: -282.53957, -175.0: -320.50657, -210.0: -365.57397}, 'odd': {100.0: 160.06294, 125.0: 200.3219, 150.0: 240.37649, 175.0: 280.01364, 210.0: 327.31439, -100.0: -214.50314, -125.0: -263.49514, -150.0: -310.72808, -175.0: -356.54392, -210.0: -415.12407}}, 1: {'even': {100.0: 168.95309, 125.0: 211.44955, 150.0: 250.00514, 175.0: 288.59494, 210.0: 334.05647, -100.0: -220.58641, -125.0: -264.1304, -150.0: -305.30816, -175.0: -341.49998, -210.0: -386.28715}, 'odd': {100.0: 179.67968, 125.0: 220.36528, 150.0: 260.56013, 175.0: 299.28333, 210.0: 347.30171, -100.0: -214.40054, -125.0: -254.42195, -150.0: -294.66077, -175.0: -332.67744, -210.0: -379.14877}}}, 'wireCA': {0: {'even': {100.0: 170.50697, 125.0: 210.8427, 150.0: 249.03095, 175.0: 284.21461, 210.0: 335.71197, -100.0: -224.47359, -125.0: -273.41711, -150.0: -317.66288, -175.0: -361.60523, -210.0: -417.67875}, 'odd': {100.0: 190.62992, 125.0: 228.3857, 150.0: 264.03898, 175.0: 299.48528, 210.0: 343.85742, -100.0: -180.87567, -125.0: -220.61795, -150.0: -261.15457, -175.0: -299.72206, -210.0: -353.24129}}, 1: {'even': {100.0: 222.81704, 125.0: 263.43654, 150.0: 307.27398, 175.0: 345.69064, 210.0: 399.92104, -100.0: -190.27878, -125.0: -233.79562, -150.0: -274.2552, -175.0: -312.71766, -210.0: -360.85713}, 'odd': {100.0: 233.53184, 125.0: 277.29328, 150.0: 320.1839, 175.0: 358.39962, 210.0: 412.38131, -100.0: -174.62304, -125.0: -214.86103, -150.0: -251.96262, -175.0: -288.44789, -210.0: -336.55506}}}}}}

levels = list()
for targetLevel in sorted(calOptions.targetLevels) :
    levels.append(targetLevel)
    levels.append(-targetLevel)

# Generate Polynomials
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                for phase in calOptions.clockPhases:
                    xVals = sorted(levels)
                    yVals = list()
                    for level in sorted(levels) :
                        yVals.append(averageVoltageDict[dataRate][lane][wire][wireSubChannel][phase][level])
                    polynomialValues = np.polyfit(xVals, yVals, 5)
                    PolynomialDict[dataRate][lane][wire][wireSubChannel][phase] = polynomialValues

# Generate Polynomials that average Odd/Even
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            for wireSubChannel in sorted(calOptions.wireSubChannels):
                xVals = list()
                yVals = list()
                for level in sorted(levels):
                    # The even and odd data are stored in a single list to fit an average polynomial
                    xVals.append(level)
                    yVals.append(averageVoltageDict[dataRate][lane][wire][wireSubChannel]['even'][level])

                    # x data must be doubled to ensure that the data is paired correctly for the fit
                    xVals.append(level)
                    yVals.append(averageVoltageDict[dataRate][lane][wire][wireSubChannel]['odd'][level])
                polynomialValues = np.polyfit(xVals, yVals, 5)
                averagePolynomialDict[dataRate][lane][wire][wireSubChannel] = polynomialValues

generatePlots()
writeAverageVoltages()
writeTransferFunctions()
writeNoteForTestRun(serialNumber)

if failFlag == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)
    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)


else:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
copyContentsOfFolder(RunNotesFolderPath, resultFolderPath)


# finalize state with coordinator
coordinator1.setState("stopped")
# allow the generator time to detect state change and exit gracefully
sleepMillis(15000)
