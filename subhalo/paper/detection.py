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

import pickle
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

"""
__Evidence__
"""
pickle_path = path.join("paper", "pickles")

pickle_file = path.join(pickle_path, pix, f"samples_subhalo_dict.pickle")

with open(pickle_file, "rb") as f:
    samples_subhalo_dict = pickle.load(f)


json_path = path.join("paper", "json")

evidence_dict_file = path.join(json_path, pix, f"evidence_grid_dict.json")

with open(evidence_dict_file, "r+") as f:
    evidence_dict = json.load(f)


agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)
"""
__Query__
"""

agg_grid = agg.grid_searches()

agg_best_fits = agg_grid.best_fits()

fit_imaging_agg = al.agg.FitImagingAgg(aggregator=agg_best_fits)
fit_imaging_gen = fit_imaging_agg.max_log_likelihood_gen_from()

search_gen = agg_best_fits.values("search")

for fit_grid, search, fit_imaging_detect in zip(
    agg_grid, search_gen, fit_imaging_gen
):

    path_prefix = search.paths.path_prefix

    key = search.paths.path_prefix.replace("/", "_")
    key = key.replace(f"subhalo_{pix}_", "")

    lens_name = f'{path_prefix.replace("/", "_")}'

    lens_name_latex = util.lens_name_latex_from(lens_name=lens_name)
    subhalo_mass_latex = util.subhalo_mass_latex_from(lens_name=lens_name)
    subhalo_centre = util.subhalo_centre_from(lens_name=lens_name)

    try:
        evidence_base = np.round(evidence_dict[key], 2)
    except KeyError:
        evidence_base = None

    evidence_label = util.evidence_label_from(pix=pix)

    evi_latex = r"$\Delta\,\mathrm{ln}\," + f"{evidence_label} =$"

    #   try:

    subhalo_search_result = al.subhalo.SubhaloResult(
        grid_search_result=fit_grid["result"], result_no_subhalo=fit_grid.parent
    )

    # except AttributeError:
    #
    #     print("PLOT FAILED")
    #
    #     continue

    plot_path = path.join(
        workspace_path, "paper", "images", "detect", database_name
    )

    title_plot = aplt.Title(
        label=f"{lens_name_latex} {subhalo_mass_latex} ({evi_latex} {evidence_base})"
    )

    mat_plot_2d = aplt.MatPlot2D(
        title=title_plot,
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(cmap="default"),
        output=aplt.Output(
            path=plot_path,
            filename=lens_name,
            format=["png", "pdf"],
            format_folder=True,
        ),
    )

    if subhalo_centre is not None:
        visuals_2d = aplt.Visuals2D(positions=al.Grid2DIrregular([subhalo_centre]))
    else:
        visuals_2d = aplt.Visuals2D()

    include_2d = aplt.Include2D(border=False)

    subhalo_plotter = al.subhalo.SubhaloPlotter(
        subhalo_result=subhalo_search_result,
        fit_imaging_detect=fit_imaging_detect,
        use_log_evidences=False,
        use_stochastic_log_likelihoods=False,
        mat_plot_2d=mat_plot_2d,
        visuals_2d=visuals_2d,
        include_2d=include_2d,
    )

    subhalo_plotter.figure_with_detection_overlay(
        image=True, remove_zeros=True, overwrite_title=False
    )
