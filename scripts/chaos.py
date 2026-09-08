#!/usr/bin/env python
"""Campagne de chaos (TP10) : frappe aléatoirement les conteneurs du Compose.

Toutes les 60 à 90 secondes : arrête (puis redémarre), redémarre ou fige un
service au hasard. Lancez scripts/trafic.py en parallèle pour mesurer.

Usage :  python scripts/chaos.py --duree 30
"""
import argparse
import random
import subprocess
import time


def services():
    sortie = subprocess.run(["docker", "compose", "ps", "--services", "--status", "running"],
                            capture_output=True, text=True, check=True).stdout
    return [s for s in sortie.split() if s]


def run(*args):
    print(f"  $ docker compose {' '.join(args)}")
    subprocess.run(["docker", "compose", *args], check=False)


def frapper(cible):
    action = random.choice(["stop_start", "restart", "pause"])
    if action == "stop_start":
        arret = random.randint(20, 45)
        print(f"⚡ {cible} : arrêt pendant {arret} s")
        run("stop", cible)
        time.sleep(arret)
        run("start", cible)
    elif action == "restart":
        print(f"⚡ {cible} : redémarrage brutal")
        run("restart", "-t", "0", cible)
    else:
        gel = random.randint(10, 30)
        print(f"⚡ {cible} : gelé pendant {gel} s (pause)")
        run("pause", cible)
        time.sleep(gel)
        run("unpause", cible)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--duree", type=float, default=30, help="durée en minutes")
    p.add_argument("--exclure", nargs="*", default=[], help="services à épargner")
    args = p.parse_args()

    fin = time.monotonic() + args.duree * 60
    print(f"Campagne de chaos : {args.duree} min. Que les plus résilients survivent !\n")
    while time.monotonic() < fin:
        cibles = [s for s in services() if s not in args.exclure]
        if cibles:
            frapper(random.choice(cibles))
        pause = random.randint(60, 90)
        print(f"…accalmie de {pause} s\n")
        time.sleep(pause)
    print("Campagne terminée. Consultez le rapport de trafic.py et complétez docs/chaos.md.")


if __name__ == "__main__":
    main()
