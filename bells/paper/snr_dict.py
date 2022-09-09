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
    "SDSSJ0029+2544",  # Index 0
    "SDSSJ0113+0250",  # Index 1
    "SDSSJ0201+3228",  # Index 2
    "SDSSJ0237-0641",  # Index 3
    "SDSSJ0742+3341",  # Index 4
    "SDSSJ0755+3445",  # Index 5
    "SDSSJ0856+2010",  # Index 6
    "SDSSJ0918+5104",  # Index 7
    "SDSSJ1110+2808",  # Index 8
    "SDSSJ1110+3649",  # Index 9
    "SDSSJ1116+0915",  # Index 10
    "SDSSJ1141+2216",  # Index 11
    "SDSSJ1201+4743",  # Index 12
    "SDSSJ1226+5457",  # Index 13
    "SDSSJ2228+1205",  # Index 14
    "SDSSJ2342-0120",  # Index 15
]

snr_dict = {}

for dataset_name in dataset_name_list:

    print(dataset_name)

    dataset_path_image = os.path.join(dataset_path, dataset_name)

    with open(path.join(dataset_path_image, "info.json")) as json_file:
        info = json.load(json_file)

    if info["scaled_annular"]:

        imaging = al.Imaging.from_fits(
            image_path=f"{dataset_path_image}/image_scaled_via_annular.fits",
            psf_path=f"{dataset_path_image}/psf.fits",
            noise_map_path=f"{dataset_path_image}/noise_map_scaled_via_annular.fits",
            pixel_scales=pixel_scales,
            name=dataset_name,
        )

    else:

        imaging = al.Imaging.from_fits(
            image_path=f"{dataset_path_image}/image_scaled_via_bspline.fits",
            psf_path=f"{dataset_path_image}/psf.fits",
            noise_map_path=f"{dataset_path_image}/noise_map_scaled_via_bspline.fits",
            pixel_scales=pixel_scales,
            name=dataset_name,
        )

    mask = al.Mask2D.from_fits(
        file_path=f"{dataset_path_image}/mask_gui.fits",
        pixel_scales=pixel_scales,
    )

    imaging = imaging.apply_mask(mask=mask)

    snr_dict[dataset_name] = float(imaging.signal_to_noise_max)

print(snr_dict)