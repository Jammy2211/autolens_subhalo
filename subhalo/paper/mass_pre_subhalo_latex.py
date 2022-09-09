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

agg = agg.order_by(agg.search.path_prefix)

"""
__Query__
"""
agg_subhalo = agg
agg_subhalo = agg_subhalo.query(agg.search.name == "subhalo[1]_mass[total_refine]")

latex_dict = {}

for samples, search in zip(
    agg_subhalo.values("samples"), agg_subhalo.values("search")
):

    # samples = samples.without_paths(
    #     [
    #         ("galaxies", "lens", "mass", "elliptical_comps"),
    # #        ("galaxies", "lens", "shear"),
    #     ]
    # )

    path_prefix = search.paths.path_prefix

    lens_name = f'{path_prefix.replace("/", "_")}'

    key = lens_name.replace(f"subhalo_{pix}_", "")

    lens_name_latex = util.lens_name_latex_from(lens_name=lens_name)
    subhalo_mass_latex = util.subhalo_mass_latex_from(lens_name=lens_name)

    latex = af.text.Samples.latex(
        samples=samples,
        include_name=False,
        include_quickmath=True,
        prefix=f"{lens_name_latex} & {subhalo_mass_latex} & ",
        suffix=r" \\[2pt]",
    )

    latex_dict[key] = latex



key_order_list = util.key_order_list_from()

import operator

sorted_tuples = sorted(latex_dict.keys(), key=lambda x:x.lower())

for key in key_order_list:

    print(f"{latex_dict[key]}")