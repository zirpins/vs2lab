# Labor Verteilte Systeme 2 (VS2Lab)

Das VS2Lab dient zur praktischen Veranschaulichung von Prinzipien verteilter Softwaresysteme sowie zur Einführung in deren softwaretechnische Konstruktion.

## 1. Vorgehen

Die Laborthemen orientieren sich an der inhaltlichen Struktur der Vorlesung VS2. Die Laborarbeit beinhaltet zunächst jeweils die Analyse gegebener Beispiele für einzelne Themenbereiche. Basierend darauf werden eigenständige Lösungen entwickelt.

Die Abgabe der Teilaufgaben erfolgt im [ILIAS Kurs 'Verteilte Systeme 2 Labor'](https://ilias.hs-karlsruhe.de/goto.php?target=crs_307307). Von dort erreichen sie auch die zugehörige Microsoft Teams Instanz des Labors in der Microsoft 365 Domäne der Hochschule. In Teams sind die genauen Regelungen der Abgabe und Abnahme durch die Dozenten zu finden.

---

**Hinweis**: Das Labor Repository wird laufend weiterentwickelt und aktualisiert. Es empfiehlt sich daher, das Labor als Git Repository zu belassen und regelmäßig per ``$ git pull`` aktuell zu halten.

---

## 2. Voraussetzungen

Das Labor wird im LKIT Rechner-Pool (Li 137) unterstützt. Die Laborplattform kann aber auch leicht auf dem eigenen Rechner eingerichtet werden. Dazu gehört:

- die Git Versionsverwaltung
- eine Laufzeitplattform mit Python und Redis
- eine Entwicklungs- und Arbeitsumgebung (bzw. IDE)

Alle Komponenten lassen sich auf den gängigen Plattformen relativ einfach installieren und sind z.T. schon standardmäßig vorhanden. Einige Tipps zur Installation folgen unten.

### NEU im Wintersemester 2021

Im Wintersemester 2021 wird eine neue virtualisierte Laborumgebung unterstützt, die sie leicht auf dem eigenen Rechner nutzen können. Die Lösung basiert auf der freien IDE [Visual Studio Code (VS Code)](https://code.visualstudio.com), die lokal auf dem Rechner installiert wird. Zur Bereitstellung einer vorkonfigurierten Laufzeitumgebung wird ein integrierter Docker Container verwendet. Dadurch braucht die Laufzeitumgebung des Labors nicht lokal auf ihrem System installiert zu werden.

- Microsoft beschreibt hier [Grundlagen zu Python in VS Code](https://code.visualstudio.com/docs/languages/python).
- Zur Bereitstellung einer vorkonfigurierten Laufzeitumgebung in VS Code verwenden wir die Erweiterung [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- Die Lösung setzt eine lokale Installation von Docker [Docker](https://www.docker.com) voraus.
  - Eine einfache Installation kann mit [Docker Desktop](https://www.docker.com/products/docker-desktop) erfolgen.

Installieren sie zunächst "Docker Desktop" und "Visual Studio Code" auf ihrem Rechner und starten sie beide Programme. Installieren sie dann in VS Code die Erweiterung "Remote Containers". Die Konfiguration der Laufzeitumgebung ist Teil des Labor-Repository. Nachdem das Labor Repository mit git kopiert wurde, wird in VSCode automatisch ein passender Docker Container dafür erzeugt (näheres dazu später).

### 2.1. Labor Repository

Das Labor nutzt die **Git** Versionsverwaltung und den **GitLab** Dienst zur Bereitstellung der Labordateien als git Repository. Git muss auf dem verwendeten Rechner verfügbar sein.

- Siehe [Git Homepage](https://git-scm.com)

Wenn ``git`` vorhanden ist, dann kopieren Sie das Labor Repository innerhalb eines Terminals wie folgt (aus dem lokalen Netz der Hochschule oder über VPN, das folgende Beispiel gilt für Linux/Mac):

```bash
git clone https://iz-gitlab-01.hs-karlsruhe.de/IWI-I/vs2lab.git
```

### 2.2. Laufzeitplattform

Das Labor basiert auf **Python** und setzt (ab Aufgabe 2) eine **Redis** Installation voraus.

#### 2.2.1. Python

Die Beispiele und Aufgaben sind weitgehend in Python 3 (>3.6) geschrieben.

[Python](https://de.wikipedia.org/wiki/Python_(Programmiersprache)) ist eine pragmatische und weit verbreitete objektorientierte (u.a.) Skriptsprache mit dynamischer Typisierung.

Python ist gut dokumentiert und einfach zu erlernen. Es ist für alle gängigen Plattformen frei verfügbar.

- [Python Website](https://www.python.org/)
- [Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Python Standard Library](https://docs.python.org/3/library/index.html)

Für das Labor muss Python verfügbar sein. Die vorgeschlagene Lösung mit VS Code und Remote Containers stellt dies automatisch sicher. Sonst (und nur dann!) ist eine Installation erforderlich:

- Prüfen einer vorhandenen Python Version: ``$ python3 --version``
- Python Installer unter [Python Downloads](https://www.python.org/downloads/)
- Alternativ über einen Package Manager in [Linux](https://docs.python-guide.org/starting/install3/linux/) oder [MacOS](https://docs.python-guide.org/starting/install3/osx/).

Verwendete Module sind u.a.

- os ([miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html))
- socket ([low-level networking interface](https://docs.python.org/3/library/socket.html))
- pickle ([python object serialization](https://docs.python.org/3/library/pickle.html))
- logging ([logging facility for Python](https://docs.python.org/3/library/logging.html))
- threading ([thread-based parallelism](https://docs.python.org/3/library/threading.html))
- multiprocessing ([process-based parallelism](https://docs.python.org/3.7/library/multiprocessing.html))

Die Pakete müssen nicht separat installiert werden. Wir binden sie bei der Einrichtung der Python Umgebung ein (siehe unten).

#### 2.2.2. Redis (erst ab Aufgabe 2)

Redis ist ein NOSQL Key-Value (KV) Store.

- Allgemeine Informationen auf der [Redis Website](ttp://redis.io/)

Für das Labor muss Redis verfügbar sein. Die vorgeschlagene Lösung mit VS Code und Remote Containers stellt dies automatisch sicher. Sonst (und nur dann!) ist eine Installation erforderlich:

- Installationsanleitung unter [Redis Quickstart](http://redis.io/topics/quickstart)

Das Labor braucht für viele Teile eine laufende Redis Instanz. Der Redis Server wird im Terminal wie folgt gestartet:

```bash
redis-server
```

Redis besitzt ein [Command Line Interface (CLI)](https://en.wikipedia.org/wiki/Command-line_interface) zur interaktiven Benutzung. In einer weiteren Shell kann damit der Redis Server beobachtet werden:

```bash
$ redis-cli
127.0.0.1:6379> monitor
OK
```

Zur Programmierung nutzen wir den [redis-py](https://github.com/andymccurdy/redis-py) Client für Python.

- Übersicht der API unter [Redis Command Reference](https://redis.io/commands)

Das Paket muss nicht separat installiert werden. Wir binden es bei der Einrichtung der Python Umgebung ein (siehe unten).

### 2.3. Package- und Dependency-Management

Die verwendeten Python Packages können per ``pip`` installiert werden. Das ist der integrierte Paketmanager des Python Laufzeitsystems. Bei Bedarf können Details im Tutorium nachgelesen werden:

- [Installing Packages](https://packaging.python.org/tutorials/installing-packages/)

Das Laborprojekt verwendet ``pip`` nicht direkt. Module sollen nämlich nicht im gesamten System sondern nur in einem isolierten Bereich für unser Labor installiert werden (unterschiedliche Projekte brauchen oft unterschiedliche
Versionen gleicher Module). In Python benutzt man dafür *virtuelle Umgebungen*, die mit ``virtualenv`` erstellt werden. Bei Bedarf können Details hier nachgelesen werden:

- [Creating Virtual Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

Das Laborprojekt verwendet auch ``virtualenv`` nicht direkt. Stattdessen wurde ``pipenv`` gewählt. Dadurch wird die Erstellung virtueller Umgebungen und die Installation von Modulen automatisch kombiniert und ist viel einfacher.
``pipenv`` muss ggf. installiert werden. Folgen Sie dieser Anleitung:

- [Managing Application Dependencies](https://packaging.python.org/tutorials/managing-dependencies/)

``pipenv`` erstellt bei der Nutzung eine Liste mit verwendeten Modulen (``Pipfile``, bzw. ``Pipfile.lock``),  die z.B. im Git Repository gut geteilt werden kann. Die Module dieser Liste können mit ``pipenv`` automatisch
installiert werden. Dadurch kann man die Module des Labors auf dem eigenen Rechner mit nur einem Befehl installieren (eine offene Internetverbindung wird dabei vorausgesetzt):

```bash
cd vs2lab # angenommen hier liegt das vs2lab Repo
pipenv install
```

Bei Bedarf können Details in den ``pipenv`` Docs nachgelesen werden:

- [Pipenv: Python Dev Workflow for Humans](https://pipenv.readthedocs.io/en/latest/)

### 2.4. Entwicklungsumgebung

#### 2.4.2. IDEs

Im Labor wird keine explizite Entwicklungsumgebung (IDE) für Python Skripte vorgeschrieben (und auch nicht dringend benötigt - es reicht im Prinzip ein Editor). Wir empfehlen und unterstützen aber die Nutzung von VS Code mit der Remote Comtainers Erweiterung. Einige alternative Möglichkeiten wären:

- [PyCharm](https://www.jetbrains.com/pycharm/) (auch im Pool LKIT vorhanden), hat u.a. einen sehr nützlichen Debugger.
- [Atom](https://atom.io) (auch im Pool LKIT vorhanden)
- [Spyder](https://www.spyder-ide.org) (Teil der Anaconda Distribution)

Für alternative IDEs können wir nur bedingt Support anbieten. 

#### 2.4.2. IPython (Interactive Python)

Bei der Arbeit mit Python wird nicht immer streng zwischen Entwicklungs- und Laufzeit von Systemen unterschieden. Entwickler können Teile des Systems wie Funktionen oder Objekte schon während der Entwicklung interaktiv ausprobieren, ohne ein explizites 'Hauptprogramm' ablaufen zu lassen. Auch Anwender können die Funktionen und Objekte von Python Systemen direkt aufrufen - ganz ohne klassische
GUI. Dies ist besonders im Bereich von Data Science Systemen üblich.

**IPython** ist ein [Command Line Interpreter
(CLI)](https://en.wikipedia.org/wiki/Command-line_interface) mit [Read-Eval-Print-Loop
(REPL)](https://en.wikipedia.org/wiki/Read–eval–print_loop) für Python. Damit wird die interaktive Arbeit mit Python Systemen in besonders leistungsfähiger und komfortabler Art möglich. Python Befehle werden hier interpretiert und deren
Ergebnis auf dem Bildschirm ausgegeben. Dies kann neben Text auch eine grafische Ausgabe (z.B. Diagramme) sein und innerhalb von GUI Anwendungen oder Webseiten eingebettet werden. Mit IPython ist zudem die interaktive Arbeit auf Cluster Systemen möglich. Näheres über IPython findet sich hier:

- [Jupyter and the future of IPython](https://ipython.org)
- [IPython Documentation](https://ipython.readthedocs.io/en/stable/)

Im VS2 Labor verwenden wir den enormen Umfang der IPython Features kaum. Wir ersetzen damit lediglich die GUI-Ebene der von uns erstellten verteilten Systeme. Alle diese Systeme werden entweder als Skripte ausgeführt oder über
eine IPython Erweiterung direkt interaktiv benutzt. Genauer verwenden wir dazu Jupyter Notebooks. IPython selber braucht deshalb auch nicht installiert werden.

#### 2.4.3. Jupyter

**Jupyter** ermöglicht die interaktive Nutzung von Programmierumgebungen verschiedener Art im Web Browser.

- [Project Jupyter](https://jupyter.org)

Im Browser können sogenannte *Notebooks* erstellt werden. Ein Notebook ist eine Mischung aus Text ([Markdown](https://de.wikipedia.org/wiki/Markdown)) und Code. Damit kann die interaktive Nutzung von Python Code erklärt werden. Näheres dazu findet sich unter folgendem Link:

- [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/)

Im Labor nutzen wir teilweise Jupyter Notebooks zur Erklärung der Beispiele oder zur Einreichung einer Aufgabe.

Jupyter wird im VS2Lab Repository automatisch installiert, wenn per ``pipenv install`` die Abhängigkeiten installiert werden. Sie starten den Jupyter notebook Server wie folgt:

```bash
cd vs2lab # angenommen hier liegt das vs2lab Repo
pipenv run jupyter notebook --ip 127.0.0.1
```

Es sollte sich ein Browserfenster mit einer Übersicht der Dateien im Ordner öffnen (lassen). Stoppen Sie den Server bei Bedarf mit ``ctrl-c``.

### 2.5. Tipps und Troubleshooting

#### Proxy

- Die Installation von Python Dependencies erfordert i.d.R. eine offene Internetverbindung. Die Rechner im LKIT-Pool sind entsprechend konfiguriert.
- Verwenden sie im Hochschulnetz möglichst HsKA-Open.

#### GIT

- Das Repository kann auch per ``ssh`` 'gecloned' werden. Hierzu benötigen Sie ein Benutzerkonto auf dem GitLab Server und müssen dort einen Schlüssel hinterlegen.

#### pipenv

- Für alle ``pipenv`` Aufrufe sollten Sie sich im Wurzelverzeichnis (vs2lab) befinden.
- Falls die Einrichtung der Umgebung per ``pipenv install``zu Fehlern führt, versuchen Sie, die Datei ``Pipfile.lock`` zu löschen.
- Als weitere Möglichkeit können Sie Packages einzeln installieren per ``pipenv install <modul>`` (Package Namen stehen im Pipfile)

#### docker

... to be continued.

## 3. Aufgaben

Die Aufgaben sind in den Unterverzeichnissen des Repositories beschrieben.
