
## Stream processing with RisingWave

In this hands-on workshop, we’ll learn how to process real-time streaming data using SQL in RisingWave. The system we’ll use is [RisingWave](https://github.com/risingwavelabs/risingwave), an open-source SQL database for processing and managing streaming data. You may not feel unfamiliar with RisingWave’s user experience, as it’s fully wire compatible with PostgreSQL.

![RisingWave](https://raw.githubusercontent.com/risingwavelabs/risingwave-docs/main/docs/images/new_archi_grey.png)

We’ll cover the following topics in this Workshop: 

- Why Stream Processing?
- Stateless computation (Filters, Projections)
- Stateful Computation (Aggregations, Joins)
- Data Ingestion and Delivery

RisingWave in 10 Minutes:
https://tutorials.risingwave.com/docs/intro

[Project Repository](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04)

## Homework

**Please setup the environment in [Getting Started](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04?tab=readme-ov-file#getting-started) and for the [Homework](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04/blob/main/homework.md#setting-up) first.**


## Question 0

_This question is just a warm-up to introduce dynamic filter, please attempt it before viewing its solution._

What are the pick up taxi zones at the latest dropoff times?

For this part, we will use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/).

<details>
<summary>Solution</summary>

```sql
CREATE MATERIALIZED VIEW latest_dropoff_time AS
    WITH t AS (
        SELECT MAX(tpep_dropoff_datetime) AS latest_dropoff_time
        FROM trip_data
    )
    SELECT taxi_zone.Zone as taxi_zone, latest_dropoff_time
    FROM t,
            trip_data
    JOIN taxi_zone
        ON trip_data.DOLocationID = taxi_zone.location_id
    WHERE trip_data.tpep_dropoff_datetime = t.latest_dropoff_time;

--    taxi_zone    | latest_dropoff_time
-- ----------------+---------------------
--  Midtown Center | 2022-01-03 17:24:54
-- (1 row)
```

</details>

### Question 1

Create a materialized view to compute the average, min and max trip time between each taxi zone.

From this MV, find the pair of taxi zones with the highest average trip time.
You may need to use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/) for this.

Bonus (no marks): Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute,
but the max trip time is 10 minutes and 20 minutes respectively.

Options:
1. Yorkville East, Steinway
2. Murray Hill, Midwood
3. East Flatbush/Farragut, East Harlem North
4. Midtown Center, University Heights/Morris Heights

```sql
DROP MATERIALIZED VIEW IF EXISTS question_1;
CREATE MATERIALIZED VIEW question_1 AS
    WITH combined_tables AS(
        SELECT 
            tpep_pickup_datetime, 
            tpep_dropoff_datetime,
            pulocationid,
            dolocationid,
            t_pu.zone AS pickup_zone,
            t_do.zone AS dropoff_zone,
            tpep_dropoff_datetime - tpep_pickup_datetime AS trip_time
        FROM 
            trip_data
        LEFT JOIN 
            taxi_zone AS t_pu
        ON 
            trip_data.PULocationID = t_pu.location_id
        LEFT JOIN
            taxi_zone t_do
        ON  
            trip_data.DOLocationID = t_do.location_id
    )

SELECT 
    pickup_zone,
    dropoff_zone,
    MAX(trip_time) AS max_trip_time,
    AVG(trip_time) AS avg_trip_time,
    MIN(trip_time) AS min_trip_time,
    count(*) AS total_trips
 FROM combined_tables
 WHERE 
    pickup_zone = 'Murray Hill'
    AND 
    dropoff_zone = 'Midwood'
GROUP BY pickup_zone, dropoff_zone

UNION 


 SELECT 
    pickup_zone,
    dropoff_zone,
    MAX(trip_time) AS max_trip_time,
    AVG(trip_time) AS avg_trip_time,
    MIN(trip_time) AS min_trip_time,
    count(*) AS total_trips
 FROM combined_tables
 WHERE 
    pickup_zone = 'Yorkville East'
    AND 
    dropoff_zone = 'Steinway'
GROUP BY pickup_zone, dropoff_zone

UNION

SELECT 
    pickup_zone,
    dropoff_zone,
    MAX(trip_time) AS max_trip_time,
    AVG(trip_time) AS avg_trip_time,
    MIN(trip_time) AS min_trip_time,
    count(*) AS total_trips
 FROM combined_tables
 WHERE 
    pickup_zone = 'East Flatbush/Farragut'
    AND 
    dropoff_zone = 'East Harlem North'
GROUP BY pickup_zone, dropoff_zone

UNION

SELECT 
    pickup_zone,
    dropoff_zone,
    MAX(trip_time) AS max_trip_time,
    AVG(trip_time) AS avg_trip_time,
    MIN(trip_time) AS min_trip_time,
    count(*) AS total_trips
 FROM combined_tables
 WHERE 
    pickup_zone = 'Midtown Center'
    AND 
    dropoff_zone = 'University Heights/Morris Heights'
GROUP BY pickup_zone, dropoff_zone;


select * from question_1;                                                                                                       ;
  pickup_zone   | dropoff_zone | max_trip_time | avg_trip_time | min_trip_time | total_trips 
----------------+--------------+---------------+---------------+---------------+-------------
 Yorkville East | Steinway     | 23:59:33      | 23:59:33      | 23:59:33      |           1

```

### Question 2

Recreate the MV(s) in question 1, to also find the number of trips for the pair of taxi zones with the highest average trip time.

Options:
1. 5
2. 3
3. 10
4. **1 <- answer**

Work is shown in output of Question 1

### Question 3

From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups?
For example if the latest pickup time is 2020-01-01 12:00:00,
then the query should return the top 3 busiest zones from 2020-01-01 11:00:00 to 2020-01-01 12:00:00.

HINT: You can use [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/)
to create a filter condition based on the latest pickup time.

NOTE: For this question `17 hours` was picked to ensure we have enough data to work with.

Options:
1. Clinton East, Upper East Side North, Penn Station
2. **LaGuardia Airport, Lincoln Square East, JFK Airport <-answer**
3. Midtown Center, Upper East Side South, Upper East Side North
4. LaGuardia Airport, Midtown Center, Upper East Side North

```sql
WITH combined_tables AS(
        SELECT 
            tpep_pickup_datetime, 
            pulocationid,
            t_pu.zone AS pickup_zone
        FROM 
            trip_data
        LEFT JOIN 
            taxi_zone AS t_pu
        ON 
            trip_data.PULocationID = t_pu.location_id
    ), latest_time AS(
        SELECT MAX(tpep_pickup_datetime) AS latest_pickup_time
        FROM trip_data
    )
    SELECT 
    	pickup_zone,
    	count(pickup_zone) AS zone_count
    FROM 
    	combined_tables, latest_time
    WHERE 
    	tpep_pickup_datetime >= latest_pickup_time - interval '17' hour 
    GROUP BY 
    	pickup_zone
    ORDER BY zone_count DESC;


     pickup_zone     | zone_count 
---------------------+------------
 LaGuardia Airport   |         19
 JFK Airport         |         17
 Lincoln Square East |         17
(3 rows)
```

## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/workshop2
- Deadline: 11 March (Monday), 23:00 CET 

## Rewards 🥳

Everyone who completes the homework will get a pen and a sticker, and 5 lucky winners will receive a Tshirt and other secret surprises!
We encourage you to share your achievements with this workshop on your socials and look forward to your submissions 😁

- Follow us on **LinkedIn**: https://www.linkedin.com/company/risingwave
- Follow us on **GitHub**: https://github.com/risingwavelabs/risingwave
- Join us on **Slack**: https://risingwave-labs.com/slack

See you around!


## Solution