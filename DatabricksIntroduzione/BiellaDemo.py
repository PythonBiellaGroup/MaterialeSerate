# Databricks notebook source
# MAGIC %md
# MAGIC ## Toy datasets
# MAGIC We can gain experience by playing with toy datasets

# COMMAND ----------

dbutils.fs.ls('/databricks-datasets')

# COMMAND ----------

# MAGIC %md
# MAGIC The **DBFS** is a file system managed behind the hood by Databricks

# COMMAND ----------

# MAGIC %md
# MAGIC ## IoT Dataset
# MAGIC 
# MAGIC `/databricks-datasets/iot/iot_devices.json` is a list of IoT Devices with IP addresses. In addition to the IP address, the file contains the geographic information for each device entry:
# MAGIC 
# MAGIC - ISO-3166-1 two and three letter codes
# MAGIC - Country Name
# MAGIC - Latitude and longitude

# COMMAND ----------

dbutils.fs.head("/databricks-datasets/iot/iot_devices.json")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Interfaces
# MAGIC 
# MAGIC There are three key Spark interfaces that you should know about. [Ref](https://databricks.com/spark/getting-started-with-apache-spark/quick-start#spark-interfaces)
# MAGIC - RDD (*original data structure for Apache Spark*)
# MAGIC - 💗 DataFrame (*most common today*)
# MAGIC - Datasets (*Java and Scala only*)

# COMMAND ----------

# MAGIC %md
# MAGIC ## DataFrames
# MAGIC These are similar in concept to the DataFrame you may be familiar with in the pandas Python library and the R language. 

# COMMAND ----------

df = spark.read.json("/databricks-datasets/iot/iot_devices.json")
type(df)

# COMMAND ----------

df

# COMMAND ----------

# MAGIC %md
# MAGIC Lazy evaluation: `df` is a definition but **no data** has been loaded yet.
# MAGIC 
# MAGIC [Ref](https://stackoverflow.com/a/38028390/2314987) For transformations, Spark adds them to a DAG of computation and only when driver requests some data, does this DAG actually gets executed. One advantage of this is that Spark can make many **optimization** decisions after it had a chance to look at the DAG in entirety. This would not be possible if it executed everything as soon as it got it.

# COMMAND ----------

display(df)

# COMMAND ----------

# Data can be visualized
display(df)

# COMMAND ----------

df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC Filtering and selecting data

# COMMAND ----------

display(
  df.where(
    (df.temp > 30) & (df.humidity > 70)
  )
)

# COMMAND ----------

# MAGIC %md
# MAGIC We can add new transformations by pipelining commands on the dataframe

# COMMAND ----------

display(
  df.where(
    (df.temp > 30) & (df.humidity > 70)
  ).select('device_id', 'cn', 'humidity', 'temp')
)

# COMMAND ----------

# MAGIC %md
# MAGIC Group by and aggregate

# COMMAND ----------

display(
  df.where(
    (df.temp > 30) & (df.humidity > 70)
  ).select('device_id', 'cn', 'humidity', 'temp')\
  .groupby('cn').avg('humidity', 'temp')
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run SQL queries
# MAGIC Before you can issue SQL queries, you must save your data DataFrame as a temporary table.

# COMMAND ----------

df.createOrReplaceTempView("iot_devices")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM iot_devices LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   cca3 as country,
# MAGIC   count(*) as devices
# MAGIC FROM iot_devices
# MAGIC GROUP BY cca3

# COMMAND ----------

# MAGIC %md
# MAGIC Can I run queries over Spark SQL tables from outside?
# MAGIC Yes, via [distributed SQL engine](https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#distributed-sql-engine). Spark SQL can also act as a distributed query engine using its JDBC/ODBC or command-line interface. In this mode, end-users or applications can interact with Spark SQL directly to run SQL queries, without the need to write any code.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Saving to CSV
# MAGIC 
# MAGIC What if we want to store the result to a csv file?

# COMMAND ----------

df.where(
  (df.temp > 30) & (df.humidity > 70)
).select('device_id', 'cn', 'humidity', 'temp')\
.groupby('cn').avg('humidity', 'temp')\
.write.mode('overwrite').csv('/tmp/test_aggregated_iot.csv')

# COMMAND ----------

dbutils.fs.ls('/tmp/')

# COMMAND ----------

# MAGIC %md
# MAGIC Do you notice the trailing `/`? `test_aggregated_iot.csv` is actually a folder.

# COMMAND ----------

display(dbutils.fs.ls('/tmp/test_aggregated_iot.csv/'))

# COMMAND ----------

# MAGIC %md
# MAGIC Partitioning the data

# COMMAND ----------

df.select('device_id', 'cn', 'humidity', 'temp')\
  .write\
  .option("header", True)\
  .partitionBy('cn')\
  .mode('overwrite')\
  .csv('/tmp/test_aggregated_iot_partitioned.csv')

# COMMAND ----------

display(dbutils.fs.ls('/tmp/test_aggregated_iot_partitioned.csv/'))

# COMMAND ----------

display(dbutils.fs.ls('/tmp/test_aggregated_iot_partitioned.csv/cn=Italy/'))

# COMMAND ----------

# MAGIC %md
# MAGIC How to read it again?
# MAGIC 
# MAGIC We can exploit the [partition discovery](https://spark.apache.org/docs/2.2.0/sql-programming-guide.html#partition-discovery) feature. Spark SQL will automatically extract the partitioning information from the paths

# COMMAND ----------

df_2 = spark\
          .read\
          .option("header", True)\
          .csv("/tmp/test_aggregated_iot_partitioned.csv") # WTF, that's  a folder!
display(df_2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reading from...
# MAGIC 
# MAGIC Spark SQL supports reading data from a variety of formats including
# MAGIC 
# MAGIC - Parquet (default)
# MAGIC - JSON
# MAGIC - Hive tables
# MAGIC - JDBC
# MAGIC - Avro
# MAGIC - csv
# MAGIC - text
# MAGIC 
# MAGIC ## Parquet files
# MAGIC 
# MAGIC [Ref](https://databricks.com/glossary/what-is-parquet) Designed for efficient as well as performant flat **columnar** storage format of data compared to row based files like CSV or TSV files. Parquet is optimized to work with complex data in bulk and features different ways for efficient data **compression** and encoding types.
# MAGIC 
# MAGIC When querying, columnar storage you can **skip** over the non-relevant data very quickly. As a result, aggregation queries are less time consuming compared to row-oriented databases. Parquet can only read the needed columns therefore greatly minimizing the IO.

# COMMAND ----------

df.select('device_id', 'cn', 'humidity', 'temp')\
  .write\
  .mode('overwrite')\
  .save('/tmp/test_aggregated_iot.parquet')

# COMMAND ----------

# MAGIC %fs ls /tmp/test_aggregated_iot.parquet/

# COMMAND ----------

# MAGIC %fs head /tmp/test_aggregated_iot.parquet/part-00000-d75d9dac-0f90-417a-aec8-529b4a6f4bf8-c000.snappy.parquet

# COMMAND ----------

display(
  spark.read.load('/tmp/test_aggregated_iot.parquet')
)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Scheduling a Job
# MAGIC 
# MAGIC We'll now look at how to create a job
