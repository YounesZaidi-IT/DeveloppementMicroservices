#!/usr/bin/env python
"""Générateur de trafic (TP10) : envoie des requêtes en continu et classe les réponses.

  - réussie        : 2xx
  - échec propre   : 4xx ou 503 rapide (le système se protège)
  - échec sale     : 5xx inattendu, ou réponse en plus de 5 secondes

Usage :  python scripts/trafic.py http://localhost:8000 [duree_minutes]
"""
import random
import sys
import time

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
DUREE = float(sys.argv[2]) if len(sys.argv) > 2 else 30
SEUIL_SALE = 5.0

stats = {"réussies": 0, "échecs propres": 0, "échecs sales": 0}


def frapper(client):
    debut = time.monotonic()
    try:
        if random.random() < 0.5:
            r = client.get("/produits")
        else:
            r = client.post("/produits", json={"nom": f"p{random.randint(1, 10 ** 6)}",
                                               "prix": random.randint(1, 500), "stock": 1})
        duree = time.monotonic() - debut
        if duree > SEUIL_SALE or r.status_code >= 500 and r.status_code != 503:
            stats["échecs sales"] += 1
        elif r.status_code < 400:
            stats["réussies"] += 1
        else:
            stats["échecs propres"] += 1
    except Exception:
        duree = time.monotonic() - debut
        stats["échecs sales" if duree > SEUIL_SALE else "échecs propres"] += 1


def main():
    fin = time.monotonic() + DUREE * 60
    dernier_affichage = 0.0
    with httpx.Client(base_url=BASE, timeout=SEUIL_SALE + 1) as client:
        while time.monotonic() < fin:
            frapper(client)
            if time.monotonic() - dernier_affichage > 10:
                total = sum(stats.values()) or 1
                print(f"[{time.strftime('%H:%M:%S')}] "
                      + " | ".join(f"{k}: {v} ({100 * v // total} %)" for k, v in stats.items()))
                dernier_affichage = time.monotonic()
            time.sleep(0.2)
    total = sum(stats.values()) or 1
    print("\n===== RAPPORT FINAL =====")
    for k, v in stats.items():
        print(f"  {k:15s} : {v:5d}  ({100 * v // total} %)")
    print("Objectif du TP10 : zéro échec sale.")


if __name__ == "__main__":
    main()
