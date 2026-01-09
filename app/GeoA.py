import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from scipy import stats
from matplotlib.colors import TwoSlopeNorm
import json
import dash
import geopandas as gpd
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table

class GeoA():
    def __init__(self, app):
        self.states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
            "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
            "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
            "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
            "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
            "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
            "Wisconsin", "Wyoming", "District of Columbia"
        ]
        self.quad_regions = {
            'northeast' : [
                "Connecticut", "Maine", "Massachusetts", "New Hampshire",
                "New Jersey", "New York", "Pennsylvania", "Rhode Island", "Vermont"
            ],
            'midwest' : [
                "Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota",
                "Missouri", "Nebraska", "North Dakota", "Ohio", "South Dakota",
                "Wisconsin"
            ],
            'south' : [
                "Alabama", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky",
                "Louisiana", "Maryland", "Mississippi", "North Carolina", "Oklahoma",
                "South Carolina", "Tennessee", "Texas", "Virginia", "West Virginia"
            ],
            'west' : [
                "Alaska", "Arizona", "California", "Colorado", "Hawaii", "Idaho",
                "Montana", "Nevada", "New Mexico", "Oregon", "Utah", "Washington",
                "Wyoming"
            ]
        }
        self.census_regions = {
            'ne_division' : ['Connecticut', 'Maine', 'Massachusetts','New Hampshire', 'Rhode Island','Vermont'],
            'mid_atlantic' : ['New Jersey', 'New York', 'Pennsylvania'],
            'e_north_cent' : ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin'],
            'w_north_cent' : ['Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
            'south_atlantic' : ['Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'West Virginia'],
            'east_south_central' : ['Alabama', 'Kentucky', 'Mississippi', 'Tennessee'],
            'west_south_central' : ['Arkansas', 'Louisiana', 'Oklahoma','Texas'],
            'mountain' : ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming'],
            'pacific' : ['Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
        }
        self.enrollment = pd.read_csv(os.path.dirname(os.getcwd()) + '/EnrollmentForecasting/data/final_enrollmentdata.csv')
        self.app = app
        self.state_codes = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC"
        }


    def comparing_quad_regions(self):
        fig = go.Figure()

        for key in self.quad_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.quad_regions[key])].groupby('Year').agg({"Total_Enrollment": "sum"}).reset_index()

            fig.add_trace(go.Scatter(
                x=region_df['Year'],
                y=region_df['Total_Enrollment'],
                mode='lines+markers',
                name=key
            ))
        return fig
    
    def scaled_comparisons_quad_regions(self):
        results = {}
        fig = go.Figure()
        for key in self.quad_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.quad_regions[key])].groupby('Year').agg({"Total_Enrollment": "sum"}).reset_index()

            region_df['baseline'] = region_df[region_df['Year'] == '2012-13']['Total_Enrollment'].values[0]

            region_df['eindex'] = (region_df['Total_Enrollment']/ region_df['baseline'])*100

            slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(region_df['Year'])), region_df['eindex'])

            results[key] = {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err
            }

            if p_value < 0.05:
                results[key]['sig'] = True
            else:
                results[key]['sig'] = False

            fig.add_trace(go.Scatter(
                x=region_df['Year'],
                y=region_df['eindex'],
                mode='lines+markers',
                name=key
            ))

        return (fig, results)
            
    def quad_region_anova(self):
        region_changes = {}
        for key in self.quad_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.quad_regions[key])]
            region_change = region_df.groupby('State')['Total_Enrollment'].apply(lambda x: x.pct_change().mean())
            region_changes[key] = region_change

        f_stat, p_value = stats.f_oneway(region_changes['northeast'], region_changes['south'], region_changes['west'], region_changes['midwest'])

        return (f_stat, p_value)

    
        
    
    def comparing_census_regions(self):
        fig = go.Figure()

        for key in self.census_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.census_regions[key])].groupby('Year').agg({"Total_Enrollment": "sum"}).reset_index()

            fig.add_trace(go.Scatter(
                x=region_df['Year'],
                y=region_df['Total_Enrollment'],
                mode='lines+markers',
                name=key
            ))
        return fig
    
    def scaled_comparing_census_regions(self):
        results = {}
        fig = go.Figure()
        for key in self.census_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.census_regions[key])].groupby('Year').agg({"Total_Enrollment": "sum"}).reset_index()

            region_df['baseline'] = region_df[region_df['Year'] == '2012-13']['Total_Enrollment'].values[0]

            region_df['eindex'] = (region_df['Total_Enrollment']/ region_df['baseline'])*100

            slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(region_df['Year'])), region_df['eindex'])

            results[key] = {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err
            }

            if p_value < 0.05:
                results[key]['sig'] = True
            else:
                results[key]['sig'] = False

            fig.add_trace(go.Scatter(
                x=region_df['Year'],
                y=region_df['eindex'],
                mode='lines+markers',
                name=key
            ))

        return (fig, results)
    
    def spatial_autocorrelation(self):
        state_dict = json.load(open(os.path.dirname(os.getcwd()) + '/EnrollmentForecasting/data/state_neighbors.json'))
        state_enrollment = self.enrollment[self.enrollment["State"].isin(self.states)]
    
        for state, neighbors in state_dict.items():
            state_trend = state_enrollment[state_enrollment['State'] == state].groupby('Year').sum().reset_index()
            state_baseline = state_trend[state_trend['Year'] == '2012-13']['Total_Enrollment'].values[0]
            state_trend['eindex'] = (state_trend['Total_Enrollment']/ state_baseline)*100

            state_slope, state_intercept, state_r_value, state_p_value, state_std_err = stats.linregress(np.arange(len(state_trend['Year'])), state_trend['eindex'])
            state_dict[state]['slope'] = state_slope
            state_dict[state]['intercept'] = state_intercept
            state_dict[state]['r_value'] = state_r_value
            state_dict[state]['p_value'] = state_p_value
            state_dict[state]['std_err'] = state_std_err

            if state_p_value < 0.05:
                state_dict[state]['sig'] = True
            else:
                state_dict[state]['sig'] = False
    
        for state, vals in state_dict.items():
            neighbors = vals['neighbors']
            neighbor_slopes = [
                state_dict[n]['slope']
                for n in neighbors
                if state_dict[n]['sig'] is True
            ]
            if len(neighbor_slopes) == 0:
                vals['signed_neighbor_index'] = None
            else:
                neighbor_avg = np.mean(neighbor_slopes)
                vals['signed_neighbor_index'] = vals['slope'] - neighbor_avg
    
    # Prepare data for Plotly
        df = (
            pd.DataFrame.from_dict(state_dict, orient='index')
            .reset_index()
            .rename(columns={'index': 'state'})
        )
        print(df)

        df['state_codes'] = df['state'].map(self.state_codes)
    
    # Create Plotly choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=df['state_codes'],
            z=df['signed_neighbor_index'],
            locationmode='USA-states',
            colorscale='RdBu_r',
            zmid=0,
            colorbar_title="Signed Neighbor Index",
            hovertemplate='<b>%{location}</b><br>' +
                          'Index: %{z:.4f}<br>' +
                          '<extra></extra>'
        ))
    
        fig.update_layout(
            title_text='Enrollment Trend Relative to Neighboring States (Signed Index)',
            geo_scope='usa',
            height=600,
            margin={"r":0,"t":50,"l":0,"b":0}
        )
    
        return fig

    
    def census_region_anova(self):
        region_changes = {}
        for key in self.census_regions:
            region_df = self.enrollment[self.enrollment['State'].isin(self.census_regions[key])]
            region_change = region_df.groupby('State')['Total_Enrollment'].apply(lambda x: x.pct_change().mean())
            region_changes[key] = region_change

        #'ne_division', 'mid_atlantic', 'e_north_cent', 'w_north_cent', 'south_atlantic', 'east_south_central', 'west_south_central', 'mountain', 'pacific'
        f_stat, p_value = stats.f_oneway(region_changes['ne_division'], region_changes['mid_atlantic'], region_changes['e_north_cent'], region_changes['w_north_cent'], region_changes['south_atlantic'], region_changes['east_south_central'], region_changes['west_south_central'], region_changes['mountain'], region_changes['pacific'])

        return (f_stat, p_value)


    def create_geographical_analysis(self):
        scaled_quad_results = self.scaled_comparisons_quad_regions()
        anova_results = self.quad_region_anova()
        table_data = []
        for region, stats in scaled_quad_results[1].items():
            table_data.append({
                'Region': region,
                'Slope': round(stats['slope'], 4),
                'Intercept': round(stats['intercept'], 4),
                'R-value': round(stats['r_value'], 4),
                'P-value': round(stats['p_value'], 4),
                'Std Error': round(stats['std_err'], 4),
                'Significant': 'Yes' if stats['sig'] else 'No'
            })
        scaled_census_results = self.scaled_comparing_census_regions()
        census_anova_results = self.census_region_anova()
        census_table_data = []
        for region, stats in scaled_census_results[1].items():
            census_table_data.append({
                'Region': region,
                'Slope': round(stats['slope'], 4),
                'Intercept': round(stats['intercept'], 4),
                'R-value': round(stats['r_value'], 4),
                'P-value': round(stats['p_value'], 4),
                'Std Error': round(stats['std_err'], 4),
                'Significant': 'Yes' if stats['sig'] else 'No'
            })
        display = html.Div(id='geographical_analysis', children=[
            html.H3("Geographical Analysis"),
        
        # Sub-tabs for quadrant vs census regions
            dcc.Tabs(
                id='geo-tabs',
                value='tab-quad-regions',
                children=[
                    dcc.Tab(
                        label='General Regions',
                        value='tab-quad-regions',
                    ),
                    dcc.Tab(
                        label='Census Regions',
                        value='tab-census-regions',
                    ),
                    dcc.Tab(
                        label="Spatial Autocorrelation",
                        value='tab-spatial-autocorrelation'
                    )
                ]
            ),
            html.Div(id='geo-tabs-content')  # Content container for geo sub-tabs
        ])
    
        self.register_geo_tab_callback(scaled_quad_results, scaled_census_results, anova_results, table_data, census_anova_results, census_table_data)
    
        return display

    def register_geo_tab_callback(self, scaled_quad_results, scaled_census_results, anova_results, table_data, census_anova_results, census_table_data):
        @self.app.callback(
            Output('geo-tabs-content', 'children'),
            Input('geo-tabs', 'value')
        )
        def update_geo_tab_content(tab):
            if tab == 'tab-quad-regions':
                return html.Div([
                html.H4("General Regions"),
                dcc.Graph(
                    id='quad_graph',
                    figure=self.comparing_quad_regions()
                ),
                html.H5("Scaled Comparison (Indexed to 2012-13 = 100)"),
                dcc.Graph(
                    id='quad_graph2',
                    figure=scaled_quad_results[0]
                ),
                html.H5("Linear Regression Statistics"),
                dash_table.DataTable(
                    id='quad_graph3',
                    columns=[
                        {"name": "Region", "id": "Region"},
                        {"name": "Slope", "id": "Slope"},
                        {"name": "Intercept", "id": "Intercept"},
                        {"name": "R-value", "id": "R-value"},
                        {"name": "P-value", "id": "P-value"},
                        {"name": "Std Error", "id": "Std Error"},
                        {"name": "Significant", "id": "Significant"}
                    ],
                    data=table_data,
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    style_table={
                        "overflowX": "auto",
                        "maxHeight": "500px"
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "8px",
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    style_header={
                        "backgroundColor": "#f2f2f2",
                        "fontWeight": "bold",
                    },
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Significant} = "Yes"',
                                'column_id': 'Significant'
                            },
                            'backgroundColor': '#d4edda',
                            'color': '#155724'
                        }
                    ]
                ),
                html.H5("ANOVA Results", style={'marginTop': '30px'}),
                html.Div([
                    html.P(f"F-statistic: {round(anova_results[0], 4)}"),
                    html.P(f"P-value: {round(anova_results[1], 4)}"),
                    html.P(
                        "Significant difference between regions" if anova_results[1] < 0.05 
                        else "No significant difference between regions",
                        style={
                            'fontWeight': 'bold',
                            'color': '#155724' if anova_results[1] < 0.05 else '#856404'
                        }
                    )
                ])
            ])
        
            elif tab == 'tab-census-regions':
                return html.Div([
                html.H4("Census Regions"),
                dcc.Graph(
                    id='census_graph',
                    figure=self.comparing_census_regions()
                ), 
                html.H5("Scaled Comparison (Indexed to 2012-13 = 100)"),
                dcc.Graph(
                    id='quad_graph2',
                    figure=scaled_census_results[0]
                ),
                html.H5("Linear Regression Statistics"),
                dash_table.DataTable(
                    id='quad_graph3',
                    columns=[
                        {"name": "Region", "id": "Region"},
                        {"name": "Slope", "id": "Slope"},
                        {"name": "Intercept", "id": "Intercept"},
                        {"name": "R-value", "id": "R-value"},
                        {"name": "P-value", "id": "P-value"},
                        {"name": "Std Error", "id": "Std Error"},
                        {"name": "Significant", "id": "Significant"}
                    ],
                    data=census_table_data,
                    page_size=10,
                    sort_action="native",
                    filter_action="native",
                    style_table={
                        "overflowX": "auto",
                        "maxHeight": "500px"
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "8px",
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    style_header={
                        "backgroundColor": "#f2f2f2",
                        "fontWeight": "bold",
                    },
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Significant} = "Yes"',
                                'column_id': 'Significant'
                            },
                            'backgroundColor': '#d4edda',
                            'color': '#155724'
                        }
                    ]
                ),
                html.H5("ANOVA Results", style={'marginTop': '30px'}),
                html.Div([
                    html.P(f"F-statistic: {round(census_anova_results[0], 4)}"),
                    html.P(f"P-value: {round(census_anova_results[1], 4)}"),
                    html.P(
                        "Significant difference between regions" if census_anova_results[1] < 0.05 
                        else "No significant difference between regions",
                        style={
                            'fontWeight': 'bold',
                            'color': '#155724' if anova_results[1] < 0.05 else '#856404'
                        }
                    )
                ])
            ])
            elif tab == 'tab-spatial-autocorrelation':
                return html.Div([
                html.H4("Spatial Autocorrelation"),
                dcc.Graph(
                    id='spatial_graph',
                    figure=self.spatial_autocorrelation()
                )
            ])


if __name__ == '__main__':
    geo = GeoA()
    geo.create_geographical_analysis()