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
model = "base"

model_list = [
    # "base",
    # "delaunay",
    # "scaled",
    # "source_mask",
     "gui_mask",
    # "clumps",
#    "decomp",
 #   "bpl",
    "multipole"
]

# model = "delaunay"
# model = "scaled"
# model = "clumps"

for model in model_list:

    database_name_list = [f"slacs_{model}_0", f"slacs_{model}_1"]

    evidence_dict = {}

    for database_name in database_name_list:

        agg = af.Aggregator.from_database(
            filename=f"{database_name}.sqlite", completed_only=False
        )

        """
        __Query__
        """

        agg_grid = agg.grid_searches()

        agg_best_fits = agg_grid.best_fits()
        search_gen = agg_best_fits.values("search")
        info_gen = agg_best_fits.values("info")

        for fit_grid, search, info in zip(agg_grid, search_gen, info_gen):

            path_prefix = search.paths.path_prefix

            try:
                subhalo_search_result = al.subhalo.SubhaloResult(
                    grid_search_result=fit_grid["result"], result_no_subhalo=fit_grid.parent
                )

                detection_array = subhalo_search_result.subhalo_detection_array_from(
                    use_log_evidences=False,
                    use_stochastic_log_likelihoods=False,
                    relative_to_no_subhalo=True,
                )

                evidence = float(np.nanmax(detection_array))

                evidence_dict[search.unique_tag] = evidence

            except AttributeError:

                print(f"The lens {search.unique_tag} could not be loaded.")

    import operator

    sorted_tuples = reversed(sorted(evidence_dict.items(), key=operator.itemgetter(1)))
    evidence_dict = {k: v for k, v in sorted_tuples}

    json_path = path.join("paper", "json", model)

    os.makedirs(json_path, exist_ok=True)

    evidence_dict_file = path.join(json_path, f"evidence_grid_dict.json")

    with open(evidence_dict_file, "w+") as f:
        json.dump(evidence_dict, f, indent=4)
