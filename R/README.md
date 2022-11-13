# Dangerosité industrielle et potentiel radon des communes en France
## Thiveyrat Clément / Tissedre Paul

### Description

Notre objectif pour ce projet est de calculer un indice de dangerosité industrielle pour chaque commune en France, à ceci nous ajoutons le potentiel radon qui donne une indication sur la dangerosité de la commune. En partant de plusieurs jeux de données comprenant notamment les usines en France, le potentiel radon, les emissions de ces usines, le nombre de dechets traités... nous allons calculer un score prenant en compte tout ces éléments.

# User Guide

## Getting Started
$ git clone [https://github.com/paul-tiss/Data_Science/tree/main/R ](https://github.com/paul-tiss/Data_Science.git)
Ce lien donne accès à nos projets de R et python. Il faut donc ouvrir le dossier R puis ouvrir le document "app.R" et appuyer sur "Run App" après avoir installé les packages mentionés ci-dessus. La liste des packages additionels ce trouve dans requirements.txt (ils sont au nombre de 6).


### Utilisation

L'utilisateur a à sa disposition un dashboard disposant de 3 onglets: Bar Plot, Carte et Histogramme. Dans bar plot, on peut observer 3 Bar Plot qui affiche le score de traitement, le score final et le score de polution. Le score de polution et un score que nous avons calculé nous-même à partir de différentes données telles que les rejets des usines, la polutions de l'air, etc. Le score de traitment est un ratio entre le nombre de déchets reçus par certaines usines et le nombre de déchets traités. Enfin le score final est lui aussi un score calculé à partir de toutes nos données précedentes. Les calculs décris précedement sont tous décris dans notre projet python. Le deuxième onglet donne accès à une carte qui affiche le nombre d'usines par communes lorsque l'on passe notre souris dessus et qui catégorise les communes avec des cercles et différentes couleurs en fonction du nombre d'usines qu'elles possèdent. La valeur du nombre d'usine à été mis sous une racine carré afin de rendre notre carte plus lisible. Il est important de noté que l'ouverture de la carte provoque un warning car certaines valeures ne sont pas dans la palette de couleur. Ce warning est volontaire car nous ne voulions pas colorier les communes ne possédant pas d'usine. Cela permet d'obtenir une carte plus aérée. Le dernier onglet donne accès à notre histogramme qui affiche le nombre de communes qui possèdent un nombre d'usines équivalent aux abscisse. Nous avons aussi ajouter un slider qui permet de modifier la première valeure des abcisses. Comme l'histogramme s'adapte automatiquement au niveau de la taille, cela permet d'etre plus précis lorsque l'on mannipule des données plus élevé.


### Sample Tests

Explain what these tests test and why

    Give an example

### Style test

Checks if the best practices and the right coding style has been used.

    Give an example

## Deployment

Add additional notes to deploy this on a live system

## Built With

  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used
    for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose
    the license

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/PurpleBooth/a-good-readme-template/tags).

## Authors

  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)

See also the list of
[contributors](https://github.com/PurpleBooth/a-good-readme-template/contributors)
who participated in this project.

## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - Hat tip to anyone whose code is used
  - Inspiration
  - etc
