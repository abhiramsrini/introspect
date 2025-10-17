# SVT Test
# SVT version 23.3.0
# Test saved 2023-09-20_0934
# Form factor: SV3C_4L3G_MIPI_DPHY_ANALYZER2
# PY3
# Checksum: df513dab15aea2b6a6cbc74811f8e414
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
computeHighVoltage = _create('computeHighVoltage', 'SvtFunction', iespName='None')
computeLowVoltage = _create('computeLowVoltage', 'SvtFunction', iespName='None')
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
generatePlots = _create('generatePlots', 'SvtFunction', iespName='None')
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName='None')
iso17025Report = _create('iso17025Report', 'SvtFunction', iespName='None')
iso17025ReportTemp = _create('iso17025ReportTemp', 'SvtFunction', iespName='None')
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName='None')

analogCapture1 = _create('analogCapture1', 'SvtMipiDphyAnalogCapture')
globalClockConfig = _create('globalClockConfig', 'SvtMipiClockConfig')
laneList1 = _create('laneList1', 'SvtMipiDphyLaneList')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
plotCreator3 = _create('plotCreator3', 'SvtPlotCreator')
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

calOptions.addField('moduleName', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[1000.0, 1500.0, 2000.0, 2500.0, 3125.0], displayOrder=(0, 2.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 125.0, 150.0, 175.0, 200.0], displayOrder=(0, 3.0))
calOptions.addField('accuracyInPercent', descrip='''Accuracy specification for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=15.0, displayOrder=(0, 4.0))
calOptions.addField('accuracyInMv', descrip='''Accuracy specification for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=25.0, displayOrder=(0, 5.0))
calOptions.addField('acceptanceInPercent', descrip='''Acceptance limit (accuracy specification with guardband) for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=15.0, displayOrder=(0, 6.0))
calOptions.addField('acceptanceInMv', descrip='''Acceptance limit (accuracy specification with guradband) for ISO compliance testingm in mV.''', attrType=float, iespInstanceName='any', defaultVal=25.0, displayOrder=(0, 7.0))
calOptions.addField('measurementUncertaintyInMv', descrip='''Measurement uncertainty for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=12.0, displayOrder=(0, 8.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.moduleName = '1234'
calOptions.dataRates = [1000.0, 1500.0, 2000.0, 2500.0, 3125.0]
calOptions.targetLevels = [100.0, 125.0, 150.0, 175.0, 200.0]
calOptions.accuracyInPercent = 15.0
calOptions.accuracyInMv = 25.0
calOptions.acceptanceInPercent = 15.0
calOptions.acceptanceInMv = 25.0
calOptions.measurementUncertaintyInMv = 12.0
calOptions.callCustomInitMethod()
computeHighVoltage.args = 'voltages'
computeHighVoltage.code = r'''dig = dftList.digitizeData(voltages[500:8000], 0)
up = dftList.findDigitalTransitions(dig)[0]
#print(up)
down = dftList.findDigitalTransitions(dig)[1]
#print(down)


startLow = up[0] + 15 + 500
if down[0] > up[0]:
    endLow = down[0] -15 + 500
else:
    endLow = down[1] -15 + 500

#print(voltages)
#print(startLow)
#print(endLow)
#print(voltages[startLow:endLow])

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)


print("HIGH", meanLocation)
return meanLocation
'''
computeHighVoltage.wantAllVarsGlobal = False

computeLowVoltage.args = 'voltages'
computeLowVoltage.code = r'''dig = dftList.digitizeData(voltages[500:8000], -100)
up = dftList.findDigitalTransitions(dig)[0]
#print(up)
down = dftList.findDigitalTransitions(dig)[1]
#print(down)
startLow = down[0] + 15 + 500
if down[0] < up[0]:
    endLow = up[0] -15 + 500
else:
    endLow = up[1] -15 + 500
#print(voltages)
#print(startLow)
#print(endLow)

#print (voltages[startLow:endLow])

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)


print("LOW", meanLocation)
return meanLocation
'''
computeLowVoltage.wantAllVarsGlobal = False

coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = '127.0.0.1'
coordinator1.serverPort = 12013

generatePlots.args = ''
generatePlots.code = r'''# generate average transfer functions
for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        titleString = 'Average Transfer Function at %0.0f MHz, Lane %d' % (dataRate,lane)
        xValues = sorted(levels)
        yValues = list()
        for targetLevel in sorted(levels) :
            yValues.append(averageVoltageDict[dataRate][lane][targetLevel])
        plotCreatorBasic1.xAxisLabel = "Input Voltage"
        plotCreatorBasic1.yAxisLabel = "Output Voltage"
        plotCreatorBasic1.yAxisLimits = [-800.0,800.0]
        plotCreatorBasic1.title = titleString
        plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots'
        plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calOptions.dataRates) :
    for lane in sorted(laneList1.lanes) :
        titleString = 'Average Transfer Function vs Fit, DR = %0.0f, Lane %d' % (dataRate,lane)
        plotCreator3.run(lane, dataRate, averageVoltageDict, averagePolynomialDict, titleString)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude'
getMeasurementsAtAmplitude.code = r'''print(amplitude)
# set lane 1 to "DATA 1" mode (normal operation)

iesp.setMipiCaptureClockSelect(0)

myString = "mipiDphyGenerator1.hsDataVoltageAmplitudes = [%d]" % abs(amplitude)
coordinator1.waitForCodeToBeRun("Generator",myString)

myString = "mipiDphyGenerator1.hsClockVoltageAmplitude = %d" % abs(amplitude)
coordinator1.waitForCodeToBeRun("Generator",myString)

myString = "dphyCustomPattern1.hsBytes = 255"
coordinator1.waitForCodeToBeRun("Generator",myString)

myString = "mipiDphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(10000)

results = analogCapture1.run()

averageVoltageForLaneHigh = dict()
for lane in sorted(laneList1.lanes) :
    averageVoltageForLaneHigh[lane] = dict()
    voltages = results.getVoltages(lane)
    #print(len(voltages))

    averageVoltageForLaneHigh[lane] = np.mean(voltages[500:8000])

myString = "dphyCustomPattern1.hsBytes = 0"
coordinator1.waitForCodeToBeRun("Generator",myString)

myString = "mipiDphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)

results = analogCapture1.run()
averageVoltageForLaneLow = dict()
for lane in sorted(laneList1.lanes) :
    averageVoltageForLaneLow[lane] = dict()
    voltages = results.getVoltages(lane)
    averageVoltageForLaneLow[lane] = np.mean(voltages[500:8000])

laneList1.lanes = [1]
#set lane 1 to "CLK" mode (special mode for CLK analog capture)
iesp.setMipiCaptureClockSelect(1)

myString = "mipiDphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(3000)
result = analogCapture1.run()

voltages = result.getVoltages(1)

averageVoltageForLaneLow[5] = computeLowVoltage(voltages)
averageVoltageForLaneHigh[5] = computeHighVoltage(voltages)

# set lane 1 to "DATA 1" mode (normal operation)
iesp.setMipiCaptureClockSelect(0)
laneList1.lanes = [1,2,3,4]

return (averageVoltageForLaneHigh, averageVoltageForLaneLow)
'''
getMeasurementsAtAmplitude.wantAllVarsGlobal = False

iso17025Report.args = ''
iso17025Report.code = r'''import os, time
failFlag = False
probableFailFlag = False
probablePassFlag = False

# create csv file output
filePathString = calOptions.moduleName+"_ISO_17025_Report.csv"
resultFolderCreator1.folderName = "ISO_17025_Report"

folderPath = resultFolderCreator1.run()
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:

    # Fill header section
    print("SV3C-DPRX HS Threshold Validation ISO 17025 Report", end=' ', file=outFile)
    print("", file=outFile)
    print("Test Date (Day/Month/Year): %s" % time.strftime("%d/%m/%y"), end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    print("Lane, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)

    print(" , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # now fill in the arrays for lanes
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for level in sorted(levels) :
                print("Lane %i," % lane, end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
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
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        # now fill in the arrays for clock
        for lane in [5] : # clock lane
            for level in sorted(levels) :
                print("Clock,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
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
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
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
    print("SV3C-DPRX module number %s: " % calOptions.moduleName, end=' ', file=outFile)
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
'''
iso17025Report.wantAllVarsGlobal = False

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
    print("dataRates,", end=' ', file=outFile)
    for dataRate in sorted(calOptions.dataRates) :
        print("%0.1f," % dataRate, end=' ', file=outFile)
    print("", file=outFile)

    print("lanes,", end=' ', file=outFile)
    for lane in sorted(laneList1.lanes) :
        print("%d," % lane, end=' ', file=outFile)
    print("", file=outFile)

    # End the header section with the keyword Voltages
    print("Voltages", file=outFile)

    # now fill in the arrays
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            commentString = "# Data Rate = %0.0f, Lane = %d" % (dataRate, lane)
            print(commentString, file=outFile)

            # Output target levels
            print("Target,", end=' ', file=outFile)
            for level in sorted(levels) :
                print("%0.0f," % level, end=' ', file=outFile)
            print("", file=outFile)

            # Output measured levels
            print("Measured,", end=' ', file=outFile)
            for level in sorted(levels) :
                print("%0.4g," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
            print("", file=outFile)

    for dataRate in sorted(calOptions.dataRates) :
        commentString = "# Data Rate = %0.0f, CLK" % (dataRate)
        print(commentString, file=outFile)

        # Output target levels
        print("Target,", end=' ', file=outFile)
        for level in sorted(levels) :
            print("%0.0f," % level, end=' ', file=outFile)
        print("", file=outFile)

        # Output measured levels
        print("Measured,", end=' ', file=outFile)
        for level in sorted(levels) :
            print("%0.4g," % averageVoltageDict[dataRate][5][level], end=' ', file=outFile)
        print("", file=outFile)
'''
writeAverageVoltages.wantAllVarsGlobal = False

iso17025ReportTemp.args = ''
iso17025ReportTemp.code = r'''import os, time
failFlag = False
probableFailFlag = False
probablePassFlag = False

# create csv file output
filePathString = calOptions.moduleName+"_ISO_17025_ReportTemp.csv"
resultFolderCreator1.folderName = "ISO_17025_ReportTemp"

folderPath = resultFolderCreator1.run()
filePath = os.path.join(folderPath, filePathString)
with open(filePath, "w") as outFile:

    # Fill header section
    print("SV3C-DPRX HS Threshold Validation ISO 17025 Report", end=' ', file=outFile)
    print("", file=outFile)
    print("Test Date (Day/Month/Year): %s" % time.strftime("%d/%m/%y"), end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    print("Lane, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)

    print(" , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # now fill in the arrays for lanes
    for dataRate in sorted(calOptions.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for level in sorted(levels) :
                print("Lane %i," % lane, end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
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
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        # now fill in the arrays for clock
        for lane in [5] : # clock lane
            for level in sorted(levels) :
                print("Clock,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
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
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
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
    print("SV3C-DPRX module number %s: " % calOptions.moduleName, end=' ', file=outFile)
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
'''
iso17025ReportTemp.wantAllVarsGlobal = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 300.0
analogCapture1.laneList = laneList1
analogCapture1.lineRateSource = 'fromClockConfig'
analogCapture1.measurementMode = 'differential'
analogCapture1.minLpDurationForStart = 500
analogCapture1.nthBurst = 1
analogCapture1.numBitsDesired = 64
analogCapture1.patternLenBits = 64
analogCapture1.refLane = 1
analogCapture1.riseTimeMode = 'RT_None'
analogCapture1.saveResults = True
analogCapture1.startVoltage = -300.0
analogCapture1.timeout = 60
analogCapture1.triggerType = 'allBursts'
analogCapture1.wantAnalysis = True
analogCapture1.wantEyeDiagrams = False
analogCapture1.wantResultImages = False

globalClockConfig.autoDetectClock = False
globalClockConfig.autoDetectTimeout = 2.0
globalClockConfig.continuousClock = False
globalClockConfig.dataRate = 1500.0
globalClockConfig.referenceClocks = refClocksConfig

laneList1.clockEqualizationDcGain = 0
laneList1.dataEqualizationDcGains = [0]
laneList1.hsClockThresholdVoltage = 50.0
laneList1.hsDataThresholdVoltages = [50.0]
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpClockThresholdVoltage = 600.0
laneList1.lpDataThresholdVoltages = [600.0]

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

plotCreator3.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
dataDict = args[2]
polyDict = args[3]
plotTitle = args[4]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()
yVals1 = list()
yVals2 = list()
for targetLevel in sorted( dataDict[dataRate][lane].keys() ) :
    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane],targetLevel)
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

refClocksConfig.externRefClockFreq = 100.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'external'

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

globalClockConfig.setup()

coordinator1.setState("running")
failFlag = 0
iesp = getIespInstance()
globalClockConfig.setup()

# ------------ print HW and FW informations
myString = "genFormFactor = iesp.__class__.__name__"
res = coordinator1.waitForCodeToBeRun("Generator",myString)
formFactor  = res[1]['genFormFactor']
print('TX: ' + formFactor)

printMsg("Serial Number: %s" % iesp.getModuleSerialNums(), 'yellow', None, True)
printMsg('Firmware Id: %s' % iesp.getFirmwareIdsFromConnection()[0], 'yellow', None, True)
printMsg("Firmware revision: %s" % iesp.getFirmwareRevisions(), 'yellow', None, True)
printMsg("Hardware revision: %s" % iesp.getHardwareRevs(), 'yellow', None, True)
# ----------------------------

# Declare global dictionary of measured values
averageVoltageDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averageVoltageDict[dataRate] = dict()
    for lane in range(6) :
        averageVoltageDict[dataRate][lane] = dict()
        for targetLevel in sorted(calOptions.targetLevels) :
            averageVoltageDict[dataRate][lane][targetLevel] = 0.0
            averageVoltageDict[dataRate][lane][-targetLevel] = 0.0
offset = dict()
for lane in range(6) :
    offset[lane] = 0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
averagePolynomialDict = dict()
for dataRate in sorted(calOptions.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(6) :
        averagePolynomialDict[dataRate][lane] = dict()
        averagePolynomialDict[dataRate][lane] = [0.0,0.0,0.0,0.0,1.0,0.0]



# now perform loop
# start generator
myString = "mipiDphyGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(5000)

# now measure
for dataRate in sorted(calOptions.dataRates) :

    for targetLevel in sorted(calOptions.targetLevels) :
        (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
        for lane in sorted(laneList1.lanes) :
            averageVoltageDict[dataRate][lane][targetLevel] = averageVoltagePerLaneHigh[lane]
            averageVoltageDict[dataRate][lane][-targetLevel] = averageVoltagePerLaneLow[lane]
            if ((averageVoltagePerLaneHigh[lane] > targetLevel + targetLevel*0.15 or averageVoltagePerLaneHigh[lane] < targetLevel - targetLevel*0.15  ) or math.isnan(averageVoltagePerLaneHigh[lane])):
                failFlag = 1
                warningMsg("Bad Value on Lane %d..." % lane)
                print(averageVoltagePerLaneHigh[lane])
                print(targetLevel)
            if ((averageVoltagePerLaneLow[lane] > -targetLevel + targetLevel*0.15 or averageVoltagePerLaneLow[lane] < -targetLevel - targetLevel*0.15  ) or math.isnan(averageVoltagePerLaneLow[lane])):
                failFlag = 1
                warningMsg("Bad Value on Lane %d..." % lane)
                print(averageVoltagePerLaneLow[lane])
                print(targetLevel)
        averageVoltageDict[dataRate][5][targetLevel] = averageVoltagePerLaneHigh[5]
        averageVoltageDict[dataRate][5][-targetLevel] = averageVoltagePerLaneLow[5]
        if ((averageVoltagePerLaneHigh[5] > targetLevel + targetLevel*0.15 or averageVoltagePerLaneHigh[5] < targetLevel - targetLevel*0.15  ) or math.isnan(averageVoltagePerLaneHigh[5])):
            failFlag = 1
            warningMsg("Bad Value on Lane 5...")
            print(averageVoltagePerLaneHigh[5])
            print(targetLevel)
        if ((averageVoltagePerLaneLow[5] > -targetLevel + targetLevel*0.15 or averageVoltagePerLaneLow[5] < -targetLevel - targetLevel*0.15  ) or math.isnan(averageVoltagePerLaneLow[5])):
            failFlag = 1
            warningMsg("Bad Value on Lane 5...")
            print(averageVoltagePerLaneLow[5])
            print(targetLevel)

    lanes = sorted(laneList1.lanes)
    lanes.append(5)

    levels = list()
    for targetLevel in sorted(calOptions.targetLevels) :
        levels.append(targetLevel)
        levels.append(-targetLevel)
    iso17025ReportTemp()
    
"""
# Generate Polynomials
for dataRate in sorted(calOptions.dataRates) :
    for lane in range(1,6,1):
        xVals = sorted(levels)
       # print xVals
        yVals = list()
        for targetLevel in sorted(levels) :
            yVals.append(averageVoltageDict[dataRate][lane][targetLevel])
        #print yVals
        polynomialValues = polyfit(xVals, yVals, 5)
        averagePolynomialDict[dataRate][lane] = polynomialValues

generatePlots()
writeAverageVoltages()
if failFlag == 0:
    writeNoteForTestRun("Pass")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL")
"""
iso17025Report()

print("****************************************")
print("****************************************")
print("****************************************")
print("Please rename result directory to "+calOptions.moduleName+".")
print("****************************************")
print("****************************************")
print("****************************************")

if failFlag == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, htmlUrl=myFileUrl, htmlSize="772x746", timeoutSecs=None, warnIfTimedOut=False)
elif failFlag:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, htmlUrl=myFileUrl, htmlSize="772x746", timeoutSecs=None, warnIfTimedOut=False)



# finalize state with coordinator
coordinator1.setState("stopped")
# allow the generator time to detect state change and exit gracefully
sleepMillis(15000)
