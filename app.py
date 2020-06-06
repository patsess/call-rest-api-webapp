
import urllib.parse
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_table
from callrestapiwebapp.app_utils.initial_layout import AppInitialLayout
from callrestapiwebapp.rest_api_caller import RestApiCaller
from callrestapiwebapp.data_handler import DataHandler

__author__ = 'psessford'

# TODO:
#  - have an "add url param" button, allow empty url params (i.e. not used if 
#  the key is empty); probably handle it by having a callback that outputs the 
#  children (i.e. a list) of url param inputs, so that I can have as many as I 
#  like without crazy hardcoding
#  - have a dropdown to preview different orientations of the data, and a
#  button to "accept" the data
#  - allow data to be uploaded to a data base
#  - allow scheduling? (and allow changing the downloaded csv names? add date
#  to name?) ...AND... maybe once the user has chosen their data, create them
#  a main.py file and a gcp_deploy.sh file that they can download and (with the
#  help of a dev team) use to create a (e.g.) GCP Cloud Function?
#  - refactor callback code into new files?


"""
note on sharing data between callbacks:
https://dash.plotly.com/sharing-data-between-callbacks

notes on downloading files:
https://community.plotly.com/t/download-raw-data/4700/8
https://community.plotly.com/t/allowing-users-to-download-csv-on-click/5550/8
"""


app = dash.Dash(__name__)
app.layout = AppInitialLayout.get_initial_layout()


@app.callback(
    Output('target-url', 'children'),
    [Input('base-url-input', 'value'),
     Input('url-param01-name-input', 'value'),
     Input('url-param01-value-input', 'value'),
     Input('url-param02-name-input', 'value'),
     Input('url-param02-value-input', 'value')],
)
def update_target_url(base_url, url_param01_name, url_param01_value,
                      url_param02_name, url_param02_value):
    """Update children of div showing the target url

    :param base_url: (str)
        e.g. 'https://data.police.uk/api/crimes-street/all-crime'
    :param url_param01_name: (str) e.g. 'lat'
    :param url_param01_value: (str) e.g. '51.5080'
    :param url_param02_name: (str) e.g. 'lng'
    :param url_param02_value: (str) e.g. '-0.1281'
    :return target_url_children: (list)
    """
    if not base_url:
        return []

    target_url = (
        f"{base_url}?{url_param01_name}={url_param01_value}&"
        f"{url_param02_name}={url_param02_value}")
    return target_url


@app.callback(
    [Output('data-preview-div', 'children'),
     Output('data-store', 'data'),
     Output('data-download-link', 'style')],
    [Input('make-api-call-button', 'n_clicks')],
    [State('target-url', 'children'),
     State('data-download-link', 'style')]
)
def update_data(n_clicks, target_url, data_download_link_style):
    """Update data retrived from an api call

    :param n_clicks: (int)
    :param target_url: (str)
    :param data_download_link_style: (dict)
    :return data_preview, full_data_json: (dash_table.DataTable, json)
    """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'make-api-call-button' in changed_id:
        api_caller = RestApiCaller()
        response_json = api_caller.make_api_call(url=target_url)
        data_handler = DataHandler()
        response_df = data_handler.parse_response_json(
            response_json=response_json)
        _ = data_download_link_style.pop('display')
    else:
        response_df = pd.DataFrame({})

    data_preview = dash_table.DataTable(
        id='data-preview-table',
        columns=[{"name": i, "id": i} for i in response_df.columns],
        data=response_df.head().to_dict('records'),
    )
    full_data_json = response_df.to_json(date_format='iso', orient='split')
    return data_preview, full_data_json, data_download_link_style


@app.callback(
    Output('data-download-link', 'href'),
    [Input('data-store', 'data')])
def update_download_link(stored_data):
    """Update link for downloading data as a csv file

    :param stored_data: (json)
    :return csv_string: (str)
    """
    df = pd.read_json(stored_data, orient='split')
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = (
        "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string))
    return csv_string


if __name__ == "__main__":
    app.run_server(debug=True)
