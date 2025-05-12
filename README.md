# Scraping des Avis Amazon

Ce projet permet de scraper les avis laissés par les utilisateurs sur une page produit Amazon à partir d'un fichier HTML local et les enregistre sous forme de fichiers CSV ou JSON. Les informations extraites incluent le nom du profil, le titre du commentaire, le contenu du commentaire, etc. Le programme prend en charge des sélecteurs CSS configurables et inclut des tests unitaires.

## Fonctionnalités

- Extraction des avis depuis un fichier HTML local.
- Exportation des résultats en CSV ou JSON.
- Configuration des sélecteurs CSS via un fichier config.json.
- Tests unitaires avec pytest pour valider la logique.
- Cache des fichiers HTML pour optimiser les performances.

## Installation

1. Clonez le dépôt :
git clone https://github.com/Theturus/amazon-scraping.git

2. Créez et activez un environnement virtuel :
python -m venv venv
./venv/Scripts/activate

3. Installez les dépendances :
pip install -r requirements.txt

4. Installez le projet :
pip install -e .

## Méthodologie

1. Entrée : Fichiers HTML contenant des pages d'avis Amazon (stockés dans data/input/).
2. Scraping : Le script src/scraping.py analyse le HTML avec BeautifulSoup, extrayant les noms, titres, commentaires, notes, dates et statuts d'achat vérifié.
3. Sortie : Les avis sont enregistrés en CSV (data/output/reviews.csv) ou JSON (data/output/reviews.json) selon les options spécifiées.
4. Tests : Les tests unitaires dans tests/test_scraping.py valident les fonctions de chargement, de configuration et de scraping.

## Utilisation

- Placez le fichier HTML de la page produit dans data/input/.
- Exécutez le script avec : python src/scraping.py data/input/fichier.html --csv --json
    - --csv : Exporter les résultats en CSV.
    - --json : Exporter les résultats en JSON.
- Les sorties sont enregistrées dans data/output/.

### Exemple de sortie console :
- Nom du profil : Paula Norton
- Titre du commentaire : Super
- Texte du commentaire : En lire plus
- Note : Non disponible
- Date : Avis laissé au Mexique le 9 novembre 2023
- Achat vérifié : Achat vérifié

### Exemple de fichier CSV généré :
name,title,comment,rating,date,verified
Amazon Customer,,En lire plus,"5,0 sur 5 étoiles",Avis laissé en France le 24 octobre 2024,Achat vérifié


## Tests
Exécutez les tests avec : pytest tests/test_scraping.py

## Configuration
Modifiez config/config.json pour ajuster les sélecteurs CSS si la structure HTML d'Amazon change :

## Améliorations Futures

- Scraping en direct avec gestion des restrictions d'Amazon.
- Interface graphique avec Streamlit pour visualiser les avis.
- Support multi-pages pour scraper plusieurs fichiers HTML.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
Contributeur

Theturus GOUDAN (https://github.com/Theturus)

