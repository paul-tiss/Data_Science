import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly_express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import json



#On importe notre DF
df_finale = pd.read_csv(r"table_finale.csv",sep=';')

#On réalise quelques asignations afin de faciliter la lecture du dash
df_finale['nb_usines_polluantes'] = df_finale['nb_usines_polluantes']*10/3
data = df_finale[df_finale['score_final'].isin( df_finale['score_final'].nlargest(10))][['commune','score_final']]
data_carte = df_finale[['code_insee','classe_potentiel']]

#On ouvre le geojson
with open("communes_light.geojson", 'r') as f:
    data2 = json.load(f)


#On commence notre dashboard
if __name__ == '__main__':

    app = dash.Dash(__name__) 

    #On crée un barplot qui sera affiché lors de l'ouverture de la page
    fig = px.bar(data, x="commune", y="score_final",labels = {"commune" : "Communes", "score_final":"Score global de dangerosité"}) 

    #On crée un histogramme qui sera affiché lors de l'ouverture de la page
    histo = px.histogram(df_finale[df_finale['nb_usines_polluantes'] > 1], x="nb_usines_polluantes")

    #On crée ensuite une carte qui sera également affichée directement
    carte = px.choropleth_mapbox(df_finale, geojson=data2, featureidkey = 'properties.code_commune', locations='code_insee', color='classe_potentiel',
                        color_continuous_scale="Viridis",
                        range_color=(1, 3),
                        mapbox_style="carto-positron",
                        zoom=6, center = {"lat": 48.7453229, "lon": 2.5073644},
                        opacity=0.5,
                        labels={'classse_potentiel':'Potentiel radon'}
                        )

    #On passe ensuite à la mise en page
    app.layout = html.Div(children=[

                #Ce premier div va concerner l'histogramme
                html.Div([

                            html.H1(children=f'Les communes les plus à risque de France',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), 

                            html.Div(children=f'''
                                Ce graphique permet de voir quelles sont les villes les plus risquées de France selon nos critères. 
                            '''),
                            
                            html.Br(),

                            html.Label('''Choix du nombre de villes que l'on veut afficher  '''),
                        
                            #On crée un selecteur afin de laisser le choix du nombre de communes que l'on veut afficher
                            dcc.Input(
                                id = 'nb_input',
                                type = 'number',
                                min = 1,
                                placeholder = 'Entrez un nombre',
                                value = 10
                                
                            ),

                            html.Br(),

                            #On crée une liste déroulante afin de permettre le choix du score que l'on veut afficher
                            dcc.Dropdown(
                                id="comparatif",
                                options=[
                                    {'label': 'Score global', 'value': "score_final"},
                                    {'label': 'Score pollution', 'value': "score_pollution"},
                                    {'label': 'Nombre usines polluantes', 'value': "nb_usines_polluantes"},
                                    {'label': 'Score traitement', 'value': "score_traitement"}
                                    
                                ],
                                value="score_final",
                            ),

                        ]),

                            html.Div([

                            html.H1(children=f'''Nombre de communes ayant un certain nombre d'usines ''',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                            dcc.Graph(
                                id='graph3',
                                figure=histo
                            ), 

                            html.Div(children=f''' On remarque que dans les communes ayant des usines la plus grosse occurence est 4 usines polluantes.
    
                                
                            '''),
                        ]
                        ),
    
#On passe à la carte du potentiel radon 

                        html.Div([

                            html.H1(children=f'Potentiel Radon ',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}),

                            dcc.Graph(
                                id='graph2',
                                figure=carte
                            ), 

                            html.Div(children=f'''
                                Cette carte permet de voir le potentiel radon de chaque commune en France. On peut lier une partie de cette carte avec 
                                celle des massifs montagneux car c'est ici qu'il y a le plus de radon. 
                            '''),
                            html.Br(),
                        ]
                        ),

                        

    ])

    #Ici on va gérer la mise a jour de l'histogramme quand on veut changer ce qui est affiché
    #Notre seul sortie est donc l'histogramme et nous avons 2 entrées une pour le nombre de communes et l'autre pour choisir le score à afficher
    @app.callback(
            Output(component_id='graph1', component_property='figure'), 
            [Input(component_id='nb_input', component_property='value'), 
            Input(component_id='comparatif', component_property='value')]  
        )

    #On met ensuite à jour notre histogramme avec les valeurs récupérées
    def update_figure(input_value,value):


        data = df_finale[df_finale[value].isin( df_finale[value].nlargest(input_value))][['commune',value]]
        data = data.sort_values('commune')
        return px.bar(data, x="commune", y=value,labels = {"score_final":"Score global de dangerosité"})

    #On lance le serveur
    app.run_server()


