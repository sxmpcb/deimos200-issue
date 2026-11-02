# Deimos200 Test Issue Tracker

This repository is used **only to log and track test defects and QA-related items for Deimos200**. No product source code lives here.

---

## 1. How to file an issue

1. Go to **Issues > New issue**
2. Pick a template:
   - **Test Defect** - bugs found during testing (structured form, key fields required)
   - **Test Case / Process Suggestion** - anything that is not a defect
3. Submit. The `triage` label is applied automatically and the issue waits for triage.

> Please search existing issues first. Duplicates are closed and linked to the original.

## 2. Severity definitions

| Level | Meaning | Response target |
| --- | --- | --- |
| **P0** | Crash, main flow completely unusable, data loss or corruption | Fix immediately, release blocker |
| **P1** | Major function broken, no workaround | Must be fixed in this release |
| **P2** | Function broken but a workaround exists | Scheduled fix |
| **P3** | UI, copy or interaction polish | Fix when convenient |

## 3. Labels

| Group | Labels |
| --- | --- |
| Type | `bug` `enhancement` `question` |
| Status | `triage` (new) `confirmed` `wontfix` `duplicate` `need-more-info` |
| Severity | `P0` `P1` `P2` `P3` |
| Module | `module:auth` `module:checkout` ... (adjust to your modules) |
| Version | `v2.3.1` style, or use Milestones |

### Creating the labels quickly

```bash
# Type and status
for l in "bug:d73a4a:Something is not working" \
         "enhancement:a2eeef:New feature or request" \
         "triage:fbca04:Awaiting triage" \
         "confirmed:0e8a16:Triage confirmed" \
         "need-more-info:d876e3:More information required" \
         "wontfix:ffffff:This will not be worked on" \
         "duplicate:cfd3d7:Already reported"; do
  name="${l%%:*}"; rest="${l#*:}"; color="${rest%%:*}"; desc="${rest#*:}"
  gh label create "$name" --color "$color" --description "$desc" --force
done

# Severity
for p in P0 P1 P2 P3; do gh label create "$p" --color "b60205" --description "Severity $p" --force; done
```

## 4. Issue lifecycle

```
New (triage) --> Triaged (confirmed + P-level + module) --> In fix --> Ready to verify --> Closed
                     |
                     +--> need-more-info / duplicate / wontfix
```

- The **tester** verifies the fix and comments the result before closing
- If a closed issue recurs, reopen it and note the version where it reappeared

## 5. Repository layout

```
.github/
+-- ISSUE_TEMPLATE/
|   +-- bug_report.yml   # structured defect form
|   +-- other.md         # test case / process suggestion
|   +-- config.yml       # template entry configuration
docs/                    # test plans and test cases
```

## 6. Collaboration notes

- Working language: **English** (UK team + remote collaboration)
- Timezone: post updates in the issue thread so async review is possible
- Anything blocking a release must be linked from the release Milestone
