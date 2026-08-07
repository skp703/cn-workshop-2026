export const workshop = {
  title: "Modern Curve Number Hydrology",
  subtitle: "Theory, spatial estimation, and Earth Observation applications",
  conference: "2026 ASCE–EWRI Watershed Management Conference",
  duration: "Four hours · 4.0 PDH",
  instructors: [
    {
      name: "John J. Ramirez-Avila",
      affiliation: "Mississippi State University",
    },
    {
      name: "Saurav Kumar",
      affiliation: "Arizona State University",
    },
  ],
  promise:
    "Evaluate the theoretical basis of the curve-number method, estimate its parameters from spatial data, and document the assumptions that govern interpretation.",
  paths: {
    core: {
      label: "Reference data pathway",
      short: "Use verified workshop datasets",
      description:
        "Use verified land-cover, soil, rainfall, runoff, and soil-moisture datasets for the two workshop watersheds. This pathway supports the complete sequence of analyses and interpretations.",
    },
    gee: {
      label: "Earth Engine application",
      short: "Analyze a selected watershed",
      description:
        "Use a registered Earth Engine project with a USGS gage number or outlet coordinates to repeat the spatial analysis for a selected watershed.",
    },
  },
  outcomes: [
    "Explain the curve-number equation, its calibration constants, and its limits.",
    "Delineate and verify a watershed boundary from a gage or outlet point.",
    "Build a composite curve number from land cover and hydrologic soil group.",
    "Compare measured change with uncertainty from condition, soil gaps, and compositing.",
    "Formulate a reproducible engineering-report statement and justify its assumptions.",
  ],
  schedule: [
    ["0:00", "Welcome and what you will build", "10 min", "Both"],
    ["0:10", "Introduction: from rainfall to curve number", "40 min", "John"],
    ["0:50", "Lab 1: understand and audit the equation", "20 min", "Both circulate"],
    ["1:10", "Report-out 1", "10 min", "John"],
    ["1:20", "Break", "15 min", ""],
    ["1:35", "From lookup tables to Earth Observation", "25 min", "Saurav"],
    ["2:00", "Lab 2: build a CN for a watershed", "35 min", "Both circulate"],
    ["2:35", "Report-out 2", "10 min", "Saurav"],
    ["2:45", "Break", "15 min", ""],
    ["3:00", "Change, antecedent condition, and uncertainty", "20 min", "Saurav"],
    ["3:20", "Lab 3: change and uncertainty", "25 min", "Both circulate"],
    ["3:45", "What would you defend in a report?", "15 min", "Both"],
    ["4:00", "End", "", ""],
  ],
  modules: [
    {
      number: "01",
      eyebrow: "Foundations",
      title: "The theoretical basis of the method",
      time: "0:10–1:20",
      narrative:
        "Start with the observation, derive the equation, and make the conventions visible before touching a satellite product.",
      concepts: [
        "Rainfall, initial abstraction, retention, and runoff",
        "What a curve number is—and is not",
        "Hydrologic soil group, land cover, and hydrologic condition",
        "Lambda 0.20 versus 0.05",
        "The composite-CN weighting trap",
      ],
      notebook: {
        label: "Open Lab 1 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/01_Understand_the_Curve_Number.ipynb",
        source: "./notebooks/01_Understand_the_Curve_Number.ipynb",
      },
      core:
        "Complete the analytical examples using the runoff equation and small embedded datasets.",
      gee:
        "Complete the same analytical examples. Earth Engine enters in the spatial-estimation module after the theoretical framework is established.",
      takeaway:
        "A curve number is an index fitted to a rainfall–runoff relation, not a directly observed property of a pixel.",
    },
    {
      number: "02",
      eyebrow: "Spatial estimation",
      title: "Estimating a curve number for a watershed",
      time: "1:35–2:45",
      narrative:
        "Move from two independent lookup tables to a spatial measurement and compare the implications of alternative data sources.",
      concepts: [
        "Watershed delineation and boundary verification",
        "Land-cover and soil provenance",
        "Marginal versus joint distributions",
        "Unmapped soil and resolution mismatch",
        "Composite CN with uncertainty stated",
      ],
      notebook: {
        label: "Open Lab 2 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/02_Build_CN_for_a_Watershed.ipynb",
        source: "./notebooks/02_Build_CN_for_a_Watershed.ipynb",
      },
      core:
        "Select Difficult Run or Accotink Creek and examine verified land-cover, soil, joint-distribution, and provenance records.",
      gee:
        "Enter a USGS gage or outlet coordinates, delineate the basin, retrieve land cover and soils, and estimate the joint distribution pixel by pixel.",
      takeaway:
        "The joint spatial distribution removes an independence assumption whose effect exceeds the measured land-cover trend.",
    },
    {
      number: "03",
      eyebrow: "Evaluation",
      title: "Temporal change, antecedent state, and uncertainty",
      time: "3:00–4:00",
      narrative:
        "Put a measured trajectory inside the uncertainty band created by the method, then decide what belongs in a report.",
      concepts: [
        "Multi-year CN trajectory",
        "Poor–fair–good hydrologic-condition band",
        "Asymptotic CN from measured storms",
        "Antecedent rainfall versus observed soil moisture",
        "A defensible provenance statement",
      ],
      notebook: {
        label: "Open Lab 3 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/03_Change_and_Uncertainty.ipynb",
        source: "./notebooks/03_Change_and_Uncertainty.ipynb",
      },
      core:
        "Analyze verified trajectories and storm records for the reference watersheds, including fitted curve numbers and antecedent soil-moisture comparisons.",
      gee:
        "Generate a trajectory and condition band for a selected watershed, then compare its scale with the measured-gage evidence from the reference watersheds.",
      takeaway:
        "Improved inputs make the remaining methodological uncertainty explicit; report the trajectory with its condition band and assumptions.",
    },
  ],
  evidence: [
    ["0.29", "CN units", "live GEE land-cover change, 2001–2019"],
    ["8.45", "CN units", "live GEE hydrologic-condition spread"],
    ["1.88", "CN units", "independence assumption, measured with the same raster marginals"],
    ["5.8", "CN units", "table value above the fitted value at Difficult Run"],
  ],
  preparedWatersheds: [
    ["Difficult Run, VA", "Suburban Piedmont", "Complete reference basin"],
    ["Accotink Creek, VA", "Urban Coastal Plain", "Contrasting fitted behavior"],
  ],
  prepare: [
    {
      title: "General preparation",
      items: [
        "Bring a laptop and charger.",
        "Use a modern browser and a Google account if you want to save a Colab copy.",
        "Open the readiness notebook once before the workshop.",
      ],
    },
    {
      title: "Earth Engine preparation",
      items: [
        "Create or select a Google Cloud project.",
        "Enable and register the project for Earth Engine.",
        "Run the one-minute authentication check in Colab.",
      ],
    },
    {
      title: "Watershed selection",
      items: [
        "A USGS gage number provides the most direct watershed identifier.",
        "Outlet latitude and longitude also work for CONUS basins.",
        "The reference watersheds are also available for the laboratory analysis.",
      ],
    },
  ],
  resources: [
    ["Earth Engine setup", "Project registration, authentication, and Colab initialization", "./docs/GEE_SETUP.md"],
    ["Readiness check", "Verify Colab, cnkit, reference data, and Earth Engine access", "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/00_Readiness_Check.ipynb"],
    ["Workshop data", "Versioned, checksum-verified prepared inputs", "./downloads/cn_workshop_v3_data.zip"],
    ["cnkit", "Installable hydrology library and API documentation", "https://github.com/skp703/cnkit"],
    ["Lecture deck", "Complete v3 lecture and exercise slides", "./downloads/2026_CN_Workshop_v3.pptx"],
    ["Participant guide", "Workshop preparation, navigation, and deliverables", "./docs/PARTICIPANT_GUIDE.md"],
  ],
};

export const repository = {
  owner: "skp703",
  name: "cn-workshop-2026",
  url: "https://github.com/skp703/cn-workshop-2026",
  pages: "https://skp703.github.io/cn-workshop-2026/",
};
