# SVT Test
# SVT version 21.4.0
# Test saved 2023-06-07_1743
# Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: caa4bbbdd2ebeadaa4d518989749ed80
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.

autoscaleScope = SvtFunction()
autoscaleScope.args = ''
autoscaleScope.code = r'''# Set to center by going to default
import time

osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
osci.WriteString("*OPC?", 1)
sleepMillis(200)


# Clear display
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(200)

# Set timebase to proper value

osci.WriteString("VBS 'app.Acquisition.Horizontal.HorScale = 5e-09'", 1)
osci.WriteString("VBS 'app.Acquisition.Trigger.Edge.Slope = \"Positive\"'", 1)

# Set Vertical scale for Channel 3 to proper value

osci.writestring("VBS 'app.Acquisition.C3.VerScale = 20e-3'", 1)
osci.writestring("VBS 'app.Acquisition.C3.VerOffset = -61.02e-3'", 1)
iesp.setMeasurementTimeout(60000)

# Turn averaging on

#osci.writestring("VBS 'app.Acquisition.C1.AverageSweeps = 1'", 1)
#osci.writestring("VBS 'app.Acquisition.C2.AverageSweeps = 1'", 1)
#osci.writestring("VBS 'app.Acquisition.C3.AverageSweeps = 1'", 1)

time.sleep(10)
'''
autoscaleScope.wantAllVarsGlobal = False
autoscaleScope._showInList = False

coarseClkSkewsToString = SvtFunction()
coarseClkSkewsToString.args = 'Pos, Neg'
coarseClkSkewsToString.code = r'''posCmd = ("00000000%s"%(hex(Pos&0xffffffff)[2:-1]))[-8:]
negCmd = ("00000000%s"%(hex(Neg&0xffffffff)[2:-1]))[-8:]

return "%s %s" % (posCmd, negCmd)
'''
coarseClkSkewsToString.wantAllVarsGlobal = False
coarseClkSkewsToString._showInList = False

coarseDataSkewsToString = SvtFunction()
coarseDataSkewsToString.args = 'Pos, Neg'
coarseDataSkewsToString.code = r'''posCmd = ("00000000%s"%(hex(Pos&0xffffffff)[2:-1]))[-8:]
negCmd = ("00000000%s"%(hex(Neg&0xffffffff)[2:-1]))[-8:]

return "%s %s %s %s %s %s %s %s" % (posCmd, negCmd, posCmd, negCmd, posCmd, negCmd, posCmd, negCmd)
'''
coarseDataSkewsToString.wantAllVarsGlobal = False
coarseDataSkewsToString._showInList = False

initScope = SvtFunction()
initScope.args = 'scopeIpAddress'
initScope.code = r'''import visa
#connect to scope
import win32com.client #imports the pywin32 library
osci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
osci.WriteString("buzz beep", 1)
osci.WriteString("VBS 'app.SetToDefaultSetup'", 1)
osci.WriteString("*OPC?", 1)
iesp.setMeasurementTimeout(60000)

# Make sure all skew are at 0. This is not reset by default
print("Setting skew to 0")
osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Deskew = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Deskew = 0'", 1)

# Display the channels
print("Setting channels to display")
osci.WriteString("VBS 'app.Acquisition.C1.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.View = true'", 1)
osci.WriteString("VBS 'app.Acquisition.C1.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C2.Coupling = 0'", 1)
osci.WriteString("VBS 'app.Acquisition.C3.Coupling = 0'", 1)

# Clear display
print("Clearing display")
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(100)

#Autoscale
#osci.WriteString("VBS 'app.Autoset.FindAllVerScale'", 1)
#osci.WriteString("VBS? 'return=app.WaitUntilIdle(5)'", 1)
#osci.WriteString("VBS 'app.Autoset.DoAutosetup'", 1)
#osci.WriteString("*OPC?", 1)
#sleepMillis(200)


# Make sure we're getting mean values

osci.WriteString("VBS 'app.Measure.P1.MeasurementType = 0'", 1)
osci.WriteString("VBS 'app.Measure.ShowMeasure = true",1)
osci.WriteString("VBS 'app.Measure.StatsOn = true",1)
osci.WriteString("VBS 'app.Measure.P1.View = true",1)
osci.WriteString("VBS 'app.Measure.P2.View = False",1)


# Set timebase to proper value

#osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 5e-9'", 1)
#iesp.setMeasurementTimeout(60000)
osci.writestring("VBS 'app.Acquisition.Trigger.C1Slope = 0'", 1)
osci.writestring("VBS 'app.Acquisition.Trigger.Edge.Source = 0'", 1)
#osci.writestring("VBS 'app.Acquisition.Trigger.Edge.FindLevel'", 1)

# Define delta-time measurement parameters

print("Setting delta-time measurement parameters")
osci.WriteString("VBS 'app.Measure.P1.ParamEngine = \"DeltaTimeAtLevel\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope1 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel1 = 50'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.Slope2 = 0'", 1)
osci.WriteString("VBS 'app.Measure.P1.Operator.PercentLevel2 = 50'", 1)

return osci
'''
initScope.wantAllVarsGlobal = False
initScope._showInList = False

measureDeltaTime = SvtFunction()
measureDeltaTime.args = 'channel'
measureDeltaTime.code = r'''# Assumes all measurements are relative to channel 1
import time
channelString = "C%d" % channel
print ("channel string is %s" % channelString)
osci.WriteString("VBS 'app.Measure.P1.Source1 = 0'" , 1)
commandString = "VBS 'app.Measure.P1.Source2 = \"%s\"'" % channelString
osci.WriteString(commandString, 1)
sleepMillis(calOptions.scopeAutoScaleDelay)
commandString = "VBS? 'return = app.Measure.P1.mean.Result.Value'"
osci.WriteString("VBS? 'return=app.WaitUntilIdle(10)'", 1)
osci.WriteString(commandString, 1)
currentDeltaTime = 0

for i in range(calOptions.numAverages) :

    varAmp = osci.WriteString(commandString, 1)
    sleepMillis(50)
    varAmp = osci.ReadString(100)
    osci.WriteString("VBS? 'return=app.WaitUntilIdle(20)'", 1)
    osci.WriteString("*OPC?", 1)
    currentDeltaTime += float(varAmp)
currentDeltaTime = currentDeltaTime / calOptions.numAverages

return currentDeltaTime
'''
measureDeltaTime.wantAllVarsGlobal = False
measureDeltaTime._showInList = False

performScopeCal = SvtFunction()
performScopeCal.args = 'lane, dataRate'
performScopeCal.code = r'''if dataRate >= 3125.0000001:
    osRatio = 2
elif dataRate >= 1500.0000001:
    osRatio = 4
elif dataRate >= 781.2500001:
    osRatio = 8
elif dataRate >= 390.6250001:
    osRatio = 16
elif dataRate >= 195.3125001:
    osRatio = 32
else:
    osRatio = 64

halfUi = 1000000 / (dataRate * osRatio) / 2 * 1e-12
halfUi = halfUi + 3e-12

if lane == 1 :
    print("Performing coarse loop...")
    coarsePos = 0
    finePos = 0

    done = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    laneMask = 0x01 << (lane-1)
    iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(coarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayNeg = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(coarsePos, int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [coarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFineNeg = 0
    iesp.setMipiDataFineSkew(accumulatedFineNeg, finePos, [lane])        #lane 1. neg. pos.
    while not done :
        currentDelayNeg = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done=1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, finePos, [lane])

    print("Fine Neg is %f ps..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 for fs
    fineDelayList = [finePos, accumulatedFineNeg*1e15]

elif lane == 5:
    print("Performing coarse loop...")
    done = 0
    accumulatedCoarsePos = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(accumulatedCoarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < halfUi :
            done = 1
            break
        numSlipsPos = round(currentDelayPos/(2*halfUi))
        accumulatedCoarsePos += numSlipsPos
        iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0550, 0x00, coarseClkSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Pos is %d..." % accumulatedCoarsePos)
    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [accumulatedCoarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFinePos = 0
    accumulatedFineNeg = 0
    iesp.setMipiClockFineSkew(accumulatedFineNeg, accumulatedFinePos)
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFinePos += -1*currentDelayPos
        iesp.setMipiClockFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12)
    # Now do channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiClockFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12)
    print("Fine Pos is %f ps ..." % (accumulatedFinePos*1e12))
    print("Fine Neg is %f ps ..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 to store as fs
    fineDelayList = [accumulatedFinePos*1e15, accumulatedFineNeg*1e15]
else:
    print("Performing coarse loop...")
    done = 0
    accumulatedCoarsePos = 0
    accumulatedCoarseNeg = 0
    #set coarse skews
    laneMask = 0x01 << (lane-1)
    iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(accumulatedCoarsePos, accumulatedCoarseNeg), 'Fail Data Coarse Skew')
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < halfUi :
            done = 1
            break
        numSlipsPos = round(currentDelayPos/(2*halfUi))
        accumulatedCoarsePos += numSlipsPos
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')
    # Now repeat for Channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < halfUi :
            done = 1
            break
        numSlipsNeg = round(currentDelayNeg/(2*halfUi))
        accumulatedCoarseNeg += numSlipsNeg
        iesp.writeSubPartDataBlock(0x0552, laneMask, coarseDataSkewsToString(int(accumulatedCoarsePos), int(accumulatedCoarseNeg)), 'Fail Data Coarse Skew')

    print("Coarse Pos is %d..." % accumulatedCoarsePos)
    print("Coarse Neg is %d..." % accumulatedCoarseNeg)

    coarseDelayList = [accumulatedCoarsePos, accumulatedCoarseNeg]

    ### Then do fine skew
    print("Performing fine loop...")
    done = 0
    accumulatedFinePos = 0
    accumulatedFineNeg = 0
    iesp.setMipiDataFineSkew(accumulatedFineNeg, accumulatedFinePos, [lane])
    while not done:
        currentDelayPos = measureDeltaTime(2)
        print("Detected delay on channel 2 is %e..." % currentDelayPos)
        if abs(currentDelayPos) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFinePos += -1*currentDelayPos
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12, [lane])
    # Now do channel 3
    done = 0
    while not done:
        currentDelayNeg = measureDeltaTime(3)
        print("Detected delay on channel 3 is %e..." % currentDelayNeg)
        if abs(currentDelayNeg) < calOptions.deltaTimeThreshold :
            done = 1
            break
        accumulatedFineNeg += -1*currentDelayNeg
        iesp.setMipiDataFineSkew(accumulatedFineNeg*1e12, accumulatedFinePos*1e12, [lane])
    print("Fine Pos is %f ps ..." % (accumulatedFinePos*1e12))
    print("Fine Neg is %f ps ..." % (accumulatedFineNeg*1e12))

    #mult by 1e15 to store as fs
    fineDelayList = [accumulatedFinePos*1e15, accumulatedFineNeg*1e15]

return (coarseDelayList, fineDelayList)
'''
performScopeCal.wantAllVarsGlobal = False
performScopeCal._showInList = False

writeCalFile = SvtFunction()
writeCalFile.args = 'measuredCoarseDelayDict, measuredFineDelayDict'
writeCalFile.code = r'''import datetime
import os

now = datetime.datetime.now()
date = "%04d%02d%02d" % (now.year, now.month, now.day)

resultFolderCreator1.resultType = "TextReport"
resultFolderCreator1.folderName = "calCoefficients_"+calOptions.serialNumber
folderPath = resultFolderCreator1.run()
FilePathString = "calCoefficients_"+calOptions.serialNumber+".txt"
filePath = os.path.join(folderPath, FilePathString)

##: Create file and while loop to fill it up
with open(filePath, "w") as outFile:
    print("BEGIN SECTION", file=outFile)
    print("section type : header", file=outFile)
    print("serial number : "+calOptions.serialNumber, file=outFile)
    print("hardware revision : RevB", file=outFile)
    print("date of manufacture(YYYYMMDD) : "+date, file=outFile)
    print("date of calibration(YYYYMMDD) : "+date, file=outFile)
    print("speed grade : 1", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type: jitter_calibration_data", file=outFile)
    print("ffffffffffffffffffffffffffffffff00000000000000000000000000000000", file=outFile)
    print("END SECTION", file=outFile)
    print("", file=outFile)
    print("BEGIN SECTION", file=outFile)
    print("section type : dptx_skew_calibration_data", file=outFile)
    print("num lanes : 5", file=outFile)
    print("num data rates : %d" % (len(calOptions.calRates) + 1), file=outFile)

    #need to print an extra entry for 4000Mbps. No longer calibrated at this rate but req for backwards compatibility
    print("#Data Rate = 4000", file=outFile)
    print("#Tx Skew Coarse and Fine", file=outFile)
    print("4000", file=outFile)

    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)
    print("0, 0, 0, 0, 0,", file=outFile)

    for rate in calOptions.calRates:
        if rate >= 3125.0000001:
            osRatio = 2
        elif rate >= 1500.0000001:
            osRatio = 4
        elif rate >= 781.2500001:
            osRatio = 8
        elif rate >= 390.6250001:
            osRatio = 16
        elif rate >= 195.3125001:
            osRatio = 32
        else:
            osRatio = 64
        print("#Data Rate = %f" % (rate*osRatio), file=outFile)
        print("#Tx Skew Coarse and Fine", file=outFile)
        print("%f " % (rate*osRatio), file=outFile)
        for wire in [0,1]:
            print("%d," % measuredCoarseDelayDict[5][rate][wire], end=' ', file=outFile)    #Clk Data
            print("%d," % measuredCoarseDelayDict[1][rate][wire], end=' ', file=outFile)    #Lane 1
            print("%d," % measuredCoarseDelayDict[2][rate][wire], end=' ', file=outFile)    #Lane 2
            print("%d," % measuredCoarseDelayDict[3][rate][wire], end=' ', file=outFile)    #Lane 3
            print("%d," % measuredCoarseDelayDict[4][rate][wire], end=' ', file=outFile)    #Lane 4
            print("", file=outFile)
        for wire in [0,1]:
            print("%d," % measuredFineDelayDict[5][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[1][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[2][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[3][rate][wire], end=' ', file=outFile)
            print("%d," % measuredFineDelayDict[4][rate][wire], end=' ', file=outFile)
            print("", file=outFile)
    print("END SECTION", file=outFile)
'''
writeCalFile.wantAllVarsGlobal = False
writeCalFile._showInList = False



calOptions = SvtDataRecord()
calOptions.addField('serialNumber', descrip='''Serial number for device under test''', attrType=str, defaultVal='1234', displayOrder=(0, 1.0))
calOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2.0))
calOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds''', attrType=float, defaultVal=1000.0, displayOrder=(0, 3.0))
calOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after the scope auto scale funtion.''', attrType=float, defaultVal=2000.0, displayOrder=(0, 4.0))
calOptions.addField('numAverages', descrip='''Number of times the measurement is queried from the scope.''', attrType=int, defaultVal=100, displayOrder=(0, 5.0))
calOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, attrSubType=int, defaultVal=[1, 2, 3, 4, 5], displayOrder=(0, 6.0))
calOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, attrSubType=float, defaultVal=[80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5, 6500.0], displayOrder=(0, 7.0))
calOptions.addField('scopeSetupFile', descrip='''''', attrType=str, defaultVal='Placeholder', displayOrder=(0, 8.0))
calOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence''', attrType=float, defaultVal=3e-12, displayOrder=(0, 9.0))
calOptions.addField('scopeConnectionTimeout', descrip='''Timeout used by PyVisa''', attrType=float, defaultVal=10000.0, displayOrder=(0, 10.0))
calOptions.addMethod('_customInit',
	'',
	r'''# The method '_customInit' is a special case.
# It is automatically called immediately after a new DataRecord instance is created.
# You can put code here to do custom initialization.
pass
''',
	False)
calOptions.serialNumber = '1234'
calOptions.scopeIPAddress = 'TCPIP0::10.20.20.200::inst0::INSTR'
calOptions.scopeMeasurementDelay = 1000.0
calOptions.scopeAutoScaleDelay = 2000.0
calOptions.numAverages = 100
calOptions.calLanes = [1, 2, 3, 4, 5]
calOptions.calRates = [80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5, 6500.0]
calOptions.scopeSetupFile = 'Placeholder'
calOptions.deltaTimeThreshold = 3e-12
calOptions.scopeConnectionTimeout = 10000.0
calOptions.callCustomInitMethod()

dphyColorBarPattern1 = SvtMipiDphyCsiColorBarPattern()
dphyColorBarPattern1.enableCsiEpd = False
dphyColorBarPattern1.errorInsertion = None
dphyColorBarPattern1.frameBlankingMode = 'frameRate'
dphyColorBarPattern1.frameRate = 4.0
dphyColorBarPattern1.gaussianBlurRadius = 0
dphyColorBarPattern1.horizLineTime = 65800.0
dphyColorBarPattern1.imageFormat = 'CSI_RGB888'
dphyColorBarPattern1.imageHeight = 480
dphyColorBarPattern1.imageWidth = 640
dphyColorBarPattern1.lineNumbering = 'disabled'
dphyColorBarPattern1.lineTimeMode = 'lineTimeTotal'
dphyColorBarPattern1.preBuiltColorBar = ColorBar_ctsHsTestPattern
dphyColorBarPattern1.timeUnits = 'nanosecond'
dphyColorBarPattern1.usePreBuiltColorBar = True
dphyColorBarPattern1.virtualChannel = 0
dphyColorBarPattern1.wantFrameNumbering = False
dphyColorBarPattern1._showInList = False

dphyParameters1 = SvtMipiDphyParameters()
dphyParameters1.clockTrailBits = ''
dphyParameters1.clockZeroBits = '0000'
dphyParameters1.hsTrailBits = ''
dphyParameters1.hsZeroBits = '0000'
dphyParameters1.sotBits = '00011101'
dphyParameters1.tAlpClk01Duration = (0.0, 20.0)
dphyParameters1.tAlpClk10Duration = (0.0, 40.0)
dphyParameters1.tAlpHs01Duration = (0.0, 20.0)
dphyParameters1.tAlpHs10Duration = (0.0, 40.0)
dphyParameters1.tAlpxDuration = 120.0
dphyParameters1.tClockLpx01Duration = (0.0, 80.0)
dphyParameters1.tClockPostDuration = (60.0, 60.0)
dphyParameters1.tClockPreDuration = (32.0, 0.0)
dphyParameters1.tClockPrepareDuration = (0.0, 80.0)
dphyParameters1.tClockTrailDuration = (0.0, 80.0)
dphyParameters1.tClockZeroDuration = (0.0, 300.0)
dphyParameters1.tHsExitDuration = 240.0
dphyParameters1.tHsIdleClkHs0Duration = (0.0, 60.0)
dphyParameters1.tHsIdlePostDuration = 8
dphyParameters1.tHsIdlePreDuration = 8
dphyParameters1.tHsLpx01Duration = (0.0, 80.0)
dphyParameters1.tHsPrepareDuration = (5.0, 60.0)
dphyParameters1.tHsTrailDuration = (8.0, 60.0)
dphyParameters1.tHsZeroDuration = (10.0, 145.0)
dphyParameters1.tTaGetDuration = 5
dphyParameters1.tTaGoDuration = 4.0
dphyParameters1.tTaSureDuration = 1.5
dphyParameters1.tlpxDuration = 80.0
dphyParameters1.useAlp = False
dphyParameters1.usePreambleSequence = False
dphyParameters1._showInList = False

mipiProtocol = SvtMipiProtocol()
mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig = SvtRefClocksConfig()
refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

mipiClockConfig1 = SvtMipiClockConfig()
mipiClockConfig1.dataRate = 800.0
mipiClockConfig1.referenceClocks = refClocksConfig
mipiClockConfig1.sscEnabled = False

mipiDphyGenerator1 = SvtMipiDphyGenerator()
mipiDphyGenerator1.clockConfig = mipiClockConfig1
mipiDphyGenerator1.clockSkew = 0.0
mipiDphyGenerator1.continuousClock = False
mipiDphyGenerator1.dataLanes = [1, 2, 3, 4]
mipiDphyGenerator1.dataSkews = [0.0]
mipiDphyGenerator1.hsClockCommonVoltage = 200.0
mipiDphyGenerator1.hsClockPostTap = 0
mipiDphyGenerator1.hsClockPreTap = 0
mipiDphyGenerator1.hsClockVoltageAmplitude = 200.0
mipiDphyGenerator1.hsDataCommonVoltages = [200.0]
mipiDphyGenerator1.hsDataPostTaps = [0]
mipiDphyGenerator1.hsDataPreTaps = [0]
mipiDphyGenerator1.hsDataVoltageAmplitudes = [200.0]
mipiDphyGenerator1.jitterInjection = None
mipiDphyGenerator1.lpClockHighVoltage = 1200.0
mipiDphyGenerator1.lpClockLowVoltage = 0.0
mipiDphyGenerator1.lpDataHighVoltages = [1200.0]
mipiDphyGenerator1.lpDataLowVoltages = [0.0]
mipiDphyGenerator1.params = dphyParameters1
mipiDphyGenerator1.pattern = dphyColorBarPattern1
mipiDphyGenerator1.resetPatternMemory = True
mipiDphyGenerator1.splitDataAcrossLanes = True
mipiDphyGenerator1._showInList = False

resultFolderCreator1 = SvtResultFolderCreator()
resultFolderCreator1.folderName = ''
resultFolderCreator1.resultType = 'CsvData'
resultFolderCreator1._showInList = False



#! TEST PROCEDURE
iesp = getIespInstance()
# Connect to scope
osci = initScope(calOptions.scopeIPAddress)

maxDataRate = iesp.getLimitMaximum("dataRate")

if maxDataRate != 6500:
    calOptions.calRates = [80.0, 93.75, 109.375, 125.0, 140.625, 156.25, 171.875, 187.5]


# Initialize generator
fileName = "GeneratedDphyPattern_compiled.csv"
mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
#mipiDphyGenerator1.usePatternsFile = True
mipiDphyGenerator1.dataLanes = calOptions.calLanes
mipiDphyGenerator1.setup()

# Define results dictionary
measuredCoarseDelayDict = dict()
measuredFineDelayDict = dict()

dftUtil.beep(554,250)
dftUtil.beep(554,320)
myString = "Please ensure a default cal file has been loaded on the module."
waitForGuiOkDialog(myString)

# Declare global dictionary
for lane in range(1,6,1) :
   measuredCoarseDelayDict[lane] = dict()
   measuredFineDelayDict[lane] = dict()
   for dataRate in sorted(calOptions.calRates) :
      measuredCoarseDelayDict[lane][dataRate] = dict()
      measuredFineDelayDict[lane][dataRate] = dict()
      for wire in [0,1]:
          measuredCoarseDelayDict[lane][dataRate][wire] = 0
          measuredFineDelayDict[lane][dataRate][wire] = 0

for lane in mipiDphyGenerator1.dataLanes:
    dftUtil.beep(554,250)
    dftUtil.beep(554,320)
    print("Measuring D-PHY Lane %d..." % lane)
    if lane == 1 :
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch1, Wire Neg to Ch2' % lane
    elif lane == 5:
        myString = 'Please connect clock signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1'
    else:
        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1' % lane
    waitForGuiOkDialog(myString)


    autoScale = True

    for dataRate in calOptions.calRates :
        print("Measuring at %f Mbps..." % dataRate)
        measuredCoarseDelayDict[lane][dataRate] = list()
        measuredFineDelayDict[lane][dataRate] = list()

        iesp.writeSubPartRegister(0x0930, 0x00, 0x01) # enable cal mode
        fileName = "GeneratedDphyPattern_compiled.csv"
        mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
       # mipiDphyGenerator1.usePatternsFile = True
        mipiClockConfig1.dataRate = dataRate
        mipiDphyGenerator1.setup()
        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern

        # Prepare scope for measurement
        if(autoScale):
            autoscaleScope()
            autoScale = False

        # Use scope to measure values
        (coarseDelayList, fineDelayList) = performScopeCal(lane,dataRate)

        # Assmeble into dictionaries
        measuredCoarseDelayDict[lane][dataRate] = coarseDelayList
        measuredFineDelayDict[lane][dataRate] = fineDelayList

# Disable alignment pattern
iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
mipiDphyGenerator1.setup()

writeCalFile(measuredCoarseDelayDict, measuredFineDelayDict)
