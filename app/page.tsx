import type { Metadata } from "next";
import { renderWorkshopMarkup } from "../content/render.mjs";

export const metadata: Metadata = {
  title: "Modern Curve Number Hydrology · 2026 workshop",
  description:
    "A workshop on curve-number theory, spatial estimation, and Earth Observation applications.",
};

export default function Home() {
  return <div dangerouslySetInnerHTML={{ __html: renderWorkshopMarkup() }} />;
}
