"""
__Imports__
"""
import json
import numpy as np
import os
from os import path
import warnings

warnings.filterwarnings("ignore")

import autofit as af
import autolens as al
import autolens.plot as aplt

from autoconf import conf

"""
__Paths__
"""
workspace_path = os.getcwd()

config_path = path.join(workspace_path, "config")
conf.instance.push(new_path=config_path)

plot_path = path.join(workspace_path, "paper", "images", "mass_subhalo_diff")

# dataset_name = "slacs0029-0055"
dataset_name = "slacs0946+1006"
# dataset_name = "slacs1430+4105"  # Index 33

# model_list = ["gui_mask", "decomp"]

# model = "gui_mask"
model = "decomp"

database_name = f"slacs_{model}_0"

json_path = path.join("paper", "json")

evidence_dict_file = path.join(json_path, model, f"evidence_grid_dict.json")

with open(evidence_dict_file, "r+") as f:
    evidence_dict = json.load(f)

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

agg_query = agg.query((agg.search.name == "subhalo[1]_mass[total_refine]"))
agg_query = agg_query.query((agg_query.search.unique_tag == dataset_name))

"""
Unique Tag Query Does Not Work
"""
fit_imaging_agg_query = al.agg.FitImagingAgg(aggregator=agg_query)
fit_imaging_gen = fit_imaging_agg_query.max_log_likelihood_gen_from()

search_gen = agg_query.values("search")

for search, fit_imaging in zip(search_gen, fit_imaging_gen):

    model_image_gui_mask = fit_imaging.model_image

database_name = f"slacs_{model}_1"

json_path = path.join("paper", "json")

evidence_dict_file = path.join(json_path, model, f"evidence_grid_dict.json")

with open(evidence_dict_file, "r+") as f:
    evidence_dict = json.load(f)

agg_query = agg.query((agg_query.search.name == "subhalo[3]_subhalo[single_plane_refine]"))
agg_query = agg_query.query((agg_query.search.unique_tag == dataset_name))

"""
Unique Tag Query Does Not Work
"""
fit_imaging_agg_query = al.agg.FitImagingAgg(aggregator=agg_query)
fit_imaging_gen = fit_imaging_agg_query.max_log_likelihood_gen_from()

search_gen = agg_query.values("search")

for search, fit_imaging in zip(search_gen, fit_imaging_gen):

    path_prefix = search.paths.path_prefix
    lens_name = search.unique_tag

    model_image_decomp = fit_imaging.model_image

include_2d = aplt.Include2D(
    border=False,
    critical_curves=True,
    light_profile_centres=False,
    mass_profile_centres=True,
)

filename = f"{lens_name}"

evidence = np.round(evidence_dict[lens_name], 2)
#
# if "gui_mask" in model:
#     evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{SO} " +  f"= {evidence}$"
# elif "bpl" in model:
#     evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{BPL} " + f"= {evidence}$"
# elif "decomp" in model:
#     evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{decomp} " +  f"= {evidence}$"
# elif "decomp" in model:
#     evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{Decomp} " +  f"= {evidence}$"
# elif "clumps" in model:
#     evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{Los} " +  f"= {evidence}$"

# vval = np.max(np.abs(fit_imaging.normalized_residual_map)) / 10.0

"""
Model Image
"""

evi_latex = 0.0

mat_plot_2d = aplt.MatPlot2D(
    title=aplt.Title(
        label=f"{lens_name.upper()} Model Image {evi_latex}"
    ),
    ylabel=aplt.YLabel(labelpad=-2.0),
    cmap=aplt.Cmap(vmin=0.0, vmax=0.007),
    output=aplt.Output(
        path=plot_path, filename=f"{filename}_{model}_subhalo_image_residual", format=["png", "pdf"], format_folder=True
    ),
)

arr = model_image_decomp - model_image_gui_mask

fit_imaging_plotter = aplt.Array2DPlotter(
    array=arr, mat_plot_2d=mat_plot_2d, include_2d=include_2d
)

fit_imaging_plotter.figure_2d()