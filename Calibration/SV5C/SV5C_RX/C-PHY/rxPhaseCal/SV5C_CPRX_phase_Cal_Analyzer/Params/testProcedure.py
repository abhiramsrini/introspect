# SVT Test
# SVT version 25.1.1
# Test saved 2025-07-07_1642
# Form factor: SV5C_4L8G_MIPI_CPHY_ANALYZER
# PY3
# Checksum: ccecd56d7f1f4371a3132b68aa2f3230
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName=None)
calParams = _create('calParams', 'SvtDataRecord', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
runCalibration = _create('runCalibration', 'SvtFunction', iespName=None)
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName=None)

bertScan1 = _create('bertScan1', 'SvtMipiCphyBertScan')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

SetupFunction.args = 'rate'
SetupFunction.code = r'''#enable alignment cal mode. no .5 sub ui offset
iesp.writeSubPartRegister(0x0930, 0x00, 0x01)

print("Data Rate: %f" % rate)
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
calParams.addField('dataRate', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=4000.0, displayOrder=(0, 2.0))
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
calParams.dataRate = 4000.0
calParams.lanes = [1, 2, 3, 4]
calParams.callCustomInitMethod()
coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

runCalibration.args = ''
runCalibration.code = r'''failFlag = 0

# --------------------------------------------------
print(' ')
printMsg('== Start calibration ==', 'magenta', None, True)

syncOffsets = []
fallingEdges = []
listDiff = []
firstBert = True
targetSyncOffset = 0

maxNumberOfTrials = 20

# --------------------------------------------------
#perform clock commit and set termination
SetupFunction(calParams.dataRate)

# loop through the wires: AB1_0, AB1_1...
for preBert in range(0, 24, 6):
    #need to ensure sync offset is the same for 6 wires of the same lane. Try until it matches
    for trial in range(maxNumberOfTrials):
        syncOffsetsTemp = []
        fallingEdgesTemp = []
        #set active lane
        lane = ((preBert//6) + 1)
        print('==Trial #%d for Lane %d' % (trial, lane))

        for wireIndex in range(preBert, preBert+6):
            laneMask = 0x01 << (lane-1)
            laneList1.lanes = [lane]
            laneList1.setup()

            #set active wire
            wire = (wireIndex//2)%3
            print(wireIndex)
            bertScan1.wires = [calParams.wires[wire]]
            bertScan1.patternSync = 'PATSYNC_strobeSync'

            #set pre bert
            iesp.writeSubPartRegister(0x66A4, 0x00, wireIndex)

            print("%s%d_%d" % (calParams.wires[wire], lane, wireIndex%2))


            #after the first sync we want to force the init wire state
            if(firstBert):
                iesp.writeSubPartRegister(0x66A8, laneMask, 0x00) #clear force wire init state
            else:
                iesp.writeSubPartRegister(0x66A8, laneMask, 0x01) #set force wire init state
            firstBert = False


            #start bertScan
            result = bertScan1.run()
            print('--> bertScan Result: ', result.getResultFolderPath().split('\\')[-1])
            edges = result._getAnalysis(lane, 'wireState')['edges']
            fallingEdge = edges[0]['location']
            print("Edge Location: %f" % fallingEdge)

            syncOffset = dftUtil.byteListToUIntValue(iesp.readSubPartRegister(0x6643, laneMask))
            print("SyncOffset: %d" % syncOffset)
            syncOffsetsTemp.append(syncOffset)
            fallingEdgesTemp.append(fallingEdge)

            if len(set(syncOffsetsTemp)) != 1:
                printMsg('syncOffset are not the same', 'yellow', None, True)
                break

        if len(set(syncOffsetsTemp)) == 1:
            printMsg('syncOffset are the same. Pass.', 'green', None, True)
            fallingEdges.extend(fallingEdgesTemp)
            syncOffsets.extend(syncOffsetsTemp)
            break
        else:
            printMsg('syncOffset are not the same!! Repeat...', 'yellow', None, True)
            #perform clock commit and set termination
            SetupFunction(calParams.dataRate)

    if len(set(syncOffsetsTemp)) != 1:
        failFlag = 1
        printMsg('syncOffset are not the same!! Number of maximum trials reached for lane %d! '% lane, 'red', None, True)
        break

print('Falling edges:')
print(fallingEdges)
print('syncOffsets:')
print(syncOffsets)

#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)
#disable alignment cal mode (enable in SetupFunction)
iesp.writeSubPartRegister(0x0930, 0x00, 0x00)
# --------------------------------------------------


length = len(fallingEdges)
for i in range(length):
    delta = fallingEdges[i] - fallingEdges[(i//6)*6]
    listDiff.append(delta)

print('listDiff')
pprint(listDiff)

if len(listDiff) == 24:
    writeTransferFunctions(listDiff)
else:
    failFlag = 1
    printMsg('FAIL: Could not find the offsets for all the lanes.', 'red', None, True)

if failFlag == 0:
    writeNoteForTestRun("Complete")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL: Try to run the procedure again. (Note: calCoefficients_%s.txt file was not created)" % serialNumber)
'''
runCalibration.wantAllVarsGlobal = False

writeTransferFunctions.args = 'listDiff'
writeTransferFunctions.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)
resultFolderCreator1.folderName = "calCoefficients_" + serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "calCoefficients_" + serialNumber + ".txt"
filePath = os.path.join(folderPath, FilePathString)
with open(filePath, "w") as outFile:
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : header\n")
    outFile.write("serial number : " + serialNumber + "\n")
    outFile.write("hardware revision : A\n")
    outFile.write("date of manufacture(YYYYMMDD) : "+date + "\n")
    outFile.write("date of calibration(YYYYMMDD) : "+date + "\n")
    outFile.write("speed grade : 0" + "\n")
    outFile.write("END SECTION\n")
    outFile.write("\n")
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : rx_phase_offset_data\n")
    outFile.write("# Each row has 6*<number of lanes> columns (i.e. 1 column per wire). So for 1 lane, the column labels are: AB1_0, AB1_1, BC1_0, BC1_1, CA1_0, CA1_1 \n")
    outFile.write("# dataRate=%f\n" % calParams.dataRate)
    length = len(listDiff)
    for i in range(length):
        outFile.write("%d, " % (listDiff[i] * 1000))
    outFile.write("\n")
    outFile.write("END SECTION")
'''
writeTransferFunctions.wantAllVarsGlobal = False


bertScan1.bertDurationInBits = 99968
bertScan1.endPhase = 1.5
bertScan1.laneList = laneList1
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = True
bertScan1.patternSync = PATSYNC_strobeSync
bertScan1.phaseOffsets = [0.0]
bertScan1.saveResults = True
bertScan1.startPhase = -1.5
bertScan1.timeUnits = 'unitWidth'
bertScan1.wantResultImages = False
bertScan1.wires = ['wireAB', 'wireBC', 'wireCA']

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

runNotes1.active = True
runNotes1.wantCopyOfLogFile = True
runNotes1.wantIespLogFile = False
runNotes1.wantPromptForNotes = False

#! TEST PROCEDURE
from pprint import pprint
from dftm.fileUtil import copyContentsOfFolder

iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("24.3", None)

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
    myString = "Start the procedure SV5C_CPTX_phase_Cal_Generator first"
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

        runCalibration()

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
