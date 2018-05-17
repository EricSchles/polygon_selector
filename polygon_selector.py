import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import json
import pandas as pd
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly' +
    '/datasets/master/2011_february_us_airport_traffic.csv')

app = dash.Dash()

app.layout = html.Div([
    html.Div(
        html.Pre(id='lasso', style={'overflowY': 'scroll', 'height': '100vh'}),
        className="three columns"
    ),
    html.Div(
        dcc.Input(
            id="polygon_label",
            placeholder="Enter a label",
            type="text",
            value=""
        )
    ),
    html.Div(
        className="nine columns",
        children=dcc.Graph(
            id='graph',
            figure={
                'data': [{
                    'lat': df.lat, 'lon': df.long, 'type': 'scattermapbox'
                }],
                'layout': {
                    'mapbox': {
                        'accesstoken': (
                            'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                            'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                        )
                    },
                    'margin': {
                        'l': 0, 'r': 0, 'b': 0, 't': 0
                    },
                }
            }
        )
    )
], className="row")


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    Output('lasso', 'children'),
    [Input('graph', 'selectedData'), Input("polygon_label", "value")])
def display_data(selectedData, value):
    points = selectedData["lassoPoints"]["mapbox"]
    geojson_polygon = {
        "type": "geojson",
        "data": {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates":[points]
                },
            "properties": {
                "name": value
            }        
        }
    }
    json.dump(geojson_polygon, open(value+".geojson","w"))
    return json.dumps(geojson_polygon, indent=2)


if __name__ == '__main__':
    for port in range(5000, 5100):
        try:
            app.run_server(port=5002)
        except:
            pass
