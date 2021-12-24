import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# Data Load
data_saeb = pd.read_excel("divulgacao_regioes_ufs_ideb_2019-AF2.xlsx")

# dividing useful columns content of data_saeb
IDEB_GRADES = ('IDEB\n2005\n(N x P)', 'IDEB\n2007\n(N x P)', 'IDEB\n2009\n(N x P)',
                        'IDEB\n2011\n(N x P)', 'IDEB\n2013\n(N x P)', 'IDEB\n2015\n(N x P)',
                        'IDEB\n2017\n(N x P)', 'IDEB_2019')

SAEB_GRADES = ('Nota Média Padronizada (N)_saeb2007', 'Nota Média Padronizada (N)__saeb2009',
               'Nota Média Padronizada (N)_saeb2011', 'Nota Média Padronizada (N)_saeb2013',
               'Nota Média Padronizada (N)_saeb2015', 'Nota Média Padronizada (N)_saeb2017',
               'Nota Média Padronizada (N)__saeb2019')

APROVATAION_RATES = ('6º_TxAp2005', '7º_TxAp2005', '8º_TxAp2005', '9º_TxAp2005',
                     '6º_TxAp2007', '7º_TxAp2007', '8º_TxAp2007', '9º_TxAp2007',
                     '6º_TxAp2009', '7º_TxAp2009', '8º_TxAp2009', '9º_TxAp2009',
                     '6º_TxAp2011', '7º_TxAp2011', '8º_TxAp2011', '9º_TxAp2011',
                     '6º_TxAp2013', '7º_TxAp2013', '8º_TxAp2013', '9º_TxAp2013',
                     '6º_TxAp2015', '7º_TxAp2015', '8º_TxAp2015', '9º_TxAp2015',
                     '6º_TxAp2017', '7º_TxAp2017', '8º_TxAp2017', '9º_TxAp2017',
                     '6º_TxAp2019', '7º_TxAp2019', '8º_TxAp2019', '9º_TxAp2019')


token = open(".mapbox_token").read()
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

brazil_states["features"][0].keys()


# columns used for graphs generating
options_columns = {APROVATAION_RATES: 'Taxa de Aprovação', SAEB_GRADES: "Notas SAEB"}

# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


fig = px.choropleth_mapbox(data_saeb, locations="Regiao",
    geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},  # https://www.google.com/maps/ -> right click -> get lat/lon
    zoom=4, color="IDEB\n2005\n(N x P)", color_continuous_scale="Redor", opacity=0.4,
    hover_data={'6º_a_9ºano_TxAp2005': True, 'Nota Médi+AP:BAa Padronizada (N)_saeb2005': True, 'IDEB\n2005\n(N x P)': True}
    )

fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor="#242424",
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)

fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )


# =====================================================================
# Layout 
app.layout = dbc.Container(
    children=[
        dbc.Row([
                html.Div([
                    html.H5(children="DASHBOARD IDEB"),
                    dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
                ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
                html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),

                html.Div(
                        className="div-for-dropdown",
                        id="div-test",
                        children=[
                            dcc.DatePickerSingle(
                                id="date-picker",
                                min_date_allowed="2005",
                                max_date_allowed="2019",
                                date="2005",
                                display_format="YYYY",
                                style={"border": "0px solid black"},
                            )
                        ],
                    ),

                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=[dcc.Graph(id="choropleth-map", figure=fig,
                                        style={'height': '100vh', 'margin-right': '10px'})],
                ),

            ],  style={
                      "padding": "25px",
                      "background-color": "#242424"
                      }),
    ], fluid=True,
)


# =====================================================================
# Interactivity
@app.callback(
    [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ], [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    # print(location, date)

    print('=-=-=-=-')
    print(date)
    print(location)
    print('=-=-=-=-=')
    return (
        26,
        1,
        1,
        1,
        1,
        1,
    )

@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value"), Input("location-button", "children")]
)


@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)

def update_map(date):

    if date is None:
        return None

    if len(date) > 4:
        date = date[:4]

    if int(date)%2 == 0:
        return None

    form = {'Rondônia': 'RO', 'Acre': 'AC', 'Amazonas': 'AM', 'Roraima': 'RR', 'Pará': 'PA', 'Amapá': 'AP',
            'Tocantins': 'TO', 'Maranhão': 'MA', 'Piauí': 'PI', 'Ceará': 'CE', 'R. G. do Norte': 'RN', 'Paraíba': 'PB',
            'Pernambuco': 'PE', 'Alagoas': 'AL', 'Sergipe': 'SE', 'Bahia': 'BA', 'Minas Gerais': 'MG',
            'Espírito Santo': 'ES', 'Rio de Janeiro': 'RJ', 'São Paulo': 'SP', 'Paraná': 'PR', 'Santa Catarina': 'SC',
            'R. G. do Sul': 'RS', 'M. G. do Sul': 'MS', 'Mato Grosso': 'MT', 'Goiás': 'GO',  'Goiânia': 'GYN', 'Distrito Federal': 'DF'}
    not_accepted = ['6º_TxAp2005', '7º_TxAp2005', '8º_TxAp2005', '9º_TxAp2005',
                     '6º_TxAp2007', '7º_TxAp2007', '8º_TxAp2007', '9º_TxAp2007',
                     '6º_TxAp2009', '7º_TxAp2009', '8º_TxAp2009', '9º_TxAp2009',
                     '6º_TxAp2011', '7º_TxAp2011', '8º_TxAp2011', '9º_TxAp2011',
                     '6º_TxAp2013', '7º_TxAp2013', '8º_TxAp2013', '9º_TxAp2013',
                     '6º_TxAp2015', '7º_TxAp2015', '8º_TxAp2015', '9º_TxAp2015',
                     '6º_TxAp2017', '7º_TxAp2017', '8º_TxAp2017', '9º_TxAp2017',
                     '6º_TxAp2019', '7º_TxAp2019', '8º_TxAp2019', '9º_TxAp2019',
                     'Indicador de Rendimento', 'Matemática', 'Língua Portuguesa', '_p']
    accepted = ['Regiao', 'Rede']

    for column in data_saeb.columns:
        if date in column:
            is_in = False
            for not_accepted_column in not_accepted:
                if not_accepted_column in column:
                    is_in = True
                    break
            if not is_in:
                accepted.append(column)

    df = data_saeb[accepted].copy()

    regions = ['Norte', 'Nordeste', 'Sul', 'Sudeste', 'Centro-Oeste']
    for value in regions:
        df = df[df.Regiao != value]

    df = df.replace(form.keys(), form.values())

    fig = px.choropleth_mapbox(df, locations="Regiao", geojson=brazil_states,
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  # https://www.google.com/maps/ -> right click -> get lat/lon
        zoom=4, color=accepted[-1], color_continuous_scale="Redor", opacity=0.55,
        hover_data={accepted[-3]: True, accepted[-2]: True, accepted[-1]: True}
        )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)

    return fig


@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"

if __name__ == "__main__":
    app.run_server(debug=False, port=8052)