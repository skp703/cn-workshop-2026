# Instructor runbook

## Instructional structure

The workshop presents two data pathways within a common analytical framework.

At each lab, put both options on the screen:

- **Reference data:** verified inputs for Difficult Run and Accotink Creek.
- **Earth Engine:** spatial inputs for a participant-selected watershed.

Participants may move between the pathways because both use the same result
schema and report-out questions. Earth Engine configuration questions can be
addressed with a helper or during a break while analysis proceeds with the
reference datasets.

## Roles

- John leads the forty-minute introduction, Lab 1 report-out, and the reporting
  implications of lambda, weighting, and table values.
- Saurav leads the Earth Observation block, Lab 2 report-out, and the uncertainty
  and antecedent-state block.
- Both instructors circulate during labs and share the close.
- Four helpers is the target for a room of forty. Brief them on the setup-cell
  output and the shared result schema for both pathways.

## Room setup

- Classroom or rounds, not theater seating.
- One helper per eight to ten participants.
- Project the persistent instruction slide during each lab.
- Put prepared-data groups and live-GEE groups at the same tables when possible.
  One authenticated participant may drive while teammates audit provenance and
  assumptions.

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
