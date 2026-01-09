import pandas as pd
import numpy as np
import os

# Plotly modules/methods/settings
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True) # enables display of plotly figures in HTML/PDF notebooks

# Dash modules/methods/settings
import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
from GeoA import GeoA
external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'
]
path = os.path.dirname(os.getcwd()) + "/EnrollmentForecasting/data/cleaned_enrollmentdata.csv"
df = pd.read_csv(path)

df.rename(columns={'State or jurisdiction': 'State'}, inplace=True)
df.sort_values(by=['State', 'Year'], inplace=True)


app = Dash(__name__, external_stylesheets=external_stylesheets)
geo = GeoA(app)
geo_layout = geo.create_geographical_analysis()

tab_style = {
    'borderRadius': '10px',
    'padding': '15px 20px',
    'marginBottom': '10px',
    'border': 'none',
    'backgroundColor': '#f8f9fa',
    'color': '#495057',
    'fontWeight': '500',
    'transition': 'all 0.3s ease',
    'cursor': 'pointer',
    'textAlign': 'left'
}

tab_selected_style = {
    'borderRadius': '10px',
    'padding': '15px 20px',
    'marginBottom': '10px',
    'border': 'none',
    'backgroundColor': '#2193b0',
    'color': 'white',
    'fontWeight': '600',
    'boxShadow': '0 4px 15px rgba(33, 147, 176, 0.4)',
    'transform': 'translateX(5px)',
    'textAlign': 'left'
}


app.layout = html.Div(children=[
    html.H1(children='Enrollment Forecasting', style={'textAlign': 'center'}),

    html.Div(className='container-fluid',children=[
        html.Div(className='row',children=[
            html.Div(
                            className="col-md-3",
                            children=[
                                html.Div(
                                    style={
                                        'position': 'sticky',
                                        'top': '20px',
                                        'background': 'white',
                                        'borderRadius': '20px',
                                        'padding': '30px 20px',
                                        'boxShadow': '0 10px 40px rgba(0,0,0,0.1)'
                                    },
                                    children=[
                                        html.H4(
                                            "Navigate",
                                            style={
                                                'marginBottom': '25px',
                                                'color': '#2193b0',
                                                'fontWeight': '700',
                                                'fontSize': '1.3rem'
                                            }
                                        ),
                                        dcc.Tabs(
                                            id='vertical-tabs',
                                            value='tab-background',
                                            parent_className='custom-tabs',
                                            className='custom-tabs-container',
                                            vertical=True,
                                            children=[
                                                dcc.Tab(
                                                    label='Background',
                                                    value='tab-background',
                                                    style=tab_style,
                                                    selected_style=tab_selected_style
                                                ),
                                                dcc.Tab(
                                                    label='Data Table',
                                                    value='tab-data-table',
                                                    style=tab_style,
                                                    selected_style=tab_selected_style
                                                ),
                                                dcc.Tab(
                                                    label='Geographical Analysis',
                                                    value='tab-geo',
                                                    style=tab_style,
                                                    selected_style=tab_selected_style
                                                ),
                                                dcc.Tab(
                                                    label='Institutional Analysis',
                                                    value='tab-breadwinner',
                                                    style=tab_style,
                                                    selected_style=tab_selected_style
                                                ),
                                                dcc.Tab(
                                                    label='Temporal Analysis',
                                                    value='tab-prestige',
                                                    style=tab_style,
                                                    selected_style=tab_selected_style
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        html.Div(
                            className="col-md-9",
                            children=[
                                html.Div(
                                    id='tabs-content',
                                    style={
                                        'background': 'white',
                                        'borderRadius': '20px',
                                        'padding': '40px',
                                        'boxShadow': '0 10px 40px rgba(0,0,0,0.1)',
                                        'minHeight': '600px'
                                    }
                                )
                            ]
                        )
                    ]
                )
    ])
])
@app.callback(
    Output('tabs-content', 'children'),
    Input('vertical-tabs', 'value')
)
def render_content(tab):
    
    if tab == 'tab-data-table':
        return html.Div([
            html.H3("Enrollment Data"),
            dash_table.DataTable(
                id="enrollment-table",
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict("records"),

                page_size=10,
                sort_action="native",
                filter_action="native",

                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                    "whiteSpace": "normal",
                    "height": "auto",
                },
                style_header={
                    "backgroundColor": "#f2f2f2",
                    "fontWeight": "bold",
                }
            )
        ])
    elif tab == 'tab-background':
        return html.Div([
            dcc.Markdown(
                """
**Notes**
 * In data cleaning section, the Not Applicable values were replaced with 0s. This is because Not Applicable is the same as having 0 enrolled, other than for contextual reasons for the reader.
 * The data will be compiled into one dataframe, which will be used to forecast enrollment for each state.

**Data Cleaning**

* Columns in final DataFrame are as follows:
  * 'State or jurisdiction' : The state or jurisdiction of the row
  * 'Total_Pub_Under' : Total public undergrad enrollment
  * '4y_Pub_Under' : 4-year public undergrad enrollment
  * '2y_Pub_Under' : 2-year public undergrad enrollment
  * 'Total_Pub_Postbacc' : Total public postbacc enrollment
  * 'Total_Priv_Under' : Total private undergrad enrollment
  * 'Np_4y_Priv_Under' : Nonprofit 4-year private undergrad enrollment
  * 'Fp_4y_Priv_Under' : For-profit 4-year private undergrad enrollment
  * 'Np_2y_Priv_Under' : Nonprofit 2-year private undergrad enrollment
  * 'Fp_2y_Priv_Under' : For-profit 2-year private undergrad enrollment
  * 'Total_Priv_Postbacc' : Total private postbacc enrollment
  * 'Np_4y_Priv_Postbacc' : Nonprofit 4-year private postbacc enrollment
  * 'Fp_4y_Priv_Postbacc' : For-profit 4-year private postbacc enrollment


**EDA**

* Utilized ydata_profiling for exploratory analysis
* Obviously highly correlated features, especially totals, as they are combinations of other columns. Will hopefully be adding years, so that we can analyze trends over time.
* Full enrollment data including year as well as data shown here will be created in the data cleaning ipynb, as well as the eda ipynb.            
"""
            )
        ])
    if tab == 'tab-geo':
        return geo_layout

if __name__ == '__main__':
    app.run_server(debug=True)
