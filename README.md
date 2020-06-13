# catch-bond-model
Analysis of catch-bond requirements of the kinetochore using mathematical model described in Akiyoshi et. al (2010).

Generates a matrix of different output types for combinations of k3 and k4 unloaded rates, assuming fixed k3 and k4 sensitivities, as well as k1 and k2 parameters.

The scripts in here are the same script essentially, except the output for each script calls for the outputs of differnet functions: the biphasic (binary) output; the optimum force output; the lifetime ratio output.

Using the code is fairly simple: just make sure the fixed variables are defined at the beginning of the script, and that the header text in the output accurately describes what the matrix is outputting. That will help users downstream when they are looking at the scoring matrix.

Darren Mallett
Asbury Lab
University of Washington, Seattle
