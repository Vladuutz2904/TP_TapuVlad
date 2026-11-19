import base64
from pathlib import Path
from turtledemo.penrose import start
from turtledemo.round_dance import stop

from urllib3.util import url


s = "Salut"
b = s.encode()          # bytes
print(b, b[0])          # b"Salut" 83
# TODO: tipareste b.hex() si refa bytes din hex
#       cu bytes.fromhex(...)
h = b.hex()
print(h)
b2 = bytes.fromhex(h)
print(b2)


import re
def ghici_strat(s):
        # TODO: daca are %xx -> "url"
    if "%" in s:
            return "url"
        # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if len(s) % 2 == 0 and all(c in
        "0123456789abcdefABCDEF" for c in s):
            return "hex"
        # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if all(c in
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in s):
            return "base64"
    return "necunoscut"
print(ghici_strat("%2Fetc"))   # url
print(ghici_strat("48656c6c6f"))  # hex


from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    #   base64 -> base64.b64decode(s)
    #   hex    -> bytes.fromhex(s)
    #   url    -> unquote(s).encode()
    # intoarce (strat, rezultat_bytes)
    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode()
    else:
        rezultat = s.encode()
    return strat, rezultat


def citibil(b):
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)


val = "NTM1OTU3NTk="
for _ in range(8):
    strat, b = desfa(val)
    # TODO: daca citibil(b): opreste si tipareste
    #       altfel val = b.decode(); continua
    if citibil(b):
        print(b.decode())
        break
    val = b.decode()


date = open("lab6/probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    # TODO: daca citibil(clar):
    #       print("cheie:", k, clar.decode())
    if citibil(clar):
        print("cheie:",k,clar.decode())


import hashlib
tinta = open("lab6/probe/hashuri.txt").readline().strip()
print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
for cuv in open("lab6/probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()
    # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
    #       == tinta: print("gasit:", cuv); break
    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break


import argparse, json, os
p = argparse.ArgumentParser()
p.add_argument("intrare")          # sir sau cale
p.add_argument("--fisier", action="store_true")
a = p.parse_args()
# TODO: daca a.fisier, citeste octetii din cale;
#       altfel trateaza intrarea ca sir
# TODO: salveaza {strat, rezultat} in
#       arsenal/forensics/fisa.json
if a.fisier:
    with open(a.intrare, "rb") as f:
        val = f.read().decode().strip()
else:
    val = a.intrare


strat, b = desfa(val)
os.makedirs("lab6/arsenal/forensics", exist_ok=True)
with open("lab6/arsenal/forensics/fisa.json", "w") as f:
    json.dump({"strat": strat, "rezultat": b.decode(errors="replace")}, f)


def tip_real(cale):
    cap = open(cale, "rb").read(8)
    # TODO: daca cap incepe cu b"%PDF" -> "pdf"
    #       b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg"
    #       b"PK\x03\x04" -> "zip/docx"
    if cap.startswith(b"%PDF"):
        return"pdf"
    if cap.startswith(b"x89PNG"):
        return"png"
    if cap.startswith(b"\xff\xd8"):
        return"jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return"zip/docx"
    return cap.hex()
print(tip_real("lab6/probe/foto.jpg"))




import re
date = open("lab6/probe/ascuns.png", "rb").read()
# TODO: for m in re.findall(rb"[ -~]{4,}", date):
#           print(m.decode())
# cauta un indiciu: o cale, un mesaj, un nume de fisier

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())


from PIL import Image
from PIL.ExifTags import TAGS

exif = Image.open("lab6/probe/foto.jpg")._getexif() or {}
gps = exif.get(34853, {})
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
# TODO: ia blocul GPS (tag 34853) si tipareste
#       latitudinea si longitudinea

    print("Latitudinea:", gps.get(2))
    print("Longitudinea:", gps.get(4))


date = open("lab6/probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
# TODO: daca i != -1:
#   open("gasit.zip","wb").write(date[i:])
#   print("arhiva extrasa de la octetul", i)
#   apoi dezarhiveaza si vezi ce era inauntru
if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)


from PIL import Image
img = Image.open("lab6/probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)
# TODO: pentru fiecare bit, ia un canal si pune
#   canal = (canal & ~1) | int(bit)
px_nou = px.copy()
for i,bit in enumerate(biti):
    r, g, b = px_nou[i]
    r = (r & ~1) | int(bit)
    px_nou[i] = (r, g, b)
# TODO: img.putdata(px_nou); img.save("stego.png")
    img.putdata(px_nou)
    img.save("stego.png")



px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
    # TODO: aduna ultimii biti (r&1, g&1, b&1)
    pass
    biti += str(r&1)
# TODO: grupeaza cate 8 biti -> octeti -> text
#       opreste-te la primul octet 0 (final de mesaj)
mesaj=""
for i in range(0, len(biti), 8):
    mesaj += chr(int(biti[i:i+8], 2))
print(mesaj)


