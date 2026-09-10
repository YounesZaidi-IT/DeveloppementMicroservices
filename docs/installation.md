# Préparer sa machine avant la séance 1

Six installations, chacune suivie de la commande qui prouve qu'elle a marché.
À faire chez soi, pas en salle : comptez 45 à 60 minutes et 5 Go d'espace disque libre.

La seule pièce vraiment indispensable est Docker Desktop. Si elle refuse de fonctionner sur
votre machine, passez directement au [plan B](#plan-b--sans-rien-installer).

---

## 1. Git

Sert à récupérer le dépôt et à poser un tag à la fin de chaque séance. Sur Windows,
l'installeur fournit aussi Git Bash, un terminal où les commandes du cours fonctionnent
telles quelles.

| Système | Commande |
|---|---|
| Windows | `winget install --id Git.Git -e` |
| macOS | `xcode-select --install` |
| Linux (Debian, Ubuntu) | `sudo apt update && sudo apt install -y git` |

Renseignez ensuite votre identité, sinon le premier commit sera refusé :

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "vous@exemple.ma"
```

**Contrôle** — `git --version` affiche un numéro, par exemple `git version 2.47.1`.

---

## 2. Docker Desktop

Tous les services du projet, ainsi que leurs bases PostgreSQL et le courtier de messages
RabbitMQ, tournent dans des conteneurs. C'est l'installation la plus longue, et elle demande
un redémarrage sur Windows.

**Windows.** Installez d'abord WSL 2 depuis un PowerShell ouvert en administrateur, puis
redémarrez :

```powershell
wsl --install
```

Installez ensuite Docker Desktop depuis docker.com, en laissant l'option WSL 2 cochée.

**macOS.** Téléchargez Docker Desktop sur docker.com. Prenez la version Apple silicon ou
Intel selon votre Mac, l'autre refusera de s'installer.

**Linux.** Installez Docker Engine et le greffon Compose, puis rejoignez le groupe docker et
rouvrez votre session :

```bash
sudo usermod -aG docker $USER
```

> **Piège Windows.** Si `wsl --install` échoue ou si Docker Desktop refuse de démarrer, la
> virtualisation matérielle est désactivée. Elle s'active dans le BIOS ou l'UEFI, sous le nom
> Intel VT-x ou AMD-V.

```bash
docker --version
docker compose version
docker run --rm hello-world
```

**Contrôle** — Docker en version 24 ou plus, Compose en `v2` et non `v1`, et le conteneur
d'essai qui affiche son message de bienvenue. Docker Desktop doit rester lancé, l'icône
baleine visible ; fermé, toutes les commandes docker échouent.

---

## 3. Python 3.12 au minimum

Les cinq services déclarent `requires-python = ">=3.12"`. Une version 3.11 ne bloque pas
Docker, mais elle empêche d'installer les services et de lancer les tests sur votre machine.

| Système | Comment |
|---|---|
| Windows | Installeur depuis python.org, en cochant « Add python.exe to PATH » sur le premier écran |
| macOS | `brew install python@3.12` |
| Linux (Debian, Ubuntu) | `sudo apt install -y python3.12 python3.12-venv` |

> **Piège Windows.** N'installez pas Python depuis le Microsoft Store. Sa version reste
> bloquée en 3.11, elle ne fournit pas le lanceur `py`, et l'installation du service s'arrête
> sur `requires a different Python: 3.11.9 not in '>=3.12'`.

**Contrôle** — `python --version` affiche `3.12` ou davantage.

---

## 4. Le dépôt et son environnement Python

```bash
git clone <url du dépôt>
cd microservices-template
cp .env.example .env
```

Le fichier `.env` contient les mots de passe locaux. Il n'est jamais versionné, c'est pour
cela qu'il faut le créer à la main.

**Windows, PowerShell :**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si l'activation est refusée, autorisez les scripts locaux une fois pour toutes avec
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**macOS et Linux :**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Le nom `(.venv)` apparaît alors au début de l'invite.

Installez enfin le service exemple et ses dépendances de test. Cette seule commande apporte
FastAPI, pytest, ruff et httpx, ce dernier étant ce dont les scripts du cours ont besoin :

```bash
pip install -e "./services/catalogue[test]"
```

**Contrôle** — `pytest --version` et `ruff --version` répondent tous les deux sans erreur.

---

## 5. VS Code et ses trois extensions

Ce sont exactement les trois extensions que déclare `.devcontainer/devcontainer.json`, donc
les mêmes que vous ayez installé la machine vous-même ou non. Python pour le langage, Docker
pour piloter les conteneurs depuis l'éditeur, Ruff pour signaler les erreurs de style avant
que la chaîne d'intégration ne le fasse.

```bash
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-docker
code --install-extension charliermarsh.ruff
```

**Contrôle** — `code --version` répond. Si la commande est introuvable sur macOS, ouvrez la
palette de VS Code et lancez « Shell Command: Install 'code' command in PATH ».

---

## 6. L'essai qui valide tout

Cette commande construit l'image du service Catalogue, démarre sa base PostgreSQL, attend
qu'elle soit saine, puis lance le service. Le premier lancement télécharge plusieurs
centaines de mégaoctets, les suivants durent quelques secondes.

```bash
docker compose up --build
```

Laissez tourner et ouvrez la documentation générée automatiquement à l'adresse
<http://localhost:8000/docs>. Dans un second terminal :

```bash
curl http://localhost:8000/health
```

**Contrôle** — la réponse attendue, au caractère près :

```json
{"status":"ok","service":"catalogue"}
```

Si vous l'obtenez, votre poste est prêt. Arrêtez tout avec `Ctrl+C` puis `docker compose down`.

---

## Plan B : sans rien installer

Si Docker Desktop refuse de fonctionner sur votre machine, ne perdez pas la séance à le
réparer. Le dépôt embarque un environnement prêt à l'emploi pour GitHub Codespaces.

Il vous faut seulement un compte GitHub. Ouvrez le dépôt sur github.com, puis Code, puis
Codespaces, puis créez un espace. Tout arrive déjà en place : Python 3.12, Docker à
l'intérieur du conteneur, les trois extensions, la copie automatique du fichier de
configuration, et les ports 8000, 8002, 8004 et 15672 redirigés vers votre navigateur.

Prévoyez le premier démarrage avant la séance, il prend plusieurs minutes.

---

## Les quatre pièges Windows

Ce sont les quatre causes qui expliquent la quasi-totalité des postes en panne le jour de la
première séance.

**A. Python du Microsoft Store.** Il se présente comme installé, mais l'installation du
service s'arrête net sur une erreur de version. Désinstallez-le et reprenez depuis python.org.

**B. Docker Desktop fermé.** Le programme doit tourner en arrière-plan, pas seulement être
installé. Sans lui, chaque commande docker répond que le démon est injoignable.

**C. Virtualisation désactivée.** WSL 2 et Docker en dépendent. Elle s'active dans le BIOS ou
l'UEFI, sous Intel VT-x ou AMD-V, et le réglage survit aux redémarrages.

**D. Accents cassés dans la console.** Les scripts du cours s'arrêtent sur une erreur
d'encodage dans le terminal Windows. Lancez-les avec l'option qui force l'UTF-8 :

```bash
python -X utf8 scripts/check_tp2.py http://localhost:8000
```

---

## La vérification finale, en six commandes

Passez ces six lignes avant d'arriver en séance. Si l'une échoue, revenez à l'étape
correspondante.

| Étape | Commande | Réponse attendue |
|---|---|---|
| 1 | `git --version` | un numéro de version |
| 2 | `docker compose version` | v2 ou plus |
| 2 | `docker run --rm hello-world` | le message de bienvenue |
| 3 | `python --version` | 3.12 au minimum |
| 4 | `pytest --version` | un numéro de version |
| 6 | `curl localhost:8000/health` | `status` ok, `service` catalogue |
