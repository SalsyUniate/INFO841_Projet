# INFO841_Projet

## Auteures
JENNY Camille (<a href="https://github.com/camille-jenny">GitHub</a>)<br>
LÉGLISE Cloé (<a href="https://github.com/SalsyUniate">GitHub</a>)
<br><br>

## Objectif du projet
Ce projet, réalisé dans un cadre scolaire, a pour but d'implémenter un proxy pour un navigateur web.
Celui-ci utilise l'algorithme RSA pour chiffrer les requêtes http ainsi que les réponses provennant des serveurs web. Ce proxy ne permets pas de traiter des requêtes de type https. Afin d'éviter la barrière du langage et pour se focaliser sur les notions, nous avons choisi Python (3.10) pour l'implémentation. Nous utilisons Pylint (2.12) pour vérifier la qualité du code et éliminer les "code smells".<br><br>

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
Ce programme permet de lancer deux serveurs de proxy en local. Lors de l'initialisation, les deux serveurs génèrent une paire de clés RSA et se les échangent pour pouvoir communiquer de manière sécurisée.<br>
Le protocole d'échange des clés est le suivant : le proxy côté client envoie en premier sa clé publique, puis, une fois réceptionné par le proxy côté web, ce dernier envoie immédiatement sa propre clé publique. Ensuite, les deux serveurs traitent les données reçues pour les transformer en objet de type <i>rsa.PublicKey</i>.<br>

Une fois que les clés ont étés échangés, les deux serveurs affichent 'Server up !' et sont désormais en attente de requêtes à traiter. C'est le proxy côté client qui reçoit les requêtes, les crypte pour les envoyer au côté web. Ce dernier décrypte la requête, la fait parvenir au server web et crypte la réponse pour la renvoier au côté client. Enfin, le proxy client décrtpte la réponse reçue et la fait parvenir au navigateur web.
<br>

Pour chaque requête reçue (côté client comme côté web), un nouveau thread est créé pour gérer la requête, ce qui permets aux serveurs de ne pas être bloqué par une requête et d'en traiter plusieurs simultanément.<br>

Enfin, le code génère deux fichiers de log pour permettre d'évaluer les performances de temps de notre proxy. Ces fichiers sont générés dans un dossier log qui est effacé et recréé à chaque nouvelle exécution.<br><br>

## Evaluation
### Généralisation à tous les sites
Nous avons constaté que notre proxy est plutôt spécifique à la page web de test, qui est http://info.cern.ch/. Nous avons essayé de chercher d'autres pages pour tester notre code mais nous n'en avons pas trouvé beaucoup. Nous avons notamment essayé de faire fonctionner le proxy sur le site http://neverssl.com mais sans succès.<br>

Cela dit, notre proxy fonctionne très bien sur la page de test. Cela signifie que les bases sont là et que le principe fontionne.<br><br>

### Vitesse d'execution
Comme expliqué dans la partie fonctionnalités, des fichiers de log sont générés pour avoit une idée du temps mis par la proxy pour retourner la réponse au navigateur. Il s'avère que pour la page de test (page textuelle de petite taille), la réponse est renvoyée en 0.1 seconde en moyenne ce qui ne nous semble pas mal. Nous n'avons pas d'idées sur le temps que mettrait notre proxy pour des pages plus grosse ou alors pour les images ou éléments plus volumineux (cela vient du fait que nous n'avons pas d'autres pages http à disposition pour faire les tests necéssaires).<br><br>

## Conclusion
Nous sommes très satisfaites du projet. En effet, nous ne savions pas avant de commencer ce qu'était un proxy et n'étions pas très à l'aise avec les sockets en python. Malgré cela, nous avons réussi à réaliser un proxy fonctionnel (même sur une fenêtre restreinte) avec un temps de réponse plutôt correct.<br><br>

## Remerciements 
Nous tenons à remercier Maxime (<a href="https://github.com/TheBigBlase">GitHub</a>) et Valentin (<a href="https://github.com/Onyx39">GitHub</a>) qui nous ont expliqué ce que sont les proxys et qui nous ont aidé à prendre en main les sockets en python.<br><br>

## Licence
Ce code est libre de droits.
