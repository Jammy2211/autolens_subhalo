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
pix = "decomp"

pickle_path = path.join("paper", "pickles")
pickle_file = path.join(pickle_path, pix, f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_dict = pickle.load(f)

latex_dict = {}

slacs_keys = ["slacs0029-0055"]

for i, key in enumerate(slacs_keys):

    latex = af.text.Samples.latex(
        samples=samples_subhalo_dict[key],
        include_name=False,
        include_quickmath=True,
    )

    latex_dict[key] = latex

for key in latex_dict.keys():

    print(f"{latex_dict[key]}")
