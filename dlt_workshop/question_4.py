import dlt
import duckdb
from IPython.display import display


dataset_name = 'generators'
table_name = 'dlt_workshop'


def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}


for person in people_1():
    print(person)


def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}


for person in people_2():
    print(person)


# define the connection to load to.
# We now use duckdb, but you can switch to Bigquery later
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name=dataset_name)


# we can load any generator to a table at the pipeline destination as follows:
info = generators_pipeline.run(people_1(), table_name=table_name, write_disposition="replace")

# the outcome metadata is returned by the load and we can inspect it by printing it.
print(info)

# we can load the next generator to the same or to a different table.
info = generators_pipeline.run(people_2(), table_name="dlt_workshop", write_disposition="merge",
                    primary_key="ID")

print(info)

conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
display(conn.sql("show tables"))

age = conn.sql("SELECT sum(Age) FROM dlt_workshop").df()
display(age)
