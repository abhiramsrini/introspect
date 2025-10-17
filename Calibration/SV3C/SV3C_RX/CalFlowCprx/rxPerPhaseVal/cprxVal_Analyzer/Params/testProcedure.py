# SVT Test
# SVT version 3.6.29
# Test saved 2022-06-20_1440
# Form factor: SV3C_4L3G_MIPI_CPHY_ANALYZER
# Checksum: 3a5dadf4632752968504215089ab87ee


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
calOptions.moduleName = 'CDPRX22060002'
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
        if analysis['eyeCenterY'] == None or analysis['eyeCenterY'] > 50 or analysis['eyeCenterY'] < -50 :
            failFlag = 1
            warningMsg("Found a failing condition on Lane %d wire %s ..." % (lane, wire))




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




print "****************************************"
print "****************************************"
print "****************************************"
print "Please rename result directory to "+calOptions.moduleName+"."
print "****************************************"
print "****************************************"
print "****************************************"
