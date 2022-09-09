"""
__Imports__
"""
import numpy as np
import os
from os import path
import warnings

warnings.filterwarnings("ignore")

import autofit as af
import autolens as al
import autolens.plot as aplt

from autoconf import conf

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
# pix = "base"
pix = "base__source_mask"
# pix = "delaunay"
# pix = "delaunay__source_mask"

database_name = f"subhalo_{pix}"

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

"""
__Query__
"""
agg_subhalo = agg
agg_subhalo = agg_subhalo.query(agg.search.name == "subhalo[1]_mass[total_refine]")

fit_imaging_agg = al.agg.FitImagingAgg(aggregator=agg_subhalo)
fit_imaging_gen = fit_imaging_agg.max_log_likelihood_gen_from()

for samples, search, fit_imaging in zip(
    agg_subhalo.values("samples"), agg_subhalo.values("search"), fit_imaging_gen
):

    path_prefix = search.paths.path_prefix

    lens_name = f'{path_prefix.replace("/", "_")}'

    lens_name_latex = util.lens_name_latex_from(lens_name=lens_name)
    subhalo_mass_latex = util.subhalo_mass_latex_from(lens_name=lens_name)
    subhalo_centre = util.subhalo_centre_from(lens_name=lens_name)

    title_plot = aplt.Title(label=f"{lens_name_latex} {subhalo_mass_latex}")

    plot_path = path.join(
        workspace_path, "paper", "images", "mass_pre_subhalo_normalized_residuals"
    )

    if subhalo_centre is not None:
        visuals_2d = aplt.Visuals2D(positions=al.Grid2DIrregular([subhalo_centre]))
    else:
        visuals_2d = aplt.Visuals2D()

    mat_plot_2d = aplt.MatPlot2D(
        title=title_plot,
        cmap=aplt.Cmap(vmax=2.0, vmin=-2.0),
        ylabel=aplt.YLabel(labelpad=-2.0),
        positions_scatter=aplt.PositionsScatter(marker="*", s=300),
        output=aplt.Output(
            filename=lens_name,
            path=plot_path,
            format=["png", "pdf"],
            format_folder=True,
        ),
    )

    include_2d = aplt.Include2D(border=False)

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging,
        mat_plot_2d=mat_plot_2d,
        include_2d=include_2d,
        visuals_2d=visuals_2d,
    )

    fit_imaging_plotter.figures_2d(normalized_residual_map=True)

    plot_path = path.join(
        workspace_path, "paper", "images", "lens_subtracted_images"
    )

    mat_plot_2d = aplt.MatPlot2D(
        title=title_plot,
        ylabel=aplt.YLabel(labelpad=-2.0),
        positions_scatter=aplt.PositionsScatter(marker="*", s=300),
        output=aplt.Output(
            filename=lens_name,
            path=plot_path,
            format=["png", "pdf"],
            format_folder=True,
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging,
        mat_plot_2d=mat_plot_2d,
        include_2d=include_2d,
        visuals_2d=visuals_2d,
    )

    fit_imaging_plotter.figures_2d_of_planes(plane_index=1, subtracted_image=True)
