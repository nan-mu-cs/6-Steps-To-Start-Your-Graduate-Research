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
            dash_table.DataTable(id="best-related-universities", columns=[
                {"id": "photo", "name": "photo", "presentation": "markdown"},
                {"id": "name", "name": "name"}],
                style_cell_conditional=[{"if": {"column_id": "photo"}, "width": "50px"},]
                )
            # html.Div(id="best-related-universities")
        ], id="widget-3"),

        html.Div([
            #input component
            dcc.Input(id="keyword_professor", type="text", placeholder="keyword", value="data mining"),
            html.Button('Sync Professor Updates', id='save_to_faculty', n_clicks=0),
            html.Div(id='sync_professor_placeholder', children=[]),
            #professor chart component
            dash_table.DataTable(id="best-related-professors", columns=[
                {"id": "photo", "name": "photo", "presentation": "markdown"},
                {"id": "name", "name": "name"},
                {"id": "phone", "name": "phone", "editable": True},
                {"id": "email", "name": "email", "editable": True},
                {"id": "faculty_id", "name": "faculty_id", "hideable": True}
                ],
                style_cell_conditional=[{"if": {"column_id": "photo"}, "width": "50px"},]
                )
            # html.Div(id="best-related-professors")
        ], id="widget-4"),

        html.Div([
            #input component
            dcc.Input(id="keyword_publications", type="text", placeholder="keyword", value="data mining"),
            #publications chart component
            # html.Div(id="best-related-publications")
            dash_table.DataTable(id="best-related-publications", columns=[
                {"id": "title", "name": "title"},
                {"id": "venue", "name": "venue"},
                {"id": "year", "name": "year"},
                {"id": "num_citations", "name": "num_citations"}
                ]
                )
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
    Output('best-related-universities', "data"),
    Input('interest_keyword', 'value')
)
def get_top_university_for_keyword(value):
    result = mongo_utils.get_top_university_for_keyword(value)
    data = []
    for university in result:
        data.append({
            "name": university['_id']['name'],
            "photo": "![]({photo}#u-photo)".format(photo=university['_id']['photo'])
        })
    return data

@callback(
    Output('best-related-professors', "data"),
    Input('keyword_professor', 'value')
)
def get_top_professors_for_keyword(value):
    result = mysql_utils.get_top_professors_for_keyword(value)
    data=[]
    for professor in result:
        data.append({
            "name": professor[0],
            "phone": professor[1],
            "email": professor[2],
            "photo": "![]({photo}#p-photo)".format(photo=professor[3]),
            "faculty_id": professor[4]
        })
    return data

@callback(
    Output('best-related-publications', "data"),
    Input('keyword_publications', 'value')
)
def get_top_s_for_keyword(value):
    result = mysql_utils.get_top_s_for_keyword(value)
    data = []
    for publication in result:
        data.append({
            "title": publication[0],
            "venue": publication[1],
            "year": publication[2],
            "num_citations": publication[3]
        })
    return data    

@callback(
    Output('sync_professor_placeholder', 'children'),
    Input('save_to_faculty', "n_clicks"),
    State('best-related-professors', 'data')
)
def save_professors(n_clicks, data):
    output = html.Plaintext("The data has been saved to your Mysql database.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})
    if n_clicks > 0:
        mysql_utils.save_professors(data)
        return output
    else:
        return no_output
    


if __name__ == '__main__':
    app.run_server(debug=True)
