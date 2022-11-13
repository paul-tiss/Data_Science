import creation_dataframe
import dashboard
import simplification_geojson


exec('creation_dataframe.py')
exec('dashboard.py')

#Si on veut tester la simplification il faut télécharger le fichier datagouv-communes.geojson qui se trouve dans le read me et décommenter
#exec('simplification_geojson.py')
