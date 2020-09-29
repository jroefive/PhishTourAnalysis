import pandas as pd
import dash_table
import numpy as np
import plotly.graph_objects as go

# Reduce  overall width
# Play with layout
def Extract(lst, element):
    return [item[element] for item in lst]

def get_values(tour):
    tour_dict = np.load('tours_dict.npy', allow_pickle = True).item()
    shows = Extract(tour_dict[tour],0)
    num_shows = len(shows)
    #ticks =  list(range(0, num_shows-1))
    percents = Extract(tour_dict[tour],1)
    new_songs = Extract(tour_dict[tour],4)
    return percents, new_songs, shows

def get_tour_graph(tour):

    tour_dict = np.load('tours_dict.npy', allow_pickle = True).item()
    tour_dict[150] = [('Show 1',1,20,0,'Every song that anyone would remember'), ('Show 2',0,20,0,' '), ('Show 3',0,20,0,' '), ('Show 4',0,20,0,' '), ('Show 5',0,20,0,' '), ('Show 6',0,20,0,' '), ('Show 7',0,20,0,' '), ('Show 8',0,20,0,' '), ('Show 9',0,20,0,' '), ('Show 10',0,20,0,' ')]
    shows = Extract(tour_dict[tour],0)
    num_shows = len(shows)
    ticks =  list(range(0, num_shows-1))
    percents = Extract(tour_dict[tour],1)
    new_songs = Extract(tour_dict[tour],4)

    fig = go.Figure([go.Bar(y=percents, hovertext=new_songs)])
    fig.update_traces(marker_color='#F15A50', marker_line_color="#2C6E91",
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(paper_bgcolor="#2C6E91",
        height=400,
        font=dict(
            family="Arial, monospace",
            size=18,
            color='#F15A50'),
        xaxis=dict(
            tickmode='array',
            tickvals=ticks,
            ticktext=shows,
            tickangle=90
        )
    )
    fig.update_layout(title = 'Hover over bar to see songs played for first time in tour',
        yaxis=dict(
            title='% songs in show not yet played in tour',
            tickmode='array',
            tickvals=[0, .2, .4, .6, .8, 1],
            ticktext=['0%', '20%', '40%', '60%', '80%', '100%']
        )
    )

    return fig

def get_era_graph(era):
    tour_dict = np.load('tours_dict.npy', allow_pickle=True).item()
    tours = []
    if era == '3.0':
        tours = [57,60,62,63,66,67,69,70,87,91,95,97,98,101,103,104,107]
    elif era == '2.0':
        tours = [52]
    elif era == '1.0':
        tours = [5,6,7,8,9,10,11,12,14,16,18,19,20,22,23,24,26,27,29,31,33,34,35,36,39,41,42,44,45,48]
    elif era == 'All':
        tours = list(tour_dict.keys())
        tours.remove(71)
    elif era == 'Pre 1995':
        tours = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 22, 23]
    elif era == '1995 - 2000':
        tours = [24,26,27,29,31,33,34,35,36,39,41,42,44,45,48]
    elif era == '2009 - 2014':
        tours = [57,60,62,63,66,67,69,70,87,91]
    elif era ==  '2015 to Present':
        tours = [95,97,98,101,103,104,107]


    era_dict = {}
    for tour in tours:
        era_dict[tour] = tour_dict[tour]

    fig = go.Figure()
    for tour in tours:
        percents, new_songs, shows = get_values(tour)
        fig.add_trace(go.Scatter(y=percents, hovertext=shows,
                                 mode='lines+markers', showlegend=False))

    fig.update_layout(title='Click any tour line to update graph above',paper_bgcolor="#2C6E91",
        font=dict(
            family="Arial, monospace",
            size=18,
            color='#F15A50'),
        xaxis=dict(
            title= 'Number of shows into tour'),
        yaxis=dict(
            title = '% songs in show not yet played in tour',
            tickmode='array',
            tickvals=[0, .2, .4, .6, .8, 1],
            ticktext=['0%', '20%', '40%', '60%', '80%', '100%']
        )
    )
    return fig

def get_tour(trace,era):
    tours = []
    if era == '3.0':
        tours = [57,60,62,63,66,67,69,70,87,91,95,97,98,101,103,104,107]
    elif era == '2.0':
        tours = [52]
    elif era == '1.0':
        tours = [5,6,7,8,9,10,11,12,14,16,18,19,20,22,23,24,26,27,29,31,33,34,35,36,39,41,42,44,45,48]
    elif era == 'All':
        tours = list(tour_dict.keys())
        tours.remove(71)
    elif era == 'Pre 1995':
        tours = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 22, 23]
    elif era == '1995 - 2000':
        tours = [24,26,27,29,31,33,34,35,36,39,41,42,44,45,48]
    elif era == '2009 - 2014':
        tours = [57,60,62,63,66,67,69,70,87,91]
    elif era ==  '2015 to Present':
        tours = [95,97,98,101,103,104,107]
    tour = tours[trace]
    return tour

def generate_table(tour,type):
    if type == 'most':
        top_songs_in_tour = np.load('top_songs_in_tour.npy', allow_pickle = True).item()
        table_list = top_songs_in_tour[tour]
        df = pd.DataFrame(table_list, columns=['Song', 'Times Played in Tour'])
    elif type == 'never':
        top_songs_in_tour = np.load('not_played_in_tour.npy', allow_pickle=True).item()
        table_list = top_songs_in_tour[tour]
        df = pd.DataFrame(table_list, columns=['Song Not Played in Tour', 'Times Played Prior to Tour'])
    return dash_table.DataTable(
        data=df.to_dict('records'),
        style_header={'textAlign':'left', 'color':"#2C6E91",'fontWeight': 'bold', 'fontSize':'20'},
        style_data={'whiteSpace': 'normal','margin-left':'10px'},
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_cell={'height': '10px', 'backgroundColor': '#e5ecf6'},
        style_data_conditional = [

                             ],
        )