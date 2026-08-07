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
        code(SETUP),
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
        longitude for a CONUS watershed. If neither is ready, use Difficult Run
        or Accotink Creek during the session.
        '''),
    ]
    return notebook("00 Readiness Check", "pre-work", cells)


def build_lab1():
    cells = [
        md(r'''
        # Lab 1 — Understand the curve number

        **Twenty minutes.** This lab establishes the theoretical and numerical
        framework used by both spatial-data pathways.

        The goal is not to memorize an equation. The goal is to see what changes
        when a convention is changed, what nonlinear averaging does, and which
        number you would defend in a report.
        '''),
        code(SETUP),
        code(r'''
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        from cnkit import (
            S_from_CN,
            cn05_from_cn20,
            composite_runoff,
            runoff,
        )
        '''),
        md(r'''
        ## 1. One storm, three documented curve numbers

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
        **Interpretation prompt:** the converted curve number is lower, but it
        reproduces nearly the same response because lambda and CN are a paired
        calibration. Write one sentence explaining why changing lambda without
        converting CN mixes two calibrations.
        '''),
        md(r'''
        ## 2. The weighting trap

        Sixty percent connected impervious cover at CN 98 sits beside forty
        percent woods at CN 55. Compute runoff from a one-inch storm three ways.
        '''),
        code(r'''
        q_distributed, q_weighted_cn, q_weighted_s = composite_runoff(
            1.0, [98, 55], [0.60, 0.40]
        )
        weighting = pd.Series(
            {
                "runoff by subarea, then area-weight": q_distributed,
                "area-weight CN, then compute runoff": q_weighted_cn,
                "area-weight S, then compute runoff": q_weighted_s,
            },
            name="runoff_inches",
        )
        weighting.round(4)
        '''),
        code(r'''
        cn_values = [98, 55]
        s_values = [float(S_from_CN(cn)) for cn in cn_values]
        print("CN 98: S = %.3f in, Ia = %.3f in" % (s_values[0], 0.2 * s_values[0]))
        print("CN 55: S = %.3f in, Ia = %.3f in" % (s_values[1], 0.2 * s_values[1]))
        print("distributed / weighted-CN ratio: %.1f" % (q_distributed / q_weighted_cn))
        '''),
        md(r'''
        The wooded subarea produces zero runoff because its initial abstraction
        exceeds the storm. Averaging CN first quietly treats the whole basin as
        partly absorbing. The arithmetic is correct in every row; the modelling
        decisions are different.
        '''),
        md(r'''
        ## 3. Why the disagreement shrinks in large storms
        '''),
        code(r'''
        storms = np.linspace(0.25, 6.0, 48)
        values = np.array([composite_runoff(p, [98, 55], [0.60, 0.40]) for p in storms])

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
        ## Report-out

        Bring back:

        1. The three runoff depths from the weighting example.
        2. Which convention you would report for a heterogeneous watershed.
        3. One sentence on the evidence behind that choice.

        **Source anchors:** NEH-630 Chapter 10 equations 10-1 and 10-11;
        TR-55 Worksheet 2; Woodward et al. (2003), DOI
        `10.1061/40685(2003)308`.
        '''),
    ]
    return notebook("01 Understand the Curve Number", "lab 1", cells)


def build_lab2():
    cells = [
        md(r'''
        # Lab 2 — Build a curve number for a watershed

        **Thirty-five minutes.**

        Prepared data is the default. The live path delineates a participant
        watershed, then uses Earth Engine to measure land cover and soil jointly.
        Both paths finish with the same questions about provenance, unmapped area,
        and defensibility.
        '''),
        code(SETUP),
        code(r'''
        import json
        import warnings
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        from cnkit import composite_from_areas

        # Change to "accotink_creek" for the second verified reference basin.
        PREPARED_WATERSHED = "difficult_run"

        # Set True only when the readiness check has already passed.
        USE_EARTH_ENGINE = False

        # Live-path input: a gage number is easiest. Set GAGE=None and provide
        # LAT/LON if you prefer a pour point.
        GAGE = "01646000"
        LAT, LON = 38.97594, -77.24581
        '''),
        md(r'''
        ## 1. The prepared tabular route

        StreamCat supplies land-cover percentages and Soil Data Access supplies
        soil-group percentages. Crossing those two marginal tables assumes they
        are independent. We make that assumption explicitly.
        '''),
        code(r'''
        landcover = pd.read_csv(DATA_DIR / "landcover_streamcat.csv")
        soils = pd.read_csv(DATA_DIR / "soils_hsg.csv", keep_default_na=False)

        def independent_cross(watershed, year):
            lc = landcover[(landcover.watershed == watershed) & (landcover.year == year)].copy()
            sg = soils[soils.watershed == watershed].copy()
            lc["key"], sg["key"] = 1, 1
            crossed = lc.merge(sg, on="key", suffixes=("_lc", "_soil"))
            crossed["area"] = crossed.pct_lc * crossed.pct_soil / 100.0
            return crossed[["nlcd", "hsg", "area"]]

        tabular = {}
        for condition in ["poor", "fair", "good"]:
            tabular[condition] = composite_from_areas(
                independent_cross(PREPARED_WATERSHED, 2019), condition=condition
            )

        pd.DataFrame(tabular).T[
            ["cn_weighted_CN", "cn_weighted_S", "percent_area_unmapped"]
        ].round(4)
        '''),
        md(r'''
        ## 2. Recorded live Earth Engine result

        The prepared path does not pretend to be live. It reads a result recorded
        from an executed Earth Engine notebook, including its asset identifiers,
        warning state, and redacted authentication prompt.
        '''),
        code(r'''
        if PREPARED_WATERSHED == "difficult_run":
            recorded = json.loads((PREPARED_DIR / "difficult_run_gee_summary.json").read_text())
            comparison = recorded["curve_number_2019_fair"]
            print("same live raster marginals crossed independently : %.4f" % comparison["marginals_crossed_independently"])
            print("live observed joint distribution                 : %.4f" % comparison["observed_joint_distribution"])
            print("independence assumption                          : %+.4f CN" % comparison["independence_assumption_cn"])
            print("raster soil area with no HSG                     : %.2f %%" % recorded["soils"]["percent_area_no_hsg"])
        else:
            print("Accotink has a complete tabular path. Its live-GEE snapshot is not yet recorded; use the live branch or compare tabular results.")
        '''),
        md(r'''
        The 1.88-unit difference isolates the independence assumption because
        both calculations use the same Earth Engine land-cover and soil
        marginals. The older 4.50-unit figure is the range between extreme
        feasible pairings of the tabular marginals—a bound, not this measurement.
        '''),
        md(r'''
        ## 3. Earth Engine application — a selected watershed

        Set `USE_EARTH_ENGINE = True` to delineate a selected watershed and
        estimate the land-cover–soil joint distribution. The recorded reference
        result remains available for direct comparison.
        '''),
        code(r'''
        live = None
        live_watershed = None

        if USE_EARTH_ENGINE:
            import os
            from getpass import getpass
            activate_full_cnkit()
            import ee
            from cnkit.delineate import watershed_from_gage, watershed_from_point
            from cnkit.gee import Basin, initialise

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass("Earth Engine project ID: ")
            ee.Authenticate()
            initialise(project=project)

            live_watershed = (
                watershed_from_gage(GAGE) if GAGE else watershed_from_point(LAT, LON)
            )
            basin = Basin(live_watershed, project=project)
            joint = basin.joint_landcover_soils(2019, soils="sda")

            lc_marginal = joint.groupby("nlcd", as_index=False)["pct"].sum()
            hsg_marginal = joint.groupby("hsg", as_index=False)["pct"].sum()
            independent = pd.DataFrame(
                [
                    {"nlcd": int(a.nlcd), "hsg": s.hsg, "pct": a.pct * s.pct / 100.0}
                    for a in lc_marginal.itertuples()
                    for s in hsg_marginal.itertuples()
                ]
            )
            kwargs = dict(condition="fair", nlcd_col="nlcd", hsg_col="hsg", area_col="pct")
            observed = composite_from_areas(joint, **kwargs)
            assumed = composite_from_areas(independent, **kwargs)
            live = {
                "area_sqmi": live_watershed.area_sqmi,
                "observed_joint_cn": observed["cn_weighted_CN"],
                "independent_cn": assumed["cn_weighted_CN"],
                "difference_cn": assumed["cn_weighted_CN"] - observed["cn_weighted_CN"],
                "unmapped_pct": observed["percent_area_unmapped"],
                "joint_rows": len(joint),
            }
            print(json.dumps(live, indent=2))
        else:
            print("Reference-data analysis active.")
            print("Set USE_EARTH_ENGINE=True to analyze a selected watershed.")
        '''),
        md(r'''
        ## 4. Put the uncertainty beside the answer
        '''),
        code(r'''
        table = pd.DataFrame(
            {
                condition: {
                    "CN weighted by CN": result["cn_weighted_CN"],
                    "CN weighted by S": result["cn_weighted_S"],
                    "unmapped area, %": result["percent_area_unmapped"],
                }
                for condition, result in tabular.items()
            }
        ).T
        table["condition spread"] = tabular["poor"]["cn_weighted_CN"] - tabular["good"]["cn_weighted_CN"]
        table.round(3)
        '''),
        md(r'''
        ## Report-out

        Bring back four values:

        1. Composite CN and weighting convention.
        2. Poor-to-good condition spread.
        3. Area without a mapped hydrologic soil group.
        4. Independence correction, measured live or read from the recorded run.

        Then answer: **which uncertainty belongs beside the headline CN in a
        report?**

        **Source anchors:** Annual NLCD Collection 1.2; gNATSGO map-unit raster;
        USDA Soil Data Access; EPA StreamCat; NEH-630 Chapters 7 and 9.
        '''),
    ]
    return notebook("02 Build CN for a Watershed", "lab 2", cells)


def build_lab3():
    cells = [
        md(r'''
        # Lab 3 — Change and uncertainty

        **Twenty-five minutes.**

        Plot a measured trajectory inside the uncertainty band created by the
        method. Then use measured storms to ask whether a single table value and
        a rainfall proxy describe what the watershed actually did.
        '''),
        code(SETUP),
        code(r'''
        import json
        import os
        from getpass import getpass

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        from cnkit import CN_from_PQ, fit_asymptotic

        USE_EARTH_ENGINE = False
        GAGE = "01646000"
        LAT, LON = 38.97594, -77.24581
        YEARS = [2001, 2004, 2007, 2010, 2013, 2016, 2019]
        '''),
        md(r'''
        ## 1. The trajectory everyone can analyze

        These are recorded outputs from a successful live Earth Engine run over
        Difficult Run. The line is measured land-cover change. The band is the
        poor-to-good hydrologic-condition assumption over the same pixels.
        '''),
        code(r'''
        trajectory = pd.read_csv(PREPARED_DIR / "difficult_run_gee_trajectory.csv").set_index("year")
        change = float(trajectory.fair.iloc[-1] - trajectory.fair.iloc[0])
        mean_spread = float(trajectory.spread.mean())
        ratio = mean_spread / abs(change)

        print("2001 CN                         %.4f" % trajectory.fair.iloc[0])
        print("2019 CN                         %.4f" % trajectory.fair.iloc[-1])
        print("measured change                %+.4f CN" % change)
        print("mean condition spread           %.4f CN" % mean_spread)
        print("assumption / signal ratio        %.1f" % ratio)
        '''),
        code(r'''
        fig, ax = plt.subplots(figsize=(8.2, 4.8))
        ax.fill_between(
            trajectory.index,
            trajectory.good,
            trajectory.poor,
            color="#c85d45",
            alpha=0.22,
            label="poor-to-good condition assumption",
        )
        ax.plot(
            trajectory.index,
            trajectory.fair,
            "o-",
            color="#007f92",
            lw=2.6,
            label="measured land-cover trajectory",
        )
        ax.set(xlabel="year", ylabel="composite curve number")
        ax.grid(alpha=0.25)
        ax.legend(loc="upper left")
        plt.show()
        '''),
        md(r'''
        ## 2. Ask the gage instead of the table

        `fit_asymptotic` uses measured rainfall and runoff events. It does not
        assume the table value is correct.
        '''),
        code(r'''
        fits = []
        for watershed, gage, table_cn in [
            ("Difficult Run", "01646000", 75.5),
            ("Accotink Creek", "01654000", 77.9),
        ]:
            events = pd.read_csv(DATA_DIR / ("events_" + gage + ".csv"))
            fit20 = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.20)
            fit05 = fit_asymptotic(events.P_in.values, events.Q_in.values, lam=0.05)
            fits.append(
                {
                    "watershed": watershed,
                    "events": len(events),
                    "table_CN": table_cn,
                    "fitted_CN_lambda_020": fit20.cn_inf,
                    "r2_lambda_020": fit20.r2,
                    "fitted_CN_lambda_005": fit05.cn_inf,
                    "r2_lambda_005": fit05.r2,
                }
            )
        pd.DataFrame(fits).set_index("watershed").round(3)
        '''),
        md(r'''
        For Difficult Run, the table is high by about 5.8 CN units. Accotink
        differs in the opposite direction and its fitted relation is weak. The
        table error is not a simple correction that transfers between basins.
        '''),
        md(r'''
        ## 3. Antecedent condition from an observed state

        Split the Difficult Run events by root-zone wetness on the day before
        each event. Compare the dry and wet thirds without inventing new AMC
        classes.
        '''),
        code(r'''
        events = pd.read_csv(DATA_DIR / "events_01646000.csv", parse_dates=["start"])
        moisture = pd.read_csv(
            DATA_DIR / "soilmoisture_power_01646000.csv", parse_dates=["date"]
        ).set_index("date")

        events["previous_day"] = events.start.dt.normalize() - pd.Timedelta(days=1)
        events["root_zone_wetness"] = events.previous_day.map(moisture.GWETROOT)
        events["event_cn"] = CN_from_PQ(events.P_in.values, events.Q_in.values)
        valid = events.replace([np.inf, -np.inf], np.nan).dropna(
            subset=["root_zone_wetness", "event_cn"]
        )
        valid["wetness_third"] = pd.qcut(
            valid.root_zone_wetness, 3, labels=["driest", "middle", "wettest"]
        )
        antecedent = valid.groupby("wetness_third", observed=True).agg(
            events=("event_cn", "size"),
            median_wetness=("root_zone_wetness", "median"),
            median_event_cn=("event_cn", "median"),
            median_runoff_ratio=("runoff_ratio", "median"),
        )
        antecedent.round(3)
        '''),
        md(r'''
        ## 4. Earth Engine trajectory — a selected watershed

        This application uses seven years and returns the hydrologic-condition
        band with the trajectory. Set `USE_EARTH_ENGINE = True` to run it for the
        selected watershed.
        '''),
        code(r'''
        live_trajectory = None

        if USE_EARTH_ENGINE:
            activate_full_cnkit()
            import ee
            from cnkit.delineate import watershed_from_gage, watershed_from_point
            from cnkit.gee import initialise
            from cnkit.workflows import cn_trajectory

            project = os.environ.get("CNKIT_EE_PROJECT") or getpass("Earth Engine project ID: ")
            ee.Authenticate()
            initialise(project=project)
            watershed = watershed_from_gage(GAGE) if GAGE else watershed_from_point(LAT, LON)

            live_trajectory = cn_trajectory(
                watershed=watershed,
                project=project,
                years=YEARS,
                condition="fair",
                soils="sda",
                progress=lambda done, total, year: print("%d/%d  %d" % (done, total, year)),
            )
            print(live_trajectory)
            print(live_trajectory.summary())
        else:
            print("Reference trajectory active.")
            print("Set USE_EARTH_ENGINE=True to calculate a selected watershed trajectory.")
        '''),
        md(r'''
        ## Final reporting statement

        Write six lines:

        1. Lambda and curve-number calibration used.
        2. Land-cover source, vintage, and resolution.
        3. Soil source and unmapped fraction.
        4. Hydrologic condition and its poor-to-good sensitivity.
        5. Composite convention: distributed runoff, weighted CN, or weighted S.
        6. Measured trajectory beside the uncertainty band.

        **Source anchors:** USGS NWIS; ACIS/PRISM; NASA POWER; Annual NLCD;
        Woodward et al. (2003); NEH-630 Chapters 9 and 10.
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
