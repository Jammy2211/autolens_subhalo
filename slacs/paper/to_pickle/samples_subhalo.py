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
model = "base"

model_list = [
 #   "delaunay",
 #   "scaled",
 #   "source_mask",
    "gui_mask",
 #   "clumps",
 #   "decomp",
 #   "bpl",
    "multipole"
]

# model = "delaunay"
# model = "scaled"
# model = "clumps"

for model in model_list:

    database_name_list = [f"slacs_{model}_0", f"slacs_{model}_1"]

    # database_name = "slacs_test"

    samples_subhalo_dict = {}

    for database_name in database_name_list:

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

            samples_subhalo_dict[search.unique_tag] = samples_subhalo

    samples_subhalo_dict_ordered = {}

    for key, evidence in samples_subhalo_dict.items():

        samples_subhalo_dict_ordered[key] = samples_subhalo_dict[key]

    pickle_path = path.join("paper", "pickles", model)

    os.makedirs(pickle_path, exist_ok=True)

    pickle_file = path.join(pickle_path, f"samples_subhalo_dict.pickle")

    with open(pickle_file, "wb") as f:
        pickle.dump(samples_subhalo_dict_ordered, f)
