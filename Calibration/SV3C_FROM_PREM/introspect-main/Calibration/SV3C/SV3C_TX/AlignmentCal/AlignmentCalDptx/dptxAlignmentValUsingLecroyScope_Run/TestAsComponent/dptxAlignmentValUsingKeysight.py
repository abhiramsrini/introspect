
# Generated via SvtTestAsComponent from Test 'dptxAlignmentValUsingLecroyScope_Run'
# 2025-10-28_1209

import os

import dftm.util as dftUtil
from dftm.svt import *
from dftm.svtComponent import SvtAttr
from dftm.componentStore import DynamicFactory
from dftm.components.basic.testAsComponent import SvtLocalTest
# Import NumPy/SciPy names since these might be used in user code:

#-------------------------------------------
@DynamicFactory.iesp(None)
def factory(B):
    class dptxAlignmentValUsingKeysight(B.SvtRunnableWithResultIespComponent):
        '''
        Regression script for validating timing alignment on the SV3C D-PHY Generator
        '''
        clsVisibleInGui = True
        category = 'testAsComponent'
        
        generatedBy = B.SvtTestAsComponent
        
        def __init__(self):
            super().__init__()
            self._localTest = None
            self._creatDone = False
        
        def _saveSymbol(self, name, value):
            if self._localTest is None:
                return
            self._localTest.saveSymbol(name, value)
        
        def _removeSavedSymbols(self):
            if self._localTest is None:
                return
            self._localTest.removeSavedSymbols()
        
        def _getSymbol(self, name):
            if self._localTest is None:
                return None
            return self._localTest.dictForRun.get(name)
        
        def _getComponent(self, name):
            if self._localTest is None:
                return None
            return self._localTest.getComponent(name, self.iesp)
        
        serialNumber = SvtAttr('serialNumber', displayOrder = (0, 1),
                defaultVal = '1234',
                descrip = '''Serial number for device under test''',
                attrType = str,
                )
        
        scopeIPAddress = SvtAttr('scopeIPAddress', displayOrder = (0, 2),
                defaultVal = 'TCPIP0::10.20.20.200::inst0::INSTR',
                descrip = '''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''',
                attrType = str,
                )
        
        scopeMeasurementDelay = SvtAttr('scopeMeasurementDelay', displayOrder = (0, 3),
                defaultVal = 1000.0,
                descrip = '''Amount of average accumulation time in milliseconds''',
                attrType = float,
                )
        
        scopeAutoScaleDelay = SvtAttr('scopeAutoScaleDelay', displayOrder = (0, 4),
                defaultVal = 2000.0,
                descrip = '''Amount of time after the scope auto scale funtion.''',
                attrType = float,
                )
        
        numAverages = SvtAttr('numAverages', displayOrder = (0, 5),
                defaultVal = 100,
                descrip = '''Number of times the measurement is queried from the scope.''',
                attrType = int,
                )
        
        calLanes = SvtAttr('calLanes', displayOrder = (0, 6),
                defaultVal = [1, 2, 3, 4],
                descrip = '''Range of lanes to measure''',
                attrType = list,
                attrSubType = int,
                )
        
        calRates = SvtAttr('calRates', displayOrder = (0, 7),
                defaultVal = [80.0, 125.0, 187.5, 6500.0],
                descrip = '''Rates at which we will collect alignment data.''',
                attrType = list,
                attrSubType = float,
                )
        
        deltaTimeThreshold = SvtAttr('deltaTimeThreshold', displayOrder = (0, 8),
                defaultVal = 1e-11,
                descrip = '''Threshold for alignment convergence''',
                attrType = float,
                )
        
        scopeConnectionTimeout = SvtAttr('scopeConnectionTimeout', displayOrder = (0, 9),
                defaultVal = 10000.0,
                descrip = '''Scope connection timeout.''',
                attrType = float,
                )
        
        minVersion = SvtAttr('minVersion', displayOrder = (0, 10),
                defaultVal = '3.5.55',
                descrip = '''Minimum Introspect ESP software version that is supported by this script.''',
                attrType = str,
                )
        
        #-------------------------------------------
        
        def _creat(self):
            logger.debug('%s: Creation of internal components' % self.name)
            
            # Builtin Components:
            ColorBar_ctsHsTestPattern = B.SvtComponent.builtins['ColorBar_ctsHsTestPattern']
            
            # SVT Test
            # SVT version 25.3.0
            # Test saved 2025-10-28_1209
            # Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR
            # PY3
            # Checksum: e2edb5d08799ced8299b2922d0627a2c
            # Note: This file is the 'Save' file for the Test.
            #       It should not be used as a standalone Python script.
            #       But it can be used via 'runSvtTest.py'.
            
            dphyColorBarPattern1 = _create('dphyColorBarPattern1', 'SvtMipiDphyCsiColorBarPattern')
            dphyParameters1 = _create('dphyParameters1', 'SvtMipiDphyParameters')
            mipiDphyGenerator1 = _create('mipiDphyGenerator1', 'SvtMipiDphyGenerator')
            mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
            refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
            resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
            
            dphyColorBarPattern1.blankingDuration = 3000.0
            dphyColorBarPattern1.cseParams = None
            dphyColorBarPattern1.csiCompressionParams = None
            dphyColorBarPattern1.enableCsiEpd = False
            dphyColorBarPattern1.epdOption = 'option1'
            dphyColorBarPattern1.errorInsertion = None
            dphyColorBarPattern1.frameBlankingDuration = 30000.0
            dphyColorBarPattern1.frameBlankingMode = 'frameRate'
            dphyColorBarPattern1.frameRate = 4.0
            dphyColorBarPattern1.gaussianBlurRadius = 0
            dphyColorBarPattern1.horizLineTime = 65800.0
            dphyColorBarPattern1.imageFormat = 'CSI_RGB888'
            dphyColorBarPattern1.imageHeight = 480
            dphyColorBarPattern1.imageWidth = 640
            dphyColorBarPattern1.lineNumbering = 'disabled'
            dphyColorBarPattern1.lineTimeMode = 'lineTimeTotal'
            dphyColorBarPattern1.numCols = 8
            dphyColorBarPattern1.numLongPacketEpdSpacers = 0
            dphyColorBarPattern1.numRows = 2
            dphyColorBarPattern1.numShortPacketEpdSpacers = 0
            dphyColorBarPattern1.numVideoFrames = None
            dphyColorBarPattern1.preBuiltColorBar = ColorBar_ctsHsTestPattern
            dphyColorBarPattern1.rawFormatBayerCell = 'BGGR'
            dphyColorBarPattern1.rawValues = None
            dphyColorBarPattern1.regionsOfInterest = []
            dphyColorBarPattern1.rgbValues = None
            dphyColorBarPattern1.sendRoiInfo = False
            dphyColorBarPattern1.timeUnits = 'nanosecond'
            dphyColorBarPattern1.usePreBuiltColorBar = True
            dphyColorBarPattern1.useRoi = False
            dphyColorBarPattern1.useVideoFps = False
            dphyColorBarPattern1.valuesMode = 'rgb'
            dphyColorBarPattern1.videoFile = ''
            dphyColorBarPattern1.virtualChannel = 0
            dphyColorBarPattern1.wantFrameNumbering = False
            
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
            dphyParameters1.tPreamble = 32
            dphyParameters1.tTaGetDuration = 5
            dphyParameters1.tTaGoDuration = 4.0
            dphyParameters1.tTaSureDuration = 1.5
            dphyParameters1.tlpxDuration = 80.0
            dphyParameters1.useAlp = False
            dphyParameters1.usePreambleSequence = False
            
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
            
            mipiProtocol.csiScramble = False
            mipiProtocol.csiVersion = 'Csi2_v1_3'
            mipiProtocol.protocol = 'CSI'
            mipiProtocol.useEotp = False
            
            refClocksConfig.externRefClockFreq = 250.0
            refClocksConfig.outputClockAFormat = 'LVDS'
            refClocksConfig.outputClockAFreq = 100.0
            refClocksConfig.outputClockBFormat = 'LVDS'
            refClocksConfig.outputClockBFreq = 100.0
            refClocksConfig.systemRefClockSource = 'internal'
            
            resultFolderCreator1.folderName = ''
            resultFolderCreator1.resultType = 'CsvData'
            
            dphyColorBarPattern1._showInList = False
            dphyParameters1._showInList = False
            mipiDphyGenerator1._showInList = False
            resultFolderCreator1._showInList = False
            # Alias for DataRecord that defines properties of this component:
            validationOptions = self
            
            # ensure that 'IESP' is available in case user refers to it
            from dftm.iespCore import IESP
            
            def autoscaleScope():
                osci = self._getSymbol('osci')
                import time
                
                
                # Clear display
                osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
                sleepMillis(200)
                
                
                
                
                time.sleep(3)
            
            def initScope(scopeIpAddress):
                iesp = self._getSymbol('iesp')
                osci = self._getSymbol('osci')
                import pyvisa
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
                
                # Set Vertical scale for Channel 3 to proper value
                
                osci.writestring("VBS 'app.Acquisition.C1.VerScale = 50e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.C1.VerOffset = -120.02e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.C2.VerScale = 50e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.C2.VerOffset = -120.02e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.C3.VerScale = 50e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.C3.VerOffset = -120.02e-3'", 1)
                
                iesp.setMeasurementTimeout(60000)
                
                # Turn averaging on
                
                osci.writestring("VBS 'app.Acquisition.C1.AverageSweeps = 16'", 1)
                osci.writestring("VBS 'app.Acquisition.C2.AverageSweeps = 16'", 1)
                osci.writestring("VBS 'app.Acquisition.C3.AverageSweeps = 16'", 1)
                
                # Set timebase to proper value
                
                osci.WriteString("VBS 'app.Acquisition.Horizontal.HorScale = 100e-12'", 1)
                osci.WriteString("VBS 'app.Acquisition.Trigger.Edge.Slope = \"Positive\"'", 1)
                
                osci.writestring("VBS 'app.Acquisition.Trigger.Edge.Source = 0'", 1)
                osci.writestring("VBS 'app.Acquisition.Trigger.C1Slope = 0'", 1)
                osci.writestring("VBS 'app.Acquisition.Trigger.C1Level = 120e-3'", 1)
                osci.writestring("VBS 'app.Acquisition.TriggerMode = 1'", 1)
                
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
                osci.WriteString("VBS 'app.Measure.P1.Out.Result.Details'", 1)
                return osci
            
            def measureDeltaTime(channel):
                osci = self._getSymbol('osci')
                # Assumes all measurements are relative to channel 1
                import time
                channelString = "C%d" % channel
                print ("channel string is %s" % channelString)
                osci.WriteString("VBS 'app.Measure.P1.Source1 = 0'" , 1)
                
                commandString = "VBS 'app.Measure.P1.Source2 = \"%s\"'" % channelString
                osci.WriteString(commandString, 1)
                sleepMillis(200)
                commandString = "VBS? 'return = app.Measure.P1.Out.Result.Value'"
                osci.WriteString(commandString, 1)
                currentDeltaTime = 0
                
                for i in range(validationOptions.numAverages) :
                
                    varAmp = osci.WriteString(commandString, 1)
                    sleepMillis(200)
                    varAmp = osci.ReadString(100)
                    osci.WriteString("VBS? 'return=app.WaitUntilIdle(10)'", 1)
                    osci.WriteString("*OPC?", 1)
                    #print("The DeltaTime@Level value is %s" %varAmp)
                   #time.sleep(10)
                    currentDeltaTime += float(varAmp.strip())
                
                currentDeltaTime = currentDeltaTime / validationOptions.numAverages
                
                return currentDeltaTime
            
            def performScopeMeasurement(lane, dataRate):
                delayList = self._getSymbol('delayList')
                if lane == 1 :
                    currentDelayPos = 0
                    currentDelayNeg = measureDeltaTime(2)
                
                    delayList = [currentDelayPos, currentDelayNeg]
                
                elif lane == 5:
                    currentDelayPos = measureDeltaTime(2)
                    currentDelayNeg = measureDeltaTime(3)
                
                    delayList = [currentDelayPos, currentDelayNeg]
                
                else:
                    currentDelayPos = measureDeltaTime(2)
                    currentDelayNeg = measureDeltaTime(3)
                
                    delayList = [currentDelayPos, currentDelayNeg]
                
                return delayList
            
            def performValidationOnCollectedData(fineDelayDict):
                print("Checking measured data...")
                for rate in validationOptions.calRates :
                    for lane in validationOptions.calLanes :
                        for wire in range(2) :
                            measuredError = abs( fineDelayDict[lane][rate][wire])
                            if measuredError > validationOptions.deltaTimeThreshold :
                                print("Found a failing condition on Lane %d..." % lane)
                                print("Measured error is %g s..." % measuredError)
                                return False
                
                return True
            
            def writeRawData(delayDict):
                filePath = self._getSymbol('filePath')
                filePath = self._getSymbol('filePath')
                import time
                import os
                ## dd/mm/yyyy format
                dateToday = time.strftime("%d/%m/%Y")
                timeNow = time.strftime("%H:%M:%S")
                
                resultFolderCreator1.folderName = validationOptions.serialNumber
                folderPath = resultFolderCreator1.run()
                
                stringAppendix = ".csv"
                filePathString = validationOptions.serialNumber + "_DptxAlignmentValidationData" + stringAppendix
                filePath = os.path.join(folderPath, filePathString)
                with open(filePath, "w") as outFile:
                    print("DPTX Alignment Validation Data", file=outFile)
                    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)
                    print("Date, %s" % dateToday, file=outFile)
                    print("Time, %s" % timeNow, file=outFile)
                    print(" ,", file=outFile)
                    print("Lane, Data Rate, Skew Pos, Skew Neg", file=outFile)
                    for lane in validationOptions.calLanes :
                        for dataRate in validationOptions.calRates :
                            print("%d, %f, %g, %g, " % (lane, dataRate, delayDict[lane][dataRate][0], delayDict[lane][dataRate][1]), file=outFile)
            
            # Create LocalTest and register internal components:
            folderOfThisScript = os.path.dirname(os.path.realpath(__file__))
            self._localTest = SvtLocalTest(folderOfThisScript, locals())
            self._localTest.registerComponent('ColorBar_ctsHsTestPattern', ColorBar_ctsHsTestPattern)
            self._localTest.registerComponent('dphyColorBarPattern1', dphyColorBarPattern1)
            self._localTest.registerComponent('dphyParameters1', dphyParameters1)
            self._localTest.registerComponent('mipiDphyGenerator1', mipiDphyGenerator1)
            self._localTest.registerComponent('refClocksConfig', refClocksConfig)
            self._localTest.registerComponent('resultFolderCreator1', resultFolderCreator1)
            self._creatDone = True
            self._customInit()
        
        def _customInit(self):
            if not self._creatDone:
                self._creat()
            
            # The method '_customInit' is a special case.
            # It is automatically called immediately after a new DataRecord instance is created.
            # You can put code here to do custom initialization.
            pass
        
        def _run(self):
            logger.debug('Starting run of %s' % self.name)
            if not self._creatDone:
                self._creat()
            
            # Alias for DataRecord that defines properties of this component:
            validationOptions = self
            
            # ensure that 'IESP' is available in case user refers to it
            from dftm.iespCore import IESP
            
            # Components referred to below:
            ColorBar_ctsHsTestPattern = self._getComponent('ColorBar_ctsHsTestPattern')
            dphyColorBarPattern1 = self._getComponent('dphyColorBarPattern1')
            dphyParameters1 = self._getComponent('dphyParameters1')
            mipiDphyGenerator1 = self._getComponent('mipiDphyGenerator1')
            refClocksConfig = self._getComponent('refClocksConfig')
            resultFolderCreator1 = self._getComponent('resultFolderCreator1')
            # Functions referred to below:
            autoscaleScope = self._getSymbol('autoscaleScope')
            initScope = self._getSymbol('initScope')
            performScopeMeasurement = self._getSymbol('performScopeMeasurement')
            performValidationOnCollectedData = self._getSymbol('performValidationOnCollectedData')
            writeRawData = self._getSymbol('writeRawData')
            
            # Tell internal components the testRunResult:
            runResultFolderPath = self.createRunResultFolder(resultType='CsvData', viewSubComponents=)
            if runResultFolderPath is None:
                return
            self._localTest.tellComponentsToUseRunResultFolder(runResultFolderPath)
            ColorBar_ctsHsTestPattern.initForTestRun()
            dphyColorBarPattern1.initForTestRun()
            dphyParameters1.initForTestRun()
            mipiDphyGenerator1.initForTestRun()
            refClocksConfig.initForTestRun()
            resultFolderCreator1.initForTestRun()
            
            #! TEST PROCEDURE
            # Check Version
            svtVersion = getSvtVersion()
            self._saveSymbol('svtVersion', svtVersion)
            #if svtVersion < validationOptions.minVersion:
             #   errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))
            
            iesp = getIespInstance()
            self._saveSymbol('iesp', iesp)
            maxDataRate = iesp.getLimitMaximum("dataRate")
            self._saveSymbol('maxDataRate', maxDataRate)
            
            if maxDataRate != 6500:
            
            # Connect to scope
            osci = initScope(validationOptions.scopeIPAddress)
            self._saveSymbol('osci', osci)
            
            # Initialize generator
            fileName = "GeneratedDphyPattern_compiled.csv"
            self._saveSymbol('fileName', fileName)
            mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
            mipiDphyGenerator1.dataLanes = validationOptions.calLanes
            mipiDphyGenerator1.setup()
            
            # Define results dictionary
            measuredCoarseDelayDict = dict()
            self._saveSymbol('measuredCoarseDelayDict', measuredCoarseDelayDict)
            measuredFineDelayDict = dict()
            self._saveSymbol('measuredFineDelayDict', measuredFineDelayDict)
            
            # Start main loop
            for lane in validationOptions.calLanes:
                dftUtil.beep(554,250)
                dftUtil.beep(554,320)
                print("Measuring D-PHY Lane %d..." % lane)
                if lane == 1 :
                    myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch1, Wire Neg to Ch2' % lane
                    self._saveSymbol('myString', myString)
                elif lane == 5:
                    myString = 'Please connect clock signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1'
                    self._saveSymbol('myString', myString)
                else:
                    myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1' % lane
                    self._saveSymbol('myString', myString)
                waitForGuiOkDialog(myString)
            
                measuredFineDelayDict[lane] = dict()
                autoScale = True
                self._saveSymbol('autoScale', autoScale)
            
                for dataRate in validationOptions.calRates :
                    print("Measuring at %f Mbps..." % dataRate)
                    measuredFineDelayDict[lane][dataRate] = list()
            
                    iesp.writeSubPartRegister(0x0930, 0x00, 0x00) # clear cal mode
                    fileName = "GeneratedDphyPattern_compiled.csv"
                    self._saveSymbol('fileName', fileName)
                    mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)
                    mipiDphyGenerator1.setup()
                    iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern
            
                    # Prepare scope for measurement
                    autoscaleScope()
            
                    # Use scope to measure values
                    delayList = performScopeMeasurement(lane,dataRate)
                    self._saveSymbol('delayList', delayList)
            
                    # Assmeble into dictionaries
                    measuredFineDelayDict[lane][dataRate] = delayList
            
            # Write all collected data points to file
            writeRawData(measuredFineDelayDict)
            
            # Disable alignment pattern
            iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern
            mipiDphyGenerator1.setup()
            
            if performValidationOnCollectedData(measuredFineDelayDict) :
                writeNoteForTestRun("Pass")
                failFlag = 0
                self._saveSymbol('failFlag', failFlag)
            else :
                writeNoteForTestRun("Fail")
                failFlag = 1
                self._saveSymbol('failFlag', failFlag)
            
            if failFlag == 0 :
                writeNoteForTestRun("PASS")
                filePath = getParamsFilePath("Pass.png")
                self._saveSymbol('filePath', filePath)
            
                myFileUrl = str(filePath)
                self._saveSymbol('myFileUrl', myFileUrl)
            
                popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
            elif failFlag:
                writeNoteForTestRun("FAIL, please check report")
                filePath = getParamsFilePath("Fail.png")
                self._saveSymbol('filePath', filePath)
            
                myFileUrl = str(filePath)
                self._saveSymbol('myFileUrl', myFileUrl)
            
                popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)
            self._removeSavedSymbols()
        
        def run(self):
            retVal = self._run()
            return retVal
        
        def getReturnValueStr(self):
            return 'retVal'
        
        #-------------------------------------------
        #-------------------------------------------
        
    
    # Component creation function
    def _create(componentName, componentClassName, iespName=None):
        cls = B.get(componentClassName)
        instance = cls()
        instance.name = componentName,
        return instance
    
    return dptxAlignmentValUsingKeysight
#TEST_PROCEDURE_FILE_CONTENT = ['# SVT Test', '# SVT version 25.3.0', '# Test saved 2025-10-28_1209', '# Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR', '# PY3', '# Checksum: e2edb5d08799ced8299b2922d0627a2c', "# Note: This file is the 'Save' file for the Test.", '#       It should not be used as a standalone Python script.', "#       But it can be used via 'runSvtTest.py'.", '', '', "autoscaleScope = _create('autoscaleScope', 'SvtFunction', iespName=None)", "initScope = _create('initScope', 'SvtFunction', iespName=None)", "measureDeltaTime = _create('measureDeltaTime', 'SvtFunction', iespName=None)", "performScopeMeasurement = _create('performScopeMeasurement', 'SvtFunction', iespName=None)", "performValidationOnCollectedData = _create('performValidationOnCollectedData', 'SvtFunction', iespName=None)", "validationOptions = _create('validationOptions', 'SvtDataRecord', iespName=None)", "writeRawData = _create('writeRawData', 'SvtFunction', iespName=None)", '', "dphyColorBarPattern1 = _create('dphyColorBarPattern1', 'SvtMipiDphyCsiColorBarPattern')", "dphyParameters1 = _create('dphyParameters1', 'SvtMipiDphyParameters')", "mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')", "mipiDphyGenerator1 = _create('mipiDphyGenerator1', 'SvtMipiDphyGenerator')", "mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')", "refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')", "resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')", "testAsComponent1 = _create('testAsComponent1', 'SvtTestAsComponent')", '', "autoscaleScope.args = ''", 'autoscaleScope.code = r\'\'\'import time\n\n\n# Clear display\nosci.WriteString("VBS \'app.Measure.ClearSweeps\'", 1)\nsleepMillis(200)\n\n\n\n\ntime.sleep(3)\n\'\'\'', 'autoscaleScope.wantAllVarsGlobal = False', '', "initScope.args = 'scopeIpAddress'", 'initScope.code = r\'\'\'import pyvisa\n#connect to scope\nimport win32com.client #imports the pywin32 library\nosci=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")\nosci.MakeConnection("IP:169.254.197.102")\nosci.WriteString("buzz beep", 1)\nosci.WriteString("VBS \'app.SetToDefaultSetup\'", 1)\nosci.WriteString("*OPC?", 1)\niesp.setMeasurementTimeout(60000)\n\n# Make sure all skew are at 0. This is not reset by default\nprint("Setting skew to 0")\nosci.WriteString("VBS \'app.Acquisition.C1.Deskew = 0\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C2.Deskew = 0\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C3.Deskew = 0\'", 1)\n\n# Display the channels\nprint("Setting channels to display")\nosci.WriteString("VBS \'app.Acquisition.C1.View = true\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C2.View = true\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C3.View = true\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C1.Coupling = 0\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C2.Coupling = 0\'", 1)\nosci.WriteString("VBS \'app.Acquisition.C3.Coupling = 0\'", 1)\n\n# Clear display\nprint("Clearing display")\nosci.WriteString("VBS \'app.Measure.ClearSweeps\'", 1)\nsleepMillis(100)\n\n#Autoscale\n#osci.WriteString("VBS \'app.Autoset.FindAllVerScale\'", 1)\n#osci.WriteString("VBS? \'return=app.WaitUntilIdle(5)\'", 1)\n#osci.WriteString("VBS \'app.Autoset.DoAutosetup\'", 1)\n#osci.WriteString("*OPC?", 1)\n#sleepMillis(200)\n\n\n# Make sure we\'re getting mean values\n\nosci.WriteString("VBS \'app.Measure.P1.MeasurementType = 0\'", 1)\nosci.WriteString("VBS \'app.Measure.ShowMeasure = true",1)\nosci.WriteString("VBS \'app.Measure.StatsOn = true",1)\nosci.WriteString("VBS \'app.Measure.P1.View = true",1)\nosci.WriteString("VBS \'app.Measure.P2.View = False",1)\n\n# Set Vertical scale for Channel 3 to proper value\n\nosci.writestring("VBS \'app.Acquisition.C1.VerScale = 50e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.C1.VerOffset = -120.02e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.C2.VerScale = 50e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.C2.VerOffset = -120.02e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.C3.VerScale = 50e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.C3.VerOffset = -120.02e-3\'", 1)\n\niesp.setMeasurementTimeout(60000)\n\n# Turn averaging on\n\nosci.writestring("VBS \'app.Acquisition.C1.AverageSweeps = 16\'", 1)\nosci.writestring("VBS \'app.Acquisition.C2.AverageSweeps = 16\'", 1)\nosci.writestring("VBS \'app.Acquisition.C3.AverageSweeps = 16\'", 1)\n\n# Set timebase to proper value\n\nosci.WriteString("VBS \'app.Acquisition.Horizontal.HorScale = 100e-12\'", 1)\nosci.WriteString("VBS \'app.Acquisition.Trigger.Edge.Slope = \\"Positive\\"\'", 1)\n\nosci.writestring("VBS \'app.Acquisition.Trigger.Edge.Source = 0\'", 1)\nosci.writestring("VBS \'app.Acquisition.Trigger.C1Slope = 0\'", 1)\nosci.writestring("VBS \'app.Acquisition.Trigger.C1Level = 120e-3\'", 1)\nosci.writestring("VBS \'app.Acquisition.TriggerMode = 1\'", 1)\n\n# Set timebase to proper value\n\n#osci.writestring("VBS \'app.Acquisition.Horizontal.HorScale = 5e-9\'", 1)\n#iesp.setMeasurementTimeout(60000)\nosci.writestring("VBS \'app.Acquisition.Trigger.C1Slope = 0\'", 1)\nosci.writestring("VBS \'app.Acquisition.Trigger.Edge.Source = 0\'", 1)\n#osci.writestring("VBS \'app.Acquisition.Trigger.Edge.FindLevel\'", 1)\n\n# Define delta-time measurement parameters\n\nprint("Setting delta-time measurement parameters")\nosci.WriteString("VBS \'app.Measure.P1.ParamEngine = \\"DeltaTimeAtLevel\\"\'", 1)\nosci.WriteString("VBS \'app.Measure.P1.Operator.Slope1 = 0\'", 1)\nosci.WriteString("VBS \'app.Measure.P1.Operator.PercentLevel1 = 50\'", 1)\nosci.WriteString("VBS \'app.Measure.P1.Operator.Slope2 = 0\'", 1)\nosci.WriteString("VBS \'app.Measure.P1.Operator.PercentLevel2 = 50\'", 1)\nosci.WriteString("VBS \'app.Measure.P1.Out.Result.Details\'", 1)\nreturn osci\n\'\'\'', 'initScope.wantAllVarsGlobal = False', '', "measureDeltaTime.args = 'channel'", 'measureDeltaTime.code = r\'\'\'# Assumes all measurements are relative to channel 1\nimport time\nchannelString = "C%d" % channel\nprint ("channel string is %s" % channelString)\nosci.WriteString("VBS \'app.Measure.P1.Source1 = 0\'" , 1)\n\ncommandString = "VBS \'app.Measure.P1.Source2 = \\"%s\\"\'" % channelString\nosci.WriteString(commandString, 1)\nsleepMillis(200)\ncommandString = "VBS? \'return = app.Measure.P1.Out.Result.Value\'"\nosci.WriteString(commandString, 1)\ncurrentDeltaTime = 0\n\nfor i in range(validationOptions.numAverages) :\n\n    varAmp = osci.WriteString(commandString, 1)\n    sleepMillis(200)\n    varAmp = osci.ReadString(100)\n    osci.WriteString("VBS? \'return=app.WaitUntilIdle(10)\'", 1)\n    osci.WriteString("*OPC?", 1)\n    #print("The DeltaTime@Level value is %s" %varAmp)\n   #time.sleep(10)\n    currentDeltaTime += float(varAmp.strip())\n\ncurrentDeltaTime = currentDeltaTime / validationOptions.numAverages\n\nreturn currentDeltaTime\n\'\'\'', 'measureDeltaTime.wantAllVarsGlobal = False', '', "performScopeMeasurement.args = 'lane, dataRate'", "performScopeMeasurement.code = r'''if lane == 1 :\n    currentDelayPos = 0\n    currentDelayNeg = measureDeltaTime(2)\n\n    delayList = [currentDelayPos, currentDelayNeg]\n\nelif lane == 5:\n    currentDelayPos = measureDeltaTime(2)\n    currentDelayNeg = measureDeltaTime(3)\n\n    delayList = [currentDelayPos, currentDelayNeg]\n\nelse:\n    currentDelayPos = measureDeltaTime(2)\n    currentDelayNeg = measureDeltaTime(3)\n\n    delayList = [currentDelayPos, currentDelayNeg]\n\nreturn delayList\n'''", 'performScopeMeasurement.wantAllVarsGlobal = False', '', "performValidationOnCollectedData.args = 'fineDelayDict'", 'performValidationOnCollectedData.code = r\'\'\'print("Checking measured data...")\nfor rate in validationOptions.calRates :\n    for lane in validationOptions.calLanes :\n        for wire in range(2) :\n            measuredError = abs( fineDelayDict[lane][rate][wire])\n            if measuredError > validationOptions.deltaTimeThreshold :\n                print("Found a failing condition on Lane %d..." % lane)\n                print("Measured error is %g s..." % measuredError)\n                return False\n\nreturn True\n\'\'\'', 'performValidationOnCollectedData.wantAllVarsGlobal = False', '', "validationOptions.addField('serialNumber', descrip='''Serial number for device under test''', attrType=str, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal='1234', displayOrder=(0, 1))", "validationOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal='TCPIP0::10.20.20.200::inst0::INSTR', displayOrder=(0, 2))", "validationOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds''', attrType=float, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal=1000.0, displayOrder=(0, 3))", "validationOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after the scope auto scale funtion.''', attrType=float, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal=2000.0, displayOrder=(0, 4))", "validationOptions.addField('numAverages', descrip='''Number of times the measurement is queried from the scope.''', attrType=int, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal=100, displayOrder=(0, 5))", "validationOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6))", "validationOptions.addField('calRates', descrip='''Rates at which we will collect alignment data.''', attrType=list, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', attrSubType=float, defaultVal=[80.0, 125.0, 187.5, 6500.0], displayOrder=(0, 7))", "validationOptions.addField('deltaTimeThreshold', descrip='''Threshold for alignment convergence''', attrType=float, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal=1e-11, displayOrder=(0, 8))", "validationOptions.addField('scopeConnectionTimeout', descrip='''Scope connection timeout.''', attrType=float, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal=10000.0, displayOrder=(0, 9))", "validationOptions.addField('minVersion', descrip='''Minimum Introspect ESP software version that is supported by this script.''', attrType=str, iespInstanceName='SV3C_4L6G_MIPI_DPHY_GENERATOR', defaultVal='3.5.55', displayOrder=(0, 10))", "validationOptions.addMethod('_customInit',\n'',\nr'''# The method '_customInit' is a special case.\n# It is automatically called immediately after a new DataRecord instance is created.\n# You can put code here to do custom initialization.\npass\n''',\nFalse)", "validationOptions.serialNumber = '1234'", "validationOptions.scopeIPAddress = 'TCPIP0::10.20.20.200::inst0::INSTR'", 'validationOptions.scopeMeasurementDelay = 1000.0', 'validationOptions.scopeAutoScaleDelay = 2000.0', 'validationOptions.numAverages = 100', 'validationOptions.calLanes = [1, 2, 3, 4]', 'validationOptions.calRates = [80.0, 125.0, 187.5, 6500.0]', 'validationOptions.deltaTimeThreshold = 1e-11', 'validationOptions.scopeConnectionTimeout = 10000.0', "validationOptions.minVersion = '3.5.55'", 'validationOptions.callCustomInitMethod()', "writeRawData.args = 'delayDict'", 'writeRawData.code = r\'\'\'import time\nimport os\n## dd/mm/yyyy format\ndateToday = time.strftime("%d/%m/%Y")\ntimeNow = time.strftime("%H:%M:%S")\n\nresultFolderCreator1.folderName = validationOptions.serialNumber\nfolderPath = resultFolderCreator1.run()\n\nstringAppendix = ".csv"\nfilePathString = validationOptions.serialNumber + "_DptxAlignmentValidationData" + stringAppendix\nfilePath = os.path.join(folderPath, filePathString)\nwith open(filePath, "w") as outFile:\n    print("DPTX Alignment Validation Data", file=outFile)\n    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)\n    print("Date, %s" % dateToday, file=outFile)\n    print("Time, %s" % timeNow, file=outFile)\n    print(" ,", file=outFile)\n    print("Lane, Data Rate, Skew Pos, Skew Neg", file=outFile)\n    for lane in validationOptions.calLanes :\n        for dataRate in validationOptions.calRates :\n            print("%d, %f, %g, %g, " % (lane, dataRate, delayDict[lane][dataRate][0], delayDict[lane][dataRate][1]), file=outFile)\n\'\'\'', 'writeRawData.wantAllVarsGlobal = False', '', '', 'dphyColorBarPattern1.blankingDuration = 3000.0', 'dphyColorBarPattern1.cseParams = None', 'dphyColorBarPattern1.csiCompressionParams = None', 'dphyColorBarPattern1.enableCsiEpd = False', "dphyColorBarPattern1.epdOption = 'option1'", 'dphyColorBarPattern1.errorInsertion = None', 'dphyColorBarPattern1.frameBlankingDuration = 30000.0', "dphyColorBarPattern1.frameBlankingMode = 'frameRate'", 'dphyColorBarPattern1.frameRate = 4.0', 'dphyColorBarPattern1.gaussianBlurRadius = 0', 'dphyColorBarPattern1.horizLineTime = 65800.0', "dphyColorBarPattern1.imageFormat = 'CSI_RGB888'", 'dphyColorBarPattern1.imageHeight = 480', 'dphyColorBarPattern1.imageWidth = 640', "dphyColorBarPattern1.lineNumbering = 'disabled'", "dphyColorBarPattern1.lineTimeMode = 'lineTimeTotal'", 'dphyColorBarPattern1.numCols = 8', 'dphyColorBarPattern1.numLongPacketEpdSpacers = 0', 'dphyColorBarPattern1.numRows = 2', 'dphyColorBarPattern1.numShortPacketEpdSpacers = 0', 'dphyColorBarPattern1.numVideoFrames = None', 'dphyColorBarPattern1.preBuiltColorBar = ColorBar_ctsHsTestPattern', "dphyColorBarPattern1.rawFormatBayerCell = 'BGGR'", 'dphyColorBarPattern1.rawValues = None', 'dphyColorBarPattern1.regionsOfInterest = []', 'dphyColorBarPattern1.rgbValues = None', 'dphyColorBarPattern1.sendRoiInfo = False', "dphyColorBarPattern1.timeUnits = 'nanosecond'", 'dphyColorBarPattern1.usePreBuiltColorBar = True', 'dphyColorBarPattern1.useRoi = False', 'dphyColorBarPattern1.useVideoFps = False', "dphyColorBarPattern1.valuesMode = 'rgb'", "dphyColorBarPattern1.videoFile = ''", 'dphyColorBarPattern1.virtualChannel = 0', 'dphyColorBarPattern1.wantFrameNumbering = False', '', "dphyParameters1.clockTrailBits = ''", "dphyParameters1.clockZeroBits = '0000'", "dphyParameters1.hsTrailBits = ''", "dphyParameters1.hsZeroBits = '0000'", "dphyParameters1.sotBits = '00011101'", 'dphyParameters1.tAlpClk01Duration = (0.0, 20.0)', 'dphyParameters1.tAlpClk10Duration = (0.0, 40.0)', 'dphyParameters1.tAlpHs01Duration = (0.0, 20.0)', 'dphyParameters1.tAlpHs10Duration = (0.0, 40.0)', 'dphyParameters1.tAlpxDuration = 120.0', 'dphyParameters1.tClockLpx01Duration = (0.0, 80.0)', 'dphyParameters1.tClockPostDuration = (60.0, 60.0)', 'dphyParameters1.tClockPreDuration = (32.0, 0.0)', 'dphyParameters1.tClockPrepareDuration = (0.0, 80.0)', 'dphyParameters1.tClockTrailDuration = (0.0, 80.0)', 'dphyParameters1.tClockZeroDuration = (0.0, 300.0)', 'dphyParameters1.tHsExitDuration = 240.0', 'dphyParameters1.tHsIdleClkHs0Duration = (0.0, 60.0)', 'dphyParameters1.tHsIdlePostDuration = 8', 'dphyParameters1.tHsIdlePreDuration = 8', 'dphyParameters1.tHsLpx01Duration = (0.0, 80.0)', 'dphyParameters1.tHsPrepareDuration = (5.0, 60.0)', 'dphyParameters1.tHsTrailDuration = (8.0, 60.0)', 'dphyParameters1.tHsZeroDuration = (10.0, 145.0)', 'dphyParameters1.tPreamble = 32', 'dphyParameters1.tTaGetDuration = 5', 'dphyParameters1.tTaGoDuration = 4.0', 'dphyParameters1.tTaSureDuration = 1.5', 'dphyParameters1.tlpxDuration = 80.0', 'dphyParameters1.useAlp = False', 'dphyParameters1.usePreambleSequence = False', '', 'mipiClockConfig1.autoDetectTimeout = 2.0', 'mipiClockConfig1.dataRate = 800.0', 'mipiClockConfig1.referenceClocks = refClocksConfig', 'mipiClockConfig1.sscEnabled = False', 'mipiClockConfig1.sscFrequency = 31.5', 'mipiClockConfig1.sscSpread = 2.0', '', 'mipiDphyGenerator1.clockConfig = mipiClockConfig1', 'mipiDphyGenerator1.clockSkew = 0.0', 'mipiDphyGenerator1.continuousClock = False', 'mipiDphyGenerator1.dataLanes = [1, 2, 3, 4]', 'mipiDphyGenerator1.dataSkews = [0.0]', 'mipiDphyGenerator1.hsClockCommonVoltage = 200.0', 'mipiDphyGenerator1.hsClockPostTap = 0', 'mipiDphyGenerator1.hsClockPreTap = 0', 'mipiDphyGenerator1.hsClockVoltageAmplitude = 200.0', 'mipiDphyGenerator1.hsDataCommonVoltages = [200.0]', 'mipiDphyGenerator1.hsDataPostTaps = [0]', 'mipiDphyGenerator1.hsDataPreTaps = [0]', 'mipiDphyGenerator1.hsDataVoltageAmplitudes = [200.0]', 'mipiDphyGenerator1.jitterInjection = None', 'mipiDphyGenerator1.lpClockHighVoltage = 1200.0', 'mipiDphyGenerator1.lpClockLowVoltage = 0.0', 'mipiDphyGenerator1.lpDataHighVoltages = [1200.0]', 'mipiDphyGenerator1.lpDataLowVoltages = [0.0]', 'mipiDphyGenerator1.params = dphyParameters1', 'mipiDphyGenerator1.pattern = dphyColorBarPattern1', 'mipiDphyGenerator1.resetPatternMemory = True', 'mipiDphyGenerator1.splitDataAcrossLanes = True', '', 'mipiProtocol.csiScramble = False', "mipiProtocol.csiVersion = 'Csi2_v1_3'", "mipiProtocol.protocol = 'CSI'", 'mipiProtocol.useEotp = False', '', 'refClocksConfig.externRefClockFreq = 250.0', "refClocksConfig.outputClockAFormat = 'LVDS'", 'refClocksConfig.outputClockAFreq = 100.0', "refClocksConfig.outputClockBFormat = 'LVDS'", 'refClocksConfig.outputClockBFreq = 100.0', "refClocksConfig.systemRefClockSource = 'internal'", '', "resultFolderCreator1.folderName = ''", "resultFolderCreator1.resultType = 'CsvData'", '', "testAsComponent1.componentClassName = 'dptxAlignmentValUsingKeysight'", 'testAsComponent1.dataRecord = validationOptions', "testAsComponent1.description = 'Regression script for validating timing alignment on the SV3C D-PHY Generator'", 'testAsComponent1.excludeGlobalClockConfig = True', 'testAsComponent1.excludedComponents = []', "testAsComponent1.mainMethodName = 'run'", "testAsComponent1.resultType = 'CsvData'", "testAsComponent1.returnValue = r'''\n\n'''", 'testAsComponent1.showMessages = True', 'testAsComponent1.usesIespHardware = True', 'testAsComponent1.viewSubComponents = []', '', '', 'autoscaleScope._showInList = False', 'initScope._showInList = False', 'measureDeltaTime._showInList = False', 'performScopeMeasurement._showInList = False', 'performValidationOnCollectedData._showInList = False', 'writeRawData._showInList = False', '', 'dphyColorBarPattern1._showInList = False', 'dphyParameters1._showInList = False', 'mipiDphyGenerator1._showInList = False', 'resultFolderCreator1._showInList = False', 'testAsComponent1._showInList = False', '#! TEST PROCEDURE', '# Check Version', 'svtVersion = getSvtVersion()', '#if svtVersion < validationOptions.minVersion:', ' #   errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))', '', 'iesp = getIespInstance()', 'maxDataRate = iesp.getLimitMaximum("dataRate")', '', 'if maxDataRate != 6500:', '    validationOptions.calRates = [80.0, 125.0, 187.5]', '', '', '# Connect to scope', 'osci = initScope(validationOptions.scopeIPAddress)', '', '# Initialize generator', 'fileName = "GeneratedDphyPattern_compiled.csv"', 'mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)', 'mipiDphyGenerator1.dataLanes = validationOptions.calLanes', 'mipiDphyGenerator1.setup()', '', '# Define results dictionary', 'measuredCoarseDelayDict = dict()', 'measuredFineDelayDict = dict()', '', '# Start main loop', 'for lane in validationOptions.calLanes:', '    dftUtil.beep(554,250)', '    dftUtil.beep(554,320)', '    print("Measuring D-PHY Lane %d..." % lane)', '    if lane == 1 :', "        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch1, Wire Neg to Ch2' % lane", '    elif lane == 5:', "        myString = 'Please connect clock signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1'", '    else:', "        myString = 'Please connect Lane %d signals to the oscilloscope. Wire Pos to Ch2, Wire Neg to Ch3. IMPORTANT: Keep Lane 1Pos connected to Ch1' % lane", '    waitForGuiOkDialog(myString)', '', '    measuredFineDelayDict[lane] = dict()', '    autoScale = True', '', '    for dataRate in validationOptions.calRates :', '        print("Measuring at %f Mbps..." % dataRate)', '        measuredFineDelayDict[lane][dataRate] = list()', '', '        iesp.writeSubPartRegister(0x0930, 0x00, 0x00) # clear cal mode', '        fileName = "GeneratedDphyPattern_compiled.csv"', '        mipiDphyGenerator1.patternsFilePath = getParamsFilePath(fileName)', '        mipiClockConfig1.dataRate = dataRate', '        mipiDphyGenerator1.setup()', '        iesp.writeSubPartRegister(0x0C80, 0x00, 0x01) # enable alignment pattern', '', '        # Prepare scope for measurement', '        autoscaleScope()', '', '        # Use scope to measure values', '        delayList = performScopeMeasurement(lane,dataRate)', '', '        # Assmeble into dictionaries', '        measuredFineDelayDict[lane][dataRate] = delayList', '', '# Write all collected data points to file', 'writeRawData(measuredFineDelayDict)', '', '# Disable alignment pattern', 'iesp.writeSubPartRegister(0x0C80, 0x00, 0x00) # enable alignment pattern', 'mipiDphyGenerator1.setup()', '', 'if performValidationOnCollectedData(measuredFineDelayDict) :', '    writeNoteForTestRun("Pass")', '    failFlag = 0', 'else :', '    writeNoteForTestRun("Fail")', '    failFlag = 1', '', 'if failFlag == 0 :', '    writeNoteForTestRun("PASS")', '    filePath = getParamsFilePath("Pass.png")', '', '    myFileUrl = str(filePath)', '', "    popupDialog(title='Test Passed!', msg='Test Passed > Place Product in Pass Bin', buttonLabels=['PLEASE PLACE PRODUCT IN THE PASS BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)", 'elif failFlag:', '    writeNoteForTestRun("FAIL, please check report")', '    filePath = getParamsFilePath("Fail.png")', '', '    myFileUrl = str(filePath)', '', "    popupDialog(title='Test Failed!', msg='Test Failed > Place Product in Fail Bin', buttonLabels=['PLACE PRODUCT IN THE FAIL BIN'], responseByButton=None, imagePath=myFileUrl, imageWidth=772, imageHeight=746, timeoutSecs=None, warnIfTimedOut=False)"]
#-------------------------------------------
#-------------------------------------------
