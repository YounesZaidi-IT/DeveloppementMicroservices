#!/usr/bin/env python
"""Vérification du TP2 : les 5 routes CRUD de /produits.

Usage :  python scripts/check_tp2.py http://localhost:8000
"""
import sys

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
ok = 0
total = 5


def result(nom, reussi, detail=""):
    global ok
    ok += bool(reussi)
    print(f"  {'✔' if reussi else '✘'} {nom}" + (f"  ({detail})" if detail else ""))


def main():
    c = httpx.Client(base_url=BASE, timeout=5)
    print(f"Vérification du TP2 sur {BASE}\n")

    # 1. POST valide -> 201 + id
    r = c.post("/produits", json={"nom": "Produit-check", "prix": 42.0, "stock": 3})
    result("POST /produits (création, 201 + id)",
           r.status_code == 201 and isinstance(r.json().get("id"), int), f"code {r.status_code}")
    pid = r.json().get("id") if r.status_code == 201 else 0

    # validation : prix négatif -> 422
    r = c.post("/produits", json={"nom": "X", "prix": -1})
    if r.status_code != 422:
        print(f"  ⚠ la validation laisse passer un prix négatif (code {r.status_code})")

    # 2. GET liste -> 200 + liste
    r = c.get("/produits")
    result("GET /produits (liste, 200)", r.status_code == 200 and isinstance(r.json(), list),
           f"code {r.status_code}")

    # 3. GET détail -> 200 ; inconnu -> 404
    r = c.get(f"/produits/{pid}")
    r404 = c.get("/produits/999999")
    result("GET /produits/{id} (200 et 404 sur inconnu)",
           r.status_code == 200 and r404.status_code == 404,
           f"codes {r.status_code}/{r404.status_code}")

    # 4. PUT -> 200
    r = c.put(f"/produits/{pid}", json={"nom": "Produit-check-v2", "prix": 43.0, "stock": 2})
    result("PUT /produits/{id} (200)", r.status_code == 200, f"code {r.status_code}")

    # 5. DELETE -> 204 puis GET -> 404
    r = c.delete(f"/produits/{pid}")
    rget = c.get(f"/produits/{pid}")
    result("DELETE /produits/{id} (204, puis 404 en lecture)",
           r.status_code == 204 and rget.status_code == 404,
           f"codes {r.status_code}/{rget.status_code}")

    print(f"\nRésultat : {ok}/{total} routes OK")
    sys.exit(0 if ok == total else 1)


if __name__ == "__main__":
    try:
        main()
    except httpx.ConnectError:
        print(f"Impossible de joindre {BASE} — le service est-il démarré ?")
        sys.exit(2)
