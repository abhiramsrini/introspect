# SVT Test
# SVT version 25.1.b4
# Test saved 2024-12-10_1126
# Form factor: SV5C_4L8G_MIPI_DPHY_ANALYZER
# PY3
# Checksum: 1af7a9d6c2607626a6990d523dcd9b4f
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calParams = _create('calParams', 'SvtDataRecord', iespName=None)
computeHighVoltage = _create('computeHighVoltage', 'SvtFunction', iespName=None)
computeLowVoltage = _create('computeLowVoltage', 'SvtFunction', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
generatePlots = _create('generatePlots', 'SvtFunction', iespName=None)
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName=None)
iso17025Report = _create('iso17025Report', 'SvtFunction', iespName=None)
runValidation = _create('runValidation', 'SvtFunction', iespName=None)

analogCapture1 = _create('analogCapture1', 'SvtMipiDphyAnalogCapture')
laneList1 = _create('laneList1', 'SvtMipiDphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
plotCreator1 = _create('plotCreator1', 'SvtPlotCreator')
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

calParams.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[200.0], displayOrder=(0, 1.0))
calParams.addField('targetLevels', descrip='''List of RX threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 150.0, 200.0], displayOrder=(0, 2.0))
calParams.addField('accuracyInPercent', descrip='''Accuracy specification for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=15.0, displayOrder=(0, 3.0))
calParams.addField('accuracyInMv', descrip='''Accuracy specification for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=30.0, displayOrder=(0, 4.0))
calParams.addField('acceptanceInPercent', descrip='''Acceptance limit (accuracy specification with guardband) for ISO compliance testing, in percent.''', attrType=float, iespInstanceName='any', defaultVal=15.0, displayOrder=(0, 5.0))
calParams.addField('acceptanceInMv', descrip='''Acceptance limit (accuracy specification with guradband) for ISO compliance testingm in mV.''', attrType=float, iespInstanceName='any', defaultVal=30.0, displayOrder=(0, 6.0))
calParams.addField('measurementUncertaintyInMv', descrip='''Measurement uncertainty for ISO compliance testing, in mV.''', attrType=float, iespInstanceName='any', defaultVal=12.0, displayOrder=(0, 7.0))
calParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calParams.dataRates = [200.0]
calParams.targetLevels = [100.0, 150.0, 175.0, 200.0]
calParams.accuracyInPercent = 15.0
calParams.accuracyInMv = 30.0
calParams.acceptanceInPercent = 15.0
calParams.acceptanceInMv = 30.0
calParams.measurementUncertaintyInMv = 12.0
calParams.callCustomInitMethod()
computeHighVoltage.args = 'voltages'
computeHighVoltage.code = r'''dig = dftList.digitizeData(voltages[500:8000], 0)
up = dftList.findDigitalTransitions(dig)[0]
down = dftList.findDigitalTransitions(dig)[1]

startLow = up[0] + 15 + 500
if down[0] > up[0]:
    endLow = down[0] -15 + 500
else:
    endLow = down[1] -15 + 500

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)

print("HIGH", meanLocation)
return meanLocation
'''
computeHighVoltage.wantAllVarsGlobal = False

computeLowVoltage.args = 'voltages'
computeLowVoltage.code = r'''dig = dftList.digitizeData(voltages[500:8000], 0)
up = dftList.findDigitalTransitions(dig)[0]
down = dftList.findDigitalTransitions(dig)[1]

startLow = down[0] + 15 + 500
if down[0] < up[0]:
    endLow = up[0] -15 + 500
else:
    endLow = up[1] -15 + 500

myLowArray = voltages[startLow:endLow]
meanLocation = np.mean(myLowArray)

print("LOW", meanLocation)
return meanLocation
'''
computeLowVoltage.wantAllVarsGlobal = False

coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

generatePlots.args = 'levels, averageVoltageDict, averagePolynomialDict,mode'
generatePlots.code = r'''# generate average transfer functions
for dataRate in sorted(calParams.dataRates) :
    for lane in sorted([1,2,3,4,5,6]) :
        titleString = 'Average Transfer Function at %0.0f MHz, Lane %d\n%s' % (dataRate,lane,mode)
        xValues = sorted(levels)
        yValues = list()
        for targetLevel in sorted(levels) :
            yValues.append(averageVoltageDict[dataRate][lane][targetLevel])
        plotCreatorBasic1.xAxisLabel = "Input Voltage"
        plotCreatorBasic1.yAxisLabel = "Output Voltage"
        plotCreatorBasic1.yAxisLimits = [-200.0,200.0]
        plotCreatorBasic1.title = titleString
        plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots_'+str(mode)
        plotCreatorBasic1.run(xValues, yValues)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude'
getMeasurementsAtAmplitude.code = r'''print(' ')
print('Amplitude:', amplitude)

print('=== Analog capture for the Data')
# set lane 1 to "DATA 1" mode (normal operation)
iesp.setMipiCaptureClockSelect(0)

myString = "customPattern1.hsBytes = [170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170]"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.hsDataVoltageAmplitudes = [%d]" % abs(amplitude)
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.hsClockVoltageAmplitude = %d" % abs(amplitude)
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "print('customPattern1.hsBytes =', customPattern1.hsBytes)"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "print('hsDataVoltageAmplitudes:', mipiGenerator1.hsDataVoltageAmplitudes)"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "print('hsClockVoltageAmplitude:', mipiGenerator1.hsClockVoltageAmplitude)"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(10000)

analogCapture1.resultName = "dataLane_capture_"+str(amplitude)+"mV"
result = analogCapture1.run()
print('--> analogCapture Result: ', result.getResultFolderPath().split('\\')[-1])
averageVoltageForLaneHigh = dict()
averageVoltageForLaneLow = dict()

laneList1.lanes = [1,2,3,4]

for lane in [1,2,3,4] :
    averageVoltageForLaneHigh[lane] = dict()
    averageVoltageForLaneLow[lane] = dict()

    voltages = result.getVoltages(lane)
    averageVoltageForLaneHigh[lane] = result.getAnalysis(lane)['digitizedLevels'][1]
    averageVoltageForLaneLow[lane] = result.getAnalysis(lane)['digitizedLevels'][0]
    print('Lane %d: Average Voltage=%.2f' % (lane, averageVoltageForLaneLow[lane]))
    print('Lane %d: Average Voltage=%.2f' % (lane, averageVoltageForLaneHigh[lane]))

# ------------------------------------------------
numberOfMaxTrials = 10
laneList1.lanes = [1]
#set lane 1 to "CLK" mode (special mode for CLK analog capture)
iesp.writeSubPartRegister(0x0C22, 0x00, 0x01)

for trial in range(numberOfMaxTrials):
    print('=== Trial %d: Analog capture for Clock1' % trial)
    myString = "mipiGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(10000)

    analogCapture1.resultName = "clock1_capture_"+str(amplitude)+"mV"
    result = analogCapture1.run()
    print('--> analogCapture Result: ', result.getResultFolderPath().split('\\')[-1])
    voltages = result.getVoltages(1)

    averageVoltageForLaneLow[5] = result.getAnalysis(1)['digitizedLevels'][0]
    averageVoltageForLaneHigh[5] = result.getAnalysis(1)['digitizedLevels'][1]

    if not math.isnan(averageVoltageForLaneLow[5]) and not math.isnan(averageVoltageForLaneHigh[5]):
        break

iesp.writeSubPartRegister(0x0C22, 0x00, 0x02)

for trial in range(numberOfMaxTrials):
    print('=== Trial %d: Analog capture for Clock2' % trial)
    myString = "mipiGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(10000)
    analogCapture1.resultName = "clock2_capture_"+str(amplitude)+"mV"
    result = analogCapture1.run()
    print('--> analogCapture Result: ', result.getResultFolderPath().split('\\')[-1])
    voltages = result.getVoltages(1)

    averageVoltageForLaneLow[6] = result.getAnalysis(1)['digitizedLevels'][0]
    averageVoltageForLaneHigh[6] = result.getAnalysis(1)['digitizedLevels'][1]

    if not math.isnan(averageVoltageForLaneLow[6]) and not math.isnan(averageVoltageForLaneHigh[6]):
        break
# set lane 1 to "DATA 1" mode (normal operation)
iesp.setMipiCaptureClockSelect(0)
laneList1.lanes = [1,2,3,4]

return (averageVoltageForLaneHigh, averageVoltageForLaneLow)
'''
getMeasurementsAtAmplitude.wantAllVarsGlobal = False

iso17025Report.args = 'levels, averageVoltageDict, averageVoltageDict_burst'
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
    print("SV5C-DPRX HS Threshold Validation ISO 17025 Report", end=' ', file=outFile)
    print("", file=outFile)
    print("Test Date (Day/Month/Year): %s" % time.strftime("%d/%m/%y"), end=' ', file=outFile)
    print("", file=outFile)
    print("Continuous Data", file=outFile)
    print("", file=outFile)

    print("Lane, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)

    print(" , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # now fill in the arrays for lanes
    for dataRate in sorted(calParams.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for level in sorted(levels) :
                print("Lane %i," % lane, end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Lane %d...Target: %.2f Got: %.2f" % (lane, level, averageVoltageDict[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Lane %d...Target: %.2f Got: %.2f" % (lane, level, averageVoltageDict[dataRate][lane][level]))
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        # now fill in the arrays for clock
        for lane in [5] : # clock lane
            for level in sorted(levels) :
                print("Clock 1,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict[dataRate][lane][level]))
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        for lane in [6] : # clock lane
            for level in sorted(levels) :
                print("Clock 2,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict[dataRate][lane][level]))
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

    print("", file=outFile)
    print("Burst Data", file=outFile)
    print("", file=outFile)

    print("Lane, Data Rate, Expected Voltage, Measured Voltage, Measured Difference, Accuracy Specification, Acceptance Limit, Measurement Uncertainty, Status", end=' ', file=outFile)
    print("", file=outFile)

    print(" , , , , , , (Guardband if applicable), , ", end=' ', file=outFile)
    print("", file=outFile)
    print(" , (Mbps) , (mV), (mV), (mV), (+/- mV), (+/- mV), (+/- mV), (Pass/Fail)", end=' ', file=outFile)
    print("", file=outFile)
    print("", file=outFile)

    # now fill in the arrays for lanes
    for dataRate in sorted(calParams.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for level in sorted(levels) :
                print("Lane %i," % lane, end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict_burst[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict_burst[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Lane %d...Target: %.2f Got: %.2f" % (lane, level, averageVoltageDict_burst[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Lane %d...Target: %.2f Got: %.2f" % (lane, level, averageVoltageDict_burst[dataRate][lane][level]))
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        # now fill in the arrays for clock
        for lane in [5] : # clock lane
            for level in sorted(levels) :
                print("Clock 1,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict_burst[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict_burst[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict_burst[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict_burst[dataRate][lane][level]))
                elif (abs(difference) + measurementUncertainty) > accuracySpec :
                    print("Pass *", end=' ', file=outFile)
                    probablePassFlag = True
                elif abs(difference) < acceptanceLimit :
                    print("Pass", end=' ', file=outFile)

                print("", file=outFile)

        for lane in [6] : # clock lane
            for level in sorted(levels) :
                print("Clock 2,", end=' ', file=outFile)
                print("%0.1f," % dataRate, end=' ', file=outFile)
                print("%0.1f," % level, end=' ', file=outFile)
                print("%0.1f," % averageVoltageDict_burst[dataRate][lane][level], end=' ', file=outFile)
                difference = averageVoltageDict_burst[dataRate][lane][level] - level
                print("%0.1f," % difference, end=' ', file=outFile)
                if (calParams.accuracyInPercent * abs(level) / 100) > calParams.accuracyInMv :
                    accuracySpec = calParams.accuracyInPercent * abs(level) / 100
                else :
                    accuracySpec = calParams.accuracyInMv
                print("%0.0f," % accuracySpec, end=' ', file=outFile)
                if (calParams.acceptanceInPercent * abs(level) / 100) > calParams.acceptanceInMv :
                    acceptanceLimit = calParams.acceptanceInPercent * abs(level) / 100
                else :
                    acceptanceLimit = calParams.acceptanceInMv
                print("%0.0f," % acceptanceLimit, end=' ', file=outFile)
                measurementUncertainty = calParams.measurementUncertaintyInMv
                print("%0.0f," % measurementUncertainty, end=' ', file=outFile)

                # determine pass / fail of measurement
                if (abs(difference) - measurementUncertainty) > accuracySpec :
                    print("Fail", end=' ', file=outFile)
                    failFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict_burst[dataRate][lane][level]))
                elif abs(difference) > acceptanceLimit :
                    print("Fail *", end=' ', file=outFile)
                    probableFailFlag = True
                    warningMsg("Bad Value on Clock... Target: %.2f Got: %.2f" % (level, averageVoltageDict_burst[dataRate][lane][level]))
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
    print("SV5C-DPRX module number %s: " % serialNumber, end=' ', file=outFile)
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

runValidation.args = ''
runValidation.code = r'''# --------------------------------------------------
print(' ')
printMsg('== Start Validation ==', 'magenta', None, True)

mipiClockConfig1.setup()
print('mipiClockConfig1.dataRate =', mipiClockConfig1.dataRate)

# Declare global dictionary of measured values in continuous mode
averageVoltageDict = dict()
for dataRate in sorted(calParams.dataRates) :
    averageVoltageDict[dataRate] = dict()
    for lane in range(1,7,1):
        averageVoltageDict[dataRate][lane] = dict()
        for targetLevel in sorted(calParams.targetLevels) :
            averageVoltageDict[dataRate][lane][targetLevel] = 0.0

# Declare global dictionary of measured values in burst mode
averageVoltageDict_burst = dict()
for dataRate in sorted(calParams.dataRates) :
    averageVoltageDict_burst[dataRate] = dict()
    for lane in range(1,7,1):
        averageVoltageDict_burst[dataRate][lane] = dict()
        for targetLevel in sorted(calParams.targetLevels) :
            averageVoltageDict_burst[dataRate][lane][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials in continuous mode
averagePolynomialDict = dict()
for dataRate in sorted(calParams.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(1,7,1):
        averagePolynomialDict[dataRate][lane] = dict()
        averagePolynomialDict[dataRate][lane] = [0.0,0.0,0.0,0.0,0.0,0.0]

# Declare global dictionary of transfer functions expressed as fifth order polynomials in burst mode
averagePolynomialDict_burst = dict()
for dataRate in sorted(calParams.dataRates) :
    averagePolynomialDict_burst[dataRate] = dict()
    for lane in range(1,7,1):
        averagePolynomialDict_burst[dataRate][lane] = dict()
        averagePolynomialDict_burst[dataRate][lane] = [0.0,0.0,0.0,0.0,0.0,0.0]

# now perform loop
# start generator
myString = "mipiGenerator1.pattern = customPattern1"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(5000)

analogCapture1.captureMode = "continuous"
# now measure
for targetLevel in sorted(calParams.targetLevels) :
    (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
    print('=== Validate measured amplitudes')
    for lane in sorted(laneList1.lanes) :
        print('Lane %d...' % lane)
        averageVoltageDict[dataRate][lane][targetLevel] = averageVoltagePerLaneHigh[lane]
        print('Average High Voltage:', averageVoltagePerLaneHigh[lane])
        if (((averageVoltagePerLaneHigh[lane] > targetLevel + targetLevel*0.15 or averageVoltagePerLaneHigh[lane] < targetLevel - targetLevel*0.15  ) and abs(averageVoltagePerLaneHigh[lane] - targetLevel) > 25) or math.isnan(averageVoltagePerLaneHigh[lane])):
            warningMsg("Bad Value on Lane %d... Target: %.2f Got: %.2f" % (lane, targetLevel, averageVoltagePerLaneHigh[lane]))
        averageVoltageDict[dataRate][lane][-targetLevel] = averageVoltagePerLaneLow[lane]
        print('Average Low Voltage:', averageVoltagePerLaneLow[lane])

    print('Clock 1...')
    averageVoltageDict[dataRate][5][targetLevel] = averageVoltagePerLaneHigh[5]
    print('Average High Voltage:', averageVoltagePerLaneHigh[5])

    averageVoltageDict[dataRate][5][-targetLevel] = averageVoltagePerLaneLow[5]
    print('Average Low Voltage:', averageVoltagePerLaneLow[5])

    print('Clock 2...')
    averageVoltageDict[dataRate][6][targetLevel] = averageVoltagePerLaneHigh[6]
    print('Average High Voltage:', averageVoltagePerLaneHigh[6])

    averageVoltageDict[dataRate][6][-targetLevel] = averageVoltagePerLaneLow[6]
    print('Average Low Voltage:', averageVoltagePerLaneLow[6])


lanes = sorted(laneList1.lanes)
lanes.append(5)
lanes.append(6)

# start generator
myString = "mipiGenerator1.pattern = customPattern2"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(5000)

analogCapture1.captureMode = "burst"
analogCapture1.triggerType = "allBursts"
analogCapture1.numBitsDesired = 1536
# now measure
for targetLevel in sorted(calParams.targetLevels) :
    (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
    print('=== Validate measured amplitudes')
    for lane in sorted(laneList1.lanes) :
        print('Lane %d...' % lane)
        averageVoltageDict_burst[dataRate][lane][targetLevel] = averageVoltagePerLaneHigh[lane]
        print('Average High Voltage:', averageVoltagePerLaneHigh[lane])
        if (((averageVoltagePerLaneHigh[lane] > targetLevel + targetLevel*calParams.accuracyInPercent/100.0 or averageVoltagePerLaneHigh[lane] < targetLevel - targetLevel*calParams.accuracyInPercent/100.0) and abs(averageVoltagePerLaneHigh[lane] - targetLevel) > calParams.accuracyInMv) or math.isnan(averageVoltagePerLaneHigh[lane])):
            warningMsg("Bad Value on Lane %d... Target: %.2f Got: %.2f" % (lane, targetLevel, averageVoltagePerLaneHigh[lane]))
        averageVoltageDict_burst[dataRate][lane][-targetLevel] = averageVoltagePerLaneLow[lane]
        print('Average Low Voltage:', averageVoltagePerLaneLow[lane])

    print('Clock 1...')
    averageVoltageDict_burst[dataRate][5][targetLevel] = averageVoltagePerLaneHigh[5]
    print('Average High Voltage:', averageVoltagePerLaneHigh[5])

    averageVoltageDict_burst[dataRate][5][-targetLevel] = averageVoltagePerLaneLow[5]
    print('Average Low Voltage:', averageVoltagePerLaneLow[5])

    print('Clock 2...')
    averageVoltageDict_burst[dataRate][6][targetLevel] = averageVoltagePerLaneHigh[6]
    print('Average High Voltage:', averageVoltagePerLaneHigh[6])

    averageVoltageDict_burst[dataRate][6][-targetLevel] = averageVoltagePerLaneLow[6]
    print('Average Low Voltage:', averageVoltagePerLaneLow[6])

levels = list()
for targetLevel in sorted(calParams.targetLevels) :
    levels.append(targetLevel)
    levels.append(-targetLevel)

# Generate Polynomials for continuous mode
for dataRate in sorted(calParams.dataRates) :
    for lane in range(1,7,1):
        xVals = sorted(levels)
        yVals = list()
        for targetLevel in sorted(levels) :
            yVals.append(averageVoltageDict[dataRate][lane][targetLevel])
        polynomialValues = np.polyfit(xVals, yVals, 5)
        averagePolynomialDict[dataRate][lane] = polynomialValues

# Generate Polynomials for burst mode
for dataRate in sorted(calParams.dataRates) :
    for lane in range(1,7,1):
        xVals = sorted(levels)
        yVals = list()
        for targetLevel in sorted(levels) :
            yVals.append(averageVoltageDict_burst[dataRate][lane][targetLevel])
        polynomialValues = np.polyfit(xVals, yVals, 5)
        averagePolynomialDict_burst[dataRate][lane] = polynomialValues

(failFlag, probableFailFlag) = iso17025Report(levels, averageVoltageDict, averageVoltageDict_burst)
generatePlots(levels, averageVoltageDict, averagePolynomialDict,"continuous")
generatePlots(levels, averageVoltageDict_burst, averagePolynomialDict_burst,"burst")

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
'''
runValidation.wantAllVarsGlobal = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 210.0
analogCapture1.forceFramePeriod = False
analogCapture1.forcedFramePeriodDuration = 1
analogCapture1.framePeriodType = 'numberOfBursts'
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
analogCapture1.startVoltage = -210.0
analogCapture1.timeout = 240
analogCapture1.triggerType = 'allBursts'
analogCapture1.wantAnalysis = True
analogCapture1.wantEyeDiagrams = False
analogCapture1.wantResultImages = False

laneList1.hsClockThresholdVoltage = 50.0
laneList1.hsDataThresholdVoltages = [50.0]
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpClockThresholdVoltage = 600.0
laneList1.lpDataThresholdVoltages = [600.0]

mipiClockConfig1.autoDetectDataRate = False
mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.continuousClock = False
mipiClockConfig1.dataRate = 200.0
mipiClockConfig1.referenceClocks = refClocksConfig1

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

plotCreator1.codeToSetupPlots = r'''lane = args[0]
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
plotA.setYLim([-400.0, 400.0])
'''
plotCreator1.fileName = 'image001'
plotCreator1.folderName = 'DataVersusPolyFit'
plotCreator1.grid = True
plotCreator1.layout = 'A'
plotCreator1.plotColors = ['blue']
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
refClocksConfig1.systemRefClockSource = 'external'

resultFolderCreator1.channelProvider = laneList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

#! TEST PROCEDURE
import datetime
import os
import math
import numpy as np
from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("25.1", None)


# check the serial number
serialNumberFailFlag = 1
for trial in range(5):
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    serialNumber = getTextDialog("Please enter the serial number of the RX unit (89-xxxx):")
    if serialNumber[:3] == '89-':
        serialNumberFailFlag = 0
        break

if serialNumberFailFlag == 0:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    myString = "Please ensure a cal file has been loaded on the module."
    waitForGuiOkDialog(myString)
    myString = "Start the procedure SV5C_DPTX_analogCapture_Cal_Generator first"
    waitForGuiOkDialog(myString)

    coordinator1.setState("running")

    # print HW, SW and FW info
    myString = "genFormFactor = iesp.__class__.__name__"
    res = coordinator1.waitForCodeToBeRun("Generator",myString)
    formFactor  = res[1]['genFormFactor']
    print('TX: ' + formFactor)
    myString = "genSN = iesp.getModuleSerialNums()"
    res = coordinator1.waitForCodeToBeRun("Generator",myString)
    print('TX: serial number: %s' % res[1]['genSN'])
    myString = "genFW = iesp.getFirmwareIdsFromConnection()[0]; genFWRev = iesp.getFirmwareRevisions()"
    res = coordinator1.waitForCodeToBeRun("Generator",myString)
    print('TX: FW: %s Revision: %s' %(res[1]['genFW'], res[1]['genFWRev']))

    printMsg("Serial Number: %s" % iesp.getModuleSerialNums(), 'magenta', None, True)
    printMsg('Firmware Id: %s' % iesp.getFirmwareIdsFromConnection()[0], 'magenta', None, True)
    printMsg("Firmware revision: %s" % iesp.getFirmwareRevisions(), 'magenta', None, True)
    printMsg("Hardware revision: %s" % iesp.getHardwareRevisions(), 'magenta', None, True)

    # rename the result folder
    renameFolderFailFlag = 0
    try:
        context = getCurrentTest()
        RunNotesFolderPath = context.getCurrRunResultFolderPath()
        # create a new folder named as the serial number of the RX unit
        resultFolderPath = context.createRunResultFolder(serialNumber)
    except:
        renameFolderFailFlag = 1
        printMsg("Fail: There is already a folder called (%s) in Results" % serialNumber, 'red', None, True)
        writeNoteForTestRun("Fail: There is already a folder called (%s) in Results" % serialNumber)

    if renameFolderFailFlag == 0:
        try:
            runValidation()
        except:
            printMsg("Failed to run validation for the RX unit (%s)." % serialNumber, 'red', None, True)
            writeNoteForTestRun("Failed to run validation for the RX unit (%s)." % serialNumber)

        # stop coordinator
        coordinator1.setState("stopped")
        # allow the generator time to detect state change and exit gracefully
        sleepMillis(20000)

    # copy runNotes folder to the result folder
    runNotes1.makeCopyOfTestLogFile()
    copyContentsOfFolder(RunNotesFolderPath, resultFolderPath)


# serial number not as expected
else:
    printMsg("Fail: The serial number provided of the RX unit (%s) is not as expected!" % serialNumber, 'red', None, True)
    writeNoteForTestRun("Fail: The serial number provided of the RX unit (%s) is not as expected!" % serialNumber)
