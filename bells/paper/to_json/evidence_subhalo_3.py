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

Load the database. If the file `bells.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
model_list = [
    "base",
    "delaunay",
    "scaled",
    "source_mask",
    "gui_mask"
    "clumps"
]

for model in model_list:

    database_name = f"bells_{model}"

    # database_name = "bells_test"

    evidence_dict = {}

    agg = af.Aggregator.from_database(
        filename=f"{database_name}.sqlite", completed_only=False
    )

    """
    __Query__
    """

    agg_no_subhalo = agg.query(
        (agg.search.name == "subhalo[1]_mass[total_refine]")
    )

    samples_gen = agg_no_subhalo.values("samples")
    search_gen = agg_no_subhalo.values("search")
    info_gen = agg_no_subhalo.values("info")

    evidence_no_subhalo_dict = {}

    for samples, search in zip(samples_gen, search_gen):
        path_prefix = search.paths.path_prefix

        evidence_no_subhalo = samples.log_evidence

        evidence_no_subhalo_dict[search.unique_tag] = evidence_no_subhalo

    agg_subhalo = agg.query(
        (agg.search.name == "subhalo[3]_subhalo[single_plane_refine]")
    )

    samples_gen = agg_subhalo.values("samples")
    search_gen = agg_subhalo.values("search")
    info_gen = agg_subhalo.values("info")

    evidence_subhalo_dict = {}

    for samples, search in zip(samples_gen, search_gen):
        path_prefix = search.paths.path_prefix

        evidence_subhalo = samples.log_evidence

        evidence_dict[search.unique_tag] = evidence_subhalo - evidence_no_subhalo_dict[search.unique_tag]

    import operator

    sorted_tuples = reversed(sorted(evidence_dict.items(), key=operator.itemgetter(1)))
    evidence_dict = {k: v for k, v in sorted_tuples}

    json_path = path.join("paper", "json", model)

    os.makedirs(json_path, exist_ok=True)

    evidence_dict_file = path.join(json_path, f"evidence_dict.json")

    with open(evidence_dict_file, "w+") as f:
        json.dump(evidence_dict, f, indent=4)
