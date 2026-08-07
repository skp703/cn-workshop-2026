# Participant guide

## Modern Curve Number Hydrology

This four-hour workshop moves from the published curve-number method to a
measured, spatially resolved result for a real watershed.

The workshop supports two complementary pathways:

- **Reference data pathway:** use verified records for Difficult Run or
  Accotink Creek and complete every calculation in the workshop sequence.
- **Earth Engine application:** bring a USGS gage number or outlet coordinates
  and use a registered Earth Engine project to repeat the spatial analysis for
  a selected watershed.

Both pathways use the same analytical framework and discussion questions.

## Before the workshop

Bring a laptop and charger. Nothing needs to be installed on your computer.
The notebooks run in Google Colab. A Google account is useful for saving your
own notebook copy.

Run `00_Readiness_Check.ipynb` once. It verifies Colab, installs the pinned
`cnkit` release if needed, downloads the versioned data pack, and includes an
Earth Engine project check.

If you want to apply the workflow through Earth Engine, follow `GEE_SETUP.md`
before the workshop. The reference-data pathway remains available for
participants who prefer to configure Earth Engine after the session.

## During the workshop

Open notebooks from the workshop website. For each lab:

1. Save a copy in Drive if you want to keep your edits.
2. Run the setup cell and wait for `setup complete`.
3. Select the reference-data or Earth Engine pathway.
4. Record the requested result and its provenance.
5. Be ready to explain what you would defend to a reviewer.

Earth Engine setup resources remain available after the session for continued
application to additional watersheds.

## Deliverables

By the close you will have:

- a watershed boundary and verification check;
- a composite curve number with its land-cover and soil sources;
- a change trajectory and hydrologic-condition band;
- a statement of unmapped area and important assumptions; and
- a six-line reporting checklist for future projects.
