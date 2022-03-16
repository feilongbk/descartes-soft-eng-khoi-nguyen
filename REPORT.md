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
#### OBSERVATION
When comparing Haversine distance computed by the formula in Wikipedia and the ones computed by other ways (haversine 2.5.1, https://www.vcalc.com/wiki/vCalc/Haversine+-+Distance, etc.), I realized that the results are coherent. However there are still small differences.
The reason might be difference in  choice of parameter (Earth average radius)  or the methods of calculation of distance (Some website and APIs might use approximated formulae of Haversine for faster response (It is not clear that USGS uses the same practices)).
The calculation errors are minor (generally <1%) when comparing to difference source.
The particular case, we can be found in cases where distance computed by our formula is greater than distance calculated by USGS API, 
#### The consequence is that some events located near the boundary (max_radius) that should be accounted in our simulation could be excluded by USGS API
#### This case can be rare, but still can happen
So it is safer to query max_radius with a tolerance of error while collecting earthquake data for simulation, I use 1.01*max_radius in stead of max_radius when loading data for simulation.
The request code consists of a generic query url builder, request and data formatting methods.

### B. Financial Modelling
Computing the payouts directly from a dataframe and policy term and conditions can be done easily and quickly. However, processing in this way makes it difficult to unit test, debug, or investigate when it comes to errors.
I allow myself to present an idea of a financial modelling framework 

So I break the modelling into different steps:
(1) Scenario: in short, the event series that occur within a year/period/scenario. This abstraction enables integration of data from other sources than USGS as long as the data format is the same. Formatting data is done outside of the class Scenario (Inversion of Control)
(2) The earthquake dataframe is reformatted by an instance of a (Base)ScenarioGenerator. Depending on the type of risk, and the dataformat, we implement different version of the data
(3) The policy with its payout structure is modelled by a (Base)Policy object containing limit, event type, and "protection layers"
In our case where protection layers are not linked, each protection layer (max_radius,payout_ratio,min_magnitude) independently compute raw loss on event series.
The policy object will aggregate the loss over location, layer and event within a scenario to produce the payout of that scenario/year.
(4) Finally, the Statistics Generator compute analysis (burning cost, VaR, loss distrubution, etc) from simulation result over all scenarii/years is 

The simulation process can be describe by the schema below:
(Analysis Metadata) 
==> Data Provider/ Loader (from a local database or APIs ) ==> (USGS data frame) 
==> Scenario Generator ==> (series of Scenario/ events per year) 
==> Policy ==> (series of payout per year/scenario) 
==> Stats Generator ==> (statistics and analysis for pricing and risk management)

### C. Parallel Computing/Performance Optimization:
Following the indications, 




 

