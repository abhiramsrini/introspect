
# Generated via SvtTestAsComponent from Test 'cptxCalUsingKeysightScope_Validation'
# 2022-04-29_1051

import os

import dftm.util as dftUtil
from dftm.svt import *
from dftm.svtComponent import SvtAttr
from dftm.componentStore import DynamicFactory
from dftm.components.basic.testAsComponent import SvtLocalTest
# Import NumPy/SciPy names since these might be used in user code:
import dftm.svtPylab as dftPylab
dftPylab.importAllNames(globals())

#-------------------------------------------
@DynamicFactory.iesp(None)
def factory(B):
    
    # Component creation function
    def _create(componentName, componentClassName, _iespName=None):
        cls = B.get(componentClassName)
        instance = cls()
        instance.name = componentName,
        return instance
    
    class cptxVoltageValUsingKeysight(B.SvtRunnableWithResultIespComponent):
        '''
        Regression script for validating voltage calibration on the SV3C C-PHY Generator
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
        
        serialNumber = SvtAttr('serialNumber', displayOrder = (0, 1.0),
                defaultVal = '1234',
                descrip = '''Serial number of device under test''',
                attrType = str,
                )
        
        scopeIPAddress = SvtAttr('scopeIPAddress', displayOrder = (0, 2.0),
                defaultVal = 'TCPIP0::10.30.30.00::inst0::INSTR',
                descrip = '''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''',
                attrType = str,
                )
        
        scopeMeasurementDelay = SvtAttr('scopeMeasurementDelay', displayOrder = (0, 3.0),
                defaultVal = 3000.0,
                descrip = '''Amount of average accumulation time in milliseconds.''',
                attrType = float,
                )
        
        scopeAutoScaleDelay = SvtAttr('scopeAutoScaleDelay', displayOrder = (0, 4.0),
                defaultVal = 2000.0,
                descrip = '''Amount of time after a scope auto-scale function''',
                attrType = float,
                )
        
        calDataRate = SvtAttr('calDataRate', displayOrder = (0, 5.0),
                defaultVal = 500.0,
                descrip = '''Base data rate for performing voltage measurements''',
                attrType = float,
                )
        
        calLanes = SvtAttr('calLanes', displayOrder = (0, 6.0),
                defaultVal = [1, 2, 3, 4],
                descrip = '''Range of lanes to measure''',
                attrType = list,
                attrSubType = int,
                )
        
        commonModeValues = SvtAttr('commonModeValues', displayOrder = (0, 7.0),
                defaultVal = [130.0, 390.0],
                descrip = '''Range of common-mode voltages to be verified''',
                attrType = list,
                attrSubType = float,
                )
        
        amplitudeValues = SvtAttr('amplitudeValues', displayOrder = (0, 8.0),
                defaultVal = [40.0, 270.0, 290.0],
                descrip = '''Range of differential voltages to be verified''',
                attrType = list,
                attrSubType = float,
                )
        
        connectedToTerminationBoard = SvtAttr('connectedToTerminationBoard', displayOrder = (0, 9.0),
                defaultVal = False,
                descrip = '''Set to true if the measurement is performed using a termination board with high-impedance probes. If the measurement is done directly on the oscilloscope 50 Ohm inputs, set to False. If set to False, a compensation value for common mode measurements is applied''',
                attrType = bool,
                )
        
        absoluteErrorThreshold = SvtAttr('absoluteErrorThreshold', displayOrder = (0, 10.0),
                defaultVal = 25.0,
                descrip = '''Pass/fail threshold for the absolute value of voltage error''',
                attrType = float,
                )
        
        percentErrorThreshold = SvtAttr('percentErrorThreshold', displayOrder = (0, 11.0),
                defaultVal = 10.0,
                descrip = '''Pass/fail threshold for the percentage of voltage error''',
                attrType = float,
                )
        
        scopeConnectionTimeout = SvtAttr('scopeConnectionTimeout', displayOrder = (0, 12.0),
                defaultVal = 10000.0,
                descrip = '''Scope connection timeout.''',
                attrType = float,
                )
        
        minVersion = SvtAttr('minVersion', displayOrder = (0, 13.0),
                defaultVal = '22.2.1',
                descrip = '''Minimum Introspect ESP software version that is supported by this script.''',
                attrType = str,
                )
        
        #-------------------------------------------
        
        def _creat(self):
            logger.debug('%s: Creation of internal components' % self.name)
            
            # Builtin Components:
            CPHY_hsOnly333 = B.SvtComponent.builtins['CPHY_hsOnly333']
            
            # SVT Test
            # SVT version 22.2.1
            # Test saved 2022-04-29_1051
            # Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
            # PY3
            # Checksum: 438521e0214e37459be7291d7175f219
            # Note: This file is the 'Save' file for the Test.
            #       It should not be used as a standalone Python script.
            #       But it can be used via 'runSvtTest.py'.
            
            cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
            mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
            mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
            refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')
            resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')
            
            cphyParams1.calPreambleNumUI = 21
            cphyParams1.calibrationPreambleFormat = 'format_1'
            cphyParams1.lp000Duration = 65.0
            cphyParams1.lp001Duration = 100.0
            cphyParams1.opticalLink = 'disabled'
            cphyParams1.post2NumUI = 112
            cphyParams1.postNumUI = 112
            cphyParams1.postSymbols = '4444444'
            cphyParams1.preBeginNumUI = 196
            cphyParams1.preBeginSymbols = '3333333'
            cphyParams1.preEndSymbols = '3333333'
            cphyParams1.progSeqSymbols = '33333333333333'
            cphyParams1.syncWord = '3444443'
            cphyParams1.t3AlpPauseMin = 50
            cphyParams1.t3AlpPauseWake = 50
            cphyParams1.tHsExitDuration = 300.0
            cphyParams1.tTaGetDuration = 5
            cphyParams1.tTaGoDuration = 4.0
            cphyParams1.tTaSureDuration = 1.5
            cphyParams1.tlpxDuration = 50.0
            cphyParams1.useAlp = False
            
            mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
            mipiCphyGenerator1.hsPostTaps = [0]
            mipiCphyGenerator1.hsPreTaps = [0]
            mipiCphyGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
            mipiCphyGenerator1.jitterInjection = None
            mipiCphyGenerator1.lanes = [1, 2, 3, 4]
            mipiCphyGenerator1.lpHighVoltages = [1200.0]
            mipiCphyGenerator1.lpLowVoltages = [0.0]
            mipiCphyGenerator1.params = cphyParams1
            mipiCphyGenerator1.pattern = CPHY_hsOnly333
            mipiCphyGenerator1.resetPatternMemory = True
            mipiCphyGenerator1.splitDataAcrossLanes = True
            mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]
            
            mipiProtocol.csiScramble = False
            mipiProtocol.csiVersion = 'Csi2_v1_3'
            mipiProtocol.protocol = 'CSI'
            
            resultFolderCreator1.folderName = ''
            resultFolderCreator1.resultType = 'CsvData'
            
            refClocksConfig.outputClockAFormat = 'LVDS'
            refClocksConfig.outputClockAFreq = 100.0
            refClocksConfig.outputClockBFormat = 'LVDS'
            refClocksConfig.outputClockBFreq = 100.0
            refClocksConfig.systemRefClockSource = 'internal'
            
            cphyParams1._showInList = False
            mipiCphyGenerator1._showInList = False
            resultFolderCreator1._showInList = False
            # Alias for DataRecord that defines properties of this component:
            validationOptions = self
            
            # ensure that 'IESP' is available in case user refers to it
            from dftm.iespCore import IESP
            
            def initScope(scopeIpAddress):
                osci = self._getSymbol('osci')
                import visa
                #connect to scope
                rm = visa.ResourceManager()
                osci = rm.get_instrument(scopeIpAddress)
                osci.lock_excl()
                
                osci.read_termination = '\n'
                osci.write_termination = '\n'
                osci.timeout = validationOptions.scopeConnectionTimeout
                
                # Set to center by going to default
                osci.write(":SYSTem:PRESet DEFault")
                sleepMillis(validationOptions.scopeAutoScaleDelay)
                
                # Make sure all skew are at 0. This is not reset by default
                osci.write(":CALibrate:SKEW CHANnel1,0")
                osci.write(":CALibrate:SKEW CHANnel2,0")
                osci.write(":CALibrate:SKEW CHANnel3,0")
                osci.write(":CALibrate:SKEW CHANnel4,0")
                
                # Display/Enable the channels
                osci.write(":CHANnel1:DISPlay 1")
                osci.write(":CHANnel2:DISPlay 1")
                osci.write(":CHANnel3:DISPlay 1")
                
                return osci
            
            def performScopeMeasurement():
                osci = self._getSymbol('osci')
                myString = self._getSymbol('myString')
                # Set timebase to proper value
                osci.write(":TIMebase:SCALe 5e-08")
                
                # Autoscale the channels
                osci.write(":AUToscale:VERTical CHANnel1")
                osci.write(":AUToscale:VERTical CHANnel2")
                osci.write(":AUToscale:VERTical CHANnel3")
                
                # Clear display
                osci.write(":CDISplay")
                
                # Measure average voltage of channel 1 to set trigger level
                osci.write(":MEASure:VAVerage DISPlay,CHANnel1")
                
                sleepMillis(validationOptions.scopeAutoScaleDelay)
                varAverage = osci.query_ascii_values(":MEASure:VAVerage? DISPlay,CHANnel1")
                currentValue = varAverage[0]
                
                osci.write(":MEASure:VAMPlitude CHANNEL1")
                sleepMillis(validationOptions.scopeMeasurementDelay)
                varAmp = osci.query_ascii_values(":MEASure:VAMPlitude? CHANNEL1")
                currentAmp = varAmp[0]
                
                triggerValue = currentValue - 0.25*currentAmp
                
                # Set trigger level to be just below the mid-point of the 3-level waveform
                myString = ":TRIGger:LEVel CHANNEL1, %f" % triggerValue
                osci.write(myString)
                
                # Clear display
                osci.write(":CDISplay")
                sleepMillis(100)
                
                ## Now perform measurements on all channels
                commonModeReturnList = list()
                amplitudeReturnList = list()
                for channel in [1,2,3] :
                    channelString = "CHANNEL%d" % channel
                    commonModeMeasurementString = ":MEASure:VAVerage DISPlay,"+channelString
                    osci.write(commonModeMeasurementString)
                    sleepMillis(validationOptions.scopeMeasurementDelay)
                    commonModeMeasurementString = ":MEASure:VAVerage? DISPlay,"+channelString
                    varAverage = osci.query_ascii_values(commonModeMeasurementString)
                    if validationOptions.connectedToTerminationBoard :
                        commonModeReturnList.append(varAverage[0]*1000) #convert to mV
                    else:
                        commonModeReturnList.append(varAverage[0]*1000/0.5) #convert to mV and apply scope attenuation factor
                
                    amplitudeMeasurementString = ":MEASure:VAMPlitude "+channelString
                    osci.write(amplitudeMeasurementString)
                    sleepMillis(validationOptions.scopeMeasurementDelay)
                    amplitudeMeasurementString = ":MEASure:VAMPlitude? "+channelString
                    varAmp = osci.query_ascii_values(amplitudeMeasurementString)
                    amplitudeReturnList.append(varAmp[0]*1000) #convert to mV
                
                return(commonModeReturnList, amplitudeReturnList)
            
            def performValidationOnCollectedData(commonData, ampData):
                fail = 0
                print("Checking measured data...")
                for lane in validationOptions.calLanes :
                        for cm in validationOptions.commonModeValues :
                            for amp in validationOptions.amplitudeValues :
                                for wire in range(3) :
                                    commonErrorValue = abs( commonData[lane][cm][amp][wire] - cm )
                                    commonErrorPercent = commonErrorValue / cm * 100
                                    ampErrorValue = abs( ampData[lane][cm][amp][wire] - amp )
                                    ampErrorPercent = ampErrorValue / amp * 100
                                    if not ( commonErrorValue < validationOptions.absoluteErrorThreshold or commonErrorPercent < validationOptions.percentErrorThreshold ):
                                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                                        print("Target common mode is %f mV" % cm)
                                        print("Measured common mode is %f mV" % commonData[lane][cm][amp][wire])
                                        print("Absolute Error is %f mV" % commonErrorValue)
                                        print("Percent Error is %f percent" % commonErrorPercent)
                                        fail = 1
                                        #return False
                                    if not ( ampErrorValue < validationOptions.absoluteErrorThreshold or ampErrorPercent < validationOptions.percentErrorThreshold ) :
                                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))
                                        print("Target amplitude is %f mV" % amp)
                                        print("Measured amplitude is %f mV" % ampData[lane][cm][amp][wire])
                                        print("Absolute Error is %f mV" % ampErrorValue)
                                        print("Percent Error is %f percent" % ampErrorPercent)
                                        #return False
                                        fail = 1
                if fail == 1:
                    return False
                else:
                    return True
            
            def writeRawData(commonData, ampData):
                import time
                import os
                ## dd/mm/yyyy format
                dateToday = time.strftime("%d/%m/%Y")
                timeNow = time.strftime("%H:%M:%S")
                
                resultFolderCreator1.folderName = validationOptions.serialNumber
                folderPath = resultFolderCreator1.run()
                
                stringAppendix = ".csv"
                filePathString = validationOptions.serialNumber + "_CptxVoltageCalData" + stringAppendix
                filePath = os.path.join(folderPath, filePathString)
                with open(filePath, "w") as outFile:
                    print("CPTX Voltage Validation Data", file=outFile)
                    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)
                    print("Date, %s" % dateToday, file=outFile)
                    print("Time, %s" % timeNow, file=outFile)
                    print(" ,", file=outFile)
                    print("Lane, WireA Programmed CM, WireA Programmed Amp, WireA Measured CM, WireA Measured Amp, WireB Programmed CM, WireB Programmed Amp, WireB Measured CM, WireB Measured Amp, WireC Programmed CM, WireC Programmed Amp, WireC Measured CM, WireC Measured Amp,", file=outFile)
                    for lane in validationOptions.calLanes :
                        for cm in validationOptions.commonModeValues :
                            for amp in validationOptions.amplitudeValues :
                                print("%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f," % (lane, cm, amp, commonData[lane][cm][amp][0], ampData[lane][cm][amp][0], cm, amp, commonData[lane][cm][amp][1], ampData[lane][cm][amp][1], cm, amp, commonData[lane][cm][amp][2], ampData[lane][cm][amp][2]), file=outFile)
            
            # Create LocalTest and register internal components:
            folderOfThisScript = os.path.dirname(os.path.realpath(__file__))
            self._localTest = SvtLocalTest(folderOfThisScript, locals())
            self._localTest.registerComponent('CPHY_hsOnly333', CPHY_hsOnly333)
            self._localTest.registerComponent('cphyParams1', cphyParams1)
            self._localTest.registerComponent('mipiCphyGenerator1', mipiCphyGenerator1)
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
            CPHY_hsOnly333 = self._getComponent('CPHY_hsOnly333')
            cphyParams1 = self._getComponent('cphyParams1')
            mipiCphyGenerator1 = self._getComponent('mipiCphyGenerator1')
            refClocksConfig = self._getComponent('refClocksConfig')
            resultFolderCreator1 = self._getComponent('resultFolderCreator1')
            # Functions referred to below:
            initScope = self._getSymbol('initScope')
            performScopeMeasurement = self._getSymbol('performScopeMeasurement')
            performValidationOnCollectedData = self._getSymbol('performValidationOnCollectedData')
            writeRawData = self._getSymbol('writeRawData')
            
            # Tell internal components the testRunResult:
            extraInfo = dict()
            extraInfo['viewSubComponents'] = ''
            runResultFolderPath = self.createRunResultFolder(resultType = 'CsvData', extraInfo=extraInfo)
            if runResultFolderPath is None:
                return
            self._localTest.tellComponentsToUseRunResultFolder(runResultFolderPath)
            CPHY_hsOnly333.initForTestRun()
            cphyParams1.initForTestRun()
            mipiCphyGenerator1.initForTestRun()
            refClocksConfig.initForTestRun()
            resultFolderCreator1.initForTestRun()
            
            #! TEST PROCEDURE
            # Check Version
            svtVersion = getSvtVersion()
            self._saveSymbol('svtVersion', svtVersion)
            if svtVersion < validationOptions.minVersion:
                errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))
            
            # Connect to scope
            osci = initScope(validationOptions.scopeIPAddress)
            self._saveSymbol('osci', osci)
            
            # Initialize generator
            mipiCphyGenerator1.lanes = validationOptions.calLanes
            mipiCphyGenerator1.setup()
            
            #disable cal mode
            iesp = getIespInstance()
            self._saveSymbol('iesp', iesp)
            iesp.writeSubPartRegister(0x0930, 0x00, 0x00)   # clear calibration mode
            
            # Define results dictionary
            measuredCommonModeDict = dict()
            self._saveSymbol('measuredCommonModeDict', measuredCommonModeDict)
            measuredAmplitudeDict = dict()
            self._saveSymbol('measuredAmplitudeDict', measuredAmplitudeDict)
            
            for lane in mipiCphyGenerator1.lanes :
                dftUtil.beep(554,250)
                dftUtil.beep(554,320)
                print("Measuring C-PHY Lane %d..." % lane)
                myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane
                self._saveSymbol('myString', myString)
                waitForGuiOkDialog(myString)
                measuredCommonModeDict[lane] = dict()
                measuredAmplitudeDict[lane] = dict()
            
                for programmedCommonMode in validationOptions.commonModeValues :
                    print("Measuring at %f mV common-mode..." % programmedCommonMode)
                    measuredCommonModeDict[lane][programmedCommonMode] = dict()
                    measuredAmplitudeDict[lane][programmedCommonMode] = dict()
            
                    for programmedAmplitude in validationOptions.amplitudeValues :
                        print("Measuring at %f mV amplitude..." % programmedAmplitude)
                        measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude] = list()
                        measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude] = list()
            
                        # Update the generator
                        mipiCphyGenerator1.hsCommonVoltagesABC = [(programmedCommonMode, programmedCommonMode, programmedCommonMode)]
                        mipiCphyGenerator1.hsVoltageAmplitudesABC = [(programmedAmplitude, programmedAmplitude, programmedAmplitude)]
                        mipiCphyGenerator1.update()
            
                        # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane
                        (measuredCommonMode, measuredAmplitude) = performScopeMeasurement()
            
                        # Accumulate the list into the dictionaries
                        for wire in range(0,3,1) :
                            # Add correstion fator of 10% because of scope terminaison
                            measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredCommonMode[wire]*1.1 )
                            measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredAmplitude[wire] )
            
                        # Display information messages
                        wires = ['A', 'B', 'C']
                        self._saveSymbol('wires', wires)
                        for wire in range(0,3,1) :
                            print("Wire %s: Programmed % f mV common-mode, and measured %f mV..." % (wires[wire],programmedCommonMode, measuredCommonMode[wire]))
                            print("Wire %s: Programmed %f mV amplitude, and measured %f mV..." % (wires[wire], programmedAmplitude, measuredAmplitude[wire]))
            
            # Dump the raw measurement values into a csv file
            writeRawData(measuredCommonModeDict, measuredAmplitudeDict)
            
            if performValidationOnCollectedData(measuredCommonModeDict, measuredAmplitudeDict) :
                writeNoteForTestRun("Pass")
            else :
                writeNoteForTestRun("Fail")
            self._removeSavedSymbols()
        
        def run(self):
            retVal = self._run()
            return retVal
        
        def getReturnValueStr(self):
            return 'retVal'
        
        #-------------------------------------------
        #-------------------------------------------
        
    return cptxVoltageValUsingKeysight
#TEST_PROCEDURE_FILE_CONTENT = ['# SVT Test', '# SVT version 22.2.1', '# Test saved 2022-04-29_1051', '# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR', '# PY3', '# Checksum: 438521e0214e37459be7291d7175f219', "# Note: This file is the 'Save' file for the Test.", '#       It should not be used as a standalone Python script.', "#       But it can be used via 'runSvtTest.py'.", '', '', "initScope = _create('initScope', 'SvtFunction', iespName='None')", "performScopeMeasurement = _create('performScopeMeasurement', 'SvtFunction', iespName='None')", "performValidationOnCollectedData = _create('performValidationOnCollectedData', 'SvtFunction', iespName='None')", "validationOptions = _create('validationOptions', 'SvtDataRecord', iespName='None')", "writeRawData = _create('writeRawData', 'SvtFunction', iespName='None')", '', "cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')", "mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')", "mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')", "mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')", "refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')", "resultFolderCreator1 = _create('resultFolderCreator1', 'SvtResultFolderCreator')", "testAsComponent1 = _create('testAsComponent1', 'SvtTestAsComponent')", '', "initScope.args = 'scopeIpAddress'", 'initScope.code = r\'\'\'import visa\n#connect to scope\nrm = visa.ResourceManager()\nosci = rm.get_instrument(scopeIpAddress)\nosci.lock_excl()\n\nosci.read_termination = \'\\n\'\nosci.write_termination = \'\\n\'\nosci.timeout = validationOptions.scopeConnectionTimeout\n\n# Set to center by going to default\nosci.write(":SYSTem:PRESet DEFault")\nsleepMillis(validationOptions.scopeAutoScaleDelay)\n\n# Make sure all skew are at 0. This is not reset by default\nosci.write(":CALibrate:SKEW CHANnel1,0")\nosci.write(":CALibrate:SKEW CHANnel2,0")\nosci.write(":CALibrate:SKEW CHANnel3,0")\nosci.write(":CALibrate:SKEW CHANnel4,0")\n\n# Display/Enable the channels\nosci.write(":CHANnel1:DISPlay 1")\nosci.write(":CHANnel2:DISPlay 1")\nosci.write(":CHANnel3:DISPlay 1")\n\nreturn osci\n\'\'\'', 'initScope.wantAllVarsGlobal = False', '', "performScopeMeasurement.args = ''", 'performScopeMeasurement.code = r\'\'\'# Set timebase to proper value\nosci.write(":TIMebase:SCALe 5e-08")\n\n# Autoscale the channels\nosci.write(":AUToscale:VERTical CHANnel1")\nosci.write(":AUToscale:VERTical CHANnel2")\nosci.write(":AUToscale:VERTical CHANnel3")\n\n# Clear display\nosci.write(":CDISplay")\n\n# Measure average voltage of channel 1 to set trigger level\nosci.write(":MEASure:VAVerage DISPlay,CHANnel1")\n\nsleepMillis(validationOptions.scopeAutoScaleDelay)\nvarAverage = osci.query_ascii_values(":MEASure:VAVerage? DISPlay,CHANnel1")\ncurrentValue = varAverage[0]\n\nosci.write(":MEASure:VAMPlitude CHANNEL1")\nsleepMillis(validationOptions.scopeMeasurementDelay)\nvarAmp = osci.query_ascii_values(":MEASure:VAMPlitude? CHANNEL1")\ncurrentAmp = varAmp[0]\n\ntriggerValue = currentValue - 0.25*currentAmp\n\n# Set trigger level to be just below the mid-point of the 3-level waveform\nmyString = ":TRIGger:LEVel CHANNEL1, %f" % triggerValue\nosci.write(myString)\n\n# Clear display\nosci.write(":CDISplay")\nsleepMillis(100)\n\n## Now perform measurements on all channels\ncommonModeReturnList = list()\namplitudeReturnList = list()\nfor channel in [1,2,3] :\n    channelString = "CHANNEL%d" % channel\n    commonModeMeasurementString = ":MEASure:VAVerage DISPlay,"+channelString\n    osci.write(commonModeMeasurementString)\n    sleepMillis(validationOptions.scopeMeasurementDelay)\n    commonModeMeasurementString = ":MEASure:VAVerage? DISPlay,"+channelString\n    varAverage = osci.query_ascii_values(commonModeMeasurementString)\n    if validationOptions.connectedToTerminationBoard :\n        commonModeReturnList.append(varAverage[0]*1000) #convert to mV\n    else:\n        commonModeReturnList.append(varAverage[0]*1000/0.5) #convert to mV and apply scope attenuation factor\n\n    amplitudeMeasurementString = ":MEASure:VAMPlitude "+channelString\n    osci.write(amplitudeMeasurementString)\n    sleepMillis(validationOptions.scopeMeasurementDelay)\n    amplitudeMeasurementString = ":MEASure:VAMPlitude? "+channelString\n    varAmp = osci.query_ascii_values(amplitudeMeasurementString)\n    amplitudeReturnList.append(varAmp[0]*1000) #convert to mV\n\nreturn(commonModeReturnList, amplitudeReturnList)\n\'\'\'', 'performScopeMeasurement.wantAllVarsGlobal = False', '', "performValidationOnCollectedData.args = 'commonData, ampData'", 'performValidationOnCollectedData.code = r\'\'\'fail = 0\nprint("Checking measured data...")\nfor lane in validationOptions.calLanes :\n        for cm in validationOptions.commonModeValues :\n            for amp in validationOptions.amplitudeValues :\n                for wire in range(3) :\n                    commonErrorValue = abs( commonData[lane][cm][amp][wire] - cm )\n                    commonErrorPercent = commonErrorValue / cm * 100\n                    ampErrorValue = abs( ampData[lane][cm][amp][wire] - amp )\n                    ampErrorPercent = ampErrorValue / amp * 100\n                    if not ( commonErrorValue < validationOptions.absoluteErrorThreshold or commonErrorPercent < validationOptions.percentErrorThreshold ):\n                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))\n                        print("Target common mode is %f mV" % cm)\n                        print("Measured common mode is %f mV" % commonData[lane][cm][amp][wire])\n                        print("Absolute Error is %f mV" % commonErrorValue)\n                        print("Percent Error is %f percent" % commonErrorPercent)\n                        fail = 1\n                        #return False\n                    if not ( ampErrorValue < validationOptions.absoluteErrorThreshold or ampErrorPercent < validationOptions.percentErrorThreshold ) :\n                        print("Found a failing condition on Lane %d wire %d..." % (lane,wire))\n                        print("Target amplitude is %f mV" % amp)\n                        print("Measured amplitude is %f mV" % ampData[lane][cm][amp][wire])\n                        print("Absolute Error is %f mV" % ampErrorValue)\n                        print("Percent Error is %f percent" % ampErrorPercent)\n                        #return False\n                        fail = 1\nif fail == 1:\n    return False\nelse:\n    return True\n\'\'\'', 'performValidationOnCollectedData.wantAllVarsGlobal = False', '', "validationOptions.addField('serialNumber', descrip='''Serial number of device under test''', attrType=str, iespInstanceName='any', defaultVal='1234', displayOrder=(0, 1.0))", "validationOptions.addField('scopeIPAddress', descrip='''Visa string specifying location of the calibration scope. Only Keysight scopes are supported''', attrType=str, iespInstanceName='any', defaultVal='TCPIP0::10.30.30.00::inst0::INSTR', displayOrder=(0, 2.0))", "validationOptions.addField('scopeMeasurementDelay', descrip='''Amount of average accumulation time in milliseconds.''', attrType=float, iespInstanceName='any', defaultVal=3000.0, displayOrder=(0, 3.0))", "validationOptions.addField('scopeAutoScaleDelay', descrip='''Amount of time after a scope auto-scale function''', attrType=float, iespInstanceName='any', defaultVal=2000.0, displayOrder=(0, 4.0))", "validationOptions.addField('calDataRate', descrip='''Base data rate for performing voltage measurements''', attrType=float, iespInstanceName='any', defaultVal=500.0, displayOrder=(0, 5.0))", "validationOptions.addField('calLanes', descrip='''Range of lanes to measure''', attrType=list, iespInstanceName='any', attrSubType=int, defaultVal=[1, 2, 3, 4], displayOrder=(0, 6.0))", "validationOptions.addField('commonModeValues', descrip='''Range of common-mode voltages to be verified''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[130.0, 390.0], displayOrder=(0, 7.0))", "validationOptions.addField('amplitudeValues', descrip='''Range of differential voltages to be verified''', attrType=list, iespInstanceName='any', attrSubType=float, defaultVal=[40.0, 270.0, 290.0], displayOrder=(0, 8.0))", "validationOptions.addField('connectedToTerminationBoard', descrip='''Set to true if the measurement is performed using a termination board with high-impedance probes. If the measurement is done directly on the oscilloscope 50 Ohm inputs, set to False. If set to False, a compensation value for common mode measurements is applied''', attrType=bool, iespInstanceName='any', defaultVal=False, displayOrder=(0, 9.0))", "validationOptions.addField('absoluteErrorThreshold', descrip='''Pass/fail threshold for the absolute value of voltage error''', attrType=float, iespInstanceName='any', defaultVal=25.0, displayOrder=(0, 10.0))", "validationOptions.addField('percentErrorThreshold', descrip='''Pass/fail threshold for the percentage of voltage error''', attrType=float, iespInstanceName='any', defaultVal=10.0, displayOrder=(0, 11.0))", "validationOptions.addField('scopeConnectionTimeout', descrip='''Scope connection timeout.''', attrType=float, iespInstanceName='any', defaultVal=10000.0, displayOrder=(0, 12.0))", "validationOptions.addField('minVersion', descrip='''Minimum Introspect ESP software version that is supported by this script.''', attrType=str, iespInstanceName='any', defaultVal='22.2.1', displayOrder=(0, 13.0))", "validationOptions.addMethod('_customInit',\n\t'',\n\tr'''# The method '_customInit' is a special case.\n# It is automatically called immediately after a new DataRecord instance is created.\n# You can put code here to do custom initialization.\npass\n''',\n\tFalse)", "validationOptions.serialNumber = '1234'", "validationOptions.scopeIPAddress = 'TCPIP0::10.30.30.00::inst0::INSTR'", 'validationOptions.scopeMeasurementDelay = 3000.0', 'validationOptions.scopeAutoScaleDelay = 2000.0', 'validationOptions.calDataRate = 500.0', 'validationOptions.calLanes = [1, 2, 3, 4]', 'validationOptions.commonModeValues = [130.0, 390.0]', 'validationOptions.amplitudeValues = [40.0, 270.0, 290.0]', 'validationOptions.connectedToTerminationBoard = False', 'validationOptions.absoluteErrorThreshold = 25.0', 'validationOptions.percentErrorThreshold = 10.0', 'validationOptions.scopeConnectionTimeout = 10000.0', "validationOptions.minVersion = '22.2.1'", 'validationOptions.callCustomInitMethod()', "writeRawData.args = 'commonData, ampData'", 'writeRawData.code = r\'\'\'import time\nimport os\n## dd/mm/yyyy format\ndateToday = time.strftime("%d/%m/%Y")\ntimeNow = time.strftime("%H:%M:%S")\n\nresultFolderCreator1.folderName = validationOptions.serialNumber\nfolderPath = resultFolderCreator1.run()\n\nstringAppendix = ".csv"\nfilePathString = validationOptions.serialNumber + "_CptxVoltageCalData" + stringAppendix\nfilePath = os.path.join(folderPath, filePathString)\nwith open(filePath, "w") as outFile:\n    print("CPTX Voltage Validation Data", file=outFile)\n    print("Serial Number, %s" % validationOptions.serialNumber, file=outFile)\n    print("Date, %s" % dateToday, file=outFile)\n    print("Time, %s" % timeNow, file=outFile)\n    print(" ,", file=outFile)\n    print("Lane, WireA Programmed CM, WireA Programmed Amp, WireA Measured CM, WireA Measured Amp, WireB Programmed CM, WireB Programmed Amp, WireB Measured CM, WireB Measured Amp, WireC Programmed CM, WireC Programmed Amp, WireC Measured CM, WireC Measured Amp,", file=outFile)\n    for lane in validationOptions.calLanes :\n        for cm in validationOptions.commonModeValues :\n            for amp in validationOptions.amplitudeValues :\n                print("%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f," % (lane, cm, amp, commonData[lane][cm][amp][0], ampData[lane][cm][amp][0], cm, amp, commonData[lane][cm][amp][1], ampData[lane][cm][amp][1], cm, amp, commonData[lane][cm][amp][2], ampData[lane][cm][amp][2]), file=outFile)\n\'\'\'', 'writeRawData.wantAllVarsGlobal = False', '', '', 'cphyParams1.calPreambleNumUI = 21', "cphyParams1.calibrationPreambleFormat = 'format_1'", 'cphyParams1.lp000Duration = 65.0', 'cphyParams1.lp001Duration = 100.0', "cphyParams1.opticalLink = 'disabled'", 'cphyParams1.post2NumUI = 112', 'cphyParams1.postNumUI = 112', "cphyParams1.postSymbols = '4444444'", 'cphyParams1.preBeginNumUI = 196', "cphyParams1.preBeginSymbols = '3333333'", "cphyParams1.preEndSymbols = '3333333'", "cphyParams1.progSeqSymbols = '33333333333333'", "cphyParams1.syncWord = '3444443'", 'cphyParams1.t3AlpPauseMin = 50', 'cphyParams1.t3AlpPauseWake = 50', 'cphyParams1.tHsExitDuration = 300.0', 'cphyParams1.tTaGetDuration = 5', 'cphyParams1.tTaGoDuration = 4.0', 'cphyParams1.tTaSureDuration = 1.5', 'cphyParams1.tlpxDuration = 50.0', 'cphyParams1.useAlp = False', '', 'mipiClockConfig1.dataRate = 500.0', 'mipiClockConfig1.referenceClocks = refClocksConfig', '', 'mipiCphyGenerator1.clockConfig = mipiClockConfig1', 'mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]', 'mipiCphyGenerator1.hsPostTaps = [0]', 'mipiCphyGenerator1.hsPreTaps = [0]', 'mipiCphyGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]', 'mipiCphyGenerator1.jitterInjection = None', 'mipiCphyGenerator1.lanes = [1, 2, 3, 4]', 'mipiCphyGenerator1.lpHighVoltages = [1200.0]', 'mipiCphyGenerator1.lpLowVoltages = [0.0]', 'mipiCphyGenerator1.params = cphyParams1', 'mipiCphyGenerator1.pattern = CPHY_hsOnly333', 'mipiCphyGenerator1.resetPatternMemory = True', 'mipiCphyGenerator1.splitDataAcrossLanes = True', 'mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]', '', 'mipiProtocol.csiScramble = False', "mipiProtocol.csiVersion = 'Csi2_v1_3'", "mipiProtocol.protocol = 'CSI'", '', "resultFolderCreator1.folderName = ''", "resultFolderCreator1.resultType = 'CsvData'", '', "testAsComponent1.componentClassName = 'cptxVoltageValUsingKeysight'", 'testAsComponent1.dataRecord = validationOptions', "testAsComponent1.description = 'Regression script for validating voltage calibration on the SV3C C-PHY Generator'", 'testAsComponent1.excludeGlobalClockConfig = True', 'testAsComponent1.excludedComponents = []', "testAsComponent1.mainMethodName = 'run'", "testAsComponent1.resultType = 'CsvData'", "testAsComponent1.returnValue = r'''\n\n'''", 'testAsComponent1.showMessages = True', 'testAsComponent1.usesIespHardware = True', 'testAsComponent1.viewSubComponents = []', '', "refClocksConfig.outputClockAFormat = 'LVDS'", 'refClocksConfig.outputClockAFreq = 100.0', "refClocksConfig.outputClockBFormat = 'LVDS'", 'refClocksConfig.outputClockBFreq = 100.0', "refClocksConfig.systemRefClockSource = 'internal'", '', '', 'initScope._showInList = False', 'initScope._showInTabs = False', 'performScopeMeasurement._showInList = False', 'performScopeMeasurement._showInTabs = False', 'performValidationOnCollectedData._showInList = False', 'writeRawData._showInList = False', 'writeRawData._showInTabs = False', '', 'cphyParams1._showInList = False', 'mipiCphyGenerator1._showInList = False', 'resultFolderCreator1._showInList = False', 'testAsComponent1._showInList = False', '#! TEST PROCEDURE', '# Check Version', 'svtVersion = getSvtVersion()', 'if svtVersion < validationOptions.minVersion:', '    errorMsg("Your version of Introspect ESP is too old (v %s). Must use installation version %s or later." % (svtVersion, validationOptions.minVersion))', '', '# Connect to scope', 'osci = initScope(validationOptions.scopeIPAddress)', '', '# Initialize generator', 'mipiCphyGenerator1.lanes = validationOptions.calLanes', 'mipiClockConfig1.dataRate = validationOptions.calDataRate', 'mipiCphyGenerator1.setup()', '', '#disable cal mode', 'iesp = getIespInstance()', 'iesp.writeSubPartRegister(0x0930, 0x00, 0x00)   # clear calibration mode', '', '# Define results dictionary', 'measuredCommonModeDict = dict()', 'measuredAmplitudeDict = dict()', '', 'for lane in mipiCphyGenerator1.lanes :', '    dftUtil.beep(554,250)', '    dftUtil.beep(554,320)', '    print("Measuring C-PHY Lane %d..." % lane)', "    myString = 'Please connect Lane %d signals to the oscilloscope. Wire A to Ch1, Wire B, to Ch2, and Wire C to Ch3' % lane", '    waitForGuiOkDialog(myString)', '    measuredCommonModeDict[lane] = dict()', '    measuredAmplitudeDict[lane] = dict()', '', '    for programmedCommonMode in validationOptions.commonModeValues :', '        print("Measuring at %f mV common-mode..." % programmedCommonMode)', '        measuredCommonModeDict[lane][programmedCommonMode] = dict()', '        measuredAmplitudeDict[lane][programmedCommonMode] = dict()', '', '        for programmedAmplitude in validationOptions.amplitudeValues :', '            print("Measuring at %f mV amplitude..." % programmedAmplitude)', '            measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude] = list()', '            measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude] = list()', '', '            # Update the generator', '            mipiCphyGenerator1.hsCommonVoltagesABC = [(programmedCommonMode, programmedCommonMode, programmedCommonMode)]', '            mipiCphyGenerator1.hsVoltageAmplitudesABC = [(programmedAmplitude, programmedAmplitude, programmedAmplitude)]', '            mipiCphyGenerator1.update()', '', '            # Use scope to measure values. Each return variable is a list of 3 values corresponding to the three wires on the lane', '            (measuredCommonMode, measuredAmplitude) = performScopeMeasurement()', '', '', '            # Accumulate the list into the dictionaries', '            for wire in range(0,3,1) :', '                # Add correstion fator of 10% because of scope terminaison', '                measuredCommonModeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredCommonMode[wire]*1.1 )', '                measuredAmplitudeDict[lane][programmedCommonMode][programmedAmplitude].append( measuredAmplitude[wire] )', '', '            # Display information messages', "            wires = ['A', 'B', 'C']", '            for wire in range(0,3,1) :', '                print("Wire %s: Programmed % f mV common-mode, and measured %f mV..." % (wires[wire],programmedCommonMode, measuredCommonMode[wire]))', '                print("Wire %s: Programmed %f mV amplitude, and measured %f mV..." % (wires[wire], programmedAmplitude, measuredAmplitude[wire]))', '', '# Dump the raw measurement values into a csv file', 'writeRawData(measuredCommonModeDict, measuredAmplitudeDict)', '', 'if performValidationOnCollectedData(measuredCommonModeDict, measuredAmplitudeDict) :', '    writeNoteForTestRun("Pass")', 'else :', '    writeNoteForTestRun("Fail")']
#-------------------------------------------
#-------------------------------------------
