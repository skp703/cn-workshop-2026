export const feedbackUrl =
  "https://docs.google.com/forms/d/e/1FAIpQLSeavvSSEWlNcENVxCJZW9g22rztcJpi2Cd6ba6smZ9JX9toSA/viewform";

export const workshop = {
  title: "Modern Curve Number Hydrology",
  subtitle: "Theory, Earth Engine, and participant-directed investigations",
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
    "Develop the theoretical basis of the curve-number method, learn how Earth Engine summarizes watershed spatial data, and investigate a hydrologic question using reproducible notebooks.",
  outcomes: [
    "Explain the event runoff equation, its threshold, and the relationship among CN, retention, and initial abstraction.",
    "Distinguish table values, spatial estimates, and event-derived curve numbers.",
    "Use the Earth Engine Code Editor to visualize and summarize watershed land-surface data.",
    "Complete one participant-directed investigation and test an analytical choice or assumption.",
    "Report a quantitative result with its data sources, conventions, interpretation, and limitation.",
  ],
  phases: [
    {
      number: "01",
      title: "Curve Number theory",
      time: "30 minutes",
      description:
        "Develop the rainfall–runoff equation, threshold behavior, parameter conventions, spatial aggregation, and evidence bases used to estimate CN.",
    },
    {
      number: "02",
      title: "Getting started with Earth Engine",
      time: "20 minutes + exploration interval",
      description:
        "Use the web Code Editor to select a watershed-scale geometry, display NLCD layers over a background map, inspect pixels, and calculate a class-area summary.",
    },
    {
      number: "03",
      title: "Participant-directed investigations",
      time: "90 minutes",
      description:
        "Select one notebook, complete its guided analytical core, and extend the analysis through a participant-selected comparison or sensitivity question.",
    },
  ],
  schedule: [
    ["0:00", "Introduction and workshop outcomes", "10 min", "Both"],
    ["0:10", "Curve Number theory", "30 min", "John"],
    ["0:40", "Getting started with Google Earth Engine", "20 min", "Saurav"],
    ["1:00", "Break and optional GEE exploration", "20 min", "Both available"],
    ["1:20", "Introduce investigations and form groups", "10 min", "Both"],
    ["1:30", "Participant-directed notebook investigations", "90 min", "Both circulate"],
    ["3:00", "Break", "15 min", ""],
    ["3:15", "Participant report-outs and discussion", "30 min", "Both"],
    ["3:45", "Synthesis, resources, and feedback", "15 min", "Both"],
    ["4:00", "End", "", ""],
  ],
  investigations: [
    {
      number: "01",
      eyebrow: "Equation behavior",
      title: "CN equation and runoff response",
      question:
        "How do storm depth, lambda, and spatial aggregation alter calculated runoff?",
      concepts: [
        "Retention and the runoff threshold",
        "Lambda and paired parameter conventions",
        "Distributed versus composite runoff",
        "Storm-depth dependence of aggregation",
      ],
      minimum:
        "Complete the equation and compositing comparison, then preserve a baseline and one modified result.",
      extensions:
        "Change storm depth, lambda, or subarea heterogeneity and explain whether the interpretation changes.",
      result:
        "A figure or table comparing runoff under two explicitly stated conventions.",
      notebook: {
        label: "Open Investigation 1 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/01_CN_Equation_and_Runoff_Response.ipynb",
        source: "./notebooks/01_CN_Equation_and_Runoff_Response.ipynb",
      },
    },
    {
      number: "02",
      eyebrow: "Spatial estimation",
      title: "Spatial CN for a watershed",
      question:
        "How do watershed boundaries, land cover, soils, and spatial pairing determine a composite CN?",
      concepts: [
        "Outlet selection and boundary verification",
        "Land-cover and soil provenance",
        "Joint versus marginal distributions",
        "Composite CN and unmapped-area accounting",
      ],
      minimum:
        "Build or audit the boundary-to-runoff workflow using a reference watershed or a selected watershed through Earth Engine.",
      extensions:
        "Change the watershed, year, hydrologic condition, soil source, or pairing assumption while controlling the other inputs.",
      result:
        "A mapped boundary and composite CN with complete spatial provenance.",
      notebook: {
        label: "Open Investigation 2 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/02_Spatial_CN_for_a_Watershed.ipynb",
        source: "./notebooks/02_Spatial_CN_for_a_Watershed.ipynb",
      },
    },
    {
      number: "03",
      eyebrow: "Temporal evidence",
      title: "Land-cover change and design runoff",
      question:
        "How large is the mapped temporal signal relative to hydrologic-condition sensitivity?",
      concepts: [
        "Controlled multi-year CN trajectory",
        "Poor-to-good condition interval",
        "Signal-to-assumption comparison",
        "Translation from CN change to runoff change",
      ],
      minimum:
        "Calculate a trajectory, start-to-end change, condition spread, and corresponding design-runoff comparison.",
      extensions:
        "Change the time interval, design rainfall, or watershed and evaluate the stability of the conclusion.",
      result:
        "A trajectory and a quantitative comparison between mapped change and methodological sensitivity.",
      notebook: {
        label: "Open Investigation 3 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/03_Land_Cover_Change_and_Design_Runoff.ipynb",
        source: "./notebooks/03_Land_Cover_Change_and_Design_Runoff.ipynb",
      },
    },
    {
      number: "04",
      eyebrow: "Observed response",
      title: "Event-derived CN and antecedent state",
      question:
        "What CN values are supported by observed events, and how do antecedent-state conventions affect interpretation?",
      concepts: [
        "Inverse rainfall–runoff equation",
        "Hawkins asymptotic response",
        "Lambda as part of the calibration",
        "Rainfall history versus root-zone wetness",
      ],
      minimum:
        "Fit an event-derived response and compare two antecedent-state classifications on the same storm dates.",
      extensions:
        "Change the watershed, lambda, event screening, or climatology window and evaluate the stability of the result.",
      result:
        "A fitted CN record and an antecedent-state comparison with diagnostics and limitations.",
      notebook: {
        label: "Open Investigation 4 in Colab",
        href: "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/04_Event_CN_and_Antecedent_State.ipynb",
        source: "./notebooks/04_Event_CN_and_Antecedent_State.ipynb",
      },
    },
  ],
  evidence: [
    ["0.29", "CN units", "mapped Difficult Run change, 2001–2019"],
    ["8.45", "CN units", "poor-to-good hydrologic-condition spread"],
    ["1.88", "CN units", "effect of the spatial independence assumption"],
    ["5.8", "CN units", "table value above fitted Difficult Run value"],
  ],
  preparedWatersheds: [
    ["Difficult Run, VA", "Suburban Piedmont", "Complete reference basin"],
    ["Accotink Creek, VA", "Urban Coastal Plain", "Contrasting event response"],
  ],
  prepare: [
    {
      title: "General preparation",
      items: [
        "Bring a laptop and charger.",
        "Use a modern browser and a Google account if you want to save Colab copies.",
        "Open the readiness notebook once before the workshop.",
      ],
    },
    {
      title: "Earth Engine preparation",
      items: [
        "Create or select a Google Cloud project.",
        "Enable and register the project for Earth Engine.",
        "Open the Code Editor and run the readiness check.",
      ],
    },
    {
      title: "Investigation selection",
      items: [
        "Review the four investigation questions before the notebook period.",
        "Bring a USGS gage number or outlet coordinates for a selected watershed application.",
        "Reference datasets support every investigation and reporting requirement.",
      ],
    },
  ],
  resources: [
    ["GEE guided exercise", "Twenty-minute Code Editor exercise and optional exploration prompts", "./gee/README.md"],
    ["Extended GEE tutorials", "Official, community, and hydrology-focused continuing resources", "https://github.com/skp703/RSTC_Workshop/tree/main/GEE#tutorials-from-the-web"],
    ["Earth Engine setup", "Project registration, authentication, and Colab initialization", "./docs/GEE_SETUP.md"],
    ["Readiness check", "Verify Colab, cnkit, reference data, and Earth Engine access", "https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/00_Readiness_Check.ipynb"],
    ["Workshop data", "Versioned, checksum-verified prepared inputs", "./downloads/cn_workshop_v3_data.zip"],
    ["cnkit", "Installable hydrology library and API documentation", "https://github.com/skp703/cnkit"],
    ["Lecture deck", "CN theory, GEE orientation, investigation launch, and synthesis", "./downloads/2026_CN_Workshop_v3.pptx"],
    ["Participant guide", "Workshop preparation, navigation, and reporting expectations", "./docs/PARTICIPANT_GUIDE.md"],
    ["Sources and citations", "Verified method, dataset, and service references used throughout the workshop", "./docs/SOURCES.md"],
    ["Workshop feedback", "Anonymous five-minute evaluation form", feedbackUrl],
  ],
};

export const repository = {
  owner: "skp703",
  name: "cn-workshop-2026",
  url: "https://github.com/skp703/cn-workshop-2026",
  pages: "https://skp703.github.io/cn-workshop-2026/",
};
