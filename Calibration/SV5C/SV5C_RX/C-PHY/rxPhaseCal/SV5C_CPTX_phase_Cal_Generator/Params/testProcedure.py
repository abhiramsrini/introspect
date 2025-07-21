# SVT Test
# SVT version 23.1.b6
# Test saved 2022-11-25_1521
# Form factor: SV5C_4L8G_MIPI_CPHY_GENERATOR
# PY3
# Checksum: 8b0e10fa237742c61209d6c4416de016
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
startCoordinator = _create('startCoordinator', 'SvtFunction', iespName='None')

customPattern1 = _create('customPattern1', 'SvtMipiCphyCustomPattern')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiCphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
params1 = _create('params1', 'SvtMipiCphyParams')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')

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


customPattern1.hsData = [42, 0]
customPattern1.hsDataMode = 'prbs'
customPattern1.hsPrbsOrder = 9
customPattern1.hsPrbsSeed = None
customPattern1.hsSymbols = '22200000000000'
customPattern1.lpBits = ''
customPattern1.packetSize = 1000
customPattern1.patternType = 'hsOnly'
customPattern1.sameDataInEachPacket = True
customPattern1.stopDuration = 0

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 5000.0
mipiClockConfig1.referenceClocks = refClocksConfig1

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.commonNoise = None
mipiGenerator1.hsCommonVoltagesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.hsPostTaps = [0]
mipiGenerator1.hsPreTaps = [0]
mipiGenerator1.hsVoltageAmplitudesABC = [(200.0, 200.0, 200.0)]
mipiGenerator1.jitterInjection = None
mipiGenerator1.lanes = [1, 2, 3, 4]
mipiGenerator1.lpHighVoltages = [1200.0]
mipiGenerator1.lpLowVoltages = [0.0]
mipiGenerator1.params = params1
mipiGenerator1.pattern = customPattern1
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = False
mipiGenerator1.wireSkewsABC = [(0.0, 0.0, 0.0)]

mipiProtocol.csiScramble = False
mipiProtocol.csiScrambleNumSeeds = 'one'
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

params1.calAlternateSeqNumPrbs = 8
params1.calPreambleNumUI = 21
params1.calUserSequence = [0x5555, 0xAAAA]
params1.calibrationPreambleFormat = 'format_1'
params1.lp000Duration = 65.0
params1.lp001Duration = 100.0
params1.opticalLink = 'disabled'
params1.post2NumUI = 112
params1.postNumUI = 112
params1.postSymbols = '4444444'
params1.preBeginNumUI = 196
params1.preBeginSymbols = '3333333'
params1.preEndSymbols = '3333333'
params1.progSeqSymbols = '33333333333333'
params1.syncWord = '3444443'
params1.t3AlpPauseMin = 50
params1.t3AlpPauseWake = 50
params1.tHsExitDuration = 300.0
params1.tTaGetDuration = 5
params1.tTaGoDuration = 4.0
params1.tTaSureDuration = 1.0
params1.tWaitOptical = 150000.0
params1.tlpxDuration = 100.0
params1.useAlp = False

refClocksConfig1.externRefClockFreq = 250.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.systemRefClockSource = 'internal'

#! TEST PROCEDURE
iesp = getIespInstance()
svtVersion = requireSvtVersionInRange("24.3", None)

analyzerIsRunning = startCoordinator()

mipiGenerator1.setup()
# Execute tests based on commands from Analyzer
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
