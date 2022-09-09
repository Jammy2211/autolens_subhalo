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

pickle_path = path.join("paper", "pickles")

pickle_file = path.join(pickle_path, "base", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_base_dict = pickle.load(f)

pickle_file = path.join(pickle_path, "base__source_mask", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_base_source_dict = pickle.load(f)

pickle_file = path.join(pickle_path, "delaunay", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_delaunay_dict = pickle.load(f)

pickle_file = path.join(pickle_path, "delaunay__source_mask", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_delaunay_source_dict = pickle.load(f)


json_path = path.join("paper", "json")

evidence_base_dict_file = path.join(json_path, "base", f"evidence_grid_dict.json")

with open(evidence_base_dict_file, "r+") as f:
    evidence_base_dict = json.load(f)

evidence_base_source_dict_file = path.join(json_path, "base__source_mask", f"evidence_grid_dict.json")

with open(evidence_base_source_dict_file, "r+") as f:
    evidence_base_source_dict = json.load(f)

evidence_delaunay_dict_file = path.join(json_path, "delaunay", f"evidence_grid_dict.json")

with open(evidence_delaunay_dict_file, "r+") as f:
    evidence_delaunay_dict = json.load(f)

evidence_delaunay_source_dict_file = path.join(json_path, "delaunay__source_mask", f"evidence_grid_dict.json")

with open(evidence_delaunay_source_dict_file, "r+") as f:
    evidence_delaunay_source_dict = json.load(f)

latex_dict = {}


for key, value in evidence_base_dict.items():

    try:
        evidence_base = np.round(evidence_base_dict[key], 2)
        if evidence_base > 10.0:
            evidence_base = r"\textbf{" + f"{evidence_base}" + "}"
    except KeyError:
        evidence_base = None

    try:
        evidence_base_source = np.round(evidence_base_source_dict[key], 2)
        if evidence_base_source > 10.0:
            evidence_base_source = r"\textbf{" + f"{evidence_base_source}" + "}"
    except KeyError:
        evidence_base_source = None

    try:
        evidence_delaunay = np.round(evidence_delaunay_dict[key], 2)
        if evidence_delaunay > 10.0:
            evidence_delaunay = r"\textbf{" + f"{evidence_delaunay}" + "}"
    except KeyError:
        evidence_delaunay = None


    try:
        evidence_delaunay_source = np.round(evidence_delaunay_source_dict[key], 2)
        if evidence_delaunay_source > 10.0:
            evidence_delaunay_source = r"\textbf{" + f"{evidence_delaunay_source}" + "}"
    except KeyError:
        evidence_delaunay_source = None

    lens_name_latex = util.lens_name_latex_from(lens_name=key)
    subhalo_mass_latex = util.subhalo_mass_latex_from(lens_name=key)
    consistent_dict = util.consistent_dict_from()

    consistent = consistent_dict[key]

    try:
        latex = af.text.Samples.latex(
            samples=samples_subhalo_base_source_dict[key],
            include_name=False,
            include_quickmath=True,
            prefix=f"{lens_name_latex} & {subhalo_mass_latex} & {evidence_base} & {evidence_delaunay} & {evidence_base_source} & {evidence_delaunay_source} & {consistent} & ",
            suffix=r" \\[2pt]",
        )
    except KeyError:
        latex = af.text.Samples.latex(
            samples=samples_subhalo_base_dict[key],
            include_name=False,
            include_quickmath=True,
            prefix=f"{lens_name_latex} & {subhalo_mass_latex} & {evidence_base} & {evidence_delaunay} & {evidence_base_source} & {evidence_delaunay_source} & {consistent} & ",
            suffix=r" \\[2pt]",
        )

    latex_dict[key] = latex

key_order_list = util.key_order_list_from()



import operator

sorted_tuples = sorted(latex_dict.keys(), key=lambda x:x.lower())

for key in key_order_list:

    print(f"{latex_dict[key]}")
