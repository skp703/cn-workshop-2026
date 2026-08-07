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


def validate(path: Path) -> None:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)

    cell_ids = [cell.id for cell in notebook.cells]
    if len(cell_ids) != len(set(cell_ids)):
        raise ValueError(f"duplicate cell IDs in {path.name}")

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
