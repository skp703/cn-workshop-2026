# Instructor runbook

## Instructional structure

Use the lecture deck and notebooks as complementary teaching artifacts. The
deck frames the engineering problem, develops the governing theory, explains
the data transformations, and identifies the decisions that require judgment.
The notebooks then expose the equations, intermediate values, library
operations, verification checks, and reportable outputs in executable form.
Neither artifact needs to carry the entire workshop alone.

The teaching cadence is therefore:

1. state the analytical question in the deck;
2. develop the governing relation or spatial method;
3. explain what `cnkit` computes and what the analyst must select;
4. move to the linked notebook for calculation and inspection; and
5. return to the deck for a report-out framed as an interpretive question.

Use these slide ranges during the four-hour workshop:

| Block | Slides | Notebook transition |
|---|---:|---|
| Orientation | 1–6 | Readiness Check before the workshop or at entry |
| Foundations and calibration | 7–15 | Slide 16 launches Notebook 01 |
| Lab 1 report-out | 17 | Return to the deck after the calculation |
| Earth Observation and spatial estimation | 18–34 | Slide 35 launches Notebook 02 |
| Lab 2 report-out | 36 | Return to the deck after the watershed result |
| Change, calibration, and antecedent state | 37–42 | Slide 43 launches Notebook 03 |
| Lab 3 report-out and synthesis | 44–48 | Complete the reporting statement before the close |

The workshop presents two data pathways within this common analytical
framework.

At each lab, put both options on the screen:

- **Reference data:** verified inputs for Difficult Run and Accotink Creek.
- **Earth Engine:** spatial inputs for a participant-selected watershed.

Participants may move between the pathways because both use the same result
schema and report-out questions. The Earth Engine setup guide and readiness
check support watershed-specific application; the versioned reference pathway
supports the complete analytical sequence with the same interpretation and
reporting requirements.

## Roles

- John leads the forty-minute introduction, Lab 1 report-out, and the reporting
  implications of lambda, weighting, and table values.
- Saurav leads the Earth Observation block, including delineation, the Earth
  Engine computation model, Annual NLCD, soils, joint distributions, and the
  Lab 2 report-out. Saurav also leads the uncertainty and antecedent-state block.
- Both instructors circulate during labs and share the close.
- Four helpers is the target for a room of forty. Brief them on the setup-cell
  output and the shared result schema for both pathways.

## Room setup

- Classroom or rounds, not theater seating.
- One helper per eight to ten participants.
- Project the persistent instruction slide during each lab.
- Put reference-data and Earth Engine groups at the same tables when possible.
  One participant may drive the watershed-specific computation while teammates
  audit provenance, spatial coverage, and assumptions.

## Lab artifacts

Lab 1: three runoff estimates and one defended convention.

Lab 2: watershed boundary, composite CN, unmapped percentage, and provenance.

Lab 3: trajectory, condition band, signal-to-assumption ratio, and a six-line
reporting statement.

## Release sequence

Keep solution notebooks instructor-only before the event. Release each solution
after its report-out, or publish all solutions in the post-workshop release.
Do not rely on a hidden branch in a public repository; public branches are
visible.

## Before the dry run

1. Test the readiness notebook from a personal Google account and an
   organization-managed account.
2. Run all prepared-data branches in fresh Colab runtimes.
3. Run the live branch of Labs 2 and 3 with two different Earth Engine projects.
4. Test all public links while signed out of GitHub and Google Drive.
5. Rehearse the full four hours with two participants who have not seen the material.
6. Load an offline copy of notebooks, `cnkit.py`, and the data pack onto USB media.
