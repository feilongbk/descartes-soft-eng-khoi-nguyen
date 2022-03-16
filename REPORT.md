# descartes_underwriting_technical_test
# Candidate: Khoi Nguyen NGUYEN, Paris, FRANCE
# email: feilongbk@gmail.com
## Disclaimer
This project is a part of the recruitment process for a position at Descartes Underwriting.
It is realized by the candidate (Khoi Nguyen NGUYEN).
Solutions and ideas presented in the project are not mean to be used for a production environment without careful study, adaptation and testing. The candidate refused all responsibility related to eventual losses and due to usage of these solutions for professional purpose.

## Introduction
The test can be decomposed into different parts that represent the process of pricing an insurance policy:
A. Data Collecting: Get earthquake data from the USGS API
B. Financial Modelling: Model an earthquake index-based policy and compute several statistics
C. Performance Optimization: Collecting large amount of earthquake data using async requests as a strategy to speed-up 

The solution consists of 3 parts:
1. Fulfill the objectives of the test
2. Study of the context and propose another strategy that could improve the solution presented in 1, from software engineering and system architecture point of view.
3. Demonstration of the proposed strategy by a little PoC

## SOLUTIONS
### A. Data Collecting
#### O:
There can be difference in the method of calculation of distance
This can come from the choice of value of Earth average radius
Or usage of approximation formula for faster calculation (especially for API involving search like USGS)
The calculation errors are minored (generally <1%) when comparing to difference source
However, we can be found in cases where distance computed by our formula is greater than distance calculated by USGS API, 
#### The consequence is that some events located near max_radius that should be accounted in our simulation are excluded by USGS API
#### This can be rare, but still can happen
So it is safer to query max_radius with a tolerance of error, I use 1.01*max_radius in stead of max_radius when loading data for simulation

### B.     


