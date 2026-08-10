# Getting started with Google Earth Engine

The workshop uses a twenty-minute guided exercise in the Earth Engine Code
Editor, followed by an optional exploration interval. The exercise introduces
the Earth Engine object model through one hydrologically relevant question:

> How can a cloud geospatial platform describe the land surface within a
> watershed boundary?

## Guided exercise

1. Open the [Earth Engine Code Editor](https://code.earthengine.google.com/).
2. Create a new script.
3. Copy the contents of [01_watershed_land_surface.js](https://github.com/skp703/cn-workshop-2026/blob/main/gee/01_watershed_land_surface.js) into the editor.
4. Run the script and inspect the map, Console, Layers panel, and pixel values.
5. During the exploration interval, complete one of the extension prompts at
   the end of the script.

The script introduces `Geometry`, `FeatureCollection`, `ImageCollection`,
filtering, band selection, clipping, visualization, `pixelArea`, grouped
reduction, and deferred execution. A satellite-image basemap remains beneath
the analytical layers for geographic context.

The HUC12 boundary is used as a compact teaching geometry. Investigation 2
develops watershed-outlet selection, delineation, boundary verification, and
Curve Number estimation in greater methodological detail.

## Continuing resources

- [Workshop GEE resource collection](https://github.com/skp703/RSTC_Workshop/tree/main/GEE#tutorials-from-the-web)
- [Official Earth Engine tutorials](https://developers.google.com/earth-engine/tutorials)
- [Beginner's Cookbook](https://developers.google.com/earth-engine/tutorials/community/beginners-cookbook)
- [Earth Engine data catalog](https://developers.google.com/earth-engine/datasets)
- [Spatial Thoughts Earth Engine course](https://spatialthoughts.com/courses/google-earth-engine/)

## Data sources

- USGS [Watershed Boundary Dataset HUC12](https://developers.google.com/earth-engine/datasets/catalog/USGS_WBD_2017_HUC12):
  `USGS/WBD/2017/HUC12`.
- USGS [NLCD 2019 release](https://developers.google.com/earth-engine/datasets/catalog/USGS_NLCD_RELEASES_2019_REL_NLCD):
  `USGS/NLCD_RELEASES/2019_REL/NLCD`.
- The complete workshop citation record is maintained in
  [`docs/SOURCES.md`](../docs/SOURCES.md).
