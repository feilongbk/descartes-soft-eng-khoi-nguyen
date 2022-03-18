# descartes_underwriting_technical_test

# Candidate: Khoi Nguyen NGUYEN, Paris, FRANCE

# email: feilongbk@gmail.com

## Introduction

The test can be decomposed into different parts that represent the process of pricing an insurance policy:

#### A. Data Collecting: Get earthquake data from the USGS API

#### B. Financial Modelling: Model an earthquake index-based policy

and compute several statistics

#### C. Performance Optimization: Collecting large amount of earthquake data using async

requests as a strategy to speed-up the process

## Solutions

### A. Data Collecting

#### OBSERVATION

When comparing Haversine distance computed by the formula in Wikipedia and the ones computed by other ways (haversine
2.5.1, https://www.vcalc.com/wiki/vCalc/Haversine+-+Distance, etc.), I observed that the results are coherent. But there
are still small errors: The calculation errors are minor (generally <1%) when comparing to difference source.

The reason might be difference in choice of parameter (Earth average radius), or the methods of calculation of
distance (Some website and APIs might use approximated formulae of Haversine for faster response. It is not clear that
USGS uses the same practic. But if therewas difference in formulae, the interesting are cases where distance computed by
our formula is smaller than distance calculated by USGS API

#### The consequence is that some events located near the boundary (max_radius) that should be accounted in our simulation could be excluded by USGS API (for example, an event with distance of 199.99 in by our method, and 200.01 by USGS, and the max_radius in the query is 200.0, which excludes the event)

#### This situation is rare, but can still happen

So it is safer to query max_radius with a tolerance of error while collecting earthquake data for simulation. I use
1.01*max_radius instead of  max_radius when loading data for simulation. 
The data collecting codes consist of a generic
query url builder, request and data formatting methods.

### B. Financial Modelling

#### OBSERVATION

A simple way is directly calculating the payout from the dataframe using Haversine distance and aggregation functions of
numpy and pandas. However, I want to try another way of design and implementation (similar to framework we used at SCOR
P&C for Nat Cat treaties and portfolios). Maybe Descartes has already a similar or better framework, but it is still interesting to test if this design works for index-based policy.

We can break the simulation of payout of a policy into different elementary steps:
(1) Scenario: in short, the event series that occur within a year/period/scenario. This abstraction enables integration
of data from other sources than USGS as long as the data format is the same. Formatting data is done outside of the
class Scenario (Inversion of Control)
(2) The earthquake dataframe is reformatted by an instance of a (Base)ScenarioGenerator. Depending on the type of risk,
and the dataformat, we implement different version of the data
(3) The policy (with its payout structure) is modeled by a (Base)Policy object containing limit, event type, and "
protection layers"
In our case where protection-layers are not linked, each layer (max_radius,payout_ratio,min_magnitude) independently
computes raw loss on event series. The policy object will aggregate the loss over location, layer and event within a
scenario to produce the payout of that scenario/year. The historical data (or data coming from other sources) is
reformatted into a list/series of Scenario, we will compute the payout over all of them and return a result as a
series (of payout).
(4) Finally, the Statistics Generator compute the required analysis (burning cost, or loss distribution, VaR, etc.) from
simulation result over the series of payout result.

### The simulation process can be described by the schema below:

#### Analysis Metadata

#### ==> Data Provider/ Loader (from a local database or APIs ) ==> USGS data frame

#### ==> Scenario Generator ==> series of scenarios

#### ==> Policy ==> Series of payout per year/scenario

#### ==> Stats Generator ==> Statistics and analysis

PROS:

- This design leverages the benefits of object-oriented programming (especially abstraction) and some classical design
  patterns like inversion of control, factory, etc.
- It is easier to validate and extend the code. as well as investigate in case of errors
- When it comes to model other types of policies, we will only need to implement the new behaviours of policy
- Can be used in a framework where analyst/underwriter team (with better business understanding) implement the business
  logic in policy classes. The rest of the job will be done by software engineers (a practice at many trading desks and
  risk departments).
- Can be easily integrated into microservice/User Interface or Analytics App for pricing and risk management, etc.

CONS:

- Require much time at the design phase
- The setup of the framework take more time
- Authors of the code should have a certain level in OOP to work with such framework
- It took me quite much time to finish the test

#### The implementation of the financial module can be found in core.financial_modelling

### C. Parallel Computing/Performance Optimization:

I have followed the indication of using a solution asyncio and iohttp. This is a very interesting way. 


Beside that, there are several problems with the USGS API.

1. The USGS API limit is only 20000 rows. Normally the simulation does not need such amount (as events are more distributed
   at low magnitude - which are rarely insured)
2. USGS has, apparently, a mechanism to prevent abusive usage of their API (slow down or temporary block requests from specific
   IPs). That might explain why some requests might take much time. (Usage of distance in the query might be another
   reason)
3. When the network connection is unstable, directly getting data from public API is not a good choice, especially for simulation of large portfolio of policies/contracts.

####So by curiosity I have also tried to study another data providing strategy, that is collecting the historical data and store in a database, and run an automated process to update events and modifications at USGS on a daily basis (using a parameters named updatedafter). In the simulation we will request from the local database/ or an in-house data API.


As the historical dataset is large, I have to split the query by intervals of longitudes ranging from -180 to 180 and
limiting only to significant events (for example magnitude > 4.0 for this test). At my estimation, downloading full
history could take up to 2 days. However the duration for weekly/daily update is several minutes. In short, centralizing
data from different sources into a datastore is a common practice, but I do not know if it suits the context of
Descartes, or if you have already another solution in production context.


#### The implementation of the historical data collecting code can be found in data_collecting.usgs

#### The local data store codes can be found in nano_data_platform: with relational_data_store for tabular and relational data based SQLite, a lightweight SQL database, key_value_datastore for NoSQL data, which used pickleDB, a lightweight database similar to Redis, and a flat_file_datastore for large data
#### I have also tried to build a simulation app with DASH for builing and simulation of policy and deployed it on Google Cloud. You can access the application with the credentials (user_001,password_001). The application is available for several weeks.
at the URL: http://35.198.191.123:2022








 

