# SVT Test
# SVT version 3.6.29
# Test saved 2022-06-14_1112
# Form factor: SV3C_4L3G_MIPI_CPHY_ANALYZER
# Checksum: f1673bb364a7cbe9e965b7fc4881ef31


calOptions = SvtDataRecord()
calOptions.addField('moduleName', descrip='''''', attrType=str, defaultVal='1234', displayOrder=1)
calOptions.addField('dataRates', descrip='''List of data rates at which we want to compute receiver transfer functions.''', attrType=list, attrSubType=float, defaultVal=[1500.0], displayOrder=2)
calOptions.addField('targetLevels', descrip='''List of Rx threshold voltage levels to be measured.''', attrType=list, attrSubType=float, defaultVal=[200.0], displayOrder=3)
calOptions.addField('saveVscans', descrip='''''', attrType=bool, defaultVal=False, displayOrder=4)
calOptions.addMethod('_customInit',
	'',
	r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
	False)
calOptions.dataRates = [1500.0]
calOptions.moduleName = '1234'
calOptions.saveVscans = False
calOptions.targetLevels = [200.0]
calOptions.callCustomInitMethod()

coordinator1 = SvtCoordinator()
coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

globalClockConfig = SvtMipiClockConfig()
globalClockConfig.dataRate = 1500.0
globalClockConfig.externRefClockFreq = 100.0
globalClockConfig.outputClockAFormat = 'LVDS'
globalClockConfig.outputClockAFreq = 100.0
globalClockConfig.outputClockBFormat = 'LVDS'
globalClockConfig.outputClockBFreq = 100.0
globalClockConfig.sscEnabled = False
globalClockConfig.systemRefClockSource = 'external'
globalClockConfig.updateDataRateDependentDefaults = True

laneList1 = SvtMipiCphyLaneList()
laneList1.expectedPattern = CPHY_hsOnlyPrbs9
laneList1.isDataSplitAcrossLanes = True
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 600.0
laneList1.syncWord = '3444443'

eyeScan1 = SvtMipiCphyEyeScan()
eyeScan1.berThreshold = 0.0
eyeScan1.bertDurationInBits = 1000000
eyeScan1.bertSyncErrorThreshold = 30
eyeScan1.endPhase = 500.0
eyeScan1.endVoltage = 550.0
eyeScan1.errorIfSyncFails = False
eyeScan1.eyeMask = None
eyeScan1.laneList = laneList1
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.saveResults = True
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -500.0
eyeScan1.startVoltage = -550.0
eyeScan1.voltageStep = 50.0
eyeScan1.wantResultImages = False
eyeScan1.wires = ['wireAB', 'wireBC', 'wireCA']

mipiProtocol = SvtMipiProtocol()
mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

writeTransferFunctions = SvtFunctionWithResults()
writeTransferFunctions.args = ''
writeTransferFunctions.code = r'''import os
import datetime



now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)
folderPath = self.createRunResultFolder("calCoefficients_"+calOptions.moduleName,"TextReport")
FilePathString = "calCoefficients_"+calOptions.moduleName+".txt"
filePath = os.path.join(folderPath, FilePathString)
with open(filePath, "w") as outFile:
    commentArray = ["# Rx Threshold Voltage Slope Correction M5", "# Rx Threshold Voltage Slope Correction M4", "# Rx Threshold Voltage Slope Correction M3", "# Rx Threshold Voltage Slope Correction M2", "# Rx Threshold Voltage Slope Correction M1", "# Rx Threshold Voltage Offset"]
    print >>outFile, "BEGIN SECTION"
    print >>outFile, "section type : header"
    print >>outFile, "serial number : "+calOptions.moduleName
    print >>outFile, "hardware revision : RevB"
    print >>outFile, "date of manufacture(YYYYMMDD) : "+date
    print >>outFile, "date of calibration(YYYYMMDD) : "+date
    print >>outFile, "speed grade : 0"
    print >>outFile, "END SECTION"
    print >>outFile, ""
    print >>outFile, "BEGIN SECTION"
    print >>outFile, "section type: jitter_calibration_data"
    print >>outFile, "ffffffffffffffffffffffffffffffff00000000000000000000000000000000"
    print >>outFile, "END SECTION"
    print >>outFile, ""
    print >>outFile, "BEGIN SECTION"
    print >>outFile, "section type : cprx_rx_threshold_voltage_calibration_data"
    print >>outFile, "# Each data rate block has 6 rows for offset, slope M1, slope M2, slope M3, slope M4, slope M5 respectively."
    print >>outFile, "# Each row has 3*<number of lanes> columns (i.e. 1 column per wire). So for 4 lanes, the column labels are: AB1, BC1, CA1, AB2, BC2, CA2, AB3, BC3, CA3, AB4, BC4, CA4"
    numRates = 1 # 43
    ratesMeasured = 0
    for dataRate in sorted(calOptions.dataRates) :
        ratesMeasured = ratesMeasured + 1
       # commentString = "# Data Rate = %0.0f" % (dataRate)
       # print >>outFile, commentString
        for i in range(5,-1,-1) :
            print >>outFile, commentArray[i]
            for lane in range(1,5,1):
                for wire in ['wireAB', 'wireBC', 'wireCA'] :
                    if i == 5:
                        #print offset[lane][wire]
                        value =  offset[lane][wire] * 1000
                    else:
                        value =  averagePolynomialDict[dataRate][lane][wire][i]
                    print >>outFile, "%0.10g," % value,
            print >>outFile, ""
    print >>outFile, "END SECTION"
'''
writeTransferFunctions.wantAllVarsGlobal = False


#! TEST PROCEDURE
iesp = IESP.getInstance()
coordinator1.setState("running")


offset = dict()
for lane in range(1,5,1) :
    offset[lane] = dict()
    for wire in ['wireAB', 'wireBC', 'wireCA'] :
        offset[lane][wire] = 0


failFlag = 0
lanes = [1,2,3,4]
wireNames = 'allWires'
iesp.setMipiEqualizationDcGain(4, wireNames, lanes)
wires = ['wireAB', 'wireBC', 'wireCA'] 
dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

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

lanes = [1]
voltage = dict()
for lane in range(5):
    voltage[lane]= 200
    
while len(lanes) < len(laneList1.lanes) and failFlag == 0:
    print("(%d, %d, %d),(%d, %d, %d),(%d, %d, %d),(%d, %d, %d)" % (voltage[1], voltage[1], voltage[1],voltage[2], voltage[2], voltage[2],voltage[3], voltage[3], voltage[3],voltage[4], voltage[4], voltage[4]))
    myString = "mipiCphyGenerator1.hsVoltageAmplitudesABC = [(%d, %d, %d),(%d, %d, %d),(%d, %d, %d),(%d, %d, %d)]" % (voltage[1], voltage[1], voltage[1],voltage[2], voltage[2], voltage[2],voltage[3], voltage[3], voltage[3],voltage[4], voltage[4], voltage[4])
    coordinator1.waitForCodeToBeRun("Generator",myString)
    myString = "mipiCphyGenerator1.setup()"
    coordinator1.waitForCodeToBeRun("Generator",myString)
    globalClockConfig.setup()
    result = eyeScan1.run()
    if result != None:
        lanes = result.getLanes()
    else:
        lanes = []
        
    for lane in [1,2,3,4]:
        if lane not in lanes:
            warningMsg("Didn't sync on lane %d" % lane)
            voltage[lane] = voltage[lane] + 50
            if voltage[lane] > 500:
                failFlag = 1
                warningMsg("Unable to sync on lane %d" % lane)

for lane in lanes:
    for wire in wires:
        analysis = result.getAnalysis(lane, wire)
        if analysis['eyeCenterY'] == None:
            offset[lane][wire] = 0
            failFlag = 1
            warningMsg("Found a failing condition on Lane %d..." % lane)
        else:
            offset[lane][wire] = analysis['eyeCenterY']

writeTransferFunctions.run()


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
    
print "****************************************"
print "****************************************"
print "****************************************"
print "Please rename result directory to "+calOptions.moduleName+"."
print "****************************************"
print "****************************************"
print "****************************************"
