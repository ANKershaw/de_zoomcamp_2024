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
- **62,610 <- answer**

```python
#How many taxi trips were there on the 15th of October?
# Consider only trips that started on the 15th of October.

spark.sql("""
SELECT 
    count(1)
FROM 
    trips_data
WHERE
    to_date(pickup_datetime) = "2019-10-15"
""").show()

+--------+
|count(1)|
+--------+
|   62610|
+--------+
```

### Question 4: 

**Longest trip for each day** 

What is the length of the longest trip in the dataset in hours?

- **631,152.50 Hours <-answer** 
- 243.44 Hours
- 7.68 Hours
- 3.32 Hours

```python
# this will give a difference in seconds between pickup and dropoff
# divide by 3600 to get hours 

spark.sql("""
SELECT 
    max(
        unix_timestamp(dropOff_datetime) - unix_timestamp(pickup_datetime)
    ) / 3600
FROM 
    trips_data
WHERE
""").show()

+----------------------------------------------------------------------------------------------------------------------------+
|(max((unix_timestamp(dropOff_datetime, yyyy-MM-dd HH:mm:ss) - unix_timestamp(pickup_datetime, yyyy-MM-dd HH:mm:ss))) / 3600)|
+----------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                    631152.5|
+----------------------------------------------------------------------------------------------------------------------------+

```

### Question 5: 

**User Interface**

Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- **4040 <- answer**
- 8080

`http://localhost:4040/jobs/`

### Question 6: 

**Least frequent pickup location zone**

Load the zone lookup data into a temp view in Spark</br>
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?</br>

- East Chelsea
- **Jamaica Bay <-answer**
- Union Sq
- Crown Heights North

```python
# Using the zone lookup data and the FHV October 2019 data, 
# what is the name of the LEAST frequent pickup location Zone?

# column from trips_data : PUlocationID
# column from zone_lookup : LocationID
spark.sql("""
SELECT 
    count(1),
    zone_lookup.Zone 
FROM 
    trips_data
LEFT JOIN 
    zone_lookup
ON
    trips_data.PUlocationID = zone_lookup.LocationID 
GROUP BY 
    zone_lookup.Zone
ORDER BY 
    count(1) ASC
""").show()

+--------+--------------------+
|count(1)|                Zone|
+--------+--------------------+
|       1|         Jamaica Bay|
|       2|Governor's Island...|
|       5| Green-Wood Cemetery|
|       8|       Broad Channel|
|      14|     Highbridge Park|
|      15|        Battery Park|
|      23|Saint Michaels Ce...|
|      25|Breezy Point/Fort...|
|      26|Marine Park/Floyd...|
|      29|        Astoria Park|
|      39|    Inwood Hill Park|
|      47|       Willets Point|
|      53|Forest Park/Highl...|
|      57|  Brooklyn Navy Yard|
|      62|        Crotona Park|
|      77|        Country Club|
|      89|     Freshkills Park|
|      98|       Prospect Park|
|     105|     Columbia Street|
|     110|  South Williamsburg|
+--------+--------------------+
```

## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw5
