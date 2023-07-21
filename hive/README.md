### Overview

The dataset of New York yellow taxi data ([2020 Yellow Taxi Trip Data ](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)) 
has been used in practice. The data format description - ([Data Dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf))

---

#### Preparation

- create S3 bucket  (Object Storage)
- copy the data into the bucket


#### Task

1. Create database `yellow_taxi`. All the next steps should be done in it.


2. Create dimension tables according to the data format description. Storage format - _parquet_, column names - _id_, _name_.


3. Create the fact table for yellow taxi trips:
   - partitioning by the _start_ day trip
   - column names should be in camel case (`vendor_id`, `payment_type_id`, etc.)
   - storage format - _parquet_
   

4. Create _view_ for calculating datamart (see below).


5. Create the _datamart_ table type of:

    
| Payment type | Date       | Tips average amount | Passengers total |
|--------------|------------|---------------------|------------------|
| Cash         | 2020-01-31 | 999.99              | 112              |


6. Fill the datamart using the view formed at the step 4.
