from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import plotly.express as px
import pandas as pd
import pymongo
from bson.objectid import ObjectId
import pprint  

client = pymongo.MongoClient('localhost', 27017)
# db = client.test
# print(db)
# exit()

db = client["academicworld"]
publications = db["publications"]
faculty = db["faculty"]


# testing = collection.find_one()
# print(testing)
# exit()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Nannan Website', style={'textAlign':'center'}),
    html.Div([
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
        ], id="widget-3")
    ]),

])

@callback(
    Output('keyword-trend-chart', "figure"),
    Input('trend_keyword', 'value')
)
def get_keyword_trend(value):


    pipeline = [
                {"$unwind":"$keywords"},
                {"$match": {"keywords.name": value}},
                {"$group":{"_id":"$year", "pub_cnt":{"$sum":1}}},
                {"$sort":{"_id": -1}},{"$limit":10}
                ]
    
    dff = pd.DataFrame(list(publications.aggregate(pipeline)), columns=["_id", "pub_cnt"])
    dff = dff.rename(columns={"_id": "YEAR", "pub_cnt": "PUBLICATIONS"})
    # pprint.pprint(dff)
    return px.line(dff, x='YEAR', y='PUBLICATIONS')

@callback(
    Output('best-related-universities', "children"),
    Input('interest_keyword', 'value')
)
def get_top_university_for_keyword(value):
    # dff = df[df.country==keyword]
    # return px.line(dff, x='year', y='num of publications')

    pipeline = [
                {"$unwind":"$keywords"},
                {"$match": {"keywords.name": value}},
                # {"$project":{"_id":0,"affiliation.name":1, "$affiliation.photoURL":1}},
                {"$group":{"_id": {"name": "$affiliation.name", "photo": "$affiliation.photoUrl"}, "faculty_cnt":{"$sum":1}}},
                {"$sort":{"faculty_cnt": -1}},{"$limit":5}
                ]
    child = []
    for university in faculty.aggregate(pipeline):
        child.append(
        html.Div([
            html.H4(university['_id']['name']),
            html.Img(src=university['_id']['photo'], height=100)
        ], className=""))
    pprint.pprint(child)
    # return html.Div(children=child)
    return child

    # pprint.pprint(dff)
    




if __name__ == '__main__':
    app.run_server(debug=True)
