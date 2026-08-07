import { repository, workshop } from "./workshop.mjs";

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

const list = (items) =>
  `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;

function scheduleRows() {
  return workshop.schedule
    .map(
      ([time, activity, duration, lead]) => `
        <tr>
          <th scope="row">${escapeHtml(time)}</th>
          <td>${escapeHtml(activity)}</td>
          <td>${escapeHtml(duration)}</td>
          <td>${escapeHtml(lead)}</td>
        </tr>`,
    )
    .join("");
}

function moduleMarkup(module) {
  return `
    <article class="module" id="module-${module.number}">
      <div class="module-index" aria-hidden="true">${module.number}</div>
      <div class="module-main">
        <div class="module-heading">
          <div>
            <p class="eyebrow">${escapeHtml(module.eyebrow)} · ${escapeHtml(module.time)}</p>
            <h3>${escapeHtml(module.title)}</h3>
          </div>
          <a class="button button-small" href="${escapeHtml(module.notebook.href)}" target="_blank" rel="noreferrer">
            ${escapeHtml(module.notebook.label)} <span aria-hidden="true">↗</span>
          </a>
        </div>
        <p class="module-narrative">${escapeHtml(module.narrative)}</p>
        <div class="module-body">
          <div>
            <h4>What we examine</h4>
            ${list(module.concepts)}
          </div>
          <div class="path-panel path-panel-core" data-path-panel="core">
            <p class="path-label">Reference data pathway</p>
            <p>${escapeHtml(module.core)}</p>
          </div>
          <div class="path-panel path-panel-gee" data-path-panel="gee">
            <p class="path-label">Earth Engine application</p>
            <p>${escapeHtml(module.gee)}</p>
          </div>
        </div>
        <div class="takeaway"><span>Interpretation</span>${escapeHtml(module.takeaway)}</div>
        <a class="source-link" href="${escapeHtml(module.notebook.source)}">Download notebook source</a>
      </div>
    </article>`;
}

function resourceMarkup() {
  return workshop.resources
    .map(
      ([title, description, href]) => `
        <a class="resource" href="${escapeHtml(href)}">
          <span class="resource-arrow" aria-hidden="true">↗</span>
          <strong>${escapeHtml(title)}</strong>
          <span>${escapeHtml(description)}</span>
        </a>`,
    )
    .join("");
}

export function renderWorkshopMarkup() {
  const instructors = workshop.instructors
    .map(
      (person) => `
        <div>
          <strong>${escapeHtml(person.name)}</strong>
          <span>${escapeHtml(person.affiliation)}</span>
        </div>`,
    )
    .join("");

  const outcomeMarkup = workshop.outcomes
    .map(
      (outcome, index) => `
        <li><span>${String(index + 1).padStart(2, "0")}</span>${escapeHtml(outcome)}</li>`,
    )
    .join("");

  const evidenceMarkup = workshop.evidence
    .map(
      ([value, unit, label]) => `
        <div class="evidence-item">
          <div><strong>${escapeHtml(value)}</strong><span>${escapeHtml(unit)}</span></div>
          <p>${escapeHtml(label)}</p>
        </div>`,
    )
    .join("");

  const prepareMarkup = workshop.prepare
    .map(
      (group) => `
        <div class="prepare-group">
          <h3>${escapeHtml(group.title)}</h3>
          ${list(group.items)}
        </div>`,
    )
    .join("");

  const watershedRows = workshop.preparedWatersheds
    .map(
      ([name, character, use]) => `
        <tr><th scope="row">${escapeHtml(name)}</th><td>${escapeHtml(character)}</td><td>${escapeHtml(use)}</td></tr>`,
    )
    .join("");

  return `
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <a class="wordmark" href="#top" aria-label="Workshop home">
        <span class="wordmark-mark">CN</span>
        <span>Modern Curve Number Hydrology</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="#prepare">Prepare</a>
        <a href="#schedule">Schedule</a>
        <a href="#modules">Labs</a>
        <a href="#resources">Resources</a>
      </nav>
      <a class="github-link" href="${repository.url}">GitHub <span aria-hidden="true">↗</span></a>
    </header>

    <main id="main">
      <section class="hero" id="top">
        <div class="hero-copy">
          <p class="eyebrow">${escapeHtml(workshop.conference)}</p>
          <h1>${escapeHtml(workshop.title)}</h1>
          <p class="hero-subtitle">${escapeHtml(workshop.subtitle)}</p>
          <p class="hero-promise">${escapeHtml(workshop.promise)}</p>
          <div class="hero-actions">
            <a class="button" href="#prepare">Preparation</a>
            <a class="text-link" href="https://colab.research.google.com/github/skp703/cn-workshop-2026/blob/main/notebooks/00_Readiness_Check.ipynb" target="_blank" rel="noreferrer">Run the readiness check ↗</a>
          </div>
        </div>
        <aside class="hero-aside" aria-label="Workshop information">
          <p class="aside-kicker">Workshop</p>
          <p class="aside-duration">${escapeHtml(workshop.duration)}</p>
          <div class="instructors">${instructors}</div>
          <p class="aside-note">Reference datasets support the full workshop sequence. Earth Engine resources extend the analysis to a participant-selected watershed.</p>
        </aside>
      </section>

      <section class="path-chooser" aria-labelledby="path-title">
        <div>
          <p class="eyebrow">Data pathways</p>
          <h2 id="path-title">Use verified reference data or apply the workflow through Earth Engine.</h2>
          <p>Both pathways use the same analytical framework, result tables, figures, and discussion questions.</p>
        </div>
        <div class="path-controls" role="group" aria-label="Workshop data path">
          <button type="button" data-path-choice="core" aria-pressed="true">
            <span>${escapeHtml(workshop.paths.core.label)}</span>
            <small>${escapeHtml(workshop.paths.core.short)}</small>
          </button>
          <button type="button" data-path-choice="gee" aria-pressed="false">
            <span>${escapeHtml(workshop.paths.gee.label)}</span>
            <small>${escapeHtml(workshop.paths.gee.short)}</small>
          </button>
        </div>
        <p class="path-description" data-path-description="core">${escapeHtml(workshop.paths.core.description)}</p>
        <p class="path-description" data-path-description="gee" hidden>${escapeHtml(workshop.paths.gee.description)}</p>
      </section>

      <section class="outcomes section-shell" aria-labelledby="outcomes-title">
        <div class="section-intro">
          <p class="eyebrow">Learning objectives</p>
          <h2 id="outcomes-title">Explain, reproduce, and critically evaluate a curve-number estimate.</h2>
        </div>
        <ol>${outcomeMarkup}</ol>
      </section>

      <section class="evidence" aria-label="Four numbers that anchor the workshop">
        <div class="evidence-lead">
          <p class="eyebrow">Comparative scale</p>
          <h2>Methodological assumptions can exceed the observed temporal signal.</h2>
        </div>
        ${evidenceMarkup}
      </section>

      <section class="prepare section-shell" id="prepare" aria-labelledby="prepare-title">
        <div class="section-intro">
          <p class="eyebrow">Preparation</p>
          <h2 id="prepare-title">Prepare Colab and, if desired, an Earth Engine project.</h2>
          <p>The workshop runs in Google Colab. The readiness notebook verifies the reference-data environment and can also verify an Earth Engine project.</p>
        </div>
        <div class="prepare-grid">${prepareMarkup}</div>
        <div class="callout">
          <div>
            <strong>Earth Engine resources</strong>
            <p>The setup guide covers project registration, authentication, and initialization. Participants may use Earth Engine for a selected watershed or conduct the complete analysis with the workshop reference datasets.</p>
          </div>
          <a class="button button-light" href="./docs/GEE_SETUP.md">Earth Engine setup</a>
        </div>
      </section>

      <section class="schedule section-shell" id="schedule" aria-labelledby="schedule-title">
        <div class="section-intro">
          <p class="eyebrow">Four hours · two breaks · three labs</p>
          <h2 id="schedule-title">Workshop schedule</h2>
          <p>This run of show is shared by the site, notebooks, lecture deck, and instructor guide.</p>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Time</th><th>Block</th><th>Duration</th><th>Lead</th></tr></thead>
            <tbody>${scheduleRows()}</tbody>
          </table>
        </div>
      </section>

      <section class="modules section-shell" id="modules" aria-labelledby="modules-title">
        <div class="section-intro">
          <p class="eyebrow">The learning arc</p>
          <h2 id="modules-title">Theory, spatial estimation, and interpretation.</h2>
          <p>Three integrated labs move from the governing equations to spatial inputs, temporal change, and the documentation required for engineering interpretation.</p>
        </div>
        <div class="module-list">${workshop.modules.map(moduleMarkup).join("")}</div>
      </section>

      <section class="watersheds section-shell" aria-labelledby="watersheds-title">
        <div class="section-intro">
          <p class="eyebrow">Reference watersheds</p>
          <h2 id="watersheds-title">Two verified basins support the complete analytical sequence.</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Watershed</th><th>Character</th><th>Role in the workshop</th></tr></thead>
            <tbody>${watershedRows}</tbody>
          </table>
        </div>
      </section>

      <section class="resources section-shell" id="resources" aria-labelledby="resources-title">
        <div class="section-intro">
          <p class="eyebrow">Workshop materials</p>
          <h2 id="resources-title">Notebooks, data, slides, code, and source documentation</h2>
          <p>Notebooks, data, slides, code, sources, and setup instructions live together in the public repository.</p>
        </div>
        <div class="resource-list">${resourceMarkup()}</div>
      </section>
    </main>

    <footer>
      <div>
        <strong>${escapeHtml(workshop.title)}</strong>
        <span>${escapeHtml(workshop.conference)}</span>
      </div>
      <p>EWRI Curve Number Hydrology Task Committee · EWRI Remote Sensing Task Committee</p>
      <a href="#top">Back to top ↑</a>
    </footer>`;
}

export function renderSiteDocument({ base = "./" } = {}) {
  return `<!doctype html>
<html lang="en" data-path="core">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="A workshop on curve-number theory, spatial estimation, and Earth Observation applications.">
    <meta name="theme-color" content="#12244b">
    <meta property="og:title" content="${escapeHtml(workshop.title)}">
    <meta property="og:description" content="${escapeHtml(workshop.subtitle)}">
    <meta property="og:image" content="https://skp703.github.io/cn-workshop-2026/og.png">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <title>${escapeHtml(workshop.title)} · 2026 workshop</title>
    <link rel="stylesheet" href="${base}workshop.css">
    <script src="${base}workshop.js" defer></script>
  </head>
  <body>${renderWorkshopMarkup()}</body>
</html>`;
}
