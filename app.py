from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import plotly.express as px
import pandas as pd
from bson.objectid import ObjectId
import mysql_utils
import mongo_utils


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Nannan Website', style={'textAlign':'center'}),
    html.Div([
    
        html.Div([
            #input component
            dcc.Input(id="trending_year", type="number", placeholder="year", value="2012"),
            #input component
            dcc.Input(id="trending_number", type="number", placeholder="amount", value="10"),
            #trend chart component
            dcc.Graph(id="popular_keywords")
        ], id="widget-1"),

        html.Div([
            #input component
            dcc.Input(id="trend_keyword", type="text", placeholder="keyword", value="data mining"),
            #trend chart component
            dcc.Graph(id="keyword-trend-chart")
        ], id="widget-2"),

        html.Div([
            #input component
            dcc.Input(id="interest_keyword", type="text", placeholder="keyword", value="data mining"),
            #university chart component
            html.Div(id="best-related-universities")
        ], id="widget-3"),

        html.Div([
            #input component
            dcc.Input(id="keyword_professor", type="text", placeholder="keyword", value="data mining"),
            #professor chart component
            html.Div(id="best-related-professors")
        ], id="widget-4"),

        html.Div([
            #input component
            dcc.Input(id="keyword_publications", type="text", placeholder="keyword", value="data mining"),
            #publications chart component
            html.Div(id="best-related-publications")
        ], id="widget-5")
    ]),

])


@callback(
    Output('popular_keywords', "figure"),
    Input('trending_year', 'value'),
    Input('trending_number', 'value'),
)
def get_popular_keywords(year, number):
    result = mysql_utils.get_popular_keywords(year, number)
    X = []
    Y = []
    for keys in result:
        X.append(keys[0])
        Y.append(keys[1])        
    return {
        'data': [
            {'x': X, 'y': Y, 'type': 'bar', 'name': 'POPULAR KEYWORDS'},
        ],
        'layout': {
            'title': 'SEE WHAT IS TRENDING'
        }
        }




@callback(
    Output('keyword-trend-chart', "figure"),
    Input('trend_keyword', 'value')
)
def get_keyword_trend(value):
    result = mongo_utils.get_keyword_trend(value)
    
    dff = pd.DataFrame(result, columns=["_id", "pub_cnt"])
    dff = dff.rename(columns={"_id": "YEAR", "pub_cnt": "PUBLICATIONS"})
    return px.line(dff, x='YEAR', y='PUBLICATIONS')

@callback(
    Output('best-related-universities', "children"),
    Input('interest_keyword', 'value')
)
def get_top_university_for_keyword(value):
    result = mongo_utils.get_top_university_for_keyword(value)
    child = []
    for university in result:
        child.append(
        html.Div([
            html.H4(university['_id']['name']),
            html.Img(src=university['_id']['photo'], height=100)
        ], className=""))
    return child

@callback(
    Output('best-related-professors', "children"),
    Input('keyword_professor', 'value')
)
def get_top_professors_for_keyword(value):
    result = mysql_utils.get_top_professors_for_keyword(value)
    child=[]
    for professor in result:
        child.append(
            html.Div([
                html.P(professor[0]),html.P(professor[1]),html.P(professor[2]),
                html.Img(src=professor[3], height=100)
            ], className=""))
    return child

@callback(
    Output('best-related-publications', "children"),
    Input('keyword_publications', 'value')
)
def get_top_s_for_keyword(value):
    result = mysql_utils.get_top_s_for_keyword(value)
    child=[]
    for publication in result:
        child.append(
            html.Div([
                html.P(publication[0]),html.P(publication[1]),html.P(publication[2]),html.P(publication[3],),
            ], className=""))
    return child    


if __name__ == '__main__':
    app.run_server(debug=True)
