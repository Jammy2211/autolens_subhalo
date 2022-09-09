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

Load the database. If the file `bells.sqlite` does not exist, it will be made by the method below, so its fine if
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

evidence_source_mask_dict_file = path.join(json_path, "source_mask", f"evidence_grid_dict.json")

with open(evidence_source_mask_dict_file, "r+") as f:
    evidence_source_mask_dict = json.load(f)


evidence_source_dict_file = path.join(json_path, "gui_mask", f"evidence_grid_dict.json")

with open(evidence_source_dict_file, "r+") as f:
    evidence_source_dict = json.load(f)


evidence_bpl_dict_file = path.join(json_path, "bpl_final", f"evidence_grid_dict.json")

with open(evidence_bpl_dict_file, "r+") as f:
    evidence_bpl_dict = json.load(f)


evidence_multipole_dict_file = path.join(json_path, "multipole", f"evidence_grid_dict.json")

with open(evidence_multipole_dict_file, "r+") as f:
    evidence_multipole_dict = json.load(f)



evidence_decomp_dict_file = path.join(json_path, "decomp", f"evidence_grid_dict.json")

with open(evidence_decomp_dict_file, "r+") as f:
    evidence_decomp_dict = json.load(f)


evidence_clumps_dict_file = path.join(json_path, "clumps_new", f"evidence_grid_dict.json")

with open(evidence_clumps_dict_file, "r+") as f:
    evidence_clumps_dict = json.load(f)

bells_keys = util.bells_keys_success_list_from()
light_fp = util.bells_light_fp_from()
light_drop = util.bells_light_drop_from()
source_fp = util.bells_source_fp_from()
source_drop = util.bells_source_drop_from()

for i, key in enumerate(bells_keys):

    try:
        evidence_base = np.round(evidence_base_dict[key], 2)
        evidence_delaunay = np.round(evidence_delaunay_dict[key], 2)

        evidence = np.max([evidence_base, evidence_delaunay])
    except KeyError:
        evidence = 0.0

    # evidence values

    try:
        evidence_scaled = f"{np.round(evidence_scaled_dict[key], 2)}"
    except KeyError:
        evidence_scaled = 0.0


    try:
        evidence_source = f"{np.round(evidence_source_dict[key], 2)}"
    except KeyError:
        evidence_source = None

    try:
        evidence_bpl = f"{np.round(evidence_bpl_dict[key], 2)}"
    except KeyError:
        evidence_bpl = None

    try:
        evidence_multipole = f"{np.round(evidence_multipole_dict[key], 2)}"
    except KeyError:
        evidence_multipole = None

    try:
        evidence_decomp = f"{np.round(evidence_decomp_dict[key], 2)}"
    except KeyError:
        evidence_decomp = None

    if "slacs1432+6317" in key:
        evidence_decomp = None

    try:
        evidence_clumps = f"{np.round(evidence_clumps_dict[key], 2)}"
    except KeyError:
        evidence_clumps = None

    # False Positives

    if evidence_scaled_dict[key] < 10.0:
        evidence_scaled = r"\textbf{" + evidence_scaled + "}"

    try:
        if evidence_scaled_dict[key] > 10.0 and evidence_source_dict[key] < 10.0:
            evidence_source = r"\textbf{" + evidence_source + "}"
    except (KeyError, TypeError):
        pass

    try:
        if evidence_source_dict[key] > 10.0 and evidence_bpl_dict[key] < 10.0:
            evidence_bpl = r"\textbf{" + evidence_bpl + "}"
    except (KeyError, TypeError):
        pass

    try:
        if evidence_source_dict[key] > 10.0 and evidence_multipole_dict[key] < 10.0:
            evidence_multipole = r"\textbf{" + evidence_multipole + "}"
    except (KeyError, TypeError):
        pass


    try:
        if evidence_source_dict[key] > 10.0 and evidence_decomp_dict[key] < 10.0:
            evidence_decomp = r"\textbf{" + evidence_decomp + "}"
    except (KeyError, TypeError):
        pass

    try:
        if evidence_source_dict[key] > 10.0 and evidence_clumps_dict[key] < 10.0:
            evidence_clumps = r"\textbf{" + evidence_clumps + "}"
    except (KeyError, TypeError):
        pass

    # Large decreases

    try:
        if evidence - evidence_scaled_dict[key] > 10.0:
            evidence_scaled = evidence_scaled + r"$^\dagger$"
    except KeyError:
        pass

    try:
        if evidence_scaled_dict[key] - evidence_source_dict[key] > 10.0:
            evidence_source = evidence_source + r"$^\dagger$"
    except KeyError:
        pass

    try:
        if evidence_source_dict[key] - evidence_bpl_dict[key] > 10.0:
            evidence_bpl = evidence_bpl + r"$^\dagger$"

        if evidence_source_dict[key] - evidence_bpl_dict[key] < -10.0:
            evidence_bpl = evidence_bpl + r"^{*}"
    except (KeyError, TypeError):
        pass

    try:
        if evidence_source_dict[key] - evidence_multipole_dict[key] > 10.0:
            evidence_multipole = evidence_multipole + r"$^\dagger$"

        if evidence_source_dict[key] - evidence_multipole_dict[key] < -10.0:
            evidence_multipole = evidence_multipole + r"^{*}"
    except (KeyError, TypeError):
        pass

    try:
        if evidence_source_dict[key] - evidence_decomp_dict[key] > 10.0:
            evidence_decomp = evidence_decomp + r"$^\dagger$"

        if evidence_source_dict[key] - evidence_decomp_dict[key] < -10.0:
            evidence_decomp = evidence_decomp + r"^{*}"
    except KeyError:
        pass


    try:
        if evidence_source_dict[key] - evidence_clumps_dict[key] > 10.0:
            evidence_clumps = evidence_clumps + r"$^\dagger$"

        if evidence_source_dict[key] - evidence_clumps_dict[key] < -10.0:
            evidence_clumps = evidence_clumps + r"^{*}"
    except KeyError:
        pass

    try:
        latex = rf"{key.upper()} & {evidence} & {evidence_scaled}  & { evidence_source} & {evidence_bpl}  & {evidence_multipole} & { evidence_decomp}  & {evidence_clumps} \\[2pt]"
    except KeyError:
        latex = rf"{key} & & & \\[2pt]"

    # latex = af.text.Samples.latex(
    #     samples=samples_subhalo_dict[key],
    #     include_name=False,
    #     include_quickmath=True,
    #     prefix=prefix,
    # )

    latex_dict[key] = latex

for key in latex_dict.keys():

    print(f"{latex_dict[key]}")
