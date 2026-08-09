# Instructor runbook

## Instructional structure

The workshop uses three complementary teaching environments:

- PowerPoint establishes the workshop question and develops Curve Number
  theory.
- The Earth Engine Code Editor provides a brief, guided introduction to cloud
  geospatial analysis.
- Four investigation notebooks support participant-directed analysis,
  extension, and interpretation.

The notebook period is intentionally participant-directed. It is not
unscaffolded: every notebook states a research question, provides a minimum
guided result, exposes intermediate calculations, explains relevant `cnkit`
operations, offers several extensions, and ends with a common reporting record.

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

## Opening: ten minutes

1. State the workshop question and five learning outcomes.
2. Explain the theory → Earth Engine → investigation sequence.
3. Show the common six-part reporting record.
4. Introduce the four investigation questions without explaining their
   procedures.

## Curve Number theory: thirty minutes

Use one numerical example throughout.

| Minutes | Focus |
|---:|---|
| 0–5 | Event water balance and the purpose of the method |
| 5–12 | CN, retention, and initial abstraction |
| 12–18 | Piecewise runoff equation, threshold, and lambda |
| 18–24 | Land cover, HSG, condition, and spatial aggregation |
| 24–30 | Table, spatial, and event-derived CN; reportable assumptions |

Retain calibration, detailed spatial processing, temporal sensitivity, and
antecedent-state analysis for the investigation notebooks.

## Earth Engine introduction: twenty minutes

Use `gee/01_watershed_land_surface.js` in the Code Editor.

| Minutes | Operation |
|---:|---|
| 0–3 | Identify the script, map, Console, Inspector, and Layers panel |
| 3–7 | Define the point and select a HUC12 `Feature` from a `FeatureCollection` |
| 7–12 | Open the NLCD `ImageCollection`; filter, select, and clip bands |
| 12–16 | Add land cover and imperviousness over the hybrid basemap |
| 16–19 | Calculate grouped class area with `pixelArea` and a reducer |
| 19–20 | Explain deferred execution and launch the optional exploration |

The HUC12 is a teaching geometry, not a substitute for outlet-based watershed
delineation. Investigation 2 treats delineation and boundary verification in
detail.

During the exploration interval, display these options:

1. change the NLCD year;
2. move the selection point;
3. inspect imperviousness values; or
4. add and describe another catalog dataset.

Participants may run the script directly, work in pairs, or review the
demonstrated outputs before selecting an investigation.

## Investigation launch: ten minutes

Present the four questions and ask participants to select one primary
investigation:

1. CN equation and runoff response;
2. spatial CN for a watershed;
3. land-cover change and design runoff; or
4. event-derived CN and antecedent state.

Ask participants to run the common setup, complete the minimum result, and then
select an extension. Groups may use versioned workshop data or apply supported
sections through Earth Engine. Both approaches require the same provenance and
interpretation record.

## Participant-directed investigations: ninety minutes

Use three facilitation checkpoints without interrupting the room:

- **20 minutes:** confirm that every group has a question, working dataset, and
  baseline result.
- **50 minutes:** ask which analytical choice the group is changing and what is
  being held constant.
- **75 minutes:** direct groups to the six-part reporting record and select one
  figure or table for discussion.

Suggested instructor distribution:

- John emphasizes equation behavior, compositing, event inversion, lambda, and
  calibration.
- Saurav emphasizes Earth Engine, boundary verification, land cover, soils,
  temporal comparison, and spatial provenance.
- Both instructors address interpretation, uncertainty, and reporting.

## Report-outs: thirty minutes

Use approximately five minutes for each investigation represented in the room,
then reserve ten minutes for cross-investigation synthesis. Each report-out
contains:

1. analytical question;
2. watershed or dataset;
3. data source and equation convention;
4. assumption or comparison examined;
5. principal quantitative result; and
6. interpretation and limitation.

## Feedback and close

Project the anonymous feedback-form link during the final fifteen minutes:

<https://docs.google.com/forms/d/e/1FAIpQLSeavvSSEWlNcENVxCJZW9g22rztcJpi2Cd6ba6smZ9JX9toSA/viewform>

The form evaluates the theory section, Earth Engine introduction, investigation
period, learning outcome, relevance, time allocation, topics needing more time,
and optional written comments.

## Before the dry run

1. Rehearse the ten-minute opening and thirty-minute theory block.
2. Run the GEE teaching script from a newly opened Code Editor session.
3. Test the optional exploration prompts with two accounts.
4. Execute every notebook from a fresh Colab runtime using reference data.
5. Run supported Earth Engine sections with two different projects.
6. Confirm all public links while signed out of GitHub.
7. Verify that the feedback form accepts a test response and remove the test
   response before the workshop.
8. Load offline copies of the notebooks, `cnkit.py`, and the data pack onto USB
   media.
