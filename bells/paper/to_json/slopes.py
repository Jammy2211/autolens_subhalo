"""
__Imports__
"""
import json
import os
from os import path
import warnings

warnings.filterwarnings("ignore")

from autoconf import conf

import autofit as af

"""
__Paths__
"""
workspace_path = os.getcwd()

config_path = path.join(workspace_path, "config")
conf.instance.push(new_path=config_path)

"""
__Database__

Load the database. If the file `slacs.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
pix = "delaunay"

database_name_list = [
    f"slacs_{pix}_reg_0",
    f"slacs_{pix}_reg_1"
]

# database_name_list = ["slacs_test"]

slope_dict = {}
slope_ue3_dict = {}
slope_le3_dict = {}

for database_name in database_name_list:

    agg = af.Aggregator.from_database(
        filename=f"{database_name}.sqlite", completed_only=False
    )

    name = agg.search.name
    agg_query = agg.query(name == "subhalo[1]_mass[total_refine]")

    samples_gen = agg_query.values("samples")
    search_gen = agg_query.values("search")

    for samples, search in zip(samples_gen, search_gen):

        lens_name = search.paths.unique_tag
        print(lens_name)

        mp_instance = samples.median_pdf_instance

        ue3_instance = samples.error_instance_at_upper_sigma(sigma=3.0)
        le3_instance = samples.error_instance_at_lower_sigma(sigma=3.0)

        mp_slope = mp_instance.galaxies.lens.mass.slope
        ue3_slope = ue3_instance.galaxies.lens.mass.slope
        le3_slope = le3_instance.galaxies.lens.mass.slope

        slope_dict[lens_name] = mp_slope
        slope_ue3_dict[lens_name] = ue3_slope
        slope_le3_dict[lens_name] = le3_slope

slope_dict = dict(sorted(slope_dict.items()))
slope_ue3_dict = dict(sorted(slope_ue3_dict.items()))
slope_le3_dict = dict(sorted(slope_le3_dict.items()))

json_path = path.join("paper", "json")

slope_dict_file = path.join(json_path, pix, f"slope_dict.json")
slope_ue3_dict_file = path.join(json_path, pix, f"slope_dict_ue3.json")
slope_le3_dict_file = path.join(json_path, pix, f"slope_dict_le3.json")

with open(slope_dict_file, "w+") as f:
    json.dump(slope_dict, f, indent=4)

with open(slope_ue3_dict_file, "w+") as f:
    json.dump(slope_ue3_dict, f, indent=4)

with open(slope_le3_dict_file, "w+") as f:
    json.dump(slope_le3_dict, f, indent=4)
