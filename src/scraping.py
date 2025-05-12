# src/scraping.py
import sys
import logging
import argparse
import json
import csv
from pathlib import Path
from functools import lru_cache
from bs4 import BeautifulSoup

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@lru_cache(maxsize=10)
def load_html_file(html_file_path):
    """Charge et parse un fichier HTML avec cache."""
    try:
        if not Path(html_file_path).is_file():
            logger.error(f"Le fichier {html_file_path} n'existe pas.")
            raise FileNotFoundError(f"Le fichier {html_file_path} n'existe pas.")
        with open(html_file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du fichier : {str(e)}")
        raise

def load_config(config_path="config/config.json"):
    """Charge les sélecteurs CSS depuis un fichier de configuration."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            required_keys = ["name", "title", "comment"]
            optional_keys = ["rating", "date", "verified"]
            for key in required_keys:
                if key not in config:
                    logger.error(f"Clé requise '{key}' manquante dans {config_path}")
                    raise KeyError(f"Clé requise '{key}' manquante")
            return config
    except FileNotFoundError:
        logger.warning("Fichier config.json non trouvé, utilisation des valeurs par défaut.")
        return {
            "name": "span.a-profile-name",
            "title": "a[data-hook='review-title'] span",
            "comment": "span[data-hook='review-body'] span",
            "rating": "i[data-hook='review-star-rating'] span.a-icon-alt",
            "date": "span[data-hook='review-date']",
            "verified": "span[data-hook='avp-badge-linkless']"
        }

def scrape_amazon_reviews(html_file_path, config_path="config/config.json"):
    """Scrape les avis Amazon à partir d'un fichier HTML."""
    try:
        source = load_html_file(html_file_path)
        soup = BeautifulSoup(source, 'html.parser')
        selectors = load_config(config_path)

        names = soup.select(selectors["name"])
        titles = soup.select(selectors["title"])
        comments = soup.select(selectors["comment"])
        ratings = soup.select(selectors.get("rating", "")) if "rating" in selectors else []
        dates = soup.select(selectors.get("date", "")) if "date" in selectors else []
        verified = soup.select(selectors.get("verified", "")) if "verified" in selectors else []

        # Log des résultats des sélecteurs pour diagnostic
        logger.info(f"Nombre de noms trouvés : {len(names)}")
        logger.info(f"Nombre de titres trouvés : {len(titles)}")
        logger.info(f"Nombre de commentaires trouvés : {len(comments)}")
        logger.info(f"Nombre de notes trouvées : {len(ratings)}")
        logger.info(f"Nombre de dates trouvées : {len(dates)}")
        logger.info(f"Nombre de vérifications trouvées : {len(verified)}")

        if not (names and titles and comments):
            logger.warning("Certaines informations n'ont pas été trouvées.")
            return []

        reviews = []
        for i, (name, title, comment) in enumerate(zip(names, titles, comments)):
            review = {
                "name": name.get_text(strip=True),
                "title": title.get_text(strip=True),
                "comment": comment.get_text(strip=True),
                "rating": ratings[i].get_text(strip=True) if i < len(ratings) else "Non disponible",
                "date": dates[i].get_text(strip=True) if i < len(dates) else "Non disponible",
                "verified": verified[i].get_text(strip=True) if i < len(verified) else "Non vérifié"
            }
            reviews.append(review)
            logger.info(f"Avis extrait : {review['name']}")

        return reviews
    except Exception as e:
        logger.error(f"Erreur lors du scraping : {str(e)}")
        return []

def export_to_csv(reviews, output_file="data/output/reviews.csv"):
    """Exporte les avis en fichier CSV."""
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'title', 'comment', 'rating', 'date', 'verified'])
            writer.writeheader()
            writer.writerows(reviews)
        logger.info(f"Avis exportés vers {output_file}")
    except Exception as e:
        logger.error(f"Erreur lors de l'exportation CSV : {str(e)}")

def export_to_json(reviews, output_file="data/output/reviews.json"):
    """Exporte les avis en fichier JSON."""
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
        logger.info(f"Avis exportés vers {output_file}")
    except Exception as e:
        logger.error(f"Erreur lors de l'exportation JSON : {str(e)}")

def display_reviews(reviews):
    """Affiche les avis dans la console."""
    for review in reviews:
        print(f"Nom du profil : {review['name']}")
        print(f"Titre du commentaire : {review['title']}")
        print(f"Texte du commentaire : {review['comment']}")
        print(f"Note : {review['rating']}")
        print(f"Date : {review['date']}")
        print(f"Achat vérifié : {review['verified']}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Script de scraping des avis Amazon.")
    parser.add_argument("html_file", type=str, help="Chemin vers le fichier HTML à scraper")
    parser.add_argument("--csv", action="store_true", help="Exporter les résultats en CSV")
    parser.add_argument("--json", action="store_true", help="Exporter les résultats en JSON")
    args = parser.parse_args()

    reviews = scrape_amazon_reviews(args.html_file)
    if reviews:
        display_reviews(reviews)
        if args.csv:
            export_to_csv(reviews)
        if args.json:
            export_to_json(reviews)
    else:
        logger.info("Aucun avis extrait.")
        sys.exit(1)

if __name__ == "__main__":
    main()