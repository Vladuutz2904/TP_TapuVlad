import requests

BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

# Partea 1: parametri în URL
def search(params):
        """GET pe /get cu parametri în URL; returnează parametrii primiți de server."""
        r = requests.get(f"{BASE}/get", params=params)
        return r.json() ["args"]
pass
def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu parametri."""
    r = requests.get(f"{BASE}/get", params=params)
    return r.url

pass
# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de server."""
    r = requests.get(BASE + "/headers", headers={"User-Agent": agent})
    return r.json()["headers"]["User-Agent"]
pass
def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]

pass
# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de server."""
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]

pass
def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de server."""
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]
print()
pass
# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau 'eroare server'."""
    try:
        r = requests.get(f"{BASE}/status/{code}")
        if 200 <= r.status_code < 300:
            return "succes"
        elif 400 <= r.status_code < 500:
            return "eroare client"
        elif 500 <= r.status_code < 600:
            return "eroare server"
        return "alt status"
    except requests.RequestException:
        return "eroare rețea"

pass
def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel False."""
    r = requests.get(BASE + "/status/" + str(code))
    try:
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False
pass
# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost
    Exercițiu de pregătire: Trusa de unelte HTTP
    Page 2 of 11
    urmate."""
    r = requests.get(f"{BASE}/redirect/{n}")
    return r.status_code
pass
def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    r = requests.get(f"{BASE}/redirect/{n}")
    return r.url
pass
def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul Location."""
    r = requests.get(f"{BASE}/redirect/{n}")
    return r.headers.get("Location")
pass
# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ sesiune."""
    s = requests.Session()
    s.get(f"https://httpbin.org/cookies/set?{name}={value}")
    r = s.get(f"{BASE}/cookies")
    return r.json().get("cookies")


pass
def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookieurile văzute de server."""
    s = requests.Session()
    requests.get(f"https://httpbin.org/cookies/set?{name}={value}")
    r = s.get(f"{BASE}/cookies")
    return r.json().get("cookies")

pass
# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    timeout = 3
    url = BASE + path
    try:
        r = requests.get(BASE, timeout=timeout)
        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content-type": r.headers.get("Content-Type"),
        }
    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }
pass
# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel False."""
    r = requests.get(f"{BASE}/basic-auth/admin/secret")
    if r.status_code == 200:
        return True
    else:
        return False
print(check_login("user", "password"))


pass

