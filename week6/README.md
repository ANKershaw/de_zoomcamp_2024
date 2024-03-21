
## Question 1: Redpanda version

Now let's find out the version of redpandas. 

For that, check the output of the command `rpk help` _inside the container_. The name of the container is `redpanda-1`.

Find out what you need to execute based on the `help` output.

What's the version, based on the output of the command you executed? (copy the entire version)

```commandline
redpanda@20d58e633e13:/$ rpk version
v22.3.5 (rev 28b2443)
```

## Question 2. Creating a topic

Before we can send data to the redpanda server, we
need to create a topic. We do it also with the `rpk`
command we used previously for figuring out the version of 
redpandas.

Read the output of `help` and based on it, create a topic with name `test-topic` 

What's the output of the command for creating a topic?

```commandline
redpanda@20d58e633e13:/$ rpk topic create test-topic
TOPIC       STATUS
test-topic  OK
```

## Question 3. Connecting to the Kafka server

We need to make sure we can connect to the server, so
later we can send some data to its topics

First, let's install the kafka connector (up to you if you
want to have a separate virtual environment for that)

```bash
pip install kafka-python
```

You can start a jupyter notebook in your solution folder or
create a script

Let's try to connect to our server:

```python
import json
import time 

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()
```

Provided that you can connect to the server, what's the output
of the last command?

```commandline
[1]: True
```

## Question 4. Sending data to the stream

Now we're ready to send some test data:

```python
t0 = time.time()

topic_name = 'test-topic'

for i in range(10):
    message = {'number': i}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
```

How much time did it take? Where did it spend most of the time?

* **Sending the messages <- answer**
* Flushing
* Both took approximately the same amount of time

(Don't remove `time.sleep` when answering this question)


## Reading data with `rpk`

You can see the messages that you send to the topic
with `rpk`:

```bash
rpk topic consume test-topic
```

Run the command above and send the messages one more time to 
see them


## Sending the taxi data

Now let's send our actual data:

* Read the green csv.gz file
* We will only need these columns:
  * `'lpep_pickup_datetime',`
  * `'lpep_dropoff_datetime',`
  * `'PULocationID',`
  * `'DOLocationID',`
  * `'passenger_count',`
  * `'trip_distance',`
  * `'tip_amount'`

Iterate over the records in the dataframe

```python
for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    print(row_dict)
    break

    # TODO implement sending the data here
```

Note: this way of iterating over the records is more efficient compared
to `iterrows`


## Question 5: Sending the Trip Data

* Create a topic `green-trips` and send the data there
* How much time in seconds did it take? (You can round it to a whole number)
* Make sure you don't include sleeps in your code

output
```commandline
took 19.880646228790283 seconds overall
```



## Creating the PySpark consumer

Now let's read the data with PySpark. 

Spark needs a library (jar) to be able to connect to Kafka, 
so we need to tell PySpark that it needs to use it:

```python
import pyspark
from pyspark.sql import SparkSession

pyspark_version = pyspark.__version__
kafka_jar_package = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark_version}"

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("GreenTripsConsumer") \
    .config("spark.jars.packages", kafka_jar_package) \
    .getOrCreate()
```

Now we can connect to the stream:

```python
green_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "green-trips") \
    .option("startingOffsets", "earliest") \
    .load()
```

In order to test that we can consume from the stream, 
let's see what will be the first record there. 

In Spark streaming, the stream is represented as a sequence of 
small batches, each batch being a small RDD (or a small dataframe).

So we can execute a function over each mini-batch.
Let's run `take(1)` there to see what do we have in the stream:

```python
def peek(mini_batch, batch_id):
    first_row = mini_batch.take(1)

    if first_row:
        print(first_row[0])

query = green_stream.writeStream.foreachBatch(peek).start()
```

You should see a record like this:

```
Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": 112, "DOLocationID": 196, "passenger_count": 1.0, "trip_distance": 5.88, "tip_amount": 0.0}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 3, 12, 22, 42, 9, 411000), timestampType=0)
```

my record:
```commandline
Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": 112, "DOLocationID": 196, "passenger_count": 1.0, "trip_distance": 5.88, "tip_amount": 0.0}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 3, 18, 18, 31, 22, 990000), timestampType=0)
```

Now let's stop the query, so it doesn't keep consuming messages
from the stream

```python
query.stop()
```

## Question 6. Parsing the data

The data is JSON, but currently it's in binary format. We need
to parse it and turn it into a streaming dataframe with proper
columns

Similarly to PySpark, we define the schema

```python
from pyspark.sql import types

schema = types.StructType() \
    .add("lpep_pickup_datetime", types.StringType()) \
    .add("lpep_dropoff_datetime", types.StringType()) \
    .add("PULocationID", types.IntegerType()) \
    .add("DOLocationID", types.IntegerType()) \
    .add("passenger_count", types.DoubleType()) \
    .add("trip_distance", types.DoubleType()) \
    .add("tip_amount", types.DoubleType())
```

And apply this schema:

```python
from pyspark.sql import functions as F

green_stream = green_stream \
  .select(F.from_json(F.col("value").cast('STRING'), schema).alias("data")) \
  .select("data.*")
```

How does the record look after parsing? Copy the output 

output:
```commandline
Row(lpep_pickup_datetime='2019-10-01 00:26:02', lpep_dropoff_datetime='2019-10-01 00:39:58', PULocationID=112, DOLocationID=196, passenger_count=1.0, trip_distance=5.88, tip_amount=0.0)
```

### Question 7: Most popular destination

Now let's finally do some streaming analytics. We will
see what's the most popular destination currently 
based on our stream of data (which ideally we should 
have sent with delays like we did in workshop 2)


This is how you can do it:

* Add a column "timestamp" using the `current_timestamp` function
* Group by:
  * 5 minutes window based on the timestamp column (`F.window(col("timestamp"), "5 minutes")`)
  * `"DOLocationID"`
* Order by count

You can print the output to the console using this 
code

```python
query = popular_destinations \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
```

Write the most popular destination. (You will need to re-send the data for this to work)

Answer: 74

```commandline
-------------------------------------------
Batch: 0
-------------------------------------------
+------------+------------------------------------------+-----+
|DOLocationID|window                                    |count|
+------------+------------------------------------------+-----+
|74          |{2024-03-20 15:55:00, 2024-03-20 16:00:00}|2462 |
|74          |{2024-03-20 16:05:00, 2024-03-20 16:10:00}|2420 |
|74          |{2024-03-20 16:20:00, 2024-03-20 16:25:00}|2393 |
|74          |{2024-03-20 16:25:00, 2024-03-20 16:30:00}|2253 |
|74          |{2024-03-20 16:10:00, 2024-03-20 16:15:00}|2211 |
|74          |{2024-03-20 16:15:00, 2024-03-20 16:20:00}|2203 |
|74          |{2024-03-20 16:00:00, 2024-03-20 16:05:00}|2072 |
|42          |{2024-03-20 16:05:00, 2024-03-20 16:10:00}|2051 |
|42          |{2024-03-20 16:00:00, 2024-03-20 16:05:00}|2050 |
|42          |{2024-03-20 16:25:00, 2024-03-20 16:30:00}|2046 |
|42          |{2024-03-20 15:55:00, 2024-03-20 16:00:00}|2020 |
|42          |{2024-03-20 16:15:00, 2024-03-20 16:20:00}|2018 |
|42          |{2024-03-20 16:20:00, 2024-03-20 16:25:00}|1996 |
|41          |{2024-03-20 16:25:00, 2024-03-20 16:30:00}|1951 |
|42          |{2024-03-20 16:10:00, 2024-03-20 16:15:00}|1883 |
|41          |{2024-03-20 16:05:00, 2024-03-20 16:10:00}|1863 |
|41          |{2024-03-20 15:55:00, 2024-03-20 16:00:00}|1854 |
|41          |{2024-03-20 16:00:00, 2024-03-20 16:05:00}|1844 |
|41          |{2024-03-20 16:15:00, 2024-03-20 16:20:00}|1813 |
|75          |{2024-03-20 16:10:00, 2024-03-20 16:15:00}|1784 |
+------------+------------------------------------------+-----+
only showing top 20 rows
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw6


## Solution

We will publish the solution here after deadline.


