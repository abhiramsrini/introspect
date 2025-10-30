# SVT Test
# SVT version 25.1.rc1
# Test saved 2025-04-23_0953
# Form factor: SV7C_16C17G
# PY3
# Checksum: 6f180db2bc8d789f37d83a576eca60fe
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName=None)
computeMean = _create('computeMean', 'SvtFunction', iespName=None)
defineEyeScanRange = _create('defineEyeScanRange', 'SvtFunction', iespName=None)
generatePlots = _create('generatePlots', 'SvtFunction', iespName=None)
generatePolynomial = _create('generatePolynomial', 'SvtFunction', iespName=None)
getEstimatedMeasurementPoint = _create('getEstimatedMeasurementPoint', 'SvtFunction', iespName=None)
getMeasurementsAtAmplitude = _create('getMeasurementsAtAmplitude', 'SvtFunction', iespName=None)
overrideCalCoefficients = _create('overrideCalCoefficients', 'SvtFunction', iespName=None)
pythonModule1 = _create('pythonModule1', 'SvtPythonModule', iespName=None)
pythonModule2 = _create('pythonModule2', 'SvtPythonModule', iespName=None)
writeAverageVoltages = _create('writeAverageVoltages', 'SvtFunction', iespName=None)
writePerPhaseVoltages = _create('writePerPhaseVoltages', 'SvtFunction', iespName=None)
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName=None)

eyeScan1 = _create('eyeScan1', 'SvtEyeScan')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
patternSync1 = _create('patternSync1', 'SvtPatternSync')
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
calOptions.addField('sv7c17DataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0], displayOrder=(0, 2.0))
calOptions.addField('sv7c28DataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0, 26200.0, 26400.0, 26600.0, 26800.0, 27000.0, 27200.0, 27400.0, 27600.0, 27800.0, 28000.0, 28200.0], displayOrder=(0, 3.0))
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[-400.0, -350.0, -300.0, -250.0, -200.0, -150.0, -100.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0], displayOrder=(0, 4.0))
calOptions.addField('usePerPhase', descrip='''''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 5.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.moduleName = '1234'
calOptions.sv7c17DataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0]
calOptions.sv7c28DataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0]
calOptions.targetLevels = [-400.0, -350.0, -300.0, -250.0, -200.0, -150.0, -100.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0]
calOptions.usePerPhase = False
calOptions.callCustomInitMethod()
computeMean.args = 'rising,voltages,errorCountsByVoltage,Phase, channel'
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

defineEyeScanRange.args = 'targetLevel, min=None, max=None'
defineEyeScanRange.code = r'''print(("TARGET LEVEL is %d mV" % (targetLevel)))

if (bool(min) & bool(max)) :
    minLevel = min - 100.0
    if minLevel < rawThresholdMin :
        minLevel = rawThresholdMin
    maxLevel = max + 100.0
    if maxLevel > rawThresholdMax :
        maxLevel = rawThresholdMax
else :
    minLevel = rawThresholdMin
    maxLevel = rawThresholdMax

print(("EYESCAN START is %d mV" % (minLevel)))
print(("EYESCAN END is %d mV" % (maxLevel)))
eyeScan1.startVoltage = minLevel
eyeScan1.endVoltage = maxLevel
vScan1.startVoltage = minLevel
vScan1.endVoltage = maxLevel
'''
defineEyeScanRange.wantAllVarsGlobal = False

generatePlots.args = ''
generatePlots.code = r'''# generate average transfer functions
for dataRate in sorted(dataRates) :
    for channel in sorted(rxChannelList1.channels) :
        titleString = 'Average C Transfer Function at %0.0f MHz, Ch %d' % (dataRate,channel)
        xValues = list()
        yValues = list()
        for targetLevel in sorted(targetLevels) :
            yValues.append(averageCVoltageDict[dataRate][channel][targetLevel])
            xValues.append(targetLevel)
        plotCreator4.xAxisLabel = "Input Voltage"
        plotCreator4.yAxisLabel = "Output Voltage"
        plotCreator4.xValues = xValues
        plotCreator4.yValues = yValues
        plotCreator4.yAxisLimits = [-800.0,800.0]
        plotCreator4.title = titleString
        plotCreator4.folderName = 'AverageCTransferFunctionPlots'
        plotCreator4.fileName = 'DR_%0.0f_MHz_Ch_%d' % (dataRate,channel)
        plotCreator4.run()

if calOptions.usePerPhase:
    for dataRate in sorted(dataRates) :
        for channel in sorted(rxChannelList1.channels) :
            plotCreator1.folderName = 'PerPhaseDcPlotsC'
            titleString = 'Per Phase C Measurements at %0.0f MHz, Ch %d' % (dataRate,channel)
            plotCreator1.run(dataRate, channel,sorted(targetLevels),measuredCVoltageDict,titleString)

for channel in sorted(rxChannelList1.channels) :
    plotCreator2.folderName = 'DataRateTrendPlotC'
    plotCreator2.fileName = 'DR_%0.0f_MHz_Ch_%d' % (dataRate,channel)
    titleString = 'Average C Transfer Functions Across Data Rates, Ch %d' % channel
    plotCreator2.run(channel, sorted(dataRates),averageCVoltageDict, titleString)

for dataRate in sorted(dataRates) :
    for channel in sorted(rxChannelList1.channels) :
        plotCreator3.folderName = 'DataVersusPolyFitC'
        plotCreator3.fileName = 'DR_%0.0f_MHz_Ch_%d' % (dataRate,channel)
        titleString = 'Average C Transfer Function vs Fit, DR = %0.0f, Ch %d' % (dataRate,channel)
        plotCreator3.run(channel, dataRate, averageCVoltageDict, averageCPolynomialDict, titleString)
'''
generatePlots.wantAllVarsGlobal = False

generatePolynomial.args = 'voltageDict, channel, dataRate, phase'
generatePolynomial.code = r'''xVals = list()
yVals = list()
for targetLevel in sorted(targetLevels) :
    xVals.append(targetLevel)
    if phase is None:
        yVals.append(voltageDict[dataRate][channel][targetLevel])
    else:
        yVals.append(voltageDict[dataRate][channel][targetLevel][phase])
    if not calOptions.usePerPhase and useActivePatternForSinglePhase:
        xVals.append(-1*targetLevel)
        yVals.append(voltageDict[dataRate][channel][-1*targetLevel])

[c5, c4, c3, c2, c1, c0] = np.polyfit(xVals,yVals,5)
polyCoeffsOrig = [c5, c4, c3, c2, c1, c0]

xVal = sorted(targetLevels)[0]
polyNegRangeIsGood = False
for m in range(15):
    # Solve for programmed voltage at min raw threshold value
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThresholdMin)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    realRootsInScanRange = [x for x in realRoots if (x > -1*thresholdMax and x < 0)]
    validRealRoots = [x for x in realRoots if (x > rawThresholdMin-100 and x < 100)]

    # Check if at the min raw threshold value there is more than 1 real root in the range the polynomial will be used
    polyInvalidCond1 = len(validRealRoots) == 0
    # Check if at the min raw threshold value there are no real roots that are in the raw threshold range (+100mv buffer). Gain of polynomial is < 1 so this should be true.
    polyInvalidCond2 = len(realRootsInScanRange) > 1

    # Solve for programmed voltage at the raw threshold value that corresponds to the min post cal threshold value
    rawThreshold = np.polyval([c5, c4, c3, c2, c1, c0], -1*thresholdMax)
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThreshold)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    realRootsInScanRange = [x for x in realRoots if (x > -1*thresholdMax and x < 0)]

    # Check if at the min post cal threshold value there is more than 1 real root (we know there is one real root already)
    polyInvalidCond3 = len(realRootsInScanRange) > 1

    # Add estimated measurement point if polynomial is not valid
    if polyInvalidCond1 or polyInvalidCond2 or polyInvalidCond3:
        xVal -= 50
        yVal = getEstimatedMeasurementPoint(xVal, voltageDict, channel, dataRate, phase)
        xVals.append(xVal)
        yVals.append(yVal)
        [c5, c4, c3, c2, c1, c0] = np.polyfit(xVals,yVals,5)
        infoMsg(f"Adding estimated point at x = {xVal}, y = {yVal} to correct real roots on channel {channel}, phase {phase} and data rate {dataRate}")
    else:
        polyNegRangeIsGood = True
        break

xVal = sorted(targetLevels)[-1]
polyPosRangeIsGood = False
for m in range(15):
    # Solve for programmed voltage at max raw threshold value
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThresholdMax)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    realRootsInScanRange = [x for x in realRoots if (x < thresholdMax and x > 0)]
    validRealRoots = [x for x in realRoots if (x < rawThresholdMax+100 and x > -100)]

    # Check if at the max raw threshold value there is more than 1 real root in the range the polynomial will be used
    polyInvalidCond1 = len(validRealRoots) == 0
    # Check if at the max raw threshold value there are no real roots that are in the raw threshold range (+100mv buffer). Gain of polynomial is < 1 so this should be true.
    polyInvalidCond2 = len(realRootsInScanRange) > 1

    # Solve for programmed voltage at the raw threshold value that corresponds to the max post cal threshold value
    rawThreshold = np.polyval([c5, c4, c3, c2, c1, c0], thresholdMax)
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThreshold)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    realRootsInScanRange = [x for x in realRoots if (x < thresholdMax and x > 0)]

    # Check if at the max post cal threshold value there is more than 1 real root (we know there is one real root already)
    polyInvalidCond3 = len(realRootsInScanRange) > 1

    # Add estimated measurement point if polynomial is not valid
    if polyInvalidCond1 or polyInvalidCond2 or polyInvalidCond3:
        xVal += 50
        yVal = getEstimatedMeasurementPoint(xVal, voltageDict, channel, dataRate, phase)
        xVals.append(xVal)
        yVals.append(yVal)
        [c5, c4, c3, c2, c1, c0] = np.polyfit(xVals,yVals,5)
        infoMsg(f"Adding estimated point at x = {xVal}, y = {yVal} to correct real roots on channel {channel}, phase {phase} and data rate {dataRate}")
    else:
        polyPosRangeIsGood = True
        break

largestSigned32Int = 2**31-1
if abs(c0*1000) < 0 or abs(c0*1000) > largestSigned32Int:
    warningMsg(f"Shifted c0 coefficient {c0} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if abs(c1) < 1/(2**28) or abs(c1*(2**28)) > largestSigned32Int:
    warningMsg(f"Shifted c1 coefficient {c1} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if abs(c2) < 1/(2**28) or abs(c2*(2**28)) > largestSigned32Int:
    warningMsg(f"Shifted c2 coefficient {c2} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if abs(c3) < 1/(2**34) or abs(c3*(2**34)) > largestSigned32Int:
    warningMsg(f"Shifted c3 coefficient {c3} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if abs(c4) < 1/(2**44) or abs(c4*(2**44)) > largestSigned32Int:
    warningMsg(f"Shifted c4 coefficient {c4} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if abs(c5) < 1/(2**50) or abs(c5*(2**50)) > largestSigned32Int:
    warningMsg(f"Shifted c5 coefficient {c5} out of range for channel {channel}, phase {phase} and data rate {dataRate}")

if not polyPosRangeIsGood or not polyNegRangeIsGood:
    warningMsg(f"Failed to correct phase {phase} polynomial for channel {channel}, data rate {dataRate}")
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThresholdMin)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    infoMsg(f"Real roots at {rawThresholdMin}: {realRoots}")
    polyCoeffsP = [c5, c4, c3, c2, c1, (c0 - rawThresholdMax)]
    roots = np.roots(polyCoeffsP)
    realRoots = np.real(roots[np.isreal(roots)])
    infoMsg(f"Real roots at {rawThresholdMax}: {realRoots}")
return [c5, c4, c3, c2, c1, c0]
'''
generatePolynomial.wantAllVarsGlobal = False

getEstimatedMeasurementPoint.args = 'requestedLevel, voltageDict, channel, dataRate, phase'
getEstimatedMeasurementPoint.code = r'''if requestedLevel < 0:
    measurementPoint1 = -400
    measurementPoint2 = -200
else:
    measurementPoint1 = 400
    measurementPoint2 = 200

if phase is not None:
    gainEstimate = (voltageDict[dataRate][channel][measurementPoint1][phase]-voltageDict[dataRate][channel][measurementPoint2][phase])/(measurementPoint1-measurementPoint2)
    return voltageDict[dataRate][channel][measurementPoint1][phase]+(requestedLevel+(-1*measurementPoint1))*gainEstimate
else:
    gainEstimate = (voltageDict[dataRate][channel][measurementPoint1]-voltageDict[dataRate][channel][measurementPoint2])/(measurementPoint1-measurementPoint2)
    return voltageDict[dataRate][channel][measurementPoint1]+(requestedLevel+(-1*measurementPoint1))*gainEstimate
'''
getEstimatedMeasurementPoint.wantAllVarsGlobal = False

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
        errCountsAByVoltage = {}
        errCountsBByVoltage = {}
        errCountsCByVoltage = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                phasesByChannel[channel] = result.getPhases(channel)
                errCountsAByVoltage[channel] = result.getErrCountsByVoltage(channel)
                errCountsBByVoltage[channel] = result.getErrCountsByVoltage(channel)
                errCountsCByVoltage[channel] = result.getErrCountsByVoltage(channel)
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

        errCountsCByVoltage = {}
        voltages = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                errCountsCByVoltage[channel] = result.getErrCounts(channel)
                voltages[channel] = result.getVoltages(channel)

    measuredAVoltageDict = dict()
    averageAVoltageForChannel = dict()
    measuredBVoltageDict = dict()
    averageBVoltageForChannel = dict()
    measuredCVoltageDict = dict()
    averageCVoltageForChannel = dict()

    for channel in sorted(rxChannelList1.channels) :
        if calOptions.usePerPhase:
            voltagesA = sorted(errCountsAByVoltage[channel].keys())
            measuredAVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredAVoltageDict[channel].append(computeMean(True,voltagesA,errCountsAByVoltage,phase, channel) )
            averageAVoltageForChannel[channel] = np.average(measuredAVoltageDict[channel])

            voltagesB = sorted(errCountsBByVoltage[channel].keys())
            measuredBVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredBVoltageDict[channel].append(computeMean(True,voltagesB,errCountsBByVoltage,phase, channel) )
            averageBVoltageForChannel[channel] = np.average(measuredBVoltageDict[channel])

            voltagesC = sorted(errCountsCByVoltage[channel].keys())
            measuredCVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredCVoltageDict[channel].append(computeMean(True,voltagesC,errCountsCByVoltage,phase, channel) )
            averageCVoltageForChannel[channel] = np.average(measuredCVoltageDict[channel])
        else:
            voltagesC = voltages[channel]
            if useActivePatternForSinglePhase:
                averageCVoltageForChannel[channel] = (computeMean(True,voltagesC,errCountsCByVoltage,None,channel), computeMean(False,voltagesC,errCountsCByVoltage,None,channel))
            else:
                averageCVoltageForChannel[channel] = computeMean(True,voltagesC,errCountsCByVoltage,None,channel)
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
        errCountsAByVoltage = {}
        errCountsBByVoltage = {}
        errCountsCByVoltage = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                phasesByChannel[channel] = result.getPhases(channel)
                errCountsAByVoltage[channel] = result.getErrCountsByVoltage(channel)
                errCountsBByVoltage[channel] = result.getErrCountsByVoltage(channel)
                errCountsCByVoltage[channel] = result.getErrCountsByVoltage(channel)
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

        errCountsCByVoltage = {}
        voltages = {}
        if result is not None:
            for channel in sorted(rxChannelList1.channels):
                errCountsCByVoltage[channel] = result.getErrCounts(channel)
                voltages[channel] = result.getVoltages(channel)

    measuredAVoltageDict = dict()
    averageAVoltageForChannel = dict()
    measuredBVoltageDict = dict()
    averageBVoltageForChannel = dict()
    measuredCVoltageDict = dict()
    averageCVoltageForChannel = dict()
    for channel in sorted(rxChannelList1.channels) :
        if calOptions.usePerPhase:
            voltagesA = sorted(errCountsAByVoltage[channel].keys())
            measuredAVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredAVoltageDict[channel].append(computeMean(False,voltagesA,errCountsAByVoltage,phase, channel) )
            averageAVoltageForChannel[channel] = np.average(measuredAVoltageDict[channel])

            voltagesB = sorted(errCountsBByVoltage[channel].keys())
            measuredBVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredBVoltageDict[channel].append(computeMean(False,voltagesB,errCountsBByVoltage,phase,channel) )
            averageBVoltageForChannel[channel] = np.average(measuredBVoltageDict[channel])

            voltagesC = sorted(errCountsCByVoltage[channel].keys())
            measuredCVoltageDict[channel] = list()
            for phase in range(0,128,1) :
                measuredCVoltageDict[channel].append(computeMean(False,voltagesC,errCountsCByVoltage,phase,channel) )
            averageCVoltageForChannel[channel] = np.average(measuredCVoltageDict[channel])
        else:
            voltagesC = voltages[channel]
            averageCVoltageForChannel[channel] = computeMean(False,voltagesC,errCountsCByVoltage,None,channel)

return (measuredAVoltageDict, measuredBVoltageDict, measuredCVoltageDict, averageAVoltageForChannel,averageBVoltageForChannel,averageCVoltageForChannel)
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

pythonModule1.wantImportAll = True

pythonModule2.wantImportAll = True

writeAverageVoltages.args = 'temp, folderPath=None'
writeAverageVoltages.code = r'''if temp is True:
    FilePathString = "AverageCVoltageMeasurementsTemp_"+calOptions.moduleName+".csv"
    filePath = os.path.join(folderPath, FilePathString)
else:
    resultFolderCreator1.resultType = "TextReport"
    resultFolderCreator1.folderName = "AverageCVoltageMeasurements"
    folderPath = resultFolderCreator1.run()
    FilePathString = "AverageCVoltageMeasurements_"+calOptions.moduleName+".csv"
    filePath = os.path.join(folderPath, FilePathString)


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
                outFile.write("%0.4g, " % averageCVoltageDict[dataRate][channel][level])
            outFile.write("\n")

    outFile.close()
'''
writeAverageVoltages.wantAllVarsGlobal = False

writePerPhaseVoltages.args = 'temp, folderPath=None'
writePerPhaseVoltages.code = r'''if calOptions.usePerPhase:
    # create csv file output
    if temp is True:
        FilePathString = "PerPhaseAVoltageMeasurementsTemp_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)
    else:
        resultFolderCreator1.resultType = "TextReport"
        resultFolderCreator1.folderName = "PerPhaseAVoltageMeasurements"
        folderPath = resultFolderCreator1.run()
        FilePathString = "PerPhaseAVoltageMeasurements_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)

    with open(filePath, "w") as outFile:
        # now fill in the arrays
        for dataRate in sorted(dataRates) :
            for channel in sorted(rxChannelList1.channels) :

                for phase in range(128) :
                    # Output measured levels
                    for level in sorted(targetLevels) :
                        outFile.write("%0.4g, " % measuredAVoltageDict[dataRate][channel][level][phase])
                    outFile.write("\n")

        outFile.close()

    if temp is True:
        FilePathString = "PerPhaseBVoltageMeasurementsTemp_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)
    else:
        resultFolderCreator1.resultType = "TextReport"
        resultFolderCreator1.folderName = "PerPhaseBVoltageMeasurements"
        folderPath = resultFolderCreator1.run()
        FilePathString = "PerPhaseBVoltageMeasurements_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)

    with open(filePath, "w") as outFile:
        # now fill in the arrays
        for dataRate in sorted(dataRates) :
            for channel in sorted(rxChannelList1.channels) :

                for phase in range(128) :
                    # Output measured levels
                    for level in sorted(targetLevels) :
                        outFile.write("%0.4g, " % measuredBVoltageDict[dataRate][channel][level][phase])
                    outFile.write("\n")

        outFile.close()

    if temp is True:
        FilePathString = "PerPhaseCVoltageMeasurementsTemp_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)
    else:
        resultFolderCreator1.resultType = "TextReport"
        resultFolderCreator1.folderName = "PerPhaseCVoltageMeasurements"
        folderPath = resultFolderCreator1.run()
        FilePathString = "PerPhaseCVoltageMeasurements_"+calOptions.moduleName+".txt"
        filePath = os.path.join(folderPath, FilePathString)

    with open(filePath, "w") as outFile:
        # now fill in the arrays
        for dataRate in sorted(dataRates) :
            for channel in sorted(rxChannelList1.channels) :

                for phase in range(128) :
                    # Output measured levels
                    for level in sorted(targetLevels) :
                        outFile.write("%0.4g, " % measuredCVoltageDict[dataRate][channel][level][phase])
                    outFile.write("\n")

        outFile.close()
'''
writePerPhaseVoltages.wantAllVarsGlobal = False

writeTransferFunctions.args = 'temp, folderPath=None'
writeTransferFunctions.code = r'''# create csv file output
import datetime
now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

if temp is True:
    FilePathString = "rxVoltageThresholdCalTemp_"+calOptions.moduleName+".txt"
    filePath = os.path.join(folderPath, FilePathString)
else:
    resultFolderCreator1.resultType = "TextReport"
    resultFolderCreator1.folderName = "rxVoltageThresholdCal"
    folderPath = resultFolderCreator1.run()

    FilePathString = "rxVoltageThresholdCal_"+calOptions.moduleName+".txt"
    filePath = os.path.join(folderPath, FilePathString)

commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]

with open(filePath, "w") as outFile:

    # Fill header section
    outFile.write("BEGIN SECTION \n")
    outFile.write("section type : header \n")
    outFile.write("serial number : "+calOptions.moduleName+"\n")
    outFile.write("hardware revision : Rev0 \n")
    outFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    outFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    outFile.write("END SECTION \n")
    outFile.write("\n")

    # Fill rx header section
    outFile.write("BEGIN SECTION \n")
    outFile.write("section type : rx_thresh_volt_cal_avg_data \n")

    # now fill in the arrays
    for dataRate in allDataRates :
        commentString = "# Data Rate = %0.0f \n" % (dataRate)
        outFile.write(commentString)
        #print offset, m1, m2, m3, m4, m5
        for i in range(5,-1,-1) :
                outFile.write(commentArray[i]+"\n")
                #output average polynomial
                for channel in range(1,17,1) :
                    #case 5 is offset. needs to be in uV
                    if dataRate <= calOptions.sv7c28DataRates[-1]:
                        if i == 5:
                            value =  averageCPolynomialDict[dataRate][channel][i] * 1000
                        else:
                            value =  averageCPolynomialDict[dataRate][channel][i]
                    else:
                        if i == 5:
                            value =  averageCPolynomialDict[calOptions.sv7c28DataRates[-1]][channel][i] * 1000
                        else:
                            value =  averageCPolynomialDict[calOptions.sv7c28DataRates[-1]][channel][i]
                    outFile.write("%0.10g, " % value)
                outFile.write("\n")

    outFile.write("END SECTION \n")
    outFile.write("\n")

    if calOptions.usePerPhase:
        # Fill rx header section
        outFile.write("BEGIN SECTION \n")
        outFile.write("section type : rx_thresh_volt_cal_even_data \n")


        # now fill in the arrays
        for dataRate in allDataRates :
            commentString = "# Data Rate = %0.0f \n" % (dataRate)
            outFile.write(commentString)
            #print offset, m1, m2, m3, m4, m5
            for i in range(5,-1,-1) :
                    outFile.write(commentArray[i]+"\n")
                    #output average polynomial
                    for channel in range(1,17,1) :
                        #case 5 is offset. needs to be in uV
                        if i == 5:
                            value =  averageAPolynomialDict[dataRate][channel][i] * 1000
                        else:
                            value =  averageAPolynomialDict[dataRate][channel][i]
                        outFile.write("%0.10g, " % value)
                    outFile.write("\n")
                    #output polynomial per phase
                    for phase in range(0,128,1):
                        for channel in range(1,17,1) :
                            if i == 5:
                                value =  measuredAPolynomialDict[dataRate][channel][phase][i] * 1000
                            else:
                                value = measuredAPolynomialDict[dataRate][channel][phase][i]
                            outFile.write("%0.10g, " % value)
                        outFile.write("\n")

        outFile.write("END SECTION \n")
        outFile.write("\n")

        # Fill rx header section
        outFile.write("BEGIN SECTION \n")
        outFile.write("section type : rx_thresh_volt_cal_odd_data \n")


        # now fill in the arrays
        for dataRate in allDataRates :
            commentString = "# Data Rate = %0.0f \n" % (dataRate)
            outFile.write(commentString)
            #print offset, m1, m2, m3, m4, m5
            for i in range(5,-1,-1) :
                    outFile.write(commentArray[i]+"\n")
                    #output average polynomial
                    for channel in range(1,17,1) :
                        #case 5 is offset. needs to be in uV
                        if i == 5:
                            value =  averageBPolynomialDict[dataRate][channel][i] * 1000
                        else:
                            value =  averageBPolynomialDict[dataRate][channel][i]
                        outFile.write("%0.10g, " % value)
                    outFile.write("\n")
                    #output polynomial per phase
                    for phase in range(0,128,1):
                        for channel in range(1,17,1) :
                            if i == 5:
                                value =  measuredBPolynomialDict[dataRate][channel][phase][i] * 1000
                            else:
                                value = measuredBPolynomialDict[dataRate][channel][phase][i]
                            outFile.write("%0.10g, " % value)
                        outFile.write("\n")

        outFile.write("END SECTION \n")

    outFile.close()
'''
writeTransferFunctions.wantAllVarsGlobal = False


eyeScan1.berThreshold = 0.0
eyeScan1.bertDurationInBits = 1024
eyeScan1.endPhase = 62.5
eyeScan1.endVoltage = 620.0
eyeScan1.eyeMask = None
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.patternSync = patternSync1
eyeScan1.rxChannelList = rxChannelList1
eyeScan1.saveResults = True
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -62.5
eyeScan1.startVoltage = -620.0
eyeScan1.timeUnits = 'picosecond'
eyeScan1.voltageStep = 20.0
eyeScan1.wantResultImages = False

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 16000.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

patternSync1.autoDiagnoseSyncFailure = True
patternSync1.durationInBits = 100000
patternSync1.errorIfSyncFails = False
patternSync1.errorTolerance = 0.0003
patternSync1.rxChannelList = None
patternSync1.standAlone = False
patternSync1.syncMethod = 'strobeSync'
patternSync1.syncMode = 'standard'
patternSync1.targetPhases = [0.0]
patternSync1.targetVoltages = [0.0]
patternSync1.voltageScanHeight = 500.0
patternSync1.wantRestoreVoltagesAfterSync = True

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
plotA.setYLim([-900.0, 900.0])
'''
plotCreator1.fileName = 'image001'
plotCreator1.folderName = 'PerPhaseDcPlots'
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

plotCreator4.codeToSetupPlots = r'''""" Example code:
xvals = arange(0, 10, 0.1)
yvals = sin(xvals)
dataSet1 = SvtPlotDataSet(xvals, yvals)
dataSet1.setColor('orange')
dataSet1.setLineStyle(':', 4)
plotA.addDataSet(dataSet1)
"""
'''
plotCreator4.fileName = 'image001'
plotCreator4.folderName = 'PlotCreatorImages'
plotCreator4.grid = True
plotCreator4.layout = 'A'
plotCreator4.plotColors = ['Auto']
plotCreator4.plotType = 'scatter'
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

resultFolderCreator1.channelProvider = None
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
vScan1.endVoltage = 620.0
vScan1.measurementMode = 'allTransitions'
vScan1.onlyDoSetupOnce = False
vScan1.patternSync = patternSync1
vScan1.rxChannelList = rxChannelList1
vScan1.rxPhaseOffset = 0.0
vScan1.saveResults = True
vScan1.startVoltage = -620.0
vScan1.wantAnalysis = False
vScan1.wantResultImages = False


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')
#! TEST PROCEDURE
import os
iesp = IESP.getInstance()
iesp.enableVeryPatientMode()

eyeScan1.phaseOffsets = [0.0]
vScan1.bertDurationForFindingEye = 1e6

rawThresholdMin = iesp.getLimitMinimum("rxComparatorThresholdRaw")
rawThresholdMax = iesp.getLimitMaximum("rxComparatorThresholdRaw")
rawThresholdStep = iesp.getLimitStep("rxComparatorThresholdRaw")
iesp.setLimitMaximum("rxComparatorThreshold", rawThresholdMax)
iesp.setLimitMinimum("rxComparatorThreshold", rawThresholdMin)
iesp.setLimitStep("rxComparatorThreshold", rawThresholdStep)

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure the module is calibrated for TX but use the default RX TG,  RX Alignment and RX Threshold"
waitForGuiOkDialog(myString)

formFactor = iesp.__class__.__name__
if formFactor == "SV7C_16C17G":
    dataRates = calOptions.sv7c17DataRates
else:
    dataRates = calOptions.sv7c28DataRates

allDataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0, 26200.0, 26400.0, 26600.0, 26800.0, 27000.0, 27200.0, 27400.0, 27600.0, 27800.0, 28000.0, 28200.0]

useActivePatternForSinglePhase = True

thresholdMax = iesp.getLimitMaximum("rxComparatorThreshold")

targetLevels = calOptions.targetLevels
if not calOptions.usePerPhase and useActivePatternForSinglePhase:
    absTargetLevels = [abs(x) for x in targetLevels]
    targetLevelsToMeasure = list(dict.fromkeys(absTargetLevels))
else:
    targetLevelsToMeasure = targetLevels

# Declare global dictionary of measured values
measuredAVoltageDict = dict()
averageAVoltageDict = dict()
for dataRate in allDataRates :
    measuredAVoltageDict[dataRate] = dict()
    averageAVoltageDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredAVoltageDict[dataRate][channel] = dict()
        averageAVoltageDict[dataRate][channel] = dict()
        for targetLevel in sorted(targetLevels) :
            measuredAVoltageDict[dataRate][channel][targetLevel] = 128*[0.0]
            averageAVoltageDict[dataRate][channel][targetLevel] = 0.0

measuredBVoltageDict = dict()
averageBVoltageDict = dict()
for dataRate in allDataRates :
    measuredBVoltageDict[dataRate] = dict()
    averageBVoltageDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredBVoltageDict[dataRate][channel] = dict()
        averageBVoltageDict[dataRate][channel] = dict()
        for targetLevel in sorted(targetLevels) :
            measuredBVoltageDict[dataRate][channel][targetLevel] = 128*[0.0]
            averageBVoltageDict[dataRate][channel][targetLevel] = 0.0

measuredCVoltageDict = dict()
averageCVoltageDict = dict()
for dataRate in allDataRates :
    measuredCVoltageDict[dataRate] = dict()
    averageCVoltageDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredCVoltageDict[dataRate][channel] = dict()
        averageCVoltageDict[dataRate][channel] = dict()
        for targetLevel in sorted(targetLevels) :
            measuredCVoltageDict[dataRate][channel][targetLevel] = 128*[0.0]
            averageCVoltageDict[dataRate][channel][targetLevel] = 0.0

# Declare global dictionary of transfer functions expressed as fifth order polynomials
measuredAPolynomialDict = dict()
averageAPolynomialDict = dict()
for dataRate in allDataRates :
    measuredAPolynomialDict[dataRate] = dict()
    averageAPolynomialDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredAPolynomialDict[dataRate][channel] = dict()
        for phase in range(0,128,1) :
            measuredAPolynomialDict[dataRate][channel][phase] = [0.0,0.0,0.0,0.0,1.0,0.0]
        averageAPolynomialDict[dataRate][channel] = [0.0,0.0,0.0,0.0,1.0,0.0]

measuredBPolynomialDict = dict()
averageBPolynomialDict = dict()
for dataRate in allDataRates :
    measuredBPolynomialDict[dataRate] = dict()
    averageBPolynomialDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredBPolynomialDict[dataRate][channel] = dict()
        for phase in range(0,128,1) :
            measuredBPolynomialDict[dataRate][channel][phase] = [0.0,0.0,0.0,0.0,1.0,0.0]
        averageBPolynomialDict[dataRate][channel] = [0.0,0.0,0.0,0.0,1.0,0.0]

measuredCPolynomialDict = dict()
averageCPolynomialDict = dict()
for dataRate in allDataRates :
    measuredCPolynomialDict[dataRate] = dict()
    averageCPolynomialDict[dataRate] = dict()
    for channel in range(1,17,1) :
        measuredCPolynomialDict[dataRate][channel] = dict()
        for phase in range(0,128,1) :
            measuredCPolynomialDict[dataRate][channel][phase] = [0.0,0.0,0.0,0.0,1.0,0.0]
        averageCPolynomialDict[dataRate][channel] = [0.0,0.0,0.0,0.0,1.0,0.0]

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "AverageVoltageMeasurementsTemp"
averageVoltagesTempFolderPath = resultFolderCreator1.run()

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "PerPhaseVoltageMeasurementsTemp"
perPhaseVoltagesTempFolderPath = resultFolderCreator1.run()

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "rxVoltageThresholdCalTemp"
transferFunctionsTempFolderPath = resultFolderCreator1.run()

# Start Measurements
for dataRate in sorted(dataRates) :
    if not calOptions.usePerPhase and useActivePatternForSinglePhase:
        if dataRate <= 17400:
            txChannelList1.patterns = [PAT_D21_5]
            rxChannelList1.expectedPatterns = [PAT_D21_5]
        else:
            txChannelList1.patterns = [PAT_DIV16]
            rxChannelList1.expectedPatterns = [PAT_DIV16]

    print(("----- Measuring at Data Rate %0.0f Mbps -----" % dataRate))
    globalClockConfig.dataRate = dataRate
    globalClockConfig.setup()

    if formFactor == "SV7C_16C17G" and calOptions.usePerPhase:
        # Zero out alignment phases after each clock commit
        iesp.zeroOutRxAutoAlignPhases()
        iesp.waitForCommandProcessors()
    #use raw threshold range
    iesp.writeSubPartRegister(0x0980, None, 1)

    #overrideCalCoefficients()

    dataRateIndex = sorted(dataRates).index(dataRate)
    if (dataRateIndex > 0) :
        previousRate = sorted(dataRates)[dataRateIndex-1]
    else :
        previousRate = None

    for targetLevel in targetLevelsToMeasure :
        if (previousRate) :
            measuredVoltages = []
            for channel in sorted(rxChannelList1.channels) :
                measuredVoltages.extend(measuredAVoltageDict[previousRate][channel][targetLevel])
                measuredVoltages.extend(measuredBVoltageDict[previousRate][channel][targetLevel])
            defineEyeScanRange(targetLevel, min(measuredVoltages), max(measuredVoltages))
        else :
            defineEyeScanRange(targetLevel)
        (voltageAPerPhasePerChannel, voltageBPerPhasePerChannel,voltageCPerPhasePerChannel, averageAVoltagePerChannel,averageBVoltagePerChannel,averageCVoltagePerChannel) = getMeasurementsAtAmplitude(targetLevel)

        for channel in sorted(rxChannelList1.channels) :
            if calOptions.usePerPhase:
                measuredAVoltageDict[dataRate][channel][targetLevel] = voltageAPerPhasePerChannel[channel]
                averageAVoltageDict[dataRate][channel][targetLevel] = averageAVoltagePerChannel[channel]
                measuredBVoltageDict[dataRate][channel][targetLevel] = voltageBPerPhasePerChannel[channel]
                averageBVoltageDict[dataRate][channel][targetLevel] = averageBVoltagePerChannel[channel]
                measuredCVoltageDict[dataRate][channel][targetLevel] = voltageCPerPhasePerChannel[channel]

            if not calOptions.usePerPhase and useActivePatternForSinglePhase:
                averageCVoltageDict[dataRate][channel][targetLevel] = averageCVoltagePerChannel[channel][0]
                averageCVoltageDict[dataRate][channel][-1*targetLevel] = averageCVoltagePerChannel[channel][1]
            else:
                averageCVoltageDict[dataRate][channel][targetLevel] = averageCVoltagePerChannel[channel]

    # Generate Polynomials
    if calOptions.usePerPhase:
        for channel in sorted(rxChannelList1.channels) :
            for phase in range(0,128,1) :
                measuredAPolynomialDict[dataRate][channel][phase] = generatePolynomial(measuredAVoltageDict, channel, dataRate, phase)

            for phase in range(0,128,1) :
                measuredBPolynomialDict[dataRate][channel][phase] = generatePolynomial(measuredBVoltageDict, channel, dataRate, phase)

            for phase in range(0,128,1) :
                measuredCPolynomialDict[dataRate][channel][phase] = generatePolynomial(measuredCVoltageDict, channel, dataRate, phase)

        for channel in sorted(rxChannelList1.channels) :
            averageAPolynomialDict[dataRate][channel] = generatePolynomial(averageAVoltageDict, channel, dataRate, None)

        for channel in sorted(rxChannelList1.channels) :
            averageBPolynomialDict[dataRate][channel] = generatePolynomial(averageBVoltageDict, channel, dataRate, None)

    for channel in sorted(rxChannelList1.channels) :
        averageCPolynomialDict[dataRate][channel] = generatePolynomial(averageCVoltageDict, channel, dataRate, None)

    writeTransferFunctions(True, transferFunctionsTempFolderPath)
    writePerPhaseVoltages(True, perPhaseVoltagesTempFolderPath)
    writeAverageVoltages(True, averageVoltagesTempFolderPath)


iesp.setLimitMaximum("rxComparatorThreshold", 418.5)
iesp.setLimitMinimum("rxComparatorThreshold", -418.5)
iesp.setLimitStep("rxComparatorThreshold", 13.5)

generatePlots()
writeAverageVoltages(False)
writeNoteForTestRun(calOptions.moduleName)
writePerPhaseVoltages(False)
writeTransferFunctions(False)
