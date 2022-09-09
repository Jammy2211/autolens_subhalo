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

"""
__Database__

Load the database. If the file `bells.sqlite` does not exist, it will be made by the method below, so its fine if
you run the code below before the file exists.
"""
# database_name = "bells_base"
database_name = "bells_delaunay"

# database_name = "bells_scaled"

# database_name = "bells_clumps"

# database_name = "bells_decomp"

# database_name = "bells_dec_clumps"

agg = af.Aggregator.from_database(
    filename=f"{database_name}.sqlite", completed_only=False
)

"""
__Evidence__
"""
json_path = path.join("paper", "json")

evidence_base_dict_file = path.join(json_path, "base", f"evidence_grid_dict.json")

with open(evidence_base_dict_file, "r+") as f:
    evidence_base_dict = json.load(f)

evidence_delaunay_dict_file = path.join(json_path, "delaunay", f"evidence_grid_dict.json")

with open(evidence_delaunay_dict_file, "r+") as f:
    evidence_delaunay_dict = json.load(f)

"""
__Query__
"""

agg_grid = agg.grid_searches()

"""
Unique Tag Query Does Not Work
"""
agg_best_fits = agg_grid.best_fits()

fit_imaging_agg = al.agg.FitImagingAgg(aggregator=agg_best_fits)
fit_imaging_gen = fit_imaging_agg.max_log_likelihood_gen_from()

search_gen = agg_best_fits.values("search")

info_gen = agg_best_fits.values("info")

for fit_grid, search, fit_imaging_detect, info in zip(
    agg_grid, search_gen, fit_imaging_gen, info_gen
):

    path_prefix = search.paths.path_prefix

    try:
        subhalo_search_result = al.subhalo.SubhaloResult(
            grid_search_result=fit_grid["result"], result_no_subhalo=fit_grid.parent
        )

        plot_path = path.join(
            workspace_path, "paper", "images", "detection", database_name
        )

        evidence_base = np.round(evidence_base_dict[search.unique_tag], 2)
        evidence_delaunay = np.round(evidence_delaunay_dict[search.unique_tag], 2)

        evidence = np.max([evidence_base, evidence_delaunay])

        filename = f'{path_prefix.replace("/", "_")}'
        #   filename = filename.replace("subhalo_bells_", "")
        filename = filename.replace(f"{database_name}_", "")
        filename = f"delaunay_{filename}"

        lens_name = search.unique_tag
        evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^{\rm Del} =$"

        mat_plot_2d = aplt.MatPlot2D(
            title=aplt.Title(
                label=f"{lens_name.upper()} ({evi_latex} {evidence})"
                #    f"{evidence_delaunay})"
            ),
            cmap=aplt.Cmap(cmap="default"),
            ylabel=aplt.YLabel(labelpad=-2.0),
            output=aplt.Output(
                path=plot_path,
                filename=filename,
                format=["png", "pdf"],
                format_folder=True,
            ),
        )

        include_2d = aplt.Include2D(border=False)

        subhalo_plotter = al.subhalo.SubhaloPlotter(
            subhalo_result=subhalo_search_result,
            fit_imaging_detect=fit_imaging_detect,
            use_log_evidences=False,
            use_stochastic_log_likelihoods=False,
            mat_plot_2d=mat_plot_2d,
            include_2d=include_2d,
        )

        subhalo_plotter.figure_with_detection_overlay(image=True, remove_zeros=True)

    except (AttributeError, KeyError):

        print(f"The lens {search.unique_tag} could not be loaded.")
