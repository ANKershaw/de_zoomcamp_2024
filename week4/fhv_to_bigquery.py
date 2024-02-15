import pandas as pd
import pandas_gbq as pd_gbq
from time import time


def fhv_load_from_api(url):
	
	# table_id = 'my_dataset.my_table'
	table_id = "trips_data_all.fhv_tripdata"
	project_id = "de-zoomcamp-412118"
	
	taxi_dtypes = {
		'dispatching_base_num':   str,
		'PUlocationID':           str,
		'DOlocationID':           str,
		'SR_Flag':                pd.Int64Dtype(),
		'Affiliated_base_number': str,
	}
	
	# native date parsing
	parse_dates = ['pickup_datetime', 'dropOff_datetime']
	
	iterator = pd.read_csv(url, compression='gzip', iterator=True, dtype=taxi_dtypes,
	                       parse_dates=parse_dates, chunksize=100000, low_memory=False)
	
	df = next(iterator)
	
	df.columns = df.columns.str.strip().str.lower()
	
	df.rename(columns={
		"pulocationid": "pickup_location_id",
		"dolocationid": "dropoff_location_id"
	}, inplace=True)
	
	pd_gbq.to_gbq(df, table_id, project_id=project_id, if_exists='append')
	
	chunks_processed = 1
	print(f'Chunks processed: {chunks_processed}')
	
	while True:
		try:
			t_start = time()
		
			chunks_processed += 1
			df = next(iterator)
		
			df.columns = df.columns.str.strip().str.lower()
			df.rename(columns={"pulocationid": "pickup_location_id", "dolocationid": "dropoff_location_id"}, inplace=True)
			
			pd_gbq.to_gbq(df, table_id, project_id=project_id, if_exists='append')
			
			t_end = time()
			print(f'Chunks processed: {chunks_processed} in {t_end - t_start:.3f} seconds')
		
		except StopIteration:
			print(f'Done with the file. Moving on...')
			break


def main():
	m_start = time()
	urls = [
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
	
	for url in urls:
		print(f'processing {url}')
		fhv_load_from_api(url)
	
	m_end = time()
	
	print(f'Finished processing in {m_end - m_start:.3f} seconds')

if __name__ == "__main__":
	main()
