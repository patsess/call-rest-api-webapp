
import logging
import time
import requests

__author__ = 'psessford'


class RestApiCaller:
    """Helper to make calls to REST API
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def make_api_call(self, url, sleep=1):
        """Make a call to a REST API

        :param url: (str)
        :param sleep: (int) seconds to pause after call
        :return response_json: (dict, or list of dict) json representation
        """
        self.logger.info(f"making api call to url {url}")
        with requests.Session() as session:
            response = session.get(url=url)

        if not response:
            self.logger.info(
                f"bad response (status_code{response.status_code})")
            return None

        time.sleep(sleep)  # guard against over-loading api
        response_json = response.json()
        # TODO: also handle non-json responses?
        self.logger.info("returning response json representation")
        return response_json


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import pandas as pd
    import flatten_json

    url = (
        f"https://data.police.uk/api/crimes-street/all-crime?"
        f"lat=51.5080&lng=-0.1281")  # &date=2019-02

    caller = RestApiCaller()
    response_json = caller.make_api_call(url=url)
    # df = pd.json_normalize(response_json)
    response_json = (flatten_json.flatten(d) for d in response_json)
    df = pd.DataFrame(response_json)

    print(df.shape)
    print(df.iloc[0])
