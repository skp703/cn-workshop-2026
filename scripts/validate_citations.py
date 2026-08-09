#!/usr/bin/env python3
"""Fail validation when known citation errors re-enter workshop materials."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_FILES = [
    ROOT / "scripts" / "build_notebooks.py",
    ROOT / "vendor" / "cnkit.py",
    ROOT / "docs" / "SOURCES.md",
    ROOT / "gee" / "README.md",
    ROOT / "README.md",
]
TEXT_FILES.extend(sorted((ROOT / "notebooks").glob("*.ipynb")))

FORBIDDEN = {
    "10.1061/(ASCE)1084-0699(2003)8:6(445)": "invalid DOI formerly attached to the Hawkins method",
    "Hawkins et al. (2003) empirical conversion": "the 2003 conversion paper is Woodward first author",
}

REQUIRED = {
    "10.1061/(ASCE)0733-9437(1993)119:2(334)": "Hawkins 1993 asymptotic method",
    "10.1061/40685(2003)308": "Woodward et al. 2003 initial-abstraction study",
}


def main() -> None:
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in TEXT_FILES)
    problems = []
    for citation, reason in FORBIDDEN.items():
        if citation in corpus:
            problems.append(f"forbidden citation found: {citation} ({reason})")
    for citation, reason in REQUIRED.items():
        if citation not in corpus:
            problems.append(f"required citation missing: {citation} ({reason})")
    if problems:
        raise SystemExit("\n".join(problems))
    print("Citation audit passed: Hawkins 1993 and Woodward et al. 2003 are distinct and correctly identified.")


if __name__ == "__main__":
    main()
