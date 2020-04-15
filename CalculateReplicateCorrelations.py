# import libraries
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse
import sys
from perseuspy import pd

# function definitions
# calculate correlation matrix
def calculate_correlation(m, method='pearson'):
    methods = {'pearson': lambda x: x.T.corr(method='pearson').values,
               'spearman': lambda x: x.T.corr(method='spearman').values,
               'kendall': lambda x: x.T.corr(method='kendall').values,
               'cosine': lambda x: cosine_similarity(x)}
    return methods[method](m)

# get lower triangle from the correlation matrix
def correlation_row(m, method='pearson'):
    cm = calculate_correlation(m, method=method)
    cv = cm[np.tril_indices(len(cm),k=-1)]
    return cv

# pivot a single df line for correlation matrix calculation
def reshapeRow(x, replicates='Replicate', variables=['Condition', 'Fraction']):
    x = x.reset_index()
    x.columns = np.append(x.columns.values[0:-1],['value'])
    if type(variables) == list:
        x['variables'] = [i+"_"+j for i,j in zip(x[variables[0]], x[variables[1]])]
        variables='variables'
    x = x.pivot(index=replicates, columns=variables, values='value')
    return x


# Script arguments
parser = argparse.ArgumentParser(description='Replicate correlation calculation')
parser.add_argument('input_file', help='Input file containing the matrix')
parser.add_argument('output_file', help='Output file that should contain the result')
parser.add_argument('-replicates', default='Replicate', help='Name of annotation row containing replicate assignments')
parser.add_argument('-variables', nargs='+', default=['Condition', 'Fraction'], help='Name(s) of annotation row(s) containing variables')
parser.add_argument('-method', default='cosine', help='Correlation method to use (cosine/pearson/kendall/spearman)')
parser.add_argument('-id', default='id', help='Column containing unique identifier')
args = parser.parse_args()
if len(args.variables) == 1:
    args.variables = args.variables[0]
print(args)


# Data loading
df = pd.read_perseus(args.input_file)
df_main = df.loc[range(len(df)), df.columns.get_level_values(level=args.replicates) != '']

# Preparation of new dataframe
reshapedRow = reshapeRow(df_main.iloc[0,:], replicates=args.replicates, variables=args.variables)
nameMatrix = np.array([["{}_{}".format(r1, r2) for r2 in np.unique(reshapedRow.index)] for r1 in np.unique(reshapedRow.index)])

# Calculation of correlations
correlations = df_main.apply(lambda x: pd.Series(correlation_row(reshapeRow(x, replicates=args.replicates, variables=args.variables), method=args.method)), axis=1)

# Returning output table
correlations.columns = nameMatrix[np.tril_indices(len(nameMatrix), k=-1)]
result = correlations.join(df[args.id])
result.to_perseus(args.output_file)