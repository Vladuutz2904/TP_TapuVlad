# Laborator: functii, metode si importuri pe web
# Student: Tapu Vlad

import hashlib
import json
import re
import socket
import ssl
import time
import urllib.parse
from datetime import datetime, timezone
from html.parser import HTMLParser

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# Ex35
def decompose_url(url: str) -> None:
    """Descompune un URL si afiseaza schema, domeniul, calea, query-ul si fragmentul."""
    p = urllib.parse.urlparse(url)
    print("scheme  :", p.scheme)
    print("netloc  :", p.netloc)
    print("path    :", p.path)
    print("query   :", p.query)
    print("fragment:", p.fragment)


# Ex36
def compose_urls(base: str, paths: list) -> list:
    """Transforma legaturile relative in URL-uri complete pornind de la base."""
    return [urllib.parse.urljoin(base, p) for p in paths]


# Ex37
def extract_links(html: str) -> list:
    """Returneaza legaturile href din html, fara duplicate (in ordinea aparitiei)."""
    found = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(found))


# Ex38
def split_links(links: list, domain: str):
    """Imparte legaturile in (interne, externe) fata de domeniul (URL-ul) domain."""
    own = urllib.parse.urlparse(domain).netloc
    internal, external = [], []
    for link in links:
        full = urllib.parse.urljoin(domain, link)
        if urllib.parse.urlparse(full).netloc == own:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


# Ex39
class ImageFinder(HTMLParser):
    """Parser HTML care colecteaza atributul src al fiecarui tag <img>."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Apelata automat de HTMLParser.feed() pentru fiecare tag de deschidere."""
        if tag == "img":  # HTMLParser aduce deja tag-urile la litere mici
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

    def handle_startendtag(self, tag, attrs):
        """Tag-urile de forma <img ... /> sunt tratate la fel ca cele obisnuite."""
        self.handle_starttag(tag, attrs)


# Ex40
def page_fingerprint(url: str) -> str:
    """Returneaza amprenta SHA-256 (hex) a continutului paginii."""
    return hashlib.sha256(requests.get(url, timeout=TIMEOUT).content).hexdigest()


# Ex41
def save_headers_json(url: str, filename: str = "headers.json") -> None:
    """Salveaza antetele raspunsului in JSON, le reincarca si afiseaza unul."""
    response = requests.get(url, timeout=TIMEOUT)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dict(response.headers), f, indent=2)
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    name = next(iter(data))
    print(f"{name}: {data[name]}")


# Ex42
def resolve(hostname: str) -> str:
    """Returneaza adresa IP a unui nume de domeniu."""
    return socket.gethostbyname(hostname)


# Ex43
def cert_days_left(hostname: str) -> int:
    """Returneaza numarul de zile ramase pana la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            cert = tls.getpeercert()
    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc)
    return (expires - datetime.now(timezone.utc)).days


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fara src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

if __name__ == "__main__":
    print("Ex35")
    decompose_url("https://cybercor.org/path?x=1#top")

    print("\nEx36")
    for u in compose_urls(BASE_URL, ["/about", "contact.html", "../index.html"]):
        print(u)

    # Ex39 - intai testul pe HTML cunoscut
    print("\nEx39")
    finder = ImageFinder()
    finder.feed(test_html)
    print(finder.images)
    assert finder.images == [
        "/logo.png",                            # imagine obisnuita
        "poza.jpg",                             # tag scris cu majuscule
        "https://cdn.example.com/banner.webp",  # tag care se inchide singur
    ], "Parserul nu a gasit exact imaginile asteptate"
    print("Testul a trecut!")

    response = requests.get(BASE_URL, timeout=TIMEOUT)
    finder = ImageFinder()
    finder.feed(response.text)
    print(len(finder.images), "imagini gasite (<img in text:", response.text.lower().count("<img"), ")")
    for src in finder.images:
        print(src)
    # handle_starttag() este apelata automat de HTMLParser, din interiorul lui
    # feed(), de fiecare data cand parserul intalneste un tag de deschidere.

    print("\nEx37/Ex38")
    links = extract_links(response.text)
    print(links)
    print(split_links(links, BASE_URL))

    print("\nEx40")
    time.sleep(1)
    a = page_fingerprint(BASE_URL)
    time.sleep(1)
    b = page_fingerprint(BASE_URL)
    print(a, b, "identice" if a == b else "diferite")
    # Rezultatele ar fi diferite daca s-ar schimba continutul paginii (text dinamic,
    # data/ora, token CSRF, reclame) intre cele doua cereri.

    print("\nEx41")
    save_headers_json(BASE_URL)

    print("\nEx42")
    print(resolve("cybercor.org"))

    print("\nEx43")
    print(cert_days_left("cybercor.org"), "zile ramase")
