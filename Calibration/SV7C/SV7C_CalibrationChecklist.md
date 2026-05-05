# SV7C Calibration Checklist

---

## Phase 1 — Firmware & Default Setup

- [ ] Open the Firmware Updater
- [ ] Press **Alt+F** before browsing to select the firmware file on the PC
- [ ] Browse to and select the `.mif` calibration firmware file *(note: this is a `.mif`, not a `.jam`)*
- [ ] Flash the firmware and wait for completion
- [ ] Load the **default calibration file** onto the unit and power cycle

---

## Phase 2 — TX Calibration

- [ ] Run **TX Common Mode Calibration** (`sv7CommonModeCalUsingLeCroy`)
- [ ] Run **TX Alignment Calibration** (`TxAlignmentCalUsingLeCroy`)
- [ ] Collect both output calibration files and upload it on sharefile
- [ ] Send calibration files to **Introspect** team for processing

> Wait for Introspect to return the generated `.jam` file before proceeding.

---

## Phase 3 — TX Validation

- [ ] Receive `.jam` file from Introspect
- [ ] Load the `.jam` file onto the unit
- [ ] Run **TX Common Mode Validation** (`sv7CommonModeValUsingLeCroy`)
- [ ] Run **TX Alignment Validation** (`TxAlignmentValUsingLeCroy`)
- [ ] Verify all channels pass

---

## Phase 4 — RX Calibration

- [ ] Run **RX PerPhase Calibration** (`RxPerPhaseThresholdCal`)
- [ ] Run **RX Auto-Align Calibration** (`RxAutoAlignCal`)
- [ ] Collect RX calibration output files
- [ ] Submit RX calibration files to **Introspect** team for processing

> Wait for Introspect to return the `.jam` file(s) before proceeding.

---

## Phase 5 — RX Validation & Sign-Off

- [ ] Receive `.jam` file(s) from Introspect
- [ ] Load the `.jam` file(s) onto the unit
- [ ] Run **RX PerPhase Validation** (`RxPerPhaseThresholdVal`)
- [ ] Run **RX Auto-Align Validation** (`RxAutoAlignVal`)
- [ ] Verify all channels pass
- [ ] Upload results

---

## Notes

| Item | Detail |
|---|---|
| Firmware file type | `.mif` (use Alt+F in Firmware Updater before browsing) |
| Cal output sent to Introspect | After Phase 2 and Phase 4 |
| `.jam` files received from Introspect | Before Phase 3 and Phase 5 |
| Scripts location | `Calibration/SV7C/` |
