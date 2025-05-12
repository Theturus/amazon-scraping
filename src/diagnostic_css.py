from bs4 import BeautifulSoup
with open("data/input/fichier.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    print("Noms:", len(soup.select("span.a-profile-name")))
    print("Titres:", len(soup.select("a[data-hook='review-title'] span")))
    print("Commentaires:", len(soup.select("span[data-hook='review-body'] span")))
    print("Notes:", len(soup.select("i[data-hook='review-star-rating'] span.a-icon-alt")))
    print("Dates:", len(soup.select("span[data-hook='review-date']")))
    print("Vérifiés:", len(soup.select("span[data-hook='avp-badge-linkless']")))