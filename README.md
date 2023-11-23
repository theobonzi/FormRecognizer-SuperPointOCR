# FormRecognizer-SuperPointOCR

## Description
FormRecognizer-SuperPointOCR est une solution avancée conçue pour optimiser et évaluer le traitement de formulaires à travers diverses techniques OCR (Reconnaissance Optique de Caractères). Ce projet intègre des technologies de pointe telles que Superpoint pour la détection de caractéristiques et supporte plusieurs moteurs OCR pour permettre des benchmarks comparatifs et des analyses de performance.

## Installation
#### Prérequis
- Python 3.9+
- [Optionnel] Environnement virtuel tel que Conda ou venv

#### Étapes d'installation
1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation
Le script principal run.py peut être utilisé pour effectuer des opérations de prétraitement et d'inférence. Les commandes disponibles sont les suivantes :

### Prétraitement

Pour lancer le prétraitement :

```bash
python run.py -preprocess <chemin_vers_donnees> [--force]
```

### Inference
Pour réaliser une inférence sur un fichier ou plusieurs formulaires à partir d'un fichier Excel :

- Sur un fichier :
```bash
python run.py -inference_file <chemin_vers_fichier> [-nb_ocr <nombre>] [-benchmark]
```

- A partir d'un fichier Excel :
```bash
python run.py -inference_excel [-nb_files <nombre>] [-nb_ocr <nombre>] [-ocr <google|trocr>] [-benchmark]
```