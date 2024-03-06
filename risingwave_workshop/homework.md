## Question 0

_This question is just a warm-up to introduce dynamic filter, please attempt it before viewing its solution._

What are the dropoff taxi zones at the latest dropoff times?

For this part, we will use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/).

```
trip_data rows:
vendorid 
tpep_pickup_datetime 
tpep_dropoff_datetime 
passenger_count 
trip_distance 
ratecodeid 
store_and_fwd_flag 
pulocationid 
dolocationid 
payment_type 
fare_amount 
extra 
mta_tax 
tip_amount 
tolls_amount 
improvement_surcharge 
total_amount 
congestion_surcharge 
airport_fee 
```
```
taxi_zone columns:
location_id 
borough 
zone 
service_zone 
```

example from dynamic filters page:
```sql
WITH max_profit AS (SELECT max(profit_margin) max FROM sales) 
SELECT product_name FROM products, max_profit 
WHERE product_profit > max;
```

CREATE MATERIALIZED VIEW mv1 AS 
    WITH cte AS(
        SELECT 
            max(tpep_dropoff_datetime) AS latest_timestamp 
        FROM trip_data
    ) 
    SELECT 
        taxi_zone.zone as taxi_zone, 
        cte.latest_timestamp
    FROM 
        cte,
        trip_data
    JOIN 
        taxi_zone
    ON 
        trip_data.DOLocationID = taxi_zone.location_id
    WHERE 
        trip_data.tpep_dropoff_datetime = cte.latest_timestamp;







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

--    taxi_zone    
--    latest_dropoff_time
-- ----------------+---------------------
--  Midtown Center 
--  2022-01-03 17:24:54
-- (1 row)
```

</details>

### Question 1

Create a materialized view to compute the average, min and max trip time between each taxi zone.

From this MV, find the pair of taxi zones with the highest average trip time.
You may need to use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/) for this.

Options:
1. **Yorkville East, Steinway <-answer**
2. Murray Hill, Midwood
3. East Flatbush/Farragut, East Harlem North
4. Midtown Center, University Heights/Morris Heights

### Question 2

Recreate the MV(s) in question 1, to also find the number of trips for the pair of taxi zones with the highest average trip time.

Options:
1. 5
2. 3
3. 10
4. **1 <- answer**

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