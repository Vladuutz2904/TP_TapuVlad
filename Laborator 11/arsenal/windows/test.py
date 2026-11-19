from dataclasses import dataclass, asdict
import json


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str


p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")


@dataclass
class Proces:
    pid: int;
    nume: str;
    user: str;
    cale: str;

    def e_suspect(self):
        # TODO: True daca una din CAI_SUSPECTE e in self.cale
        return any(p in self.cale for p in CAI_SUSPECTE)


print(p.e_suspect())  # True (update.exe din Temp)
