"""Create a Dash app within a Flask app."""
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import pandas as pd
from app.functions import get_tour_graph, get_era_graph, generate_table, get_tour
from dash.dependencies import Input, Output, State


tour_dict = np.load('tours_dict.npy', allow_pickle = True).item()
del tour_dict[71]
all_tours = list(tour_dict.keys())


all_first_dates = []
all_last_dates = []
for tour, lists in tour_dict.items():
    all_first_dates.append(tour_dict[tour][0][0])
    all_last_dates.append(tour_dict[tour][-1][0])

tour_list = list(zip(all_tours, all_first_dates, all_last_dates))
tour_list = sorted(tour_list)
joke = (150, 'Abba', 'ZZ Top')
tour_list.append(joke)

eras = ['All', '1.0', '2.0', '3.0', 'Pre 1995', '1995 - 2000', '2009 - 2014', '2015 to Present']


def create_dashboard(server):
    #Initiate the dashboard
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=['/static/style.css']
                         )

    #Pull in default html saved in layout.py
    #dash_app.index_string = html_layout
    #Create overall layout
    dash_app.layout = html.Div([
            # Input window for dates and graph options.
            html.Div([html.Img(
            src='https://github.com/jroefive/jroefive.github.io/blob/master/photos/phish-donut-stripe.jpg?raw=true', style={'width':'100%'})]),
            html.Div([
                html.Div([dcc.Dropdown(id='Tour',
                    options=[{'label': str(i[1])+' to '+str(i[2]), 'value': i[0]} for i in tour_list],
                    placeholder = "Select Tour to View")],
                    style={'width':'50%', 'display': 'inline-block'}),
                html.Div([dcc.Dropdown(id='Era',
                    options=[{'label': i, 'value': i} for i in eras],
                    placeholder="Select an Era to Compare Tours")],
                    style={'width':'50%', 'display': 'inline-block'}),],
                style = {'width': '80%', 'color': '#F15A50', 'text-align': 'center', 'backgroundColor': '#2C6E91',
                 'display': 'inline-block', 'min-height': '10px'}),
                #Graph options inputs
            html.Div([dcc.Graph(id='graph_tour')],style={'width':'90%','margin-left': '75px'}),
            html.Div([html.P(id='most-table', style={'width': '40%', 'display': 'inline-block'}),
                    html.P(id='never-table', style={'width': '40%', 'display': 'inline-block'})],
                 style={'width': '80%', 'color': '#F15A50', 'text-align': 'center', 'backgroundColor': '#2C6E91',
                        'margin-left':'25px', 'display': 'inline-block', 'min-height': '10px'}),
            html.Div([dcc.Graph(id='graph_era')], style={'width': '90%', 'margin-left': '75px'}),
            html.P('Feedback and feature requests welcome: jroefive@gmail.com',
                    style={'color': '#F15A50', 'font-family': 'Arial', 'text-align': 'center', 'height': '50px'}),
            dcc.Link('o          Phish Show Digest          ', href='https://phish-show-digest.wl.r.appspot.com/dashapp/',
                 style={'color': '#F15A50'}),
            dcc.Link('o          Phish Song Graphs          ',
                 href='https://the-story-of-a-phish-song.wl.r.appspot.com/dashapp/',
                 style={'color': '#F15A50'}),
            dcc.Link('o          Phish Set Closer Prediction          o',
                 href='https://predicting-phish-set-closers.wl.r.appspot.com/dashapp/',
                 style={'color': '#F15A50'}),
            html.Div([html.Img(
                src='https://github.com/jroefive/jroefive.github.io/blob/master/photos/phish-donut-stripe.jpg?raw=true',
                style={'width': '100%'})])],
        style={'text-align': 'center','backgroundColor':'#2C6E91'})


    #Update the month options after a year is chosen
    @dash_app.callback(
        Output('graph_tour', 'figure'),
        [Input('Tour', 'value')])
    def show_graph_tour(tour):
        figure = get_tour_graph(tour)
        return figure

    @dash_app.callback(
        Output('most-table', 'children'),
        [Input('Tour', 'value')])
    def show_graph_tour(tour):
        type = 'most'
        return generate_table(tour,type)

    @dash_app.callback(
        Output('never-table', 'children'),
        [Input('Tour', 'value')])
    def show_graph_tour(tour):
        type = 'never'
        return generate_table(tour,type)

    @dash_app.callback(
        Output('graph_era', 'figure'),
        [Input('Era', 'value')])
    def show_graph_era(era):
        figure = get_era_graph(era)
        return figure

    @dash_app.callback(
        Output('Tour', 'value'),
        [Input('graph_era', 'clickData')],
        [State('Era', 'value')])
    def update_tour_value(clickData,era):
        trace = clickData['points'][0]['curveNumber']
        tour = get_tour(trace, era)
        return tour

    return dash_app.server
