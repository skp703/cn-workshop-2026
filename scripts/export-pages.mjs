import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { renderSiteDocument } from "../content/render.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const output = resolve(root, "dist-pages");

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await writeFile(resolve(output, "index.html"), renderSiteDocument(), "utf8");

for (const file of ["workshop.css", "workshop.js", "og.png"]) {
  await cp(resolve(root, "public", file), resolve(output, file));
}

for (const folder of ["notebooks", "docs", "downloads"]) {
  await cp(resolve(root, folder), resolve(output, folder), { recursive: true });
}

await writeFile(resolve(output, ".nojekyll"), "", "utf8");
console.log(`GitHub Pages export written to ${output}`);
