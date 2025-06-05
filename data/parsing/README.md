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

# WKT and WKB Parsing Test Files

These files are intended primarily as tests for WKT and WKB parsing
and formatting, and cover the full matrix of geometry types, dimensions,
big/little endian, and extended/ISO well-known binary.

- `example.yaml`: The source from which the other files in this directory are derived. This is derived from the [GeoSpatial test files in the Parquet testing repo](https://github.com/apache/parquet-testing/tree/master/data/geospatial).
- `example-wkt.tsv`: A tab-separated values file with columns `id`, `group`, and `geometry`, where geometry is formatted as well-known text.
- `example-wkb-le.tsv`: A tab-separated values file with columns `id`, `group`, and `geometry`, where geometry is formatted as little-endian ISO well-known binary.
- `example-wkb-be.tsv`: A tab-separated values file with columns `id`, `group`, and `geometry`, where geometry is formatted as big-endian ISO well-known binary.
- `example-ewkb-le.tsv`: A tab-separated values file with columns `id`, `group`, and `geometry`, where geometry is formatted as little-endian ISO well-known binary (EWKB).
- `example-ewkb-be.tsv`: A tab-separated values file with columns `id`, `group`, and `geometry`, where geometry is formatted as big-endian extended well-known binary (EWKB).

This directory also contains the files used to generate the .tsv formatted versions (`example-gen.py` and `example-gen.R`).
