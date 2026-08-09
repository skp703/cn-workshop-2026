import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("renders the participant-first workshop portal", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /Modern Curve Number Hydrology/);
  assert.match(html, /Curve Number theory/);
  assert.match(html, /Getting started with Google Earth Engine/);
  assert.match(html, /Participant-directed notebook investigations/);
  assert.match(html, /Select one investigation and develop it/);
  assert.match(html, /Learning objectives/);
  assert.doesNotMatch(html, /never required|three-minute rule|Two paths\. One learning journey/i);
  assert.match(html, /0:00/);
  assert.match(html, /4:00/);
  assert.match(html, /Open workshop feedback form/);
  assert.match(html, /01_CN_Equation_and_Runoff_Response\.ipynb/);
  assert.match(html, /04_Event_CN_and_Antecedent_State\.ipynb/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("exports a static GitHub Pages version with workshop assets", async () => {
  const [html, css, js, gee] = await Promise.all([
    readFile(new URL("../dist-pages/index.html", import.meta.url), "utf8"),
    readFile(new URL("../dist-pages/workshop.css", import.meta.url), "utf8"),
    readFile(new URL("../dist-pages/workshop.js", import.meta.url), "utf8"),
    readFile(new URL("../dist-pages/gee/01_watershed_land_surface.js", import.meta.url), "utf8"),
  ]);

  assert.match(html, /workshop\.css/);
  assert.match(html, /00_Readiness_Check\.ipynb/);
  assert.match(css, /--navy:\s*#12244b/);
  assert.match(js, /classList\.add\("js"\)/);
  assert.match(gee, /USGS\/WBD\/2017\/HUC12/);
  await access(new URL("../dist-pages/.nojekyll", import.meta.url));
  await access(new URL("../dist-pages/og.png", import.meta.url));
});
