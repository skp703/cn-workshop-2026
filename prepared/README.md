# Prepared Earth Engine outputs

These files let participants complete the same analysis when Earth Engine
access is unavailable.

They are not illustrative values. They were transcribed from the executed
notebooks under `evidence/gee-live/`, which preserve outputs, timestamps,
warnings, asset identifiers, and redacted authentication prompts.

`difficult_run_gee_summary.json` records the live 2019 joint land-cover/soil
result. `difficult_run_gee_trajectory.csv` records the seven-year trajectory
returned by `cnkit.workflows.cn_trajectory` for 2001 through 2019.

The V3 validation suite checks the anchor values against the executed notebook
outputs so this prepared route cannot silently diverge from the live evidence.
