# FormRecognizer-SuperPointOCR

## Description
Ce projet est conçu pour faciliter le traitement et l'analyse de données. Il utilise un script Python pour prétraiter les données (preprocess) et effectuer des inférences à partir de ces données. Le script intègre des fonctionnalités de force et de benchmark pour une flexibilité accrue dans les opérations de traitement des données.

## Installation
Pour utiliser ce projet, assurez-vous que Python est installé sur votre système. Clonez ensuite le répertoire du projet et installez les dépendances nécessaires (si elles sont listées dans un fichier `requirements.txt`).

## Utilisation
Le script principal du projet est exécuté à partir de la ligne de commande et offre plusieurs options.

### Preprocess
Pour lancer le preprocess, utilisez l'option `-preprocess` suivie du chemin vers vos données. Par exemple:

```bash
python main.py -preprocess chemin/vers/donnees
```

Si vous souhaitez forcer l'exécution du preprocess, utilisez l'option --force:

```bash
python main.py -preprocess chemin/vers/donnees --force
```

### Inference
Pour effectuer une inférence, utilisez l'option -inference suivie du chemin vers vos données. Par exemple:

```bash
python main.py -inference chemin/vers/donnees
```

Pour activer le benchmark pendant l'inférence, ajoutez l'option -benchmark:

```bash
python main.py -inference chemin/vers/donnees -benchmark
```

Notez que l'option -benchmark ne peut être utilisée qu'avec -inference.

