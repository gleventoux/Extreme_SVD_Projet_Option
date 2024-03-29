

# Extreme_SVD_Projet_Option

## Introduction

Ce repo comporte tout notre code produit dans le cadre de notre projet d'option visant établir un benchmark de méthodes SVD out-of-core implémentées en Python.
```
python setup.py install
```

## Dépendances

- [Scikit learn](https://scikit-learn.org/stable/index.html)
```
conda install scikit-learn
```

- [Dask](https://www.dask.org/)
```
conda install dask
```

## Génération de matrices

Afin de tester nos méthodes de SVD, nous avons conçu une CLI permettant de générer des matrices de plusieurs types : aléatoire, physique, svd-connu.

La CLI doit être utilisée depuis la racine du projet. Les matrices sont générées au format .hdf5 dans le sous-répertoire ```matrix```.

### Matrices aléatoires

Pour générer une matrice de réels aléatoires dont les coéfficients sont tirés uniformément dans un intervalle, exécuter la commande suivante :

```
python3 -m generate random <FILENAME> <N> <M> --low=<LOW> --high=<HIGH> --bsize=<BSIZE> 
```
Arguments positionnels:
- FILENAME (str) : nom du fichier sans extension
- N (int) : nombre de lignes
- M (int) : nombre de colonnes

Arguments optionnels:
- LOW (float, default=0) : Borne inf pour les coefficients
- HIGH (float, default=1) : Borne sup pour les coefficients
- BSIZE (int, defaulft=1000) : Taille des batchs 

### Matrices aléatoires avec SVD

Pour générer une matrice aléatoire ainsi que sa décomposition SVD, exécuter la commande suivante :

```
python3 -m generate svd_known <N> <M> --filename=<FILENAME> --low=<LOW> --high=<HIGH> --bsize=<BSIZE> 
```
Arguments positionnels:
- N (int) : nombre de lignes
- M (int) : nombre de colonnes

Arguments optionnels:
- FILENAME (str) : nom du fichier sans extension
- LOW (float, default=0) : Borne inf pour les coefficients
- HIGH (float, default=1) : Borne sup pour les coefficients
- BSIZE (int, defaulft=1000) : Taille des batchs

Après exécution de cette commande, apparaît dans le répertoire ```matrix/``` les deux fichiers suivants:
- ```filename.hdf5``` : stock la matrice aléatoire découpée en batch (un dataset = un batch)
- ```filenameSVD.hdf5``` : stock la SVD de la matrice. Quatre datasets sont définis : U, S, V, M. 

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

si pip primme ne fonctionne pas , voici les sources :
git clone https://github.com/primme/primme

make python_install

pour utiliser benchmark.py, il faut utiliser line_profiler ou memory_profiler

kernprof -l benchmark.py

python -m line_profiler benchmark.py.lprof

ou 

python -m memory_profiler benchmark.py

plus d'info :
https://www.realpythonproject.com/how-to-benchmark-functions-in-python/



pour installer le h5py avec parallèle acceleration, c'est plus vite de reinstall h5py

```bash
conda uninstall h5py
```

```bash
conda install -c conda-forge "h5py>=2.9=mpi*"
```

et vérifier l'installation:

```bash
$ which mpirun
/anaconda/envs/env_name/bin/mpirun
```

eventuellement ajouter pour un processeur Intel
conda update intel-openmp.


pour tester le code parallel

```
python3 test_parallel.py
```

ou

```bash
mpirun -np 4 python3 svd_func.py
```

