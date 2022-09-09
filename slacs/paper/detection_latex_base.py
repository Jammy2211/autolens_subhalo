"""
__Imports__
"""
import json
import numpy as np
import os
from os import path
import pickle
import warnings

warnings.filterwarnings("ignore")

from autoconf import conf
import autofit as af

import autofit as af
import autolens as al
import autolens.plot as aplt

import util

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
# pix = "delaunay"

pickle_path = path.join("paper", "pickles")
pickle_file = path.join(pickle_path, pix, f"samples_subhalo_dict.pickle")

latex_dict = {}

with open(pickle_file, "rb") as f:
    samples_subhalo_dict = pickle.load(f)

json_path = path.join("paper", "json")

evidence_base_dict_file = path.join(json_path, "base", f"evidence_grid_dict.json")

with open(evidence_base_dict_file, "r+") as f:
    evidence_base_dict = json.load(f)

evidence_delaunay_dict_file = path.join(json_path, "delaunay", f"evidence_grid_dict.json")

with open(evidence_delaunay_dict_file, "r+") as f:
    evidence_delaunay_dict = json.load(f)


evidence_scaled_dict_file = path.join(json_path, "scaled", f"evidence_grid_dict.json")

with open(evidence_scaled_dict_file, "r+") as f:
    evidence_scaled_dict = json.load(f)

slacs_keys = util.slacs_keys_list_from()
consistent_list = util.consistent_list_from()
snr_dict = util.slacs_snr_dict_from()

for i, key in enumerate(slacs_keys):

    evidence_base = np.round(evidence_base_dict[key], 2)
    evidence_delaunay = np.round(evidence_delaunay_dict[key], 2)

    evidence_max = np.max([evidence_base, evidence_delaunay])

    snr = np.round(snr_dict[key], 1)

    prefix = f"{key.upper()} & {evidence_max} & {evidence_base} & {evidence_delaunay} & {consistent_list[i]} & "
    suffix = fr" & {snr} \\[2pt]"

    latex = af.text.Samples.latex(
        samples=samples_subhalo_dict[key],
        include_name=False,
        include_quickmath=True,
        prefix=prefix,
        suffix=suffix
    )

    latex_dict[key] = latex

for key in latex_dict.keys():

    print(f"{latex_dict[key]}")
