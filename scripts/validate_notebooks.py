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
    "01_Understand_the_Curve_Number.ipynb": [
        "## 1. The event water-balance model",
        "### Analysis 1B — Verify the implementation against the equation",
        "## 2. Nonlinearity and the compositing question",
        "## 5. What `cnkit` did—and did not do",
    ],
    "02_Build_CN_for_a_Watershed.ipynb": [
        "## Step 2 — Delineate the watershed boundary",
        "## Step 3 — Verify and inspect the boundary",
        "## Step 7 — Construct land-cover–soil pairs",
        "## What the convenience method does",
    ],
    "03_Change_and_Uncertainty.ipynb": [
        "### Step 1 — Define what changes and what remains fixed",
        "### Optional application — delineate a selected watershed",
        "### Step 5 — Invert the rainfall–runoff equation",
        "### Step 8 — Distinguish rainfall history from observed wetness",
        "## What each library layer contributes",
    ],
}


def validate(path: Path) -> None:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)

    cell_ids = [cell.id for cell in notebook.cells]
    if len(cell_ids) != len(set(cell_ids)):
        raise ValueError(f"duplicate cell IDs in {path.name}")

    markdown = "\n".join(
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    )
    for required_text in CONTENT_REQUIREMENTS.get(path.name, []):
        if required_text not in markdown:
            raise ValueError(f"missing {required_text!r} in {path.name}")

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
