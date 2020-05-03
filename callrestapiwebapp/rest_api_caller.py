
import logging
import time
import requests

__author__ = 'psessford'

logging.basicConfig(level=logging.INFO)


class RestApiCaller:
    """Helper to make calls to REST API
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def make_api_call(self, url, sleep=1):
        """Make a call to a REST API

        :param url: (str)
        :param sleep: (int) seconds to pause after call
        :return response_dict: (dict)
        """
        self.logger.info(f"making api call to url {url}")
        with requests.Session() as session:
            response = session.get(url=url)

        if not response:
            self.logger.info(
                f"bad response (status_code{response.status_code})")
            return None

        time.sleep(sleep)  # guard against over-loading api
        response_dict = response.json()
        # TODO: also handle non-json responses?
        self.logger.info("returning response dict")
        return response_dict


if __name__ == '__main__':
    import pandas as pd

    url = (
        f"https://data.police.uk/api/crimes-street/all-crime?"
        f"lat=51.5080&lng=-0.1281")  # &date=2019-02

    caller = RestApiCaller()
    response_dict = caller.make_api_call(url=url)
    df = pd.DataFrame(response_dict)

    print(df.shape)
    print(df.iloc[0])
