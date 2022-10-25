from cmath import nan
import pandas as pd
import numpy as np


df_insee = pd.read_csv(r"C:\Users\cleth\Desktop\correspondance-code-insee-code-postal.csv",sep=';')
df_etab = pd.read_csv(r"C:\Users\cleth\Desktop\2020\2020\etablissements.csv",sep=';')



# #On renomme la colonne comunne pour qu'ils puissent se fusionner
df_insee = df_insee.rename(columns={"Code Postal":"code_postal", "Commune":"commune"})


#df_insee['code_postal'] = df_insee['code_postal'].apply(lambda z : z if len(z) == 5 | len(z) == 4 else z[0:4])
df_insee['code_postal'] = df_insee['code_postal'].apply(lambda z :"0" + z if len(z) == 4 else z)
df_insee['code_postal'] = df_insee['code_postal'].apply(lambda z : z.split("/")[0])


df_etab['code_postal'] = df_etab['code_postal'].apply(str)
df_etab['code_postal'] = df_etab['code_postal'].apply(lambda z : z.split("/")[0])
df_etab['code_postal'] = df_etab['code_postal'].apply(lambda z :"0" + z if len(z) == 4 else z)

#df_insee = df_insee.rename(columns={"code_postal":"code_postal_", "commune":"commune_"})


df_insee['code_postal'] = df_insee['code_postal'].astype(str)
df_etab['code_postal'] = df_etab['code_postal'].astype(str)

df_insee.reset_index(drop=True)
df_etab.reset_index(drop=True)

df_etab['commune'] = df_etab['commune'].apply(lambda z : str(z).split("/")[0])

df_insee['commune'] = df_insee['commune'].str.upper()
df_etab['commune'] = df_etab['commune'].str.upper()



df_etab['commune'] = df_etab['commune'].apply(lambda z: str(z).replace(' ','-'))
df_insee['commune'] = df_insee['commune'].apply(lambda z: str(z).replace(' ','-'))

df_etab['commune'] = df_etab['commune'].apply(lambda z: str(z).replace('-','_'))
df_insee['commune'] = df_insee['commune'].apply(lambda z: str(z).replace('-','_'))

#print(df_insee['code_postal_'], df_etab['code_postal'])
# g = np.intersect1d(df_insee['code_postal_'], df_etab['code_postal'])
# print(len(g))

# #On fusionne deux tables selon la commune pour avoir le code INSEE des usines 
# df_new = df_etab[['code_postal', 'commune']].merge(df_insee[['code_postal_', 'commune_', 'Code INSEE']], )
df_new = pd.merge(df_etab,df_insee, how='left', left_on=['commune','code_postal'], right_on=['commune','code_postal'] )


#print(df_new['commune'])
# print(np.where(df_new['commune'].isna())[0])
# print(np.where(df_new['code_postal'].isna())[0])
# print(np.where(df_new['Code INSEE'].isna())[0])

# print(df_new['code_postal_'])
# print(np.where(df_new['code_postal_'] == "92036"))

#print(list(df_new.columns))


# print(df_new['code_postal'].equals(df_new['code_postal_']))

#print(df_new['code_postal'])

#print(df_new['code_postal'].value_counts(dropna=False))



# fichier = open("salete.txt", "a")

# for i in range(len(df_insee['Code INSEE'])):
#      fichier.write("\n" + str(i) + ":" + " " + df_insee['Code INSEE'][i])
    
# fichier.close()

# fichier = open("cp1.txt", "a")

# for i in range(len(df_etab['code_postal'])):
#      fichier.write("\n" + str(i) + ":" + " " + df_etab['code_postal'][i])
    
# fichier.close()


# fichier = open("cp2.txt", "a")

# for i in range(len(df_insee['code_postal'])):
#      fichier.write("\n" + str(i) + ":" + " " + df_insee['code_postal'][i])
    
# fichier.close()


print(len(np.where(df_new['Code INSEE'].isna())[0]))

# print(df_new.loc[[0]]['code_postal'])
# print(df_new.loc[[0]]['commune'])
# print(df_new.loc[[0]]['Code INSEE'])

# fichier = open("machin.txt", "a")

# for i in range(len(df_etab['commune'])):
#     fichier.write("\n" + df_etab['commune'][i])
    
# fichier.close()


# fichier = open("truc.txt", "a")

# for i in range(len(df_insee['commune'])):
#     fichier.write("\n" + df_insee['commune'][i])
    
# fichier.close()


# print(df_new['Code Arrondissement'])
# print(df_insee['Code Arrondissement'].isnull().sum().sum())
# print(df_new['Code Arrondissement'].isnull().sum().sum())
# #Nettoyage de la nouvelle table (on vire les colonnes qui servent à rien)
# a = a.drop(columns=['numero_siret','code_epsg','code_ape','code_eprtr','libelle_eprtr'])

# #print(len(list(a.columns)))

# #On vérifie le nombre de données manquantes et on cherche le nombre de données uniques
# #print(a['libelle_ape'].isnull().sum().sum())
# #print(a['libelle_ape'].nunique())

# #On a pas besoin du code postal et ce département fait des trucs chelous
# a = a.drop(columns=['code_postal','Code Postal','Département','Région'])



#Comme on a geo_point_2d pas besoin des coordonées x et y et geo_shape sert  rien
# a = a.drop(columns=['coordonnees_x','coordonnees_y','geo_shape','ID Geofla'])

# print(list(a.columns))




















