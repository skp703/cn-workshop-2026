"""Build the four participant notebooks for the V3 workshop.

The generated notebooks support verified reference datasets and live Earth
Engine analysis through a common analytical and reporting framework.
"""

from __future__ import annotations

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
        ## What the setup cell does

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
        ## How the library is organized

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
        md(r'''
        ## Core environment

        This verifies the equation, the weighting calculation, and the files
        needed by the prepared-data path.
        '''),
        code(r'''
        from cnkit import composite_runoff

        expected = [0.4745, 0.0949, 0.0277]
        actual = [round(x, 4) for x in composite_runoff(1.0, [98, 55], [0.6, 0.4])]
        print("weighting check:", actual)
        assert actual == expected

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
        print("reference-data pathway: ready")
        '''),
        md(r'''
        ## Earth Engine project check

        Set `TEST_EARTH_ENGINE = True` after registering a Cloud project for
        Earth Engine. Leave it at `False` when using the workshop reference data.

        The project ID is requested at runtime and is not saved in this notebook.
        '''),
        code(r'''
        TEST_EARTH_ENGINE = False

        if TEST_EARTH_ENGINE:
            import os
            from getpass import getpass
            import ee

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass("Earth Engine project ID: ")
            ee.Authenticate()
            ee.Initialize(project=project)
            answer = ee.Number(21).multiply(2).getInfo()
            assert answer == 42
            print("Earth Engine check:", answer)
            print("live path: ready")
        else:
            print("Reference-data environment: ready")
            print("Set TEST_EARTH_ENGINE=True to verify an Earth Engine project.")
        '''),
        md(r'''
        ## Bring one watershed identifier if you can

        The live path accepts either a USGS gage number or outlet latitude and
        longitude for a CONUS watershed. Difficult Run and Accotink Creek are
        also available as fully documented reference analyses.
        '''),
    ]
    return notebook("00 Readiness Check", "pre-work", cells)


def build_lab1():
    cells = [
        md(r'''
        # Lab 1 — Understand the curve number

        **Twenty minutes.** This lab establishes the theoretical and numerical
        framework used by both spatial-data pathways.

        The guided analysis is organized as a sequence of explicit operations:

        1. translate curve number to potential retention;
        2. apply the initial-abstraction threshold;
        3. calculate event runoff;
        4. compare distributed and lumped compositing;
        5. treat lambda and curve number as a paired calibration; and
        6. distinguish a table estimate from a value inferred from observed
           rainfall–runoff events.

        The explanatory cells are intended to remain useful after the workshop.
        During the twenty-minute laboratory, complete the numbered **Analysis**
        cells and use the remaining material as a technical reference.
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
        ## 1. The event water-balance model

        The curve-number method is an event-scale, lumped rainfall–runoff
        relation. For rainfall depth $P$, direct-runoff depth $Q$, potential
        maximum retention $S$, and initial abstraction $I_a$, the standard
        equations in inch units are

        \[
        S = \frac{1000}{CN} - 10,
        \qquad I_a = \lambda S,
        \]

        \[
        Q = \begin{cases}
        0, & P \le I_a,\\[4pt]
        \dfrac{(P-I_a)^2}{P+(1-\lambda)S}, & P>I_a.
        \end{cases}
        \]

        A curve number is therefore a dimensionless transformation of $S$;
        it is not a directly observed land-surface property. Larger CN implies
        smaller retention, a smaller rainfall threshold, and greater runoff for
        the same event. The conventional value \(\lambda=0.20\) specifies the
        assumed fraction of retention that must be satisfied before runoff
        begins.
        '''),
        md(r'''
        ### Analysis 1A — Translate CN into retention and threshold

        `S_from_CN` implements only the first equation. The initial-abstraction
        threshold remains explicit in the notebook so that the role of lambda
        can be inspected directly.
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
        The threshold is mathematically consequential. At CN 70 and
        $\lambda=0.20$, $I_a$ is approximately 0.86 inches; an event below
        that depth produces zero direct runoff in the model. This is a model
        statement, not a claim that no water moves within the watershed.

        `cnkit.runoff` applies the piecewise equation, validates CN and lambda,
        broadcasts scalar or array inputs, and returns zero below the threshold.
        It does not select CN, lambda, rainfall, or the spatial unit of analysis.
        Those remain analyst decisions.
        '''),
        md(r'''
        ### Analysis 1B — Verify the implementation against the equation
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
        ## 2. Nonlinearity and the compositing question

        The runoff equation is nonlinear in CN because CN is first transformed
        to $S$, enters both the threshold and denominator, and appears inside
        a squared numerator. Consequently,

        \[
        Q\!\left(P,\sum_i w_i CN_i\right)
        \ne \sum_i w_i Q(P,CN_i)
        \]

        in general. The left side is a lumped calculation; the right side
        computes runoff for each hydrologically distinct subarea and then
        aggregates runoff volume. Both are reproducible calculations, but they
        represent different spatial models.
        '''),
        md(r'''
        ### Analysis 2A — Resolve the weighting calculation by subarea

        Sixty percent connected impervious cover at CN 98 is combined with
        forty percent woods at CN 55 under a one-inch storm. `composite_runoff`
        returns three results in a fixed order:

        1. runoff by subarea, subsequently area weighted;
        2. CN area weighted first, followed by one runoff calculation; and
        3. retention $S$ area weighted first, converted back to CN, followed
           by one runoff calculation.
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
        The wooded subarea remains below its initial-abstraction threshold while
        the impervious subarea is already producing runoff. A lumped parameter
        removes that threshold contrast before the nonlinear equation is
        evaluated. This explains why the difference is largest for smaller
        storms and heterogeneous watersheds.
        '''),
        md(r'''
        ### Analysis 2B — Examine how the difference changes with storm depth
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
        ## 3. Lambda and CN form a paired calibration

        Lambda is not an independent switch applied after CN has been selected.
        Event-derived and table-derived curve numbers are conditional on the
        lambda used in the runoff equation. A CN calibrated with
        \(\lambda=0.20\) should therefore be converted or refitted before it is
        used with \(\lambda=0.05\).

        `cn05_from_cn20` implements the Hawkins et al. (2003) empirical
        conversion. The converted CN is numerically lower because the smaller
        initial-abstraction ratio permits runoff to begin earlier. Similar
        runoff response—not equal CN—is the comparison to make.
        '''),
        md(r'''
        ### Analysis 3 — Compare three documented parameter estimates

        Difficult Run has a 2019 table composite near 75.5 and a fitted
        asymptotic value of 69.7. The lambda conversion below is a third number:
        it describes the same response convention under lambda 0.05 rather than
        0.20.
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
        The three rows have different evidentiary bases: a spatial lookup, a
        rainfall–runoff fit, and a conversion between equation conventions.
        They should be labelled accordingly rather than described as competing
        measurements of one fixed property.
        '''),
        md(r'''
        ## 4. How a curve number is inferred from measured events

        For an observed event pair \((P,Q)\), `CN_from_PQ` algebraically inverts
        the same runoff equation for a specified lambda. Each valid event
        produces an event-derived CN. These values vary with storm depth,
        antecedent state, measurement error, and model adequacy; the variation
        is information rather than a reason to average immediately.

        `fit_asymptotic` then fits the Hawkins standard relation

        \[
        CN(P)=CN_{\infty}+(100-CN_{\infty})e^{-kP}
        \]

        by nonlinear least squares. \(CN_{\infty}\) is the large-storm
        asymptote, $k$ controls the rate of approach, and $R^2$ describes
        how much of the event-CN variation is explained by this specific
        functional form. The fit does not establish that the watershed has a
        unique physical CN.
        '''),
        code(r'''
        events = pd.read_csv(DATA_DIR / "events_01646000.csv")
        event_cn = CN_from_PQ(events.P_in.values, events.Q_in.values, lam=0.20)
        fit = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.20)

        valid = np.isfinite(event_cn)
        p_line = np.linspace(events.P_in.min(), events.P_in.max(), 200)
        fitted_line = fit.cn_inf + (100.0 - fit.cn_inf) * np.exp(-fit.k * p_line)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.scatter(events.P_in.values[valid], event_cn[valid], s=12, alpha=0.25,
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

        print("events:       ", len(events))
        print("CN infinity:   %.3f" % fit.cn_inf)
        print("decay k:       %.3f" % fit.k)
        print("R squared:     %.3f" % fit.r2)
        '''),
        md(r'''
        ## 5. What `cnkit` did—and did not do

        | Call | Library operation | Analyst responsibility |
        |---|---|---|
        | `S_from_CN` | Applies the CN-to-retention transformation | Establish the basis and scale of CN |
        | `runoff` | Applies the piecewise event equation | Select $P$, CN, lambda, and spatial representation |
        | `composite_runoff` | Returns distributed, weighted-CN, and weighted-S calculations | Choose and justify the compositing convention |
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
           \(CN_{\infty}\).

        **Source anchors:** NEH-630 Chapter 10 equations 10-1 and 10-11;
        TR-55 Worksheet 2; Woodward et al. (2003), DOI
        `10.1061/40685(2003)308`; Hawkins et al. (2003), DOI
        `10.1061/(ASCE)1084-0699(2003)8:6(445)`.
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

        fig, ax = plt.subplots(figsize=(6.2, 5.5))
        for ring in rings:
            coordinates = np.asarray(ring)
            ax.fill(coordinates[:, 0], coordinates[:, 1], color="#5ca6a6", alpha=0.28)
            ax.plot(coordinates[:, 0], coordinates[:, 1], color="#17274f", lw=1.4)
        ax.plot(float(site["sample_lon"]), float(site["sample_lat"]), "o",
                color="#b24d35", label="gage / outlet")
        ax.set(xlabel="longitude", ylabel="latitude", title=site["name"])
        ax.set_aspect(1.0 / np.cos(np.deg2rad(float(site["centroid_lat"]))))
        ax.legend()
        ax.grid(alpha=0.18)
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

        \[
        A_{ij}=A\,p(LC_i)\,p(HSG_j).
        \]

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
        area weighting, as demonstrated in Lab 1.
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

        ### Step 1 — Define what changes and what remains fixed

        For year $t$, the area-weighted curve number is

        \[
        CN_t=\frac{\sum_i A_{i,t}CN_i}{\sum_i A_{i,t}},
        \]

        where $A_{i,t}$ is the area of land-cover–soil pair $i$ in year
        $t$, and $CN_i$ is the lookup value assigned to that pair. Across
        the trajectory, `cnkit` holds the watershed boundary, soil layer,
        lookup crosswalk, hydrologic condition, pixel scale, and compositing
        convention constant. Annual NLCD is the changing input.

        Consequently, the year-to-year difference is attributable to mapped
        land-cover change under those fixed analytical choices. It is not a
        direct measurement of infiltration, storage, or runoff.
        '''),
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
        used in Lab 2:

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
        ### Optional application — delineate a selected watershed

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
        ### Optional application — calculate the annual trajectory

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

        ### Step 5 — Invert the rainfall–runoff equation

        For an event with measured rainfall $P$ and direct-runoff depth $Q$,
        `CN_from_PQ` solves the curve-number equation backward. With
        $I_a=\lambda S$, the physically admissible root is used to recover
        $S$, followed by

        \[
        CN=\frac{1000}{S+10}.
        \]

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

        \[
        CN(P)=CN_{\infty}+(100-CN_{\infty})e^{-kP}.
        \]

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
        md(r'''
        ## Part 3 — Antecedent-condition conventions

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
        ## What each library layer contributes

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


BUILDERS = {
    "00_Readiness_Check.ipynb": build_readiness,
    "01_Understand_the_Curve_Number.ipynb": build_lab1,
    "02_Build_CN_for_a_Watershed.ipynb": build_lab2,
    "03_Change_and_Uncertainty.ipynb": build_lab3,
}


def main():
    for filename, builder in BUILDERS.items():
        target = OUT / filename
        nbf.write(builder(), target)
        print("wrote", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
