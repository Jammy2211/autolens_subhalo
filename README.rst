Scanning For Dark Matter Subhalos in Hubble Space Telescope Imaging of 54 Strong Lenses
=======================================================================================

This repository contains result and scripts to accompany the paper "Scanning For Dark Matter Subhalos in \textit{Hubble} Space
Telescope Imaging of 54 Strong Lenses":.

https://arxiv.org/abs/2209.10566

Structure
---------

The workspace includes the following main directories:

- ``PyAuto``: The PyAutoLens (and parent projects) source code used to generate the results and paper figures. Use
this via a GitHub clone to run the .sqlite files.
- ``slacs``: The results of fits to the SLACS sample and visualization scripts to produce paper plots.
- ``bells``: The results of fits to the BELLS-GALLERY sample and visualization scripts to produce paper plots.
- ``subhalo``: The scripts used to generate latex tables and figures in the paper.

What Results Are Here?
----------------------

The ``slacs/output`` and ``bells/output`` folders contain folders with with following information for the lens light,
mass and subhalo models fitted to every lens:

- ``model.info``: The model parameterization and priors.
- ``model.results``: The inferred model parameters (maximum likelihood, 1 and 3 sigma confidence intervals).
- ``search.summary``: A summary of the _dynesty_ non-linear search.
- ``image``: Images showing the results of the fit, triangle plots and other quantities.

What Results Are Not Here?
--------------------------

Due to GitHub file size limits the following results are not included:

- The Source pipeline results which perform model-fits initializing the source pixelization.
- The ``image`` folder of every fit of the subhale grid search (``subhalo[2]_mass[total]_source_subhalo[search_lens_plane]``).
- The ``dynesty` samples of every fit.

How Do I Get Those Results?
---------------------------

Sqlite3 databases containing all of the results, including the full Dynesty samples, can be found at the following
Zenodo links:

https://zenodo.org/record/7051604#.YxjdFdTML-g

These databases are required to reproduce the majority of visuals in the paper via the scripts on this repository.

