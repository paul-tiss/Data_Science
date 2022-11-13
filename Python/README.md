# Dangerosité industrielle et potentiel radon des communes en France

Notre objectif pour ce projet est de calculer un indice de dangerosité industrielle pour chaque commune en France, à ceci nous ajoutons le potentiel radon qui donne une indication sur la dangerosité de la commune. En partant de plusieurs jeux de données comprenant notamment les usines en France, le potentiel radon, les emissions de ces usines, le nombre de dechets traités... nous allons calculer un score prenant en compte tout ces éléments.   

### User guide
## Getting Started


$ git clone https://github.com/paul-tiss/Data_Science.git Ce lien donne accès à nos projets de R et python. Il faut donc ouvrir le dossier Data_Science puis ouvrir le dossier Python pour accéder aux fichiers. Une fois le fichier télécharger il faut se placer dans ce dossier avec le terminal pour lancer les programmes. Tous les packages necessaire sont renseigné dans le requirement.txt 

## Informations

Notre projet est divisé en trois programmes. Le premier "creation_dataframe.py" permet à partir de plusieurs dataframe de créer un dataframe final qui sera utilisé pour le dashboard. Il faut noter que la façon dont les codes sont obtenus est expliquée en détail dans les commentaires du code. Par soucis de simplicité cette dataframe finale est déjà présente dans le répertoire.

Le second programme "simplification_geojson.py" permet de simplifier le geojson. En effet, Git ne veut pas de fichiers >50Mo or les fichiers geojson sont plus lourd que ça. Il faut donc les telecharger aux adresses suivantes. A noter que commune_light est une version simplifiée de datagouv-communes. La présence de ce dernier fichier est uniquement utile pour le test du programme de simplification. Mais le dashboard prendra automatiquement communes_light.

datagouv-communes.geojson: https://drive.google.com/file/d/1bf4ITZwitC0YTaA7NaB9VfTrExp8H3al/view?usp=share_link
communes_light.geojson: https://drive.google.com/file/d/1eoXrfaMcUMS2Ss7lU6DjWihcSxudHil7/view?usp=share_link

Et finalement le troisième programme dashboard.py permet de lancer le dahsboard. Il prendra automatiquement la table finale et le geojson simplifié.


## Dashboard

Il faut noter que le dashboard peut prendre une certain temps à se charger en fonction de la puissance de l'ordinateur. 

### Developper guide

## Architecture du code 

![image](https://user-images.githubusercontent.com/116153375/201546932-26a98c64-b703-4fde-bf3b-38dbfb9cae4d.png)

## Copyright

Nous déclarons sur l'honneur avoir produit notre code entiérement par nous même. Les seules ressources utilisées proviennent du cours et des help pour savoir comment utiliser certaines fonctions.






