# SVT Test
# SVT version 22.2.2
# Test saved 2022-06-09_1508
# Form factor: SV3C_4L6G_MIPI_DPHY_GENERATOR
# PY3
# Checksum: 0e632fc3e58a95c1f02417bdb503b160
# Note: This file is the 'Save' file for the Test.
#       It should not be used as a standalone Python script.
#       But it can be used via 'runSvtTest.py'.


coordinator1 = _create('coordinator1', 'SvtCoordinator', iespName='None')
startCoordinator = _create('startCoordinator', 'SvtFunction', iespName='None')

dphyCustomPattern1 = _create('dphyCustomPattern1', 'SvtMipiDphyCustomPattern')
dphyParameters1 = _create('dphyParameters1', 'SvtMipiDphyParameters')
mipiClockConfig1 = _create('mipiClockConfig1', 'SvtMipiClockConfig')
mipiDphyGenerator1 = _create('mipiDphyGenerator1', 'SvtMipiDphyGenerator')
mipiProtocol = _create('mipiProtocol', 'SvtMipiProtocol')
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


dphyCustomPattern1.hsBytes = [0]
dphyCustomPattern1.hsDataMode = 'hsBytes'
dphyCustomPattern1.patternType = 'hsOnly'

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
dphyParameters1.tTaSureDuration = 1.0
dphyParameters1.tlpxDuration = 80.0
dphyParameters1.useAlp = False
dphyParameters1.usePreambleSequence = False

mipiProtocol.csiScramble = False
mipiProtocol.csiVersion = 'Csi2_v1_3'
mipiProtocol.protocol = 'CSI'

refClocksConfig1.outputClockAFormat = 'LVDS'
refClocksConfig1.outputClockAFreq = 100.0
refClocksConfig1.outputClockBFormat = 'LVDS'
refClocksConfig1.outputClockBFreq = 100.0
refClocksConfig1.systemRefClockSource = 'internal'

mipiClockConfig1.dataRate = 1500.0
mipiClockConfig1.referenceClocks = refClocksConfig1
mipiClockConfig1.sscEnabled = False

mipiDphyGenerator1.clockConfig = mipiClockConfig1
mipiDphyGenerator1.clockSkew = 0.0
mipiDphyGenerator1.continuousClock = False
mipiDphyGenerator1.dataLanes = [1, 2, 3, 4]
mipiDphyGenerator1.dataSkews = [0.0]
mipiDphyGenerator1.hsClockCommonVoltage = 200.0
mipiDphyGenerator1.hsClockPostTap = 0
mipiDphyGenerator1.hsClockPreTap = 0
mipiDphyGenerator1.hsClockVoltageAmplitude = 100.0
mipiDphyGenerator1.hsDataCommonVoltages = [200.0]
mipiDphyGenerator1.hsDataPostTaps = [0]
mipiDphyGenerator1.hsDataPreTaps = [0]
mipiDphyGenerator1.hsDataVoltageAmplitudes = [100.0]
mipiDphyGenerator1.jitterInjection = None
mipiDphyGenerator1.lpClockHighVoltage = 1200.0
mipiDphyGenerator1.lpClockLowVoltage = 0.0
mipiDphyGenerator1.lpDataHighVoltages = [1200.0]
mipiDphyGenerator1.lpDataLowVoltages = [0.0]
mipiDphyGenerator1.params = dphyParameters1
mipiDphyGenerator1.pattern = dphyCustomPattern1
mipiDphyGenerator1.resetPatternMemory = True
mipiDphyGenerator1.splitDataAcrossLanes = False

#! TEST PROCEDURE
iesp = getIespInstance()
dphyCustomPattern1.hsBytes = 255
mipiDphyGenerator1.setup()

analyzerIsRunning = startCoordinator()

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
