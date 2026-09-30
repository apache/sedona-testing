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

# Zarr Test Files

These small synthetic fixtures exercise Zarr transport and geospatial metadata
interoperability. They are generated data and may be redistributed under this
repository's Apache License 2.0.

| Fixture | Format | Purpose |
| --- | --- | --- |
| `v2-cf-grid-mapping.zarr` | Zarr v2, consolidated | Xarray `_ARRAY_DIMENSIONS`; a CF/rioxarray `spatial_ref` scalar containing WKT2 and a GDAL-order `GeoTransform`; `time`, `x`, and `y` coordinate arrays. |
| `v3-geozarr-consolidated.zarr` | Zarr v3, inline consolidated | GeoZarr `proj:code`, `spatial:dimensions`, and affine-order `spatial:transform`; two compatible raster arrays. Child `zarr.json` files are intentionally absent, so array discovery must use the root's inline consolidated metadata and does not require store listing or extra metadata requests. |
| `v3-geozarr-bbox-pixel.zarr` | Zarr v3 | GeoZarr `proj:wkt2` and `spatial:bbox` with pixel (cell-area) registration and `latitude`/`longitude` spatial dimension names. |
| `v3-geozarr-bbox-node.zarr` | Zarr v3 | GeoZarr `proj:projjson` and `spatial:bbox` with node (cell-center) registration and `northing`/`easting` spatial dimension names. |
| `v3-lon-lat-coordinates.zarr` | Zarr v3 | No explicit CRS or transform. Regular `latitude` and `longitude` coordinate arrays provide the transform and identify geographic coordinates. |

All raster arrays have shape `(2, 4, 6)` and chunks `(1, 2, 3)`, producing a
chunk grid of `(2, 2, 2)`. V3 arrays use uncompressed chunks and v2 arrays use
`compressor: null`, keeping fixtures simple for static HTTP and S3-compatible
test servers.

The GeoZarr stores register the versioned [`proj`](https://github.com/zarr-conventions/proj/blob/v0.1/README.md)
and [`spatial`](https://github.com/zarr-conventions/spatial/blob/v0.1/README.md)
conventions in their `zarr_conventions` attributes. Together they cover all
three CRS representations and both explicit affine and bbox-derived transforms.

[`manifest.json`](manifest.json) records the expected raster arrays, chunk-grid
shape, CRS authority, and GDAL-order geotransform for each fixture so consumers
can share the same assertions.

## Regenerating

From this directory, create an environment and run:

```bash
python -m pip install -r requirements.txt
python generate.py
python generate.py --check
```

`--check` regenerates every fixture in a temporary directory and compares the
result byte-for-byte with the committed files.
