"""Build the readiness notebook and four participant investigations.

The generated notebooks support verified reference datasets and live Earth
Engine analysis through a common analytical and reporting framework.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import json
import textwrap

try:
    import nbformat as nbf
except ImportError:
    class _V4:
        @staticmethod
        def new_markdown_cell(source):
            return {
                "cell_type": "markdown",
                "id": hashlib.sha1(("md:" + source).encode()).hexdigest()[:8],
                "metadata": {},
                "source": source,
            }

        @staticmethod
        def new_code_cell(source):
            return {
                "cell_type": "code",
                "id": hashlib.sha1(("code:" + source).encode()).hexdigest()[:8],
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source,
            }

        @staticmethod
        def new_notebook(cells):
            return {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}

    class _Nbf:
        v4 = _V4()

        @staticmethod
        def write(notebook_value, target):
            Path(target).write_text(json.dumps(notebook_value, indent=1) + "\n", encoding="utf-8")

    nbf = _Nbf()


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"
OUT.mkdir(exist_ok=True)


def clean(value: str) -> str:
    return textwrap.dedent(value).strip("\n") + "\n"


def md(value: str):
    return nbf.v4.new_markdown_cell(clean(value))


def code(value: str):
    return nbf.v4.new_code_cell(clean(value))


def gee_data_source_register(title="## Earth Engine data-source register"):
    """Document every Earth Engine asset used by the workshop workflows."""
    return md(f'''
    {title}

    The table below records the exact Earth Engine asset identifiers used in
    the guided exercise and the optional live notebook pathway. An asset
    identifier documents the computational input; the agency product remains
    the scientific data source that should be cited in a report.

    | Workshop use | Publisher and product | Exact Earth Engine asset | Relevant band or object | Native scale | Catalog status |
    |---|---|---|---|---:|---|
    | Guided watershed geometry | U.S. Geological Survey, Watershed Boundary Dataset, HUC12 | `USGS/WBD/2017/HUC12` | `FeatureCollection`; field `huc12` | vector | Official Earth Engine catalog |
    | Guided land cover and imperviousness | U.S. Geological Survey, NLCD 2019 release | `USGS/NLCD_RELEASES/2019_REL/NLCD` | `landcover`; `impervious` | 30 m | Official Earth Engine catalog |
    | Live annual land-cover distribution and trajectory | U.S. Geological Survey, Annual NLCD Collection 1 | `projects/sat-io/open-datasets/USGS/ANNUAL_NLCD/LANDCOVER` | first band of each annual image | 30 m | Earth Engine Community Catalog mirror |
    | Live mean fractional impervious surface | U.S. Geological Survey, Annual NLCD Collection 1 | `projects/sat-io/open-datasets/USGS/ANNUAL_NLCD/FRACTIONAL_IMPERVIOUS_SURFACE` | first band of each annual image | 30 m | Earth Engine Community Catalog mirror |
    | Live soil map-unit keys for `SOILS_SOURCE="sda"` | USDA Natural Resources Conservation Service, gNATSGO | `projects/sat-io/open-datasets/gNATSGO/raster/mukey` | first band; integer map-unit key | 30 m | Earth Engine Community Catalog mirror |
    | Optional global HSG comparison for `SOILS_SOURCE="hihydro"` | FutureWater, HiHydroSoil v2.0 | `projects/sat-io/open-datasets/HiHydroSoilv2_0/Hydrologic_Soil_Group_250m` | first band; modeled HSG class | 250 m | Earth Engine Community Catalog asset |

    **Supporting services that are not Earth Engine assets.** The USGS NLDI
    [web service](https://api.water.usgs.gov/docs/nldi/) constructs the live watershed
    boundary before `cnkit` converts it to an Earth Engine geometry. For the
    `sda` soil pathway, Earth Engine supplies only the gNATSGO map-unit keys;
    the USDA NRCS Soil Data Access
    [web service](https://sdmdataaccess.sc.egov.usda.gov/WebServiceHelp.aspx)
    supplies the dominant-condition hydrologic-soil-group attributes joined to
    those keys.

    **Source and access documentation.** See the USGS
    [Annual NLCD product page](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database),
    USDA NRCS [gNATSGO documentation](https://www.nrcs.usda.gov/resources/data-and-reports/gridded-national-soil-survey-geographic-database-gnatsgo),
    the Earth Engine catalog entries for
    [WBD HUC12](https://developers.google.com/earth-engine/datasets/catalog/USGS_WBD_2017_HUC12)
    and [NLCD 2019](https://developers.google.com/earth-engine/datasets/catalog/USGS_NLCD_RELEASES_2019_REL_NLCD),
    and the [Earth Engine Community Catalog Annual NLCD record](https://gee-community-catalog.org/projects/annual_nlcd/).

    The `projects/sat-io` paths are community-hosted access copies. Record the
    exact asset ID and retrieval date for reproducibility, but cite the original
    agency product as the data source. Availability of annual images is checked
    at runtime rather than assumed from a fixed list of years.
    ''')


def notebook(title: str, role: str, cells: list):
    nb = nbf.v4.new_notebook(cells=cells)
    metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": title, "provenance": []},
        "cnkit_workshop": {
            "version": "3.0",
            "role": role,
            "default_path": "reference data",
            "earth_engine_supported": True,
        },
    }
    if isinstance(nb, dict):
        nb["metadata"] = metadata
    else:
        nb.metadata = metadata
    return nb


SETUP = r'''
# V3 portable setup: local repository, GitHub Pages bundle, or Colab.
from pathlib import Path
import hashlib
import importlib
import importlib.util
import os
import subprocess
import sys
import urllib.request
import zipfile

CNKIT_VERSION = "1.1.0"
BUNDLE_URL = (
    "https://skp703.github.io/cn-workshop-2026/"
    "downloads/cn_workshop_v3_data.zip"
)
BUNDLE_SHA256 = "925861246fe9520c4b7f399227ca6133e60f27a5063a73c9fb6715cd9904780c"


def _is_workshop_root(path):
    return (path / "data" / "sites.csv").exists() and (path / "prepared").exists()


def _find_workshop_root():
    candidates = [
        Path.cwd(),
        Path.cwd().parent,
        Path("/content/cnkit_workshop"),
    ]
    requested = os.environ.get("CNKIT_WORKSHOP_HOME")
    if requested:
        candidates.insert(0, Path(requested).expanduser())
    for candidate in candidates:
        candidate = candidate.resolve()
        if _is_workshop_root(candidate):
            return candidate, "existing workshop folder"

    destination = Path("/content/cnkit_workshop") if Path("/content").exists() else Path.cwd() / ".cnkit_workshop"
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / "cn_workshop_v3_data.zip"
    print("Downloading the versioned V3 workshop bundle...")
    request = urllib.request.Request(BUNDLE_URL, headers={"User-Agent": "cn-workshop-v3"})
    with urllib.request.urlopen(request, timeout=120) as response, archive.open("wb") as handle:
        handle.write(response.read())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != BUNDLE_SHA256:
        raise RuntimeError(
            "Workshop bundle checksum mismatch. Expected %s, received %s. "
            "Delete %s and try again." % (BUNDLE_SHA256, digest, archive)
        )
    with zipfile.ZipFile(archive) as zipped:
        zipped.extractall(destination)
    if not _is_workshop_root(destination):
        raise RuntimeError("The workshop bundle downloaded but required files are missing.")
    return destination.resolve(), "checksum-verified workshop download"


WORKSHOP_ROOT, DATA_SOURCE = _find_workshop_root()
DATA_DIR = WORKSHOP_ROOT / "data"
PREPARED_DIR = WORKSHOP_ROOT / "prepared"


def _load_cnkit():
    try:
        import cnkit as package
        if getattr(package, "__version__", None) == CNKIT_VERSION:
            return package, "installed package"
    except ImportError:
        pass

    for candidate in [
        WORKSHOP_ROOT / "vendor" / "cnkit.py",
        WORKSHOP_ROOT / "cnkit.py",
        Path.cwd() / "vendor" / "cnkit.py",
        Path.cwd().parent / "vendor" / "cnkit.py",
    ]:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("cnkit", candidate)
            package = importlib.util.module_from_spec(spec)
            sys.modules["cnkit"] = package
            spec.loader.exec_module(package)
            return package, str(candidate)

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "cnkit==" + CNKIT_VERSION]
    )
    importlib.invalidate_caches()
    import cnkit as package
    return package, "PyPI"


def activate_full_cnkit():
    """Return the installed package with data, delineation, and GEE modules."""
    global cnkit, CNKIT_SOURCE
    if hasattr(cnkit, "__path__"):
        return cnkit
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "cnkit[gee]==" + CNKIT_VERSION]
    )
    for name in [key for key in sys.modules if key == "cnkit" or key.startswith("cnkit.")]:
        del sys.modules[name]
    importlib.invalidate_caches()
    cnkit = importlib.import_module("cnkit")
    CNKIT_SOURCE = "PyPI with Earth Engine dependencies"
    return cnkit


cnkit, CNKIT_SOURCE = _load_cnkit()
print("cnkit version:", getattr(cnkit, "__version__", CNKIT_VERSION + " workshop module"))
print("cnkit source :", CNKIT_SOURCE)
print("data source  :", DATA_SOURCE)
print("data folder  :", DATA_DIR)
print("setup complete")
'''


def build_readiness():
    cells = [
        md(r'''
        # Readiness check

        Run this notebook before the workshop. It verifies the reference-data
        environment and includes an Earth Engine project check for participants
        who plan to analyze a selected watershed.

        **Success means:** `cnkit 1.1.0`, a checksum-verified data bundle or a
        local workshop folder, and three known runoff values. If you enable the
        Earth Engine check, success also prints `42`.
        '''),
        md(r'''
        ## Step 1 — Establish the reproducible environment

        The setup cell performs infrastructure work only. It does not calculate
        a curve number and it does not authenticate Earth Engine.

        1. It looks for an existing workshop folder.
        2. If needed, it downloads the versioned data bundle and verifies its
           SHA-256 checksum before extraction.
        3. It loads `cnkit` 1.1.0 from the installed package, the workshop's
           portable module, or PyPI—in that order.
        4. It defines `DATA_DIR` and `PREPARED_DIR` so every later code cell
           records where its inputs came from.

        The printed version and source lines are part of the analytical
        provenance. Retain them when exporting a notebook for review.
        '''),
        code(SETUP),
        md(r'''
        ## Step 2 — Identify the library layers

        | Layer | Responsibility |
        |---|---|
        | `cnkit.core` | Rainfall–runoff equation, inverse equation, and compositing mathematics |
        | `cnkit.lookup` | NLCD–soil-group lookup tables, hydrologic condition, and unmapped-area accounting |
        | `cnkit.delineate` | Outlet snapping, watershed delineation, area checks, geometry, and boundary provenance |
        | `cnkit.gee` | Earth Engine requests for land cover, imperviousness, soils, and their pixelwise joint distribution |
        | `cnkit.workflows` | Reproducible orchestration across years; it delegates the hydrologic calculations to the layers above |

        The laboratory notebooks call these layers separately before showing
        the corresponding convenience workflow. This makes the scientific
        assumptions visible rather than embedding them in a single function.
        '''),
        gee_data_source_register("## Step 2A — Record the Earth Engine data sources"),
        md(r'''
        ## Step 3 — Verify the core calculation and data files

        The numerical check calls `composite_runoff` for a known heterogeneous
        watershed example. Internally, the function validates the curve numbers
        and area weights, normalizes the weights, evaluates runoff on each
        subarea, and also evaluates runoff from area-weighted CN and
        area-weighted retention. The three expected values therefore test the
        core equation and both aggregation pathways.

        The second check confirms that the event, land-cover, soil, boundary,
        and recorded Earth Engine products used later are present.
        '''),
        code(r'''
        from cnkit import composite_runoff

        expected = [0.4745, 0.0949, 0.0277]
        actual = [round(x, 4) for x in composite_runoff(1.0, [98, 55], [0.6, 0.4])]
        print("weighting check:", actual)
        assert actual == expected
        CORE_CALCULATION_READY = actual == expected

        required = [
            DATA_DIR / "events_01646000.csv",
            DATA_DIR / "landcover_streamcat.csv",
            DATA_DIR / "soils_hsg.csv",
            PREPARED_DIR / "difficult_run_gee_summary.json",
            PREPARED_DIR / "difficult_run_gee_trajectory.csv",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise FileNotFoundError("Missing workshop files:\n" + "\n".join(missing))
        REFERENCE_DATA_READY = not missing
        print("reference-data pathway: ready")
        '''),
        md(r'''
        ## Step 4 — Verify an Earth Engine project

        Set `TEST_EARTH_ENGINE = True` after registering a Cloud project for
        Earth Engine. Leave it at `False` when using the workshop reference data.

        The project ID is requested at runtime and is not saved in this notebook.
        '''),
        code(r'''
        TEST_EARTH_ENGINE = False
        EARTH_ENGINE_STATUS = "not checked"

        if TEST_EARTH_ENGINE:
            import os
            from getpass import getpass
            import ee

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass("Earth Engine project ID: ")
            ee.Authenticate()
            ee.Initialize(project=project)
            answer = ee.Number(21).multiply(2).getInfo()
            assert answer == 42
            EARTH_ENGINE_STATUS = "verified"
            print("Earth Engine check:", answer)
            print("live path: ready")
        else:
            print("Reference-data environment: ready")
            print("Set TEST_EARTH_ENGINE=True to verify an Earth Engine project.")
        '''),
        md(r'''
        ## Step 5 — Select a watershed identifier

        Choose the identifier that will be used in the spatial notebooks. The
        reference selection uses a prepared watershed record. The other
        selections store either a USGS gage number or an outlet coordinate for
        the live application.

        Edit only the configuration lines at the beginning of the next cell:

        - `WATERSHED_INPUT="reference"` with `REFERENCE_WATERSHED` set to
          `"difficult_run"` or `"accotink_creek"`;
        - `WATERSHED_INPUT="gage"` with an eight-digit USGS gage number; or
        - `WATERSHED_INPUT="outlet"` with latitude and longitude in decimal
          degrees.

        The cell validates the format and prints a compact configuration record.
        It does not delineate the watershed; that operation is shown and
        verified separately in Investigation 2.
        '''),
        code(r'''
        import pandas as pd
        from IPython.display import display

        # Participant configuration
        WATERSHED_INPUT = "reference"       # "reference", "gage", or "outlet"
        REFERENCE_WATERSHED = "difficult_run"
        SELECTED_GAGE = "01646000"
        OUTLET_LAT = 38.97594
        OUTLET_LON = -77.24581

        sites = pd.read_csv(DATA_DIR / "sites.csv", dtype={"gage_number": str})
        display(
            sites[
                [
                    "watershed", "name", "gage_number", "drainage_area_sqmi",
                    "sample_lat", "sample_lon", "physiography",
                ]
            ]
        )

        if WATERSHED_INPUT == "reference":
            match = sites.loc[sites.watershed == REFERENCE_WATERSHED]
            if len(match) != 1:
                raise ValueError(
                    "REFERENCE_WATERSHED must be 'difficult_run' or 'accotink_creek'"
                )
            selected = match.iloc[0]
            WATERSHED_CONFIG = {
                "input": "reference",
                "watershed": selected.watershed,
                "name": selected["name"],
                "gage": selected.gage_number,
                "latitude": float(selected.sample_lat),
                "longitude": float(selected.sample_lon),
            }
        elif WATERSHED_INPUT == "gage":
            gage = str(SELECTED_GAGE).strip()
            if not (gage.isdigit() and len(gage) == 8):
                raise ValueError("SELECTED_GAGE must contain eight digits")
            WATERSHED_CONFIG = {"input": "gage", "gage": gage}
        elif WATERSHED_INPUT == "outlet":
            latitude = float(OUTLET_LAT)
            longitude = float(OUTLET_LON)
            if not (24.0 <= latitude <= 50.0 and -125.0 <= longitude <= -66.0):
                raise ValueError("Outlet coordinates must fall within CONUS bounds")
            WATERSHED_CONFIG = {
                "input": "outlet",
                "latitude": latitude,
                "longitude": longitude,
            }
        else:
            raise ValueError(
                "WATERSHED_INPUT must be 'reference', 'gage', or 'outlet'"
            )

        WATERSHED_SELECTION_READY = True
        print("Selected watershed configuration")
        print(pd.Series(WATERSHED_CONFIG).to_string())
        '''),
        md(r'''
        ## Step 6 — Review the readiness record

        The final cell distinguishes the common computational requirements from
        the Earth Engine project check. A verified core calculation, reference
        data bundle, and watershed selection support the full reference-data
        analysis. The Earth Engine status records whether the selected project
        was checked during this session.
        '''),
        code(r'''
        readiness = pd.DataFrame(
            [
                ["core calculation", "verified" if CORE_CALCULATION_READY else "review"],
                ["reference data", "verified" if REFERENCE_DATA_READY else "review"],
                ["watershed selection", "verified" if WATERSHED_SELECTION_READY else "review"],
                ["Earth Engine project", EARTH_ENGINE_STATUS],
            ],
            columns=["component", "status"],
        )
        display(readiness)

        assert CORE_CALCULATION_READY
        assert REFERENCE_DATA_READY
        assert WATERSHED_SELECTION_READY
        print("Readiness check complete. Continue to the common workshop introduction.")
        '''),
    ]
    return notebook("00 Readiness Check", "pre-work", cells)


def build_lab1():
    cells = [
        md(r'''
        # Lab 1 — Understand the curve number

        **Twenty minutes.** This lab establishes the theoretical and numerical
        framework used by both spatial-data pathways.

        The guided analysis is organized into eight explicit steps:

        1. define the event water-balance model;
        2. translate curve number to retention and initial abstraction;
        3. evaluate the piecewise runoff equation;
        4. compare distributed and lumped watershed representations;
        5. examine how the compositing difference varies with storm depth;
        6. treat lambda and curve number as a paired calibration;
        7. invert observed rainfall and runoff to event curve numbers; and
        8. fit and interpret an asymptotic curve number.

        Each step states the theoretical purpose, shows the intermediate
        quantities, explains the corresponding `cnkit` operation, and ends with
        the interpretation expected from the participant. During the
        twenty-minute laboratory, prioritize the code cells and retain the
        surrounding material as a technical reference.
        '''),
        code(SETUP),
        code(r'''
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        from cnkit import (
            CN_from_PQ,
            S_from_CN,
            cn05_from_cn20,
            composite_runoff,
            fit_asymptotic,
            runoff,
        )
        '''),
        md(r'''
        ## Step 1 — Define the event water-balance model

        The curve-number method is an event-scale, lumped rainfall–runoff
        relation. For rainfall depth $P$, direct-runoff depth $Q$, potential
        maximum retention $S$, and initial abstraction $I_a$, the standard
        equations in inch units are

        $$
        S = \frac{1000}{CN} - 10,
        \qquad I_a = \lambda S,
        $$

        $$
        Q = \begin{cases}
        0, & P \le I_a,\\[4pt]
        \dfrac{(P-I_a)^2}{P+(1-\lambda)S}, & P>I_a.
        \end{cases}
        $$

        A curve number is therefore a dimensionless transformation of $S$;
        it is not a directly observed land-surface property. Larger CN implies
        smaller retention, a smaller rainfall threshold, and greater runoff for
        the same event. The conventional value $\lambda=0.20$ specifies the
        assumed fraction of retention that must be satisfied before runoff
        begins.
        '''),
        md(r'''
        ## Step 2 — Translate CN into retention and initial abstraction

        **Why this step is needed.** CN is used by the runoff equation only
        after it has been transformed to retention. Displaying retention and
        the abstraction threshold makes the physical consequence of a CN
        choice visible before runoff is calculated.

        **How the library performs it.** `S_from_CN` converts its input to a
        numeric array, checks that every curve number is in the interval
        $0<CN\leq100$, and applies $1000/CN-10$ element by element. It does
        not assign lambda, so the notebook calculates $I_a=\lambda S$
        explicitly.

        **What to inspect.** Compare the change in retention with the change in
        CN. The transformation is nonlinear: a ten-unit CN change does not
        represent a constant change in storage across the CN range.
        '''),
        code(r'''
        curve_numbers = np.array([55, 70, 85, 98], dtype=float)
        retention = S_from_CN(curve_numbers)
        theory_table = pd.DataFrame(
            {
                "curve_number": curve_numbers,
                "retention_S_in": retention,
                "initial_abstraction_Ia_in": 0.20 * retention,
            }
        )
        theory_table.round(3)
        '''),
        md(r'''
        **Interpretation.** The threshold is mathematically consequential. At CN 70 and
        $\lambda=0.20$, $I_a$ is approximately 0.86 inches; an event below
        that depth produces zero direct runoff in the model. This is a model
        statement, not a claim that no water moves within the watershed.
        '''),
        md(r'''
        ## Step 3 — Evaluate and verify the runoff equation

        **Why this step is needed.** Reproducing a library result from the
        published equation confirms the units, threshold convention, and
        numerical interpretation before the method is applied spatially.

        **How the library performs it.** `cnkit.runoff` validates rainfall, CN,
        and lambda; broadcasts compatible scalar or array inputs; calculates
        $S$ and $I_a$; and uses a piecewise mask to return zero where
        $P\leq I_a$. For the remaining elements it evaluates the rational
        runoff equation. The library does not select CN, lambda, rainfall, or
        the spatial unit of analysis.
        '''),
        code(r'''
        def runoff_written_out(P, cn, lam=0.20):
            P = np.asarray(P, dtype=float)
            S = 1000.0 / float(cn) - 10.0
            Ia = lam * S
            return np.where(P > Ia, (P - Ia) ** 2 / (P + (1.0 - lam) * S), 0.0)

        storms_check = np.array([0.50, 1.00, 2.00, 4.00])
        by_equation = runoff_written_out(storms_check, 70, lam=0.20)
        by_library = runoff(storms_check, 70, lam=0.20)
        verification = pd.DataFrame(
            {
                "P_in": storms_check,
                "Q_equation_in": by_equation,
                "Q_cnkit_in": by_library,
                "absolute_difference": np.abs(by_equation - by_library),
            }
        )
        assert np.allclose(by_equation, by_library)
        verification.round(6)
        '''),
        md(r'''
        **Interpretation.** The assertion checks every storm depth numerically.
        Values below the threshold should be exactly zero, and the remaining
        values should agree to floating-point precision. This establishes that
        later differences arise from parameter or spatial choices rather than a
        second equation.
        '''),
        md(r'''
        ## Step 4 — Compare distributed and lumped watershed representations

        The runoff equation is nonlinear in CN because CN is first transformed
        to $S$, enters both the threshold and denominator, and appears inside
        a squared numerator. Consequently,

        $$
        Q\!\left(P,\sum_i w_i CN_i\right)
        \ne \sum_i w_i Q(P,CN_i)
        $$

        in general. The left side is a lumped calculation; the right side
        computes runoff for each hydrologically distinct subarea and then
        aggregates runoff volume. Both are reproducible calculations, but they
        represent different spatial models.

        Sixty percent connected impervious cover at CN 98 is combined with
        forty percent woods at CN 55 under a one-inch storm. `composite_runoff`
        returns three results in a fixed order:

        1. runoff by subarea, subsequently area weighted;
        2. CN area weighted first, followed by one runoff calculation; and
        3. retention $S$ area weighted first, converted back to CN, followed
           by one runoff calculation.

        **How the library performs it.** The function validates that CN and
        area arrays are finite, positive, and equal in length; normalizes area
        to weights; calls `runoff` on each subarea; and calculates the weighted
        sum of runoff. It then calls `composite_cn` and
        `composite_cn_via_S` to produce the two lumped comparisons. The return
        order is distributed runoff, runoff from weighted CN, and runoff from
        weighted retention.
        '''),
        code(r'''
        P_weighting = 1.0
        subarea_cn = np.array([98.0, 55.0])
        subarea_fraction = np.array([0.60, 0.40])

        q_distributed, q_weighted_cn, q_weighted_s = composite_runoff(
            P_weighting, subarea_cn, subarea_fraction
        )

        subarea_detail = pd.DataFrame(
            {
                "description": ["connected impervious", "woods on HSG B"],
                "area_fraction": subarea_fraction,
                "CN": subarea_cn,
                "S_in": S_from_CN(subarea_cn),
                "Ia_in": 0.20 * S_from_CN(subarea_cn),
                "subarea_Q_in": runoff(P_weighting, subarea_cn),
            }
        )
        subarea_detail["runoff_contribution_in"] = (
            subarea_detail.area_fraction * subarea_detail.subarea_Q_in
        )
        subarea_detail.round(4)
        '''),
        code(r'''
        weighting = pd.Series(
            {
                "runoff by subarea, then area-weight": q_distributed,
                "area-weight CN, then compute runoff": q_weighted_cn,
                "area-weight S, then compute runoff": q_weighted_s,
            },
            name="runoff_inches",
        )
        print(weighting.round(4))
        print("distributed / weighted-CN ratio: %.1f" % (q_distributed / q_weighted_cn))
        '''),
        md(r'''
        **Interpretation.** The wooded subarea remains below its
        initial-abstraction threshold while the impervious subarea is already
        producing runoff. A lumped parameter removes that threshold contrast
        before the nonlinear equation is evaluated. This explains why the
        difference is largest for smaller storms and heterogeneous watersheds.
        '''),
        md(r'''
        ## Step 5 — Examine how compositing depends on storm depth

        **Why this step is needed.** A single design storm shows one point on a
        nonlinear response. Repeating the same three spatial representations
        across rainfall depths reveals whether their difference is structural
        or specific to the selected storm.

        **How the library performs it.** The notebook calls
        `composite_runoff` once per rainfall depth while keeping CN values,
        areas, and lambda fixed. Only $P$ changes. Each plotted line therefore
        represents one compositing convention under otherwise identical input.
        '''),
        code(r'''
        storms = np.linspace(0.25, 6.0, 48)
        values = np.array(
            [composite_runoff(p, subarea_cn, subarea_fraction) for p in storms]
        )

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.plot(storms, values[:, 0], lw=2.5, label="distributed runoff")
        ax.plot(storms, values[:, 1], lw=2, label="weighted CN")
        ax.plot(storms, values[:, 2], lw=2, label="weighted S")
        ax.set(xlabel="storm depth, inches", ylabel="runoff depth, inches")
        ax.grid(alpha=0.25)
        ax.legend()
        plt.show()
        '''),
        md(r'''
        **Interpretation.** Near the abstraction thresholds, some subareas
        produce runoff while others do not, so early parameter aggregation has
        its greatest effect. With larger storms, every subarea contributes and
        the relative separation generally decreases. Record both storm depth
        and spatial convention when reporting the comparison.
        '''),
        md(r'''
        ## Step 6 — Treat lambda and CN as a paired calibration

        Lambda is not an independent switch applied after CN has been selected.
        Event-derived and table-derived curve numbers are conditional on the
        lambda used in the runoff equation. A CN calibrated with
        $\lambda=0.20$ should therefore be converted or refitted before it is
        used with $\lambda=0.05$.

        `cn05_from_cn20` implements the Woodward et al. (2003) empirical
        conversion. The converted CN is numerically lower because the smaller
        initial-abstraction ratio permits runoff to begin earlier. Similar
        runoff response—not equal CN—is the comparison to make.

        Difficult Run has a 2019 table composite near 75.5 and a fitted
        asymptotic value of 69.7. The lambda conversion below is a third number:
        it describes the same response convention under lambda 0.05 rather than
        0.20.

        **How the library performs it.** `cn05_from_cn20` applies the published
        empirical conversion to each validated CN value. This is a parameter
        conversion, not a second runoff calculation. The notebook then calls
        `runoff` with each CN–lambda pair at the same storm depth so that the
        resulting response can be compared on a common basis.
        '''),
        code(r'''
        P = 3.0
        table_cn20 = 75.5
        fitted_cn20 = 69.7
        table_cn05 = float(cn05_from_cn20(table_cn20))

        comparison = pd.DataFrame(
            [
                ["table", 0.20, table_cn20, float(runoff(P, table_cn20, lam=0.20))],
                ["fitted to gage", 0.20, fitted_cn20, float(runoff(P, fitted_cn20, lam=0.20))],
                ["same table response, converted", 0.05, table_cn05, float(runoff(P, table_cn05, lam=0.05))],
            ],
            columns=["basis", "lambda", "curve_number", "runoff_in"],
        )
        comparison.round(4)
        '''),
        md(r'''
        **Interpretation.** The three rows have different evidentiary bases: a
        spatial lookup, a rainfall–runoff fit, and a conversion between
        equation conventions. They should be labelled accordingly rather than
        described as competing measurements of one fixed property.
        '''),
        md(r'''
        ## Step 7 — Invert observed rainfall and runoff to event curve numbers

        For an observed event pair $(P,Q)$, `CN_from_PQ` algebraically inverts
        the same runoff equation for a specified lambda. Each valid event
        produces an event-derived CN. These values vary with storm depth,
        antecedent state, measurement error, and model adequacy; the variation
        is information rather than a reason to average immediately.

        **How the library performs it.** `CN_from_PQ` broadcasts rainfall and
        runoff arrays, identifies physically admissible events, solves the
        quadratic relation for retention, and transforms retention to CN. An
        event receives `NaN` when the inputs do not support a physical inverse,
        such as non-positive runoff or runoff exceeding rainfall. Lambda is an
        explicit argument because it changes the inverse solution.
        '''),
        code(r'''
        events = pd.read_csv(DATA_DIR / "events_01646000.csv")
        events["event_CN"] = CN_from_PQ(
            events.P_in.values, events.Q_in.values, lam=0.20
        )
        events["valid_inverse"] = np.isfinite(events.event_CN)

        print("event records:       ", len(events))
        print("valid inverse events:", int(events.valid_inverse.sum()))
        events[
            ["P_in", "Q_in", "runoff_ratio", "event_CN", "valid_inverse"]
        ].head(12).round(3)
        '''),
        md(r'''
        **Interpretation.** Event CN is derived from measured quantities under
        a specified model convention. The event table should therefore retain
        rainfall, runoff, runoff ratio, lambda, and validity status beside the
        transformed value.
        '''),
        md(r'''
        ## Step 8 — Fit and interpret an asymptotic curve number

        `fit_asymptotic` then fits the standard relation described by
        [Hawkins (1993)](https://doi.org/10.1061/%28ASCE%290733-9437%281993%29119%3A2%28334%29):

        $$
        CN(P)=CN_{\infty}+(100-CN_{\infty})e^{-kP}
        $$

        by nonlinear least squares. $CN_{\infty}$ is the large-storm
        asymptote, $k$ controls the rate of approach, and $R^2$ describes
        how much of the event-CN variation is explained by this specific
        functional form. The fit does not establish that the watershed has a
        unique physical CN.

        **How the library performs it.** The function calls `CN_from_PQ`,
        retains finite event values, checks that the requested minimum event
        count is available, and uses bounded nonlinear least squares to
        estimate $CN_{\infty}$ and $k$. It returns a structured result with
        the model name, coefficients, event count, RMSE, and $R^2$. Its
        `predict` method evaluates the selected fitted model at new rainfall
        depths.
        '''),
        code(r'''
        fit = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.20)

        valid = events.valid_inverse.values
        p_line = np.linspace(events.P_in.min(), events.P_in.max(), 200)
        fitted_line = fit.predict(p_line)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.scatter(events.P_in.values[valid], events.event_CN.values[valid], s=12, alpha=0.25,
                   label="event-derived CN")
        ax.plot(p_line, fitted_line, color="#b24d35", lw=2.5,
                label="Hawkins standard fit")
        ax.axhline(table_cn20, color="#17274f", ls="--", lw=1.8,
                   label="2019 table composite")
        ax.set(xlabel="event rainfall P, inches", ylabel="event-derived curve number")
        ax.set_ylim(0, 102)
        ax.grid(alpha=0.2)
        ax.legend()
        plt.show()

        print("event records:", len(events))
        print("events fitted:", fit.n_events)
        print("CN infinity:   %.3f" % fit.cn_inf)
        print("decay k:       %.3f" % fit.k)
        print("R squared:     %.3f" % fit.r2)
        '''),
        md(r'''
        **Interpretation.** Compare the event cloud, fitted curve, table value,
        fitted event count, and diagnostics together. A numerical asymptote is
        meaningful only to the extent that the selected response form is
        supported over the observed rainfall range.
        '''),
        md(r'''
        ## Method audit — Library operation and analyst decision

        | Call | Library operation | Analyst responsibility |
        |---|---|---|
        | `S_from_CN` | Applies the CN-to-retention transformation | Establish the basis and scale of CN |
        | `runoff` | Applies the piecewise event equation | Select $P$, CN, lambda, and spatial representation |
        | `composite_runoff` | Returns distributed, weighted-CN, and weighted-S calculations | Choose and justify the compositing convention |
        | `cn05_from_cn20` | Applies the published empirical parameter conversion | Keep the converted CN paired with lambda 0.05 |
        | `CN_from_PQ` | Inverts the event equation | Verify rainfall, direct-runoff separation, and event selection |
        | `fit_asymptotic` | Fits a named CN-versus-rainfall model | Evaluate fit adequacy and interpretability |

        The library makes the transformations reproducible; it does not make
        the scientific choices interchangeable.
        '''),
        md(r'''
        ## Report-out

        Bring back:

        1. The three runoff depths from the weighting example.
        2. Which convention you would report for a heterogeneous watershed.
        3. One sentence explaining why lambda must be reported with CN.
        4. One sentence distinguishing the table composite from
           $CN_{\infty}$.

        **Source anchors:** NEH-630 Chapter 10 equations 10-1 and 10-11;
        TR-55 Worksheet 2; Woodward et al. (2003),
        [doi:10.1061/40685(2003)308](https://doi.org/10.1061/40685%282003%29308);
        Hawkins (1993),
        [doi:10.1061/(ASCE)0733-9437(1993)119:2(334)](https://doi.org/10.1061/%28ASCE%290733-9437%281993%29119%3A2%28334%29).
        '''),
    ]
    return notebook("01 Understand the Curve Number", "lab 1", cells)


def build_lab2():
    cells = [
        md(r'''
        # Lab 2 — Build a curve number for a watershed

        **Thirty-five minutes.**

        This notebook separates the spatial workflow into the operations that
        are often hidden inside a single composite-CN function:

        1. identify the watershed outlet;
        2. delineate and verify the watershed boundary;
        3. establish the Earth Engine session when that application is selected;
        4. obtain land-cover and impervious-surface distributions;
        5. obtain hydrologic soil groups;
        6. construct the land-cover–soil joint distribution;
        7. apply the curve-number lookup by spatial unit;
        8. aggregate the local values and state the weighting convention; and
        9. calculate runoff and assemble provenance.

        The reference-data pathway executes the same analytical sequence with
        verified tables for Difficult Run or Accotink Creek. The Earth Engine
        application replaces the marginal tables with pixelwise spatial
        measurements for a selected watershed.

        Each numbered step states why the operation is needed, describes how
        the relevant library layer performs it, exposes the intermediate table
        or geometry, and identifies the result that should be interpreted.
        '''),
        code(SETUP),
        code(r'''
        import json
        import warnings
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from IPython.display import display

        from cnkit import composite_from_areas, runoff

        # Change to "accotink_creek" for the second verified reference basin.
        PREPARED_WATERSHED = "difficult_run"
        ANALYSIS_YEAR = 2019
        HYDROLOGIC_CONDITION = "fair"
        SOILS_SOURCE = "sda"

        # Set True only when the readiness check has already passed.
        USE_EARTH_ENGINE = False
        ADD_BACKGROUND_MAP = True

        # The outlet route produces a split catchment at the supplied point.
        # The gage route produces the NHDPlus aggregated upstream catchment.
        DELINEATION_INPUT = "outlet"  # "outlet" or "gage"
        GAGE = "01646000"
        LAT, LON = 38.97594, -77.24581
        '''),
        md(r'''
        ## The analytical data flow

        | Stage | Reference-data pathway | Earth Engine application | `cnkit` layer |
        |---|---|---|---|
        | Boundary | Verified workshop GeoJSON and site metadata | USGS NLDI or SS-Delineate | `cnkit.delineate` |
        | Land cover | EPA StreamCat watershed percentages | Annual NLCD frequency histogram | `cnkit.gee.Basin.landcover` |
        | Soils | NRCS Soil Data Access percentages | gNATSGO map-unit raster plus Soil Data Access lookup | `cnkit.gee.Basin.soil_groups` |
        | Pairing | Product of marginal percentages | Pixelwise joint frequency histogram | `cnkit.gee.Basin.joint_landcover_soils` |
        | CN lookup | TR-55/NEH-630 table indexed by NLCD and HSG | Same lookup table | `cnkit.lookup` |
        | Composite | Area-weighted CN and area-weighted S | Same calculation | `cnkit.lookup.composite_from_areas` |

        The hydrologic arithmetic is shared. Earth Engine changes how the
        spatial area table is measured; it does not introduce a second
        curve-number equation.
        '''),
        gee_data_source_register(),
        md(r'''
        ## Step 1 — Identify the watershed and outlet

        A watershed analysis begins with an outlet definition, not with a land-
        cover raster. The outlet fixes the contributing area and therefore the
        denominator of every percentage calculated later.

        The workshop metadata distinguish the **gage coordinate**, where all
        point data and Atlas 14 depths were sampled, from the **basin centroid**,
        which is descriptive and should not be used as the pour point.
        '''),
        code(r'''
        sites = pd.read_csv(DATA_DIR / "sites.csv", dtype={"gage_number": str})
        site = sites.loc[sites.watershed == PREPARED_WATERSHED].iloc[0]
        boundaries = json.loads((DATA_DIR / "basins.geojson").read_text())
        reference_feature = boundaries[PREPARED_WATERSHED]["features"][0]

        site_summary = pd.Series(
            {
                "watershed": site["name"],
                "USGS gage": site["gage_number"],
                "published drainage area, sq mi": site["drainage_area_sqmi"],
                "gage latitude": site["sample_lat"],
                "gage longitude": site["sample_lon"],
                "basin centroid latitude": site["centroid_lat"],
                "basin centroid longitude": site["centroid_lon"],
            }
        )
        site_summary
        '''),
        md(r'''
        ## Step 2 — Delineate the watershed boundary

        `cnkit` supports two scientifically distinct USGS routes.

        **Outlet-coordinate route — `watershed_from_point(lat, lon)`**

        1. The coordinate is validated in latitude–longitude order.
        2. USGS NLDI `hydrolocation` snaps the point to an NHDPlusV2 flowline.
        3. The snapped coordinate is submitted to the NLDI split-catchment
           process with upstream tracing enabled.
        4. If that route is unavailable, `method="auto"` tries USGS
           SS-Delineate.
        5. The returned polygon area is recomputed from its coordinates and
           compared with a minimum-area guard before a `Watershed` is returned.

        **Gage route — `watershed_from_gage(gage)`**

        NLDI resolves the gage identifier and returns the aggregated upstream
        NHDPlusV2 catchment. It is convenient and reproducible, but it ends at a
        catchment boundary rather than splitting the outlet catchment at the
        exact gage coordinate. For Difficult Run this distinction is about one
        NHDPlus catchment: approximately 58.15 square miles from the gage route
        versus 57.82 square miles from the split-catchment route and 57.8 square
        miles in the published gage metadata.

        The live code is deliberately separate from Earth Engine
        authentication: delineation is a USGS web-service operation and does
        not use Earth Engine.
        '''),
        code(r'''
        live_watershed = None

        if USE_EARTH_ENGINE:
            activate_full_cnkit()
            from cnkit.delineate import watershed_from_gage, watershed_from_point

            if DELINEATION_INPUT == "outlet":
                live_watershed = watershed_from_point(LAT, LON, method="auto")
            elif DELINEATION_INPUT == "gage":
                live_watershed = watershed_from_gage(GAGE)
            else:
                raise ValueError("DELINEATION_INPUT must be 'outlet' or 'gage'")

            print(live_watershed)
            print("method:       ", live_watershed.method)
            print("source:       ", live_watershed.source_dataset)
            print("area, sq mi:  ", round(live_watershed.area_sqmi, 3))
            print("request point:", live_watershed.request_point)
            print("snapped point:", live_watershed.snapped_point)
            print("warnings:     ", live_watershed.warnings)
        else:
            print("Reference boundary selected:", site["name"])
            print("Set USE_EARTH_ENGINE=True to delineate the selected outlet live.")
        '''),
        md(r'''
        ## Step 3 — Verify and inspect the boundary

        Boundary verification is an analytical step. At minimum, compare the
        computed area with an independent published drainage area, inspect the
        outlet position, and retain the delineation method and warnings.

        The reference boundary below is a compact workshop geometry for visual
        inspection. The recorded Earth Engine result also retains the full
        NLDI split-catchment area and vertex count used in the live analysis.

        The map requests the public **USGS Topo** basemap from The National Map.
        It provides geographic names, transportation, hydrography, elevation,
        land cover, and administrative context beneath the analytical boundary.
        The basemap is cartographic context only; it is not used to calculate
        area, land cover, soils, or curve number. Source:
        [USGS National Map basemap services](https://www.usgs.gov/faqs/what-are-base-map-services-or-urls-used-national-map).
        '''),
        code(r'''
        recorded = None
        if PREPARED_WATERSHED == "difficult_run":
            recorded = json.loads(
                (PREPARED_DIR / "difficult_run_gee_summary.json").read_text()
            )

        if live_watershed is not None:
            delineated_area = live_watershed.area_sqmi
            delineation_method = live_watershed.method
        elif recorded is not None:
            delineated_area = recorded["watershed"]["area_sqmi"]
            delineation_method = recorded["watershed"]["delineation"]
        else:
            delineated_area = float(site["drainage_area_sqmi"])
            delineation_method = "verified workshop boundary"

        area_check = pd.Series(
            {
                "published area, sq mi": float(site["drainage_area_sqmi"]),
                "delineated area, sq mi": delineated_area,
                "difference, sq mi": delineated_area - float(site["drainage_area_sqmi"]),
                "difference, percent": 100.0 * (
                    delineated_area / float(site["drainage_area_sqmi"]) - 1.0
                ),
                "method": delineation_method,
            }
        )
        area_check
        '''),
        code(r'''
        import io
        import urllib.parse
        import urllib.request

        from PIL import Image
        from matplotlib.ticker import FormatStrFormatter, MaxNLocator

        def add_usgs_topo_basemap(ax, bounds):
            """Draw a USGS Topo export beneath EPSG:4326 analytical layers."""
            west, south, east, north = bounds
            parameters = {
                "bbox": ",".join(str(value) for value in bounds),
                "bboxSR": 4326,
                "imageSR": 4326,
                "size": "1000,800",
                "format": "png32",
                "transparent": "false",
                "f": "image",
            }
            endpoint = (
                "https://basemap.nationalmap.gov/arcgis/rest/services/"
                "USGSTopo/MapServer/export"
            )
            request = urllib.request.Request(
                endpoint + "?" + urllib.parse.urlencode(parameters),
                headers={"User-Agent": "cn-workshop-2026"},
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    image = Image.open(io.BytesIO(response.read())).convert("RGB")
                ax.imshow(
                    np.asarray(image),
                    extent=(west, east, south, north),
                    interpolation="bilinear",
                    zorder=0,
                    aspect="auto",
                )
                return "USGS Topo loaded"
            except Exception as exc:
                ax.set_facecolor("#eef1ec")
                return "USGS Topo request noted: %s" % type(exc).__name__


        geometry_for_plot = (
            live_watershed.geojson["geometry"]
            if live_watershed is not None
            else reference_feature["geometry"]
        )
        rings = (
            geometry_for_plot["coordinates"]
            if geometry_for_plot["type"] == "Polygon"
            else [ring for polygon in geometry_for_plot["coordinates"] for ring in polygon]
        )

        coordinate_arrays = [np.asarray(ring, dtype=float) for ring in rings]
        all_coordinates = np.vstack(coordinate_arrays)
        west, south = all_coordinates.min(axis=0)
        east, north = all_coordinates.max(axis=0)
        longitude_padding = max((east - west) * 0.12, 0.01)
        latitude_padding = max((north - south) * 0.12, 0.01)
        map_bounds = (
            west - longitude_padding,
            south - latitude_padding,
            east + longitude_padding,
            north + latitude_padding,
        )

        fig, ax = plt.subplots(figsize=(8.2, 6.4))
        basemap_status = (
            add_usgs_topo_basemap(ax, map_bounds)
            if ADD_BACKGROUND_MAP
            else "background map disabled"
        )
        for coordinates in coordinate_arrays:
            ax.fill(
                coordinates[:, 0], coordinates[:, 1],
                color="#38a3a5", alpha=0.18, zorder=2,
            )
            ax.plot(
                coordinates[:, 0], coordinates[:, 1],
                color="#17274f", lw=2.0, zorder=3,
            )

        marker_lat_lon = None
        if live_watershed is not None:
            marker_lat_lon = live_watershed.snapped_point or live_watershed.request_point
        if marker_lat_lon is None and (
            live_watershed is None or str(GAGE) == str(site["gage_number"])
        ):
            marker_lat_lon = (float(site["sample_lat"]), float(site["sample_lon"]))
        if marker_lat_lon is not None:
            marker_lat, marker_lon = marker_lat_lon
            ax.plot(
                marker_lon, marker_lat, "o", ms=7,
                color="#b24d35", markeredgecolor="white", markeredgewidth=1.2,
                label="gage / outlet", zorder=4,
            )

        map_title = (
            site["name"]
            if live_watershed is None
            else "Selected watershed — %s" % live_watershed.method
        )
        ax.set(
            xlim=(map_bounds[0], map_bounds[2]),
            ylim=(map_bounds[1], map_bounds[3]),
            xlabel="longitude",
            ylabel="latitude",
            title=map_title,
        )
        center_latitude = (map_bounds[1] + map_bounds[3]) / 2.0
        ax.set_aspect(1.0 / np.cos(np.deg2rad(center_latitude)))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.annotate(
            "N", xy=(0.965, 0.94), xytext=(0.965, 0.85),
            xycoords="axes fraction", textcoords="axes fraction",
            ha="center", va="center", fontsize=9, fontweight="bold",
            arrowprops={"arrowstyle": "-|>", "color": "#17274f", "lw": 1.4},
            zorder=5,
        )
        ax.text(
            0.99, 0.01, "Basemap: USGS The National Map — USGS Topo",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7,
            color="#17274f", bbox={"facecolor": "white", "alpha": 0.78, "edgecolor": "none"},
            zorder=5,
        )
        if marker_lat_lon is not None:
            ax.legend()
        ax.grid(alpha=0.16, color="#54636f")
        print("background map:", basemap_status)
        plt.show()
        '''),
        md(r'''
        ## Step 4 — Initialize Earth Engine and bind the boundary

        Earth Engine authentication and watershed delineation are independent.
        After authentication, `cnkit.gee.Basin` converts the verified GeoJSON
        geometry to an Earth Engine geometry and stores the analysis scale,
        pixel limit, soil-drainage convention, request cache, and project
        context. Constructing `Basin` does not yet reduce a raster.
        '''),
        code(r'''
        basin = None
        project = None

        if USE_EARTH_ENGINE:
            import os
            from getpass import getpass
            import ee
            from cnkit.gee import Basin, initialise

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass(
                "Earth Engine project ID: "
            )
            ee.Authenticate()
            initialise(project=project)
            basin = Basin(live_watershed, project=project)
            print("Earth Engine basin ready at", basin.scale, "m analysis scale")
        else:
            print("Reference-data pathway active; Earth Engine initialization is not used.")
        '''),
        md(r'''
        ## Step 5 — Measure land cover

        The reference pathway reads EPA StreamCat watershed percentages. The
        Earth Engine pathway calls `Basin.landcover`, which selects the requested
        Annual NLCD image, clips it to the boundary, and applies one frequency-
        histogram reduction. One histogram returns all classes in one request;
        class-by-class masks would repeat the same spatial reduction.

        The percentages include recognized classes and NoData so their
        denominator remains the full analysis area. `Basin.impervious` is a
        separate reduction of the fractional impervious product; developed
        class percentage and impervious percentage are not interchangeable.
        '''),
        code(r'''
        landcover_all = pd.read_csv(DATA_DIR / "landcover_streamcat.csv")
        reference_landcover = landcover_all[
            (landcover_all.watershed == PREPARED_WATERSHED)
            & (landcover_all.year == ANALYSIS_YEAR)
        ][["nlcd", "pct"]].copy()

        live_landcover = None
        live_impervious_pct = None
        if basin is not None:
            live_landcover = basin.landcover(years=[ANALYSIS_YEAR])[
                ["nlcd", "pct"]
            ].copy()
            live_impervious_pct = basin.impervious(ANALYSIS_YEAR)
            print("Live Annual NLCD distribution")
            display(live_landcover.sort_values("pct", ascending=False).head(12))
            print("mean impervious surface: %.2f %%" % live_impervious_pct)
        else:
            print("Reference StreamCat distribution")
            display(reference_landcover.sort_values("pct", ascending=False).head(12))

        print("land-cover percentage sum:", round(
            float((live_landcover if live_landcover is not None else reference_landcover).pct.sum()), 4
        ))
        '''),
        md(r'''
        ## Step 6 — Measure hydrologic soil group

        Hydrologic soil group (HSG) summarizes infiltration and transmission
        behavior used by the lookup tables. The soil source is a required
        argument in `cnkit`; the library does not choose one implicitly.

        With `soils="sda"`, Earth Engine supplies the 30 m gNATSGO map-unit-key
        raster. `cnkit` extracts only the map-unit keys present in the basin and
        resolves those integers to the dominant-condition HSG through one USDA
        Soil Data Access query. This avoids sending thousands of SSURGO polygons
        into Earth Engine. Dual groups retain their `A/D`, `B/D`, or `C/D`
        designation, and map units without an HSG remain explicitly unmapped.
        '''),
        code(r'''
        soils_all = pd.read_csv(DATA_DIR / "soils_hsg.csv", keep_default_na=False)
        reference_soils = soils_all[
            soils_all.watershed == PREPARED_WATERSHED
        ][["hsg", "pct"]].copy()

        live_soils = None
        if basin is not None:
            live_soils = basin.soil_groups(soils=SOILS_SOURCE)
            print("Live soil distribution")
            display(live_soils)
        else:
            print("Reference Soil Data Access distribution")
            display(reference_soils)

        soil_table_used = live_soils if live_soils is not None else reference_soils
        unmapped_soil_pct = float(
            soil_table_used.loc[
                soil_table_used.hsg.isin(["", "(none mapped)"]), "pct"
            ].sum()
        )
        print("soil percentage sum:       %.4f" % soil_table_used.pct.sum())
        print("area with no mapped HSG:   %.2f %%" % unmapped_soil_pct)
        '''),
        md(r'''
        ## Step 7 — Construct land-cover–soil pairs

        StreamCat supplies land-cover percentages and Soil Data Access supplies
        soil-group percentages. Crossing those two marginal tables assumes they
        are statistically independent:

        $$
        A_{ij}=A\,p(LC_i)\,p(HSG_j).
        $$

        The reference pathway performs that product explicitly. Earth Engine
        instead observes the joint distribution by packing each pixel's land-
        cover and soil codes into one integer band, applying one frequency
        histogram, decoding the pairs, and converting counts to percentages.
        The joint table is the principal spatial contribution: it retains which
        combinations actually coexist rather than reconstructing them from two
        separate summaries.
        '''),
        code(r'''
        def cross_marginals(lc, sg, area_column="area"):
            lc = lc.copy()
            sg = sg.copy()
            lc["key"], sg["key"] = 1, 1
            crossed = lc.merge(sg, on="key", suffixes=("_lc", "_soil"))
            crossed[area_column] = crossed.pct_lc * crossed.pct_soil / 100.0
            return crossed[["nlcd", "hsg", area_column]]

        reference_pairs = cross_marginals(reference_landcover, reference_soils)
        live_pairs = (
            basin.joint_landcover_soils(ANALYSIS_YEAR, soils=SOILS_SOURCE)
            if basin is not None
            else None
        )

        analysis_pairs = live_pairs if live_pairs is not None else reference_pairs
        analysis_area_column = "pct" if live_pairs is not None else "area"

        print("reference independence cross rows:", len(reference_pairs))
        if live_pairs is not None:
            print("observed joint-distribution rows:", len(live_pairs))
        print("analysis area sum:", round(float(analysis_pairs[analysis_area_column].sum()), 4))
        display(analysis_pairs.sort_values(analysis_area_column, ascending=False).head(12))
        '''),
        md(r'''
        ## Step 8 — Apply the lookup to each pair

        `cnkit.lookup.cn_lookup` indexes the selected hydrologic-condition row
        using NLCD class and HSG. A local curve number is attached to each area
        row before aggregation. Unrecognized land-cover classes and unmapped
        soil groups remain `NaN`; their area is counted and reported instead of
        being silently removed from the denominator.

        Hydrologic condition—poor, fair, or good—is a table selection based on
        cover density, residue, grazing, compaction, and related field
        attributes. It is not inferred from the NLCD class itself.
        '''),
        code(r'''
        lookup_detail = analysis_pairs.copy()
        lookup_detail["curve_number"] = cnkit.cn_lookup(
            lookup_detail.nlcd.values,
            lookup_detail.hsg.values,
            condition=HYDROLOGIC_CONDITION,
        )
        lookup_detail["CN_contribution"] = (
            lookup_detail[analysis_area_column] * lookup_detail.curve_number / 100.0
        )
        display(
            lookup_detail.sort_values("CN_contribution", ascending=False).head(15).round(4)
        )
        print("mapped pairs:  ", int(lookup_detail.curve_number.notna().sum()))
        print("unmapped pairs:", int(lookup_detail.curve_number.isna().sum()))
        '''),
        md(r'''
        ## Step 9 — Aggregate and state the convention

        `composite_from_areas` performs the same lookup shown above and returns
        two lumped parameters:

        - `cn_weighted_CN`: area-weight local CN values, following the TR-55
          Worksheet 2 procedure;
        - `cn_weighted_S`: transform each local CN to retention, area-weight
          retention, and convert the result back to CN.

        The function also reports the fraction of the original area table for
        which no lookup was possible. It does not calculate distributed runoff;
        that requires applying the runoff equation to each mapped pair before
        area weighting, as demonstrated in Investigation 1.
        '''),
        code(r'''
        composites = {
            condition: composite_from_areas(
                analysis_pairs,
                condition=condition,
                nlcd_col="nlcd",
                hsg_col="hsg",
                area_col=analysis_area_column,
            )
            for condition in ["poor", "fair", "good"]
        }

        composite_table = pd.DataFrame(composites).T[
            ["cn_weighted_CN", "cn_weighted_S", "percent_area_unmapped"]
        ]
        composite_table["poor_minus_good_CN"] = (
            composites["poor"]["cn_weighted_CN"]
            - composites["good"]["cn_weighted_CN"]
        )
        composite_table.round(4)
        '''),
        md(r'''
        ## Step 10 — Quantify the independence assumption

        When a live joint table is present, the code below derives both
        marginals from that same table and crosses them. Boundary, pixels, year,
        soil source, and class totals are therefore held constant; the
        difference isolates the independence assumption.

        In the reference pathway, the recorded Difficult Run result preserves
        the corresponding calculation from the executed Earth Engine analysis.
        '''),
        code(r'''
        if live_pairs is not None:
            lc_from_joint = live_pairs.groupby("nlcd", as_index=False)["pct"].sum()
            hsg_from_joint = live_pairs.groupby("hsg", as_index=False)["pct"].sum()
            independent_from_live = cross_marginals(
                lc_from_joint, hsg_from_joint, area_column="pct"
            )
            observed_result = composite_from_areas(
                live_pairs, condition="fair", area_col="pct"
            )
            independent_result = composite_from_areas(
                independent_from_live, condition="fair", area_col="pct"
            )
            independence_summary = {
                "marginals crossed independently": independent_result["cn_weighted_CN"],
                "observed joint distribution": observed_result["cn_weighted_CN"],
                "independence assumption, CN": (
                    independent_result["cn_weighted_CN"]
                    - observed_result["cn_weighted_CN"]
                ),
            }
            print(pd.Series(independence_summary).round(4))
        elif recorded is not None:
            comparison = recorded["curve_number_2019_fair"]
            print("same live raster marginals crossed independently : %.4f" % comparison["marginals_crossed_independently"])
            print("live observed joint distribution                 : %.4f" % comparison["observed_joint_distribution"])
            print("independence assumption                          : %+.4f CN" % comparison["independence_assumption_cn"])
            print("raster soil area with no HSG                     : %.2f %%" % recorded["soils"]["percent_area_no_hsg"])
        else:
            print("Reference marginal analysis complete for", site["name"])
        '''),
        md(r'''
        For the recorded 2019 Difficult Run analysis, the raster marginals give
        CN 77.6638 when crossed independently and CN 75.7790 when their observed
        pixelwise joint distribution is used. The 1.8848-unit difference is an
        empirical estimate of this assumption for that boundary, year, soil
        source, and analysis scale.
        '''),
        md(r'''
        ## Step 11 — Calculate design runoff and assemble provenance

        The composite CN is a parameter; a runoff depth additionally requires a
        storm depth and lambda. The ten-year, twenty-four-hour rainfall below is
        taken from the versioned NOAA Atlas 14 table at the reference gage.

        The provenance object places data source, year, boundary, soil source,
        condition, compositing convention, unmapped area, and rainfall basis
        beside the numerical result. A reviewer should not have to reconstruct
        those choices from the code.
        '''),
        code(r'''
        atlas14 = pd.read_csv(DATA_DIR / "atlas14_depths.csv")
        design_depth = float(
            atlas14.loc[
                (atlas14.watershed == PREPARED_WATERSHED)
                & (atlas14.duration == "24-hr")
                & (atlas14.ari_years == 10),
                "depth_in",
            ].iloc[0]
        )
        headline = composites[HYDROLOGIC_CONDITION]
        design_runoff = float(
            runoff(design_depth, headline["cn_weighted_CN"], lam=0.20)
        )

        provenance = {
            "watershed": site["name"],
            "boundary_method": delineation_method,
            "boundary_area_sqmi": round(float(delineated_area), 4),
            "analysis_path": "Earth Engine observed joint" if live_pairs is not None else "reference marginal cross",
            "land_cover": "Annual NLCD" if live_pairs is not None else "EPA StreamCat NLCD summary",
            "land_cover_year": ANALYSIS_YEAR,
            "soils": SOILS_SOURCE if live_pairs is not None else "NRCS Soil Data Access summary",
            "hydrologic_condition": HYDROLOGIC_CONDITION,
            "composite_convention": "area-weighted curve number",
            "unmapped_area_pct": round(float(headline["percent_area_unmapped"]), 4),
            "lambda": 0.20,
            "design_storm": "NOAA Atlas 14, 10-year 24-hour at reference gage",
            "design_depth_in": design_depth,
            "composite_cn": round(float(headline["cn_weighted_CN"]), 4),
            "runoff_depth_in": round(design_runoff, 4),
        }
        print(json.dumps(provenance, indent=2))
        '''),
        md(r'''
        ## What the convenience method does

        For a live `Basin`, the production call

        ```python
        basin.composite_cn(year, condition="fair", soils="sda")
        ```

        performs Steps 7 through 9 by calling
        `joint_landcover_soils` and then delegating the hydrologic arithmetic to
        `cnkit.lookup.composite_from_areas`. It returns the composite results
        together with asset identifiers, scale, soil source, boundary area,
        pair count, and unmapped fractions. The notebook used the lower-level
        calls so that the intermediate area table and every assumption remain
        available for inspection.
        '''),
        md(r'''
        ## Method audit — Library operation and analyst decision

        | Step | Call or object | Operation performed by `cnkit` | Decision or check retained by the analyst |
        |---|---|---|---|
        | 1–3 | `watershed_from_point`, `watershed_from_gage`, `Watershed` | Resolve the outlet, obtain upstream geometry, calculate area, and retain method provenance | Select the outlet meaning and verify boundary, area, and warnings |
        | 4 | `Basin` | Convert the checked boundary to an Earth Engine geometry and retain scale, project, pixel, drainage, and cache settings | Select project, scale, and drainage convention |
        | 5 | `Basin.landcover`, `Basin.impervious` | Reduce categorical Annual NLCD and fractional imperviousness separately | Select year and interpret class area separately from impervious fraction |
        | 6 | `Basin.soil_groups` | Summarize map-unit keys and resolve the occurring keys through Soil Data Access | Select soil source and account for dual or unmapped groups |
        | 7 | `Basin.joint_landcover_soils` | Pack two raster codes, execute one histogram, and decode observed pairs | Decide whether joint spatial evidence or a marginal approximation supports the analysis |
        | 8 | `cn_lookup` | Index the crosswalk by NLCD, HSG, and hydrologic condition | Establish the crosswalk and condition basis |
        | 9 | `composite_from_areas` | Calculate weighted-CN and weighted-retention composites and unmapped fractions | Select and report the aggregation convention |
        | 10 | marginal cross and joint comparison | Recalculate from controlled marginals to isolate the independence effect | Interpret the difference at the stated boundary, year, source, and scale |
        | 11 | `runoff` | Apply the event equation to the selected storm, CN, and lambda | Select the rainfall basis and retain complete provenance |
        '''),
        md(r'''
        ## Report-out

        Bring back the following record:

        1. Watershed identifier, delineation route, area, and verification
           difference.
        2. Land-cover source/year and soil source.
        3. Composite CN and weighting convention.
        4. Poor-to-good condition spread.
        5. Area without a mapped lookup value.
        6. Independence correction, measured live or read from the recorded run.
        7. Design storm, lambda, and resulting runoff depth.

        Then identify which uncertainty should be reported beside the headline
        CN for this analysis and justify that choice from the intermediate
        tables.

        **Source anchors:** Annual NLCD Collection 1.2; gNATSGO map-unit raster;
        USDA Soil Data Access; EPA StreamCat; USGS NLDI; NOAA Atlas 14;
        TR-55 Worksheet 2; NEH-630 Chapters 7, 9, and 10.
        '''),
    ]
    return notebook("02 Build CN for a Watershed", "lab 2", cells)


def build_lab3():
    cells = [
        md(r'''
        # Lab 3 — Change and uncertainty

        **Twenty-five minutes.**

        This notebook separates three questions that are often combined in a
        curve-number analysis:

        1. **Spatial change:** how does the mapped land-cover–soil composition
           change through time?
        2. **Event response:** what curve numbers are implied by observed
           rainfall and runoff?
        3. **Antecedent state:** how sensitive is the result to the convention
           used to describe conditions before a storm?

        The recorded Difficult Run products support the complete analysis. An
        optional Earth Engine section repeats the spatial trajectory for a
        selected watershed.

        Each numbered step states the scientific question, describes the
        library operation, shows its intermediate result, and identifies the
        interpretation that belongs in a methods or results statement.
        '''),
        code(SETUP),
        code(r'''
        import json
        import os
        from getpass import getpass

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from IPython.display import display

        from cnkit import (
            CN_from_PQ,
            compare_conventions,
            doy_climatology,
            fit_asymptotic,
            runoff,
            sm_percentile,
        )

        USE_EARTH_ENGINE = False
        DELINEATION_INPUT = "gage"       # "gage" or "outlet"
        GAGE = "01646000"
        LAT, LON = 38.97594, -77.24581
        YEARS = [2001, 2004, 2007, 2010, 2013, 2016, 2019]
        SOILS_SOURCE = "sda"
        DESIGN_DEPTH_IN = 4.78
        '''),
        md(r'''
        ## Part 1 — A spatial curve-number trajectory

        This part holds boundary, soil, lookup, condition, scale, and
        compositing convention constant while land-cover year changes.
        '''),
        md(r'''

        ### Step 1 — Define what changes and what remains fixed

        For year $t$, the area-weighted curve number is

        $$
        CN_t=\frac{\sum_i A_{i,t}CN_i}{\sum_i A_{i,t}},
        $$

        where $A_{i,t}$ is the area of land-cover–soil pair $i$ in year
        $t$, and $CN_i$ is the lookup value assigned to that pair. Across
        the trajectory, `cnkit` holds the watershed boundary, soil layer,
        lookup crosswalk, hydrologic condition, pixel scale, and compositing
        convention constant. Annual NLCD is the changing input.

        Consequently, the year-to-year difference is attributable to mapped
        land-cover change under those fixed analytical choices. It is not a
        direct measurement of infiltration, storage, or runoff.
        '''),
        gee_data_source_register("### Earth Engine data sources for this trajectory"),
        md(r'''
        ### Step 2 — Load the recorded Earth Engine trajectory

        The table below was produced by the live workflow for Difficult Run.
        It contains poor, fair, and good hydrologic-condition calculations for
        the same annual joint land-cover–soil distribution. The three columns
        differ only in the lookup-table condition row.
        '''),
        code(r'''
        trajectory = pd.read_csv(PREPARED_DIR / "difficult_run_gee_trajectory.csv").set_index("year")
        recorded = json.loads(
            (PREPARED_DIR / "difficult_run_gee_summary.json").read_text()
        )
        change = float(trajectory.fair.iloc[-1] - trajectory.fair.iloc[0])
        mean_spread = float(trajectory.spread.mean())
        ratio = mean_spread / abs(change)

        print("boundary method                 NLDI split-catchment upstream")
        print("boundary area                   %.4f square miles" % recorded["watershed"]["area_sqmi"])
        print("land-cover asset                %s" % recorded["land_cover"]["asset"])
        print("soil asset                      %s" % recorded["soils"]["asset"])
        print("soil area without mapped HSG    %.2f %%" % recorded["soils"]["percent_area_no_hsg"])
        print()
        print("2001 CN                         %.4f" % trajectory.fair.iloc[0])
        print("2019 CN                         %.4f" % trajectory.fair.iloc[-1])
        print("mapped land-cover change       %+.4f CN" % change)
        print("mean condition spread           %.4f CN" % mean_spread)
        print("condition spread / change        %.1f" % ratio)
        display(trajectory.round(4))
        '''),
        md(r'''
        ### Step 3 — Interpret the hydrologic-condition interval

        Poor, fair, and good are field descriptions of cover density,
        management, residue, grazing, and related surface conditions. Annual
        NLCD classifies land cover but does not observe those attributes.
        Recalculating all pixels with the poor and good lookup rows therefore
        provides a **sensitivity interval** around the fair-condition result.

        This interval is not a statistical confidence interval: no probability
        distribution has been assigned to hydrologic condition. Its purpose is
        to show how strongly an unobserved table choice affects the trajectory.
        '''),
        code(r'''
        fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.5))

        axes[0].plot(
            trajectory.index,
            trajectory.fair,
            "o-",
            color="#007f92",
            lw=2.6,
        )
        axes[0].set_title("Fair-condition trajectory (expanded scale)")

        axes[1].fill_between(
            trajectory.index,
            trajectory.good,
            trajectory.poor,
            color="#c85d45",
            alpha=0.22,
            label="poor-to-good sensitivity interval",
        )
        axes[1].plot(
            trajectory.index,
            trajectory.fair,
            "o-",
            color="#007f92",
            lw=2.6,
            label="fair-condition trajectory",
        )
        axes[1].set_title("Trajectory in the condition interval")
        axes[1].legend(loc="upper left")

        for ax in axes:
            ax.set(xlabel="year", ylabel="composite curve number")
            ax.grid(alpha=0.25)
        plt.show()
        '''),
        md(r'''
        ### Step 4 — Understand how `cn_trajectory` performs the calculation

        The convenience workflow organizes the same lower-level operations
        used in Investigation 2:

        1. Accept an existing `Watershed`, or delineate one from coordinates.
        2. Create one `Basin` so the boundary and scale remain fixed.
        3. For each requested year, call `joint_landcover_soils`; that method
           packs land-cover and soil codes into one integer image, applies one
           Earth Engine frequency histogram, and decodes the observed pairs.
        4. Send the same joint table to `composite_from_areas` for poor, fair,
           and good lookup rows. No additional Earth Engine reduction is needed
           for the condition calculations.
        5. Optionally transform each composite CN to runoff at a stated design
           depth, then attach assets, scale, boundary, and unmapped-area
           provenance to the returned result.

        The workflow is convenient, but the scientific definition of the
        trajectory remains the equation in Step 1.
        '''),
        md(r'''
        ### Step 4A — Delineate a selected watershed

        The application is separated into boundary construction and Earth
        Engine analysis so each spatial operation can be inspected. Change the
        gage or outlet configuration above, then set `USE_EARTH_ENGINE=True`.
        '''),
        code(r'''
        selected_watershed = None

        if USE_EARTH_ENGINE:
            activate_full_cnkit()
            from cnkit.delineate import watershed_from_gage, watershed_from_point

            if DELINEATION_INPUT == "gage":
                selected_watershed = watershed_from_gage(GAGE)
            elif DELINEATION_INPUT == "outlet":
                selected_watershed = watershed_from_point(LAT, LON)
            else:
                raise ValueError("DELINEATION_INPUT must be 'gage' or 'outlet'")

            print(selected_watershed)
            print("area: %.3f square miles" % selected_watershed.area_sqmi)
        else:
            print("Recorded Difficult Run trajectory selected.")
        '''),
        md(r'''
        ### Step 4B — Calculate the annual trajectory

        Authentication and the annual reductions occur only in this cell. The
        preceding boundary can therefore be checked before any raster summary
        is requested.
        '''),
        code(r'''
        live_trajectory = None

        if USE_EARTH_ENGINE:
            import ee
            from cnkit.gee import initialise
            from cnkit.workflows import cn_trajectory

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass(
                "Earth Engine project ID: "
            )
            ee.Authenticate()
            initialise(project=project)

            live_trajectory = cn_trajectory(
                watershed=selected_watershed,
                project=project,
                years=YEARS,
                condition="fair",
                soils=SOILS_SOURCE,
                design_depth_in=DESIGN_DEPTH_IN,
                progress=lambda done, total, year: print(
                    "%d/%d  %d" % (done, total, year)
                ),
            )
            display(live_trajectory)
            print(live_trajectory.summary())
        else:
            print("Set USE_EARTH_ENGINE=True to calculate the selected watershed.")
        '''),
        md(r'''
        ## Part 2 — Curve numbers inferred from observed events

        This part changes the evidence base from spatial lookup tables to
        rainfall and direct-runoff observations at streamgages.
        '''),
        md(r'''

        ### Step 5 — Invert the rainfall–runoff equation

        For an event with measured rainfall $P$ and direct-runoff depth $Q$,
        `CN_from_PQ` solves the curve-number equation backward. With
        $I_a=\lambda S$, the physically admissible root is used to recover
        $S$, followed by

        $$
        CN=\frac{1000}{S+10}.
        $$

        Event CN is therefore a transformed observation, not a direct sensor
        measurement. It depends on rainfall, hydrograph separation and runoff
        volume, watershed area, event definition, and the selected lambda.
        Events with $Q\leq0$, $Q>P$, or no physically valid solution are
        excluded from the asymptotic fit.
        '''),
        code(r'''
        difficult_events = pd.read_csv(
            DATA_DIR / "events_01646000.csv", parse_dates=["start", "end"]
        )
        difficult_events["CN_lambda_020"] = CN_from_PQ(
            difficult_events.P_in.values,
            difficult_events.Q_in.values,
            lam=0.20,
        )
        difficult_events["CN_lambda_005"] = CN_from_PQ(
            difficult_events.P_in.values,
            difficult_events.Q_in.values,
            lam=0.05,
        )
        display(
            difficult_events[
                ["start", "P_in", "Q_in", "runoff_ratio", "CN_lambda_020", "CN_lambda_005"]
            ].head(10).round(3)
        )
        print("event records:", len(difficult_events))
        '''),
        md(r'''
        ### Step 6 — Estimate the standard asymptotic response

        Event-derived CN commonly varies with storm depth. The Hawkins
        standard response represents a decreasing sequence that approaches a
        stable value as rainfall increases:

        $$
        CN(P)=CN_{\infty}+(100-CN_{\infty})e^{-kP}.
        $$

        `fit_asymptotic` first derives event CN with the specified lambda, then
        uses bounded nonlinear least squares to estimate $CN_{\infty}$ and
        $k$. It returns the fitted parameters, event count, RMSE, and
        coefficient of determination. The diagnostic statistics describe this
        functional fit; they do not account for uncertainty in precipitation,
        discharge, or hydrograph separation.
        '''),
        code(r'''
        fits = []
        fitted_objects = {}
        for watershed, gage, table_cn in [
            ("Difficult Run", "01646000", 75.5),
            ("Accotink Creek", "01654000", 77.9),
        ]:
            events = pd.read_csv(DATA_DIR / ("events_" + gage + ".csv"))
            fit20 = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.20)
            fit05 = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.05)
            fitted_objects[(gage, 0.20)] = fit20
            fitted_objects[(gage, 0.05)] = fit05
            fits.append(
                {
                    "watershed": watershed,
                    "events": len(events),
                    "table_CN": table_cn,
                    "CN_inf_lambda_020": fit20.cn_inf,
                    "r2_lambda_020": fit20.r2,
                    "CN_inf_lambda_005": fit05.cn_inf,
                    "r2_lambda_005": fit05.r2,
                }
            )
        fit_table = pd.DataFrame(fits).set_index("watershed")
        display(fit_table.round(3))
        '''),
        code(r'''
        difficult_fit = fitted_objects[("01646000", 0.20)]
        valid_event_cn = difficult_events.replace([np.inf, -np.inf], np.nan).dropna(
            subset=["P_in", "CN_lambda_020"]
        )
        rainfall_grid = np.linspace(
            valid_event_cn.P_in.min(), valid_event_cn.P_in.max(), 250
        )

        fig, ax = plt.subplots(figsize=(8.2, 4.8))
        ax.scatter(
            valid_event_cn.P_in,
            valid_event_cn.CN_lambda_020,
            s=18,
            alpha=0.32,
            color="#6f7f89",
            label="event-derived CN",
        )
        ax.plot(
            rainfall_grid,
            difficult_fit.predict(rainfall_grid),
            color="#c85d45",
            lw=2.8,
            label=r"standard fit, $CN_{\infty}=%.1f$" % difficult_fit.cn_inf,
        )
        ax.axhline(75.5, color="#007f92", ls="--", label="table CN = 75.5")
        ax.set(xlabel="event rainfall, inches", ylabel="event-derived curve number")
        ax.set_ylim(0, 103)
        ax.grid(alpha=0.25)
        ax.legend()
        plt.show()
        '''),
        md(r'''
        ### Step 7 — Treat lambda and CN as a paired calibration

        The tabulated curve numbers were developed with the conventional
        relation $I_a=0.20S$. Replacing lambda with 0.05 changes both the
        rainfall threshold and the fitted event CN. The two fitted columns
        above show why a reported CN must include its lambda; the number and
        the equation convention form one calibration.

        Compare the two fitted $CN_{\infty}$ values and their diagnostics.
        A better fit under one lambda is evidence about this event sample, not
        a universal conversion factor for another watershed.
        '''),
        code(r'''
        gage_names = {
            "01646000": "Difficult Run",
            "01654000": "Accotink Creek",
        }
        paired_rows = []
        for (gage, lam), fitted in fitted_objects.items():
            paired_rows.append(
                {
                    "watershed": gage_names[gage],
                    "lambda": lam,
                    "CN_infinity": fitted.cn_inf,
                    "events_fitted": fitted.n_events,
                    "R_squared": fitted.r2,
                    "runoff_at_design_depth_in": float(
                        runoff(DESIGN_DEPTH_IN, fitted.cn_inf, lam=lam)
                    ),
                }
            )

        paired_calibration = pd.DataFrame(paired_rows).sort_values(
            ["watershed", "lambda"], ascending=[True, False]
        )
        display(paired_calibration.round(3))
        '''),
        md(r'''
        **Interpretation.** Compare lambda values within one watershed. The
        fitted CN changes because the inverse event equation changes, while the
        final runoff column places each fitted CN back inside its corresponding
        equation. Report the CN, lambda, event count, and fit diagnostic as one
        calibration record.
        '''),
        md(r'''
        ## Part 3 — Antecedent-condition conventions

        This part compares two operational descriptions of the watershed state
        before an event: five-day rainfall history and seasonally standardized
        root-zone wetness.
        '''),
        md(r'''

        ### Step 8 — Distinguish rainfall history from observed wetness

        The historical antecedent moisture condition (AMC) convention assigns
        class I, II, or III from five-day rainfall thresholds that vary between
        growing and dormant seasons. NEH-630 now uses the broader term
        antecedent runoff condition (ARC) to emphasize that runoff response
        also reflects cover, temperature, frozen ground, and event history.

        The alternative examined here uses NASA POWER `GWETROOT`, a
        model-assimilated root-zone wetness index. It represents a broad soil
        layer at a comparatively coarse spatial scale; it is not an in-situ
        soil-moisture measurement for every point in the watershed.

        Raw wetness values have a seasonal cycle. `doy_climatology` pools all
        observations within ±15 calendar days of each day of year across the
        record. `sm_percentile` compares the previous day's value with that
        local seasonal pool. This makes a January and July percentile
        comparable while retaining the stated 31-day window as an analytical
        choice.
        '''),
        code(r'''
        events = pd.read_csv(DATA_DIR / "events_01646000.csv", parse_dates=["start"])
        precipitation = pd.read_csv(
            DATA_DIR / "precip_01646000.csv", parse_dates=["date"]
        ).set_index("date").P_in
        moisture = pd.read_csv(
            DATA_DIR / "soilmoisture_power_01646000.csv", parse_dates=["date"]
        ).set_index("date").GWETROOT

        climatology = doy_climatology(moisture, window=15)
        events["previous_day"] = events.start.dt.normalize() - pd.Timedelta(days=1)
        events["root_zone_wetness"] = events.previous_day.map(moisture)
        events["wetness_percentile"] = [
            sm_percentile(moisture, day, climatology=climatology)
            for day in events.previous_day
        ]
        events["event_cn"] = CN_from_PQ(
            events.P_in.values, events.Q_in.values, lam=0.20
        )

        display(
            events[
                ["start", "P_in", "Q_in", "root_zone_wetness", "wetness_percentile", "event_cn"]
            ].head(10).round(3)
        )
        '''),
        md(r'''
        ### Step 9 — Compare the conventions on the same storm dates

        `compare_conventions` performs both classifications without blending
        them. For every event date it:

        1. sums the preceding five days of daily rainfall and applies the
           historical seasonal AMC thresholds;
        2. calculates the previous-day wetness percentile from the ±15-day
           climatology;
        3. maps each class to a CN relative to the same fair-condition `cn2`;
        4. optionally applies each CN to the same design storm.

        The disagreement rate is a sensitivity diagnostic: it identifies how
        often the two proxies point to different antecedent states.
        '''),
        code(r'''
        convention_comparison = compare_conventions(
            events.start,
            precipitation,
            moisture,
            cn2=75.5,
            design_depth_in=DESIGN_DEPTH_IN,
            window=15,
        )

        print("comparable events:", convention_comparison.attrs["n_comparable"])
        print("agreements:       ", convention_comparison.attrs["n_agree"])
        print("disagreement rate: %.3f" % convention_comparison.attrs["disagreement_rate"])
        display(
            pd.crosstab(
                convention_comparison.AMC_direction,
                convention_comparison.SM_direction,
                margins=True,
            )
        )
        display(
            convention_comparison.loc[
                ~convention_comparison.conventions_agree,
                [
                    "date", "P5_in", "AMC_direction", "SM_percentile",
                    "SM_direction", "CN_from_AMC", "CN_from_SM",
                    "Q_from_AMC_in", "Q_from_SM_in",
                ],
            ].head(12)
        )
        '''),
        md(r'''
        ### Step 10 — Relate wetness rank to observed event response

        The percentile record can also be divided into equal-width lower,
        middle, and upper ranges. Grouping observed event CN and runoff ratio
        by those ranges tests whether wetter antecedent states correspond to a
        systematically different event response in this record. The groups are
        descriptive; they do not redefine NRCS ARC classes.
        '''),
        code(r'''
        valid = events.replace([np.inf, -np.inf], np.nan).dropna(
            subset=["wetness_percentile", "event_cn", "runoff_ratio"]
        ).copy()
        valid["wetness_range"] = pd.cut(
            valid.wetness_percentile,
            bins=[0, 33.333, 66.667, 100],
            labels=["lower third", "middle third", "upper third"],
            include_lowest=True,
        )
        antecedent_summary = valid.groupby("wetness_range", observed=True).agg(
            events=("event_cn", "size"),
            median_percentile=("wetness_percentile", "median"),
            median_event_cn=("event_cn", "median"),
            median_runoff_ratio=("runoff_ratio", "median"),
        )
        display(antecedent_summary.round(3))
        '''),
        md(r'''
        ## Method audit — Library operation and analyst decision

        | Layer | Operation performed by `cnkit` | Scientific choice retained by the analyst |
        |---|---|---|
        | `delineate` | Resolves an outlet or gage through NLDI and constructs an upstream boundary | Outlet meaning, delineation route, and boundary verification |
        | `gee` | Summarizes annual joint land-cover–soil pixels inside a fixed `Basin` | Imagery year, soil source, scale, and treatment of unmapped area |
        | `lookup` | Maps each NLCD–HSG pair to the selected table row and aggregates areas | Crosswalk, hydrologic condition, and composite convention |
        | `workflows` | Repeats the same joint calculation across years and records provenance | Which differences are interpreted as temporal change |
        | `core` | Evaluates or inverts the rainfall–runoff equation | Lambda, event definition, and measurement basis |
        | `asymptotic` | Fits the selected response model to event-derived CN | Model family, event screening, and adequacy of fit |
        | `antecedent` | Implements five-day rainfall and wetness-percentile conventions side by side | Proxy, climatology window, thresholds, and interpretation |

        The library makes these operations reproducible. It does not select the
        scientifically appropriate convention for a particular study.
        '''),
        md(r'''
        ## Final reporting statement

        Write a concise six-part methods-and-results record:

        1. Boundary method, area, land-cover source/years, soil source, and
           unmapped fraction.
        2. Lookup condition, composite convention, and lambda.
        3. Fair-condition trajectory change and poor-to-good sensitivity
           interval, identifying which inputs were held constant.
        4. Event-derived asymptotic CN, model form, event count, and fit
           diagnostic for each lambda examined.
        5. Antecedent proxies, climatology window, and convention disagreement
           rate.
        6. One conclusion that distinguishes mapped change, event response,
           and antecedent-condition sensitivity.

        **Source anchors:** USGS NWIS; ACIS/PRISM; NASA POWER; Annual NLCD;
        Hawkins (1993); Woodward et al. (2003); NEH-630 Chapters 9 and 10;
        NEH-4 Chapter 4 (historical AMC thresholds).
        '''),
    ]
    return notebook("03 Change and Uncertainty", "lab 3", cells)


def _source(cell):
    """Return source text for a NotebookNode or fallback dictionary cell."""
    return cell["source"] if isinstance(cell, dict) else cell.source


def _first_cell(cells, prefix):
    for index, cell in enumerate(cells):
        if _source(cell).lstrip().startswith(prefix):
            return index
    raise ValueError("Notebook cell not found: %s" % prefix)


def build_investigation1():
    """Focus the theory notebook on equation behavior and compositing."""
    base = build_lab1()
    source_cells = deepcopy(base["cells"] if isinstance(base, dict) else base.cells)
    calibration_start = _first_cell(source_cells, "## Step 7")
    cells = source_cells[:calibration_start]
    cells[0] = md(r'''
    # Investigation 1 — CN equation and runoff response

    **Participant-directed investigation.** Complete Steps 1–4 as the guided
    core, then select at least one extension. This investigation examines how
    rainfall depth, curve number, initial abstraction, and spatial aggregation
    govern event runoff.

    **Minimum result:** one figure or table comparing runoff under two stated
    modeling conventions, accompanied by the rainfall depth, CN basis, lambda,
    and aggregation method.
    ''')
    cells.extend([
        md(r'''
        ## Open investigation — Choose a question

        Select one or more extensions and state your comparison before changing
        the code.

        1. **Storm-depth dependence:** identify the rainfall range over which
           distributed and composite runoff differ most.
        2. **Parameter pairing:** compare lambda 0.20 with a consistently
           converted lambda 0.05 curve number.
        3. **Watershed heterogeneity:** replace the example subareas with a
           contrasting CN distribution that retains the same mean CN.
        4. **Decision sensitivity:** determine whether an alternative
           convention changes the interpretation, not only the numerical value.

        Retain the original result and the modified result so the effect of the
        chosen change remains auditable.
        '''),
        md(r'''
        ## Method audit and reporting record

        | Call | Library operation | Analyst responsibility |
        |---|---|---|
        | `S_from_CN` | Applies the CN-to-retention transformation | Establish the CN basis and units |
        | `runoff` | Applies the piecewise event equation | Select rainfall, CN, lambda, and spatial representation |
        | `composite_runoff` | Returns distributed, weighted-CN, and weighted-retention results | Select and justify an aggregation convention |
        | `cn05_from_cn20` | Applies the published empirical conversion | Keep the converted CN paired with lambda 0.05 |

        Record: analytical question; inputs and units; convention changed;
        principal quantitative result; interpretation; and one limitation.

        ## References

        - U.S. Department of Agriculture, Natural Resources Conservation
          Service. 2004. *National Engineering Handbook, Part 630, Chapter 10:
          Estimation of Direct Runoff from Storm Rainfall*.
          [Official PDF](https://directives.nrcs.usda.gov/sites/default/files2/1712930608/7300.pdf).
        - U.S. Department of Agriculture, Soil Conservation Service. 1986.
          *Urban Hydrology for Small Watersheds*, Technical Release 55,
          second edition. Worksheet 2.
        - Woodward, D. E., R. H. Hawkins, R. Jiang, A. T. Hjelmfelt Jr.,
          J. A. Van Mullem, and Q. D. Quan. 2003. “Runoff Curve Number Method:
          Examination of the Initial Abstraction Ratio.” *World Water &
          Environmental Resources Congress 2003*, 1–10.
          [doi:10.1061/40685(2003)308](https://doi.org/10.1061/40685%282003%29308).
        - Hawkins, R. H. 1993. “Asymptotic Determination of Runoff Curve
          Numbers from Data.” *Journal of Irrigation and Drainage Engineering*
          119(2):334–345.
          [doi:10.1061/(ASCE)0733-9437(1993)119:2(334)](https://doi.org/10.1061/%28ASCE%290733-9437%281993%29119%3A2%28334%29).

        The complete cross-notebook source ledger is available in
        [workshop source ledger](https://github.com/skp703/cn-workshop-2026/blob/main/docs/SOURCES.md).
        '''),
    ])
    return notebook("01 CN Equation and Runoff Response", "investigation 1", cells)


def build_investigation2():
    """Retain the spatial workflow and add an explicit inquiry section."""
    base = build_lab2()
    cells = deepcopy(base["cells"] if isinstance(base, dict) else base.cells)
    cells[0] = md(r'''
    # Investigation 2 — Spatial CN for a watershed

    **Participant-directed investigation.** Follow the numbered spatial
    workflow to produce a watershed boundary, land-cover–soil area table,
    composite curve number, and design-runoff estimate. Verified reference
    products support the complete investigation; a registered Earth Engine
    project can apply the same workflow to a selected watershed.

    **Minimum result:** a mapped boundary and a composite CN reported with year,
    land-cover source, soil source, hydrologic condition, aggregation convention,
    analysis scale, and unmapped fraction.
    ''')
    report_index = _first_cell(cells, "## Report-out")
    cells.insert(report_index, md(r'''
    ## Open investigation — Choose a question

    1. Compare the observed joint land-cover–soil distribution with the product
       of its marginal distributions.
    2. Change the watershed, analysis year, hydrologic condition, or soil source
       while holding the other inputs fixed.
    3. Examine whether unmapped area or boundary choice materially affects the
       reported composite.
    4. Compare the effect on CN with the effect on runoff for the stated design
       rainfall depth.

    Change one analytical choice at a time and preserve the baseline result.
    '''))
    cells[report_index + 1] = md(r'''
    ## Reporting record

    Record: watershed and outlet; boundary method and area; land-cover and soil
    sources; year and scale; lookup and aggregation conventions; composite CN;
    unmapped fraction; design runoff; extension result; and one limitation.

    ## References and data sources

    - U.S. Geological Survey. *Annual National Land Cover Database*.
      [Collection 1 products and citation](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database).
    - USDA Natural Resources Conservation Service.
      [gNATSGO](https://www.nrcs.usda.gov/resources/data-and-reports/gridded-national-soil-survey-geographic-database-gnatsgo)
      and [Soil Data Access](https://sdmdataaccess.sc.egov.usda.gov/WebServiceHelp.aspx).
    - U.S. Environmental Protection Agency. [StreamCat Dataset](https://www.epa.gov/national-aquatic-resource-surveys/streamcat-dataset).
    - U.S. Geological Survey. [Network Linked Data Index documentation](https://api.water.usgs.gov/docs/nldi/).
    - NOAA National Weather Service. [Atlas 14](https://www.weather.gov/owp/hdsc).
    - USDA NRCS. 2004. [NEH Part 630, Chapter 10](https://directives.nrcs.usda.gov/sites/default/files2/1712930608/7300.pdf).

    The complete cross-notebook source ledger is available in
    [workshop source ledger](https://github.com/skp703/cn-workshop-2026/blob/main/docs/SOURCES.md).
    ''')
    return notebook("02 Spatial CN for a Watershed", "investigation 2", cells)


def build_investigation3():
    """Extract mapped change and hydrologic-condition sensitivity."""
    base = build_lab3()
    source_cells = deepcopy(base["cells"] if isinstance(base, dict) else base.cells)
    part1_start = _first_cell(source_cells, "## Part 1")
    part2_start = _first_cell(source_cells, "## Part 2")
    cells = [
        md(r'''
        # Investigation 3 — Land-cover change and design runoff

        **Participant-directed investigation.** Quantify a mapped curve-number
        trajectory while holding the watershed boundary, soil layer, lookup,
        hydrologic condition, scale, and aggregation convention fixed. Then
        compare the temporal signal with a hydrologic-condition sensitivity
        interval and its effect on design runoff.

        **Minimum result:** a CN trajectory, start-to-end change, poor-to-good
        condition spread, and a statement identifying which inputs changed and
        which were controlled.
        '''),
        code(SETUP),
        code(r'''
        import json
        import os
        from getpass import getpass

        import matplotlib.pyplot as plt
        import pandas as pd
        from IPython.display import display

        from cnkit import runoff

        USE_EARTH_ENGINE = False
        DELINEATION_INPUT = "gage"       # "gage" or "outlet"
        GAGE = "01646000"
        LAT, LON = 38.97594, -77.24581
        YEARS = [2001, 2004, 2007, 2010, 2013, 2016, 2019]
        SOILS_SOURCE = "sda"
        DESIGN_DEPTH_IN = 4.78
        '''),
    ]
    analysis_cells = source_cells[part1_start + 1:part2_start]
    for cell in analysis_cells:
        if cell["cell_type"] == "markdown":
            cell["source"] = cell["source"].replace("### Step", "## Step")
    cells.extend(analysis_cells)
    cells.extend([
        md(r'''
        ## Step 5 — Translate the trajectory to design runoff

        The nonlinear runoff equation determines whether a small change in CN
        has a consequential effect at the selected rainfall depth. Calculate
        runoff for the first and last fair-condition CN values and for the poor
        and good bounds in the final year.
        '''),
        code(r'''
        design_comparison = pd.Series(
            {
                "first-year fair runoff, in": float(runoff(
                    DESIGN_DEPTH_IN, trajectory.fair.iloc[0], lam=0.20
                )),
                "last-year fair runoff, in": float(runoff(
                    DESIGN_DEPTH_IN, trajectory.fair.iloc[-1], lam=0.20
                )),
                "last-year poor runoff, in": float(runoff(
                    DESIGN_DEPTH_IN, trajectory.poor.iloc[-1], lam=0.20
                )),
                "last-year good runoff, in": float(runoff(
                    DESIGN_DEPTH_IN, trajectory.good.iloc[-1], lam=0.20
                )),
            }
        )
        display(design_comparison.round(4))
        '''),
        md(r'''
        ## Open investigation — Choose a question

        1. Select different start and end years and explain whether the inferred
           trend is stable.
        2. Compare CN change with runoff change at two rainfall depths.
        3. Use a selected watershed through Earth Engine and compare its signal
           with the Difficult Run reference trajectory.
        4. Identify which land-cover transitions would need to be examined to
           explain the mapped trajectory.

        Record: boundary and years; controlled inputs; CN and runoff changes;
        condition interval; extension result; interpretation; and limitation.
        '''),
        md(r'''
        ## Method audit

        `cn_trajectory` reuses one watershed and `Basin`, requests the joint
        land-cover–soil distribution for each year, applies the same lookup and
        aggregation conventions, and attaches the spatial provenance. The
        analyst selects the years, data sources, scale, hydrologic condition,
        design rainfall, and interpretation of the resulting differences.

        ## References and data sources

        - U.S. Geological Survey. [Annual National Land Cover Database](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database).
        - USDA Natural Resources Conservation Service.
          [gNATSGO](https://www.nrcs.usda.gov/resources/data-and-reports/gridded-national-soil-survey-geographic-database-gnatsgo)
          and [Soil Data Access](https://sdmdataaccess.sc.egov.usda.gov/WebServiceHelp.aspx).
        - NOAA National Weather Service. [Atlas 14 precipitation-frequency estimates](https://www.weather.gov/owp/hdsc).
        - USDA NRCS. 2004. [NEH Part 630, Chapter 10](https://directives.nrcs.usda.gov/sites/default/files2/1712930608/7300.pdf).

        The complete cross-notebook source ledger is available in
        [workshop source ledger](https://github.com/skp703/cn-workshop-2026/blob/main/docs/SOURCES.md).
        '''),
    ])
    return notebook("03 Land-Cover Change and Design Runoff", "investigation 3", cells)


def build_investigation4():
    """Extract event calibration and antecedent-state analysis."""
    base = build_lab3()
    source_cells = deepcopy(base["cells"] if isinstance(base, dict) else base.cells)
    part2_start = _first_cell(source_cells, "## Part 2")
    audit_start = _first_cell(source_cells, "## Method audit")
    analysis_cells = source_cells[part2_start + 1:audit_start]

    replacements = {
        "### Step 5": "## Step 1",
        "### Step 6": "## Step 2",
        "### Step 7": "## Step 3",
        "### Step 8": "## Step 4",
        "### Step 9": "## Step 5",
        "### Step 10": "## Step 6",
            "## Part 3 — Antecedent-condition conventions":
            "## Part 2 — Antecedent-condition conventions",
    }
    for cell in analysis_cells:
        if cell["cell_type"] == "markdown":
            for old, new in replacements.items():
                cell["source"] = cell["source"].replace(old, new)

    cells = [
        md(r'''
        # Investigation 4 — Event-derived CN and antecedent state

        **Participant-directed investigation.** Use observed rainfall and
        direct-runoff events to infer event curve numbers, estimate an
        asymptotic response, and compare two antecedent-state conventions.

        **Minimum result:** one fitted curve number reported with lambda, event
        count, model form, and diagnostic, plus one comparison of rainfall-
        history and root-zone-wetness classifications.
        '''),
        code(SETUP),
        code(r'''
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from IPython.display import display

        from cnkit import (
            CN_from_PQ,
            compare_conventions,
            doy_climatology,
            fit_asymptotic,
            runoff,
            sm_percentile,
        )

        DESIGN_DEPTH_IN = 4.78
        '''),
        md(r'''
        ## Part 1 — Curve numbers inferred from observed events

        This part changes the evidence base from spatial lookup tables to
        rainfall and direct-runoff observations at streamgages.
        '''),
    ]
    cells.extend(analysis_cells)
    cells.extend([
        md(r'''
        ## Open investigation — Choose a question

        1. Compare lambda 0.20 and 0.05 within one watershed and retain the
           fitted event count and diagnostic.
        2. Compare Difficult Run and Accotink Creek using the same model and
           event-screening rules.
        3. Remove the smallest rainfall events and evaluate the stability of
           $CN_{\infty}$.
        4. Change the wetness-climatology window and examine the convention
           disagreement rate.
        5. Test whether observed event CN or runoff ratio differs systematically
           among wetness ranges.
        '''),
        md(r'''
        ## Method audit and reporting record

        | Layer | Library operation | Analyst responsibility |
        |---|---|---|
        | `core` | Evaluates and inverts the rainfall–runoff equation | Lambda, event definition, rainfall and runoff basis |
        | `asymptotic` | Fits the selected response model to event-derived CN | Model family, event screening, and fit interpretation |
        | `antecedent` | Calculates five-day rainfall and wetness-percentile conventions side by side | Proxy, climatology window, thresholds, and interpretation |

        Record: watershed and event period; equation convention; fitted model,
        event count, parameter, and diagnostic; antecedent proxies and window;
        extension result; interpretation; and limitation.

        ## References and data sources

        - Hawkins, R. H. 1993. “Asymptotic Determination of Runoff Curve
          Numbers from Data.” *Journal of Irrigation and Drainage Engineering*
          119(2):334–345.
          [doi:10.1061/(ASCE)0733-9437(1993)119:2(334)](https://doi.org/10.1061/%28ASCE%290733-9437%281993%29119%3A2%28334%29).
        - Woodward, D. E., R. H. Hawkins, R. Jiang, A. T. Hjelmfelt Jr.,
          J. A. Van Mullem, and Q. D. Quan. 2003. “Runoff Curve Number Method:
          Examination of the Initial Abstraction Ratio.” *World Water &
          Environmental Resources Congress 2003*, 1–10.
          [doi:10.1061/40685(2003)308](https://doi.org/10.1061/40685%282003%29308).
        - U.S. Geological Survey. [Water Data for the Nation](https://waterdata.usgs.gov/nwis/),
          [doi:10.5066/F7P55KJN](https://doi.org/10.5066/F7P55KJN).
        - PRISM Group, Oregon State University. [PRISM climate data](https://prism.oregonstate.edu/terms/),
          accessed 9 August 2026 through the
          [ACIS web service](https://docs.rcc-acis.org/acisws/).
        - NASA POWER. [Daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/).
        - USDA NRCS. 2004. [NEH Part 630, Chapter 10](https://directives.nrcs.usda.gov/sites/default/files2/1712930608/7300.pdf).

        The complete cross-notebook source ledger is available in
        [workshop source ledger](https://github.com/skp703/cn-workshop-2026/blob/main/docs/SOURCES.md).
        '''),
    ])
    return notebook("04 Event-Derived CN and Antecedent State", "investigation 4", cells)


BUILDERS = {
    "00_Readiness_Check.ipynb": build_readiness,
    "01_CN_Equation_and_Runoff_Response.ipynb": build_investigation1,
    "02_Spatial_CN_for_a_Watershed.ipynb": build_investigation2,
    "03_Land_Cover_Change_and_Design_Runoff.ipynb": build_investigation3,
    "04_Event_CN_and_Antecedent_State.ipynb": build_investigation4,
}

STALE_NOTEBOOKS = {
    "01_Understand_the_Curve_Number.ipynb",
    "02_Build_CN_for_a_Watershed.ipynb",
    "03_Change_and_Uncertainty.ipynb",
}


def main():
    for filename in STALE_NOTEBOOKS:
        target = OUT / filename
        if target.exists():
            target.unlink()
    for filename, builder in BUILDERS.items():
        target = OUT / filename
        nbf.write(builder(), target)
        print("wrote", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
