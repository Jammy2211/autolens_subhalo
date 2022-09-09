"""
__Imports__
"""
import os
from os import path
import warnings

warnings.filterwarnings("ignore")

import autofit as af
import autolens as al

from autoconf import conf

import numpy as np
import json

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
pix = "base"
# pix = "base__source_mask"
pix = "delaunay"
# pix = "delaunay__source_mask"

database_name = f"subhalo_{pix}"

evidence_dict = {}

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

"""
__Query__
"""

agg_grid = agg.grid_searches()

agg_best_fits = agg_grid.best_fits()
search_gen = agg_best_fits.values("search")

for fit_grid, search in zip(agg_grid, search_gen):

    path_prefix = search.paths.path_prefix

    subhalo_search_result = al.subhalo.SubhaloResult(
        grid_search_result=fit_grid["result"], result_no_subhalo=fit_grid.parent
    )

    detection_array = subhalo_search_result.subhalo_detection_array_from(
        use_log_evidences=False,
        use_stochastic_log_likelihoods=False,
        relative_to_no_subhalo=True,
    )

    evidence = float(np.nanmax(detection_array))

    key = search.paths.path_prefix.replace("/", "_")
    key = key.replace(f"subhalo_{pix}_", "")

    evidence_dict[key] = evidence

import operator

sorted_tuples = reversed(sorted(evidence_dict.items(), key=operator.itemgetter(1)))
evidence_dict = {k: v for k, v in sorted_tuples}

json_path = path.join("paper", "json")

evidence_dict_file = path.join(json_path, pix, f"evidence_grid_dict.json")

with open(evidence_dict_file, "w+") as f:
    json.dump(evidence_dict, f, indent=4)
