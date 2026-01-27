# SVT Test
# SVT version 25.3.rc0
# Test saved 2025-08-04_1051
# Form factor: SV5C_4L8G_MIPI_CPHY_ANALYZER
# PY3
# Checksum: 14085c4a21f4de9abe649d099ec8f2d5
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
iso17025Report = _create('iso17025Report', 'SvtFunction', iespName=None)
plotCreator3 = _create('plotCreator3', 'SvtPlotCreator', iespName=None)
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName=None)

analogCapture1 = _create('analogCapture1', 'SvtMipiCphyAnalogCapture')
globalClockConfig = _create('globalClockConfig', 'SvtMipiClockConfig')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

calOptions.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[250.0], displayOrder=(0, 1.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 150.0, 200.0], displayOrder=(0, 2.0))
calOptions.addField('accuracyInPercent', descrip='''Accuracy specification for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=20.0, displayOrder=(0, 3.0))
calOptions.addField('accuracyInMv', descrip='''Accuracy specification for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=30.0, displayOrder=(0, 4.0))
calOptions.addField('acceptanceInPercent', descrip='''Acceptance limit (accuracy specification with guardband) for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=20.0, displayOrder=(0, 5.0))
calOptions.addField('acceptanceInMv', descrip='''Acceptance limit (accuracy specification with guradband) for ISO compliance testingm in mV.''', attrType=float, iespInstanceName='any', defaultVal=30.0, displayOrder=(0, 6.0))
calOptions.addField('measurementUncertaintyInMv', descrip='''Measurement uncertainty for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=12.0, displayOrder=(0, 7.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.dataRates = [200.0]
calOptions.targetLevels = [100.0, 150.0, 200.0]
calOptions.accuracyInPercent = 20.0
calOptions.accuracyInMv = 30.0
calOptions.acceptanceInPercent = 20.0
calOptions.acceptanceInMv = 30.0
calOptions.measurementUncertaintyInMv = 12.0
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


#print("HIGH", meanLocation)
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


#print("LOW", meanLocation)
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
generatePlots.code = r'''# generate average transfer functions for continuous mode
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            titleString = 'Average Transfer Function at %0.0f MHz, Lane %d, Wire %s\nContinuous Mode' % (dataRate,lane, wire)
            xValues = sorted(levels)
            yValues = list()
            for targetLevel in sorted(levels) :
                yValues.append(averageVoltageDict[dataRate][lane][wire][targetLevel])
            plotCreatorBasic1.xAxisLabel = "Input Voltage"
            plotCreatorBasic1.yAxisLabel = "Output Voltage"
            plotCreatorBasic1.yAxisLimits = [-400.0,400.0]
            plotCreatorBasic1.title = titleString
            plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots_continuous'
            plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            titleString = 'Average Transfer Function vs Fit, DR = %0.0f, Lane %d, wire %s\nContinuous Mode' % (dataRate,lane, wire)
            plotCreator3.run(lane, dataRate, wire, averageVoltageDict, averagePolynomialDict, titleString)

# generate average transfer functions for burst mode
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            titleString = 'Average Transfer Function at %0.0f MHz, Lane %d, Wire %s\nBurst Mode' % (dataRate,lane, wire)
            xValues = sorted(levels)
            yValues = list()
            for targetLevel in sorted(levels) :
                yValues.append(averageVoltageDict_burst[dataRate][lane][wire][targetLevel])
            plotCreatorBasic1.xAxisLabel = "Input Voltage"
            plotCreatorBasic1.yAxisLabel = "Output Voltage"
            plotCreatorBasic1.yAxisLimits = [-400.0,400.0]
            plotCreatorBasic1.title = titleString
            plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots_burst'
            plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            titleString = 'Average Transfer Function vs Fit, DR = %0.0f, Lane %d, wire %s\nBurst Mode' % (dataRate,lane, wire)
            plotCreator3.run(lane, dataRate, wire, averageVoltageDict_burst, averagePolynomialDict_burst, titleString)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude'
getMeasurementsAtAmplitude.code = r'''myString = "mipiCphyGenerator1.hsVoltageAmplitudesABC = [(%d, %d, %d)]" % ((abs(amplitude)),(abs(amplitude)),(abs(amplitude)))

coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiCphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(1000)

analogCapture1.resultName = "Lane_data_"+str(amplitude)+"mV"
result = analogCapture1.run()
lowVoltageForWire = dict()
highVoltageForWire = dict()
for lane in sorted(laneList1.lanes) :
    lowVoltageForWire[lane] = dict()
    highVoltageForWire[lane] = dict()
    for targetWire in ['wireAB', 'wireBC', 'wireCA'] :
        #print targetWire, lane
        #voltages = result.getAnalysis(lane, targetWire)['digitizedLevels']
        #print voltages
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

iso17025Report.args = ''
iso17025Report.code = r'''import os, time
failFlag = False
probableFailFlag = False
probablePassFlag = False

# create csv file output
filePathString = serialNumber+"_ISO_17025_Report.csv"
resultFolderCreator1.folderName = "ISO_17025_Report"

folderPath = resultFolderCreator1.run()
filePath = os.path.join(folderPath, filePathString)

with open(filePath, "w") as outFile:

    # Fill header section
    print("SV5C-CPRX HS Threshold Validation ISO 17025 Report", end=' ', file=outFile)
    print("", file=outFile)
    print("Test Date (Day/Month/Year): %s" % time.strftime("%d/%m/%y"), end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)
    print("Continuous Mode Data", end=' ', file=outFile)
    print("", file=outFile)
    print("Lane, Wire, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)
    print(" , , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # Write out the continuous mode data
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                for level in sorted(levels) :
                    print("Lane %i," % lane, end=' ', file=outFile)
                    print("%s," % wire, end=' ', file=outFile)
                    print("%0.1f," % dataRate, end=' ', file=outFile)
                    print("%0.1f," % level, end=' ', file=outFile)
                    print("%0.1f," % averageVoltageDict[dataRate][lane][wire][level], end=' ', file=outFile)
                    difference = averageVoltageDict[dataRate][lane][wire][level] - level
                    print("%0.1f," % difference, end=' ', file=outFile)
                    if (calOptions.accuracyInPercent * abs(level) / 100) > calOptions.accuracyInMv :
                        accuracySpec = calOptions.accuracyInPercent * abs(level) / 100
                    else :
                        accuracySpec = calOptions.accuracyInMv
                    print("%0.0f," % accuracySpec, end=' ', file=outFile)
                    if (calOptions.acceptanceInPercent * abs(level) / 100) > calOptions.acceptanceInMv :
                        acceptanceLimit = calOptions.acceptanceInPercent * abs(level) / 100
                    else :
                        acceptanceLimit = calOptions.acceptanceInMv
                    print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                    measurementUncertainty = calOptions.measurementUncertaintyInMv
                    print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                    # determine pass / fail of measurement
                    if (abs(difference) - measurementUncertainty) > accuracySpec :
                        print("Fail", end=' ', file=outFile)
                        failFlag = True
                        warningMsg("Bad Value on Lane %d %s...Target: %.2f Got: %.2f" % (lane, wire, level, averageVoltageDict[dataRate][lane][wire][level]))
                    elif abs(difference) > acceptanceLimit :
                        print("Fail *", end=' ', file=outFile)
                        probableFailFlag = True
                        warningMsg("Bad Value on Lane %d %s...Target: %.2f Got: %.2f" % (lane, wire, level, averageVoltageDict[dataRate][lane][wire][level]))

                    elif (abs(difference) + measurementUncertainty) > accuracySpec :
                        print("Pass *", end=' ', file=outFile)
                        probablePassFlag = True
                    elif abs(difference) < acceptanceLimit :
                        print("Pass", end=' ', file=outFile)

                    print("", file=outFile)


    print("", file=outFile)
    print("Burst Mode Data", end=' ', file=outFile)
    print("", file=outFile)
    print("Lane, Wire, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)
    print(" , , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # Write out the burst mode data
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                for level in sorted(levels) :
                    print("Lane %i," % lane, end=' ', file=outFile)
                    print("%s," % wire, end=' ', file=outFile)
                    print("%0.1f," % dataRate, end=' ', file=outFile)
                    print("%0.1f," % level, end=' ', file=outFile)
                    print("%0.1f," % averageVoltageDict_burst[dataRate][lane][wire][level], end=' ', file=outFile)
                    difference = averageVoltageDict_burst[dataRate][lane][wire][level] - level
                    print("%0.1f," % difference, end=' ', file=outFile)
                    if (calOptions.accuracyInPercent * abs(level) / 100) > calOptions.accuracyInMv :
                        accuracySpec = calOptions.accuracyInPercent * abs(level) / 100
                    else :
                        accuracySpec = calOptions.accuracyInMv
                    print("%0.0f," % accuracySpec, end=' ', file=outFile)
                    if (calOptions.acceptanceInPercent * abs(level) / 100) > calOptions.acceptanceInMv :
                        acceptanceLimit = calOptions.acceptanceInPercent * abs(level) / 100
                    else :
                        acceptanceLimit = calOptions.acceptanceInMv
                    print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                    measurementUncertainty = calOptions.measurementUncertaintyInMv
                    print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                    # determine pass / fail of measurement
                    if (abs(difference) - measurementUncertainty) > accuracySpec :
                        print("Fail", end=' ', file=outFile)
                        failFlag = True
                        warningMsg("Bad Value on Lane %d %s...Target: %.2f Got: %.2f" % (lane, wire, level, averageVoltageDict_burst[dataRate][lane][wire][level]))
                    elif abs(difference) > acceptanceLimit :
                        print("Fail *", end=' ', file=outFile)
                        probableFailFlag = True
                        warningMsg("Bad Value on Lane %d %s...Target: %.2f Got: %.2f" % (lane, wire, level, averageVoltageDict_burst[dataRate][lane][wire][level]))

                    elif (abs(difference) + measurementUncertainty) > accuracySpec :
                        print("Pass *", end=' ', file=outFile)
                        probablePassFlag = True
                    elif abs(difference) < acceptanceLimit :
                        print("Pass", end=' ', file=outFile)

                    print("", file=outFile)

    print("", file=outFile)
    print("Test status definitions:", end=' ', file=outFile)
    print("", file=outFile)

    print("Pass - The measured value was observed within the acceptance limits and the measurement uncertainty interval was within the specification range.", end=' ', file=outFile)
    print("", file=outFile)

    print("Pass * - The measured value was observed within the acceptance limits but part of the measurement uncertainty interval extended beyond the specification range.", end=' ', file=outFile)
    print("", file=outFile)

    print("Fail * - The measured value was observed outside the acceptance limits but part of the measurement uncertainty interval extended within the specification range.", end=' ', file=outFile)
    print("", file=outFile)

    print("Fail - The measured value was observed outside the acceptance limits and the measurement uncertainty interval of was entirely outside the specification range.", end=' ', file=outFile)
    print("", file=outFile)

    print("", file=outFile)
    print("SV5C-CPRX module number %s: " % serialNumber, end=' ', file=outFile)
    print("", file=outFile)
    print("HS threshold validation final status: ", end=' ', file=outFile)
    if failFlag :
        print("Fail", end=' ', file=outFile)
    elif probableFailFlag :
        print("Probable Fail", end=' ', file=outFile)
    elif probablePassFlag :
        print("Probable Pass", end=' ', file=outFile)
    else :
        print("Pass", end=' ', file=outFile)
    print("", file=outFile)

return (failFlag, probableFailFlag)
'''
iso17025Report.wantAllVarsGlobal = False

writeAverageVoltages.args = ''
writeAverageVoltages.code = r'''import os

# create csv file output
stringAppendix = ".csv"
filePathString = "AverageVoltageMeasurements_continuous" + stringAppendix
resultFolderCreator1.folderName = "AverageVoltageMeasurements_continuous"
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

# create csv file output
stringAppendix = ".csv"
filePathString = "AverageVoltageMeasurements_burst" + stringAppendix
resultFolderCreator1.folderName = "AverageVoltageMeasurements_burst"
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
                    print( "%0.4g," % averageVoltageDict_burst[dataRate][lane][wire][level],file=outFile)
                print( "",file=outFile)
'''
writeAverageVoltages.wantAllVarsGlobal = False

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
plotA.setYLim([-400.0, 400.0])
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

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 210.0
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
analogCapture1.startVoltage = -210.0
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


coordinator1.setState("running")
iesp = IESP.getInstance()
globalClockConfig.setup()
failFlag = 0

# Declare global dictionary of measured values in continuous mode
averageVoltageDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averageVoltageDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averageVoltageDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averageVoltageDict[dataRate][lane][wire] = dict()
            for targetLevel in sorted(calOptions.targetLevels) :
                averageVoltageDict[dataRate][lane][wire][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials in continuous mode
averagePolynomialDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(1,5,1) :
        averagePolynomialDict[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averagePolynomialDict[dataRate][lane][wire] = [0.0,0.0,0.0,0.0,1.0,0.0]

# Declare global dictionary of measured values in burst mode
averageVoltageDict_burst = dict()
for dataRate in sorted(calOptions.dataRates) :
    averageVoltageDict_burst[dataRate] = dict()
    for lane in range(1,5,1) :
        averageVoltageDict_burst[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averageVoltageDict_burst[dataRate][lane][wire] = dict()
            for targetLevel in sorted(calOptions.targetLevels) :
                averageVoltageDict_burst[dataRate][lane][wire][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials burst mode
averagePolynomialDict_burst = dict()
for dataRate in sorted(calOptions.dataRates) :
    averagePolynomialDict_burst[dataRate] = dict()
    for lane in range(1,5,1) :
        averagePolynomialDict_burst[dataRate][lane] = dict()
        for wire in ['wireAB', 'wireBC', 'wireCA'] :
            averagePolynomialDict_burst[dataRate][lane][wire] = [0.0,0.0,0.0,0.0,1.0,0.0]

# now perform loop
for dataRate in sorted(calOptions.dataRates) :
    # start generator for continuous captures
    myString = "mipiCphyGenerator1.pattern = 'CPHY_hsOnly333'"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    myString = "mipiCphyGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(5000)

    # now measure
    for targetLevel in sorted(calOptions.targetLevels) :
        (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                #print averageVoltagePerLane[lane][wire]
                acceptance_mV = calOptions.acceptanceInMv
                if abs((calOptions.acceptanceInPercent/100.0)*targetLevel) > acceptance_mV:
                    acceptance_mV = abs((calOptions.acceptanceInPercent/100.0)*targetLevel)

                error_in_mV_high = abs(averageVoltagePerLaneHigh[lane][wire]-targetLevel)
                error_in_mV_low = abs(averageVoltagePerLaneLow[lane][wire]+targetLevel)

                if error_in_mV_high>acceptance_mV or error_in_mV_low>acceptance_mV:
                    failFlag = 1
                    print("Found failing condition on lane %d, %s, at level %.1f in continuous mode."%(lane,wire,targetLevel))
                averageVoltageDict[dataRate][lane][wire][targetLevel] = averageVoltagePerLaneHigh[lane][wire]
                averageVoltageDict[dataRate][lane][wire][-targetLevel] = averageVoltagePerLaneLow[lane][wire]

for dataRate in sorted(calOptions.dataRates) :
    # start generator for burst captures
    myString = "mipiCphyGenerator1.pattern = 'cphyCustomPattern1'"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    myString = "mipiCphyGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(5000)

    analogCapture1.captureMode = 'burst'
    analogCapture1.triggerType = 'allBursts'
    analogCapture1.numBitsDesired = 2048
    # now measure
    for targetLevel in sorted(calOptions.targetLevels) :
        (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
        for lane in sorted(laneList1.lanes) :
            for wire in ['wireAB', 'wireBC', 'wireCA'] :
                #print averageVoltagePerLane[lane][wire]
                acceptance_mV = calOptions.acceptanceInMv
                if abs((calOptions.acceptanceInPercent/100.0)*targetLevel) > acceptance_mV:
                    acceptance_mV = abs((calOptions.acceptanceInPercent/100.0)*targetLevel)

                error_in_mV_high = abs(averageVoltagePerLaneHigh[lane][wire]-targetLevel)
                error_in_mV_low = abs(averageVoltagePerLaneLow[lane][wire]+targetLevel)

                if error_in_mV_high>acceptance_mV or error_in_mV_low>acceptance_mV:
                    failFlag = 1
                    print("Found failing condition on lane %d, %s, at level %.1f in burst mode."%(lane,wire,targetLevel))
                averageVoltageDict_burst[dataRate][lane][wire][targetLevel] = averageVoltagePerLaneHigh[lane][wire]
                averageVoltageDict_burst[dataRate][lane][wire][-targetLevel] = averageVoltagePerLaneLow[lane][wire]


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
            yVals_1 = list()
            yVals_2 = list()
            for targetLevel in sorted(levels) :
                yVals_1.append(averageVoltageDict[dataRate][lane][wire][targetLevel])
                yVals_2.append(averageVoltageDict_burst[dataRate][lane][wire][targetLevel])
            #print yVals
            polynomialValues_1 = np.polyfit(xVals, yVals_1, 5)
            averagePolynomialDict[dataRate][lane][wire] = polynomialValues_1

            polynomialValues_2 = np.polyfit(xVals, yVals_2, 5)
            averagePolynomialDict_burst[dataRate][lane][wire] = polynomialValues_2

generatePlots()
writeAverageVoltages()
writeNoteForTestRun(serialNumber)
(failFlag, probableFailFlag) = iso17025Report()
if failFlag == False and probableFailFlag == False:
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)
    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)

else:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
# finalize state with coordinator
coordinator1.setState("stopped")
# allow the generator time to detect state change and exit gracefully
sleepMillis(15000)
