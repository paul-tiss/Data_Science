import json
import math

#On ouvre le geojson concerné
with open("datagouv-communes.geojson", 'r') as f:
    data = json.load(f)


#On va parcourir le json pour enlever des décimales aux coordonées 
for j in range(len(data["features"])):
    for i in range(len(data["features"][j]["geometry"]['coordinates'][0])):
        if(type(data["features"][j]["geometry"]['coordinates'][0][i][0]) == float):
            data["features"][j]["geometry"]['coordinates'][0][i][0] = round(data["features"][j]["geometry"]['coordinates'][0][i][0],6)
            data["features"][j]["geometry"]['coordinates'][0][i][1] = round(data["features"][j]["geometry"]['coordinates'][0][i][1],6) 


#On crée un nouveau fichier geojson 
with open("communes_light.geojson","w") as f:
    json.dump(data, f)



