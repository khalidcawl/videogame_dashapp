import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data

import pandas as pd

alt.renderers.enable("mimetype")
alt.data_transformers.enable("data_server")

sales = pd.read_csv("vgsales.csv")


def plot_altair(top_val):
    top_publishers = sales["Publisher"].value_counts().head(int(top_val)).index.tolist()
    top_publishers_df = sales.query("Publisher in @top_publishers")
    chart = alt.Chart(top_publishers_df).mark_bar().encode(
            x="count()",
            y=alt.Y("Publisher", sort="-x")
        )
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

top_values = [5,10,15,20]
app.layout = html.Div([
        dcc.Dropdown(
            id='top_val', value='10',
            options=[{'label': i, 'value': i} for i in top_values]),
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            srcDoc=plot_altair(top_val='10'))])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('top_val', 'value'))
def update_output(top_val):
    return plot_altair(top_val)

if __name__ == '__main__':
    server = app.run_server(debug=True)