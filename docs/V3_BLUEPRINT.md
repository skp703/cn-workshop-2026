# V3 blueprint

## Communication job

The participant should leave with a result, not a folder of examples:

> Build and audit a curve number for a real watershed, then state which parts
> are measurements and which are assumptions.

V3 replaces the nine-deck, eight-core-notebook sequence with one master deck,
three labs, one readiness check, and one participant portal. The schedule on
the site, in the slides, in the notebooks, and in the instructor runbook is the
same schedule.

## Two synchronized data pathways

- The **reference-data pathway** uses verified outputs for several contrasting
  watersheds. It completes every hydrologic calculation and every learning
  objective.
- The **Earth Engine pathway** applies the spatial workflow to a
  participant-selected watershed.

Both pathways use the same result schemas and rejoin for every report-out. A
live analysis and a reference-data analysis can therefore be interpreted through
the same questions and reporting framework.

## Four-hour run of show

| Time | Block | Minutes | Lead |
|---|---|---:|---|
| 0:00 | Welcome and what you will build | 10 | Both |
| 0:10 | Introduction: from rainfall to curve number | 40 | John |
| 0:50 | Lab 1: understand and audit the equation | 20 | Both circulate |
| 1:10 | Report-out 1 | 10 | John |
| 1:20 | Break | 15 | |
| 1:35 | From lookup tables to Earth Observation | 25 | Saurav |
| 2:00 | Lab 2: build a CN for a watershed | 35 | Both circulate |
| 2:35 | Report-out 2 | 10 | Saurav |
| 2:45 | Break | 15 | |
| 3:00 | Change, antecedent condition, and uncertainty | 20 | Saurav |
| 3:20 | Lab 3: change and uncertainty | 25 | Both circulate |
| 3:45 | What would you defend in a report? | 15 | Both |
| 4:00 | End | | |

## V2 to V3 content map

| V2 material | V3 destination |
|---|---|
| Welcome deck | Master deck opening and participant portal |
| Part 0 fundamentals + Part 1 | One forty-minute introduction |
| A1 and A2 | Lab 1, with the strongest calculations retained |
| Part 2 + B1/B2/B3 | Earth Observation lecture and Lab 2 |
| D1 + D2 | Live branch of Lab 2 |
| Part 3 + C1/C2/C3 | Uncertainty lecture and prepared branch of Lab 3 |
| D3 | Live branch of Lab 3 |
| Recent developments and close | Final synthesis and reporting checklist |
| GEE account guide | Pre-work setup page and readiness notebook |

## Public/private boundary

Public:

- Participant portal and schedule
- Readiness notebook and three attendee labs
- Prepared data pack
- Master lecture deck
- Participant guide and Earth Engine setup guide
- Source citations, environment files, and reproducible build scripts

Instructor-only until release:

- Solutions and answer keys
- Dry-run observations and timing notes
- Instructor Earth Engine extraction notebook
- Internal validation results requiring credentials
- Conference contacts and logistical correspondence

## Design principles

1. The method comes before the platform.
2. Reference datasets and Earth Engine outputs use the same analytical schema.
3. Every lab produces one reportable artifact.
4. Prepared and live data share the same schema.
5. Every number shown in slides is pinned by a test or source record.
6. The site is the participant's front door; Drive is not part of the normal path.
7. Earth Engine resources remain available for continued watershed applications
   after the scheduled session.

## V3 live anchors

The Earth Engine notebooks were executed successfully on 6 August 2026 after
the initial V2 handoff was written. V3 uses those observed live values rather
than the earlier estimates:

| Quantity | Live result |
|---|---:|
| 2019 CN, observed joint distribution | 75.7790 |
| 2019 CN, same raster marginals crossed independently | 77.6638 |
| Independence assumption | +1.8848 CN |
| 2001 to 2019 CN change | +0.2876 CN |
| Mean poor-to-good condition spread | 8.4473 CN |
| Assumption-to-signal ratio | 29.4 |
| Raster soil area with no HSG | 21.2655% |

The earlier 4.50-CN figure is a range between extreme feasible pairings of the
two tabular marginals. It is a bound, not the measured Earth Engine correction,
and V3 labels it accordingly whenever it is retained as a teaching example.
