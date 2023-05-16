# INFO841_Projet

## Auteures
JENNY Camille (<a href="https://github.com/camille-jenny">GitHub</a>)<br>
LÉGLISE Cloé (<a href="https://github.com/SalsyUniate">GitHub</a>)
<br><br>

## Objectif du projet
Ce projet, réalisé dans un cadre scolaire, a pour but d'implémenter un proxy pour un navigateur web.
Celui-ci utilise l'algorithme RSA pour chiffrer les requêtes http ainsi que les réponses provennant des serveurs web. Afin d'éviter la barrière du langage et pour se focaliser sur les notions, nous avons choisi Python (3.10) pour l'implémentation. Nous utilisons Pylint (2.12) pour vérifier la qualité du code et éliminer les "code smells".<br><br>

## Installation
### Installation des dépendances
Il est recommandé d'utiliser <b>Python 3.10</b> pour exécuter ce projet. Les versions antérieures de Python n'ont pas été testées. 

Installez toutes les librairies utilisées avec la commande :
```
pip install -r requirements.txt
```

### Paramètrage du navigateur web
Ouvrez ensuite un navigateur web et configurez le pour rediriger les requêtes vers un proxy. Le proxy étant implémenté localement, entrez <b>localhost</b> et séléctionnez un port disponible (par défaut il s'agit du <b>5454</b>, vous pouvez modifier sa valeur dans le fichier <i>constants</i>, constante SOCKET_IN).

Vous pouvez vérifier que les autres ports soient également disponibles. Dans le cas contraires, vous pouvez toujours modifier les valeurs des constantes dans le fichier <i>constants</i>.
<br><br>

## Exécution
### Méthode 1 : en ligne de commande
Pour lancer le projet, exécutez à la racine du projet :
```
./start.sh
```

### Méthode 2 : manuellement
Vous pouvez lancer manuellement les deux serveurs dans deux terminaux différents.<br>
<b>Attention</b> : Vous devez commencer par allumer le serveur côté web !<br><br>


## Fonctionnalités
wip...<br><br>

## Evaluation
### Généralisation à tous les sites
wip...<br><br>

### Vitesse d'execution
wip...<br><br>

## Remerciements 
wip...<br><br>

## Licence
wip...<br><br>
