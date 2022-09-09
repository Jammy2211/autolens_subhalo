import re


def lens_name_latex_from(lens_name):

    if "slacs" in lens_name:

        if "lens_0" in lens_name:
            return "$\mathrm{Lens}_{1}$"
        elif "lens_2" in lens_name:
            return "$\mathrm{Lens}_{2}$"
        elif "lens_1" in lens_name:
            return "REMOVE REMOVE REMOVE"

    if "bells" in lens_name:

        if "lens_0" in lens_name:
            return "$\mathrm{Lens}_{3}$"
        elif "lens_2" in lens_name:
            return "REMOVE REMOVE REMOVE"
        elif "lens_1" in lens_name:
            return "REMOVE REMOVE REMOVE"
        elif "lens_3" in lens_name:
            return "$\mathrm{Lens}_{4}$"


def subhalo_mass_latex_from(lens_name):

    if "subhalo_mass_105" in lens_name:
        return "$10^{10.5}M_{\odot}$"
    elif "subhalo_mass_100" in lens_name:
        return "$10^{10.0}M_{\odot}$"
    elif "subhalo_mass_95" in lens_name:
        return "$10^{9.5}M_{\odot}$"
    elif "no_subhalo" in lens_name:
        return "No Subhalo"


def survey_str_from(lens_name):

    if "slacs" in lens_name:
        return "slacs"
    elif "bells" in lens_name:
        return "bells"

def lens_str_from(lens_name):

    if "lens_0" in lens_name:
        return "lens_0"
    elif "lens_1" in lens_name:
        return "lens_1"
    elif "lens_2" in lens_name:
        return "lens_2"
    elif "lens_3" in lens_name:
        return "lens_3"

def subhalo_mass_str_from(lens_name):

    if "subhalo_mass_105" in lens_name:
        return "subhalo_mass_105"
    elif "subhalo_mass_100" in lens_name:
        return "subhalo_mass_100"
    elif "subhalo_mass_95" in lens_name:
        return "subhalo_mass_95"
    elif "no_subhalo" in lens_name:
        return "no_subhalo"

def subhalo_centre_from(lens_name):

    if "no_subhalo" in lens_name:
        return

    if "lens_0" in lens_name:
        return (1.901, 0.3)
    elif "lens_1" in lens_name:
        return (1.001, 0.3)
    elif "lens_2" in lens_name:
        return (1.341, 0.501)
    elif "lens_3" in lens_name:
        return (0.6, -1.251)


def vmin_vmax_from(lens_name):

    if "slacs" in lens_name:

        if "lens_0" in lens_name:
            return -3.0, 3.0
        elif "lens_2" in lens_name:
            return -2.0, 2.0
        elif "lens_1" in lens_name:
            return None, None

    if "bells" in lens_name:

        if "lens_0" in lens_name:
            return -3.0, 3.0
        elif "lens_2" in lens_name:
            return -3.0, 3.0
        elif "lens_1" in lens_name:
            return -2.0, 2.0
        elif "lens_3" in lens_name:
            return -3.0, 3.0
