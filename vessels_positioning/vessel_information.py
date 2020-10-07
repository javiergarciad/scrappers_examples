import logging
from pathlib import Path
from urllib.parse import urlparse, ParseResult

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def get_project_root():
    """Returns project root folder."""
    return Path(__file__).parent


def get_input(filepath):
    """
    Open and read input CSV
    :param filepath:
    :return: DataFrame
    """
    try:
        logger.info("Opening input file: {}".format(filepath))
        return pd.read_csv(filepath, dtype=str)
    except Exception as e:
        logger.error("Unable to read input file.")
        logger.error(e)
        raise SystemExit


def build_url(name=None, mmsi=None, imo=None):
    """
    Build URL for querying the https://www.myshiptracking.com website about a
    specific vessel
    :param name: vessel name
    :param mmsi: vessel mmsi
    :param imo: vessel imo
    :return: URL string
    """

    if name is None or mmsi is None or imo is None:
        logger.error("Must provide complete information for {}-{}-{}".format(name, mmsi, imo))
        return False

    scheme = 'https'
    netloc = 'www.myshiptracking.com'
    name = name.replace(" ", "-").lower()
    path = '/vessels/' + name + "-mmsi-" + str(mmsi) + "-imo-" + str(imo)

    url = ParseResult(scheme=scheme, netloc=netloc, path=path, params='', query='', fragment='').geturl()

    return url


def get_response(name, mmsi, imo):
    """

    :param name:
    :param mmsi:
    :param imo:
    :return:
    """
    url = build_url(name, mmsi, imo)
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logger.error("Request exception for '{}'".format(url))
        logger.error(e)
        return None

    if response.status_code != 200:
        logger.error("Unable to acquire information for {}  with status {}".format(name, response.status_code))
        return None

    return response


def parse_response(response):
    """
    Convert a valid response form the https://www.myshiptracking.com/vessels/ website
    into a dictionary containing the information parsed from the 'vessels_table2'

    :param response:
    :return: dict
    """
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", {"class": "vessels_table2"})

    data = []
    for table in tables:
        rows = table.findAll(lambda tag: tag.name == "tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

    ans = {x[0]: x[1] for x in data if len(x) == 2}

    return ans


def create_output(data, filepath):
    """
    export data to csv
    :param data: list of dict
    :param filepath: location of output file
    :return:
    """
    df = pd.DataFrame.from_records(data=data)
    df.to_csv(path_or_buf=filepath)


def main(input_filename, output_filename):
    input_filepath = Path(get_project_root(), input_filename)
    input_df = get_input(input_filepath)

    output_filepath = Path(get_project_root(), output_filename)

    data = []
    for _i, row in input_df.iterrows():
        name = row["NAME"]
        mmsi = row["MMSI"]
        imo = row["IMO"]
        x = {"Name": name, "MMSI": mmsi, "IMO": imo}

        response = get_response(name, mmsi, imo)

        if response is not None:
            y = parse_response(response)
            z = {**x, **y}
            data.append(z)

    return create_output(data=data, filepath=output_filepath)


if __name__ == "__main__":
    main(input_filename="input.csv", output_filename="output.csv")
