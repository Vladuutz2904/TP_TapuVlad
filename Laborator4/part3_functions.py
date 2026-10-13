# Laborator: functii, metode si importuri pe web
# Student: Tapu Vlad

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# Ex21 / Ex23 - fetch cu timeout implicit
def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Trimite o cerere GET catre url si returneaza obiectul raspuns."""
    return requests.get(url, timeout=timeout)


# Ex22 + Ex26 - doar codul de stare, cu type hints
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa url."""
    return fetch(url, TIMEOUT).status_code


# Ex24 / Ex25
def get_title(html: str) -> str:
    """Returneaza textul dintre <title> si </title> dintr-un sir HTML.

    Nu face operatii de retea: primeste doar textul HTML.
    """
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()


# Ex27
def page_exists(url: str) -> bool:
    """Returneaza True daca pagina raspunde cu succes, altfel False (fara exceptii)."""
    try:
        requests.get(url, timeout=TIMEOUT).raise_for_status()
        return True
    except requests.RequestException:
        return False


# Ex28
def check_paths(base: str, paths: list) -> dict:
    """Returneaza un dictionar {cale: cod_de_stare} pentru fiecare cale relativa."""
    results = {}
    for path in paths:
        results[path] = get_status(base + path)
        time.sleep(1)
    return results


# Ex29
def get_header(url: str, name: str, default: str = "lipseste") -> str:
    """Returneaza valoarea antetului name sau default daca lipseste."""
    return fetch(url).headers.get(name, default)


# Ex30
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


# Ex31
def score_headers(results: dict) -> str:
    """Returneaza scorul antetelor sub forma 'prezente/total', de ex. '3/5'."""
    return f"{sum(1 for ok in results.values() if ok)}/{len(results)}"


# Ex32
def fetch_robots(base: str):
    """Returneaza textul din /robots.txt sau None daca fisierul lipseste."""
    try:
        response = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    return response.text if response.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    """Returneaza lista valorilor Disallow: din textul robots.txt (lista goala pentru None)."""
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


# Ex33
def response_times(*urls: str) -> dict:
    """Returneaza {url: secunde} cu timpul de raspuns pentru fiecare url primit."""
    times = {}
    for url in urls:
        times[url] = fetch(url).elapsed.total_seconds()
        time.sleep(1)
    return times


# Ex34
def log(message: str, **details) -> None:
    """Afiseaza mesajul urmat de fiecare detaliu, in forma 'mesaj | cheie=valoare'."""
    parts = [message] + [f"{key}={value}" for key, value in details.items()]
    print(" | ".join(parts))


if __name__ == "__main__":
    # Ex21
    print("Ex21:", fetch(BASE_URL).status_code)

    # Ex22
    for p in ["/", "/robots.txt", "/sitemap.xml"]:
        print("Ex22:", p, get_status(BASE_URL + p))
        time.sleep(1)

    # Ex23
    print("Ex23:", fetch(BASE_URL).status_code, fetch(BASE_URL, timeout=3).status_code)
    time.sleep(1)

    # Ex24 / Ex25
    print("Ex24:", get_title(fetch(BASE_URL).text))
    help(get_title)

    # Ex26
    try:
        print(get_status(123))
    except Exception as e:
        print("Ex26: eroare ->", type(e).__name__)
    # Adnotarile de tip sunt doar indicii pentru cititor si pentru editoare:
    # Python nu le verifica la rulare, deci nu ne opresc sa apelam get_status(123).
    # Eroarea apare mai tarziu, din requests, care nu stie ce sa faca cu un int.

    # Ex27
    print("Ex27:", page_exists(BASE_URL), page_exists("https://this-domain-does-not-exist.invalid"))

    # Ex28
    print("Ex28:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

    # Ex29
    print("Ex29:", get_header(BASE_URL, name="Server"))

    # Ex30 / Ex31
    time.sleep(1)
    sec = security_headers(BASE_URL)
    print("Ex30:", sec)
    print("Ex31:", score_headers(sec))

    # Ex32
    time.sleep(1)
    print("Ex32:", disallowed_paths(fetch_robots(BASE_URL)), disallowed_paths(None))

    # Ex33
    time.sleep(1)
    print("Ex33:", response_times(BASE_URL, BASE_URL + "/robots.txt"))

    # Ex34
    log("verificat", url=BASE_URL, status=200)

    # Verificati-va: print() doar afiseaza valoarea pe ecran, iar functia returneaza
    # None; return trimite valoarea inapoi apelantului, care o poate stoca,
    # compara sau folosi mai departe.
