"""
__Imports__
"""

import os
from os import path
import re
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
pix = "base"

database_name = f"subhalo_base"

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

search_gen = agg_subhalo.values("search")

for fit_imaging, search in zip(fit_imaging_gen, search_gen):

    plot_path = path.join(workspace_path, "paper", "images", "data")

    lens_name = f'{search.paths.path_prefix.replace("/", "_")}'

    lens_name_latex = util.lens_name_latex_from(lens_name=lens_name)
    subhalo_mass_latex = util.subhalo_mass_latex_from(lens_name=lens_name)
    subhalo_centre = util.subhalo_centre_from(lens_name=lens_name)

    title_plot = aplt.Title(label=f"{lens_name_latex}: Image")

    if subhalo_centre is not None:
        visuals_2d = aplt.Visuals2D(positions=al.Grid2DIrregular([subhalo_centre]))
    else:
        visuals_2d = aplt.Visuals2D()

    filename = lens_name.replace("subhalo_base_", "data_")

    mat_plot_2d = aplt.MatPlot2D(
        title=title_plot,
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(cmap="default"),
        output=aplt.Output(
            path=plot_path,
            filename=filename,
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

    fit_imaging_plotter.figures_2d(image=True)
