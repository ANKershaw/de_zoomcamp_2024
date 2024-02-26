## Week 5 Homework 

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the FHV 2019-10 data found here. [FHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz)

### Question 1: 

**Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

```console
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.0
      /_/

Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 11.0.16.1)
Type in expressions to have them evaluated.
Type :help for more information.

scala> spark.version
res0: String = 3.5.0
```

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)

### Question 2: 

**FHV October 2019**

Read the October 2019 FHV into a Spark Dataframe with a schema as we did in the lessons.

Repartition the Dataframe to 6 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 1MB
- **6MB <-answer**
- 25MB
- 87MB

```commandline
░▒▓    ~/Py/DE_zoomcamp/week5/fhv/2/10    week5_data> ls -larth | grep parquet                   
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00000-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00002-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00001-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00003-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00004-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff    48K Feb 26 15:25 .part-00005-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet.crc
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00004-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00002-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00000-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00003-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00001-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
-rw-r--r--   1 amanda  staff   6.0M Feb 26 15:25 part-00005-72e8e4e9-76c4-4f61-834a-e71d25d3b19f-c000.snappy.parquet
```


### Question 3: 

**Count records** 

How many taxi trips were there on the 15th of October?

Consider only trips that started on the 15th of October.

- 108,164
- 12,856
- 452,470
- 62,610

> [!IMPORTANT]
> Be aware of columns order when defining schema

### Question 4: 

**Longest trip for each day** 

What is the length of the longest trip in the dataset in hours?

- 631,152.50 Hours
- 243.44 Hours
- 7.68 Hours
- 3.32 Hours



### Question 5: 

**User Interface**

Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080



### Question 6: 

**Least frequent pickup location zone**

Load the zone lookup data into a temp view in Spark</br>
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?</br>

- East Chelsea
- Jamaica Bay
- Union Sq
- Crown Heights North


## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw5
- Deadline: See the website