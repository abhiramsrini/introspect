# SVT Test
# SVT version 22.2.2
# Test saved 2022-06-14_1112
# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 3ab0930a8cb5b60d9b6bb15ab196d957
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
startCoordinator = _create('startCoordinator', 'SvtFunction', iespName='None')

cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig = _create('refClocksConfig', 'SvtRefClocksConfig')

coordinator1.clientName = 'Generator'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

startCoordinator.args = ''
startCoordinator.code = r'''coordinator1.startLocalServerOnGui()

status = coordinator1.waitForClientState("Analyzer", "running", 20)
if status :
    analyzerIsRunning = 1
else :
    print("Analyzer not ready...")
    analyzerIsRunning = 0

return analyzerIsRunning
'''
startCoordinator.wantAllVarsGlobal = False


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
cphyParams1.tTaSureDuration = 1.0
cphyParams1.tlpxDuration = 100.0
cphyParams1.useAlp = False

mipiClockConfig1.dataRate = 1500.0
mipiClockConfig1.referenceClocks = refClocksConfig

mipiCphyGenerator1.clockConfig = mipiClockConfig1
mipiCphyGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiCphyGenerator1.hsPostTaps = [0]
mipiCphyGenerator1.hsPreTaps = [0]
mipiCphyGenerator1.hsVoltageAmplitudesABC = [(100.0, 100.0, 100.0)]
mipiCphyGenerator1.jitterInjection = None
mipiCphyGenerator1.lanes = [1, 2, 3, 4]
mipiCphyGenerator1.lpHighVoltages = [1200.0]
mipiCphyGenerator1.lpLowVoltages = [0.0]
mipiCphyGenerator1.params = cphyParams1
mipiCphyGenerator1.pattern = CPHY_hsOnlyPrbs9
mipiCphyGenerator1.resetPatternMemory = True
mipiCphyGenerator1.splitDataAcrossLanes = True
mipiCphyGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig.outputClockAFormat = 'LVDS'
refClocksConfig.outputClockAFreq = 100.0
refClocksConfig.outputClockBFormat = 'LVDS'
refClocksConfig.outputClockBFreq = 100.0
refClocksConfig.systemRefClockSource = 'internal'

#! TEST PROCEDURE
analyzerIsRunning = startCoordinator()
mipiCphyGenerator1.setup()

while (analyzerIsRunning) :
    status = coordinator1.runCodeFromClient("Analyzer")
    sleepMillis(500)
    (state,time) = coordinator1.getState("Analyzer")
    if state == 'running' :
        analyzerIsRunning = 1
    else :
        analyzerIsRunning = 0
        print("Analyzer is stopped...")
        break
