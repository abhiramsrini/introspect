# SVT Test
# SVT version 23.3.b11
# Test saved 2023-06-09_1047
# Form factor: SV3C_4L3G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 29c69a6ab249598d5a895f0adec324e3
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
startCoordinator = _create('startCoordinator', 'SvtFunction', iespName='None')

cphyCustomPattern1 = _create('cphyCustomPattern1', 'SvtMipiCphyCustomPattern')
cphyParams1 = _create('cphyParams1', 'SvtMipiCphyParams')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiCphyGenerator1 = _create('mipiCphyGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')

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


cphyCustomPattern1.hsData = [42, 0]
cphyCustomPattern1.hsDataMode = 'prbs'
cphyCustomPattern1.hsPrbsOrder = 9
cphyCustomPattern1.hsPrbsSeed = None
cphyCustomPattern1.hsSymbols = '22200000000000'
cphyCustomPattern1.lpBits = ''
cphyCustomPattern1.packetSize = 1000
cphyCustomPattern1.patternType = 'packetLoop'
cphyCustomPattern1.sameDataInEachPacket = True
cphyCustomPattern1.stopDuration = 0

cphyParams1.calAlternateSeqNumPrbs = 8
cphyParams1.calPreambleNumUI = 21
cphyParams1.calUserSequence = [0x5555, 0xAAAA]
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
cphyParams1.tWaitOptical = 150000.0
cphyParams1.tlpxDuration = 100.0
cphyParams1.useAlp = False

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 200.0
mipiClockConfig1.referenceClocks = None

mipiCphyGenerator1.clockConfig = mipiClockConfig1
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
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

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
