# SVT Test
# SVT version 24.4.b8
# Test saved 2024-09-30_1430
# Form factor: SV7C_16C17G
# PY3
# Checksum: 6175a610a2d5553cf3179f0f90505fca
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
computeMean = _create('computeMean', 'SvtFunction', iespName='None')
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName='None')
dataFile2 = _create('dataFile2', 'SvtDataFile', iespName='None')
generatePlots = _create('generatePlots', 'SvtFunction', iespName='None')
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName='None')
overrideCalCoefficients = _create('overrideCalCoefficients', 'SvtFunction', iespName='None')
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName='None')
writeValidationReport = _create('writeValidationReport', 'SvtFunction', iespName='None')

eyeScan1 = _create('eyeScan1', 'SvtEyeScan')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
plotCreator1 = _create('plotCreator1', 'SvtPlotCreator')
plotCreator2 = _create('plotCreator2', 'SvtPlotCreator')
plotCreator3 = _create('plotCreator3', 'SvtPlotCreator')
plotCreator4 = _create('plotCreator4', 'SvtPlotCreator')
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
rxChannelList1 = _create('rxChannelList1', 'SvtRxChannelList')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
vScan1 = _create('vScan1', 'SvtVScan')

calOptions.addField('moduleName', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('sv7c17DataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[16000.0], displayOrder=(0, 2.0))
calOptions.addField('sv7c28DataRates', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[26000.0], displayOrder=(0, 3.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[-400.0, -300.0, -200.0, 200.0, 300.0, 400.0], displayOrder=(0, 4.0))
calOptions.addField('saveEyeScans', descrip='''''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 5.0))
calOptions.addField('usePerPhase', descrip='''''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 6.0))
calOptions.addField('Error_prct', descrip='''The maximum allowable error for target level in percent (%)''', attrType=float, iespInstanceName='any', defaultVal=10.0, displayOrder=(0, 7.0))
calOptions.addField('Error_mV', descrip='''The maximum allowable error for target level in mV''', attrType=float, iespInstanceName='any', defaultVal=15.0, displayOrder=(0, 8.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.moduleName = '1234'
calOptions.sv7c17DataRates = [16000.0]
calOptions.sv7c28DataRates = [26000.0]
calOptions.targetLevels = [-375.0, -325.0, -275.0, -225.0, -175.0, 175.0, 225.0, 275.0, 325.0, 375.0]
calOptions.saveEyeScans = False
calOptions.usePerPhase = False
calOptions.Error_prct = 15.0
calOptions.Error_mV = 15.0
calOptions.callCustomInitMethod()
computeMean.args = 'rising,voltages,errorCountsByVoltage,Phase,channel'
computeMean.code = r'''searchRange = len(voltages)-1
voltageStep = voltages[1]-voltages[0]
if calOptions.usePerPhase:
    divisionFactor = eyeScan1.bertDurationInBits
elif useActivePatternForSinglePhase:
    divisionFactor = vScan1.bertDurationInBits/2
else:
    divisionFactor = vScan1.bertDurationInBits

if calOptions.usePerPhase:
    maxError=errorCountsByVoltage[channel][voltages[0]][Phase]
    minError=errorCountsByVoltage[channel][voltages[0]][Phase]
else:
    maxError=errorCountsByVoltage[channel][0]
    minError=errorCountsByVoltage[channel][0]

if rising :
    meanLocation = 0.0
    for i in range(int(searchRange/2)-5, searchRange) :
        if calOptions.usePerPhase:
            errorCount1 = errorCountsByVoltage[channel][voltages[i+1]][Phase]
            errorCount2 = errorCountsByVoltage[channel][voltages[i]][Phase]
        else:
            errorCount1 = errorCountsByVoltage[channel][i+1]
            errorCount2 = errorCountsByVoltage[channel][i]
        if i == (searchRange-1) :
            if errorCount1 < divisionFactor :
                errorCount1 = divisionFactor
        f_x = +1.0*(errorCount1-errorCount2) / (voltages[i+1] - voltages[i])
        meanLocation = meanLocation + voltages[i]*f_x

        if (errorCount2 < minError) :
            minError = errorCount2
        if (errorCount2 > maxError) :
            maxError = errorCount2

    meanLocation = voltageStep*(meanLocation / divisionFactor) + voltageStep / 2
else :
    meanLocation = 0.0
    for i in range(0, int(searchRange/2)+5) :
        if calOptions.usePerPhase:
            errorCount1 = errorCountsByVoltage[channel][voltages[i+1]][Phase]
            errorCount2 = errorCountsByVoltage[channel][voltages[i]][Phase]
        else:
            errorCount1 = errorCountsByVoltage[channel][i+1]
            errorCount2 = errorCountsByVoltage[channel][i]
        if i == 0 :
            if errorCount2 < divisionFactor :
                errorCount2 = divisionFactor
        f_x = -1.0*(errorCount1-errorCount2) / (voltages[i+1] - voltages[i])
        meanLocation = meanLocation + voltages[i]*f_x

        if (errorCount2 < minError) :
            minError = errorCount2
        if (errorCount2 > maxError) :
            maxError = errorCount2

    meanLocation = voltageStep*(meanLocation / divisionFactor) + voltageStep / 2

if ((maxError<divisionFactor) | (minError!=0)) :
    if calOptions.usePerPhase:
        print('possible missed edge channel %i, phase %i'%(channel,Phase))
    else:
        print('possible missed edge channel %i'%(channel))
    print('minError: %i, maxError: %i'%(minError, maxError))
return meanLocation
'''
computeMean.wantAllVarsGlobal = False

dataFile1.delimiter = ','
dataFile1.fileName = 'PhaseThresholdCal.csv'
dataFile1.numFields = 1
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'

dataFile2.delimiter = ','
dataFile2.fileName = 'AverageVoltageMeasurements.csv'
dataFile2.numFields = 1
dataFile2.otherFolderPath = r'None'
dataFile2.parentFolder = 'Results'

generatePlots.args = ''
generatePlots.code = r'''# generate average transfer functions
for dataRate in sorted(dataRates) :
    for channel in sorted(rxChannelList1.channels) :
        titleString = 'Average Transfer Function at %0.0f MHz, Ch %d' % (dataRate,channel)
        xValues = list()
        yValues = list()
        for targetLevel in sorted(targetLevels) :
            yValues.append(averageVoltageDict[dataRate][channel][targetLevel])
            xValues.append(targetLevel)
        plotCreatorBasic1.xAxisLabel = "Input Voltage"
        plotCreatorBasic1.yAxisLabel = "Output Voltage"
        plotCreatorBasic1.yAxisLimits = [-800.0,800.0]
        plotCreatorBasic1.title = titleString
        plotCreatorBasic1.folderName = 'AverageTransferFunctionPlots'
        plotCreatorBasic1.run(xValues, yValues)

if calOptions.usePerPhase:
    for dataRate in sorted(dataRates) :
        for channel in sorted(rxChannelList1.channels) :
            plotCreator1.folderName = 'PerPhaseDcPlots'
            titleString = 'Per Phase Measurements at %0.0f MHz, Ch %d' % (dataRate,channel)
            plotCreator1.run(dataRate, channel,sorted(targetLevels),measuredVoltageDict,titleString)

for channel in sorted(rxChannelList1.channels) :
    plotCreator2.folderName = 'DataRateTrendPlot'
    titleString = 'Average Transfer Functions Across Data Rates, Ch %d' % channel
    plotCreator2.run(channel, sorted(dataRates),averageVoltageDict, titleString)

for dataRate in sorted(dataRates) :
    for channel in sorted(rxChannelList1.channels) :
        plotCreator3.folderName = 'DataVersusPolyFit'
        titleString = 'Average Transfer Function vs Fit, DR = %0.0f, Ch %d' % (dataRate,channel)
        plotCreator3.run(channel, dataRate, averageVoltageDict, averagePolynomialDict, titleString)
'''
generatePlots.wantAllVarsGlobal = False

getMeasurementsAtAmplitude.args = 'amplitude'
getMeasurementsAtAmplitude.code = r'''if amplitude > 0.0 :
    txChannelList1.voltageSwings = amplitude * 2.0
    txChannelList1.setup()
    txChannelList1.polarities = 'inverted'
    txChannelList1.update()
    rxChannelList1.polarities = 'inverted'
    rxChannelList1.setup()

    (minPhase, maxPhase, minPhaseStep) = iesp.getRxPhaseScanLimits()
    eyeScan1.startPhase = 0
    eyeScan1.endPhase = minPhaseStep*127
    if calOptions.usePerPhase:
        result = eyeScan1.run()
        phasesByChannel = {}
        errCountsByVoltage = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                phasesByChannel[channel] = result.getPhases(channel)
                errCountsByVoltage[channel] = result.getErrCountsByVoltage(channel)
    else:
        for i in range(10):
            result = vScan1.run()

            if not useActivePatternForSinglePhase:
                break

            rxPhaseFound = True
            for channel in sorted(rxChannelList1.channels):
                rxPhase = vScan1.getRxPhaseForChannel(channel)
                if rxPhase == 0: #usually indicates vScan setup failed so be wary of the eye center
                    rxPhaseFound = False

            if rxPhaseFound:
                break

            if i==9:
                errorMsg("Failed to find center vScan")

        errCountsByVoltage = {}
        voltagesByChannel = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                errCountsByVoltage[channel] = result.getErrCounts(channel)
                voltagesByChannel[channel] = result.getVoltages(channel)

    measuredVoltageDict = dict()
    averageVoltageForChannel = dict()
    for channel in sorted(rxChannelList1.channels) :
        if calOptions.usePerPhase:
            voltages = sorted(errCountsByVoltage[channel].keys())
            measuredVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredVoltageDict[channel].append(computeMean(True,voltages,errCountsByVoltage,phase,channel) )
            averageVoltageForChannel[channel] = np.average(measuredVoltageDict[channel])
        else:
            voltages = voltagesByChannel[channel]
            if useActivePatternForSinglePhase:
                averageVoltageForChannel[channel] = (computeMean(True,voltages,errCountsByVoltage,None,channel), computeMean(False,voltages,errCountsByVoltage,None,channel))
            else:
                averageVoltageForChannel[channel] = computeMean(True,voltages,errCountsByVoltage,None,channel)
else :
    txChannelList1.voltageSwings = -1.0*amplitude * 2.0
    txChannelList1.setup()
    txChannelList1.polarities = 'normal'
    txChannelList1.update()
    rxChannelList1.polarities = 'normal'
    rxChannelList1.setup()

    (minPhase, maxPhase, minPhaseStep) = iesp.getRxPhaseScanLimits()
    eyeScan1.startPhase = 0
    eyeScan1.endPhase = minPhaseStep*127
    if calOptions.usePerPhase:
        result = eyeScan1.run()
        phasesByChannel = {}
        errCountsByVoltage = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                phasesByChannel[channel] = result.getPhases(channel)
                errCountsByVoltage[channel] = result.getErrCountsByVoltage(channel)
    else:
        for i in range(10):
            result = vScan1.run()

            if not useActivePatternForSinglePhase:
                break

            rxPhaseFound = True
            for channel in sorted(rxChannelList1.channels):
                rxPhase = vScan1.getRxPhaseForChannel(channel)
                if rxPhase == 0: #usually indicates vScan setup failed so be wary of the eye center
                    rxPhaseFound = False

            if rxPhaseFound:
                break

            if i==9:
                errorMsg("Failed to find center vScan")

        errCountsByVoltage = {}
        voltagesByChannel = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                errCountsByVoltage[channel] = result.getErrCounts(channel)
                voltagesByChannel[channel] = result.getVoltages(channel)

    measuredVoltageDict = dict()
    averageVoltageForChannel = dict()
    for channel in sorted(rxChannelList1.channels) :
        if calOptions.usePerPhase:
            voltages = sorted(errCountsByVoltage[channel].keys())
            measuredVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredVoltageDict[channel].append(computeMean(False,voltages,errCountsByVoltage,phase,channel))
            averageVoltageForChannel[channel] = np.average(measuredVoltageDict[channel])
        else:
            voltages = voltagesByChannel[channel]
            if useActivePatternForSinglePhase:
                averageVoltageForChannel[channel] = (computeMean(False,voltages,errCountsByVoltage,None,channel), computeMean(False,voltages,errCountsByVoltage,None,channel))
            else:
                averageVoltageForChannel[channel] = computeMean(False,voltages,errCountsByVoltage,None,channel)

return (measuredVoltageDict, averageVoltageForChannel)
'''
getMeasurementsAtAmplitude.wantAllVarsGlobal = False

overrideCalCoefficients.args = ''
overrideCalCoefficients.code = r'''# If desired, manually load the calibration coefficients


p1 = [ 0.0,  0.0,   1.0,  0.0]
p2 = [ 0.0,  0.0,   1.0,  0.0]
p3 = [ 0.0,  0.0,   1.0,  0.0]
p4 = [ 0.0,  0.0,   1.0,  0.0]
p5 = [ 0.0,  0.0,   1.0,  0.0]
p6 = [ 0.0,  0.0,   1.0,  0.0]
p7 = [ 0.0,  0.0,   1.0,  0.0]
p8 = [ 0.0,  0.0,   1.0,  0.0]



#setDebugLevel(3)

offset = p1[3]*1
success = writeRegister(0x414, 0x01, offset)
m1 = (p1[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x01, m1)
m2 = (p1[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x01, m2)
m3 = (p1[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x01, m3)


offset = p2[3]*1
success = writeRegister(0x414, 0x02, offset)
m1 = (p2[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x02, m1)
m2 = (p2[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x02, m2)
m3 = (p2[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x02, m3)

offset = p3[3]*1
success = writeRegister(0x414, 0x04, offset)
m1 = (p3[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x04, m1)
m2 = (p3[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x04, m2)
m3 = (p3[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x04, m3)

offset = p4[3]*1
success = writeRegister(0x414, 0x08, offset)
m1 = (p4[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x08, m1)
m2 = (p4[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x08, m2)
m3 = (p4[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x08, m3)

offset = p5[3]*1
success = writeRegister(0x414, 0x10, offset)
m1 = (p5[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x10, m1)
m2 = (p5[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x10, m2)
m3 = (p5[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x10, m3)

offset = p6[3]*1
success = writeRegister(0x414, 0x20, offset)
m1 = (p6[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x20, m1)
m2 = (p6[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x20, m2)
m3 = (p6[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x20, m3)

offset = p7[3]*1
success = writeRegister(0x414, 0x40, offset)
m1 = (p7[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x40, m1)
m2 = (p7[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x40, m2)
m3 = (p7[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x40, m3)

offset = p8[3]*1
success = writeRegister(0x414, 0x80, offset)
m1 = (p8[2] * math.pow(2.0,24))
success = writeRegister(0x0416, 0x80, m1)
m2 = (p8[1] * math.pow(2.0,24))
success = writeRegister(0x0419, 0x80, m2)
m3 = (p8[0] * math.pow(2.0,24))
success = writeRegister(0x041A, 0x80, m3)

#setDebugLevel(0)
'''
overrideCalCoefficients.wantAllVarsGlobal = False

writeAverageVoltages.args = ''
writeAverageVoltages.code = r'''# create csv file output
dataFile1.fileName = "AverageVoltageMeasurements_"+calOptions.moduleName
filePath = dataFile1.getFilePath()


with open(filePath, "w") as outFile:

    # Fill header section
    outFile.write("dataRates, ")
    for dataRate in sorted(dataRates) :
        outFile.write("%0.1f, " % dataRate)
    outFile.write("\n")

    outFile.write("channels, ")
    for channel in sorted(rxChannelList1.channels) :
        outFile.write("%d, " % channel)
    outFile.write("\n")

    # End the header section with the keyword Voltages
    outFile.write("Voltages \n")

    # now fill in the arrays
    for dataRate in sorted(dataRates) :
        for channel in sorted(rxChannelList1.channels) :
            commentString = "# Data Rate = %0.0f, Channel = %d \n" % (dataRate, channel)
            outFile.write(commentString)

            # Output target levels
            outFile.write("Target, ")
            for level in sorted(targetLevels) :
                outFile.write("%0.0f, " % level)
            outFile.write("\n")

            # Output measured levels
            outFile.write("Measured, ")
            for level in sorted(targetLevels) :
                outFile.write("%0.4g, " % averageVoltageDict[dataRate][channel][level])
            outFile.write("\n")

    outFile.close()

dataFile1.saveAsResult("AverageVoltageMeasurements")
'''
writeAverageVoltages.wantAllVarsGlobal = False

writeValidationReport.args = ''
writeValidationReport.code = r'''import os
resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "valReport"
folderPath = resultFolderCreator1.run()
FilePathString = "valReport_"+calOptions.moduleName+".csv"
filePath = os.path.join(folderPath, FilePathString)


with open(filePath, "w") as outFile:
    print("Channel, Test Frequency Setting, Target  Value (mV),  Measured Value (mV), Acceptance Limit High (mV), Acceptance Limit Low (mV), PASS/FAIL", file=outFile)
    for dataRate in sorted(dataRates):
        for channel in sorted(rxChannelList1.channels):
            for level in sorted(calOptions.targetLevels):
                acceptance_high = level+ calOptions.Error_mV
                acceptance_low = level- calOptions.Error_mV
                Pass_Fail = "FAIL"

                if abs(level*calOptions.Error_prct/100)>calOptions.Error_mV:
                    acceptance_high = level + abs(level*calOptions.Error_prct/100)
                    acceptance_low = level - abs(level*calOptions.Error_prct/100)

                if averageVoltageDict[dataRate][channel][level]<acceptance_high and averageVoltageDict[dataRate][channel][level]>acceptance_low:
                    Pass_Fail = "PASS"
                print("%d, %0.1f, %0.0f, %0.4g, %0.1f, %0.1f, %s" % (channel, dataRate, level, averageVoltageDict[dataRate][channel][level],acceptance_high,acceptance_low,Pass_Fail), file=outFile)
'''
writeValidationReport.wantAllVarsGlobal = False


eyeScan1.berThreshold = 0.0
eyeScan1.bertDurationInBits = 1024
eyeScan1.endPhase = 125.0
eyeScan1.endVoltage = 409.5
eyeScan1.eyeMask = None
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.patternSync = PATSYNC_strobeSync
eyeScan1.rxChannelList = rxChannelList1
eyeScan1.saveResults = False
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -125.0
eyeScan1.startVoltage = -409.5
eyeScan1.timeUnits = 'picosecond'
eyeScan1.voltageStep = 6.5
eyeScan1.wantResultImages = False

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 6500.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

plotCreator1.codeToSetupPlots = r'''dataRate = args[0]
channel = args[1]
targetLevels = args[2]
dataDict = args[3]
plotTitle = args[4]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']
i = 0
for targetLevel in sorted(targetLevels) :
    index = i % 8
    xVals = list(range(0,128,1))
    yVals = dataDict[dataRate][channel][targetLevel]
    dataSet1 = SvtPlotDataSet(xVals, yVals)
    dataSet1.setColor(colors[index])
    dataSet1.setLineStyle(':')
    dataSet1.setMarker('o',2)
    plotA.addDataSet(dataSet1)
    i = i + 1
plotA.setTitle(plotTitle)
plotA.setYLim([-700.0, 700.0])
'''
plotCreator1.fileName = 'image001'
plotCreator1.folderName = 'PerPhaseDcPlotsBertScan'
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

plotCreator2.codeToSetupPlots = r'''channel = args[0]
dataRates = args[1]
dataDict = args[2]
plotTitle = args[3]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']
i = 0
for dataRate in sorted(dataRates) :
    index = i % 8
    xVals = list()
    yVals = list()
    for targetLevel in sorted( dataDict[dataRate][channel].keys() ) :
        xVals.append(targetLevel)
        yVals.append(dataDict[dataRate][channel][targetLevel])
    dataSet1 = SvtPlotDataSet(xVals, yVals)
    dataSet1.setColor(colors[index])
    dataSet1.setLineStyle(':')
    dataSet1.setMarker('o',2)
    plotA.addDataSet(dataSet1)
    i = i + 1
plotA.setTitle(plotTitle)
plotA.setYLim([-700.0, 700.0])
'''
plotCreator2.fileName = 'image001'
plotCreator2.folderName = 'DataRateTrendPlot'
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

plotCreator3.codeToSetupPlots = r'''channel = args[0]
dataRate = args[1]
dataDict = args[2]
polyDict = args[3]
plotTitle = args[4]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']

xVals = list()
yVals1 = list()
yVals2 = list()
for targetLevel in sorted( dataDict[dataRate][channel].keys() ) :
    xVals.append(targetLevel)
    yVals1.append(dataDict[dataRate][channel][targetLevel])
    polyFitResult = np.polyval(polyDict[dataRate][channel],targetLevel)
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

plotCreator4.codeToSetupPlots = r'''dataRate = args[0]
channel = args[1]
targetLevels = args[2]
dataDict = args[3]
plotTitle = args[4]

colors = ['blue', 'green', 'orange', 'red', 'cyan', 'yellow', 'magenta', 'black']
i = 0
for targetLevel in sorted(targetLevels) :
    index = i % 8
    xVals = list(range(0,128,1))
    yVals = dataDict[dataRate][channel][targetLevel]
    dataSet1 = SvtPlotDataSet(xVals, yVals)
    dataSet1.setColor(colors[index])
    dataSet1.setLineStyle(':')
    dataSet1.setMarker('o',2)
    plotA.addDataSet(dataSet1)
    i = i + 1
plotA.setTitle(plotTitle)
plotA.setYLim([-700.0, 700.0])
'''
plotCreator4.fileName = 'image001'
plotCreator4.folderName = 'PerPhaseDcPlotsVscan'
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

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

resultFolderCreator1.channelProvider = rxChannelList1
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'Generic'

rxChannelList1.channelLabeling = None
rxChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
rxChannelList1.comparatorThresholds = [0.0]
rxChannelList1.equalizationAcGains = [0]
rxChannelList1.equalizationEqGains = [0]
rxChannelList1.expectedPatterns = [PAT_AllZeros]
rxChannelList1.polarities = ['inverted']

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [400.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [PAT_AllZeros]
txChannelList1.polarities = ['inverted']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [1000.0]
txChannelList1.jitterInjection = None
txChannelList1.holdPatternStates = ['idle']

vScan1.bertDurationInBits = 1000000
vScan1.endVoltage = 409.5
vScan1.measurementMode = 'allTransitions'
vScan1.onlyDoSetupOnce = False
vScan1.patternSync = PATSYNC_strobeSync
vScan1.rxChannelList = rxChannelList1
vScan1.rxPhaseOffset = 0.0
vScan1.saveResults = True
vScan1.startVoltage = -409.5
vScan1.wantAnalysis = False
vScan1.wantResultImages = False


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')
#! TEST PROCEDURE
iesp = IESP.getInstance()
iesp.enableVeryPatientMode()

eyeScan1.saveResults = False
if calOptions.saveEyeScans :
    eyeScan1.saveResults = True

formFactor = iesp.__class__.__name__
if formFactor == "SV7C_16C17G":
    dataRates = calOptions.sv7c17DataRates
else:
    dataRates = calOptions.sv7c28DataRates

useActivePatternForSinglePhase = True

thresholdMax = iesp.getLimitMaximum("rxComparatorThreshold")

if not calOptions.usePerPhase and useActivePatternForSinglePhase:
    absTargetLevels = [abs(x) for x in calOptions.targetLevels]
    targetLevelsForMeas = list(dict.fromkeys(absTargetLevels))
else:
    targetLevelsForMeas = calOptions.targetLevels
targetLevels = calOptions.targetLevels

eyeScan1.startVoltage = iesp.getLimitMinimum("rxComparatorThreshold")
eyeScan1.endVoltage = iesp.getLimitMaximum("rxComparatorThreshold")
eyeScan1.voltageStep = iesp.getLimitStep("rxComparatorThreshold")
vScan1.startVoltage = iesp.getLimitMinimum("rxComparatorThreshold")
vScan1.endVoltage = iesp.getLimitMaximum("rxComparatorThreshold")
vScan1.voltageStep = iesp.getLimitStep("rxComparatorThreshold")

vScan1.bertDurationForFindingEye = 1e6
eyeScan1.bertDurationInBits = 1024
eyeScan1.phaseOffsets = [0.0]

# Declare global dictionary of measured values
measuredVoltageDict = dict()
averageVoltageDict = dict()
passfailDict = dict()

globalClockConfig.refClockSyncMode = 'synchronous'

for dataRate in sorted(dataRates) :
    measuredVoltageDict[dataRate] = dict()
    averageVoltageDict[dataRate] = dict()
    passfailDict[dataRate] = dict()

    for channel in range(1,17,1) :
        measuredVoltageDict[dataRate][channel] = dict()
        averageVoltageDict[dataRate][channel] = dict()
        for targetLevel in sorted(targetLevels) :
            measuredVoltageDict[dataRate][channel][targetLevel] = 128*[0.0]
            averageVoltageDict[dataRate][channel][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
measuredPolynomialDict = dict()
averagePolynomialDict = dict()
for dataRate in sorted(dataRates) :
    measuredPolynomialDict[dataRate] = dict()
    averagePolynomialDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredPolynomialDict[dataRate][channel] = dict()
        for phase in range(0,128,1) :
            measuredPolynomialDict[dataRate][channel][phase] = 2*[0.0]
        averagePolynomialDict[dataRate][channel] = 2*[0.0]

valFail = 0

# Start Measurements
for dataRate in sorted(dataRates) :
    print(("----- Measuring at Data Rate %0.0f Mbps -----" % dataRate))
    if dataRate <= 17400:
        txChannelList1.patterns = [PAT_D21_5]
        rxChannelList1.expectedPatterns = [PAT_D21_5]
    else:
        txChannelList1.patterns = [PAT_DIV16]
        rxChannelList1.expectedPatterns = [PAT_DIV16]
    globalClockConfig.dataRate = dataRate
    globalClockConfig.setup()

    for targetLevel in sorted(targetLevelsForMeas) :
        print(("TARGET LEVEL is %d mV" % (targetLevel)))

        (voltagePerPhasePerChannel, averageVoltagePerChannel) = getMeasurementsAtAmplitude(targetLevel)
        for channel in sorted(rxChannelList1.channels) :
            if calOptions.usePerPhase:
                measuredVoltageDict[dataRate][channel][targetLevel] = voltagePerPhasePerChannel[channel]
                averageVoltageDict[dataRate][channel][targetLevel] = averageVoltagePerChannel[channel]
            elif useActivePatternForSinglePhase:
                averageVoltageDict[dataRate][channel][targetLevel] = averageVoltagePerChannel[channel][0]
                averageVoltageDict[dataRate][channel][-1*targetLevel] = averageVoltagePerChannel[channel][1]
            else:
                averageVoltageDict[dataRate][channel][targetLevel] = averageVoltagePerChannel[channel]

# Generate Polynomials
if calOptions.usePerPhase:
    for dataRate in sorted(dataRates) :
        for channel in sorted(rxChannelList1.channels) :
            for phase in range(0,128,1) :
                xVals = list()
                yVals = list()
                for targetLevel in sorted(targetLevels) :
                    yVals.append(measuredVoltageDict[dataRate][channel][targetLevel][phase])
                    xVals.append(targetLevel)
                    if not calOptions.usePerPhase and useActivePatternForSinglePhase:
                        xVals.append(-1*targetLevel)
                polynomialValues = np.polyfit(xVals, yVals, 1) #TODO: add full=True and check leaset squares error
                measuredPolynomialDict[dataRate][channel][phase] = polynomialValues
                slopeError = abs(1-polynomialValues[0])
                if slopeError > 0.15:
                    print(f"Calibration failed on channel {channel} at data rate {dataRate} and phase {phase}")
                    valFail = 1

for dataRate in sorted(dataRates) :
    for channel in sorted(rxChannelList1.channels) :
        xVals = targetLevels
        yVals = list()
        for targetLevel in sorted(targetLevels) :
            yVals.append(averageVoltageDict[dataRate][channel][targetLevel])
        polynomialValues = np.polyfit(xVals, yVals, 1) #TODO: add full=True and check least squares error
        averagePolynomialDict[dataRate][channel] = polynomialValues
        slopeError = abs(1-polynomialValues[0])

        for (xVal,yVal) in zip(xVals,yVals):
            err_acceptance = calOptions.Error_mV
            if abs(xVal*calOptions.Error_prct/100.0)>calOptions.Error_mV:
                err_acceptance = abs(xVal*calOptions.Error_prct/100.0)
            err = abs(xVal-yVal)
            if err > err_acceptance:
                valFail = 1
                print("Calibration failed on channel %d at data rate %d, target level was %0.0f, measured level was %0.0f."%(channel,dataRate,xVal,yVal))
                print("Error in mV = %0.0f, Acceptance limit in mV = %0.0f"%(err,err_acceptance))

        if slopeError > 0.15:
            print("Calibration failed on channel %d at data rate %d" % (channel,dataRate ))
            valFail = 1


generatePlots()
writeAverageVoltages()
writeValidationReport()

if valFail == 0 :
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=filePath, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
elif valFail:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = "file:///" + str(filePath)

    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=filePath, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
newFolderPath = resultFolderCreator1.run()
