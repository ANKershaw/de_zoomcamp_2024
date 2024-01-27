## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`  <span style="color:green">**<- answer**</span>


```commandline
░▒▓    ~ ▓▒░ docker run --help                        ░▒▓ ✔  13:54:07  ▓▒░

Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Create and run a new container from an image

Aliases:
  docker container run, docker run

Options:
      --add-host list                  Add a custom host-to-IP mapping
                                       (host:ip)
      --annotation map                 Add an annotation to the container
                                       (passed through to the OCI
                                       runtime) (default map[])
.
.
.

  -q, --quiet                          Suppress the pull output
      --read-only                      Mount the container's root
                                       filesystem as read only
      --restart string                 Restart policy to apply when a
                                       container exits (default "no")
      --rm                             Automatically remove the container
                                       when it exits
```

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- <span style="color:green">**0.42.0**</span>
- 1.0.0
- 23.0.1 
- 58.1.0

```commandline
░▒▓    ~ ▓▒░ docker run -it --entrypoint="bash" python:3.9
root@675e6b5e8a57:/# pip list
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0
```

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- <span style="color:green">**15612**</span>
- 15859
- 89009


```
SELECT 
	count(*)
FROM yellow_taxi_data y
WHERE 
	y.lpep_pickup_datetime::date = '2019-09-18'
	AND
	y.lpep_dropoff_datetime::date = '2019-09-18'
```

```
"count"
15612
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- <span style="color:green">**2019-09-26** </span>
- 2019-09-21

```commandline
SELECT
	y.lpep_pickup_datetime::date AS pickup_date,
	max(y.trip_distance) AS longest_trip
FROM yellow_taxi_data y 
WHERE 
	lpep_pickup_datetime::date IN ('2019-09-18', '2019-09-16', '2019-09-26', '2019-09-21')
GROUP BY pickup_date
ORDER BY longest_trip DESC
```

| pickup_date                                   | longest_trip                              |
|-----------------------------------------------|-------------------------------------------|
| <span style="color:green"> 2019-09-26 </span> | <span style="color:green"> 341.64 </span> |
| 2019-09-21                                    | 135.53                                    |
| 2019-09-16                                    | 114.3                                     |
| 2019-09-18                                    | 70.28                                     |                           |


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- <span style="color:green">**"Brooklyn" "Manhattan" "Queens"** </span>
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

```commandline
SELECT 
	z.borough AS borough,
	sum(total_amount) AS total_amount
FROM yellow_taxi_data y
LEFT JOIN taxi_zone z ON y."PULocationID" = z.locationid
WHERE y.lpep_pickup_datetime::date = '2019-09-18'
GROUP BY borough
ORDER BY total_amount DESC
```

| borough                                     | total_amount                                       |
|---------------------------------------------|----------------------------------------------------|
| <span style="color:green">Brooklyn </span>  | <span style="color:green">96333.24000000475</span> |
| <span style="color:green">Manhattan </span> | <span style="color:green">92271.300000005</span>   |
| <span style="color:green">Queens </span>    | <span style="color:green">78671.71000000216</span> |
| Bronx                                       | 32830.08999999965                                  |
| Unknown                                     | 728.75                                             |
| Staten Island                               | 342.59                                             |



## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- <span style="color:green">**Long Island City/Queens Plaza**</span>

```
SELECT 
	z2.zone AS dropoff_zone,
	sum(y.tip_amount) AS total_dropoffs
FROM yellow_taxi_data y 
	LEFT JOIN taxi_zone z1 ON y."PULocationID" = z1.locationid 
	LEFT JOIN taxi_zone z2 ON y."DOLocationID" = z2.locationid
WHERE y.lpep_pickup_datetime BETWEEN '2019-09-01 00:00:00' AND '2019-09-30 23:59:59'
	AND z1.zone = 'Astoria'
	AND z2.zone IN ('Central Park', 'Jamaica', 'JFK Airport', 'Long Island City/Queens Plaza')
GROUP BY dropoff_zone
ORDER BY total_dropoffs DESC
```

| dropoff_zone                                                       | total_dropoffs                              |
|--------------------------------------------------------------------|---------------------------------------------|
| <span style="color:green">**Long Island City/Queens Plaza**</span> | <span style="color:green">**709.03**</span> |
| JFK Airport                                                        | 277.26                                      |
| Central Park                                                       | 57.92                                       |
| Jamaica                                                            | 26.380000000000003                          |



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

```terraform
 terraform apply -var="project=de-zoomcamp-412118"

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "de-zoomcamp-412118"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "dtc_data_lake_de-zoomcamp-412118"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 1s [id=projects/de-zoomcamp-412118/datasets/demo_dataset]
google_storage_bucket.demo-bucket: Creation complete after 1s [id=dtc_data_lake_de-zoomcamp-412118]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

```