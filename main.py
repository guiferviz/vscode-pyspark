from typing import Optional
from pathlib import Path

import delta
from pyspark.sql import SparkSession


def config_spark_builder_with_delta(
    builder: SparkSession.Builder,
) -> SparkSession.Builder:
    # https://docs.delta.io/latest/quick-start.html#python
    builder = builder.config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension",
    ).config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    # Add spark.jars.packages with a version that matches the installed
    # delta-spark Python package.
    return delta.configure_spark_with_delta_pip(builder)


def get_local_spark_session(
    data_dir: Optional[str] = None, delta: bool = True
) -> SparkSession:
    builder = (
        SparkSession.builder.master("local[1]")
        .appName("my_spark_project")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.databricks.delta.snapshotPartitions", "1")
        .config(
            "spark.sql.adaptive.coalescePartitions.initialPartitionNum",
            "1",
        )
    )
    if delta:
        builder = config_spark_builder_with_delta(builder)
    if data_dir is not None:
        data_dir = Path(data_dir).resolve().as_posix()
        builder = builder.config("spark.sql.warehouse.dir", data_dir).config(
            "spark.driver.extraJavaOptions",
            f"-Dderby.system.home={data_dir}",
        )
    return builder.enableHiveSupport().getOrCreate()


spark = get_local_spark_session()
df = spark.range(10)
df.show()
df.write.format("delta").mode("overwrite").save("/tmp/range")