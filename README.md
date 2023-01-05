# Extreme_SVD_Projet_Option

## Introduction

Ce repo comporte tout notre code produit dans le cadre de notre projet d'option visant établir un benchmark de méthodes SVD out-of-core implémantées en Python.

## TODO 

Scikit learn
- incremental PCA
- memmap

PyParSVD
- regarder autres méthodes

Soutenance
- date : deuxième semaine de la rentrée
- mise en commun de nos portions de code
- produire un benchmark modulaire (possibiliter de rajouter des méthodes simplement)
- produire un executable
- analyse des résultats (notebook)
- résulats visuels (visualisation des données, étude statistique, extraction des caractéristiques)

Supercalculateur
- ligerion.ec-nantes.fr (login : identifiant centrale
- remplir formulaire
- lire documentation calculateur
- nom du projet : projet_PAPY_SVD_2022
- via vpn de l'ecole
- ssh util@login02:~/
- batch slurm (attribution du calcul à un noeud de calcul)
- batch : préciser librairies utilisées (ex: module load python3.10)
- fournir à Lestandi, la liste de toutes les bibliothèques utilisées

Datasets
- equation de la chaleur
- données atmosphérique, thermodynamique
- matrice réelle (coefficients uniformément répartis sur [-1,1] ou [0,1])

test_paul.py et test_simple_paul.py nécessite d'installer primme à partir des sources
git clone https://github.com/primme/primme
cd primme
make python_install

pour utiliser test_paul.py, il faut utiliser line_profiler ou memory_profiler
kernprof -l test_paul.py
python -m line_profiler test_paul.py.lprof

ou 
python -m memory_profiler test_paul.py

plus d'info :
https://www.realpythonproject.com/how-to-benchmark-functions-in-python/