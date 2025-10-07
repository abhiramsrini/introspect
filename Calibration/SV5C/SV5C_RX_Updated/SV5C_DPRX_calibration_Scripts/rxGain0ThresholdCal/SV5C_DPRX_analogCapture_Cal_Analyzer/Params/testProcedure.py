# SVT Test
# SVT version 25.3.rc0
# Test saved 2025-08-04_1043
# Form factor: SV5C_4L8G_MIPI_DPHY_ANALYZER
# PY3
# Checksum: d4a3c7731c1888fd27210ac0db9bdc83
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calParams = _create('calParams', 'SvtDataRecord', iespName=None)
computeHighVoltage = _create('computeHighVoltage', 'SvtFunction', iespName=None)
computeLowVoltage = _create('computeLowVoltage', 'SvtFunction', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
generatePlots = _create('generatePlots', 'SvtFunction', iespName=None)
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName=None)
plotCreator1 = _create('plotCreator1', 'SvtPlotCreator', iespName=None)
plotCreator2 = _create('plotCreator2', 'SvtPlotCreator', iespName=None)
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic', iespName=None)
runCalibration = _create('runCalibration', 'SvtFunction', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName=None)
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName=None)

analogCapture1 = _create('analogCapture1', 'SvtMipiDphyAnalogCapture')
laneList1 = _create('laneList1', 'SvtMipiDphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

calParams.addField('dataRates', descrip='''List of data rates at which we want to compute receiver tranfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[200.0], displayOrder=(0, 1.0))
calParams.addField('targetLevels', descrip='''List of RX threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[100.0, 125.0, 150.0, 175.0, 210.0], displayOrder=(0, 2.0))
calParams.addField('wireSubChannels', descrip='''List of sub-receivers to calibrate.''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[0, 1], displayOrder=(0, 3.0))
calParams.addField('clockPhases', descrip='''List of bit-phases to calibrate.''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['even', 'odd'], displayOrder=(0, 4.0))
calParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calParams.dataRates = [200.0]
calParams.targetLevels = [100.0, 125.0, 150.0, 175.0, 210.0]
calParams.wireSubChannels = [0, 1]
calParams.clockPhases = ['even', 'odd']
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

generatePlots.args = 'levels, averageVoltageDict, PolynomialDict, averagePolynomialDict'
generatePlots.code = r'''for dataRate in sorted(calParams.dataRates) :
    for lane in sorted([1,2,3,4,5,6]) :
        for wireSubChannel in calParams.wireSubChannels:
            for phase in calParams.clockPhases:
                titleString = 'Average Transfer Function at %0.0f MHz, Lane %d\nsub-receiver %d, phase: %s' % (dataRate,lane,wireSubChannel,phase)
                xValues = sorted(levels)
                yValues = list()
                for targetLevel in sorted(levels) :
                    yValues.append(averageVoltageDict[dataRate][lane][wireSubChannel][phase][targetLevel])
                plotCreatorBasic1.xAxisLabel = "Input Voltage"
                plotCreatorBasic1.yAxisLabel = "Output Voltage"
                plotCreatorBasic1.yAxisLimits = [-630.0,630.0]
                plotCreatorBasic1.title = titleString
                plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots'
                plotCreatorBasic1.run(xValues, yValues)


for dataRate in sorted(calParams.dataRates) :
    for lane in sorted([1,2,3,4,5,6]) :
        for wireSubChannel in calParams.wireSubChannels:
            titleString = 'Average Transfer Function vs Fit, DR = %0.0f MHz, Lane %d\nsub-receiver %d' % (dataRate,lane,wireSubChannel)
            plotCreator2.run(lane, dataRate,wireSubChannel, averageVoltageDict, averagePolynomialDict, titleString)
            for phase in calParams.clockPhases:
                titleString = 'Average Transfer Function vs Fit, DR = %0.0f MHz, Lane %d\nsub-receiver %d, phase: %s' % (dataRate,lane,wireSubChannel,phase)
                plotCreator1.run(lane, dataRate,wireSubChannel,phase, averageVoltageDict, PolynomialDict, titleString)
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
analogCapture1.resultName = "Lane_amp_"+str(amplitude)
results = analogCapture1.run()
print('--> analogCapture Result: ', results.getResultFolderPath().split('\\')[-1])
averageVoltageForLaneHigh = dict()
averageVoltageForLaneLow = dict()

laneList1.lanes = [1,2,3,4]

for lane in [1,2,3,4] :
    averageVoltageForLaneHigh[lane] = dict()
    averageVoltageForLaneLow[lane] = dict()

    voltages = results.getVoltages(lane)

    src = HwTarget(lane)
    digitized_voltages = results.analysisByChannel[src]['digitizedLevels']

    averageVoltageForLaneHigh[lane] = digitized_voltages[1]#computeHighVoltage(voltages)
    averageVoltageForLaneLow[lane] = digitized_voltages[0]#computeLowVoltage(voltages)

    print('Lane %d: Average Voltage=%.2f' % (lane, averageVoltageForLaneLow[lane]))
    print('Lane %d: Average Voltage=%.2f' % (lane, averageVoltageForLaneHigh[lane]))
    #if not math.isnan(averageVoltageForLaneLow[lane]) and not math.isnan(averageVoltageForLaneHigh[lane]):
    #    break

"""
print('TX: customPattern1.hsBytes = [0]')
myString = "customPattern1.hsBytes = [0]"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "print('customPattern1.hsBytes =', customPattern1.hsBytes)"
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)

results = analogCapture1.run()
print('--> analogCapture Result: ', results.getResultFolderPath().split('\\')[-1])
averageVoltageForLaneLow = dict()
for lane in sorted(laneList1.lanes) :
    averageVoltageForLaneLow[lane] = dict()
    voltages = results.getVoltages(lane)
    averageVoltageForLaneLow[lane] = np.mean(voltages[500:8000])
    print('Lane %d: Average Voltage=%.2f' % (lane, np.mean(voltages[500:8000])))
"""
# ------------------------------------------------
numberOfMaxTrials = 10
laneList1.lanes = [1]
#set lane 1 to "CLK" mode (special mode for CLK analog capture)
iesp.writeSubPartRegister(0x0C22, 0x00, 0x01)
iesp.waitForCommandProcessors()

for trial in range(numberOfMaxTrials):
    print('=== Trial %d: Analog capture for Clock 1' % trial)
    myString = "mipiGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(10000)
    analogCapture1.resultName = "Clk1_amp_"+str(amplitude)
    clk_result = analogCapture1.run()
    print('--> analogCapture Result: ', clk_result.getResultFolderPath().split('\\')[-1])
    voltages = clk_result.getVoltages(1)

    src = HwTarget(1)
    digitized_voltages = clk_result.analysisByChannel[src]['digitizedLevels']

    averageVoltageForLaneLow[5] = digitized_voltages[0]#computeLowVoltage(voltages)
    averageVoltageForLaneHigh[5] = digitized_voltages[1]#computeHighVoltage(voltages)

    if not math.isnan(averageVoltageForLaneLow[5]) and not math.isnan(averageVoltageForLaneHigh[5]):
        break

#iesp.setMipiCaptureClockSelect(2)
iesp.writeSubPartRegister(0x0C22, 0x00, 0x02)
iesp.waitForCommandProcessors()
for trial in range(numberOfMaxTrials):
    print('=== Trial %d: Analog capture for Clock 2' % trial)
    myString = "mipiGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    sleepMillis(10000)
    analogCapture1.resultName = "Clk2_amp_"+str(amplitude)
    clk_result = analogCapture1.run()
    print('--> analogCapture Result: ', clk_result.getResultFolderPath().split('\\')[-1])
    voltages = clk_result.getVoltages(1)

    src = HwTarget(1)
    digitized_voltages = clk_result.analysisByChannel[src]['digitizedLevels']

    averageVoltageForLaneLow[6] = digitized_voltages[0]#computeLowVoltage(voltages)
    averageVoltageForLaneHigh[6] = digitized_voltages[1]#computeHighVoltage(voltages)

    if not math.isnan(averageVoltageForLaneLow[6]) and not math.isnan(averageVoltageForLaneHigh[6]):
        break
# set lane 1 to "DATA 1" mode (normal operation)
iesp.setMipiCaptureClockSelect(0)
laneList1.lanes = [1,2,3,4]

return (averageVoltageForLaneHigh, averageVoltageForLaneLow)
'''
getMeasurementsAtAmplitude.wantAllVarsGlobal = False

plotCreator1.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
wireSubChannel = args[2]
phase = args[3]
dataDict = args[4]
polyDict = args[5]
plotTitle = args[6]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()
yVals1 = list()
yVals2 = list()
for targetLevel in sorted( dataDict[dataRate][lane][wireSubChannel][phase].keys() ) :
    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][wireSubChannel][phase][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane][wireSubChannel][phase],targetLevel)
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

plotCreator2.codeToSetupPlots = r'''lane = args[0]
dataRate = args[1]
wireSubChannel = args[2]
dataDict = args[3]
polyDict = args[4]
plotTitle = args[5]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()

yVals1 = list()
yVals2 = list()
yVals3 = list()
for targetLevel in sorted( dataDict[dataRate][lane][wireSubChannel]['even'].keys() ) :

    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][lane][wireSubChannel]['even'][targetLevel])

    yVals2.append(dataDict[dataRate][lane][wireSubChannel]['odd'][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][lane][wireSubChannel],targetLevel)
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
plotCreator2.fileName = 'image001'
plotCreator2.folderName = 'DataVersusPolyFit_average'
plotCreator2.grid = True
plotCreator2.layout = 'A'
plotCreator2.plotColors = ['blue']
plotCreator2.plotType = 'line'
plotCreator2.projection = 'rectilinear'
plotCreator2.title = ''
plotCreator2.xAxisLabel = ''
plotCreator2.xAxisLimits = []
plotCreator2.xAxisScale = 'linear'
plotCreator2.xValues = r'''

'''
plotCreator2.yAxisLabel = ''
plotCreator2.yAxisLimits = []
plotCreator2.yAxisScale = 'linear'
plotCreator2.yValues = r'''

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

runCalibration.args = ''
runCalibration.code = r'''failFlag = 0

# --------------------------------------------------
print(' ')
printMsg('== Start calibration ==', 'magenta', None, True)

mipiClockConfig1.setup()
print('mipiClockConfig1.dataRate =', mipiClockConfig1.dataRate)

# Declare global dictionary of measured values
averageVoltageDict = dict()
for dataRate in sorted(calParams.dataRates) :
    averageVoltageDict[dataRate] = dict()
    for lane in range(1,7,1):
        averageVoltageDict[dataRate][lane] = dict()
        for wireSubChannel in calParams.wireSubChannels:
            averageVoltageDict[dataRate][lane][wireSubChannel] = dict()
            for phase in calParams.clockPhases:
                averageVoltageDict[dataRate][lane][wireSubChannel][phase] = dict()
                for targetLevel in sorted(calParams.targetLevels) :
                    averageVoltageDict[dataRate][lane][wireSubChannel][phase][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
PolynomialDict = dict()
for dataRate in sorted(calParams.dataRates) :
    PolynomialDict[dataRate] = dict()
    for lane in range(1,7,1):
        PolynomialDict[dataRate][lane] = dict()
        for wireSubChannel in calParams.wireSubChannels:
            PolynomialDict[dataRate][lane][wireSubChannel] = dict()
            for phase in calParams.clockPhases:
                PolynomialDict[dataRate][lane][wireSubChannel][phase] = [0.0,0.0,0.0,0.0,0.0,0.0]

# Declare global dictionary of transfer functions that will average the even and odd states
averagePolynomialDict = dict()
for dataRate in sorted(calParams.dataRates) :
    averagePolynomialDict[dataRate] = dict()
    for lane in range(1,7,1):
        averagePolynomialDict[dataRate][lane] = dict()
        for wireSubChannel in calParams.wireSubChannels:
            averagePolynomialDict[dataRate][lane][wireSubChannel] = [0.0,0.0,0.0,0.0,0.0,0.0]

# now perform loop
# start generator
myString = "mipiGenerator1.setup()"
coordinator1.waitForCodeToBeRun("Generator",myString)
sleepMillis(5000)


for targetLevel in sorted(calParams.targetLevels) :
    for wireSubChannel in calParams.wireSubChannels:
        # Placing clock commit here to ensure that the even/odd states toggle correctly
        mipiClockConfig1.setup()

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
            iesp.writeSubPartRegister(0xFEED, 0x00, subRecOption)
            iesp.waitForCommandProcessors()
        elif wireSubChannel == 1:
            print("Selecting sub-receiver 1")
            # Select Dual Receiver 1
            subRecOption = 0x03
            iesp.writeSubPartRegister(0xFEED, 0x00, subRecOption)
            iesp.waitForCommandProcessors()
        for phase in calParams.clockPhases:
            if phase == "odd":
                print("Toggling odd phase state.")
                iesp.writeSubPartRegister(0xFEEC, 0x00, 0x00) # Toggles even/odd state
                iesp.waitForCommandProcessors()

            (averageVoltagePerLaneHigh, averageVoltagePerLaneLow) = getMeasurementsAtAmplitude(targetLevel)
            print('=== Validate measured amplitudes')
            for lane in sorted(laneList1.lanes) :
                print('Lane %d...' % lane)
                averageVoltageDict[dataRate][lane][wireSubChannel][phase][targetLevel] = averageVoltagePerLaneHigh[lane]
                averageVoltageDict[dataRate][lane][wireSubChannel][phase][-targetLevel] = averageVoltagePerLaneLow[lane]
                if math.isnan(averageVoltagePerLaneHigh[lane]) or math.isnan(averageVoltagePerLaneLow[lane]):
                    failFlag = 1
                    warningMsg("Bad Value on Lane %d... Value None" % lane)
                elif (averageVoltagePerLaneHigh[lane] - averageVoltagePerLaneLow[lane]) < 100:
                    print('averageVoltagePerLaneLow', averageVoltagePerLaneLow[lane])
                    print('averageVoltagePerLaneHigh', averageVoltagePerLaneHigh[lane])
                    failFlag = 1
                    warningMsg("Bad Value on Lane %d... Difference less than 100" % lane)

            print('Clock 1...')
            print(averageVoltagePerLaneHigh[5])
            print(averageVoltagePerLaneLow[5])
            averageVoltageDict[dataRate][5][wireSubChannel][phase][targetLevel] = averageVoltagePerLaneHigh[5]
            averageVoltageDict[dataRate][5][wireSubChannel][phase][-targetLevel] = averageVoltagePerLaneLow[5]
            if math.isnan(averageVoltagePerLaneHigh[5]) or math.isnan(averageVoltagePerLaneLow[5]):
                failFlag = 1
                warningMsg("Bad Value on clock... Value None")
            elif (averageVoltagePerLaneHigh[5] - averageVoltagePerLaneLow[5]) < 100:
                print('averageVoltagePerLaneLow', averageVoltagePerLaneLow[5])
                print('averageVoltagePerLaneHigh', averageVoltagePerLaneHigh[5])
                failFlag = 1
                warningMsg("Bad Value on clock")

            print('Clock 2...')
            print(averageVoltagePerLaneHigh[6])
            print(averageVoltagePerLaneLow[6])
            averageVoltageDict[dataRate][6][wireSubChannel][phase][targetLevel] = averageVoltagePerLaneHigh[6]
            averageVoltageDict[dataRate][6][wireSubChannel][phase][-targetLevel] = averageVoltagePerLaneLow[6]
            if math.isnan(averageVoltagePerLaneHigh[6]) or math.isnan(averageVoltagePerLaneLow[6]):
                failFlag = 1
                warningMsg("Bad Value on clock... Value None")
            elif (averageVoltagePerLaneHigh[6] - averageVoltagePerLaneLow[6]) < 100:
                print('averageVoltagePerLaneLow', averageVoltagePerLaneLow[6])
                print('averageVoltagePerLaneHigh', averageVoltagePerLaneHigh[6])
                failFlag = 1
                warningMsg("Bad Value on clock")

lanes = sorted(laneList1.lanes)
lanes.append(5)
print(averageVoltageDict)
#averageVoltageDict = {200.0: {1: {0: {'even': {100.0: 210.01825, 125.0: 257.94221, 150.0: 301.31887, 175.0: 345.96603, 210.0: 394.29343, -100.0: -232.30941, -125.0: -281.26773, -150.0: -324.08609, -175.0: -369.13142, -210.0: -416.82987}, 'odd': {100.0: 189.88435, 125.0: 230.1515, 150.0: 270.04658, 175.0: 307.31379, 210.0: 347.61305, -100.0: -244.11254, -125.0: -288.10449, -150.0: -332.19888, -175.0: -375.84911, -210.0: -426.8559}}, 1: {'even': {100.0: 190.6727, 125.0: 233.08593, 150.0: 274.24477, 175.0: 313.02558, 210.0: 356.21633, -100.0: -214.92954, -125.0: -264.07864, -150.0: -309.36423, -175.0: -350.85839, -210.0: -402.37061}, 'odd': {100.0: 291.49709, 125.0: 346.16966, 150.0: 394.76015, 175.0: 449.5053, 210.0: 506.1283, -100.0: -151.88764, -125.0: -202.39047, -150.0: -250.16273, -175.0: -297.97822, -210.0: -344.88878}}}, 2: {0: {'even': {100.0: 191.61466, 125.0: 231.71549, 150.0: 269.95908, 175.0: 306.6799, 210.0: 350.4225, -100.0: -169.95447, -125.0: -209.46749, -150.0: -247.34711, -175.0: -278.83604, -210.0: -326.15193}, 'odd': {100.0: 179.80835, 125.0: 212.17687, 150.0: 250.25011, 175.0: 286.57141, 210.0: 328.03866, -100.0: -172.8318, -125.0: -210.55263, -150.0: -249.76426, -175.0: -284.66918, -210.0: -327.64518}}, 1: {'even': {100.0: 210.83103, 125.0: 253.03398, 150.0: 290.61934, 175.0: 332.03016, 210.0: 383.24944, -100.0: -190.30284, -125.0: -230.48541, -150.0: -266.63691, -175.0: -296.54783, -210.0: -345.45661}, 'odd': {100.0: 209.34784, 125.0: 248.13362, 150.0: 284.54868, 175.0: 320.50057, 210.0: 372.35102, -100.0: -215.54373, -125.0: -259.73284, -150.0: -302.08936, -175.0: -344.68956, -210.0: -402.35744}}}, 3: {0: {'even': {100.0: 189.90949, 125.0: 229.94181, 150.0: 266.55295, 175.0: 300.38133, 210.0: 337.42187, -100.0: -209.96718, -125.0: -250.43947, -150.0: -291.19547, -175.0: -330.37031, -210.0: -380.34127}, 'odd': {100.0: 201.1337, 125.0: 242.99971, 150.0: 284.99619, 175.0: 319.47093, 210.0: 364.50564, -100.0: -203.30628, -125.0: -244.92681, -150.0: -285.26295, -175.0: -319.01199, -210.0: -364.90749}}, 1: {'even': {100.0: 220.60024, 125.0: 265.24293, 150.0: 307.41639, 175.0: 345.09538, 210.0: 385.03912, -100.0: -190.89642, -125.0: -235.70606, -150.0: -276.68502, -175.0: -312.04492, -210.0: -354.09264}, 'odd': {100.0: 190.14037, 125.0: 230.03224, 150.0: 268.27957, 175.0: 304.38664, 210.0: 343.61452, -100.0: -222.84834, -125.0: -265.77324, -150.0: -309.78916, -175.0: -348.1884, -210.0: -391.77659}}}, 4: {0: {'even': {100.0: 190.15724, 125.0: 240.62577, 150.0: 287.01845, 175.0: 327.77935, 210.0: 378.3419, -100.0: -270.23668, -125.0: -323.45069, -150.0: -370.13175, -175.0: -419.6977, -210.0: -477.7694}, 'odd': {100.0: 273.39261, 125.0: 323.2716, 150.0: 370.32868, 175.0: 413.74425, 210.0: 471.29513, -100.0: -170.06574, -125.0: -211.50976, -150.0: -251.13363, -175.0: -290.59586, -210.0: -335.57569}}, 1: {'even': {100.0: 211.48764, 125.0: 251.59725, 150.0: 290.94991, 175.0: 328.85919, 210.0: 370.07385, -100.0: -149.52427, -125.0: -187.06097, -150.0: -215.81815, -175.0: -251.12021, -210.0: -290.30122}, 'odd': {100.0: 189.89543, 125.0: 226.30277, 150.0: 256.16235, 175.0: 290.32417, 210.0: 329.83862, -100.0: -167.71687, -125.0: -200.60647, -150.0: -233.49677, -175.0: -270.07859, -210.0: -309.15601}}}, 5: {0: {'even': {100.0: 230.68875, 125.0: 280.21508, 150.0: 323.40861, 175.0: 360.03937, 210.0: 408.94993, -100.0: -190.84461, -125.0: -235.33608, -150.0: -273.26602, -175.0: -311.18238, -210.0: -356.50061}, 'odd': {100.0: 192.41803, 125.0: 233.08672, 150.0: 272.82885, 175.0: 310.98683, 210.0: 356.06359, -100.0: -230.24941, -125.0: -277.72811, -150.0: -319.02927, -175.0: -358.21593, -210.0: -406.04388}}, 1: {'even': {100.0: 201.26074, 125.0: 240.53291, 150.0: 277.36997, 175.0: 312.00949, 210.0: 353.91172, -100.0: -192.63197, -125.0: -236.84766, -150.0: -277.39791, -175.0: -315.14512, -210.0: -357.17653}, 'odd': {100.0: 222.98864, 125.0: 265.86642, 150.0: 311.19589, 175.0: 354.4413, 210.0: 400.18807, -100.0: -201.59178, -125.0: -247.78671, -150.0: -293.21377, -175.0: -340.16681, -210.0: -389.50111}}}, 6: {0: {'even': {100.0: 0.0, 125.0: 0.0, 150.0: 0.0, 175.0: 0.0, 210.0: 0.0}, 'odd': {100.0: 0.0, 125.0: 0.0, 150.0: 0.0, 175.0: 0.0, 210.0: 0.0}}, 1: {'even': {100.0: 0.0, 125.0: 0.0, 150.0: 0.0, 175.0: 0.0, 210.0: 0.0}, 'odd': {100.0: 0.0, 125.0: 0.0, 150.0: 0.0, 175.0: 0.0, 210.0: 0.0}}}}}

levels = list()
for targetLevel in sorted(calParams.targetLevels) :
    levels.append(targetLevel)
    levels.append(-targetLevel)


# Generate Polynomials for even/odd states
for dataRate in sorted(calParams.dataRates) :
    for lane in range(1,7,1):
        for wireSubChannel in calParams.wireSubChannels:
            for phase in calParams.clockPhases:
                xVals = sorted(levels)
                yVals = list()
                for targetLevel in sorted(levels) :
                    yVals.append(averageVoltageDict[dataRate][lane][wireSubChannel][phase][targetLevel])
                polynomialValues = np.polyfit(xVals, yVals, 5)
                PolynomialDict[dataRate][lane][wireSubChannel][phase] = polynomialValues

# Generate Polynomials that average even/odd states
for dataRate in sorted(calParams.dataRates) :
    for lane in range(1,7,1):
        for wireSubChannel in calParams.wireSubChannels:
            xVals = list()
            yVals = list()
            for targetLevel in sorted(levels) :
                xVals.append(targetLevel)
                yVals.append(averageVoltageDict[dataRate][lane][wireSubChannel]['even'][targetLevel])

                xVals.append(targetLevel)
                yVals.append(averageVoltageDict[dataRate][lane][wireSubChannel]['odd'][targetLevel])
            polynomialValues = np.polyfit(xVals, yVals, 5)
            averagePolynomialDict[dataRate][lane][wireSubChannel] = polynomialValues

generatePlots(levels, averageVoltageDict, PolynomialDict,averagePolynomialDict)
writeAverageVoltages(levels, averageVoltageDict)

if failFlag == 0 :
    writeTransferFunctions(PolynomialDict,averagePolynomialDict)
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
runCalibration.wantAllVarsGlobal = False

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

writeAverageVoltages.args = 'levels, averageVoltageDict'
writeAverageVoltages.code = r'''# create csv file output
stringAppendix = ".csv"
filePathString = "AverageVoltageMeasurements" + stringAppendix
resultFolderCreator1.folderName = "AverageVoltageMeasurements"
folderPath = resultFolderCreator1.run()
filePath = os.path.join(folderPath, filePathString)


with open(filePath, "w") as outFile:

    # Fill header section
    print("dataRates,", end=' ', file=outFile)
    for dataRate in sorted(calParams.dataRates) :
        print("%0.1f," % dataRate, end=' ', file=outFile)
    print("", file=outFile)

    print("lanes,", end=' ', file=outFile)
    for lane in sorted(laneList1.lanes) :
        print("%d," % lane, end=' ', file=outFile)
    print("", file=outFile)

    # End the header section with the keyword Voltages
    print("Voltages", file=outFile)

    # now fill in the arrays
    for dataRate in sorted(calParams.dataRates) :
        for lane in sorted(laneList1.lanes) :
            for wireSubChannel in calParams.wireSubChannels:
                for phase in calParams.clockPhases:
                    commentString = "# Data Rate = %0.0f, Lane = %d, sub-Receiver = %d, phase = %s" % (dataRate, lane, wireSubChannel,phase)
                    print(commentString, file=outFile)

                    # Output target levels
                    print("Target,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.0f," % level, end=' ', file=outFile)
                    print("", file=outFile)

                    # Output measured levels
                    print("Measured,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.4g," % averageVoltageDict[dataRate][lane][wireSubChannel][phase][level], end=' ', file=outFile)
                    print("", file=outFile)

    for dataRate in sorted(calParams.dataRates) :
        for wireSubChannel in calParams.wireSubChannels:
                for phase in calParams.clockPhases:
                    commentString = "# Data Rate = %0.0f, CLK 1, sub-Receiver = %d, phase = %s" % (dataRate, wireSubChannel,phase)
                    print(commentString, file=outFile)

                    # Output target levels
                    print("Target,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.0f," % level, end=' ', file=outFile)
                    print("", file=outFile)

                    # Output measured levels
                    print("Measured,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.4g," % averageVoltageDict[dataRate][5][wireSubChannel][phase][level], end=' ', file=outFile)
                    print("", file=outFile)

    for dataRate in sorted(calParams.dataRates) :
        for wireSubChannel in calParams.wireSubChannels:
                for phase in calParams.clockPhases:
                    commentString = "# Data Rate = %0.0f, CLK 2, sub-Receiver = %d, phase = %s" % (dataRate, wireSubChannel,phase)
                    print(commentString, file=outFile)

                    # Output target levels
                    print("Target,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.0f," % level, end=' ', file=outFile)
                    print("", file=outFile)

                    # Output measured levels
                    print("Measured,", end=' ', file=outFile)
                    for level in sorted(levels) :
                        print("%0.4g," % averageVoltageDict[dataRate][6][wireSubChannel][phase][level], end=' ', file=outFile)
                    print("", file=outFile)
'''
writeAverageVoltages.wantAllVarsGlobal = False

writeTransferFunctions.args = 'PolynomialDict, averagePolynomialDict'
writeTransferFunctions.code = r'''now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)
resultFolderCreator1.folderName = "calCoefficients_" + serialNumber
folderPath = resultFolderCreator1.run()

stringAppendix = ".txt"
filePathString = "calCoefficients_" + serialNumber + stringAppendix
filePath = os.path.join(folderPath, filePathString)

with open(filePath, "w") as outFile:
    commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    print("BEGIN SECTION", file=outFile)
    print("section type : header", file=outFile)
    print("serial number : "+serialNumber, file=outFile)
    print("hardware revision : B", file=outFile)
    print("date of manufacture(YYYYMMDD) : "+date, file=outFile)
    print("date of calibration(YYYYMMDD) : "+date, file=outFile)
    print("speed grade : 0", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : dprx_rx_threshold_volt_gain0_calibration_data", file=outFile)
    numRates = 1
    ratesMeasured = 0
    for dataRate in sorted(calParams.dataRates) :
        ratesMeasured = ratesMeasured + 1
        commentString = "# Data Rate = %0.0f" % (dataRate)
        print(commentString, file=outFile)
        outFile.write("# Each row has 2*<number of data lanes> + 4*<Clock lane> columns , i.e, D0_0, D0_1, D1_0, D1_1, D2_0, D2_1,  D3_0, D3_1, CLK0_0, CLK0_1, CLK1_0, CLK1_1 \n")
        for i in range(5,-1,-1) :
            print(commentArray[i], file=outFile)
            for lane in range(1,7,1):
                if i == 5:
                    value_0 = PolynomialDict[dataRate][lane][0]['even'][i] * 1000
                    value_1 = PolynomialDict[dataRate][lane][1]['even'][i] * 1000
                else:
                    value_0 = PolynomialDict[dataRate][lane][0]['even'][i]
                    value_1 = PolynomialDict[dataRate][lane][1]['even'][i]

                print("%0.10g,%0.10g," % (value_0, value_1), end=' ', file=outFile)
            print("", file=outFile)

        for i in range(5,-1,-1) :
            print(commentArray[i], file=outFile)
            for lane in range(1,7,1):
                if i == 5:
                    value_0 = PolynomialDict[dataRate][lane][0]['odd'][i] * 1000
                    value_1 = PolynomialDict[dataRate][lane][1]['odd'][i] * 1000
                else:
                    value_0 = PolynomialDict[dataRate][lane][0]['odd'][i]
                    value_1 = PolynomialDict[dataRate][lane][1]['odd'][i]

                print("%0.10g,%0.10g," % (value_0, value_1), end=' ', file=outFile)
            print("", file=outFile)
        for i in range(5,-1,-1) :
            print(commentArray[i], file=outFile)
            for lane in range(1,7,1):
                if i == 5:
                    value_0 = averagePolynomialDict[dataRate][lane][0][i] * 1000
                    value_1 = averagePolynomialDict[dataRate][lane][1][i] * 1000
                else:
                    value_0 = averagePolynomialDict[dataRate][lane][0][i]
                    value_1 = averagePolynomialDict[dataRate][lane][1][i]

                print("%0.10g,%0.10g," % (value_0, value_1), end=' ', file=outFile)
            print("", file=outFile)
    print("END SECTION", file=outFile)
'''
writeTransferFunctions.wantAllVarsGlobal = False


analogCapture1.captureMode = 'continuous'
analogCapture1.dataRateAttr = 0.0
analogCapture1.endVoltage = 350.0
analogCapture1.forceFramePeriod = False
analogCapture1.forcedFramePeriodDuration = 1
analogCapture1.framePeriodType = 'numberOfBursts'
analogCapture1.laneList = laneList1
analogCapture1.lineRateSource = 'fromClockConfig'
analogCapture1.measurementMode = 'differential'
analogCapture1.minLpDurationForStart = 500
analogCapture1.nthBurst = 1
analogCapture1.numBitsDesired = 64
analogCapture1.patternLenBits = 2
analogCapture1.refLane = 1
analogCapture1.riseTimeMode = 'RT_None'
analogCapture1.saveResults = True
analogCapture1.startVoltage = -350.0
analogCapture1.timeout = 300
analogCapture1.triggerType = 'allBursts'
analogCapture1.wantAnalysis = True
analogCapture1.wantEyeDiagrams = False
analogCapture1.wantResultImages = False

laneList1.expectedPattern = None
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

refClocksConfig1.externRefClockFreq = 100.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.systemRefClockSource = 'external'

resultFolderCreator1.channelProvider = laneList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

#! TEST PROCEDURE
import datetime
import os
import math
import numpy as np
from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder
from dftm.miscTypes import HwTarget

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("25.1", None)

iesp.disableValidation()
analogCapture1.startVoltage = -630
analogCapture1.endVoltage = 630

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
            runCalibration()
        except:
            printMsg("Failed to run calibration for the RX unit (%s)." % serialNumber, 'red', None, True)
            writeNoteForTestRun("Failed to run calibration for the RX unit (%s)." % serialNumber)

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
