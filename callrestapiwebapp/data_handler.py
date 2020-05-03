
import logging
import numpy as np
import pandas as pd

__author__ = 'psessford'

logging.basicConfig(level=logging.INFO)


class DataHandler:
    """Helper to handle data response form a REST API call
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse_response_dict(self, response_dict):
        """Parse a response dict from an api call into a data frame

        :param response_dict: (dict)
        :return response_df: (pd.DataFrame)
        """
        self.logger.info("parsing response dict into a data frame")
        response_df = pd.DataFrame(response_dict)
        # TODO: try-except different orients, using from_dict()

        response_df = self._filter_out_problematic_columns(
            response_df=response_df)
        self.logger.info(
            f"returning data frame of {response_df.shape[0]} rows and "
            f"{response_df.shape[1]} columns")
        return response_df

    def _filter_out_problematic_columns(self, response_df):
        n_cols = response_df.shape[1]
        sample_row_dict = response_df.iloc[0].to_dict()
        acceptable_cols = [
            k for k, v in sample_row_dict.items()
            if isinstance(v, (str, int, float, np.int64, np.float64))]
        response_df = response_df[acceptable_cols]

        self.logger.info(f"filtered out {response_df.shape[1] - n_cols} "
                         f"problematic columns")
        return response_df
