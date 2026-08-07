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
  assert.match(html, /Reference data pathway/);
  assert.match(html, /Earth Engine application/);
  assert.match(html, /Theory, spatial estimation, and interpretation/);
  assert.match(html, /Learning objectives/);
  assert.doesNotMatch(html, /never required|three-minute rule|Two paths\. One learning journey/i);
  assert.match(html, /0:00/);
  assert.match(html, /4:00/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("exports a static GitHub Pages version with workshop assets", async () => {
  const [html, css, js] = await Promise.all([
    readFile(new URL("../dist-pages/index.html", import.meta.url), "utf8"),
    readFile(new URL("../dist-pages/workshop.css", import.meta.url), "utf8"),
    readFile(new URL("../dist-pages/workshop.js", import.meta.url), "utf8"),
  ]);

  assert.match(html, /workshop\.css/);
  assert.match(html, /00_Readiness_Check\.ipynb/);
  assert.match(css, /--navy:\s*#12244b/);
  assert.match(js, /cn-workshop-path/);
  await access(new URL("../dist-pages/.nojekyll", import.meta.url));
  await access(new URL("../dist-pages/og.png", import.meta.url));
});
