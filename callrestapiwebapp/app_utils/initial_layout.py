
import dash_core_components as dcc
import dash_html_components as html

__author__ = 'psessford'


EXAMPLE_INPUTS = {
    'base-url-input': 'https://data.police.uk/api/crimes-street/all-crime',
    'url-param01-name-input': 'lat',
    'url-param01-value-input': '52.5080',
    'url-param02-name-input': 'lng',
    'url-param02-value-input': '-0.1281',
}


class AppInitialLayout:
    """Helper to specify the initial layout of dash app
    """
    @classmethod
    def get_initial_layout(cls):
        """Shortcut to get initial layout of dash app

        :return app_initial_layout: (html.Div)
        """
        app_initial_layout_helper = cls()
        app_initial_layout = app_initial_layout_helper()
        return app_initial_layout

    def __call__(self):
        """
        :return initial_layout: (html.Div)
        """
        initial_layout = html.Div([
            self._get_base_url_input_div(),
            html.Br(),
            self._get_url_params_input_div(),
            html.Br(),
            html.Br(),
            self._get_target_url_div(),
            html.Br(),
            html.Br(),
            self._get_make_api_call_button(),
            dcc.Store(id='data-store'),
            html.Div(id='data-preview-div'),
            self._get_download_csv_link(),
        ])
        return initial_layout

    @staticmethod
    def _get_base_url_input_div():
        return html.Div([
            html.I("Enter base URL:", style={'marginRight': '0.5em'}),
            dcc.Input(
                id='base-url-input', type='text',
                value=EXAMPLE_INPUTS['base-url-input'],
                placeholder=(f"e.g. {EXAMPLE_INPUTS['base-url-input']}"),
                style={'width': '70%'}),
        ])

    @staticmethod
    def _get_url_params_input_div():
        return html.Div([
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
        ])

    @staticmethod
    def _get_target_url_div():
        return html.Div(id='target-url-div', children=[
            html.I("Target URL:", style={'marginRight': '0.5em'}),
            html.Div(id='target-url')
        ])

    @staticmethod
    def _get_make_api_call_button():
        return html.Button(
            'Make API call', id='make-api-call-button', n_clicks=0)

    @staticmethod
    def _get_download_csv_link():
        return html.A('Download CSV', id='data-download-link',
            download='data_from_api_call.csv', href='',
            target='_blank', style={'display': 'none'})
