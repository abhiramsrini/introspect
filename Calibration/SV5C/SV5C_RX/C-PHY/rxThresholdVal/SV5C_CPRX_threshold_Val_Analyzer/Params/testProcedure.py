# SVT Test
# SVT version 25.2.0
# Test saved 2025-07-07_1439
# Form factor: SV5C_4L8G_MIPI_CPHY_ANALYZER
# PY3
# Checksum: 165866505c3c711ece8c783d68238d71
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName=None)
calParams = _create('calParams', 'SvtDataRecord', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
createCsvReport = _create('createCsvReport', 'SvtFunction', iespName=None)
runNotes1 = _create('runNotes1', 'SvtRunNotes', iespName=None)
runValidation = _create('runValidation', 'SvtFunction', iespName=None)

eyeScan1 = _create('eyeScan1', 'SvtMipiCphyEyeScan')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')

SetupFunction.args = 'rate'
SetupFunction.code = r'''print("Data Rate: %f" % rate)
myString = "mipiClockConfig1.dataRate = %f" % (rate)
coordinator1.waitForCodeToBeRun("Generator",myString)
myString = "mipiGenerator1.setup();print('Setup finished...')"
coordinator1.waitForCodeToBeRun("Generator",myString, timeout=60.0)

mipiClockConfig1.dataRate = rate
refClocksConfig1.externRefClockFreq = 100.0
mipiClockConfig1.setup()


#freeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x01)

#set bert pattern trigger period. PRBS9 (511*16)bits
iesp.writeSubPartRegister(0x66A0, 0x00, 8177)

#override termination
iesp.writeSubPartRegister(0x0D40, 0x00, 0x01)

#force term on A
iesp.writeSubPartRegister(0xD13, 0x0F, 0x01)

#force term on B
iesp.writeSubPartRegister(0xD14, 0x0F, 0x01)

#force term on C
iesp.writeSubPartRegister(0xD15, 0x0F, 0x01)

#set pre cdr bert enable
iesp.writeSubPartRegister(0x66A2, 0x00, 0x01)

# set expected pattern
testPatt = SvtMipiCphyExpectedPattern()
testPatt.hsMode = 'prbs'
testPatt.prbsSeed = 0x9980789A
testPatt.prbsOrder = 'PRBS_9'

laneList1.expectedPattern = testPatt
'''
SetupFunction.wantAllVarsGlobal = False

calParams.addField('wires', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=str, defaultVal=['wireAB', 'wireBC', 'wireCA'], displayOrder=(0, 1.0))
calParams.addField('dataRate', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=4500.0, displayOrder=(0, 2.0))
calParams.addField('lanes', descrip='''''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 3.0))
calParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calParams.wires = ['wireAB', 'wireBC', 'wireCA']
calParams.dataRate = 4500.0
calParams.lanes = [1, 2, 3, 4]
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

# --------------------------------------------------
#perform clock commit and set termination
SetupFunction(calParams.dataRate)

# loop through the wires: AB1_0, AB1_1...
for preBert in range(24):
    #set active lane
    lane = ((preBert//6) + 1)
    laneMask = 0x01 << (lane-1)
    laneList1.lanes = [lane]
    laneList1.setup()

    #set active wire
    wire = (preBert//2)%3
    eyeScan1.wires = [calParams.wires[wire]]

    #set pre bert
    iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = True

    eyeScanFail = 0
    for trial in range(maxNumberOfTrials):
        print('==Trial #%d for %s%d_%d' % (trial, calParams.wires[wire], lane, preBert%2))
        try:
            results = eyeScan1.run()
            print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
            print(results.getAnalysis(lane, 'wireState'))
            eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
            eyeHeight = results.getAnalysis(lane, 'wireState')['eyeHeight']
            print(eyeCenterY)
            if eyeCenterY == None or eyeHeight < 300:
                eyeScanFail = 1
                warningMsg("Found a failing condition on %s%d_%d..." % (calParams.wires[wire], lane, preBert%2))
            else:
                eyeScanFail = 0
                if abs(eyeCenterY) > 60:
                    failFlag = 1
                    warningMsg("Found a failing condition on %s%d_%d..." % (calParams.wires[wire], lane, preBert%2))
                    csvReportList.append(['%s%d_%d' % (calParams.wires[wire], lane, preBert%2), eyeCenterY, "FAIL",'Exceed tolerance of +-60mV'])
                else:
                    csvReportList.append(['%s%d_%d' % (calParams.wires[wire], lane, preBert%2), eyeCenterY, "PASS",''])
                break
        except:
            # eye scan run failed -- try again
            eyeScanFail = 1
            # setup the clock again
            SetupFunction(calParams.dataRate)

    if eyeScanFail == 1:
        failFlag = 1
        warningMsg("Found a failing condition for %s%d_%d... Number of maximum trials reached!" % (calParams.wires[wire], lane, preBert%2))
        csvReportList.append(['%s%d_%d' % (calParams.wires[wire], lane, preBert%2), '', "FAIL",'Eye scan failed'])


#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)
# --------------------------------------------------


if failFlag == 0:
    writeNoteForTestRun("Pass")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL")
'''
runValidation.wantAllVarsGlobal = False

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False


eyeScan1.berThreshold = 0.0
eyeScan1.bertDurationInBits = 99968
eyeScan1.endPhase = 1.0
eyeScan1.endVoltage = 630.0
eyeScan1.eyeMask = None
eyeScan1.laneList = laneList1
eyeScan1.measurementMode = 'allTransitions'
eyeScan1.patternSync = PATSYNC_strobeSync
eyeScan1.saveResults = True
eyeScan1.scanMode = 'bertScan'
eyeScan1.startPhase = -1.0
eyeScan1.startVoltage = -630.0
eyeScan1.timeUnits = 'unitWidth'
eyeScan1.voltageStep = 40.0
eyeScan1.wantResultImages = False
eyeScan1.wires = ['wireAB', 'wireBC', 'wireCA']

laneList1.expectedPattern = None
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpThresholdVoltage = 600.0

mipiClockConfig1.autoDetectDataRate = False
mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 5000.0
mipiClockConfig1.referenceClocks = refClocksConfig1

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
from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("24.3", None)
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
    myString = "Start the procedure SV5C_CPTX_threshold_Val_Generator first"
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
        print('Waitting for 5 min to let the units warm up...')
        sleepMillis(300000)

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
