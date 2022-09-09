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

pixel_scales = 0.05

dataset_path = "dataset"

dataset_name_list = [
    "slacs0956+5100",  # Index 14
    "slacs0946+1006"
]

vmax_dict = {
    "slacs0956+5100":1.2,
    "slacs0946+1006": 1.2,
}

for dataset_name in dataset_name_list:

    dataset_path_image = os.path.join(dataset_path, dataset_name)

    image = al.Array2D.from_fits(
        file_path=f"{dataset_path_image}/F814W_image.fits",
        pixel_scales=pixel_scales,
    )

    with open(path.join(dataset_path_image, "clump_centres.json")) as json_file:
        clump_centres = json.load(json_file)

    """
    Observed Image
    """

    mat_plot_2d = aplt.MatPlot2D(
        title=aplt.Title(
            label=f"{dataset_name.upper()} Image"
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