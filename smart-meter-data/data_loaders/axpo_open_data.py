from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

DATASET = 'dataset-b'

def fetch_smartmeter_data_urls():
    base_url = "https://open.data.axpo.com/%24web/"
    url = base_url + f"index.html#{DATASET}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []

    # Find all <a> tags with href containing "ckw_opendata_smartmeter_dataset_a" and ".csv.gz"
    for link in soup.find_all('a', href=re.compile(r'ckw_opendata_smartmeter_dataset_b.*\.csv\.gz')):
        urls.append(urljoin(base_url, link['href']))

    return urls


@data_loader
def load_data_from_axpo(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    smd_urls = fetch_smartmeter_data_urls()

    dfs = []

    for smd_url in smd_urls:
        dfs.append(pd.read_csv(smd_url))

    # Concatenate all data into one DataFrame
    return pd.concat(dfs, ignore_index=True)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
