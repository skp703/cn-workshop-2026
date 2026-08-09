# Sources and citation record

This source ledger distinguishes model references, empirical-method papers,
data products, and web services used in the workshop. Bibliographic details and
DOIs were checked against publisher or agency records on 9 August 2026.

## Curve Number methods

- U.S. Department of Agriculture, Natural Resources Conservation Service.
  2004. *National Engineering Handbook, Part 630, Chapter 10: Estimation of
  Direct Runoff from Storm Rainfall*. July 2004. Equations 10-1 and 10-10
  through 10-13 are the numbering used in the notebooks.
  [Official PDF](https://directives.nrcs.usda.gov/sites/default/files2/1712930608/7300.pdf).
- U.S. Department of Agriculture, Natural Resources Conservation Service.
  2025. *Title 210—National Engineering Handbook, Part 630, Subpart H:
  Estimation of Direct Runoff from Storm Rainfall*. Amended August 2025.
  [Official PDF](https://directives.nrcs.usda.gov/sites/default/files2/1754923466/Subpart%20H%20%E2%80%93%20Estimation%20of%20Direct%20Runoff%20from%20Storm%20Rainfall.pdf).
- U.S. Department of Agriculture, Soil Conservation Service. 1986. *Urban
  Hydrology for Small Watersheds*. Technical Release 55, second edition,
  210-VI-TR-55. Washington, DC.
- Hawkins, R. H. 1993. “Asymptotic Determination of Runoff Curve Numbers from
  Data.” *Journal of Irrigation and Drainage Engineering* 119(2):334–345.
  [doi:10.1061/(ASCE)0733-9437(1993)119:2(334)](https://doi.org/10.1061/%28ASCE%290733-9437%281993%29119%3A2%28334%29).
- Woodward, D. E., R. H. Hawkins, R. Jiang, A. T. Hjelmfelt Jr., J. A. Van
  Mullem, and Q. D. Quan. 2003. “Runoff Curve Number Method: Examination of the
  Initial Abstraction Ratio.” *World Water & Environmental Resources Congress
  2003*, 1–10.
  [doi:10.1061/40685(2003)308](https://doi.org/10.1061/40685%282003%29308).
- Hawkins, R. H., A. T. Hjelmfelt Jr., and A. W. Zevenbergen. 1985. “Runoff
  Probability, Storm Depth, and Curve Numbers.” *Journal of Irrigation and
  Drainage Engineering* 111(4):330–340.
  [doi:10.1061/(ASCE)0733-9437(1985)111:4(330)](https://doi.org/10.1061/%28ASCE%290733-9437%281985%29111%3A4%28330%29).
- Moglen, G. E., H. Sadeq, L. H. Hughes II, M. E. Meadows, J. J. Miller,
  J. J. Ramirez-Avila, and E. W. Tollner. 2022. “NRCS Curve Number Method:
  Comparison of Methods for Estimating the Curve Number from Rainfall-Runoff
  Data.” *Journal of Hydrologic Engineering* 27(10).
  [doi:10.1061/(ASCE)HE.1943-5584.0002210](https://doi.org/10.1061/%28ASCE%29HE.1943-5584.0002210).

The 1993 Hawkins paper supports the asymptotic rainfall–runoff analysis. The
2003 Woodward-first-author paper supports the initial-abstraction-ratio study
and associated CN conversion. These are separate methods and citations.

## Watershed and hydrologic observations

- U.S. Geological Survey. *USGS Water Data for the Nation: National Water
  Information System database*. Accessed 9 August 2026.
  [doi:10.5066/F7P55KJN](https://doi.org/10.5066/F7P55KJN).
- U.S. Geological Survey. [Network Linked Data Index API documentation](https://api.water.usgs.gov/docs/nldi/).
- NOAA National Weather Service, Hydrometeorological Design Studies Center.
  [NOAA Atlas 14 precipitation-frequency estimates](https://www.weather.gov/owp/hdsc).

## Land cover, soil, and watershed attributes

- U.S. Geological Survey. 2024. *Annual NLCD Collection 1 Science Products*.
  U.S. Geological Survey data release.
  [doi:10.5066/P94UXNTS](https://doi.org/10.5066/P94UXNTS).
  The [USGS Annual NLCD landing page](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database)
  records the current collection and citation.
- U.S. Department of Agriculture, Natural Resources Conservation Service.
  [Gridded National Soil Survey Geographic Database (gNATSGO)](https://www.nrcs.usda.gov/resources/data-and-reports/gridded-national-soil-survey-geographic-database-gnatsgo).
- U.S. Department of Agriculture, Natural Resources Conservation Service.
  [Soil Data Access Web Service](https://sdmdataaccess.sc.egov.usda.gov/WebServiceHelp.aspx).
- Hill, R. A., M. H. Weber, S. G. Leibowitz, A. R. Olsen, and D. J. Thornbrugh.
  2016. “The Stream-Catchment (StreamCat) Dataset: A Database of Watershed
  Metrics for the Conterminous United States.” *Journal of the American Water
  Resources Association* 52:120–128.
  [doi:10.1111/1752-1688.12372](https://doi.org/10.1111/1752-1688.12372).

## Climate and antecedent-state data

- PRISM Group, Oregon State University. *PRISM Climate Data*. Accessed
  9 August 2026 through the Applied Climate Information System.
  [PRISM citation guidance](https://prism.oregonstate.edu/terms/);
  [ACIS web-service documentation](https://docs.rcc-acis.org/acisws/).
- NASA Prediction Of Worldwide Energy Resources (POWER).
  [Daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/).

## Google Earth Engine teaching exercise

- Google Earth Engine. [Earth Engine documentation and tutorials](https://developers.google.com/earth-engine/tutorials).
- U.S. Geological Survey. [Watershed Boundary Dataset HUC12 Earth Engine catalog entry](https://developers.google.com/earth-engine/datasets/catalog/USGS_WBD_2017_HUC12).
- U.S. Geological Survey. [NLCD 2019 release Earth Engine catalog entry](https://developers.google.com/earth-engine/datasets/catalog/USGS_NLCD_RELEASES_2019_REL_NLCD).

The guided Code Editor exercise uses the official assets
`USGS/WBD/2017/HUC12` and `USGS/NLCD_RELEASES/2019_REL/NLCD`. The optional live
Python pathway uses the following Earth Engine Community Catalog assets:

- Annual NLCD land cover:
  `projects/sat-io/open-datasets/USGS/ANNUAL_NLCD/LANDCOVER`;
- Annual NLCD fractional impervious surface:
  `projects/sat-io/open-datasets/USGS/ANNUAL_NLCD/FRACTIONAL_IMPERVIOUS_SURFACE`;
- gNATSGO map-unit keys:
  `projects/sat-io/open-datasets/gNATSGO/raster/mukey`; and
- optional HiHydroSoil comparison:
  `projects/sat-io/open-datasets/HiHydroSoilv2_0/Hydrologic_Soil_Group_250m`.

The `projects/sat-io` identifiers are computational access paths, not the
scientific publisher citations. Reports should cite USGS Annual NLCD or USDA
NRCS gNATSGO, as appropriate, and record the exact Earth Engine asset ID and
retrieval date in the methods or data-availability statement. USGS NLDI and
USDA NRCS Soil Data Access support the live spatial workflow but are web
services rather than Earth Engine assets.
