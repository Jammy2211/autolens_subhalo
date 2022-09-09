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
    "slacs0008-0004",  # Index 0
    "slacs0029-0055",  # Index 1
    "slacs0157-0056",  # Index 2
    "slacs0216-0813",  # Index 3
    "slacs0252+0039",  # Index 4
    "slacs0330-0020",  # Index 5
    "slacs0728+3835",  # Index 6
    "slacs0737+3216",  # Index 7
    "slacs0822+2652",  # Index 8
    "slacs0903+4116",  # Index 10
    "slacs0912+0029",  # Index 11
    "slacs0936+0913",  # Index 12
    "slacs0946+1006",  # Index 13
    "slacs0956+5100",  # Index 14
    "slacs0959+0410",  # Index 15
    "slacs1020+1122",  # Index 18
    "slacs1023+4230",  # Index 19
    "slacs1029+0420",  # Index 20
    "slacs1032+5322",  # Index 21
    "slacs1142+1001",  # Index 23
    "slacs1143-0144",  # Index 24
    "slacs1205+4910",  # Index 26
    "slacs1213+6708",  # Index 27
    "slacs1218+0830",  # Index 32
    "slacs1250+0523",  # Index 29
    "slacs1402+6321",  # Index 30
    "slacs1420+6019",  # Index 32
    "slacs1430+4105",  # Index 33
    "slacs1432+6317",  # Index 34
    "slacs1451-0239",  # Index 35
    "slacs1525+3327",  # Index 36
    "slacs1627-0053",  # Index 37
    "slacs1630+4520",  # Index 38
    "slacs2238-0754",  # Index 39
    "slacs2300+0022",  # Index 40
    "slacs2303+1422",  # Index 41
    "slacs2341+0000",  # Index 42
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