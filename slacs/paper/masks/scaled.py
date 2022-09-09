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

plot_path = path.join(workspace_path, "paper", "images", "masks")

"""
__Database__

Load the database. If the file `slacs.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
database_name = "slacs_scaled_1"

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

agg = agg.query((agg.search.name == "subhalo[1]_mass[total_refine]"))
agg = agg.query((agg.search.unique_tag == "slacs1430+4105"))

"""
Unique Tag Query Does Not Work
"""
fit_imaging_agg = al.agg.FitImagingAgg(aggregator=agg)
fit_imaging_gen = fit_imaging_agg.max_log_likelihood_gen_from()

search_gen = agg.values("search")

for search, fit_imaging in zip(search_gen, fit_imaging_gen):

    path_prefix = search.paths.path_prefix

    include_2d = aplt.Include2D(
        border=False,
        critical_curves=True,
        light_profile_centres=False,
        mass_profile_centres=False,
    )

#    evidence_voronoi = np.round(evidence_voronoi_dict[search.unique_tag], 2)
#    evidence_delaunay = np.round(evidence_delaunay_dict[search.unique_tag], 2)

    lens_name = search.unique_tag
    filename = f"{lens_name}"
    evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L} =$"

    vval = np.max(np.abs(fit_imaging.normalized_residual_map)) / 10.0

    """
    Observed Image
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{lens_name.upper()} Lens Light Cleaned S/N Map"
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
     #   cmap=aplt.Cmap(vmin=0.0, vmax=1.2),
        output=aplt.Output(
            path=plot_path, filename="scaled", format=["png", "pdf"], format_folder=True
        ),
    )

    fit_imaging_plotter = aplt.FitImagingPlotter(
        fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
    )

    fit_imaging_plotter.figures_2d(signal_to_noise_map=True)