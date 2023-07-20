### Overview

The dataset of New York yellow taxi data ([2020 Yellow Taxi Trip Data ](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)) 
has been used in practice. The data format description - ([Data Dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf))

---

#### Preparation

- create S3 bucket  (Object Storage)
- copy the data into the bucket


#### Task
Write the map-reduce application using data copied to Object storage and computing report for each month of 2020 type:

| Payment type | Month   | Tips average amount |
|--------------|---------|---------------------|
| Cash         | 2020-01 | 999.99              |

##### Requirements

- number of files -1
- format - csv
- sorting - `Month` by ascent, `Payment type` by ascent
- `Month` needs to be calculated for the _start_ date trip
