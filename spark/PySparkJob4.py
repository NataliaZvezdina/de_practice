import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def process(spark, flights_path, airlines_path, airports_path, result_path):
    """
    The main process.

    :param spark: SparkSession
    :param flights_path: path to flights dataset
    :param airlines_path: path to airlines dataset
    :param airports_path: path to airports dataset
    :param result_path: path with transformations result
    """
    df_flights = spark.read.parquet(flights_path)
    df_airlines = spark.read.parquet(airlines_path)
    df_airports = spark.read.parquet(airports_path)

    datamart_ = df_flights.withColumnRenamed('AIRLINE', 'AIRLINE_NAME') \
        .join(other=df_airlines, on=df_airlines['IATA_CODE'] == f.col('AIRLINE_NAME'), how='inner') \
        .join(other=df_airports, on=df_airports['IATA_CODE'] == f.col('ORIGIN_AIRPORT'), how='inner') \
        .select(f.col('AIRLINE').alias('AIRLINE_NAME'), f.col('TAIL_NUMBER'), f.col('COUNTRY').alias('ORIGIN_COUNTRY'),
                f.col('AIRPORT').alias('ORIGIN_AIRPORT_NAME'),
                f.col('LATITUDE').alias('ORIGIN_LATITUDE'), f.col('LONGITUDE').alias('ORIGIN_LONGITUDE'),
                f.col('DESTINATION_AIRPORT')) \
        .join(other=df_airports, on=df_airports['IATA_CODE'] == f.col('DESTINATION_AIRPORT'), how='inner') \
        .select(f.col('AIRLINE_NAME'), f.col('TAIL_NUMBER'), f.col('ORIGIN_COUNTRY'), f.col('ORIGIN_AIRPORT_NAME'),
                f.col('ORIGIN_LATITUDE'), f.col('ORIGIN_LONGITUDE'), f.col('COUNTRY').alias('DESTINATION_COUNTRY'),
                f.col('AIRPORT').alias('DESTINATION_AIRPORT_NAME'),
                f.col('LATITUDE').alias('DESTINATION_LATITUDE'),
                f.col('LONGITUDE').alias('DESTINATION_LONGITUDE'))

    datamart_.write.parquet(result_path)


def main(flights_path, airlines_path, airports_path, result_path):
    spark = _spark_session()
    process(spark, flights_path, airlines_path, airports_path, result_path)


def _spark_session():
    """
    Create the SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('PySparkJob4').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flights_path', type=str, default='flights.parquet', help='Please set flights datasets path.')
    parser.add_argument('--airlines_path', type=str, default='airlines.parquet', help='Please set airlines datasets path.')
    parser.add_argument('--airports_path', type=str, default='airports.parquet', help='Please set airports datasets path.')
    parser.add_argument('--result_path', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    flights_path = args.flights_path
    airlines_path = args.airlines_path
    airports_path = args.airports_path
    result_path = args.result_path
    main(flights_path, airlines_path, airports_path, result_path)
