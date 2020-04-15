# PerseusPy-ReplicateCorrelation
Perseus tools for calculating replicate correlations for multivariate data.

## Main usage
This is meant as an extension to the correlation functions in Perseus. It allows to compare multivariate profiles of the same protein across replicates. Correlations will be calculated within each row based on annotation rows defining replicates and variables.

## Relevant parameters
- -replicates, default='Replicate': Name of the annotation row containing replicate assignments
- -variables, default=['Condition', 'Fraction']: Name(s) of annotation row(s) containing variables. If several are given they will be fused combinatorically. Important note: This needs ot be provided as first argument for the argparser to know how many following words to use.
- -method, default='cosine': Correlation method to use (cosine/pearson/kendall/spearman).
- -id, default='id': Column containing the unique identifier.

## Required libraries:
- sklearn
- numpy
- argparse
- sys
- perseuspy

## How-to
Copy the file to your machine and run it through the Persue menu External > python.

Example for additional arguments to provide:

-variables Timepoint -replicates Repeat -method pearson -id Uniprot
