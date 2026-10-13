# Laborator: functii, metode si importuri pe web
# Student: Tapu Vlad

import time
import requests
import urllib.request
from requests import get
import requests as rq

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def pauza():
    """Pauza de o secunda intre cereri, ca sa nu suprasolicitam site-ul."""
    time.sleep(1)


# Ex1 - primul import
print("Ex1: versiunea requests =", requests.__version__)
# requests este o biblioteca externa (a fost scrisa de terti si nu face parte
# din Python), de aceea trebuie descarcata cu pip install requests.
# urllib face parte din biblioteca standard: vine deja instalata odata cu Python.

# Ex2 - doua stiluri de import
pauza()
print("Ex2 (import requests):", requests.get(BASE_URL, timeout=TIMEOUT).status_code)
pauza()
print("Ex2 (from requests import get):", get(BASE_URL, timeout=TIMEOUT).status_code)
# Avantaj "import requests": se vede mereu de unde vine functia (requests.get),
# deci nu apar conflicte de nume cu alte functii numite get.
# Avantaj "from requests import get": codul este mai scurt, se scrie direct get(...).

# Ex3 - alias
pauza()
print("Ex3:", rq.get(BASE_URL, timeout=TIMEOUT).status_code)
# Un alias face codul mai usor de citit cand este o abreviere cunoscuta sau
# cand numele modulului este lung (np, pd, rq). Il face mai greu de citit cand
# este o litera sau un cuvant fara legatura cu biblioteca (de ex. "import requests as x"),
# pentru ca cititorul nu mai stie ce reprezinta numele.

# Ex4 - doar biblioteca standard
pauza()
with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
    print("Ex4: status =", response.status)
    body = response.read().decode("utf-8")  # .read() returneaza bytes -> decode in str
    print(body[:200])

# Ex5 - dir()
print("Ex5:", dir(requests))
# Trei nume din rezultat:
#   "get"       - functie (requests.get)
#   "Session"   - clasa (requests.Session)
#   "adapters"  - modul (requests.adapters)

# Ex6 - documentatia
help(requests.get)
# Parametrul care seteaza timpul maxim de asteptare este "timeout" (prin **kwargs).
pauza()
print("Ex6:", requests.get(BASE_URL, timeout=TIMEOUT))

# Ex7 - cronometrare
pauza()
start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()
print(f"Ex7: perf_counter = {end - start:.6f} s")
print("Ex7: response.elapsed =", response.elapsed.total_seconds(), "s")
# perf_counter masoara tot timpul scurs in programul nostru (inclusiv crearea
# conexiunii si citirea corpului); elapsed masoara doar intervalul dintre trimiterea
# cererii si primirea antetelor raspunsului, deci este de obicei putin mai mic.

# Ex8 - import care esueaza
try:
    import bs4
    print("Ex8: modulul bs4 este instalat")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

# Verificati-va: modul = un singur fisier .py care se poate importa;
# pachet = director cu mai multe module (are __init__.py);
# biblioteca = colectie de module/pachete cu un scop comun (ex: requests).
