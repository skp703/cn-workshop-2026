/* global ee */

// Modern Curve Number Hydrology — Getting started with Earth Engine
// Question: How can Earth Engine describe the land surface within a watershed?

// -----------------------------------------------------------------------------
// 1. Define an outlet used only to select a teaching watershed.
// Earth Engine coordinates use longitude, latitude order.
// -----------------------------------------------------------------------------
var outlet = ee.Geometry.Point([-77.24581, 38.97594]);

// A FeatureCollection is a server-side collection of vector features.
var huc12Collection = ee.FeatureCollection('USGS/WBD/2017/HUC12');

// Select the smallest HUC12 feature intersecting the point.
var watershed = ee.Feature(
  huc12Collection.filterBounds(outlet).sort('areasqkm').first()
);

print('Outlet geometry', outlet);
print('Selected HUC12 feature', watershed);
print('HUC12 name', watershed.get('name'));
print('Published HUC12 area, km2', watershed.get('areasqkm'));

// The HYBRID basemap supplies geographic context; it is not used in analysis.
Map.setOptions('HYBRID');
Map.centerObject(watershed, 11);
Map.addLayer(
  ee.FeatureCollection([watershed]).style({
    color: '00D5E6',
    fillColor: '00000000',
    width: 3
  }),
  {},
  'HUC12 boundary'
);
Map.addLayer(outlet, {color: 'F6C344'}, 'Selection point');

// -----------------------------------------------------------------------------
// 2. Load an ImageCollection and select one year.
// Change YEAR to another available epoch such as 2001, 2006, 2011, or 2016.
// -----------------------------------------------------------------------------
var YEAR = 2019;
var nlcdCollection = ee.ImageCollection('USGS/NLCD_RELEASES/2019_REL/NLCD');
var nlcd = ee.Image(
  nlcdCollection.filter(ee.Filter.eq('system:index', String(YEAR))).first()
);

print('NLCD ImageCollection', nlcdCollection);
print('Selected NLCD image', nlcd);
print('Selected image band names', nlcd.bandNames());

// select() identifies analytical bands; clip() limits their display and
// subsequent reduction to the selected geometry.
var landcover = nlcd.select('landcover').clip(watershed.geometry());
var impervious = nlcd.select('impervious').clip(watershed.geometry());

var classCodes = [11, 12, 21, 22, 23, 24, 31, 41, 42, 43, 52, 71, 81, 82, 90, 95];
var classPalette = [
  '466B9F', 'D1DEF8', 'DEC5C5', 'D99282',
  'EB0000', 'AB0000', 'B3AC9F', '68AB5F',
  '1C5F2C', 'B5C58F', 'CCBA7C', 'E3E3C2',
  'DCD939', 'AB6C28', 'B8D9EB', '6C9FB8'
];

// Remapping produces consecutive display indices without changing the source
// class codes used for the calculation below.
var landcoverDisplay = landcover.remap(
  classCodes,
  ee.List.sequence(0, classCodes.length - 1)
);

Map.addLayer(
  landcoverDisplay,
  {min: 0, max: classCodes.length - 1, palette: classPalette},
  'NLCD land cover ' + YEAR,
  true,
  0.78
);
Map.addLayer(
  impervious,
  {min: 0, max: 100, palette: ['FFFFFF', 'F7B267', 'B21F35']},
  'NLCD imperviousness ' + YEAR,
  false,
  0.82
);

// -----------------------------------------------------------------------------
// 3. Reduce the raster to a class-area table.
// pixelArea() supplies square metres. Division by 1e6 reports square kilometres.
// The class band is the second band, so groupField is 1.
// -----------------------------------------------------------------------------
var areaAndClass = ee.Image.pixelArea()
  .divide(1e6)
  .rename('area_km2')
  .addBands(landcover.rename('class'));

var classAreas = areaAndClass.reduceRegion({
  reducer: ee.Reducer.sum().group({
    groupField: 1,
    groupName: 'class'
  }),
  geometry: watershed.geometry(),
  scale: 30,
  maxPixels: 1e10,
  tileScale: 4
});

print('NLCD class areas, km2', classAreas.get('groups'));

// Earth Engine constructs a server-side computation graph. Map layers and
// print statements request evaluation; the variables above are not local pixel
// arrays transferred to the browser.

// -----------------------------------------------------------------------------
// Exploration interval — choose one change, rerun, and interpret the result.
// -----------------------------------------------------------------------------
// A. Change YEAR and compare the mapped pattern or class-area table.
// B. Move the outlet to a familiar location and inspect the selected HUC12.
// C. Turn imperviousness on in the Layers panel and inspect values with Inspector.
// D. Add another catalog layer and print its band names and metadata.
