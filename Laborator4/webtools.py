# Laborator: functii, metode si importuri pe web
# Student: Tapu Vlad
"""Modul cu functii reutilizabile pentru analiza unui site web."""

import csv
import json
import re
import socket
import ssl
import time
import urllib.parse
from datetime import datetime, timezone

import requests

TIMEOUT = 10  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-Tapu-Vlad"}  # Ex47


# Ex44
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Trimite o cerere GET (cu antetele implicite) si returneaza raspunsul."""
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Returneaza textul dintre <title> si </title> dintr-un sir HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()


def security_headers(url: str) -> dict:
    """Returneaza {antet: True/False} pentru cele cinci antete de securitate."""
    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    headers = fetch(url).headers
    return {name: name in headers for name in names}


def score_headers(results: dict) -> str:
    """Returneaza scorul antetelor, de ex. '3/5'."""
    return f"{sum(1 for ok in results.values() if ok)}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Returneaza {cale: cod_de_stare} pentru fiecare cale relativa."""
    results = {}
    for path in paths:
        results[path] = get_status(base + path)
        time.sleep(1)
    return results


def resolve(hostname: str) -> str:
    """Returneaza adresa IP a unui nume de domeniu."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returneaza numarul de zile ramase pana la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            cert = tls.getpeercert()
    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc)
    return (expires - datetime.now(timezone.utc)).days


def extract_links(html: str) -> list:
    """Returneaza legaturile href din html, fara duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list, domain: str):
    """Imparte legaturile in (interne, externe) fata de domeniul dat."""
    own = urllib.parse.urlparse(domain).netloc
    internal, external = [], []
    for link in links:
        full = urllib.parse.urljoin(domain, link)
        if urllib.parse.urlparse(full).netloc == own:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


def fetch_robots(base: str):
    """Returneaza textul din /robots.txt sau None daca lipseste."""
    try:
        response = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    return response.text if response.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    """Returneaza lista valorilor Disallow: din robots.txt (lista goala pentru None)."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths


def get_redirects(url: str) -> list:
    """Returneaza lantul de redirectionari pornind de la varianta http:// a url-ului."""
    http_url = "http://" + urllib.parse.urlparse(url).netloc
    response = fetch(http_url)
    return [f"{r.status_code} -> {r.headers.get('Location', '?')}" for r in response.history]


# Ex49
def create_csv(base: str, paths: list, filename: str = "report.csv") -> None:
    """Salveaza rezultatul check_paths() in CSV, cu coloanele path, status, checked_at."""
    results = check_paths(base, paths)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])


# Ex50
def site_report(url: str, filename: str = "report.json") -> dict:
    """Colecteaza informatii despre site, le afiseaza si le salveaza in report.json."""
    url = url.rstrip("/")
    host = urllib.parse.urlparse(url).hostname

    response = fetch(url)
    time.sleep(1)
    redirects = get_redirects(url)
    time.sleep(1)
    internal, external = split_links(extract_links(response.text), url + "/")
    robots = disallowed_paths(fetch_robots(url))
    time.sleep(1)

    report = {
        "Cod de stare": response.status_code,
        "URL final": response.url,
        "Titlu": get_title(response.text),
        "Adresa IP": resolve(host),
        "Redirectionari": redirects,
        "Scor securitate": score_headers(security_headers(url)),
        "Certificat": f"{cert_days_left(host)} de zile ramase",
        "Legaturi": f"{len(internal)} interne, {len(external)} externe",
        "Cai interzise": robots,
    }

    print(f"=== Raport site: {url} ===")
    for key, value in report.items():
        if isinstance(value, list):
            value = ", ".join(value) if value else "-"
        print(f"{key}: {value}")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"Salvat in {filename}")
    return report


# Bonus - BeautifulSoup
def get_title_bs(html: str) -> str:
    """Returneaza titlul paginii folosind BeautifulSoup (sigur si cand lipseste <title>)."""
    from bs4 import BeautifulSoup
    tag = BeautifulSoup(html, "html.parser").find("title")
    return tag.get_text(strip=True) if tag else ""


def extract_links_bs(html: str) -> list:
    """Returneaza legaturile <a href> folosind BeautifulSoup, fara duplicate."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(a["href"] for a in soup.find_all("a", href=True)))


# Ex46
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
# Autotestul ruleaza doar la "python webtools.py", cand fisierul este programul
# principal (__name__ == "__main__"). La "python main.py", webtools este doar
# importat, iar __name__ devine "webtools", deci blocul se sare.
