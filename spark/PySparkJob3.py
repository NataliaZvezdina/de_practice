import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def process(spark, flights_path, result_path):
    """
    The main process.

    :param spark: SparkSession
    :param flights_path: path to flights dataset
    :param result_path: path with transformations result
    """
    df_flights = spark.read.parquet(flights_path) \
        .groupBy(f.col('ORIGIN_AIRPORT')) \
        .agg(f.avg(f.col('DEPARTURE_DELAY')).alias('avg_delay'),
             f.min(f.col('DEPARTURE_DELAY')).alias('min_delay'),
             f.max(f.col('DEPARTURE_DELAY')).alias('max_delay'),
             f.corr(f.col('DEPARTURE_DELAY'), f.col('DAY_OF_WEEK')).alias('corr_delay2day_of_week')) \
        .where(f.col('max_delay') >= 1000)

    df_flights.write.parquet(result_path)


def main(flights_path, result_path):
    spark = _spark_session()
    process(spark, flights_path, result_path)


def _spark_session():
    """
    Create the SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('PySparkJob3').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flights_path', type=str, default='flights.parquet', help='Please set flights datasets path.')
    parser.add_argument('--result_path', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    flights_path = args.flights_path
    result_path = args.result_path
    main(flights_path, result_path)
