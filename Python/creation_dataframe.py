import pandas as pd
import numpy as np


#On ouvre les csv
df_insee = pd.read_csv("correspondance-code-insee-code-postal.csv",sep=';')
df_etab = pd.read_csv(r"etablissements.csv",sep=';')


#On retire les colonnes inutiles
df_insee = df_insee.drop(columns = ['Statut','geo_shape','ID Geofla','Code Canton','Code Arrondissement','Altitude Moyenne'])
df_etab = df_etab.drop(columns = ['numero_siret','adresse','coordonnees_x','coordonnees_y','code_epsg','code_ape','code_eprtr','libelle_eprtr'])

#Concernant les doublons type region/département on regarde si la liste contient des NaN et si 0 alors on garde celle de Etab

#print(len(np.where(df_etab['departement'].isna())[0]))
#print(len(np.where(df_etab['region'].isna())[0]))

df_insee = df_insee.drop(columns = ['Département','Région'])

#On affiche les colonnes qui ont survécues 

#print(list(df_etab.columns))
#print(list(df_insee.columns))

#Concernant les codes commune/departement de la table Insee on garde pour l'instant mais ça peut être retiré si pas besoin 
#(potentiellement un lien + tard)


#On renomme les colonnes commune code postal pour simplifier la fusion
df_insee = df_insee.rename(columns={"Code Postal":"code_postal", "Commune":"commune"})

#traitements sur les données pour tout uniformiser
#Ici on rajoute un 0 pour les codes postal qui doivent commencer par un 0 et qui a été effacé car c'est un int
df_insee['code_postal'] = df_insee['code_postal'].apply(lambda z :"0" + z if len(z) == 4 else z)
#Des fois il y a plusieurs code postaux par ligne. On garde donc uniquement le premier
df_insee['code_postal'] = df_insee['code_postal'].apply(lambda z : z.split("/")[0])


df_etab['code_postal'] = df_etab['code_postal'].apply(str)
df_etab['code_postal'] = df_etab['code_postal'].apply(lambda z : z.split("/")[0])
df_etab['code_postal'] = df_etab['code_postal'].apply(lambda z :"0" + z if len(z) == 4 else z)


#On passe les noms en majuscule pour avoir plus de correspondance 
df_insee['commune'] = df_insee['commune'].str.upper()
df_etab['commune'] = df_etab['commune'].str.upper()

#On change tous les espaces en - puis en _ afin d'etre sur que tout est écrit de la même manière
df_etab['commune'] = df_etab['commune'].apply(lambda z: str(z).replace(' ','-'))
df_insee['commune'] = df_insee['commune'].apply(lambda z: str(z).replace(' ','-'))
df_etab['commune'] = df_etab['commune'].apply(lambda z: str(z).replace('-','_'))
df_insee['commune'] = df_insee['commune'].apply(lambda z: str(z).replace('-','_'))



#On fusionne deux tables selon la commune et le code postal pour avoir le code INSEE des usines. 
#Tout en évitant différentes communes qui ont le même code postal

df_new = pd.merge(df_etab,df_insee, how='left', left_on=['commune','code_postal'], right_on=['commune','code_postal'] )

#On affiche le nombre Nan qu'on a pour le code Insee (696 ici)

#print(np.where(df_new['Code INSEE'].isna())[0])

#Il y a 7% de données manquantes, nous allons donc essayer de faire baisser ce chiffre

#On récupére les lignes avec un code Insee vide
insee_vide = df_new[df_new['Code INSEE'].isna()]

#On fusionne ces lignes avec la tab insee sur le nom de la commune 
insee_vide = pd.merge(insee_vide,df_insee,how='left',on =['commune'])


#Les x correspondent aux données naze de la table d'avant donc ça dégage 
insee_vide = insee_vide.drop(columns = list(insee_vide.filter(regex='_x',axis=1)))

#On vire aussi les _y qui du coup ne servent à rien
insee_vide.columns = insee_vide.columns.str.rstrip('_y')

#print(list(insee_vide.columns))
#print(list(df_new.columns))

#On remarque qu'il y a plus d'élements dans insee_vide que le nombre de données manquantes de notre table de base
#On supprime donc les données dupliquées en focntion de l'identifiant de l'usine qui est présumé unique

insee_vide = insee_vide.drop_duplicates(subset='identifiant')

#Après nos manipulations on tombe à 0.7% de NaN

#print(len(np.where(insee_vide['Code INSEE'].isna())[0]))

#On remarque que les colonnes ne sont plus rangées dans le bon ordre
new_col = ['identifiant', 'nom_etablissement', 'code_postal','commune', 'departement', 'region', 'libelle_ape', 'Code INSEE', 'Superficie', 'Population', 'geo_point_2d', 'Code Commune', 'Code Département', 'Code Région']
insee_vide = insee_vide.reindex(columns = new_col)

#On retire les valeurs manquantes de l'ancienne table 
df_new = df_new.dropna(subset='Code INSEE')
#On ajoute la table avec moins de NaN à notre table originale
df_new = pd.concat([df_new,insee_vide], ignore_index = True)

#On a bien ici encore 72 données manquantes

#print(len(np.where(df_new['Code INSEE'].isna())[0]))


#On va donc répéter l'opération précédente mais cette fois-ci sur le code postal


insee_vide2 = df_new[df_new['Code INSEE'].isna()]
insee_vide2 = pd.merge(insee_vide2,df_etab[['commune','code_postal']],how='left',on =['commune'])
insee_vide2 = insee_vide2.drop_duplicates(subset='identifiant')
insee_vide2 = insee_vide2.rename(columns={"code_postal_y":"code_postal"})
insee_vide2 = pd.merge(insee_vide2,df_insee,how='left',on =['code_postal'])
insee_vide2 = insee_vide2.drop_duplicates(subset='identifiant')
insee_vide2 = insee_vide2.drop(columns = list(insee_vide2.filter(regex='_x',axis=1)))
insee_vide2.columns = insee_vide2.columns.str.rstrip('_y')
new_col = ['identifiant', 'nom_etablissement', 'code_postal','commune', 'departement', 'region', 'libelle_ape', 'Code INSEE', 'Superficie', 'Population', 'geo_point_2d', 'Code Commune', 'Code Département', 'Code Région']
insee_vide2 = insee_vide2.reindex(columns = new_col)

#On ajoute ce que l'on vient de faire à notre table
df_new = df_new.dropna(subset='Code INSEE')
df_new = pd.concat([df_new,insee_vide2], ignore_index = True)

#On a plus que 9 données manquantes qu'on va donc supprimer

#print(len(np.where(df_new['Code INSEE'].isna())[0]))
df_new = df_new.dropna(subset='Code INSEE')

#On uniformise les noms de colonnes
df_new = df_new.rename(columns={"Code INSEE":"code_insee", "Superficie":"superficie","Population":"population","Code Commune":"code_commune","Code Département":"code_departement","Code Région":"code_region"})

#On vérifie ensuite que l'on a bien des identifiants différents partout 

#print(df_new['identifiant'].nunique())



#--------------------------------------------------------------------------------------------
#Création de la table finale
#--------------------------------------------------------------------------------------------

#On récupére la table insee pour avoir une liste de toutes les communes de france
df_finale = df_insee
df_finale = df_finale.rename(columns={"Code INSEE":"code_insee", "Superficie":"superficie","Population":"population","Code Commune":"code_commune","Code Département":"code_departement","Code Région":"code_region"})


#--------------------------------------------------------------------------------------------
#On passe maintenant au radon
#--------------------------------------------------------------------------------------------

df_radon = pd.read_csv(r"radon.csv",sep=';')

df_radon = df_radon.drop(columns = ['nom_dept','reg'])
df_radon = df_radon.rename(columns={"insee_com":"code_insee","nom_comm":"commune"})
df_radon['commune'] = df_radon['commune'].str.upper()
df_radon['commune'] = df_radon['commune'].apply(lambda z: str(z).replace(' ','-'))
df_radon['commune'] = df_radon['commune'].apply(lambda z: str(z).replace('-','_'))


df_finale = pd.merge(df_finale,df_radon[['classe_potentiel','code_insee']],how='left',on =['code_insee'])
#On remplace les données manquantes par des 1 qui correspond au potentiel le plus faible et le plus courant (afin de ne pas fausser les valeurs)
df_finale['classe_potentiel'] = df_finale['classe_potentiel'].fillna(1)

# radon_vide = df_finale[df_finale['classe_potentiel'].isna()]
# radon_vide = pd.merge(radon_vide,df_radon,how='left',on=['commune'])
# radon_vide = radon_vide.drop(columns = list(radon_vide.filter(regex='_x',axis=1)))
# radon_vide.columns = radon_vide.columns.str.rstrip('_y')
# radon_vide = radon_vide.drop_duplicates(subset='code_insee')

# df_finale = df_finale.dropna(subset='classe_potentiel')
# df_finale = pd.concat([df_finale,radon_vide], ignore_index = True)


# print(df_finale['code_insee'].nunique())
# df_finale = df_finale.drop_duplicates(subset='code_insee')

# print(len(np.where(df_finale['classe_potentiel'].isna())[0]))
# print(len(df_finale))
# print(df_finale['code_insee'].nunique())




#--------------------------------------------------------------------------------------------
#On passe maintenant aux émissions
#--------------------------------------------------------------------------------------------

df_emission= pd.read_csv(r"emissions.csv",sep=';')


#On vérifie si toutes les données sont sur la même année et si les unités sont identiques afin de pouvoir les supprimer si jamais

#print(df_emission['unite'].nunique())
#print(df_emission['annee_emission'].nunique())

df_emission = df_emission.drop(columns = ['unite','annee_emission'])

#On crée une colonne score qui permettra de stocker le score emission de chaque commune
df_emission['score'] = np.arange(df_emission.shape[0])

#On crée une DF avec tous les différents polluants
df_score = pd.DataFrame(list(df_emission['polluant'].unique()))

#On y associe ensuite une valeur entre 1 et 3 que l'on trouve ainsi. 1: Le produit est peu dangereux. 3:Le produit est interdit par la 
#France ou par l'UE et enfin 2: le reste 
#Afin de trouver ces valeurs nous avons fait des recherches sur CHAQUE polluant afin de déterminer son score 

df_score['score'] = [3, 3, 2, 2,  2, 2,  2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 3, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 3, 3, 2, 2, 3, 2, 1, 1, 2, 2, 2, 3, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 3, 2, 2, 1, 2, 1, 3, 3, 2, 2, 1, 2, 3, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1, 2, 1, 2, 2, 1]

#On isole ensuite les elements en fonction de leur score
tab_1 = df_score[df_score['score'] == 1 ]
tab_2 = df_score[df_score['score'] == 2 ]

#On remplace chaque element par son score dans la grande table
tab_polluant = df_emission['polluant']
tab_polluant = tab_polluant.apply(lambda z: 1 if tab_1.isin([z]).any().any() else 2 if tab_2.isin([z]).any().any() else 3)

# Ici on associe un score a chaque milieu de pollution selon la logique suivante eau(indirecte) < eau(directe) < sol < air
tab_milieu = df_emission['milieu'] 
tab_milieu = tab_milieu.apply(lambda z: 1 if z == "Eau (indirect)" else 1.2 if z =="Eau (direct)" else 1.5 if z == "Sol" else 2)


#On vérifie la longeur des colonnes avant de d'y faire des opérations

#print(len(df_emission['score']),len(df_emission['quantite']),len(tab_test),len(tab_milieu))

#On multiplie les colonnes pour avoir un score emission selon la formule suivante quantite*type de polluant*millieu
df_temp = df_emission['score'].apply(lambda z: df_emission['quantite'][z] * tab_polluant[z] * tab_milieu[z])

#Finalement on remplis notre colonne score dans la DF emission
df_emission['score'] = df_temp

#On fusionne ensuite les deux DF selon l'identifiant
df_new = pd.merge(df_new,df_emission,how='left',on=['identifiant'])
df_new = df_new.drop_duplicates(subset='identifiant')

#On nettois les noms de colonne
df_new = df_new.drop(columns = list(df_new.filter(regex='_y',axis=1)))
df_new.columns = df_new.columns.str.rstrip('_x')

#Pour les usines sans score pollution on ajoute des 1
df_new['score'] = df_new['score'].fillna(1)




#--------------------------------------------------------------------------------------------
#On passe maintenant à la production de dechets dangereux 
#--------------------------------------------------------------------------------------------

df_dechet= pd.read_csv(r"Prod_dechets_dangereux.csv",sep=';')


#On cherche le nombre d'occurence de chaque indentifiant pour voir les usines qui produisent le plus de dechets
df_dechet['nb'] = df_dechet.groupby('identifiant')['identifiant'].transform('count')
df_dechet = df_dechet.drop_duplicates(subset='identifiant')
#On garde seulement les colonnes qui nous intéressent 
df_dechet = df_dechet[['identifiant','nb']]

#On ajoute ces informations à notre DF et on change les NaN en 0
df_new = pd.merge(df_new,df_dechet,how='left',on='identifiant')
df_new['nb'] = df_new['nb'].fillna(0)

#On renomme des colonnes par soucis de lisibilité
df_new = df_new.rename(columns={'score':'score_pollution','nb':'nb_usines_polluantes'})



#--------------------------------------------------------------------------------------------
#On passe maintenant au traitement de déchets dangereux
#--------------------------------------------------------------------------------------------


df_traitement= pd.read_csv(r"Trait_dechets_dangereux.csv",sep=';')

#On vérifie que les deux colonnes quantité ne comportent pas de NaN

# print(len(np.where(df_traitement['quantite_admise'].isna())[0]))
# print(len(np.where(df_traitement['quantite_traitee'].isna())[0]))

#On ne prend que les colonnes dont on a besoin
df_traitement = df_traitement[['quantite_admise','quantite_traitee','identifiant']]
#On calcule un ratio entre les deux
df_traitement['ratio'] = df_traitement['quantite_admise'] / df_traitement['quantite_traitee']
#On arrondis la valeur car une grosse précision est inutile et cela fait moins de valeurs uniques 
df_traitement['ratio'] = round(df_traitement['ratio'],0)

#On remplace les inf par 50000 car le score le plus haut est de 37000 donc on asismile l'infini à un plus gros score
df_traitement = df_traitement.replace(np.inf,50000)
#On remplace les Nan par un score de 1 qui est un score neutre
df_traitement['ratio'] = df_traitement['ratio'].fillna(1)

#On récupére tous les identifiants uniques
df_ident = pd.DataFrame(df_traitement['identifiant'].unique())
df_ident = df_ident.rename(columns = {0:'identifiant'})
#On crée une colonne score 
df_ident['somme_score'] = np.arange(df_ident.shape[0])

#On calcul le score d'un identifiant en sommant tout ses scores 
df_ident['somme_score'] = df_ident['somme_score'].apply(lambda z: sum(df_traitement['ratio'][df_traitement['identifiant'] == df_ident['identifiant'][z]]))


#On ajoute nos scores à la base de données des usines 
df_new = pd.merge(df_new,df_ident,how='left',on='identifiant')


df_new = df_new.rename(columns={'somme_score':'score_traitement'})
#On ajoute des 0 pour les identifiants sans score
df_new['score_traitement'] = df_new['score_traitement'].fillna(0)

#On fusionne enfin notre table usine avec notre table finale
df_finale = pd.merge(df_finale,df_new,how='left',on='code_insee')

df_finale = df_finale.drop_duplicates(subset='code_insee')
df_finale = df_finale.drop(columns = list(df_finale.filter(regex='_y',axis=1)))
df_finale.columns = df_finale.columns.str.rstrip('_x')

#On va ensuite vérifier combien de NaN il y a par colonne et on va les traiter une par une

#print(df_finale.isna().sum())

#On peut laisser les strings comme le nom de l''établissement en NaN car elles ne sont la qu'a titre indicatif
#Pour l'indentifiant on le laisse également en Nan car dans certaines communes il n'y a pas d'usines
#Finalement on va simplement remplir avec des 0 les cellules des commosantes qui nous permettrons de calculer le score de chaque commmune
#Ainsi que la colonne quantite qui pourra servir plus tard
df_finale['quantite'] = df_finale['quantite'].fillna(0)
df_finale['score_pollution'] = df_finale['score_pollution'].fillna(0)
df_finale['nb_usines_polluantes'] = df_finale['nb_usines_polluantes'].fillna(0)
df_finale['score_traitement'] = df_finale['score_traitement'].fillna(0)


#On crée une fonction afin de pouvoir observer tous les scores différents et ceci dans le but d'avoir une idée des ordres de grandeur
#Cette manipulation est importante car elle va permettre de créer l'équation du score finale en donnant plus ou moins de poids à chaque score

def print_values_score(df_tempo):
    print("\n",df_tempo.name)
    print(np.sort(df_tempo.unique()))
    print("\n")

#Afin de faciliter la compréhension voici la signification de ces valeurs

#Pour le score pollution, un score plus élevé indique un endroit plus pollué
#print_values_score(df_finale['score_pollution'])
#Pour le nombre d'usines polluantes plus il y en a plus c'est dangereux
#print_values_score(df_finale['nb_usines_polluantes'])
#Pour la classe_potententiel, on s'attarde ici sur le potentiel radon. Il est situé entre 1 et 3 avec 3 le potentiel le plus élevé donc le +dangereux
#print_values_score(df_finale['classe_potentiel'])
#Et finalement pour le score traitement plus le chiffre est bas plus l'usine a traitée de dechets dangereux
#print_values_score(df_finale['score_traitement'])


df_finale['score_final'] = np.arange(df_finale.shape[0])

#On uniformise les echelles et on y applique un multiplicateur en fonction de l'importance de chaque score
df_finale['score_pollution'] = 5*(df_finale['score_pollution']/100000000)
df_finale['nb_usines_polluantes'] = 3*(df_finale['nb_usines_polluantes']/10)
df_finale['score_traitement'] = 3*(df_finale['score_traitement']/1000000)

#On calcule le score final, on notera que plus le score est élevé plus la commune est dangereuse 
df_finale['score_final'] = df_finale['score_pollution'] + df_finale['nb_usines_polluantes'] + df_finale['score_traitement'] + df_finale['classe_potentiel']

df_finale = df_finale.drop(columns = ['code_commune','code_departement','code_region','nom_etablissement','libelle_ape'])


#On remarque que certaines villes sont découpées en arrondissement et chaque arrondissement est enregistré comme une commune
#Or ce n'est pas le cas dans les geojson ce qui va nous poser probleme pour les cartes


#On crée une fonction qui va simplifier la fusion des arrondissements en une seule ville 
def fusion_arrondissement(data,ville,code_insee,code_postal):

    data['commune'] = ville
    data['code_insee'] = str(code_insee)
    data['code_postal'] = code_postal
    data['superficie'] = data['superficie'].sum()
    data['population'] = data['population'].sum()
    data['classe_potentiel'] = round(data['classe_potentiel'].sum()/len(data['classe_potentiel']))
    data['quantite'] = data['quantite'].sum()
    data['score_pollution'] = data['score_pollution'].sum()
    data['nb_usines_polluantes'] = data['nb_usines_polluantes'].sum()
    data['score_traitement'] = data['score_traitement'].sum()
    data['score_final'] = data['score_final'].sum()

    return data.loc[[0]]


#Paris
temp = df_finale[df_finale["commune"].str.startswith("PARIS_")]
temp = temp.drop(temp.index[[11]])
temp = temp.reset_index()
index1 = temp['index']
temp = temp.drop(columns = ['index'])
df_finale = df_finale.drop(index1)
df_finale = pd.concat([df_finale,fusion_arrondissement(temp,"PARIS",75056,75000)])
df_finale = df_finale.reset_index()
df_finale = df_finale.drop(columns = ['index'])


#Marseille
temp = df_finale[df_finale["commune"].str.startswith("MARSEILLE_")]
temp = temp.drop(temp.index[[9]])
temp = temp.reset_index()
index1 = temp['index']
temp = temp.drop(columns = ['index'])
df_finale = df_finale.drop(index1)
df_finale = pd.concat([df_finale,fusion_arrondissement(temp,"MARSEILLE",13055,13000)])
df_finale = df_finale.reset_index()
df_finale = df_finale.drop(columns = ['index'])


#Lyon
temp = df_finale[df_finale["commune"].str.startswith("LYON_")]
temp = temp.reset_index()
index1 = temp['index']
temp = temp.drop(columns = ['index'])
df_finale = df_finale.drop(index1)
df_finale = pd.concat([df_finale,fusion_arrondissement(temp,"LYON",69123,69000)])
df_finale = df_finale.reset_index()
df_finale = df_finale.drop(columns = ['index'])

#On enleve les dom tom
df_finale = df_finale[df_finale["code_postal"].astype('int') < 97000]
df_finale = df_finale.reset_index()
df_finale = df_finale.drop(columns = ['index'])

#On sépare la colonne geo_point en deux colonnes latitude et longitude

df_finale['lat'] = np.arange(df_finale.shape[0])
df_finale['long'] = np.arange(df_finale.shape[0])

df_finale['lat'] = df_finale['lat'].apply(lambda z: df_finale['geo_point_2d'][z].split(',')[0] )
df_finale['long'] = df_finale['long'].apply(lambda v: df_finale['geo_point_2d'][v].split(',')[1])

df_finale = df_finale.drop(columns = ['geo_point_2d'])

df_finale.to_csv('table_finale.csv',encoding='utf-8', index=False,sep=';')


  





















