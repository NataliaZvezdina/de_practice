create schema yellow_taxi location 's3a://karpov-test-h1/warehouse';
set hive.execution.engine=tez;

use yellow_taxi;

-- create dim tables
create external table dim_vendor
(
    id int,
    name string
)
stored as parquet;

insert into dim_vendor
select 1, 'Creative Mobile Technologies'
union all
select 2, 'VeriFone Inc';

create external table dim_rates
(
    id int,
    name string
)
stored as parquet;

insert into dim_rates
select 1, 'Standard rate'
union all
select 2, 'JFK'
union all
select 3, 'Newark'
union all
select 4, 'Nassau or Westchester'
union all
select 5, 'Negotiated fare'
union all
select 6, 'Group ride';

create external table dim_payment
(
    id int,
    name string
)
stored as parquet;

insert into dim_payment
select 1, 'Credit card'
union all
select 2, 'Cash'
union all
select 3, 'No charge'
union all
select 4, 'Dispute'
union all
select 5, 'Unknown'
union all
select 6, 'Voided trip';


-- create temporary table
create external table temp_table
(
vendor_id string,
tpep_pickup_datetime timestamp,
tpep_dropoff_datetime timestamp,
passenger_count int,
trip_distance double,
ratecode_id int,
store_and_fwd_flag string,
pulocation_id int,
dolocation_id int,
payment_type int,
fare_amount double,
extra double,
mta_tax double,
tip_amount double,
tolls_amount double,
improvement_surcharge double,
total_amount double,
congestion_surcharge double
)
row format delimited
fields terminated by ','
lines terminated by '\n'
location 's3a://karpov-test-h1/2020'
tblproperties ("skip.header.line.count"="1");


-- create partition table and insert the data from temporary table
set hive.exec.dynamic.partition = true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.max.dynamic.partitions=300;

create external table taxi_data (
vendor_id string,
tpep_pickup_datetime timestamp,
tpep_dropoff_datetime timestamp,
passenger_count int,
trip_distance double,
ratecode_id int,
store_and_fwd_flag string,
pulocation_id int,
dolocation_id int,
payment_type_id int,
fare_amount double,
extra double,
mta_tax double,
tip_amount double,
tolls_amount double,
improvement_surcharge double,
total_amount double,
congestion_surcharge double
)
partitioned by (dt date)
stored AS parquet;

insert into taxi_data partition(dt) select *, to_date(tpep_pickup_datetime) from temp_table;


-- create view and the datamart based on view
create view if not exists taxi_view as
select p.name as `Payment type`, t.dt as `Date`,round(avg(t.tip_amount), 2) as `Tips average amount`,
       sum(t.passenger_count) as `Passengers total`
from taxi_data t JOIN dim_vendor v ON t.vendor_id = v.id
                 JOIN dim_rates r ON t.ratecode_id = r.id
                 JOIN dim_payment p ON t.payment_type_id = p.id
where extract(year from t.dt) = 2020 and t.tip_amount >= 0 group by t.dt, p.name;

create table taxi_datamart location 's3a://karpov-test-h1/warehouse/taxi_datamart' as
select * from taxi_view;
