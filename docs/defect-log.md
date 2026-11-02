# Test defect log

Source: `mars abnormal.xlsx`, 11 records. Tested firmware: 1.26.31.

Order and priority follow the sheet: P0 first (two uncommanded-motion defects), then the
light-red rows as P1, then the orange rows as P2. Each entry is written as a GitHub issue:
searchable title, component prefix, explicit Expected vs Actual, and copy-pasteable steps.

---

## Terminology decisions

| Machine translation (original) | Reviewed | Why |
| --- | --- | --- |
| upper computer | RocketIDE | "upper computer" is a literal translation of shangweiji and is not used in English |
| XX is malfunctioning | specific symptom in the title | A title must be searchable and describe the failure, not the verdict |
| sporadic | intermittent | Standard bug-reporting term |
| collision error warning | collision alarm | Matches servo/EtherCAT vocabulary |
| unable to move | does not move | Active voice, shorter |
| the axis enablement exception | axis does not enable | Symptom-first |
| software stuck | hangs | Standard |
| must be powered off | requires a power cycle | Standard |
| IO number | IO points / channels | Standard for IO modules |
| as same as | identical | Correctness |

Also normalised: `EtherCAT` capitalisation, `OP state`, `Stop` button, `unlink`, function names in backticks.

---

## 1

**Title:** `link/unlink: unlinking a linked axis makes it jump back to the start position`

**Labels:** `bug` `safety` `module:axis` `module:motion`
**Priority:** P0   **Firmware:** 1.26.31
**Flag:** review as safety relevant - the axis performs an uncommanded move

**Description**
After a single axis is linked into `i_group` and a move has completed, calling `unlink` on that
axis makes it immediately return to the start position of the move. The motion is not commanded
by the application.

**Steps to reproduce**
1. `m_axis(0).link(0, 0, 1)`
2. `ECAT.Enable(0)`
3. `i_group(0).move([10])`
4. Wait for the move to complete
5. `m_axis(0).unlink(0)`
6. The axis jumps back to the start position

**Expected:** `unlink` detaches the axis and leaves its position unchanged.
**Actual:** the axis returns to the start position of the previous move.

---

## 2

**Title:** `i_group: cancel() during a reverse move makes the axis jump to the target position`

**Labels:** `bug` `safety` `module:motion`
**Priority:** P0   **Firmware:** 1.26.31
**Flag:** review as safety relevant - uncommanded motion at target position

**Description**
While an `i_group` axis is moving in the reverse direction, calling `cancel` causes the axis to
jump straight to the configured target position instead of decelerating and stopping.

**Steps to reproduce**
1. `m_axis(0).link(0, 0, 1)`
2. `ECAT.Enable(0)`
3. `i_group(0).move([10])`
4. `i_group(0).move([-30])`
5. `time.sleep_ms(20)`
6. `i_group(0).cancel()`
7. The axis jumps to the target position

**Expected:** `cancel` stops the move with a controlled deceleration at the current position.
**Actual:** the axis moves immediately to the target position.

---

## 3

**Title:** `solo_ax: define_pos() / default_speed() hangs RocketIDE and leaves the controller unresponsive`

**Labels:** `bug` `module:axis` `module:rocketide`
**Priority:** P1   **Firmware:** 1.26.31
**Subsystem:** Axis control (solo_ax) + RocketIDE

**Description**
Calling `solo_ax(0).define_pos()` followed by `solo_ax(0).default_speed([0, 10, 50])` from the
console makes RocketIDE wait for a long time. Most of RocketIDE then stops
working and the controller also enters a fault state. Only a power cycle restores normal operation.

**Steps to reproduce**
1. `solo_ax(0).define_pos()`
2. `solo_ax(0).default_speed([0, 10, 50])`
3. RocketIDE becomes unusable

**Expected:** both calls return promptly; RocketIDE and the controller stay responsive.
**Actual:** long wait, most RocketIDE functions unusable, controller unresponsive, power cycle required.

---

## 4

**Title:** `solo_ax: axis does not move after ECAT.Enable(0)`

**Labels:** `bug` `module:axis`
**Priority:** P1   **Firmware:** 1.26.31

**Description**
Enabling the axis through `solo_ax` and then calling `move` leaves the axis stationary.
The axis reports as enabled but never executes the motion.

**Steps to reproduce**
1. `ECAT.Enable(0)`
2. `solo_ax(0).move(10)`
3. The axis does not move

**Expected:** the axis moves 10 units.
**Actual:** no motion, no error reported.

---

## 5

**Title:** `Controller stops responding after Stop is pressed following a program hang`

**Labels:** `bug` `module:runtime`
**Priority:** P1   **Firmware:** 1.26.31
**Flag:** review as safety relevant - control is lost while powered and enabled

**Description**
Running a large program file causes the interpreter to hang. Pressing Stop tears down the program
thread, after which the controller enters a fault state and no longer responds to RocketIDE. Recovery requires a power cycle.

**Steps to reproduce**
1. Run a large program file
2. Wait until execution hangs
3. Press the Stop button
4. The program thread is terminated and the controller stops responding

**Expected:** Stop aborts the running program and leaves the controller responsive.
**Actual:** the controller becomes unresponsive to all commands.

---

## 6

**Title:** `ECAT.Enable(): axis reports enabled but move commands do nothing, and breakpoint debugging hangs`

**Labels:** `bug` `module:axis` `module:runtime`
**Priority:** P1   **Firmware:** 1.26.31

**Description**
Using `ECAT.Enable()` in code can leave the axis in a state where it reports as enabled but does
not move, and `move` calls have no effect. Breakpoint debugging also hangs in the same state.
Disabling and re-enabling a different axis reproduces it.

**Steps to reproduce**
1. `ECAT.Enable(0)`, then `ECAT.Disable(0)`
2. `ECAT.Enable(1)`
3. `i_group(0).move([0, 12])`
4. Axis 1 no longer moves

**Expected:** axis 1 executes the move and breakpoints remain usable.
**Actual:** axis 1 is enabled but does not move; breakpoint debugging does not respond.

---

## 7

**Title:** `Large single-file program: intermittent failures immediately after power-up`

**Labels:** `bug` `module:runtime` `need-more-info`
**Priority:** P1   **Firmware:** 1.26.31

**Description**
When a large single-file program is executed immediately after power-up, it fails intermittently:
sometimes the axis will not enable, sometimes the axis is enabled but does not move. The failure
is not deterministic and depends on running the file right after boot.

**Steps to reproduce**
1. Power on the controller and connect RocketIDE
2. Immediately run the large program file
3. Observe an intermittent failure (axis will not enable, or enabled but does not move)

**Expected:** the program runs normally on every power-up.
**Actual:** intermittent failures, frequency depends on how soon the file is started after boot.

**Note:** needs the failing program (or a reduced version) plus a serial log from boot to failure.

---

## 8

**Title:** `IO scan: two controllers with an identical EtherCAT configuration report different IO counts`

**Labels:** `bug` `module:fieldbus` `module:io`
**Priority:** P1   **Firmware:** 1.26.31

**Description**
Two MARS controllers loaded with the same EtherCAT configuration file and connected to the same
IO modules report a different number of IO points after scanning. The hardware setup is identical,
so the scan result should also be identical.

**Steps to reproduce**
1. Load the same EtherCAT configuration file on both controllers
2. Connect the same IO modules to both controllers
3. Compare the IO points shown in RocketIDE

**Expected:** both controllers report the same number of IO points.
**Actual:** the reported IO counts differ between the two units.

**Note:** please attach both configuration files, the IO module model numbers and a screenshot of
each scan result.

---

## 9

**Title:** `RocketIDE help: collapsible sections cannot be collapsed`

**Labels:** `bug` `module:rocketide`
**Priority:** P2   **Firmware:** 1.26.31

**Description**
In the RocketIDE help documentation, clicking a section header expands the section, but the
section cannot be collapsed again.

**Steps to reproduce**
1. Open the RocketIDE documentation
2. Click any collapsible section header
3. The section expands and can no longer be collapsed

**Expected:** clicking the header toggles the section open and closed.
**Actual:** the section stays expanded.

---

## 10

**Title:** `EtherCAT status window does not show the axis collision alarm`

**Labels:** `bug` `module:fieldbus` `module:rocketide`
**Priority:** P2   **Firmware:** 1.26.31

**Description**
When an EtherCAT axis is commanded to move and a collision alarm is raised, the alarm is not
visible anywhere in the RocketIDE EtherCAT status window. There is no way to see
the error code that caused the stop.

**Steps to reproduce**
1. Initialise the EtherCAT motion axes
2. Trigger a collision alarm on a moving axis
3. Open the EtherCAT status window

**Expected:** the collision alarm and its error code are displayed.
**Actual:** no error information is shown.

---

## 11

**Title:** `RocketIDE: EtherCAT status is not refreshed after reconnecting`

**Labels:** `bug` `module:rocketide` `module:fieldbus`
**Priority:** P2   **Firmware:** 1.26.31

**Description**
After RocketIDE is disconnected from and then reconnected to the controller, the
EtherCAT status is not re-read. The window keeps showing the state captured before the disconnect.

**Steps to reproduce**
1. Connect RocketIDE to the controller
2. Initialise EtherCAT to OP state
3. Disconnect RocketIDE
4. Reconnect

**Expected:** the EtherCAT status is re-read and reflects the current state.
**Actual:** the status stays frozen at the pre-disconnect state.

---

---
