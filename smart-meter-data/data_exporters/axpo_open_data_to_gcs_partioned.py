import os
import pyarrow as pa
import pyarrow.parquet as pq
from pandas import DataFrame
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/smart-meter-data-portfolio-2319e28e4a79.json"

bucket_name = 'smart-meter-bucket-1'
project_id = 'smart-meter-data-portfolio'
table_name = 'smart-meter-data-agg-part'

root_path = f"{bucket_name}/{table_name}"


@data_exporter
def export_data(df: DataFrame, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month-year'] = (df["timestamp"].dt.month_name() + "-" + df["timestamp"].dt.year.astype(str))

    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path = root_path,
        partition_cols=['month-year'],
        filesystem=gcs
    )

    # Specify your data exporting logic here


