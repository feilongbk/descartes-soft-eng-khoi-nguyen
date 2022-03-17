# descartes_underwriting_technical_test
# Candidate: Khoi Nguyen NGUYEN, Paris, FRANCE
# email: feilongbk@gmail.com

## Introduction
The test can be decomposed into different parts that represent the process of pricing an insurance policy:
A. Data Collecting: Get earthquake data from the USGS API
B. Financial Modelling: Model an earthquake index-based policy and compute several statistics
C. Performance Optimization: Collecting large amount of earthquake data using async requests as a strategy to speed-up the process




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
A simple way is directly calculating the payout from the dataframe using Haversine distance and aggregation functions of numpy and pandas.
However, I want to try another way of design and implementation (similar to a solution we used at SCOR P&C for Nat Cat reinsurance contracts and portfolios). Maybe Descartes has already a better financial modelling framework, but it is still interesting to test if this design works for index-based policy.
We break the simulation of payout into different steps:
(1) Scenario: in short, the event series that occur within a year/period/scenario. This abstraction enables integration of data from other sources than USGS as long as the data format is the same. Formatting data is done outside of the class Scenario (Inversion of Control)
(2) The earthquake dataframe is reformatted by an instance of a (Base)ScenarioGenerator. Depending on the type of risk, and the dataformat, we implement different version of the data
(3) The policy with its payout structure is modelled by a (Base)Policy object containing limit, event type, and "protection layers"

In our case where protection layers are not linked, each protection layer (max_radius,payout_ratio,min_magnitude) independently compute raw loss on event series.
The policy object will aggregate the loss over location, layer and event within a scenario to produce the payout of that scenario/year.
(4) Finally, the Statistics Generator compute analysis (burning cost, VaR, loss distrubution, etc) from simulation result over all scenarii/years

The simulation process can be described by the schema below:
(Analysis Metadata) 
==> Data Provider/ Loader (from a local database or APIs ) ==> (USGS data frame) 
==> Scenario Generator ==> (series of Scenario/ events per year) 
==> Policy ==> (series of payout per year/scenario) 
==> Stats Generator ==> (statistics and analysis for pricing and risk management)

PROS:
- This design leverages the benefits of object-oriented programming (especially abstraction) and some classical design patterns like inversion of control, factory, etc.
- It is easier to validate and extend the code. as well as investigate in case of errors
- When it comes to model other types of policies, we will only need to implement the new behaviours of policy
- Can be used in a framework where analyst/underwriter team (with better business understanding) implement the business logic in policy classes, the rest of the job will be done by software engineers (with more solid technical skills) (a practice at many trading desks and risk departments).
- Can be easily integrated into microservice/User Interface or Analytics App for pricing and risk management, etc.
  
CONS:
- Require much time at the design phase
- The setup of the framework take more time
- Authors of the code should have a certain level in OOP to work with such framework
- It took me quite much time to finish the test


#### The implementation of the financial module can be found in core.financial_modelling

### C. Parallel Computing/Performance Optimization:
I have followed the indication of using a solution asyncio and iohttp. This it is a very interesting way for running parallel requests.
However there are several problems. 
1. The USGS API limit is 20000 rows. Normally the simulation does not need such amount (as events are more distributed at low magnitude - which is rarely insured)
2. USGS has, apparently, a mechanism to prevent abusive usage of their API (slow down or block requests from specific IPs). That might explain why some requests might take much time. (Usage of distance in the query might be another reason)
3. When the network connection is unstable, directly getting data from public API is not a good choice.

I have also tried another strategy, that is collecting the historical data and store in a database and run an automatic process to update events and modifications at USGS on a daily basis (using a parameters named updatedafter).  
As the historical dataset is large, I have to split the query by intervals of longitudes ranging from -180 to 180 and limiting only to significant events (for example magnitude > 4.0 for this test).
At my estimation, downloading full history could take up to 2 days. However the duration for weekly/daily update is several minutes.
In short, centralizing data from different sources into a datastore is a common practice, but I do not know if it suits the context of Descartes, or if you have already another solution in place.

#### The implementation of the historical data collecting code can be found in data_collecting.usgs

### The local data store codes can be found in nano_data_platform: with relational_data_store for tabular and relational data based SQLite, a lightweight SQL database, key_value_datastore for NoSQL data, which used pickleDB, a lightweight database similar to Redis, and a flat_file_datastore for large data

### Of course the lightweight DBs do not suit professional purposes (but their industrial alternatives will), however, it might be a proof of concept of how a robust IT platform could be built. 









 

