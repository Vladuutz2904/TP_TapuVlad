# Laborator: functii, metode si importuri pe web
# Student: Tapu Vlad

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def pauza():
    """Pauza de o secunda intre cereri."""
    time.sleep(1)


response = requests.get(BASE_URL, timeout=TIMEOUT)

# Ex9
print("Ex9")
print(response.status_code)  # atribut
print(response.ok)           # atribut
print(response.url)          # atribut
print(response.encoding)     # atribut

# Ex10
print("\nEx10")
response.raise_for_status()  # metoda; pe pagina principala nu arunca nimic
pauza()
try:
    r404 = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    r404.raise_for_status()
    print("Pagina inexistenta a raspuns totusi cu", r404.status_code)
except requests.HTTPError as e:
    print("Pagina ceruta nu exista sau nu poate fi accesata:", e)

# Ex11
print("\nEx11")
for name, value in response.headers.items():
    print(f"{name}: {value}")

# Ex12
print("\nEx12")
print(response.headers.get("Server", "lipseste"))
print(response.headers.get("Content-Type", "lipseste"))
print(response.headers.get("content-type", "lipseste"))
# Observatie: numele antetelor nu tin cont de majuscule/minuscule
# (response.headers este un dictionar insensibil la litere mari/mici).

# Ex13
print("\nEx13")
print(response.text.lower().count("cyber"))
# Putem inlantui pentru ca .lower() returneaza un sir nou (str), iar pe un str
# se poate apela imediat o alta metoda de sir, .count().

# Ex14
print("\nEx14")
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
print(html[start:end].strip())

# Ex15
print("\nEx15")
lines = html.splitlines()
print(len(lines), "linii; cea mai lunga are", len(max(lines, key=len)) if lines else 0, "caractere")

# Ex16
print("\nEx16")
if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")

# Ex17
print("\nEx17")
pauza()
r = requests.get("http://cybercor.org", timeout=TIMEOUT)
for step in r.history:
    print(step.status_code, step.url)
print("URL final:", r.url)

# Ex18
print("\nEx18")
pauza()
r_head = requests.head(BASE_URL, timeout=TIMEOUT)
print("HEAD:", len(r_head.content), "| GET:", len(response.content))
# HEAD returneaza doar codul de stare si antetele, fara corp (len = 0);
# GET returneaza si corpul paginii, deci continutul are lungime mare.

# Ex19
print("\nEx19")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
for cookie in response.cookies:
    print(cookie.name, cookie.secure)

# Ex20
print("\nEx20")
pauza()
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Tapu-Vlad"})
r_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(r_echo.json())
print("Antetul a fost trimis:", r_echo.json()["headers"].get("User-Agent") == "WebLab-Tapu-Vlad")

# Verificati-va: response.text este un atribut (o valoare deja calculata), deci
# nu are paranteze; response.json() este o metoda (o actiune care parseaza corpul
# ca JSON la apel), deci se apeleaza cu paranteze.
