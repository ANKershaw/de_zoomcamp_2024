## Notes For Loading Data

## 1. Data Required

In this homework, we'll use the models developed during the week 4 videos and enhance the already presented dbt project using the already loaded Taxi data for fhv vehicles for year 2019 in our DWH.

This means that in this homework we use the following data [Datasets list](https://github.com/DataTalksClub/nyc-tlc-data/)
* Yellow taxi data - Years 2019 and 2020
* Green taxi data - Years 2019 and 2020 
* fhv data - Year 2019. 


Backup for NYC TLC data for the DE Zoomcamp course

CSV data:

Yellow taxi data: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow
Green taxi data: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green
For-hire vehicles (FHV): https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv
For-hire vehicles high volume (FHVHV): https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhvhv
Misc (zone lookup file): https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/misc


https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow

```python
yellow_taxi_data_2019_2020 = [
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-02.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-03.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-04.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-05.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-06.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-07.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-08.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-09.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-10.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-11.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-12.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-02.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-03.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-04.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-05.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-06.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-07.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-08.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-09.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-10.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-11.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz',
]


green_taxi_data_2019_2020 = [
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-02.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-03.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-04.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-05.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-06.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-07.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-08.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-11.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-12.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-02.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-03.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-04.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-05.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-06.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-07.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-08.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-09.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz',
]

fhv_data_2019 = [
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-02.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-03.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-04.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-05.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-06.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-07.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-08.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-09.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-11.csv.gz',
    'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-12.csv.gz',
]
```
