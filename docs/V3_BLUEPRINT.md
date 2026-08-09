# V3 blueprint

## Communication job

Participants should leave able to distinguish the Curve Number model from the
evidence used to estimate its parameters, use Earth Engine to inspect
watershed-scale spatial data, and defend one analytical result.

The workshop is organized around a common foundation followed by participant
inquiry:

1. ten-minute introduction;
2. thirty-minute Curve Number theory block;
3. twenty-minute guided Earth Engine exercise;
4. optional Earth Engine exploration during the first break;
5. ninety-minute participant-directed investigation period; and
6. comparative report-outs, synthesis, resources, and feedback.

## Roles of the teaching artifacts

- The lecture deck establishes the scientific problem, develops the governing
  equations, explains the evidence types, frames the GEE demonstration, and
  structures the report-outs.
- The Code Editor script introduces Earth Engine objects and operations through
  one watershed land-surface example.
- The notebooks expose equations, intermediate values, library operations,
  verification checks, extensions, and reporting records.
- The participant portal is the entry point for preparation, schedule,
  investigation selection, resources, and feedback.

## Participant investigations

The readiness notebook is pre-work and is not counted as an investigation.

| Investigation | Research focus | Minimum reportable result |
|---|---|---|
| CN equation and runoff response | Rainfall depth, lambda, and spatial aggregation | Runoff comparison under two stated conventions |
| Spatial CN for a watershed | Boundary, land cover, soils, spatial pairing, and composite CN | Mapped boundary and CN with provenance |
| Land-cover change and design runoff | Temporal signal relative to condition sensitivity | Trajectory and runoff comparison |
| Event-derived CN and antecedent state | Event inversion, asymptotic fit, and antecedent proxy | Fitted CN and antecedent-state comparison |

Each notebook contains a guided core that can be completed before selecting an
extension. Participants choose one primary investigation rather than following
all notebooks sequentially.

## Data and computation

Earth Engine is taught as a spatial-analysis environment before the notebook
period. Investigation 2 and Investigation 3 support direct application to a
selected watershed through Earth Engine. Versioned workshop products support
the complete analytical and reporting requirements of all four investigations.

Both live and versioned results must retain the applicable watershed, year,
source asset, scale, lookup, equation convention, and unmapped-area information.

## Four-hour run of show

| Time | Block | Minutes | Lead |
|---|---|---:|---|
| 0:00 | Introduction and workshop outcomes | 10 | Both |
| 0:10 | Curve Number theory | 30 | John |
| 0:40 | Getting started with Google Earth Engine | 20 | Saurav |
| 1:00 | Break and optional GEE exploration | 20 | Both available |
| 1:20 | Introduce investigations and form groups | 10 | Both |
| 1:30 | Participant-directed notebook investigations | 90 | Both circulate |
| 3:00 | Break | 15 | |
| 3:15 | Participant report-outs and discussion | 30 | Both |
| 3:45 | Synthesis, resources, and feedback | 15 | Both |
| 4:00 | End | | |

## Common reporting record

Every investigation ends with the same six elements:

1. analytical question;
2. watershed or dataset;
3. data source, year, scale, and equation convention;
4. assumption or comparison examined;
5. principal quantitative result; and
6. interpretation and limitation.

This common structure allows cross-investigation discussion even when groups
select different questions.

## Feedback instrument

The anonymous Google Form evaluates:

- theory-section clarity;
- Earth Engine introduction clarity;
- the balance of guidance and analytical choice;
- ability to identify reportable data sources and assumptions;
- relevance to professional, teaching, or research work;
- time allocation;
- topics that should receive more time; and
- optional written recommendations.

## Public/private boundary

Public:

- participant portal and schedule;
- readiness notebook and four investigations;
- GEE teaching script and continuing resources;
- prepared data pack;
- lecture deck;
- participant guide and Earth Engine setup guide;
- feedback form;
- source citations, environment files, and reproducible build scripts.

Instructor-only until release:

- solutions and answer keys;
- dry-run observations and timing notes;
- instructor Earth Engine extraction notebooks;
- internal validation results requiring credentials;
- conference contacts and logistical correspondence.

## Design principles

1. Establish the model before introducing the platform.
2. Teach Earth Engine through one coherent hydrologic example.
3. Use notebooks for participant investigation rather than sequential lecture
   transcription.
4. Give every investigation a minimum analytical result and open extensions.
5. Preserve intermediate results and provenance.
6. Use the same reporting structure across investigations.
7. Pin every numerical example to a test or source record.
8. Keep the participant portal, deck, notebooks, GEE exercise, and runbook on
   the same schedule.

## V3 live anchors

The Earth Engine notebooks were executed successfully on 6 August 2026. These
observed values support the spatial and temporal investigations:

| Quantity | Live result |
|---|---:|
| 2019 CN, observed joint distribution | 75.7790 |
| 2019 CN, same raster marginals crossed independently | 77.6638 |
| Independence assumption | +1.8848 CN |
| 2001 to 2019 CN change | +0.2876 CN |
| Mean poor-to-good condition spread | 8.4473 CN |
| Assumption-to-signal ratio | 29.4 |
| Raster soil area with no HSG | 21.2655% |

The earlier 4.50-CN example is the range between extreme feasible pairings of
two tabular marginals. It is a bound rather than the measured Earth Engine
correction and must be labeled accordingly when retained.
