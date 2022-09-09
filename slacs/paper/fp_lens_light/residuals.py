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

plot_path = path.join(workspace_path, "paper", "images", "fp_lens_light")

"""
__Database__

Load the database. If the file `slacs.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
database_name = "slacs_base_1"

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
agg = agg.query((agg.search.unique_tag == "slacs2341+0000"))

# TODO : Residual map may be dodgy because fractiona_accuracy not used properly in Grid2DITerate due to source bug.

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

    lens_name = search.unique_tag
    filename = f"{lens_name}"
    evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L} =$"

    vval = np.max(np.abs(fit_imaging.normalized_residual_map)) / 10.0

    """
    Observed Image
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Image"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(vmin=0.0, vmax=1.2),
        output=aplt.Output(
            path=plot_path, filename="image", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d(image=True)

    """
    Lens Subtracted Image.
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Lens Light Subtracted Image"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(vmin=0.0, vmax=0.6),
        output=aplt.Output(
            path=plot_path, filename="subtracted_image", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d_of_planes(plane_index=1, subtracted_image=True)

    """
    Residual Map
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label="Normalized Residuals"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(vmin=-2.0, vmax=2.0),
        output=aplt.Output(
            path=plot_path, filename="normalized_residual_map", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d(normalized_residual_map=True)
