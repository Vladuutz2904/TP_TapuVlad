from httptools import *

print("--- Partea 1: Parametri în URL ---")
print(search({"q": "python", "page": "2"}))
print(search({"q": "hello world & co"}))
print(search_url({"q": "python", "page": "2"}))

print("\n--- Partea 2: Anteturi ---")
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())

print("\n--- Partea 3: Trimiterea datelor ---")
print(post_json({"name": "Ana", "age": 19, "tags": ["a", "b"]}))
print(post_form({"user": "ana", "city": "Bălți"}))

print("\n--- Partea 4: Coduri de stare ---")
print(describe_status(200))
print(describe_status(404))
print(describe_status(503))
print(is_ok(204))
print(is_ok(500))

print("\n--- Partea 5: Redirecționări ---")
print(count_redirects(3))
print(final_url(2))
print(first_hop(3))

print("\n--- Partea 6: Sesiuni și cookie-uri ---")
print(cookie_demo("theme", "dark"))
print(no_session_demo("theme", "dark"))

print("\n--- Partea 7: Raportul final ---")
for path in PATHS:
    print(path, report(path))

print("\n--- Partea 8: Autentificare ---")
print(check_login("admin", "secret"))
print(check_login("admin", "greșit"))