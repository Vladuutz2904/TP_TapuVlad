import requests
from requests.exceptions import RequestException

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.rstrip("/")
    path = path.lstrip("/")

    if not host.startswith("http://") and not host.startswith("https://"):
        host = "https://" + host

    return host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.lower().startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))
    except RequestException as error:
        print("Eroare la cerere:", error)


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except RequestException as error:
        return {
            "status": None,
            "error": str(error),
        }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []

    for url in SITES:
        results.append({
            "url": url,
            "details": check_site(url),
        })

    working_sites = []
    for result in results:
        if result["details"]["status"] == 200:
            working_sites.append(result)

    working_sites.sort(
        key=lambda result: result["details"]["length"],
        reverse=True,
    )

    for result in working_sites:
        print(
            result["url"],
            "->",
            str(result["details"]["status"]) + ",",
            str(result["details"]["length"]) + " octeți",
        )

    failed = len(results) - len(working_sites)
    print("Reușite:", len(working_sites), "| Eșuate:", failed)


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        response_headers = []
        for header in response.headers:
            response_headers.append(header.lower())

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in response_headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(len(present) * 100 / len(SECURITY_HEADERS))
        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except RequestException as error:
        return {
            "status": None,
            "error": str(error),
        }


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None
    attempts_made = 0
    last_error = None
    got_response = False

    for _ in range(max(0, attempts)):
        attempts_made += 1
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            got_response = True
            if status < 500:
                break
        except RequestException as error:
            last_error = str(error)

    result = {
        "status": status,
        "attempts": attempts_made,
    }

    if not got_response and last_error is not None:
        result["error"] = last_error

    return result
