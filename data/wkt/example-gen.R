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

library(tidyverse)
library(wk)
library(yaml)

examples <- yaml.load_file("data/wkt/example.yaml")

wkb_example_hex_ewkb <- function(endian = 0x01) {
  tibble(
    group = names(examples),
    geometry = examples |>
      map(as.list)
  ) |>
    unnest_longer(geometry) |>
    transmute(
      id = 0:(n() - 1),
      group,
      geometry = geometry |>
        wkt() |>
        wk_handle(wkb_writer(endian = endian)) |>
        unclass() |>
        map(~ {
          if (is.null(.x)) {
            NA_character_
          } else {
            paste(PKI::raw2hex(.x), collapse = "")
          }
        }) |>
        as.character() |>
        str_to_upper()
    )
}

wkb_example_hex_ewkb(endian = 0x01) |>
  write_tsv("data/wkt/example-ewkb-le.tsv")

wkb_example_hex_ewkb(endian = 0x00) |>
  write_tsv("data/wkt/example-ewkb-be.tsv")
