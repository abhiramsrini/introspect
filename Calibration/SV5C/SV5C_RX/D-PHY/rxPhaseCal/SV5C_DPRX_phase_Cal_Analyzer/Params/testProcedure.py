# SVT Test
# SVT version 25.1.1
# Test saved 2025-07-08_2009
# Form factor: SV5C_4L8G_MIPI_DPHY_ANALYZER
# PY3
# Checksum: 0a37406314d96d8de7e452b7f665edce
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName=None)
calParams = _create('calParams', 'SvtDataRecord', iespName=None)
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
runCalibration = _create('runCalibration', 'SvtFunction', iespName=None)
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName=None)

bertScan1 = _create('bertScan1', 'SvtMipiDphyBertScan')
eyeScan1 = _create('eyeScan1', 'SvtMipiDphyEyeScan')
laneList1 = _create('laneList1', 'SvtMipiDphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

SetupFunction.args = 'rate'
SetupFunction.code = r'''#enabled calibration mode
iesp.writeSubPartRegister(0x0930, 0x00, 0x01)
iesp.waitForCommandProcessors() # abhi adding this line

print("Data Rate: %f" % rate)
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

calParams.addField('dataRate', descrip='''''', attrType=float, iespInstanceName='any', defaultVal=5000.0, displayOrder=(0, 1.0))
calParams.addMethod('_customInit',
'',
r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
False)
calParams.dataRate = 5000.0
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

syncOffsetsGroupe1 = []
fallingEdgesGroupe1 = []
listDiffGroupe1 = []

syncOffsetsGroupe2 = []
fallingEdgesGroupe2 = []
listDiffGroupe2 = []

maxNumberOfTrials = 30

# --------------------------------------------------
#perform clock commit and set termination
SetupFunction(calParams.dataRate)



print('\n\n Groupe 1')
# ---------------------  Groupe 1
# 2 (D2_0), 3 (D2_1), 4 (D3_0), 5 (D3_1) 8 (CLK_0), 9 (CLK_1)

# need to ensure sync offset is the same for 6 wires in this groupe. Try until it matches.
for trial in range(maxNumberOfTrials):
    print('==Trial #%d for Groupe 1' % trial)
    syncOffsetsTemp = []
    fallingEdgesTemp = []

    # --------------- data lanes
    # disable capture clock select. This mode need to be set when measuring the data lanes.
    iesp.setMipiCaptureClockSelect(0)
    for preBert in [2, 3, 4, 5]:
        #set active lane
        lane = ((preBert//2) + 1)
        laneMask = 0x01 << (lane-1)
        print("Lane: %d" % lane)
        laneList1.lanes = [lane]
        laneList1.setup()

        print('==D%d_%d' % (lane, preBert%2))

        #set pre bert
        iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

        bertScan1.patternSync = 'PATSYNC_strobeSync'

        #start bertScan
        result = bertScan1.run()
        print('--> bertScan Result: ', result.getResultFolderPath().split('\\')[-1])
        edges = result.getAnalysis(lane, 'wireState')['edges']
        fallingEdge = edges[0]['location']
        print("Edge Location: %f" % fallingEdge)

        syncOffset = dftUtil.byteListToUIntValue(iesp.readSubPartRegister(0x6643, laneMask))
        print("SyncOffset: %d" % syncOffset)
        syncOffsetsTemp.append(syncOffset)
        fallingEdgesTemp.append(fallingEdge)

        if len(set(syncOffsetsTemp)) != 1:
            printMsg('syncOffset are not the same', 'yellow', None, True)
            break


    # ----------------- CLK lanes
    #enabled capture clock select. this mode needs to be enabled when measuring clk lanes.
    if len(set(syncOffsetsTemp)) == 1:
        iesp.setMipiCaptureClockSelect(1)
        for preBert in [8, 9]:
            clkIdx = preBert - 8

            #set active lane
            lane = 1
            laneMask = 0x01 << (lane-1)
            print("Lane: %d" % lane)
            laneList1.lanes = [lane]
            laneList1.setup()

            print('== CLK%d' % (clkIdx))

            #set pre bert
            iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

            bertScan1.patternSync = 'PATSYNC_strobeSync'

            #start bertScan
            result = bertScan1.run()
            print('--> bertScan Result: ', result.getResultFolderPath().split('\\')[-1])
            edges = result.getAnalysis(lane, 'wireState')['edges']
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
        fallingEdgesGroupe1.extend(fallingEdgesTemp)
        syncOffsetsGroupe1.extend(syncOffsetsTemp)
        break
    else:
        printMsg('syncOffset are not the same!! Repeat...', 'yellow', None, True)
        #perform clock commit and set termination
        SetupFunction(calParams.dataRate)

if len(set(syncOffsetsTemp)) != 1:
    failFlag = 1
    printMsg('syncOffset are not the same!! Number of maximum trial is reached for groupe 1...', 'red', None, True)



print('\n\n Groupe 2')
# ---------------------  Groupe 2
# 0 (D1_0), 1 (D1_1), 6 (D4_0), 7 (D4_1) 10 (CLK_2), 11 (CLK_3)

# need to ensure sync offset is the same for 6 wires in this groupe. Try until it matches.
for trial in range(maxNumberOfTrials):
    print('==Trial #%d for Groupe 2' % trial)
    syncOffsetsTemp = []
    fallingEdgesTemp = []

    # --------------- data lanes
    # disable capture clock select. This mode need to be set when measuring the data lanes.
    iesp.setMipiCaptureClockSelect(0)
    for preBert in [0, 1, 6, 7]:
        #set active lane
        lane = ((preBert//2) + 1)
        laneMask = 0x01 << (lane-1)
        print("Lane: %d" % lane)
        laneList1.lanes = [lane]
        laneList1.setup()

        print('==D%d_%d' % (lane, preBert%2))

        #set pre bert
        iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

        bertScan1.patternSync = 'PATSYNC_strobeSync'

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


    # ----------------- CLK lanes
    # enabled capture clock select. This mode needs to be enabled when measuring clk lanes.
    if len(set(syncOffsetsTemp)) == 1:
        iesp.setMipiCaptureClockSelect(1)
        for preBert in [10, 11]:
            clkIdx = preBert - 8

            #set active lane
            lane = 1
            laneMask = 0x01 << (lane-1)
            print("Lane: %d" % lane)
            laneList1.lanes = [lane]
            laneList1.setup()

            print('== CLK%d' % (clkIdx))

            #set pre bert
            iesp.writeSubPartRegister(0x66A4, 0x00, preBert)

            bertScan1.patternSync = 'PATSYNC_strobeSync'

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
        fallingEdgesGroupe2.extend(fallingEdgesTemp)
        syncOffsetsGroupe2.extend(syncOffsetsTemp)
        break
    else:
        printMsg('syncOffset are not the same!! Repeat...', 'yellow', None, True)
        #perform clock commit and set termination
        SetupFunction(calParams.dataRate)

if len(set(syncOffsetsTemp)) != 1:
    failFlag = 1
    printMsg('syncOffset are not the same!! Number of maximum trial is reached for groupe 2...', 'red', None, True)



#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)
# --------------------------------------------------

if not failFlag:
    # compute the differences for each groupe
    length = len(fallingEdgesGroupe1)
    for i in range(length):
        # groupe 1
        delta = fallingEdgesGroupe1[i] - fallingEdgesGroupe1[0]
        listDiffGroupe1.append(delta)
        # groupe 2
        delta = fallingEdgesGroupe2[i] - fallingEdgesGroupe2[0]
        listDiffGroupe2.append(delta)


print('**** Groupe1:')
print('Falling edges:')
print(fallingEdgesGroupe1)
print('syncOffsets:')
print(syncOffsetsGroupe1)
print('listDiff')
print(listDiffGroupe1)

print('**** Groupe2:')
print('Falling edges:')
print(fallingEdgesGroupe2)
print('syncOffsets:')
print(syncOffsetsGroupe2)
print('listDiff')
print(listDiffGroupe2)



if failFlag == 0:
    writeTransferFunctions(listDiffGroupe1, listDiffGroupe2)
    writeNoteForTestRun("Complete")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL: Try to run the procedure again. (Note: calCoefficients_%s.txt file was not created)" % serialNumber)
'''
runCalibration.wantAllVarsGlobal = False

writeTransferFunctions.args = 'listDiffGroupe1, listDiffGroupe2'
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
    outFile.write("section type : dprx_phase_offset_data\n")
    outFile.write("# Each row has 2*<number of data lanes> + 4*<Clock lane> columns , i.e, D0_0, D0_1, D1_0, D1_1, D2_0, D2_1,  D3_0, D3_1, CLK0_0, CLK0_1, CLK1_0, CLK1_1 \n")
    outFile.write("# dataRate=%f\n" % calParams.dataRate)
    #for i in range(12):
        #outFile.write("%d, " % (listDiff[i] * 1000))
    # CalFile Format is
    # D1_0, D1_1, D2_0, D2_1, D3_0, D3_1, D4_0, D4_1, CLK_0, CLK_1, CLK_2, CLK_3
    # D1_0, D1_1
    outFile.write("%d,%d, " % (listDiffGroupe2[0] * 1000, listDiffGroupe2[1] * 1000))
    # D2_0, D2_1
    outFile.write("%d,%d, " % (listDiffGroupe1[0] * 1000, listDiffGroupe1[1] * 1000))
    # D3_0, D3_1
    outFile.write("%d,%d, " % (listDiffGroupe1[2] * 1000, listDiffGroupe1[3] * 1000))
    # D4_0, D4_1
    outFile.write("%d,%d, " % (listDiffGroupe2[2] * 1000, listDiffGroupe2[3] * 1000))
    # CLK_0, CLK_1
    outFile.write("%d,%d, " % (listDiffGroupe1[4] * 1000, listDiffGroupe1[5] * 1000))
    # CLK_2, CLK_3
    outFile.write("%d,%d, " % (listDiffGroupe2[4] * 1000, listDiffGroupe2[5] * 1000))
    outFile.write("\n")
    outFile.write("END SECTION")
'''
writeTransferFunctions.wantAllVarsGlobal = False


bertScan1.bertDurationInBits = 10000000
bertScan1.endPhase = 1.5
bertScan1.laneList = laneList1
bertScan1.measurementMode = 'allTransitions'
bertScan1.onlyDoSetupOnce = False
bertScan1.patternSync = PATSYNC_strobeSync
bertScan1.phaseOffsets = [0.0]
bertScan1.saveResults = True
bertScan1.startPhase = -1.5
bertScan1.timeUnits = 'unitWidth'
bertScan1.wantResultImages = False
bertScan1.wires = ['pos', 'neg']

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
eyeScan1.voltageStep = 10.0
eyeScan1.wantResultImages = False
eyeScan1.wires = ['pos', 'neg']

laneList1.expectedPattern = None
laneList1.hsClockThresholdVoltage = 50.0
laneList1.hsDataThresholdVoltages = [50.0]
laneList1.lanes = [1, 2, 3, 4]
laneList1.lpClockThresholdVoltage = 600.0
laneList1.lpDataThresholdVoltages = [600.0]

mipiClockConfig1.autoDetectDataRate = False
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
    myString = "Start the procedure SV5C_DPTX_phase_Cal_Generator first"
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
