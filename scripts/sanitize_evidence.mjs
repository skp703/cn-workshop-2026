import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const introductions = {
  "D2_executed_2026-08-06.ipynb": [
    "# D2. A curve number from Earth Engine\n",
    "\n",
    "This validation record applies the spatial curve-number workflow to Difficult Run near Great Falls, Virginia. It was executed on 6 August 2026 with `cnkit` 1.1.0, a registered Earth Engine project, USGS watershed delineation, Annual NLCD, and Soil Data Access.\n",
    "\n",
    "The analysis estimates the observed joint distribution of land cover and hydrologic soil group, calculates a composite curve number, and retains the source, scale, coverage, and unmapped-area fields needed for interpretation. The reference basin generally completes in two to four minutes.\n",
    "\n",
    "Notebook D1 supplies the watershed boundary used here. The executed outputs below support the values reported in the workshop materials.\n",
  ],
  "D3_executed_2026-08-06.ipynb": [
    "# D3. Curve-number change and methodological uncertainty\n",
    "\n",
    "This validation record evaluates a seven-year curve-number trajectory for Difficult Run near Great Falls, Virginia. It was executed on 6 August 2026 with `cnkit` 1.1.0, a registered Earth Engine project, USGS watershed delineation, Annual NLCD, and Soil Data Access.\n",
    "\n",
    "Each year uses the same watershed, soil source, lookup implementation, and reporting schema. The analysis reports the fair-condition trajectory together with the poor-to-good condition range, runoff estimate, unmapped area, and data provenance. The reference sequence generally completes in two to five minutes.\n",
    "\n",
    "The executed outputs below support the trajectory and uncertainty comparisons reported in the workshop materials.\n",
  ],
};

function removePrivateRuntimeMetadata(value) {
  if (Array.isArray(value)) {
    value.forEach(removePrivateRuntimeMetadata);
    return;
  }
  if (!value || typeof value !== "object") return;

  for (const key of ["executionInfo", "outputId", "user", "userId"]) {
    delete value[key];
  }
  Object.values(value).forEach(removePrivateRuntimeMetadata);
}

for (const [filename, source] of Object.entries(introductions)) {
  const path = resolve(root, "evidence", "gee-live", filename);
  const notebook = JSON.parse(await readFile(path, "utf8"));
  notebook.cells[0].source = source;
  removePrivateRuntimeMetadata(notebook);
  await writeFile(path, `${JSON.stringify(notebook, null, 1)}\n`);
  console.log(`sanitized evidence/gee-live/${filename}`);
}
