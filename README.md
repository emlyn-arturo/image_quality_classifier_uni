# UnikittyPy

Finds the best photo for you!

## Was developed for a project course in Deep Learning at the Technical Unviersity of Munich. 
#### MISSING: Only SVM is currently in the repository. The other used algorithms need to be added in future commits
---

## Development setup and tips

### Dependencies
Wenn immer Sie Ihrem Projekt eine neue externe Library hinzufügen möchten,
tragen Sie diese in der Datei `setup.py` in die Liste `install_requires` ein.
Damit stellen Sie sicher, dass bei allen Projektmitgliedern die gleichen
Packages installiert werden.

Dependencies installieren

```bash
python3 setup.py develop
python3 pip install -r requirements
```

Submodules (momenant nur für iterne Datensammlung nötig)
```bash
git submodules init
git submodules update
```

### Git Commits
```bash
git pull  # Download der Änderungen die bisher auf dem GIT-Server verfügbar geworden sind.
git status  # Zeigt Dateinamen der geänderten Dateien

# Für das Hinzufügen von Änderungen gibt es mehrere Möglichkeiten
git add <dateiname>  # Fügt der Stage alle Änderung der Datei hinzu
git add -p
    # Hierdurch ist es möglich, einzelne Schnippsel 
    # per (y) oder (n) einzeln zu selektieren und hinzuzufügen.
    # Empfohlen, da man gut selektieren!
    
git commit  # Nachricht eingeben, Textdatei abspeichern
git push  # Lädt die Änderungen auf den GIT-Server hoch
```

### Flake8 (& PEP8) git hook
Sie sollten immer nur PEP8 konformen Code schreiben und in das Repository
einchecken. Es empfiehlt sich einen [Git
Hook](http://flake8.readthedocs.org/en/latest/vcs.html) einzurichten, welcher
Ihnen dabei hilft Ihren Code sauber zu halten.

Im Repository:
```bash
flake8 --install-hook git
git config flake8.strict true
```


### Working with Packages

Erstellen Sie keine Python-Dateien im Hauptverzeichnis dieses Repositories.
Gruppieren Sie Ihre Module immer in sinnvollen Python-Packages
(Unterverzeichnis mit `__init__.py`).



## Python Virtualenv

Für ein (Gruppen-)Pythonprojekt empfiehlt es sich in einem Python-Virtualenv zu
entwickeln. Damit ist sichergestellt, dass alle Entwickler (Studenten) und
Nutzer (Kursleitung) exakt den Code in der exakt gleichen Umgebung ausführen,
unabhängig von Hardware oder Betriebssystem. Lesen Sie sich dazu in
[virtualenv](https://docs.python.org/3/library/venv.html) ein.

Einmalige Einrichtung in jedem geklonten Repository:

```bash
# Mit anaconda (https://conda.io/docs/faq.html#creating-new-environments)
conda create -n virtualenv python=3.6 anaconda
python setup.py develop
```

```bash
# Mit einem system python
python -m venv virtualenv
. virtualenv/bin/activate
```

```bash
# Virtualenv via `[sudo] pip install virtualenv`
mkdir ~/venv
cd ~/venv
virtualenv -p ptyhon3 unikittypy
. ~/venv/unikittypy/bin/activate  # alternativ: source venv/bin/activate
```

In jeder Shell aus der Ihr Programm oder Tests gestartet werden muss das
virtualenv aktiviert werden (`. venv/bin/activate` oder `source venv/bin/activate`).



### Testen im Virtualenv

Starten Sie Ihre nosetests wie gehabt:

```bash
    nosetests -v
```

Sie können sich auch einen Test Coverage Report erstellen lassen:

```bash
    nosetests -v --with-coverage --cover-html
```

Den Coverage Report finden Sie dann in der Datei `cover/index.html`.
