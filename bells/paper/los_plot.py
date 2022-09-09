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

plot_path = path.join(workspace_path, "paper", "images", "los_plot")

pixel_scales = 0.04

dataset_path = "dataset"

dataset_name_list = [
    "SDSSJ0755+3445",  # Index 5
    "SDSSJ0029+2544",  # Index 0
    "SDSSJ0918+5104",  # Index 7
    "SDSSJ0113+0250",  # Index 1
    "SDSSJ2342-0120",  # Index 15
    "SDSSJ0201+3228",  # Index 2
    "SDSSJ1226+5457",  # Index 13
    "SDSSJ1201+4743",  # Index 12
]

vmax_dict = {
    "SDSSJ0755+3445": 0.3,
    "SDSSJ0029+2544": 0.3,
    "SDSSJ0918+5104": 0.3,
    "SDSSJ0113+0250" : 0.3,
    "SDSSJ2342-0120" : 0.3,
    "SDSSJ0201+3228": 0.3,
    "SDSSJ1226+5457": 0.3,
    "SDSSJ1201+4743": 0.3,
}

for dataset_name in dataset_name_list:

    dataset_path_image = os.path.join(dataset_path, dataset_name)

    image = al.Array2D.from_fits(
        file_path=f"{dataset_path_image}/image_origin.fits",
        pixel_scales=pixel_scales,
    )

    with open(path.join(dataset_path_image, "clump_centres.json")) as json_file:
        clump_centres = json.load(json_file)

    clump_centres_new = []

    for centre in clump_centres:

        centre_new = (centre[0] * 0.8, centre[1] * 0.8)

        clump_centres_new.append(centre_new)

    clump_centres = clump_centres_new

    """
    Observed Image
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{dataset_name.upper()} Image".replace("SDSSJ", "BELLS")
        ),
        ylabel=aplt.YLabel(labelpad=-2.0),
        cmap=aplt.Cmap(vmin=0.0, vmax=vmax_dict[dataset_name]),
        output=aplt.Output(
            path=plot_path, filename=dataset_name, format=["png", "pdf"], format_folder=True
        ),
    )

    visuals_2d = aplt.Visuals2D(positions=al.Grid2DIrregular(grid=clump_centres))

    imaging_plotter = aplt.Array2DPlotter(
        array=image, mat_plot_2d=mat_plot_2d, visuals_2d=visuals_2d
    )

    imaging_plotter.figure_2d()