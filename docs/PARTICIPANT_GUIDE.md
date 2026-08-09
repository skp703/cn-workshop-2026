# Participant guide

## Modern Curve Number Hydrology

This four-hour workshop combines a common theoretical foundation, a guided
Google Earth Engine exercise, and a participant-directed hydrologic
investigation.

The workshop has three academic components:

1. **Curve Number theory:** governing equations, threshold behavior, parameter
   conventions, spatial aggregation, and evidence used to estimate CN.
2. **Getting started with Earth Engine:** a live Code Editor exercise using a
   watershed-scale boundary and NLCD data.
3. **Participant investigation:** ninety minutes devoted to one of four
   notebook questions, including a guided analytical core and optional
   extensions.

## Before the workshop

Bring a laptop and charger. The notebooks run in Google Colab, and the guided
Earth Engine exercise runs in the web Code Editor. A Google account is useful
for saving Colab copies and working directly in Earth Engine.

Run `00_Readiness_Check.ipynb` once. It verifies `cnkit`, the versioned workshop
data, and the core calculations. It can also verify a registered Earth Engine
project.

For direct participation in the Earth Engine exercise, follow `GEE_SETUP.md`
and open the Code Editor before the workshop. The guided demonstration and the
versioned notebook datasets remain available to all attendees.

## Workshop schedule

| Time | Activity |
|---|---|
| 0:00–0:10 | Introduction and workshop outcomes |
| 0:10–0:40 | Curve Number theory |
| 0:40–1:00 | Getting started with Google Earth Engine |
| 1:00–1:20 | Break and optional GEE exploration |
| 1:20–1:30 | Investigation introduction and group formation |
| 1:30–3:00 | Participant-directed notebook investigations |
| 3:00–3:15 | Break |
| 3:15–3:45 | Participant report-outs and discussion |
| 3:45–4:00 | Synthesis, resources, and feedback |

## Earth Engine exercise

The guided script asks how Earth Engine can describe the land surface inside a
watershed-scale boundary. It introduces geometries, feature collections, image
collections, filtering, band selection, clipping, visualization, pixel
inspection, `pixelArea`, grouped reduction, and deferred execution.

During the exploration interval, participants may change the NLCD year, map
location, visible layers, or catalog dataset. The exercise files are under
`gee/` in the workshop repository.

## Select one investigation

### 1. CN equation and runoff response

Examine how rainfall depth, lambda, and spatial aggregation alter runoff.

### 2. Spatial CN for a watershed

Build or audit a watershed boundary, land-cover–soil distribution, composite
CN, and design-runoff estimate.

### 3. Land-cover change and design runoff

Compare a controlled CN trajectory with hydrologic-condition sensitivity and
translate both to design runoff.

### 4. Event-derived CN and antecedent state

Infer CN from observed events, fit an asymptotic response, and compare
rainfall-history and root-zone-wetness conventions.

Each notebook includes a minimum guided result and several extensions. Select
one investigation as the primary activity; completion of every notebook is not
an instructional objective.

## Reporting record

Prepare a short report-out containing:

1. analytical question;
2. watershed or dataset;
3. data source, year, scale, and equation convention;
4. assumption or comparison examined;
5. principal quantitative result;
6. interpretation and limitation.

## Feedback

Complete the anonymous five-minute [workshop feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeavvSSEWlNcENVxCJZW9g22rztcJpi2Cd6ba6smZ9JX9toSA/viewform). It asks about conceptual clarity, the Earth Engine introduction, the participant-directed investigation period, time allocation, and future topics.
