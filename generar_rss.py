import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
from datetime import datetime, timezone

PAGINA = "https://www.italiaoggi.it/settori"
ARCHIVO_RSS = "italiaoggi.xml"

cabeceras = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

respuesta = requests.get(PAGINA, headers=cabeceras, timeout=30)
respuesta.raise_for_status()

sopa = BeautifulSoup(respuesta.text, "html.parser")

enlaces = []
vistos = set()

for enlace in sopa.find_all("a", href=True):
    titulo = enlace.get_text(" ", strip=True)
    url = urljoin(PAGINA, enlace["href"])

    if (
        titulo
        and len(titulo) >= 20
        and "italiaoggi.it" in url
        and url not in vistos
    ):
        vistos.add(url)
        enlaces.append((titulo, url))

generador = FeedGenerator()
generador.id(PAGINA)
generador.title("ItaliaOggi - Settori")
generador.description("Últimas publicaciones de la sección Settori de ItaliaOggi")
generador.link(href=PAGINA, rel="alternate")
generador.link(href=ARCHIVO_RSS, rel="self")
generador.language("it")

fecha = datetime.now(timezone.utc)

for titulo, url in enlaces[:50]:
    entrada = generador.add_entry()
    entrada.id(url)
    entrada.title(titulo)
    entrada.link(href=url)
    entrada.pubDate(fecha)

generador.rss_file(ARCHIVO_RSS, pretty=True)

print(f"RSS creada con {len(enlaces[:50])} publicaciones")
