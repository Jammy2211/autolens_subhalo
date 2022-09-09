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

plot_path = path.join(workspace_path, "paper", "images", "lens_light_residuals")

"""
__Database__

Load the database. If the file `slacs.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
database_name = "slacs_base_1"
dataset_name = "slacs2341+0000"

# database_name = "slacs_base_0"
# dataset_name = "slacs0252+0039"

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

json_path = path.join("paper", "json")

evidence_delaunay_dict_file = path.join(json_path, "delaunay", f"evidence_dict.json")

with open(evidence_delaunay_dict_file, "r+") as f:
    evidence_delaunay_dict = json.load(f)

evidence_base_dict_file = path.join(json_path, "base", f"evidence_dict.json")

with open(evidence_base_dict_file, "r+") as f:
    evidence_base_dict = json.load(f)

"""
__Query__
"""
agg = agg.query((agg.search.name == "subhalo[1]_mass[total_refine]"))
unique_tag = agg.search.unique_tag
agg = agg.query(unique_tag == dataset_name)

fit_imaging_agg = al.agg.FitImagingAgg(aggregator=agg, use_hyper_scaling=False)
fit_imaging_gen = fit_imaging_agg.max_log_likelihood_gen_from()

search_gen = agg.values("search")

for search, fit_imaging in zip(search_gen, fit_imaging_gen):

    path_prefix = search.paths.path_prefix

    include_2d = aplt.Include2D(
        border=False,
        critical_curves=False,
        light_profile_centres=False,
        mass_profile_centres=False,
    )

    evidence_base = np.round(evidence_base_dict[search.unique_tag], 2)
    evidence_delaunay = np.round(evidence_delaunay_dict[search.unique_tag], 2)

    evidence = np.max([evidence_delaunay, evidence_base])

    lens_name = search.unique_tag
    filename = f"{lens_name}"
    evi_latex = r"$\Delta\,\mathrm{ln}\,\epsilon_{\rm base} =$"

    vval = np.max(np.abs(fit_imaging.normalized_residual_map)) / 10.0

    ### Image ###

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Image"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(norm="log", vmin=1e-2, vmax=1.0),
        output=aplt.Output(
            path=plot_path, filename=f"{filename}_image", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d(image=True)

    ### Image Lens Sub ###

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Lens Subtracted Image"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(norm="log", vmin=1e-2, vmax=1.0),
        output=aplt.Output(
            path=plot_path, filename=f"{filename}_image_lens_sub", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d_of_planes(plane_index=1, subtracted_image=True)

    ### NORMALIZED RESIDUAL MAP ###

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Normalized Residuals"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(vmin=-2.0, vmax=2.0),
        output=aplt.Output(
            path=plot_path, filename=f"{filename}_norm", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d(normalized_residual_map=True)
