# SVT Test
# SVT version 23.2.b2
# Test saved 2023-02-21_2137
# Form factor: SV7C_16C17G
# PY3
# Checksum: f9350e0ca5bc7bda524ec85a0f1462e9
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


calOptions = _create('calOptions', 'SvtDataRecord', iespName='None')
dataFile1 = _create('dataFile1', 'SvtDataFile', iespName='None')

bertScan1 = _create('bertScan1', 'SvtBertScanVNL')
globalClockConfig = _create('globalClockConfig', 'SvtGlobalClockConfig')
jitterInjection1 = _create('jitterInjection1', 'SvtJitterInjection')
plotCreatorBasic1 = _create('plotCreatorBasic1', 'SvtPlotCreatorBasic')
plotCreatorBasic2 = _create('plotCreatorBasic2', 'SvtPlotCreatorBasic')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
rxChannelList1 = _create('rxChannelList1', 'SvtRxChannelList')
txChannelList1 = _create('txChannelList1', 'SvtTxChannelList')
userPattern1 = _create('userPattern1', 'SvtUserPattern')

calOptions.addField('sv7c17DataRates', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0], displayOrder=(0, 1.0))
calOptions.addField('sv7c28DataRates', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0, 26200.0, 26400.0, 26600.0, 26800.0, 27000.0, 27200.0, 27400.0, 27600.0, 27800.0, 28000.0, 28200.0], displayOrder=(0, 2.0))
calOptions.addField('moduleName', descrip='''''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 3.0))
calOptions.addField('calChannels', descrip='''List of channels to calibrate''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], displayOrder=(0, 4.0))
calOptions.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calOptions.sv7c17DataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0]
calOptions.sv7c28DataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0, 26200.0, 26400.0, 26600.0, 26800.0, 27000.0, 27200.0, 27400.0, 27600.0, 27800.0, 28000.0, 28200.0]
calOptions.moduleName = '1234'
calOptions.calChannels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
calOptions.callCustomInitMethod()
dataFile1.delimiter = ','
dataFile1.fileName = 'phaseTransferFunctions.csv'
dataFile1.numFields = 128
dataFile1.otherFolderPath = r'None'
dataFile1.parentFolder = 'Results'


bertScan1.bertDurationInBits = 2000000
bertScan1.endPhase = 194.805194805
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = True
bertScan1.patternSync = PATSYNC_strobeSync
bertScan1.phaseOffsets = [0.0]
bertScan1.rxChannelList = rxChannelList1
bertScan1.saveResults = False
bertScan1.startPhase = 0.0
bertScan1.timeUnits = 'picosecond'
bertScan1.wantAnalysis = True
bertScan1.wantResultImages = False

globalClockConfig.clockRecoveryChannel = 1
globalClockConfig.dataRate = 7700.0
globalClockConfig.refClockSyncMode = 'synchronous'
globalClockConfig.referenceClocks = refClocksConfig
globalClockConfig.sscEnabled = False
globalClockConfig.sscFrequency = 50.0
globalClockConfig.sscSpread = 1.0

jitterInjection1.rjAmplitude = 0.0
jitterInjection1.sj1Amplitude = 300.0
jitterInjection1.sj1Frequency = 0.3
jitterInjection1.timeUnits = 'picosecond'
jitterInjection1.voltageNoise = 'off'
jitterInjection1.voltageNoiseAmplitudeCommon = 20.0
jitterInjection1.voltageNoiseAmplitudeDifferential = 40.0

plotCreatorBasic1.plotColors = ['Auto']
plotCreatorBasic1.plotType = 'line'
plotCreatorBasic1.title = ''
plotCreatorBasic1.xAxisLabel = ''
plotCreatorBasic1.xAxisScale = 'linear'
plotCreatorBasic1.xValues = r'''
phaseSteps
'''
plotCreatorBasic1.yAxisLabel = ''
plotCreatorBasic1.yAxisScale = 'linear'
plotCreatorBasic1.yValues = r'''
finalPhaseStepTf
'''

plotCreatorBasic2.plotColors = ['Auto']
plotCreatorBasic2.plotType = 'bar'
plotCreatorBasic2.title = ''
plotCreatorBasic2.xAxisLabel = ''
plotCreatorBasic2.xAxisScale = 'linear'
plotCreatorBasic2.xValues = r'''

'''
plotCreatorBasic2.yAxisLabel = ''
plotCreatorBasic2.yAxisScale = 'linear'
plotCreatorBasic2.yValues = r'''
histogram
'''

refClocksConfig.externRefClockFreq = 250.0
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

rxChannelList1.channelLabeling = None
rxChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
rxChannelList1.comparatorThresholds = [0.0]
rxChannelList1.equalizationAcGains = [0]
rxChannelList1.equalizationDcGains = [0]
rxChannelList1.equalizationEqGains = [0]
rxChannelList1.expectedPatterns = [userPattern1]
rxChannelList1.polarities = ['normal']
rxChannelList1.rxClockModes = ['system']

txChannelList1.busPatternTimeline = None
txChannelList1.channelLabeling = None
txChannelList1.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
txChannelList1.coarseSkews = [0.0]
txChannelList1.commonModeVoltages = [400.0]
txChannelList1.fineSkews = [0.0]
txChannelList1.patternMode = 'standard'
txChannelList1.patterns = [userPattern1]
txChannelList1.polarities = ['normal']
txChannelList1.preEmphasis = None
txChannelList1.voltageSwings = [800.0]
txChannelList1.jitterInjection = [jitterInjection1]
txChannelList1.holdPatternStates = ['idle']

userPattern1.bits = '00001111'
userPattern1.notes = ''


# NOTE: 'setSharedProperty' is only for use when loading a Test
# NOTE: 'setSharedProperty' is only for use when loading a Test
SvtTxChannelList.setSharedProperty('altABits', '11111111')
SvtTxChannelList.setSharedProperty('altBBits', '00000000')
#! TEST PROCEDURE
import datetime
iesp = IESP.getInstance()
iesp.setMeasurementTimeout(900000)
txChannelList1.channels = calOptions.calChannels
rxChannelList1.channels = calOptions.calChannels

allDataRates = [8800.0, 9000.0, 9200.0, 9400.0, 9600.0, 9800.0, 10000.0, 10200.0, 10400.0, 10600.0, 10800.0, 11000.0, 11200.0, 11400.0, 11600.0, 11800.0, 12000.0, 12200.0, 12400.0, 12600.0, 12800.0, 13000.0, 13200.0, 13400.0, 13600.0, 13800.0, 14000.0, 14200.0, 14400.0, 14600.0, 14800.0, 15000.0, 15200.0, 15400.0, 15600.0, 15800.0, 16000.0, 16200.0, 16400.0, 16600.0, 16800.0, 17000.0, 17200.0, 17400.0, 17600.0, 17800.0, 18000.0, 18200.0, 18400.0, 18600.0, 18800.0, 19000.0, 19200.0, 19400.0, 19600.0, 19800.0, 20000.0, 20200.0, 20400.0, 20600.0, 20800.0, 21000.0, 21200.0, 21400.0, 21600.0, 21800.0, 22000.0, 22200.0, 22400.0, 22600.0, 22800.0, 23000.0, 23200.0, 23400.0, 23600.0, 23800.0, 24000.0, 24200.0, 24400.0, 24600.0, 24800.0, 25000.0, 25200.0, 25400.0, 25600.0, 25800.0, 26000.0, 26200.0, 26400.0, 26600.0, 26800.0, 27000.0, 27200.0, 27400.0, 27600.0, 27800.0, 28000.0, 28200.0]

formFactor = iesp.__class__.__name__
if formFactor == "SV7C_16C17G":
    dataRates = calOptions.sv7c17DataRates
else:
    dataRates = calOptions.sv7c28DataRates


allFinalPhaseStepTfs = dict()
for dataRate in allDataRates :
    allFinalPhaseStepTfs[dataRate] = dict()
    for channel in range(1,17,1):
        #put default value (cannot be 0)
        allFinalPhaseStepTfs[dataRate][channel] = [0.00000000,0.53864323,1.18356141,1.88222397,2.50664620,3.18388261,3.85910373,4.35871516,5.01386466,5.98765263,6.95825756,8.13917731,9.66570244,11.52490493,13.46296920,15.64160039,18.15597556,20.41784919,22.51492375,24.10144447,25.68665694,26.89107697,27.82443911,28.71916900,29.31657843,29.92787466,30.53549718,31.15679560,31.63344386,31.94733928,32.02854520,32.21338162,32.23191934,32.50485829,32.98713553,33.56486558,34.23638577,34.70762624,35.24149306,35.90294352,36.45208692,37.23345906,38.19212562,39.30921569,40.77740243,42.55567890,45.20225036,47.85865686,50.38793616,52.55430156,54.53498460,56.07105956,57.60450742,58.97731732,60.22078273,61.20154143,62.03343721,62.69456752,63.05762305,63.41425137,63.73890761,63.92798530,64.26604532,64.59730499,64.83163660,65.12926644,65.44207376,65.81223873,66.15229104,66.59140769,67.06731522,67.68553777,68.50452925,69.33645862,70.40326176,71.72248210,73.43317742,75.47452518,77.76554491,80.00691382,82.28740290,84.21731769,86.04645510,87.67579028,89.12186517,90.15599383,91.23087345,92.14410794,92.99828879,93.74388797,94.18133361,94.66515699,95.04467151,95.27064368,95.61381999,95.69950709,95.83085587,96.14736384,96.54045384,96.98571937,97.52656123,98.04451908,98.42235739,98.89102114,99.46974178,100.29261875,101.34835851,102.64553274,104.43223044,106.41086418,108.93228509,111.70151310,114.74850778,117.32819848,119.56318431,121.14425927,122.35271129,123.46198284,124.50148532,125.33060892,126.13823117,126.77317978,127.23918930,127.50054164,127.73397483,127.81173782,127.82962399,127.87052016]

bertErrorsByChannel = dict()
for channel in range(1,17,1) :
    bertErrorsByChannel[channel] = []


for dataRate in sorted(dataRates) :
    badDataRate = 1
    while badDataRate == 1:
        badDataRate = 0
        globalClockConfig.dataRate = dataRate
        uiWidthInPs = (1/dataRate)*1000000
        phaseStepInPs = uiWidthInPs/64
        jitterAmplitudeInPs = 160*phaseStepInPs
        #print("jitter amplitude:", jitterAmplitudeInPs)
        bertScanEndPhase = 6*uiWidthInPs-phaseStepInPs
        bertScanStartPhase = 0

        globalClockConfig.setup()
        print(("data rate:", iesp.getDataRate()))
        iesp.setTxToRxLoopbackState(True, calOptions.calChannels)
        jitterInjection1.sj1Amplitude = 0 #jitter injection stop
        txChannelList1.setup()

        if formFactor == "SV7C_16C17G":
            # Zero out rx alignment phases
            iesp.writeSubPartRegister(0x0462, None, 0x00000001)
            iesp.waitForCommandProcessors()

        # Now perform data collection and analysis
        bertScan1.startPhase = bertScanStartPhase
        bertScan1.endPhase = bertScanEndPhase
        bertScan1.measurementMode = 'singleEdge'
        bertScan1.wantDoubleMode = False
        bertScan1.setup()
        jitterInjection1.sj1Amplitude = jitterAmplitudeInPs #jitter injection start
        txChannelList1.update()
        result = bertScan1.run()
        channels = result.getChannels()
        for channel in sorted(channels) :
            bertErrorsByChannel[channel] = result.getErrCounts(channel)


        for channel in sorted(calOptions.calChannels) :
            errCounts = bertErrorsByChannel[channel]
            phases = result.getPhases(channel);

            # Find left edge
            indices = np.nonzero(np.array(errCounts)==0)
            if len(indices[0]) == 0:
                print("ERROR restart datarate - No region of BER=0")
                badDataRate = 1
            else:
                histogramLeftEdge = max(indices[0])

                phasesTruncLeft = phases[histogramLeftEdge:]
                errorCountsTruncLeft = errCounts[histogramLeftEdge:]

                # Find right edge
                maxCount = max(errCounts)
                indices = np.nonzero(np.array(errorCountsTruncLeft)==maxCount)
                histogramRightEdge = min(indices[0])

                phasesBathtubEdgeTrunc = phasesTruncLeft[0:histogramRightEdge+1]
                errorCountsBathtubEdgeTrunc = errorCountsTruncLeft[0:histogramRightEdge+1]

                # Histogram
                histogram = np.diff(errorCountsBathtubEdgeTrunc) # this returns a shorter array, offset by 1 to the right

                # Linearize the sinuoidal jitter component
                transitions = list()
                for j in range(len(list(histogram))) :
                  T = -1*np.cos(np.pi*errorCountsBathtubEdgeTrunc[j]/maxCount)
                  transitions.append(T)

                linearizedHistogram = np.diff(transitions)

                # Truncate right side to UI width
                phasesTruncLeft = phasesBathtubEdgeTrunc[int(len(phasesBathtubEdgeTrunc)/2)-64:]
                linearizedHistogramTruncLeft = linearizedHistogram[int(len(linearizedHistogram)/2)-64:]
                phase2UITrunc = phasesTruncLeft[0:128]
                linearizedHistogram2UITrunc = linearizedHistogramTruncLeft[0:128]

                # Find DNL
                lsb = sum(np.array(linearizedHistogram2UITrunc)) / len(linearizedHistogram2UITrunc)
                dnl = list()
                dnl.append(0)
                for l in range(len(linearizedHistogram2UITrunc)) :
                  dnl.append(linearizedHistogram2UITrunc[l]/lsb-1)

                # Find INL
                inl = np.cumsum(np.array(dnl))

                # Find final transfer function - expected phase vs actual phase
                phaseTf = list()
                for i in range(128) :
                    phaseTf.append(phase2UITrunc[i] + inl[i]*phaseStepInPs)

                phaseSteps = np.linspace(0, 127, 128);

                # Move the phase transfer function so it ranges from phase step 0 to 127
                phase2UITruncStart = np.nonzero(np.array(phases) == phase2UITrunc[0])
                phaseTfExpandedRange = [x - (phaseStepInPs*64*2) for x in phaseTf] + phaseTf
                phasesExpandedRange = phases[phase2UITruncStart[0][0]-128:phase2UITruncStart[0][0]+128]
                phaseStep0p1 = np.nonzero(np.array([round(np.mod(x, phaseStepInPs*128), 0) for x in phasesExpandedRange]) == 0)
                phaseStep0p2 = np.nonzero(np.array([round(np.mod(x, phaseStepInPs*128), 0) for x in phasesExpandedRange]) == round(phaseStepInPs*128, 0))
                if len(np.hstack((phaseStep0p1[0], phaseStep0p2[0]))) == 0:
                    print("ERROR restart datarate")
                    badDataRate = 1
                else:

                    phaseStep0 = min(np.hstack((phaseStep0p1[0], phaseStep0p2[0])))
                    finalPhaseTf = [x-phaseTfExpandedRange[phaseStep0] for x in phaseTfExpandedRange[phaseStep0:phaseStep0+128]]
                    finalPhaseStepTf = [x/phaseStepInPs for x in finalPhaseTf]
                    negTfVals = np.nonzero(np.array(finalPhaseStepTf) < 0)
                    if negTfVals[0].size > 0: #check if any values are negative and adjust the indices if so
                        finalPhaseStepTf = [x-finalPhaseStepTf[negTfVals[0][0]] for x in finalPhaseStepTf]
                    allFinalPhaseStepTfs[dataRate][channel] = finalPhaseStepTf

                    plotCreatorBasic1.title = "channel: %0.0f data rate: %0.0f \n" % (channel, dataRate)
                    plotCreatorBasic1.run()

        dataFile1.fileName = "calCoefficientsTemp_"+calOptions.moduleName+".txt"
        filePath = dataFile1.getFilePath()
        now = datetime.datetime.now()
        date = "%04d%02d%02d" % (now.year, now.month, now.day)
        with open(filePath, "w") as calFile:
            # Fill header section
            calFile.write("BEGIN SECTION\n")
            calFile.write("section type : header\n")
            calFile.write("serial number : "+calOptions.moduleName+"\n")
            calFile.write("hardware revision : Rev0\n")
            calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
            calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
            calFile.write("END SECTION\n\n")

            calFile.write("BEGIN SECTION\n")
            calFile.write("section type : rx_tg_calibration_data\n")

            for dataRateTemp in allDataRates :
                calFile.write("# Data Rate = %0.0f\n" % (dataRateTemp))
                for channel in range(1,17,1):
                    for phase in range(128) :
                        calFile.write("%0.8f," % allFinalPhaseStepTfs[dataRateTemp][channel][phase])
                    calFile.write("\n")

            calFile.write("END SECTION\n")

            calFile.close()

        dataFile1.saveAsResult("calCoefficientsTemp_"+calOptions.moduleName)

dataFile1.fileName = "calCoefficients_"+calOptions.moduleName+".txt"
filePath = dataFile1.getFilePath()

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

with open(filePath, "w") as calFile:
    # Fill header section
    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : header\n")
    calFile.write("serial number : "+calOptions.moduleName+"\n")
    calFile.write("hardware revision : Rev0\n")
    calFile.write("date of manufacture(YYYYMMDD) : "+date+"\n")
    calFile.write("date of calibration(YYYYMMDD) : "+date+"\n")
    calFile.write("END SECTION\n\n")

    calFile.write("BEGIN SECTION\n")
    calFile.write("section type : rx_tg_calibration_data\n")

    for dataRate in allDataRates:
        calFile.write("# Data Rate = %0.0f\n" % (dataRate))
        for channel in range(1,17,1):
            for phase in range(128) :
                calFile.write("%0.8f," % allFinalPhaseStepTfs[dataRate][channel][phase])
            calFile.write("\n")

    calFile.write("END SECTION\n")

    calFile.close()

dataFile1.saveAsResult("calCoefficients_"+calOptions.moduleName)
dataFile1.deleteFile()
