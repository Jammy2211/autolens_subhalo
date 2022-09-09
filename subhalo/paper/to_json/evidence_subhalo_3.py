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
# pix = "base"
pix = "base__source_mask"
# pix = "delaunay"
# pix = "delaunay__source_mask"

database_name = f"subhalo_{pix}"

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

evidence_no_subhalo_dict = {}

for samples, search in zip(samples_gen, search_gen):

    path_prefix = search.paths.path_prefix

    evidence_no_subhalo = samples.log_evidence

    key = search.paths.path_prefix.replace("/", "_")
    key = key.replace(f"subhalo_{pix}_", "")

    evidence_no_subhalo_dict[key] = evidence_no_subhalo



agg_subhalo = agg.query(
    (agg.search.name == "subhalo[3]_subhalo[single_plane_refine]")
)

samples_gen = agg_subhalo.values("samples")
search_gen = agg_subhalo.values("search")

evidence_dict = {}

for samples, search in zip(samples_gen, search_gen):

    path_prefix = search.paths.path_prefix

    evidence_subhalo = samples.log_evidence

    key = search.paths.path_prefix.replace("/", "_")
    key = key.replace(f"subhalo_{pix}_", "")

    evidence_dict[key] = evidence_subhalo - evidence_no_subhalo_dict[key]

import operator

sorted_tuples = reversed(sorted(evidence_dict.items(), key=operator.itemgetter(1)))
evidence_dict = {k: v for k, v in sorted_tuples}

json_path = path.join("paper", "json")

evidence_dict_file = path.join(json_path, pix, f"evidence_dict.json")

with open(evidence_dict_file, "w+") as f:
    json.dump(evidence_dict, f, indent=4)
