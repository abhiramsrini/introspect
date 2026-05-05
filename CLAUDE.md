# Introspect Calibration Repository

## Overview

This repository holds calibration and validation test procedures for Introspect Technology signal generator units: **SV3C**, **SV5C**, **SV7C**, and **SV7-PAM3**. Scripts were originally written for Keysight Infiniium oscilloscopes and have been manually converted to support **Teledyne LeCroy** oscilloscopes using the MAUI VBS automation interface.

All scripts run inside **Introspect ESP (SVT)** software — they are not standalone Python scripts.

---

## Folder Structure & Status

```
Calibration/
├── SV3C/                   # Active SV3C TX and RX procedures
├── SV3C_FROM_PREM/         # READ-ONLY — reference copy from Primeasure. Never modify.
├── SV5C/                   # Active SV5C C-PHY and D-PHY procedures
├── SV7-PAM3/               # Active SV7 PAM3 TX calibrations
└── SV7C/                   # Active SV7C TX alignment and common mode + RX procedures
```

### Folder naming conventions

| Pattern | Status | Action |
|---|---|---|
| `*UsingLeCroy` / `*UsingLeCroyScope` | **Active** | Modify these |
| `*UsingKeysightScope` / `*UsingKeySightScope` | Deprecated reference | Do not modify |
| `OLD_*` prefix | Deprecated earlier LeCroy attempt | Do not touch |
| `*Cal` suffix | Calibration (generates cal coefficients) | — |
| `*Val` suffix | Validation (verifies cal against thresholds) | — |
| `Results/` subdirectories | Run output snapshots | Never modify |

---

## SVT Framework

Every `testProcedure.py` is an **SVT save file**, not a standalone script. It uses a special DSL:

```python
obj = _create('name', 'SvtType', iespName='None')   # create SVT object
obj.args = 'arg1, arg2'                              # function signature
obj.code = r'''...python code...'''                  # function body as raw string
obj.wantAllVarsGlobal = False
```

The `#! TEST PROCEDURE` comment marks the start of main execution code — everything above it is object configuration.

### SVT built-in globals (available in all function code)
- `sleepMillis(ms)` — sleep
- `waitForGuiOkDialog(msg)` — pause for operator confirmation
- `getIespInstance()` — get handle to device under test
- `getSvtVersion()` — get software version string
- `dftUtil.beep(freq, duration)` — audio alert
- `writeNoteForTestRun("Pass"/"Fail")` — mark test result
- `warningMsg(str)` / `errorMsg(str)` — log messages
- `np` (numpy) — available after `import numpy as np` in the procedure body

---

## Teledyne LeCroy Oscilloscope API

### Connection (Windows only — requires LeCroy ActiveDSO COM object)
```python
import win32com.client
osci = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
osci.MakeConnection("IP:169.254.197.102")
```

> **Known issue**: Many `initScope` functions hardcode `169.254.197.102` instead of using
> `calOptions.scopeIPAddress`. This is a known limitation — the IP should be extracted
> from the VISA string and passed in. When modifying `initScope`, prefer using the address
> from `scopeIpAddress` argument rather than hardcoding.

### Command syntax

| Purpose | Syntax |
|---|---|
| Send VBS command (no return value) | `osci.WriteString("VBS 'app.property = value'", 1)` |
| Query VBS value (returns a string) | `osci.WriteString("VBS? 'return=app.property'", 1)` |
| Read response separately | `result = osci.ReadString(500)` |
| Wait for scope operation | `osci.WriteString("*OPC?", 1)` |

`WriteString` and `writestring` both work (COM is case-insensitive) but **PascalCase `WriteString` is preferred** for consistency.

### Channel naming — LeCroy vs Keysight
| Scope | Format | Example |
|---|---|---|
| LeCroy VBS (active) | `C<n>` | `"C1"`, `"C2"` |
| Keysight SCPI (deprecated) | `CHANnel<n>` / `CHAN<n>` | `"CHANnel1"` |

---

## Key VBS Property Paths (MAUI Automation)

```vbs
app.SetToDefaultSetup
app.WaitUntilIdle(timeout_seconds)          ' returns when scope is idle

' Acquisition
app.Acquisition.Cx.View = True/False
app.Acquisition.Cx.Deskew = 0
app.Acquisition.Cx.Coupling = 0             ' 0 = 50 Ohm
app.Acquisition.Cx.AverageSweeps = 1
app.Acquisition.Horizontal.HorScale = <sec_per_div>
app.Acquisition.Trigger.CxSlope = 0         ' 0 = rising edge

' Autoscale
app.Autoset.FindAllVerScale
app.Autoset.DoAutosetup

' Measurements
app.Measure.ShowMeasure = True
app.Measure.StatsOn = True
app.Measure.ClearSweeps
app.Measure.Px.View = True/False
app.Measure.Px.ParamEngine = "Mean"/"Amplitude"/"DeltaTimeAtLevel"
app.Measure.Px.Source1 = "C1"
app.Measure.Px.Source2 = "C2"
app.Measure.Px.Out.Result.Mean
app.Measure.Px.Out.Result.Sdev
app.Measure.Px.Out.Result.Sweeps

' DeltaTimeAtLevel operator settings
app.Measure.Px.Operator.Slope1 = 0          ' 0 = rising edge
app.Measure.Px.Operator.PercentLevel1 = 50
app.Measure.Px.Operator.Slope2 = 0
app.Measure.Px.Operator.PercentLevel2 = 50
```

---

## Standard Function Patterns

### `initScope` (LeCroy)
Always returns `osci`. Standard sequence:
1. Dispatch COM object and connect via IP
2. `app.SetToDefaultSetup` + `*OPC?`
3. Enable channel views and zero deskew
4. Set 50 Ohm coupling
5. Configure measurement parameters (P1, P2, etc.)
6. Optionally autoscale
7. `return osci`

### `measureDeltaTime` (TxAlignment LeCroy — robust quality-controlled pattern)
```python
channelSource = "C%d" % channel
osci.WriteString("VBS 'app.Measure.P1.Source1 = \"C1\"'", 1)
osci.WriteString("VBS 'app.Measure.P1.Source2 = \"%s\"'" % channelSource, 1)
osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)
sleepMillis(calOptions.scopeAutoScaleDelay)

max_meas_iterations = 15
currentDeltaTime = 0

for i in range(max_meas_iterations):
    sweeps = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Sweeps'", 1))
    std    = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Sdev'", 1))
    if sweeps > calOptions.numAverages and std * 1e12 < calOptions.max_std_ps:
        currentDeltaTime = float(osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Mean'", 1))
        break
    elif sweeps > calOptions.numAverages and std * 1e12 > calOptions.max_std_ps:
        osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)  # restart, too noisy
    else:
        sleepMillis(500)  # still accumulating

assert currentDeltaTime != 0, 'Unable to measure delay within std threshold.'
return currentDeltaTime
```

### Common `calOptions` fields
| Field | Type | Purpose |
|---|---|---|
| `serialNumber` | str | DUT serial number |
| `scopeIPAddress` | str | VISA string (e.g. `TCPIP0::169.254.197.102::inst0::INSTR`) |
| `scopeMeasurementDelay` | float | ms to wait for measurement to settle |
| `scopeAutoScaleDelay` | float | ms to wait after autoscale |
| `numAverages` | int | Minimum sweeps before accepting a reading |
| `max_std_ps` | float | Maximum acceptable std deviation in picoseconds |
| `calChannels` / `calLanes` | list[int] | Channels to calibrate (e.g. 1–16) |
| `calRates` | list[float] | Data rates in Mbps to sweep (alignment cal) |
| `commonModeValues` | list[float] | Common-mode voltages in mV to test |
| `amplitudeValues` | list[float] | Differential amplitudes in mV to test |

---

## Calibration Output File Format

Cal files follow a section-based text format:
```
BEGIN SECTION
section type : header
serial number : <SN>
hardware revision : <Rev>
date of calibration(YYYYMMDD) : <date>
END SECTION

BEGIN SECTION
section type : tx_alignment_calibration_data
<polynomial coefficients, one row per coefficient order>
END SECTION
```

---

## Known Issues / Gotchas

1. **Hardcoded scope IP**: `initScope` in most LeCroy scripts hardcodes `169.254.197.102` instead of using `calOptions.scopeIPAddress`. Always update the IP when deploying to a different lab setup.

2. **Keysight VISA string default**: The default `scopeIPAddress` value in many scripts (`TCPIP0::10.20.20.200::inst0::INSTR`) points to the old Keysight scope. Update to the LeCroy scope's actual address.

3. **`WaitUntilIdle` typo**: Some scripts have `app.WaitUntiIdle` (missing `l`). Correct form is `app.WaitUntilIdle(5)`.

4. **Missing VBS quote**: In some SV3C `performScopeMeasurement` functions, `"VBS app.Measure.P2.Source1 = \"%s\"'"` is missing the opening `'` after `VBS`. Correct form: `"VBS 'app.Measure.P2.Source1 = \"%s\"'"`.

5. **`osci` is not automatically global**: `initScope` returns `osci`; the caller must assign it (`osci = initScope(...)`). Functions that use `osci` depend on it being in the SVT global scope — this works because `initScope` is typically called at the top of the `#! TEST PROCEDURE` block.

---

## Keysight → LeCroy Command Reference

| Keysight (deprecated) | LeCroy VBS equivalent |
|---|---|
| `scope1.connect()` / `scope1.reset()` | `osci.MakeConnection("IP:...")` + `app.SetToDefaultSetup` |
| `scope1.sendCommand(":CALibrate:SKEW CHANnel1,0")` | `osci.WriteString("VBS 'app.Acquisition.C1.Deskew = 0'", 1)` |
| `scope1.setTimeScale(5e-8)` | `osci.writestring("VBS 'app.Acquisition.Horizontal.HorScale = 5e-8'", 1)` |
| `osci.write(":MEASure:DELTatime CHANnel1,...")` | Set `P1.Source1`/`P1.Source2` + `P1.ParamEngine = "DeltaTimeAtLevel"` |
| `osci.query(":MEASure:RESults?")` | `osci.WriteString("VBS? 'return=app.Measure.P1.Out.Result.Mean'", 1)` |
| `vCmMeasurement.run()` (`SvtScopeMeasurement`) | Manual VBS loop with `P1.ParamEngine = "Mean"` |
| `vAmpMeasurement.run()` (`SvtScopeMeasurement`) | Manual VBS loop with `P1.ParamEngine = "Amplitude"` |
| `scope1._resetAllMeasurements()` | `osci.WriteString("VBS 'app.Measure.ClearSweeps'", 1)` |
