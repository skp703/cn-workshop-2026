import { feedbackUrl, repository, workshop } from "./workshop.mjs";

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

function investigationMarkup(module) {
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
        <p class="module-narrative">${escapeHtml(module.question)}</p>
        <div class="module-body">
          <div>
            <h4>What we examine</h4>
            ${list(module.concepts)}
          </div>
          <div class="investigation-plan">
            <p class="path-label">Guided core</p>
            <p>${escapeHtml(module.minimum)}</p>
            <p class="path-label">Participant extension</p>
            <p>${escapeHtml(module.extensions)}</p>
          </div>
        </div>
        <div class="takeaway"><span>Reportable result</span>${escapeHtml(module.result)}</div>
        <a class="source-link" href="${escapeHtml(module.notebook.source)}">Download notebook source</a>
      </div>
    </article>`;
}

function phaseMarkup() {
  return workshop.phases
    .map(
      (phase) => `
        <article class="phase-card">
          <span>${escapeHtml(phase.number)}</span>
          <p>${escapeHtml(phase.time)}</p>
          <h3>${escapeHtml(phase.title)}</h3>
          <div>${escapeHtml(phase.description)}</div>
        </article>`,
    )
    .join("");
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
        <a href="#modules">Investigations</a>
        <a href="#resources">Resources</a>
        <a href="#feedback">Feedback</a>
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
          <p class="aside-note">A common theory and Earth Engine introduction leads to four participant-directed hydrologic investigations.</p>
        </aside>
      </section>

      <section class="path-chooser" aria-labelledby="path-title">
        <div>
          <p class="eyebrow">Workshop design</p>
          <h2 id="path-title">A common foundation followed by participant inquiry.</h2>
          <p>Theory defines the model, Earth Engine introduces spatial evidence, and the notebooks provide room for investigation and interpretation.</p>
        </div>
        <div class="phase-grid">
          ${phaseMarkup()}
        </div>
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
          <h2 id="prepare-title">Prepare Colab and the Earth Engine Code Editor.</h2>
          <p>The readiness notebook verifies the computational environment. The Earth Engine guide supports the live web exercise and selected-watershed applications.</p>
        </div>
        <div class="prepare-grid">${prepareMarkup}</div>
        <div class="callout">
          <div>
            <strong>Guided Earth Engine exercise</strong>
            <p>The twenty-minute script introduces geometries, collections, visualization, pixel inspection, and grouped area reduction. The exploration interval provides four optional modifications.</p>
          </div>
          <a class="button button-light" href="./gee/README.md">Open the exercise</a>
        </div>
      </section>

      <section class="schedule section-shell" id="schedule" aria-labelledby="schedule-title">
        <div class="section-intro">
          <p class="eyebrow">Four hours · two breaks · four investigations</p>
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
          <p class="eyebrow">Participant inquiry</p>
          <h2 id="modules-title">Select one investigation and develop it.</h2>
          <p>Each notebook contains a guided analytical core, participant-selected extensions, verification steps, and a common reporting record.</p>
        </div>
        <div class="module-list">${workshop.investigations.map(investigationMarkup).join("")}</div>
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

      <section class="feedback section-shell" id="feedback" aria-labelledby="feedback-title">
        <div class="section-intro">
          <p class="eyebrow">Workshop evaluation</p>
          <h2 id="feedback-title">Help improve the next offering.</h2>
          <p>The anonymous form takes approximately five minutes and asks about conceptual clarity, the Earth Engine introduction, the investigation period, time allocation, and future topics.</p>
        </div>
        <a class="button" href="${escapeHtml(feedbackUrl)}" target="_blank" rel="noreferrer">Open workshop feedback form ↗</a>
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
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="A workshop on Curve Number theory, Google Earth Engine, and participant-directed hydrologic investigations.">
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
