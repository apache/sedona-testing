# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Generate the small Zarr interoperability fixtures in this directory."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import warnings
from pathlib import Path

import numpy as np
import zarr
from pyproj import CRS

HERE = Path(__file__).parent
FIXTURE_NAMES = (
    "v2-cf-grid-mapping.zarr",
    "v3-cf-grid-mapping.zarr",
    "v3-geozarr-bbox-node.zarr",
    "v3-geozarr-bbox-pixel.zarr",
    "v3-geozarr-consolidated.zarr",
    "v3-lon-lat-coordinates.zarr",
)
MANIFEST_NAME = "manifest.json"
ZARR_JSON_NAMES = {
    ".zarray",
    ".zattrs",
    ".zgroup",
    ".zmetadata",
    "zarr.json",
}

# Stable v0.1 references from the GeoZarr proj and spatial conventions. Keeping
# these here makes the fixture metadata self-describing and avoids duplicating
# URLs and permanent convention identifiers in every creator below.
# https://github.com/zarr-conventions/proj/blob/v0.1/README.md
# https://github.com/zarr-conventions/spatial/blob/v0.1/README.md
GEOZARR_CONVENTIONS = [
    {
        "schema_url": (
            "https://raw.githubusercontent.com/zarr-conventions/proj/"
            "refs/tags/v0.1/schema.json"
        ),
        "spec_url": "https://github.com/zarr-conventions/proj/blob/v0.1/README.md",
        "uuid": "f17cb550-5864-4468-aeb7-f3180cfb622f",
        "name": "proj",
        "description": "Coordinate reference system information for geospatial data",
    },
    {
        "schema_url": (
            "https://raw.githubusercontent.com/zarr-conventions/spatial/"
            "refs/tags/v0.1/schema.json"
        ),
        "spec_url": ("https://github.com/zarr-conventions/spatial/blob/v0.1/README.md"),
        "uuid": "689b58e2-cf7b-45e0-9fff-9cfc0883d6b4",
        "name": "spatial",
        "description": "Spatial coordinate information",
    },
]


def sample_cube(dtype: str) -> np.ndarray:
    """Return deterministic, non-uniform values with shape (time, y, x)."""
    return np.arange(2 * 4 * 6, dtype=dtype).reshape(2, 4, 6)


def create_v2_cf_grid_mapping(output: Path) -> None:
    """Create an xarray/rioxarray-style Zarr v2 hierarchy."""
    path = output / "v2-cf-grid-mapping.zarr"
    root = zarr.create_group(store=path, zarr_format=2, overwrite=True)
    root.attrs.update(
        {
            "title": "Zarr v2 fixture with CF grid-mapping metadata",
            "Conventions": "CF-1.8",
        }
    )

    root.create_array(
        "temperature",
        data=sample_cube("int16"),
        chunks=(1, 2, 3),
        compressor=None,
        attributes={
            "_ARRAY_DIMENSIONS": ["time", "y", "x"],
            "grid_mapping": "spatial_ref",
            "coordinates": "time y x spatial_ref",
            "units": "K",
        },
    )
    for name, values, dimensions in (
        ("time", np.array([0, 1], dtype="int32"), ["time"]),
        ("y", np.array([199.5, 198.5, 197.5, 196.5]), ["y"]),
        ("x", np.array([100.5, 101.5, 102.5, 103.5, 104.5, 105.5]), ["x"]),
    ):
        root.create_array(
            name,
            data=values,
            chunks=values.shape,
            compressor=None,
            attributes={"_ARRAY_DIMENSIONS": dimensions},
        )

    root.create_array(
        "spatial_ref",
        data=np.array(0, dtype="int32"),
        compressor=None,
        attributes={
            "_ARRAY_DIMENSIONS": [],
            "crs_wkt": CRS.from_epsg(3857).to_wkt(version="WKT2_2019"),
            "spatial_ref": CRS.from_epsg(3857).to_wkt(version="WKT2_2019"),
            "GeoTransform": "100 1 0 200 0 -1",
        },
    )
    zarr.consolidate_metadata(path, zarr_format=2)


def create_v3_cf_grid_mapping(output: Path) -> None:
    """Create an unconsolidated CF grid-mapping hierarchy in Zarr v3."""
    # CF 1.13 grid mappings and extended grid_mapping syntax:
    # https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#grid-mappings-and-projections
    path = output / "v3-cf-grid-mapping.zarr"
    root = zarr.create_group(
        store=path,
        zarr_format=3,
        overwrite=True,
        attributes={
            "title": "Zarr v3 fixture with CF grid-mapping metadata",
            "Conventions": "CF-1.13",
        },
    )

    root.create_array(
        "precipitation",
        data=sample_cube("int16"),
        chunks=(1, 2, 3),
        dimension_names=("time", "y", "x"),
        compressors=[],
        attributes={
            "grid_mapping": "spatial_ref: x y",
            "coordinates": "time y x",
            "standard_name": "lwe_precipitation_rate",
            "units": "kg m-2 s-1",
        },
    )
    for name, values, standard_name, units in (
        (
            "time",
            np.array([0, 1], dtype="int32"),
            "time",
            "days since 2000-01-01",
        ),
        (
            "y",
            np.array([199.5, 198.5, 197.5, 196.5]),
            "projection_y_coordinate",
            "m",
        ),
        (
            "x",
            np.array([100.5, 101.5, 102.5, 103.5, 104.5, 105.5]),
            "projection_x_coordinate",
            "m",
        ),
    ):
        root.create_array(
            name,
            data=values,
            chunks=values.shape,
            dimension_names=(name,),
            compressors=[],
            attributes={"standard_name": standard_name, "units": units},
        )

    crs = CRS.from_epsg(3857)
    root.create_array(
        "spatial_ref",
        data=np.array(0, dtype="int32"),
        compressors=[],
        dimension_names=(),
        attributes={
            **crs.to_cf(),
            "spatial_ref": crs.to_wkt(version="WKT2_2019"),
            "GeoTransform": [100.0, 1.0, 0.0, 200.0, 0.0, -1.0],
        },
    )


def create_v3_geozarr_consolidated(output: Path) -> None:
    """Create a GeoZarr-style v3 store readable from root metadata alone."""
    path = output / "v3-geozarr-consolidated.zarr"
    root = zarr.create_group(
        store=path,
        zarr_format=3,
        overwrite=True,
        attributes={
            "title": "Zarr v3 fixture with inline consolidated metadata",
            "zarr_conventions": GEOZARR_CONVENTIONS,
            "proj:code": "EPSG:32610",
            "spatial:dimensions": ["y", "x"],
            "spatial:shape": [4, 6],
            "spatial:transform": [30.0, 0.0, 500000.0, 0.0, -30.0, 5200000.0],
        },
    )
    root.create_array(
        "reflectance",
        data=sample_cube("uint16"),
        chunks=(1, 2, 3),
        dimension_names=("time", "y", "x"),
        compressors=[],
        attributes={"units": "1"},
    )
    root.create_array(
        "quality",
        data=(sample_cube("uint8") % 4),
        chunks=(1, 2, 3),
        dimension_names=("time", "y", "x"),
        compressors=[],
        attributes={"flag_values": [0, 1, 2, 3]},
    )

    # V3 consolidation is an inline extension stored in the root zarr.json.
    # Remove child metadata after consolidation so consumers must use that one
    # root document. This models HTTP object stores that cannot list paths.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        zarr.consolidate_metadata(path, zarr_format=3)
    for child_metadata in path.glob("*/zarr.json"):
        child_metadata.unlink()


def create_v3_geozarr_bbox_pixel(output: Path) -> None:
    """Create a GeoZarr v3 store using a bbox with pixel registration."""
    path = output / "v3-geozarr-bbox-pixel.zarr"
    root = zarr.create_group(
        store=path,
        zarr_format=3,
        overwrite=True,
        attributes={
            "title": "GeoZarr v3 fixture with a pixel-registered bbox",
            "zarr_conventions": GEOZARR_CONVENTIONS,
            "proj:wkt2": CRS.from_epsg(4326).to_wkt(version="WKT2_2019"),
            "spatial:dimensions": ["latitude", "longitude"],
            "spatial:shape": [4, 6],
            "spatial:bbox": [-124.0, 48.0, -121.0, 50.0],
            "spatial:registration": "pixel",
        },
    )
    root.create_array(
        "air_temperature",
        data=sample_cube("float32"),
        chunks=(1, 2, 3),
        dimension_names=("time", "latitude", "longitude"),
        compressors=[],
        attributes={"units": "K"},
    )


def create_v3_geozarr_bbox_node(output: Path) -> None:
    """Create a GeoZarr v3 store using a bbox with node registration."""
    path = output / "v3-geozarr-bbox-node.zarr"
    root = zarr.create_group(
        store=path,
        zarr_format=3,
        overwrite=True,
        attributes={
            "title": "GeoZarr v3 fixture with a node-registered bbox",
            "zarr_conventions": GEOZARR_CONVENTIONS,
            "proj:projjson": CRS.from_epsg(32610).to_json_dict(),
            "spatial:dimensions": ["northing", "easting"],
            "spatial:shape": [4, 6],
            # Node-registration bounds describe the centers of the border
            # cells rather than the outside edges of the raster footprint.
            "spatial:bbox": [500015.0, 5199895.0, 500165.0, 5199985.0],
            "spatial:registration": "node",
        },
    )
    root.create_array(
        "elevation",
        data=sample_cube("float32"),
        chunks=(1, 2, 3),
        dimension_names=("time", "northing", "easting"),
        compressors=[],
        attributes={"units": "m"},
    )


def create_v3_lon_lat_coordinates(output: Path) -> None:
    """Create a v3 hierarchy georeferenced only by coordinate arrays."""
    path = output / "v3-lon-lat-coordinates.zarr"
    root = zarr.create_group(
        store=path,
        zarr_format=3,
        overwrite=True,
        attributes={"title": "Zarr v3 fixture with regular lon/lat coordinates"},
    )
    root.create_array(
        "air_temperature",
        data=sample_cube("float32"),
        chunks=(1, 2, 3),
        dimension_names=("time", "latitude", "longitude"),
        compressors=[],
        attributes={"units": "K"},
    )
    for name, values in (
        ("time", np.array([0, 1], dtype="int32")),
        ("latitude", np.array([49.75, 49.25, 48.75, 48.25])),
        (
            "longitude",
            np.array([-123.75, -123.25, -122.75, -122.25, -121.75, -121.25]),
        ),
    ):
        root.create_array(
            name,
            data=values,
            chunks=values.shape,
            dimension_names=(name,),
            compressors=[],
        )


def generate(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name in FIXTURE_NAMES:
        path = output / name
        if path.exists():
            shutil.rmtree(path)
    create_v2_cf_grid_mapping(output)
    create_v3_cf_grid_mapping(output)
    create_v3_geozarr_consolidated(output)
    create_v3_geozarr_bbox_pixel(output)
    create_v3_geozarr_bbox_node(output)
    create_v3_lon_lat_coordinates(output)
    manifest = {
        "v2-cf-grid-mapping.zarr": {
            "zarr_format": 2,
            "raster_arrays": ["temperature"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:3857",
            "geotransform": [100.0, 1.0, 0.0, 200.0, 0.0, -1.0],
            "metadata": "CF grid mapping in a scalar spatial_ref array",
            "consolidated_metadata": ".zmetadata",
        },
        "v3-cf-grid-mapping.zarr": {
            "zarr_format": 3,
            "raster_arrays": ["precipitation"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:3857",
            "geotransform": [100.0, 1.0, 0.0, 200.0, 0.0, -1.0],
            "metadata": "CF grid mapping in a scalar spatial_ref array",
            "consolidated_metadata": None,
        },
        "v3-geozarr-consolidated.zarr": {
            "zarr_format": 3,
            "raster_arrays": ["quality", "reflectance"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:32610",
            "geotransform": [500000.0, 30.0, 0.0, 5200000.0, 0.0, -30.0],
            "metadata": "GeoZarr-style group attributes",
            "consolidated_metadata": "inline root zarr.json",
        },
        "v3-geozarr-bbox-pixel.zarr": {
            "zarr_format": 3,
            "raster_arrays": ["air_temperature"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:4326",
            "geotransform": [-124.0, 0.5, 0.0, 50.0, 0.0, -0.5],
            "metadata": "GeoZarr WKT2 and pixel-registered spatial bbox",
            "consolidated_metadata": None,
        },
        "v3-geozarr-bbox-node.zarr": {
            "zarr_format": 3,
            "raster_arrays": ["elevation"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:32610",
            "geotransform": [500000.0, 30.0, 0.0, 5200000.0, 0.0, -30.0],
            "metadata": "GeoZarr PROJJSON and node-registered spatial bbox",
            "consolidated_metadata": None,
        },
        "v3-lon-lat-coordinates.zarr": {
            "zarr_format": 3,
            "raster_arrays": ["air_temperature"],
            "chunk_grid_shape": [2, 2, 2],
            "crs_authority": "EPSG:4326",
            "geotransform": [-124.0, 0.5, 0.0, 50.0, 0.0, -0.5],
            "metadata": "regular latitude and longitude coordinate arrays",
            "consolidated_metadata": None,
        },
    }
    (output / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    # Zarr-Python emits compact metadata without a final newline. Normalize the
    # committed JSON documents so repository text-file hooks leave them intact.
    for name in FIXTURE_NAMES:
        for path in (output / name).rglob("*"):
            if path.is_file() and path.name in ZARR_JSON_NAMES:
                contents = path.read_bytes()
                if not contents.endswith(b"\n"):
                    path.write_bytes(contents + b"\n")


def compare_trees(expected: Path, actual: Path) -> list[str]:
    """Return relative paths whose presence, type, or bytes differ."""
    expected_paths = {path.relative_to(expected) for path in expected.rglob("*")}
    actual_paths = {path.relative_to(actual) for path in actual.rglob("*")}
    differences = expected_paths ^ actual_paths
    for relative_path in expected_paths & actual_paths:
        expected_path = expected / relative_path
        actual_path = actual / relative_path
        if expected_path.is_file() != actual_path.is_file():
            differences.add(relative_path)
        elif (
            expected_path.is_file()
            and expected_path.read_bytes() != actual_path.read_bytes()
        ):
            differences.add(relative_path)
    return sorted(str(path) for path in differences)


def check() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        generated = Path(temporary_directory)
        generate(generated)
        differences = compare_trees(HERE, generated)
        differences = [
            path
            for path in differences
            if path == MANIFEST_NAME or path.startswith(FIXTURE_NAMES)
        ]
        if differences:
            formatted = "\n".join(f"  {path}" for path in differences)
            raise SystemExit(f"fixtures are not reproducible:\n{formatted}")
    print("Zarr fixtures match generate.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate in a temporary directory and compare bytes",
    )
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(HERE)
