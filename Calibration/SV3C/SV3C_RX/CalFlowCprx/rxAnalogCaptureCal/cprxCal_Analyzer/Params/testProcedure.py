# SVT Test
# SVT version 22.4.0
# Test saved 2022-11-23_1007
# Form factor: SV3C_4L3G_MIPI_CPHY_ANALYZER2
# PY3
# Checksum: 731635c84edea6164c0065207217768f
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
computeHighVoltage = _create('computeHighVoltage', 'SvtFunction', iespName='None')
computeLeftEdgeLocation = _create('computeLeftEdgeLocation', 'SvtFunction', iespName='None')
computeLowVoltage = _create('computeLowVoltage', 'SvtFunction', iespName='None')
computeRightEdgeLocation = _create('computeRightEdgeLocation', 'SvtFunction', iespName='None')
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
generatePlots = _create('generatePlots', 'SvtFunction', iespName='None')
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName='None')
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName='None')
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName='None')

analogCapture1 = _create('analogCapture1', 'SvtMipiCphyAnalogCapture')
globalClockConfig = _create('globalClockConfig', 'SvtMipiClockConfig')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
plotCreator3 = _create('plotCreator3', 'SvtPlotCreator')
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

calOptions.addField('moduleName', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[250.0], displayOrder=(0, 2.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 200.0, 300.0, 400.0], displayOrder=(0, 3.0))
calOptions.addField('saveVscans', descrip='''''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 4.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.moduleName = '1234'
calOptions.dataRates = [250.0]
calOptions.targetLevels = [100.0, 200.0, 300.0, 400.0]
calOptions.saveVscans = False
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
            titleString = 'Average Transfer Function at %0.0f MHz, Lane %d, Wire %s' % (dataRate,lane, wire)
            xValues = sorted(levels)
            yValues = list()
            for targetLevel in sorted(levels) :
                yValues.append(averageVoltageDict[dataRate][lane][wire][targetLevel])
            plotCreatorBasic1.xAxisLabel = "Input Voltage"
            plotCreatorBasic1.yAxisLabel = "Output Voltage"
            plotCreatorBasic1.yAxisLimits = [-800.0,800.0]
            plotCreatorBasic1.title = titleString
            plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots'
            plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            titleString = 'Average Transfer Function vs Fit, DR = %0.0f, Lane %d, wire %s' % (dataRate,lane, wire)
            plotCreator3.run(lane, dataRate, wire, averageVoltageDict, averagePolynomialDict, titleString)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude'
getMeasurementsAtAmplitude.code = r'''#print amplitude
#if (amplitude < 0):
#    myString = "mipiCphyGenerator1.hsVoltageAmplitudesABC = [(%d, %d, %d)]" % ((abs(amplitude)*2),(abs(amplitude)*2),(abs(amplitude)*2))
#else:
myString = "mipiCphyGenerator1.hsVoltageAmplitudesABC = [(%d, %d, %d)]" % ((abs(amplitude)),(abs(amplitude)),(abs(amplitude)))

coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiCphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(1000)

minVoltage = -550
maxVoltage = 550
#(voltagesByLane,errCountsByLaneT) = iesp.doVScan(minVoltage, maxVoltage, laneList1.lanes, 1.00032e5, targetWire)
result = analogCapture1.run()
#print errCountsByLaneT
lowVoltageForWire = dict()
highVoltageForWire = dict()
for lane in sorted(laneList1.lanes) :
    lowVoltageForWire[lane] = dict()
    highVoltageForWire[lane] = dict()
    for targetWire in ['wireAB', 'wireBC', 'wireCA'] :
        #print targetWire, lane
        voltages = result.getVoltages(lane,targetWire)
        #print voltages
        lowVoltageForWire[lane][targetWire] = computeLowVoltage(voltages)
        highVoltageForWire[lane][targetWire] = computeHighVoltage(voltages)

    #print lowVoltageForWire[1][targetWire]
    #print highVoltageForWire[1][targetWire]

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
                commentString = "# Data Rate = %0.0f, Lane = %d, Wire = %s" % (dataRate, lane, wire)
                print( commentString,file=outFile)

                # Output target levels
                print( "Target,",file=outFile)
                for level in sorted(levels) :
                    print( "%0.0f," % level,file=outFile)
                print( "",file=outFile)

                # Output measured levels
                print( "Measured,",file=outFile)
                for level in sorted(levels) :
                    print( "%0.4g," % averageVoltageDict[dataRate][lane][wire][level],file=outFile)
                print( "",file=outFile)
'''
writeAverageVoltages.wantAllVarsGlobal = False

writeTransferFunctions.args = ''
writeTransferFunctions.code = r'''import os
import datetime



now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)
resultFolderCreator1.folderName = "calCoefficients_" + calOptions.moduleName
folderPath = resultFolderCreator1.run()

stringAppendix = ".txt"
filePathString = "calCoefficients_" + calOptions.moduleName + stringAppendix
filePath = os.path.join(folderPath, filePathString)

with open(filePath, "w") as outFile:
    commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : header\n")
    outFile.write("serial number : \n"+calOptions.moduleName)
    outFile.write("hardware revision : RevB\n")
    outFile.write("date of manufacture(YYYYMMDD) : \n"+date)
    outFile.write("date of calibration(YYYYMMDD) : \n"+date)
    outFile.write("speed grade : 0\n")
    outFile.write("END SECTION\n")
    outFile.write("\n")
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type: jitter_calibration_data\n")
    outFile.write("ffffffffffffffffffffffffffffffff00000000000000000000000000000000\n")
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
       # commentString = "# Data Rate = %0.0f" % (dataRate)
       # outFile.write(commentString
        for i in range(5,-1,-1) :
            outFile.write(commentArray[i]+"\n")
            for lane in range(1,5,1):
                for wire in ['wireAB', 'wireBC', 'wireCA'] :
                    if i == 5:
                        #print offset[lane][wire]
                        #value =  offset[lane][wire] * 1000
                        value =  averagePolynomialDict[dataRate][lane][wire][i] * 1000
                    else:
                        value =  averagePolynomialDict[dataRate][lane][wire][i]
                    outFile.write("%0.10g," % value)
            outFile.write("\n")
    outFile.write("END SECTION\n")
'''
writeTransferFunctions.wantAllVarsGlobal = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 550.0
analogCapture1.laneList = laneList1
analogCapture1.lineRateSource = 'fromClockConfig'
analogCapture1.measurementMode = 'differential'
analogCapture1.numBitsDesired = 512
analogCapture1.patternLenSymbols = 8
analogCapture1.refLane = 1
analogCapture1.saveResults = True
analogCapture1.startVoltage = -550.0
analogCapture1.timeout = 120
analogCapture1.wantAnalysis = True
analogCapture1.wantEyeDiagrams = False
analogCapture1.wantResultImages = False
analogCapture1.wires = ['wireAB', 'wireBC', 'wireCA']

globalClockConfig.autoDetectClock = False
globalClockConfig.autoDetectTimeout = 2.0
globalClockConfig.dataRate = 2000.0
globalClockConfig.referenceClocks = refClocksConfig1

laneList1.equalizationAcGain = [(7, 7, 7)]
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 600.0

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

plotCreator3.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
wire = args[2]
dataDict = args[3]
polyDict = args[4]
plotTitle = args[5]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()
yVals1 = list()
yVals2 = list()
for targetLevel in sorted( dataDict[dataRate][lane][wire].keys() ) :
    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][wire][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane][wire],targetLevel)
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
plotA.setYLim([-700.0, 700.0])
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

refClocksConfig1.externRefClockFreq = 100.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.outputClockBFormat = 'LVDS'
refClocksConfig1.outputClockBFreq = 100.0
refClocksConfig1.systemRefClockSource = 'external'

resultFolderCreator1.channelProvider = laneList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

#! TEST PROCEDURE
import math
import numpy as np

coordinator1.setState("running")
iesp = IESP.getInstance()
globalClockConfig.setup()
failFlag = 0

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

iesp.disableValidation()
analogCapture1.startVoltage = -630
analogCapture1.endVoltage = 630

# Declare global dictionary of measured values
averageVoltageDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averageVoltageDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averageVoltageDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averageVoltageDict[dataRate][lane][wire] = dict()
            for targetLevel in sorted(calOptions.targetLevels) :
                averageVoltageDict[dataRate][lane][wire][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
averagePolynomialDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averagePolynomialDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averagePolynomialDict[dataRate][lane][wire] = [0.0,0.0,0.0,0.0,1.0,0.0]



# now perform loop

    # start generator
    myString = "mipiCphyGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(5000)

    # now measure
    for targetLevel in sorted(calOptions.targetLevels) :
        (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                #print averageVoltagePerLane[lane][wire]
                averageVoltageDict[dataRate][lane][wire][targetLevel] = averageVoltagePerLaneHigh[lane][wire]
                averageVoltageDict[dataRate][lane][wire][-targetLevel] = averageVoltagePerLaneLow[lane][wire]
                if ((averageVoltagePerLaneHigh[lane][wire] - averageVoltagePerLaneLow[lane][wire]) < 100) or math.isnan(averageVoltagePerLaneHigh[lane][wire]) or math.isnan(averageVoltagePerLaneLow[lane][wire]):
                    failFlag = 1
                    warningMsg("Bad Value on Lane %d wire %s..." % (lane, wire))

offset = dict()
for lane in range(1,5,1) :
    offset[lane] = dict()
    for wire in ['wireAB', 'wireBC', 'wireCA'] :
        offset[lane][wire] = 0

for lane in sorted(laneList1.lanes) :
    for wire in ['wireAB', 'wireBC', 'wireCA'] :
        if (abs(averageVoltagePerLaneHigh[lane][wire]) > abs(averageVoltagePerLaneLow[lane][wire])) or (averageVoltagePerLaneHigh[lane][wire] < 0):
            offset[lane][wire] = averageVoltagePerLaneHigh[lane][wire] - (averageVoltagePerLaneHigh[lane][wire] - averageVoltagePerLaneLow[lane][wire]) / 2
        else:
            offset[lane][wire] = averageVoltagePerLaneLow[lane][wire] + (averageVoltagePerLaneHigh[lane][wire] - averageVoltagePerLaneLow[lane][wire]) / 2

#levels is -300 to 300.
levels = list()
for targetLevel in sorted(calOptions.targetLevels) :
    levels.append(targetLevel)
    levels.append(-targetLevel)

# Generate Polynomials
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            xVals = sorted(levels)
           # print xVals
            yVals = list()
            for targetLevel in sorted(levels) :
                yVals.append(averageVoltageDict[dataRate][lane][wire][targetLevel])
            #print yVals
            polynomialValues = np.polyfit(xVals, yVals, 5)
            averagePolynomialDict[dataRate][lane][wire] = polynomialValues

generatePlots()
writeAverageVoltages()
writeTransferFunctions()
writeNoteForTestRun(calOptions.moduleName)

if failFlag == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Calibration Passed!', msg='Calibration Passed > Continue with validation', buttonLabels=['PLEASE CONTINUE WITH VALIDATION'], responseByButton=None, htmlUrl=myFileUrl, htmlSize="772x746", timeoutSecs=None, warnIfTimedOut=False)
elif failFlag:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Calibration Failed!', msg='Calibration Failed > Retry calibration', buttonLabels=['PLEASE RETRY CALIBRATION'], responseByButton=None, htmlUrl=myFileUrl, htmlSize="772x746", timeoutSecs=None, warnIfTimedOut=False)

print("****************************************")
print("****************************************")
print("****************************************")
print("Please rename result directory to "+calOptions.moduleName+".")
print("****************************************")
print("****************************************")
print("****************************************")


# finalize state with coordinator
coordinator1.setState("stopped")
# allow the generator time to detect state change and exit gracefully
sleepMillis(15000)
newFolderPath = resultFolderCreator1.run()
