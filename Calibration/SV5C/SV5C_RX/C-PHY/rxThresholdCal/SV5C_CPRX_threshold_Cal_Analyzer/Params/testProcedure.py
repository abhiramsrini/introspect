# SVT Test
# SVT version 23.1.0
# Test saved 2023-06-22_1050
# Form factor: SV5C_4L8G_MIPI_CPHY_ANALYZER
# PY3
# Checksum: ab31b44b3d48e3564baf7bf47e796737
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


SetupFunction = _create('SetupFunction', 'SvtFunction', iespName='None')
calParams = _create('calParams', 'SvtDataRecord', iespName='None')
checkSyncOnAllWires = _create('checkSyncOnAllWires', 'SvtFunction', iespName='None')
coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
runCalibration = _create('runCalibration', 'SvtFunction', iespName='None')
runWarmUpEyeScans = _create('runWarmUpEyeScans', 'SvtFunction', iespName='None')
writeTransferFunctions = _create('writeTransferFunctions', 'SvtFunction', iespName='None')

bertScan1 = _create('bertScan1', 'SvtMipiCphyBertScan')
eyeScan1 = _create('eyeScan1', 'SvtMipiCphyEyeScan')
laneList1 = _create('laneList1', 'SvtMipiCphyLaneList')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')
resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
runNotes1 = _create('runNotes1', 'SvtRunNotes')

SetupFunction.args = 'rate, bitphase'
SetupFunction.code = r'''if bitphase == 0:
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

if bitphase == 1:
    iesp.writeSubPartRegister(0xFEEC, 0x00, 0x00) # Toggles even/odd state
    iesp.waitForCommandProcessors()


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
checkSyncOnAllWires.args = ''
checkSyncOnAllWires.code = r'''# check the sync succeeds on all wires by doing bertScan
print('== Check sync on all wires == ')

syncFailFlag = 0
rate = 1800.0
firstBert = True
failedWires = []

#perform clock commit and set termination
SetupFunction(rate, 0)

# loop through the wires: AB1_0, AB1_1...
for preBert in range(0, 24, 6):
    #set active lane
    lane = ((preBert//6) + 1)
    print('==Lane %d' % (lane))

    for wireIndex in range(preBert, preBert+6):
        try:
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

            bertScan1.patternSync = 'PATSYNC_strobeSync'

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
        except Exception as e:
            printMsg(f'Exception: {type(e)} -- {str(e)}', 'orange') 
            syncFailFlag = 1
            printMsg("Failed to sync for %s%d_%d:" % (calParams.wires[wire], lane, wireIndex%2), 'red')
            failedWires.append('%s%d_%d' % (calParams.wires[wire], lane, wireIndex%2))


return (syncFailFlag, failedWires)
'''
checkSyncOnAllWires.wantAllVarsGlobal = False

coordinator1.clientName = 'Analyzer'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

runCalibration.args = ''
runCalibration.code = r'''failFlag = 0

# --------------------------------------------------
print(' ')
printMsg('== Start actual calibration ==', 'magenta', None, True)

maxNumberOfTrials = 10

# now start eye scans
offsetList = []
offsetEvenList = []
offsetOddList = []

# loop through the wires: AB1_0, AB1_1...
for preBert in range(24):

    # ---------------------------------------- EVEN
    #perform clock commit and set termination
    SetupFunction(calParams.dataRate, 0)

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

    print("%s%d: State 1" % (calParams.wires[wire], lane))

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = True

    eyeScanFail = 0
    for trial in range(maxNumberOfTrials):
        print('==Trial #%d for %s%d_%d' % (trial, calParams.wires[wire], lane, preBert%2))
        results = eyeScan1.run()
        print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
        print(results.getAnalysis(lane, 'wireState'))
        eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
        eyeHeight = results.getAnalysis(lane, 'wireState')['eyeHeight']
        print(eyeCenterY)
        if eyeCenterY == None or eyeHeight < 350:
            eyeScanFail = 1
            warningMsg("Found a failing condition on Lane %d..." % lane)
        else:
            eyeScanFail = 0
            offsetEven = eyeCenterY
            offsetEvenList.append(offsetEven)
            break
    if eyeScanFail == 1:
        failFlag = 1
        warningMsg("Found a failing condition on Lane %d... Number of maximum trials reached!" % lane)


    #unfreeze cdr
    #iesp.writeSubPartRegister(0x66B0,0x00,0x00)
    # ----------------------------------------

    print("temperatures: %s" % iesp.getModuleTemperatures())




    # ---------------------------------------- ODD
    #perform clock commit and set termination
    SetupFunction(calParams.dataRate, 1)

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

    print("%s%d: State 2" % (calParams.wires[wire], lane))

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = True

    eyeScanFail = 0
    for trial in range(maxNumberOfTrials):
        print('==Trial #%d for %s%d_%d' % (trial, calParams.wires[wire], lane, preBert%2))
        results = eyeScan1.run()
        print('--> eyeScan Result: ', results.getResultFolderPath().split('\\')[-1])
        print(results.getAnalysis(lane, 'wireState'))
        eyeCenterY = results.getAnalysis(lane, 'wireState')['eyeCenterY']
        eyeHeight = results.getAnalysis(lane, 'wireState')['eyeHeight']
        print(eyeCenterY)
        if eyeCenterY == None or eyeHeight < 350:
            eyeScanFail = 1
            warningMsg("Found a failing condition on Lane %d..." % lane)
        else:
            eyeScanFail = 0
            offsetOdd = eyeCenterY
            offsetOddList.append(offsetOdd)
            break
    if eyeScanFail == 1:
        failFlag = 1
        warningMsg("Found a failing condition on Lane %d... Number of maximum trials reached!" % lane)


    #unfreeze cdr
    iesp.writeSubPartRegister(0x66B0,0x00,0x00)
    # ----------------------------------------
    print("temperatures: %s" % iesp.getModuleTemperatures())

    offsetAverage = (offsetEven + offsetOdd)/2
    print('Average offset: %f' % offsetAverage)
    offsetList.append(offsetAverage)


print('offsetEvenList: ' + str(offsetEvenList))
print('offsetOddList: ' + str(offsetOddList))
print('offsetList: ' + str(offsetList))


if failFlag == 0:
    writeTransferFunctions(offsetList)
    writeNoteForTestRun("Complete")
else :
    writeNoteForTestRun("Fail")
    warningMsg("FAIL: There's a failure in one of the lanes. (Note: calCoefficients_%s.txt file was not created)" % serialNumber)
'''
runCalibration.wantAllVarsGlobal = False

runWarmUpEyeScans.args = ''
runWarmUpEyeScans.code = r'''# --------------------------------------------------
print(' ')
printMsg('== Run dummy eye scans to let the unit warm up ==', 'magenta', None, True)


# ------------------------------- data lanes
for preBert in range(3):
    print(preBert)

    # ---------------------------------------- State 1
    #perform clock commit and set termination
    SetupFunction(calParams.dataRate, 0)

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

    print("%s%d: State 1" % (calParams.wires[wire], lane))

    eyeScan1.patternSync = 'PATSYNC_strobeSync'
    eyeScan1.saveResults = False
    try:
        results = eyeScan1.run()
        print(results.getAnalysis(lane, 'wireState'))
    except:
        # eye scan run failed -- try again
        SetupFunction(calParams.dataRate, 0)


#unfreeze cdr
iesp.writeSubPartRegister(0x66B0,0x00,0x00)
'''
runWarmUpEyeScans.wantAllVarsGlobal = False

writeTransferFunctions.args = 'offsetList'
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
    outFile.write("date of manufacture(YYYYMMDD) : " + date + "\n")
    outFile.write("date of calibration(YYYYMMDD) : " + date + "\n")
    outFile.write("speed grade : 0\n")
    outFile.write("END SECTION\n")
    outFile.write("\n")
    outFile.write("BEGIN SECTION\n")
    outFile.write("section type : cprx_rx_threshold_voltage_calibration_data\n")
    outFile.write("# dataRate=%f\n" % calParams.dataRate)
    outFile.write("# Each row has 6*<number of lanes> columns (i.e. 1 column per wire). So for 1 lane, the column labels are: AB1_0, AB1_1, BC1_0, BC1_1, CA1_0, CA1_1\n")
    for wire in range(24):
        value = offsetList[wire] * 1000
        outFile.write("%0.10g, " % value)
    outFile.write("\n")
    outFile.write("# Rx Threshold Voltage Slope Correction M1\n")
    outFile.write("1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,\n")
    outFile.write("# Rx Threshold Voltage Slope Correction M2\n")
    outFile.write("0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\n")
    outFile.write("# Rx Threshold Voltage Slope Correction M3\n")
    outFile.write("0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\n")
    outFile.write("# Rx Threshold Voltage Slope Correction M4\n")
    outFile.write("0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\n")
    outFile.write("# Rx Threshold Voltage Slope Correction M5\n")
    outFile.write("0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\n")
    outFile.write("END SECTION\n")
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

mipiClockConfig1.autoDetectClock = False
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
    myString = "Start the procedure SV5C_CPTX_threshold_Cal_Generator first"
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
        syncFailFlag, failedWires = checkSyncOnAllWires()

        if syncFailFlag == 1:
            failFlag = 1
            writeNoteForTestRun("Fail: Sync failed")
            printMsg("FAIL: Sync failed for: %s" % str(failedWires), 'red')
        else:
            #runWarmUpEyeScans()
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
