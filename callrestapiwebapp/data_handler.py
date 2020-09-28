
import logging
import numpy as np
import pandas as pd
import flatten_json

__author__ = 'psessford'

# TODO: unit test for various different json structures


class DataHandler:
    """Helper to handle data response form a REST API call
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @property
    def flatten_json_separator(self):
        """
        return: (str) separator to be used when flattening a json, e.g. '.'
        """
        return '.'

    def parse_response_json(self, response_json, verbose=True):
        """Parse a response json representation from an api call into a data
        frame

        :param response_json: (dict, or list of dict)
        :param verbose: (bool) whether to log progress
        :return response_df: (pd.DataFrame)
        """
        self.logger.info("starting to parse response json into a data frame")

        is_json_list_of_dicts = self._get_is_json_list_of_dicts(
            json_=response_json)
        
        if is_json_list_of_dicts:
            response_df = self._parse_list_of_dicts_json(json_=response_json)
        elif isinstance(response_json, dict):
            response_df = self._parse_dict_json(json_=response_json)
        else:
            raise TypeError(f"unsupported json type {type(response_json)}")

        # response_df = self._filter_out_problematic_columns(
        #     response_df=response_df)

        self.logger.info(
            f"returning data frame of {response_df.shape[0]} rows and "
            f"{response_df.shape[1]} columns")
        return response_df

    def _get_is_json_list_of_dicts(self, json_):
        is_json_list_of_dicts = (
            isinstance(json_, list) and 
            all((isinstance(d, dict) for d in json_)))
        if is_json_list_of_dicts:
            self.logger.info("json found that is list of dicts")
        
        return is_json_list_of_dicts

    def _parse_list_of_dicts_json(self, json_, method='pandas'):
        if method == 'pandas':
            self.logger.info("normalising list-of-dicts json into data frame")
            df = pd.json_normalize(json_)
            # TODO: give options of different orients, using from_dict()?

        elif method == 'flatten_json':
            self.logger.info("flattening list-of-dicts json")
            json_ = (
                flatten_json.flatten(d, separator=self.flatten_json_separator)
                for d in json_)

            self.logger.info("converting flattened json into data frame")
            df = pd.DataFrame(json_)

        else:
            raise ValueError(f"unrecognised method {method}")
            
        return df

    def _parse_dict_json(self, json_):
        self.logger.info("parsing dict json")

        json_ = {k: self._parse_data_from_dict_json(name=k, data=d) 
                 for k, d in json_.items()}

        if not any((isinstance(d, pd.DataFrame) for d in json_.values())):
            if any((isinstance(d, list) for d in json_.values())):
                return pd.DataFrame(json_)
            else:
                return pd.DataFrame(json_, index=[0])

        df = pd.concat([
            d for d in json_.values() if isinstance(d, pd.DataFrame)
        ], axis=1, ignore_index=False)
        
        json_ = {
            k: d for k, d in json_.items() if not isinstance(d, pd.DataFrame)}
        for k, d in json_.items():
            df[k] = np.repeat(d, repeats=df.shape[0])  # allow d to be a list

        return df

    def _parse_data_from_dict_json(self, name, data):
        if isinstance(data, list):
            if all((isinstance(dd_, dict) for dd_ in data)):
                df = self._parse_list_of_dicts_json(json_=data)
                df.rename(columns={
                    c: f"{name}{self.flatten_json_separator}{c}" 
                    for c in df.columns.values}, inplace=True)
                return df
            else:
                return data  # accept without parsing
        
        elif isinstance(data, dict):
            data = {f"{name}{self.flatten_json_separator}{k}": d 
                    for k, d in data.items()}
            return self._parse_dict_json(json_=data)
        
        else:
            return data  # accept without parsing

    # def _filter_out_problematic_columns(self, response_df):
    #     n_cols = response_df.shape[1]
    #     sample_row_dict = response_df.iloc[0].to_dict()
    #     acceptable_cols = [
    #         k for k, v in sample_row_dict.items()
    #         if isinstance(v, (str, int, float, np.int64, np.float64))]
    #     response_df = response_df[acceptable_cols]

    #     self.logger.info(f"filtered out {response_df.shape[1] - n_cols} "
    #                      f"problematic columns")
    #     return response_df


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # response_json = {'a': 1, 'b': 2, 'c': [{'a': 11, 'b': 12}]}
    response_json = {
        'a': 1, 'b': 2, 'c': [{'a': 11, 'b': 12}, {'a': 110, 'b': 120}]}
    # response_json = {'a': 1, 'b': 2, 'c': {'a': 11, 'b': 12}}
    # response_json = [{'a': 1, 'b': [1, 2], 'c': 'abc'}]
    # response_json = [{'a': 1, 'b': [1, 2], 'c': 'abc'}, 
    #                  {'a': 10, 'b': [10, 20, 30], 'c': 'def'}]

    data_handler = DataHandler()
    df = data_handler.parse_response_json(response_json=response_json)
    
    print(df.shape)
    print(df.head())
