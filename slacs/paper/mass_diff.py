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

plot_path = path.join(workspace_path, "paper", "images", "mass_diff")

# dataset_name = "slacs1430+4105"  # Index 33
# dataset_name = "slacs1213+6708"  # Index 33
dataset_name = "slacs0029-0055"  # Index 33

model_list = ["gui_mask", "bpl", "multipole", "decomp", "clumps"]

for model in model_list:

    """
    __Database__
    
    Load the database. If the file `slacs.sqlite` does not exist, it will be made by the method below, so its fine if
    you run the code below before the file exists.
    """

    database_name = f"slacs_{model}_0"

    json_path = path.join("paper", "json")

    evidence_dict_file = path.join(json_path, model, f"evidence_grid_dict.json")

    with open(evidence_dict_file, "r+") as f:
        evidence_dict = json.load(f)

    agg = af.Aggregator.from_database(
        filename=f"{database_name}.sqlite", completed_only=False
    )

    agg = agg.query((agg.search.name == "subhalo[1]_mass[total_refine]"))
    agg = agg.query((agg.search.unique_tag == dataset_name))

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
            mass_profile_centres=True,
        )

        lens_name = search.unique_tag
        filename = f"{lens_name}"

        evidence = np.round(evidence_dict[lens_name], 2)

        """
        Image
        """

        if "gui_mask" in model:

            mat_plot_2d = aplt.MatPlot2D(
                title=aplt.Title(
                    label=f"{lens_name.upper()} Image"
                ),
                ylabel=aplt.YLabel(labelpad=-2.0),
                cmap=aplt.Cmap(vmin=0.0, vmax=0.25),
                output=aplt.Output(
                    path=plot_path, filename=f"{filename}_{model}_image", format=["png", "pdf"], format_folder=True
                ),
            )

            fit_imaging_plotter = aplt.FitImagingPlotter(
                fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
            )

            fit_imaging_plotter.figures_2d(image=True)


        """
        Model Image
        """

        if "gui_mask" in model:
            evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{SO} " +  f"= {evidence}$"
        elif "bpl" in model:
            evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{BPL} " + f"= {evidence}$"
        elif "multipole" in model:
            evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{Multipole} " +  f"= {evidence}$"
        elif "decomp" in model:
            evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{Decomp} " +  f"= {evidence}$"
        elif "clumps" in model:
            evi_latex = r"$\Delta\,\mathrm{ln}\,\mathcal{L}^\mathrm{Los} " +  f"= {evidence}$"

        mat_plot_2d = aplt.MatPlot2D(
            title=aplt.Title(
                label=f"{lens_name.upper()} Model Image {evi_latex}"
            ),
            ylabel=aplt.YLabel(labelpad=-2.0),
            cmap=aplt.Cmap(vmin=0.0, vmax=0.25),
            output=aplt.Output(
                path=plot_path, filename=f"{filename}_{model}_model_image", format=["png", "pdf"], format_folder=True
            ),
        )

        fit_imaging_plotter = aplt.FitImagingPlotter(
            fit=fit_imaging, mat_plot_2d=mat_plot_2d, include_2d=include_2d
        )

        fit_imaging_plotter.figures_2d(model_image=True)