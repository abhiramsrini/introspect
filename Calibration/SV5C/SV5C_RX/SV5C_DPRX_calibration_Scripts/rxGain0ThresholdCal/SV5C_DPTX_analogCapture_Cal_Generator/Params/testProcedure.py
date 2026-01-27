# SVT Test
# SVT version 25.1.b4
# Test saved 2024-12-05_1029
# Form factor: SV5C_4L8G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: 51c0870c857721994a743aa98fe10d93
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName=None)
startCoordinator = _create('startCoordinator', 'SvtFunction', iespName=None)

customPattern1 = _create('customPattern1', 'SvtMipiDphyCustomPattern')
dphyParameters1 = _create('dphyParameters1', 'SvtMipiDphyParameters')
jitterInjection1 = _create('jitterInjection1', 'SvtMipiDphyJitterInjection')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiGenerator1 = _create('mipiGenerator1', 'SvtMipiDphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
refClocksConfig1 = _create('refClocksConfig1', 'SvtRefClocksConfig')

coordinator1.clientName = 'Generator'
coordinator1.clientSecret = ''
coordinator1.serverHostName = 'localhost'
coordinator1.serverPort = 12013

startCoordinator.args = ''
startCoordinator.code = r'''coordinator1.startLocalServerOnGui()

status = coordinator1.waitForClientState("Analyzer", "running", 120)
if status :
    analyzerIsRunning = 1
else :
    print("Analyzer not ready...")
    analyzerIsRunning = 0

return analyzerIsRunning
'''
startCoordinator.wantAllVarsGlobal = False


customPattern1.hsBytes = [0]
customPattern1.hsDataMode = 'hsBytes'
customPattern1.hsPrbsOrder = 'PRBS_9'
customPattern1.hsPrbsSeed = None
customPattern1.lpBits = ''
customPattern1.packetSize = 1000
customPattern1.patternType = 'hsOnly'
customPattern1.sameDataInEachPacket = True
customPattern1.stopDuration = 0

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
dphyParameters1.tTaSureDuration = 1.0
dphyParameters1.tlpxDuration = 80.0
dphyParameters1.useAlp = False
dphyParameters1.usePreambleSequence = False

jitterInjection1.hsClockJitterAmplitude = 0.0
jitterInjection1.hsClockJitterFrequency = 20.0
jitterInjection1.hsClockRandomJitterAmplitude = 0.0
jitterInjection1.hsDataJitterAmplitudes = [0.0]
jitterInjection1.hsDataJitterFrequencies = [20.0]
jitterInjection1.hsDataRandomJitterAmplitudes = [0.0]
jitterInjection1.timeUnits = 'unitWidth'
jitterInjection1.wires = 'both'

mipiClockConfig1.autoDetectTimeout = 2.0
mipiClockConfig1.dataRate = 200.0
mipiClockConfig1.referenceClocks = refClocksConfig1
mipiClockConfig1.sscEnabled = False
mipiClockConfig1.sscFrequency = 50.0
mipiClockConfig1.sscSpread = 1.0

mipiGenerator1.clockConfig = mipiClockConfig1
mipiGenerator1.clockSkew = 0.0
mipiGenerator1.commonNoise = None
mipiGenerator1.continuousClock = False
mipiGenerator1.dataLanes = [1, 2, 3, 4]
mipiGenerator1.dataSkews = [0.0]
mipiGenerator1.hsClockCommonVoltage = 200.0
mipiGenerator1.hsClockPostTap = 0
mipiGenerator1.hsClockPreTap = 0
mipiGenerator1.hsClockVoltageAmplitude = 100.0
mipiGenerator1.hsDataCommonVoltages = [200.0]
mipiGenerator1.hsDataPostTaps = [0]
mipiGenerator1.hsDataPreTaps = [0]
mipiGenerator1.hsDataVoltageAmplitudes = [100.0]
mipiGenerator1.jitterInjection = jitterInjection1
mipiGenerator1.lpClockHighVoltage = 1200.0
mipiGenerator1.lpClockLowVoltage = 0.0
mipiGenerator1.lpDataHighVoltages = [1200.0]
mipiGenerator1.lpDataLowVoltages = [0.0]
mipiGenerator1.params = dphyParameters1
mipiGenerator1.pattern = customPattern1
mipiGenerator1.resetPatternMemory = True
mipiGenerator1.splitDataAcrossLanes = False

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'
mipiProtocol.useEotp = False

refClocksConfig1.externRefClockFreq = 250.0
refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.systemRefClockSource = 'internal'

#! TEST PROCEDURE
svtVersion = requireSvtVersionInRange("25.1", None)

analyzerIsRunning = startCoordinator()
iesp = getIespInstance()

customPattern1.hsBytes = [170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170]
mipiGenerator1.pattern = customPattern1
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
