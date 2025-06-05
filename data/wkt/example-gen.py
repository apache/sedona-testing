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

from pathlib import Path

import geoarrow.pyarrow as ga
import yaml

HERE = Path(__file__).parent

if __name__ == "__main__":
    with open(HERE / "example.yaml") as f:
        examples = yaml.safe_load(f)

    with open(HERE / "example-wkt.tsv", "w") as f:
        f.write("id\tgroup\tgeometry\n")
        row = 0
        for group_name, geometries_wkt in examples.items():
            for geometry in geometries_wkt:
                geometry = "" if geometry is None else geometry
                f.write(f"{row}\t{group_name}\t{geometry}\n")
                row += 1

    with open(HERE / "example-wkb-le.tsv", "w") as f:
        f.write("id\tgroup\tgeometry\n")
        row = 0
        for group_name, geometries_wkt in examples.items():
            for geometry in geometries_wkt:
                if geometry is not None:
                    geometry_wkb = bytes(ga.as_wkb([geometry]).storage[0].as_py())
                else:
                    geometry_wkb = b""

                f.write(f"{row}\t{group_name}\t{geometry_wkb.hex().upper()}\n")
                row += 1
