### Overview

The dataset of flights data ([2015 Flight Delays and Cancellations](https://www.kaggle.com/datasets/usdot/flight-delays)) 
has been used in practice. The work has been performing on prepared _parquet_ files with data on _airlines_, _airports_ 
and _flights_.

---

### Tasks

1. Build the summary table showing top 10 aircraft (`TAIL_NUMBER`) by number of departures at all times.


2. Find the top 10 air routs (`ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`) by number of flights, as well as calculate 
the average flight time (`AIR_TIME`).


3. Determine the list of airports that have the most problems with the delay on the flight. Calculate the average, 
minimum, maximum delay time and select airports only those where the maximum delay (`DEPARTURE_DELAY`) is _1000_ seconds
or more. Additionally calculate the correlation between delay time and week day (`DAY_OF_WEEK`).


4. Build a table based on our data with the required fields:
`AIRLINE_NAME`, `TAIL_NUMBER`, `ORIGIN_COUNTRY`, `ORIGIN_AIRPORT_NAME`, `ORIGIN_LATITUDE`, `ORIGIN_LONGITUDE`, 
`DESTINATION_COUNTRY`, `DESTINATION_AIRPORT_NAME`, `DESTINATION_LATITUDE`, `DESTINATION_LONGITUDE`.


5. The Analytics Department is interested in company statistics about problems. The task is to build a summary table 
of all airlines containing the following data:
   - `AIRLINE_NAME`
   - `correct_count` - number of flights performed
   - `diverted_count` - number of flights delayed
   - `cancelled_count` - number of flights cancelled
   - `avg_distance` - average distance of flights
   - `avg_air_time`- average time in the sky
   - `airline_issue_count` - delays due to aircraft problems (`CANCELLATION_REASON`)
   - `weather_issue_count` - delays due to weather conditions (`CANCELLATION_REASON`)
   - `nas_issue_count` - delays due to NAS problems (`CANCELLATION_REASON`)
   - `security_issue_count` - delays due to security problems (`CANCELLATION_REASON`)


---

#### Requirements

- Save the result in _parquet_ format
