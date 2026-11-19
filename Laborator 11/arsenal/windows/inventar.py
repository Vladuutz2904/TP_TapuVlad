from dataclasses import dataclass
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")


# A1 + A2
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str


    def e_suspect(self):
        # TODO: True daca una din CAI_SUSPECTE e in self.cale
        return any(c in self.cale for c in CAI_SUSPECTE)


# A3
SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        # TODO: True daca self.id in SUSPECTE_ID SAU self.nivel == "critical"
        return self.id in SUSPECTE_ID or self.nivel == "critical"


# A4
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce [Proces(**d) for d in json.load(f)]
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


# B1 + B2
@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            # TODO: return cls([Proces(**d) for d in json.load(f)])
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        # TODO: lista proceselor cu p.e_suspect()
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        # TODO: dict user -> lista de nume (foloseste setdefault)
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat


# B3
def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]
    # TODO: cu --json, json.dumps cu asdict pe suspecte si alarma;
    #       fara, un rezumat citibil
    if a.json:
        print(json.dumps({
            "procese_suspecte": [
                {"pid": p.pid, "nume": p.nume, "user": p.user, "cale": p.cale}
                for p in inv.suspecte()
            ],
            "evenimente_alarma": [
                {"id": e.id, "nivel": e.nivel, "sursa": e.sursa,
                 "cont": e.cont, "mesaj": e.mesaj}
                for e in alarma
            ]
        }, indent=2))

    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")

        for p in inv.suspecte():
            print(f" [{p.pid}] {p.nume} ({p.user}) {p.cale}")

        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")

        for e in alarma:
            print(f" {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()