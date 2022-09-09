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
import matplotlib.pyplot as plt

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

pickle_file = path.join(pickle_path, "gui_mask", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_pl_dict = pickle.load(f)


pickle_file = path.join(pickle_path, "bpl", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_bpl_dict = pickle.load(f)


pickle_file = path.join(pickle_path, "decomp", f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_decomp_dict = pickle.load(f)


slacs_keys = util.slacs_mass_keys_list_from()

sigma = 3.0

mass_pl_list = []
upper_pl_list = []
lower_pl_list = []

mass_bpl_list = []
upper_bpl_list = []
lower_bpl_list = []

mass_decomp_list = []
upper_decomp_list = []
lower_decomp_list = []

for i, key in enumerate(slacs_keys):

    mass_pl_list.append(samples_pl_dict[key].median_pdf_vector[2])
    upper_pl_list.append(samples_pl_dict[key].error_vector_at_upper_sigma(sigma=sigma)[2])
    lower_pl_list.append(samples_pl_dict[key].error_vector_at_lower_sigma(sigma=sigma)[2])

    try:
        mass_bpl_list.append(samples_bpl_dict[key].median_pdf_vector[2])
        upper_bpl_list.append(samples_bpl_dict[key].error_vector_at_upper_sigma(sigma=sigma)[2])
        lower_bpl_list.append(samples_bpl_dict[key].error_vector_at_lower_sigma(sigma=sigma)[2])
    except KeyError:
        mass_bpl_list.append(1e9)
        upper_bpl_list.append(0.0)
        lower_bpl_list.append(0.0)

    mass_decomp_list.append(samples_decomp_dict[key].median_pdf_vector[2])
    upper_decomp_list.append(samples_decomp_dict[key].error_vector_at_upper_sigma(sigma=sigma)[2])
    lower_decomp_list.append(samples_decomp_dict[key].error_vector_at_lower_sigma(sigma=sigma)[2])


plot_path = path.join("paper", "images", "masses")

x_centre = np.arange(len(slacs_keys))
x_left = x_centre - 0.1
x_right = x_centre + 0.1

elinewidth = 8
capsize = 20

plt.figure(figsize=(16, 14))
plt.errorbar(
    x=slacs_keys,
    y=mass_pl_list,
  #  marker=".",
    linestyle="",
    elinestyle="--",
    elinewidth=elinewidth,
    capsize=capsize,
    yerr=[lower_pl_list, upper_pl_list],
    label="PL + Shear",
)
plt.errorbar(
    x=slacs_keys,
    y=mass_bpl_list,
  #  marker=".",
    linestyle="",
    elinewidth=elinewidth,
    capsize=capsize,
    yerr=[lower_bpl_list, upper_bpl_list],
    label="BPL + Shear",
)
plt.errorbar(
    x=slacs_keys,
    y=mass_decomp_list,
  #  marker=".",
    linestyle="",
    elinewidth=elinewidth,
    capsize=capsize,
    yerr=[lower_decomp_list, upper_decomp_list],
    label="Stellar + Dark + Shear",
)

#plt.xticks(np.arange(len(slacs_keys)))

plt.xticks(ticks=np.arange(len(slacs_keys)), labels=slacs_keys, rotation=45, fontsize=26)

plt.yscale('log',base=10)
plt.ylim([1e6, 1e12])
plt.yticks(fontsize=26)
plt.legend(fontsize=20)
plt.ylabel(r"$M^{\rm sub}_{\rm 200}$[M$_{\rm \odot}$]", fontsize=30)

plt.savefig(path.join(plot_path, f"masses.png"))