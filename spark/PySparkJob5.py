import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def process(spark, flights_path, airlines_path, result_path):
    """
    The main process.

    :param spark: SparkSession
    :param flights_path: path to flights dataset
    :param airlines_path: path to airlines dataset
    :param result_path: path with transformations result
    """
    df_flights = spark.read.parquet(flights_path)
    df_airlines = spark.read.parquet(airlines_path)

    datamart_ = df_flights \
        .groupBy(f.col('AIRLINE').alias('AIRLINE_NAME')) \
        .agg(
            f.sum(f.when(f.col('CANCELLED') == 1, 0).when(f.col('DIVERTED') == 1, 0).otherwise(1)).alias('correct_count'),
            f.sum(f.col('DIVERTED')).alias('diverted_count'),
            f.sum(f.col('CANCELLED')).alias('cancelled_count'),
            f.avg(f.col('DISTANCE')).alias('avg_distance'),
            f.avg(f.col('AIR_TIME')).alias('avg_air_time'),
            f.sum(f.when(f.col('CANCELLATION_REASON') == 'A', 1).otherwise(0)).alias('airline_issue_count'),
            f.sum(f.when(f.col('CANCELLATION_REASON') == 'B', 1).otherwise(0)).alias('weather_issue_count'),
            f.sum(f.when(f.col('CANCELLATION_REASON') == 'C', 1).otherwise(0)).alias('nas_issue_count'),
            f.sum(f.when(f.col('CANCELLATION_REASON') == 'D', 1).otherwise(0)).alias('security_issue_count')) \
        .join(other=df_airlines, on=df_airlines['IATA_CODE'] == f.col('AIRLINE_NAME'), how='inner') \
        .select(f.col('AIRLINE').alias('AIRLINE_NAME'), f.col('correct_count'),
                f.col('diverted_count'), f.col('cancelled_count'), f.col('avg_distance'), f.col('avg_air_time'),
                f.col('airline_issue_count'), f.col('weather_issue_count'),
                f.col('nas_issue_count'), f.col('security_issue_count'))

    datamart_.write.parquet(result_path)


def main(flights_path, airlines_path, result_path):
    spark = _spark_session()
    process(spark, flights_path, airlines_path, result_path)


def _spark_session():
    """
    Create the SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('PySparkJob5').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flights_path', type=str, default='flights.parquet', help='Please set flights datasets path.')
    parser.add_argument('--airlines_path', type=str, default='airlines.parquet',
                        help='Please set airlines datasets path.')
    parser.add_argument('--result_path', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    flights_path = args.flights_path
    airlines_path = args.airlines_path
    result_path = args.result_path
    main(flights_path, airlines_path, result_path)
