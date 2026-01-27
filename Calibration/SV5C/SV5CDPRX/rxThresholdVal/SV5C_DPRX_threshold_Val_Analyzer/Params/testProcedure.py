# SVT Test
# SVT version 23.3.b10
# Test saved 2023-06-01_1246
# Form factor: SV5C_4L8G_MIPI_DPHY_ANALYZER
# PY3
# Checksum: ef41b46d37cf932b42b6fa4cbc51420c
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName='None')
calParams = _create('calParams', 'SvtDataRecord', iespName='None')
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
createCsvReport = _create('createCsvReport', 'SvtFunction', iespName='None')
runValidation = _create('runValidation', 'SvtFunction', iespName='None')
runWarmUpEyeScans = _create('runWarmUpEyeScans', 'SvtFunction', iespName='None')

eyeScan1 = _create('eyeScan1', 'SvtMipiDphyEyeScan')
laneList1 = _create('laneList1', 'SvtMipiDphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

SetupFunction.args = 'rate'
SetupFunction.code = r'''print("Data Rate: %f" % rate)
myString = "mipiClockConfig1.dataRate = %f" % (rate)
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup();print('Setup finished...')"
coordinator1.waitForCodeToBeRun("Generator",myString, timeout=60.0)

mipiClockConfig1.dataRate = rate
mipiClockConfig1.setup()


#freeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x01)

#set bert pattern trigger period. PRBS9 = 511
iesp.writeSubPartRegister(0x66A0, 0x1F, 511)

#override termination
iesp.writeSubPartRegister(0x0C40, 0x1F, 0x01)

#force term on Pos
iesp.writeSubPartRegister(0x0C14, 0x1F, 0x01)

#force term on Neg
iesp.writeSubPartRegister(0x0C15, 0x1F, 0x01)

#force filtering mode
iesp.writeSubPartRegister(0xC16, 0x1F, 0x01)

#set pre cdr bert enable
iesp.writeSubPartRegister(0x66A2, 0x00, 0x01)

#NOTE
#Untimately we were want to calibrate 2 groups.
#Group1: 2 (D2_0), 3 (D2_1), 4 (D3_0), 5 (D3_1) 8 (CLK_0), 9 (CLK_1)
#Group2: 0 (D1_0), 1 (D1_1), 6 (D4_0), 7 (D4_1) 10 (CLK_2), 11 (CLK_3)
#CalFile Format is
#D1_0, D1_1, D2_0, D2_1, D3_0, D3_1, D4_0, D4_1, CLK_0, CLK_1, CLK_2, CLK_3

# set expected pattern
testPatt = SvtMipiDphyExpectedPattern()
testPatt.hsMode = 'prbs'
testPatt.prbsSeed = 0xFF
testPatt.prbsOrder = 'PRBS_9'

laneList1.expectedPattern = testPatt
'''
SetupFunction.wantAllVarsGlobal = False

calParams.addField('dataRate', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=6250.0, displayOrder=(0, 1.0))
calParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calParams.dataRate = 6250.0
calParams.callCustomInitMethod()
coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

createCsvReport.args = ''
createCsvReport.code = r'''import time
import os
## dd/mm/yyyy format
dateToday = time.strftime("%d/%m/%Y")
timeNow = time.strftime("%H:%M:%S")

# create csv file output
resultFolderCreator1.folderName = serialNumber
resultFolderCreator1.resultType = "CsvData"

folderPath = resultFolderCreator1.run()
stringAppendix = ".csv"
FilePathString = serialNumber + stringAppendix
filePath = os.path.join(folderPath, FilePathString)
with open(filePath, "w") as outFile:
    print("Serial number, %s" % serialNumber, file=outFile)
    print("Date, %s" % dateToday, file=outFile)
    print("Time, %s" % timeNow, file=outFile)
    print(" ", file=outFile)

    print("Wire, eyeCenterY, Result, Failure description", file=outFile)
    for i in range(len(csvReportList)) :
        print("%s, %s, %s, %s" % (csvReportList[i][0], csvReportList[i][1], csvReportList[i][2], csvReportList[i][3]), file=outFile)
'''
createCsvReport.wantAllVarsGlobal = False

runValidation.args = ''
runValidation.code = r'''failFlag = 0

# --------------------------------------------------
print(' ')
printMsg('== Start actual validation ==', 'magenta', None, True)
maxNumberOfTrials = 10

#perform clock commit and set termination
SetupFunction(calParams.dataRate)

# ------------------------------- data lanes
#disable capture clock select. this mode need to be set when measuring the data lanes. ie pre-bert values 0-7
iesp.setMipiCaptureClockSelect(0)
for preBert in range(8):
    print(preBert)

    #set active lane
    lane = ((preBert//2) + 1)
    laneMask = 0x01 << (lane-1)
    print("Lane: %d" % lane)
    laneList1.lanes = [lane]
    laneList1.setup()

    #set pre bert
    iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = True

    eyeScanFail = 0
    for trial in range(maxNumberOfTrials):
        try:
            print('==Trial #%d for D%d_%d' % (trial, lane, preBert%2))
            results = eyeScan1.run()
            print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
            print(results.getAnalysis(lane, 'wireState'))
            eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
            print(eyeCenterY)
            if eyeCenterY == None:
                eyeScanFail = 1
                warningMsg("Found a failing condition on D%d_%d: eye center None..." % (lane, preBert%2))
            else:
                eyeScanFail = 0
                if abs(eyeCenterY) > 60:
                    eyeScanFail = 0
                    failFlag = 1
                    warningMsg("Found a failing condition on D%d_%d..." % (lane, preBert%2))
                    csvReportList.append(['D%d_%d' % (lane, preBert%2), eyeCenterY, "FAIL",'Exceed tolerance of +-60mV'])
                else:
                    csvReportList.append(['D%d_%d' % (lane, preBert%2), eyeCenterY, "PASS",''])
                break
        except:
            # eye scan run failed -- try again
            eyeScanFail = 1
            # setup the clock again
            SetupFunction(calParams.dataRate)

    if eyeScanFail == 1:
        failFlag = 1
        warningMsg("Found a failing condition on D%d_%d... Number of maximum trials reached!" % (lane, preBert%2))
        csvReportList.append(['D%d_%d' % (lane, preBert%2),'', "FAIL",'eyeScan failed'])

    print("temperatures: %s" % iesp.getModuleTemperatures())



# ------------------------------- clk lanes
clkIdx = 1
#enabled capture clock select. this mode needs to be enabled when measuring clk lanes. ie pre-bert values 8-11
iesp.setMipiCaptureClockSelect(1)
for preBert in range(8,12,1):
    print(preBert)

    #set active lane
    lane = 1
    laneMask = 0x01 << (lane-1)
    print("Lane: %d" % lane)
    print("Clk%d" % clkIdx)
    laneList1.lanes = [lane]
    laneList1.setup()

    #set pre bert
    iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = True

    eyeScanFail = 0
    for trial in range(maxNumberOfTrials):
        try:
            print('==Trial #%d for CLK%d' % (trial, clkIdx))
            results = eyeScan1.run()
            print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
            print(results.getAnalysis(lane, 'wireState'))
            eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
            print(eyeCenterY)
            if eyeCenterY == None:
                eyeScanFail = 1
                warningMsg("Found a failing condition on CLK%d: eye center None..." % clkIdx)
            else:
                eyeScanFail = 0
                if abs(eyeCenterY) > 60:
                    failFlag = 1
                    warningMsg("Found a failing condition on CLK%d..." % clkIdx)
                    csvReportList.append(['CLK%d.' % clkIdx, eyeCenterY, "FAIL",'Exceed tolerance of +-60mV'])
                else:
                    csvReportList.append(['CLK%d' % clkIdx, eyeCenterY, "PASS",''])
                break
        except:
            # eye scan run failed -- try again
            eyeScanFail = 1
            # setup the clock again
            SetupFunction(calParams.dataRate)

    if eyeScanFail == 1:
        failFlag = 1
        warningMsg("Found a failing condition for CLK%d... Number of maximum trials reached!" % clkIdx)
        csvReportList.append(['CLK%d' % clkIdx, '', "FAIL",'Eye scan failed'])

    clkIdx = clkIdx + 1

    print("temperatures: %s" % iesp.getModuleTemperatures())


#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)

if failFlag == 0:
    writeNoteForTestRun("Pass")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL")
if failFlag == 0:
    writeNoteForTestRun("PASS")
    filePath = getParamsFilePath("Pass.png")

    myFileUrl = str(filePath)
    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)


else:
    writeNoteForTestRun("FAIL, please check report")
    filePath = getParamsFilePath("Fail.png")

    myFileUrl = str(filePath)
'''
runValidation.wantAllVarsGlobal = False

runWarmUpEyeScans.args = ''
runWarmUpEyeScans.code = r'''# --------------------------------------------------
print(' ')
printMsg('== Run dummy eye scans to let the unit warm up ==', 'magenta', None, True)


# --------------------------------------------------
#perform clock commit and set termination
SetupFunction(calParams.dataRate)

# ------------------------------- data lanes
iesp.setMipiCaptureClockSelect(0)
for preBert in range(3):
    print(preBert)

    #set active lane
    lane = ((preBert//2) + 1)
    laneMask = 0x01 << (lane-1)
    print("Lane: %d" % lane)
    laneList1.lanes = [lane]
    laneList1.setup()

    #set pre bert
    iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = False

    print("D%d_%d" % (preBert%2, lane))

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = False
    try:
        results = eyeScan1.run()
        print(results.getAnalysis(lane, 'wireState'))
    except:
        # eye scan run failed -- try again
        SetupFunction(calParams.dataRate)

#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)
'''
runWarmUpEyeScans.wantAllVarsGlobal = False


eyeScan1.berThreshold = 1e-12
eyeScan1.bertDurationInBits = 1000000
eyeScan1.endPhase = 1.0
eyeScan1.endVoltage = 550.0
eyeScan1.eyeMask = None
eyeScan1.laneList = laneList1
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.patternSync = PATSYNC_strobeSync
eyeScan1.saveResults = True
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -1.0
eyeScan1.startVoltage = -550.0
eyeScan1.timeUnits = 'unitWidth'
eyeScan1.voltageStep = 30.0
eyeScan1.wantResultImages = False
eyeScan1.wires = ['pos', 'neg']

laneList1.expectedPattern = None
laneList1.hsClockThresholdVoltage = 50.0
laneList1.hsDataThresholdVoltages = [50.0]
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpClockThresholdVoltage = 600.0
laneList1.lpDataThresholdVoltages = [600.0]

mipiClockConfig1.autoDetectClock = False
mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.continuousClock = False
mipiClockConfig1.dataRate = 5000.0
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

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

#! TEST PROCEDURE
from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("23.1", None)
csvReportList = list()


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
    myString = "Start the procedure SV5C_DPTX_threshold_Val_Generator first"
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
        runWarmUpEyeScans()
        runValidation()
        createCsvReport()

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
