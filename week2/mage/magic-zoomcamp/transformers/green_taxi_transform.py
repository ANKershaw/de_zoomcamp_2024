if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: rows with trip distance greater than 0: {data['trip_distance'].gt(0).sum()}")
    print(f"Preprocessing: vendorid existing values: {data.VendorID.unique()}")
    
    data = data.rename(columns={'VendorID': 'vendor_id', 'RatecodeID': 'ratecode_id', 'PULocationID': 'pu_location_id', 'DOLocationID': 'do_location_id'})

    
    passenger_mask = data['passenger_count'] > 0
    distance_mask = data['trip_distance'] > 0 

    print(f'{data.columns}')

    return data[distance_mask & passenger_mask]


@test
def test_output(output, *args) -> None:
    """
    vendor_id is one of the existing values in the column (currently)
    passenger_count is greater than 0
    trip_distance is greater than 0    
    """ 
    assert 'vendor_id' in output.columns , "vendor_id is not a column"
    assert (output['passenger_count'] > 0).all() , "passenger_count is not greater than 0"
    assert (output['trip_distance'] > 0).all() , "trip_distance is not greater than 0"
