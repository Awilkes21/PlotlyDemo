#################################################################
# UNCLASSIFIED
#################################################################

import os
import sys

import getopt
import logging

import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import Dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

from waitress import serve

from urllib.parse import urlparse, parse_qs

import pandas as pd


################################################
app = Dash(__name__, title='Example Plotly Dash App', suppress_callback_exceptions=True)
app.layout = html.Div(children=[
    dcc.Store(id='store_example_redirect_store', storage_type='session', data={}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



#################################################################
# load data from excel sheet and put into dataframe
# data from census.gov for years 2010-2019
df = pd.read_csv("CleanedCensusData.csv")

#################################################################


def Page_NotFound():
    return html.H1(children="Page Not Found!", style={'font-weight': 'bold'})


###############################################

# determine which page to display
@app.callback(
    [Output('page-content', 'children'),
     Output('store_example_redirect_store', 'data')],
    [Input('url', 'pathname'), Input('url', 'href')],
    State('store_example_redirect_store', 'data'))
def display_page(pathname, href, store_example_redirect_store):
    
    if not pathname == '/' and len(store_example_redirect_store) == 0:
        return dcc.Location(pathname="/", id="loc_redirect"), store_example_redirect_store
    elif pathname == '/':
        return FillPage(), {"index_page":True}
    elif  '/nav_page' in pathname:
        return html.Div("This is the nav page!"), store_example_redirect_store

    return Page_NotFound(), store_example_redirect_store


#################################################################

# Fills the page with all of the html and dash components we need
def FillPage()->html.Div:
    return [
        #app.layout = html.Div([
            html.H1("Welcome, this is an example Plotly Dash App!", style={'text-align': 'center'}),

            # dropdown that allows the user to pick between total population and percent change
            html.Div([
                dcc.Dropdown(
                    id='select-data',
                    options=[
                        {'label': 'Percent Change in Population', 'value': 'PPOPCHG'},
                        {'label': 'Total Change in Population', 'value': 'NPOPCHG'},
                        {'label': 'Total Population', 'value': 'POPESTIMATE'},   
                    ],
                    multi=False,
                    value='PPOPCHG'
                )],
                style={'width':'25%'}
            ),
            html.Br(),

            # create the empty map
            dcc.Graph(id='population-map'),

            # create a range slider for the years
            html.Div(id='slider-text'),
            html.Div([
                dcc.RangeSlider(
                    id='year-slider',
                    min=2010,
                    max=2019,
                    step=1,
                    dots=True,
                    updatemode = 'mouseup',
                    pushable=1,
                    tooltip={'always_visible':False,
                            'placement': 'bottom'},
                    marks={
                        2010: '2010',
                        2015: '2015',
                        2019: '2019',
                    },
                    value=[2010, 2011]
                )],
                style={'width':'70%', 'position':'absolute', 'left':'5%'}
            ),
            
            html.Br(),
            html.Br(),
            html.Div(id='US-average'),
        ]
#################################################################
# Callback to fill the graph depending on user input
@app.callback(
    [Output('population-map', 'figure'),
    Output('slider-text', 'children'),
    Output('US-average', 'children')],
    [Input('select-data', 'value'),
    Input('year-slider', 'value')]
)
def UpdateGraph(dataChosen, yearRange):
    # create various strings depending on the map selected to output later
    title = ''
    description = ''
    unit = ''
    if (dataChosen == 'POPESTIMATE'):
        title = 'Estimated Population in the U.S. by State'
        description = 'estimated population'
        unit = ' people'
    elif (dataChosen == 'PPOPCHG'):
        title = 'Percent Change in Population in the U.S. by State'
        description = 'percent change in population'
        unit = '%'
    else:
        title = 'Total Change in Population in the U.S. by State'
        description = 'total change in population'
        unit = ' people'
    
    # output the current selected range
    rangeContainer = 'The current year range is {}'.format(yearRange)
    
    # create a new empty dataframe for all of the information we need based on the year filter
    dff = df[(df['YEAR'] >= yearRange[0])&(df['YEAR'] <= yearRange[1])]

    # group the data and find the average of the type chosen in the dropdown, make sure not to make them the index
    dfaverage = dff.groupby(['STATE_CODE', 'STATE'], as_index=False)[dataChosen].mean()

    # calculate the average for the entire country
    # gets the average of each individual state, then finds one average for the country
    average = 0
    count = 0
    for item in dfaverage[dataChosen]:
        average += item
        count += 1
    average /= count

    # create a string to output
    outputAverage = "The average {} in a U.S. state from {} to {} is {}{}".format(description, str(yearRange[0]), str(yearRange[1]), str(average), unit)

    # create the choropleth map to display
    fig = px.choropleth(
        data_frame=dfaverage,
        # ensure the map of the US is used
        locationmode='USA-states',
        locations='STATE_CODE',
        scope='usa',
        # change color based on the data we are quantifying
        color=dataChosen,
        # display certain items on hover
        hover_name='STATE',
        hover_data={'STATE_CODE', dataChosen},
        labels={'POPESTIMATE':'Population Estimate', 'PPOPCHG':'Population Change %', 'NPOPCHG':'Total Population Change', 'STATE':'State', 'STATE_CODE': 'State Code'},
        title=title,
        height=550,
    )
    # return the graph and the year range selected
    return fig, rangeContainer, outputAverage
#################################################################

if __name__ == '__main__':
    
    # setup logging mode
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s %(funcName)20s()",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # default host and port
    host='0.0.0.0'
    port=8050

    # default setting to run using Waitress Web Server Gateway Interface
    run_in_waitress=False

    # process command line arguments
    # define the options flags to parse out of the command line
    opts, args = getopt.getopt(sys.argv[1:],"h:p:w")
    # parse the command line optons
    for opt, arg in opts:
        if opt == '-h':
            host=arg
        if opt == '-p':
            port=arg
        if opt == '-w':
            run_in_waitress=False

    if run_in_waitress:
        # run waitress server
        serve(app.server, host=host, port=port)
    else:
        app.run_server(host=host, port=port, debug=True)

#################################################################
# UNCLASSIFIED
#################################################################