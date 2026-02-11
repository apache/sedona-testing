<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
 -->

# Raster Test Files

This directory contains raster files used for testing Sedona's raster functionality.
Files are sourced from public datasets and the [Apache Sedona test resources](https://github.com/apache/sedona/tree/master/spark/common/src/test/resources/raster).

## Public Dataset Tiles

These are small cropped tiles from well-known public raster datasets. All permit free redistribution.

- `naip.jp2`: A 512x512 JPEG 2000 tile from the [NAIP](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-aerial-photography-national-agriculture-imagery-program-naip) (National Agriculture Imagery Program), 3 bands, 0.6m resolution, NAD83 / UTM zone 10N. NAIP imagery is U.S. public domain.
- `landsat8.tif`: A 512x512 GeoTIFF tile from [Landsat 8](https://www.usgs.gov/landsat-missions/landsat-8) (USGS/NASA), 1 band, 30m resolution, WGS 84 / UTM zone 46N. Landsat data is U.S. public domain.
- `sentinel2.tif`: A 512x512 GeoTIFF tile from [Sentinel-2](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2) (ESA/Copernicus), 1 band, 10m resolution, WGS 84 / UTM zone 14N. Contains modified Copernicus Sentinel data. Licensed under the [Copernicus Sentinel Data Terms](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), free and open access.
- `alphaearth.tiff`: A 128x128 GeoTIFF tile from the [AlphaEarth Foundations Satellite Embedding](https://developers.google.com/earth-engine/datasets/catalog/google_research_open_buildings_temporal_v1) dataset, 64 bands (Int8), WGS 84 / UTM zone 10N. Licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: "The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind."

## Test Files from Apache Sedona

These files originate from the [Apache Sedona repository](https://github.com/apache/sedona/tree/master/spark/common/src/test/resources/raster), licensed under Apache License 2.0.

- `test1.tiff`: A 512x517 single-band GeoTIFF (Byte)
- `test1.asc`: A 2x2 Esri ASCII Grid (cellsize 30)
- `test2.tif`: A 1491x1387 GeoTIFF with 3 bands (Byte, RGB)
- `test3.tif`: A 32x32 GeoTIFF with 4 bands (UInt16, LZW compressed)
- `test4.tiff`: A 10x10 single-band GeoTIFF (Byte)
- `test5.tiff`: A 1440x720 single-band GeoTIFF (Byte, palette color)
- `test.nc`: A NetCDF file (512x512)
