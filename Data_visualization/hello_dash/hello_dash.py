import dash
from dash.dependencies import Output, Input
#An event (Input)  is what triggers some sort of function. Lots of time an input is called as an "event"

import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque 
#Deque is a container with max size. As a list that pop-out extra elements and insert the new one. 

X = deque(maxlen=20)
Y = deque(maxlen=20)

X.append(1)
Y.append(1)

app = dash.Dash(__name__)
#We need an id to actualized the element
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    #This will trigger an event
    dcc.Interval(
        id='graph-update', 
        interval = 1000,
        n_intervals=0
    ), 
])

@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])

def update_graph():
    #Maybe you will have a SQL query to replace this. But this in only an example of how to change X and Y
    X.append(X[-1]+1)
    Y.append(Y[-1] + Y[-1]*random.uniform(-0.1,0.1))

    #Here is where the Plot.ly code goes!

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
    )

    return {'data':[data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server(debug=True)