import argparse
import json

import arsenal.aparare.detector
from arsenal.aparare.parse_auth import citeste_esecuri


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    # TODO: intoarce lista de (ip, n) cu n >= prag,
    #       sortata descrescator dupa n
    rezultat =[(ip, n) for ip,n in counts.items() if n >= prag]
    rezultat = sorted(rezultat, key=lambda x: x[1], reverse=True)
    return rezultat



from collections import Counter

c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
print(suspecti(c))
print(suspecti(c, prag=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)
    # TODO: cu --json, scoate json.dumps cu {esecuri, pe_ip, suspecti};
    #       fara, un rezumat cu "BRUTE FORCE" pe fiecare suspect
    if a.json:
        print(json.dumps({
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": sus,
        }, indent=2))
        return




