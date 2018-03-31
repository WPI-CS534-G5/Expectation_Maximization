# Expectation-Maximization
### Authors
 - Heric Flores Huerta
 - Eduardo Calle Ortiz
 - Nikolaos Kalampalikis

## Program Behavior

### Run & Input
`$python main.py [data] [C]`

 - `data` is a csv file of n-dimensional data points where each dimension is a column and each point is a row.
 - `C` is either `X` or a number >= 1. This represents the number of clusters to run EM with or to use a BIC(Bayesian Information Criterion) estimate of the number of clusters in the data-set.

Example
`$python em.py data.csv X`


### Output
Running with a given number of clusters will output output the same final information as running with the BIC calculations. Running with BIC and the `DEBUG` flags set will output calculations for each number of clusters tried.