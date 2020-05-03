
import dash_core_components as dcc
import dash_html_components as html

__author__ = 'psessford'

# TODO: convert get_initial_layout() into class


EXAMPLE_INPUTS = {
    'base-url-input': 'https://data.police.uk/api/crimes-street/all-crime',
    'url-param01-name-input': 'lat',
    'url-param01-value-input': '52.5080',
    'url-param02-name-input': 'lng',
    'url-param02-value-input': '-0.1281',
}


def get_initial_layout():
    """Get initial layout of dash app

    :return initial_layout: (html.Div)
    """
    initial_layout = html.Div(
        [
            html.I("Enter base URL:", style={'marginRight': '0.5em'}),
            dcc.Input(
                id='base-url-input', type='text',
                value=EXAMPLE_INPUTS['base-url-input'],
                placeholder=(f"e.g. {EXAMPLE_INPUTS['base-url-input']}"),
                style={'width': '70%'}),
            html.Br(),
            html.I("Enter URL parameter:", style={'marginRight': '0.5em'}),
            dcc.Input(
                id='url-param01-name-input', type='text',
                value=EXAMPLE_INPUTS['url-param01-name-input'],
                placeholder=(
                    f"name, e.g. {EXAMPLE_INPUTS['url-param01-name-input']}"),
                style={'marginRight': '0.5em'}),
            dcc.Input(
                id='url-param01-value-input', type='text',
                value=EXAMPLE_INPUTS['url-param01-value-input'],
                placeholder=(f"value, e.g. "
                             f"{EXAMPLE_INPUTS['url-param01-value-input']}")),
            html.Br(),
            html.I("Enter URL parameter:", style={'marginRight': '0.5em'}),
            dcc.Input(
                id='url-param02-name-input', type='text',
                value=EXAMPLE_INPUTS['url-param02-name-input'],
                placeholder=(
                    f"name, e.g. {EXAMPLE_INPUTS['url-param02-name-input']}"),
                style={'marginRight': '0.5em'}),
            dcc.Input(
                id='url-param02-value-input', type='text',
                value=EXAMPLE_INPUTS['url-param02-value-input'],
                placeholder=(f"value, e.g. "
                             f"{EXAMPLE_INPUTS['url-param02-value-input']}")),
            html.Br(),
            html.Br(),
            html.Div(id='target-url-div', children=[
                html.I("Target URL:", style={'marginRight': '0.5em'}),
                html.Div(id='target-url')
            ]),
            html.Br(),
            html.Br(),
            html.Button(
                'Make API call', id='make-api-call-button', n_clicks=0),
            dcc.Store(id='data-store'),
            html.Div(id='data-preview-div'),
            html.A('Download CSV', id='data-download-link',
                   download='data_from_api_call.csv', href='',
                   target='_blank', style={'display': 'none'}),
        ]
    )
    return initial_layout
