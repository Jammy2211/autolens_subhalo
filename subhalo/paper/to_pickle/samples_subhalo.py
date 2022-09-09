"""
__Imports__
"""
import os
from os import path
import warnings

warnings.filterwarnings("ignore")

import autofit as af

from autoconf import conf

import pickle

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
# pix = "base__source_mask"
pix = "delaunay"
# pix = "delaunay__source_mask"

database_name = f"subhalo_{pix}"

samples_subhalo_dict = {}

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

"""
__Query__
"""

agg_result = agg.query(
    (agg.search.name == "subhalo[3]_subhalo[single_plane_refine]__stochastic")
)

search_gen = agg_result.values("search")
samples_gen = agg_result.values("samples")

for samples, search in zip(samples_gen, search_gen):

    samples_subhalo = samples.with_paths([("galaxies.subhalo.mass")])

    key = search.paths.path_prefix.replace("/", "_")
    key = key.replace(f"subhalo_{pix}_", "")

    samples_subhalo_dict[key] = samples_subhalo

samples_subhalo_dict_ordered = {}

for key, evidence in samples_subhalo_dict.items():

    samples_subhalo_dict_ordered[key] = samples_subhalo_dict[key]

pickle_path = path.join("paper", "pickles")

pickle_file = path.join(pickle_path, pix, f"samples_subhalo_dict.pickle")

with open(pickle_file, "wb") as f:
    pickle.dump(samples_subhalo_dict_ordered, f)
