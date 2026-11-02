# Deimos200 Test Issue Tracker

Issue tracker for **Deimos200**, a motion controller running **MicroPython** firmware.

This repository holds **test defects and QA records only**. No product source code, firmware binaries or private keys live here.

---

## 1. Product under test

| Item | Detail |
| --- | --- |
| Product | Deimos200 motion controller |
| Runtime | MicroPython (custom board port) |
| Interfaces | USB CDC, UART / RS-485, CAN, Ethernet, Wi-Fi |
| Axes | Multi-axis, encoder feedback, homing and limit switches |

When filing an issue always state **firmware version**, **hardware revision** and **MicroPython version**.
Without them a motion defect usually cannot be reproduced.

## 2. Safety-critical defects

Motion controllers can injure people and damage hardware. If you observe any of the following:

- unexpected, uncontrolled or runaway axis motion
- position or parameter loss after a power cycle
- a motor stalling, overheating, or drawing abnormal current
- a safety interlock, limit switch or e-stop being ignored
- a firmware crash while an axis is moving under load

then:

1. **Stop the rig and remove power** before investigating further
2. Mark the issue `P0` and add the `safety` label
3. Escalate immediately through the agreed safety channel - an issue alone is not an escalation
4. Preserve the log, the script and the exact rig configuration

## 3. How to file an issue

1. Go to **Issues > New issue**
2. Choose a template:
   - **Test Defect** - structured form for firmware, motion and protocol defects
   - **Test Case / Process Suggestion** - coverage gaps and process improvements
3. Submit. `triage` is applied automatically.

> Search existing issues first. Duplicates are closed and linked to the original.

## 4. Severity definitions

| Level | Meaning | Response target |
| --- | --- | --- |
| **P0** | Safety event, crash, unrecoverable state, data/parameter loss, main function unusable | Fix immediately, release blocker |
| **P1** | Core motion or protocol function incorrect, no workaround | Must be fixed in this release |
| **P2** | Function incorrect but a workaround exists | Scheduled fix |
| **P3** | Usability, diagnostics, documentation and polish | Fix when convenient |

## 5. Labels

| Group | Labels |
| --- | --- |
| Type | `bug` `enhancement` `question` |
| Status | `triage` `confirmed` `wontfix` `duplicate` `need-more-info` |
| Severity | `P0` `P1` `P2` `P3` |
| Safety | `safety` |
| Subsystem | `module:motion` `module:axis` `module:homing` `module:encoder` `module:io` `module:fieldbus` `module:runtime` `module:flash` `module:ota` |
| Firmware | `fw:1.4.2` style, or use Milestones |

### Creating the labels quickly

```bash
# Type, status and safety
for l in "bug:d73a4a:Something is not working" \
         "enhancement:a2eeef:New feature or request" \
         "triage:fbca04:Awaiting triage" \
         "confirmed:0e8a16:Triage confirmed" \
         "need-more-info:d876e3:More information required" \
         "wontfix:ffffff:This will not be worked on" \
         "duplicate:cfd3d7:Already reported" \
         "safety:b60205:Safety relevant - escalate immediately"; do
  name="${l%%:*}"; rest="${l#*:}"; color="${rest%%:*}"; desc="${rest#*:}"
  gh label create "$name" --color "$color" --description "$desc" --force
done

# Severity
for p in P0 P1 P2 P3; do gh label create "$p" --color "b60205" --description "Severity $p" --force; done

# Subsystems
for m in motion axis homing encoder io fieldbus runtime flash ota; do
  gh label create "module:$m" --color "1d76db" --description "Subsystem: $m" --force
done
```

## 6. Issue lifecycle

```
New (triage) --> Triaged (confirmed + P-level + subsystem) --> In fix --> Ready to verify --> Closed
                     |
                     +--> need-more-info / duplicate / wontfix
```

- Fix verification is done on the rig by the **reporter** or a nominated tester, and the result is commented before closing
- Always record the firmware build used for verification
- If a closed issue recurs, reopen it and note the firmware version where it reappeared

## 7. What to include with every report

- firmware build and hardware revision of the unit
- MicroPython version
- rig configuration: number of axes, steps per revolution, supply voltage, load
- the shortest script or REPL sequence that triggers the defect
- full traceback, error or status codes
- measured values where applicable (position error, latency, jitter, current)

## 8. Repository layout

```
.github/
+-- ISSUE_TEMPLATE/
|   +-- bug_report.yml   # structured defect form
|   +-- other.md         # test case / process suggestion
|   +-- config.yml       # template entry configuration
docs/                    # test plans, test cases, rig notes
```

## 9. Collaboration notes

- Working language: **English** (UK team, remote and asynchronous)
- Leave findings in the issue thread rather than in chat, so both sites can follow the history
- Anything blocking a release must be linked from the release Milestone
