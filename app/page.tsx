import type { Metadata } from "next";
import { renderWorkshopMarkup } from "../content/render.mjs";

export const metadata: Metadata = {
  title: "Modern Curve Number Hydrology · 2026 workshop",
  description:
    "A workshop on Curve Number theory, Google Earth Engine, and participant-directed hydrologic investigations.",
};

export default function Home() {
  return <div dangerouslySetInnerHTML={{ __html: renderWorkshopMarkup() }} />;
}
