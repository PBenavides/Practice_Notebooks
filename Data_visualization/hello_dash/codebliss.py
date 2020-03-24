#This is a tutorial example from codebliss video on youtube. 

#This is a single page, without multiple pages or urls. We will use different dropdowns and stuff.

#We will use iexfinance, to get trading data. 

import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html 
import plotly.graph_objs as go
import pandas as pd
from dateutil.relativedelta import relativedelta

df = pd.read_csv('df_prueba.csv')

#First, we should do a stacked scatter plot



def make_stacked_plot(df,lista_palabras_a_buscar = ['mal','negativo','suma_good']):
  """
  Despues de haber creado las columnas correspondientes... 
  Se necesitará una lista de palabras a buscar para crear los plots.
  """

  #Defino los colores por si se quieren buscar más palabras. LIMITE: 6 palabras. 
  lista_colores = ["RoyalBlue","GhostWhite","MediumTurquoise","SlateGray","Black","LightSkyBlue","LightCyan"] 
  nro_palabras = len(lista_palabras_a_buscar)
  data_bar = []

  for palabra, color in zip(lista_palabras_a_buscar, lista_colores[0:nro_palabras]):
    data_bar.append(go.Bar(name=palabra, y=df.nombres, x=df[palabra], marker = {'color':color},orientation='h'))

  fig = go.Figure(data=data_bar)

  fig.update_layout(barmode='stack',title="Prueba dash",xaxis_title="Corporates",
                    width=840,height=800,autosize=False, font = dict(size=10))

  return fig


fig = make_stacked_plot(df)

app = dash.Dash()

#This element are going to contain all the other elements.

#With children you can look out the title of the page as h1. 
app.layout = html.Div([
    html.H1(children="Hello World"),
    html.Label("Dash graph"),
    html.Div(dcc.Graph(id="Prueba dash",
    figure = fig))

])

if __name__ == "__main__":
    app.run_server(debug=True)  #To run the server

