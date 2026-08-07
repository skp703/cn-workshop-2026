"""Validate and execute the reference-data pathway in all participant notebooks."""

from __future__ import annotations

import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "notebooks" / "00_Readiness_Check.ipynb",
    ROOT / "notebooks" / "01_Understand_the_Curve_Number.ipynb",
    ROOT / "notebooks" / "02_Build_CN_for_a_Watershed.ipynb",
    ROOT / "notebooks" / "03_Change_and_Uncertainty.ipynb",
]

CONTENT_REQUIREMENTS = {
    "00_Readiness_Check.ipynb": [
        "## Step 1 — Establish the reproducible environment",
        "## Step 2 — Identify the library layers",
        "## Step 3 — Verify the core calculation and data files",
        "## Step 4 — Verify an Earth Engine project",
        "## Step 5 — Select a watershed identifier",
        "## Step 6 — Review the readiness record",
    ],
    "01_Understand_the_Curve_Number.ipynb": [
        "## Step 1 — Define the event water-balance model",
        "## Step 2 — Translate CN into retention and initial abstraction",
        "## Step 3 — Evaluate and verify the runoff equation",
        "## Step 4 — Compare distributed and lumped watershed representations",
        "## Step 5 — Examine how compositing depends on storm depth",
        "## Step 6 — Treat lambda and CN as a paired calibration",
        "## Step 7 — Invert observed rainfall and runoff to event curve numbers",
        "## Step 8 — Fit and interpret an asymptotic curve number",
        "## Method audit — Library operation and analyst decision",
    ],
    "02_Build_CN_for_a_Watershed.ipynb": [
        "## Step 1 — Identify the watershed and outlet",
        "## Step 2 — Delineate the watershed boundary",
        "## Step 3 — Verify and inspect the boundary",
        "## Step 4 — Initialize Earth Engine and bind the boundary",
        "## Step 5 — Measure land cover",
        "## Step 6 — Measure hydrologic soil group",
        "## Step 7 — Construct land-cover–soil pairs",
        "## Step 8 — Apply the lookup to each pair",
        "## Step 9 — Aggregate and state the convention",
        "## Step 10 — Quantify the independence assumption",
        "## Step 11 — Calculate design runoff and assemble provenance",
        "## What the convenience method does",
        "## Method audit — Library operation and analyst decision",
    ],
    "03_Change_and_Uncertainty.ipynb": [
        "### Step 1 — Define what changes and what remains fixed",
        "### Step 2 — Load the recorded Earth Engine trajectory",
        "### Step 3 — Interpret the hydrologic-condition interval",
        "### Step 4 — Understand how `cn_trajectory` performs the calculation",
        "### Step 4A — Delineate a selected watershed",
        "### Step 4B — Calculate the annual trajectory",
        "### Step 5 — Invert the rainfall–runoff equation",
        "### Step 6 — Estimate the standard asymptotic response",
        "### Step 7 — Treat lambda and CN as a paired calibration",
        "### Step 8 — Distinguish rainfall history from observed wetness",
        "### Step 9 — Compare the conventions on the same storm dates",
        "### Step 10 — Relate wetness rank to observed event response",
        "## Method audit — Library operation and analyst decision",
    ],
}

CODE_REQUIREMENTS = {
    "00_Readiness_Check.ipynb": [
        'WATERSHED_INPUT = "reference"',
        "WATERSHED_CONFIG = {",
        "WATERSHED_SELECTION_READY = True",
        'print("Readiness check complete. Continue to Lab 1.")',
    ],
    "02_Build_CN_for_a_Watershed.ipynb": [
        "ADD_BACKGROUND_MAP = True",
        '"USGSTopo/MapServer/export"',
        '"Basemap: USGS The National Map — USGS Topo"',
    ],
    "03_Change_and_Uncertainty.ipynb": [
        "paired_calibration = pd.DataFrame(paired_rows)",
        'runoff(DESIGN_DEPTH_IN, fitted.cn_inf, lam=lam)',
    ],
}


def validate_markdown_math(markdown: str, path: Path) -> None:
    """Require GitHub/Colab dollar delimiters and balanced math spans."""
    legacy_inline = [token for token in (r"\(", r"\)") if token in markdown]
    legacy_display = [
        line.strip()
        for line in markdown.splitlines()
        if line.strip() in {r"\[", r"\]"}
    ]
    if legacy_inline or legacy_display:
        found = sorted(set(legacy_inline + legacy_display))
        raise ValueError(f"legacy math delimiters {found!r} in {path.name}")

    if markdown.count("$$") % 2:
        raise ValueError(f"unbalanced display-math delimiters in {path.name}")

    mixed_display_lines = [
        line for line in markdown.splitlines() if "$$" in line and line.strip() != "$$"
    ]
    if mixed_display_lines:
        raise ValueError(f"display math must use standalone $$ lines in {path.name}")

    without_display = markdown.replace("$$", "")
    if without_display.count("$") % 2:
        raise ValueError(f"unbalanced inline-math delimiters in {path.name}")

    unbalanced_inline_lines = [
        line for line in without_display.splitlines() if line.count("$") % 2
    ]
    if unbalanced_inline_lines:
        raise ValueError(f"inline math must close on the same line in {path.name}")


def validate(path: Path) -> None:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)

    empty_cells = [
        index
        for index, cell in enumerate(notebook.cells)
        if not cell.source.strip()
    ]
    if empty_cells:
        raise ValueError(f"empty cells {empty_cells!r} in {path.name}")

    cell_ids = [cell.id for cell in notebook.cells]
    if len(cell_ids) != len(set(cell_ids)):
        raise ValueError(f"duplicate cell IDs in {path.name}")

    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    validate_markdown_math(markdown, path)
    for required_text in CONTENT_REQUIREMENTS.get(path.name, []):
        if required_text not in markdown:
            raise ValueError(f"missing {required_text!r} in {path.name}")

    source_code = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "code"
    )
    for required_text in CODE_REQUIREMENTS.get(path.name, []):
        if required_text not in source_code:
            raise ValueError(f"missing code {required_text!r} in {path.name}")

    client = NotebookClient(
        notebook,
        timeout=300,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    )
    client.execute()
    print(f"validated {path.relative_to(ROOT)}")


def main() -> None:
    runtime = ROOT / ".tmp"
    runtime.mkdir(exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(runtime / "matplotlib"))
    os.environ.setdefault("IPYTHONDIR", str(runtime / "ipython"))
    for path in NOTEBOOKS:
        validate(path)


if __name__ == "__main__":
    main()
