# Labor Verteilte Systeme 2 (VS2Lab)

Das VS2Lab dient zur praktischen Veranschaulichung von Prinzipien verteilter
Softwaresysteme sowie zur Einführung in deren softwaretechnische Konstruktion.

## 1. Vorgehen

Die Laborthemen orientieren sich an der inhaltlichen Struktur der Vorlesung VS2.
Die Laborarbeit beinhaltet zunächst die Analyse gegebener Beispiele für einzelne
Themenbereiche. Basierend darauf werden eigenständige Lösungen entwickelt.

Neben den Pflichtaufgaben kann durch Bearbeitung einer Zusatzaufgabe ein Bonus
für die Modulklausur erworben werden.

Laboraufgaben können in kleinen Teams bis maximal 3 Personen bearbeitet werden.
Die Abnahme erfolgt bei den Betreuern im Kurs (grundsätzlich nur für anwesende
Teammitglieder) und per Upload im ILIAS.

---

**Hinweis**: Das Labor Repository ist zur Zeit nicht vollständig und wird über
das Semester laufend aktualisiert. Es empfiehlt sich daher, das Labor als Git
Repository zu belassen und regelmäßig per ``$ git pull`` aktuell zu halten.

---

## 2. Voraussetzungen

Das Labor wird zur Zeit nicht aktiv in den IWI Rechner-Pools unterstützt. Es
wird daher empfohlen, die Laborplattform auf dem Laptop einzurichten. Dazu
gehört:

- Git Versionsverwaltung
- Laufzeitplattform mit Python und Redis
- Entwicklungs- und Arbeitsumgebung

Alle Komponenten lassen sich auf den gängigen Plattformen trivial einfach
installieren und sind z.T. schon standardmäßig vorhanden. Einige Tipps zur
Installation folgen unten.

### 2.1. Labor Repository

Das Labor nutzt die Git Versionsverwaltung und den GitLab Dienst zur
Bereitstellung der Labordateien als git Repository. Git muss auf dem verwendeten
Rechner verfügbar sein.

- [Git](https://git-scm.com)

Wenn ``git`` vorhanden ist, dann kopieren Sie das Labor Repository wie folgt
(aus dem lokalen Netz der Hochschule oder über VPN):

```bash
git clone https://IWI-I-gitlab-1.HS-Karlsruhe.DE:2443/zich0001/vs2lab.git
```

### 2.2. Laufzeitplattform

Das Labor basiert auf **Python** und setzt (ab Aufgabe 2) eine **Redis**
Installation voraus.

#### 2.2.1. Python

Die Beispiele und Aufgaben sind weitgehend in Python 3 (~3.6) geschrieben.

[Python](https://de.wikipedia.org/wiki/Python_(Programmiersprache)) ist eine
pragmatische und weit verbreitete objektorientierte (u.a.) Skriptsprache mit
dynamischer Typisierung.

Python ist gut dokumentiert und einfach zu erlernen. Es ist für alle gängigen
Plattformen frei verfügbar.

- [Python Website](https://www.python.org/)
- [Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Python Standard Library](https://docs.python.org/3/library/index.html)

Für das Labor muss Python lokal verfügbar sein. Oft (vor allem bei Linux oder
OSX) ist das schon der Fall. Sonst ist eine Installation erforderlich:

- Prüfen einer vorhandenen Python Version: ``$ python3 --version`
- Python Installer unter  [Python Downloads](https://www.python.org/downloads/)
- Alternativ über einen Package Manager in
  [Linux](https://docs.python-guide.org/starting/install3/linux/) (z.B.
  Ubuntu:``$ sudo apt-get install python3.6``) oder
  [MacOS](https://docs.python-guide.org/starting/install3/osx/)
  ([Homebrew](https://docs.brew.sh/Homebrew-and-Python); ``$ brew install
  python``)

Verwendete Module sind u.a.

- os ([miscellaneous operating system
  interfaces](https://docs.python.org/3/library/os.html))
- socket ([low-level networking
  interface](https://docs.python.org/3/library/socket.html))
- pickle ([python object
  serialization](https://docs.python.org/3/library/pickle.html))
- logging ([logging facility for
  Python](https://docs.python.org/3/library/logging.html))
- threading ([thread-based
  parallelism](https://docs.python.org/3/library/threading.html))
- multiprocessing ([process-based
  parallelism](https://docs.python.org/3.7/library/multiprocessing.html))

Die Pakete müssen nicht separat installiert werden. Wir binden sie bei der
Einrichtung der Python Umgebung ein (siehe unten).

#### 2.2.2. Redis (erst ab Aufgabe 2)

Redis ist ein NOSQL Key-Value-Store.

- Allgemeine Informationen auf der [Redis Website](ttp://redis.io/)

Redis muss zunächst installiert werden:

- Installationsanleitung unter [Redis
  Quickstart](http://redis.io/topics/quickstart)

Das Labor braucht für viele Teile eine laufende Redis Instanz. Der Redis Server
wird wie folgt gestartet:

```bash
redis-server
```

Redis besitzt ein [Command Line Interface
(CLI)](https://en.wikipedia.org/wiki/Command-line_interface) zur interaktiven
Benutzung. In einer weiteren Shell kann damit der Redis Server beobachtet
werden:

```bash
$ redis-cli
127.0.0.1:6379> monitor
OK
```

Zur Programmierung nutzen wir den
[redis-py](https://github.com/andymccurdy/redis-py) Client für Python.

- Übersicht der API unter [Redis Command Reference](https://redis.io/commands)

Das Paket muss nicht separat installiert werden. Wir binden es bei der
Einrichtung der Python Umgebung ein (siehe unten).

### 2.3. Package- und Dependency-Management

Die verwendeten Python Packages können per ``pip`` installiert werden. pip ist
der integrierte Paketmanager des Python Laufzeitsystems. Bei Bedarf können
Details im Tutorium nachgelesen werden:

- [Installing
  Packages](https://packaging.python.org/tutorials/installing-packages/)

Das Laborprojekt verwendet ``pip`` nicht direkt. Module sollen nämlich nicht im
gesamten System sondern nur in einem isolierten Bereich für unser Labor
installiert werden (unterschiedliche Projekte brauchen oft unterschiedliche
Versionen gleicher Module). In Python benutzt man dafür *virtuelle Umgebungen*,
die mit ``virtualenv`` erstellt werden. Bei Bedarf können Details im Tutorium
nachgelesen werden:

- [Creating Virtual
  Environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

Das Laborprojekt verwendet auch ``virtualenv`` nicht direkt. Stattdessen wurde
``pipenv`` verwendet. Dadurch wird die Erstellung virtueller Umgebungen und die
Installation von Modulen automatisch kombiniert und ist viel einfacher.
``pipenv`` muss ggf. installiert werden. Folgen Sie dieser Anleitung:

- [Managing Application
  Dependencies](https://packaging.python.org/tutorials/managing-dependencies/)

``pipenv`` erstellt bei der Nutzung eine Liste mit verwendeten Modulen
(``Pipfile``, bzw. ``Pipfile.lock``),  die z.B. im Git Repository gut geteilt
werden kann. Die Module dieser Liste können mit ``pipenv`` automatisch
installiert werden. Dadurch kann man die Module des Labors auf dem eigenen
Rechner mit nur einem Befehl installieren:

```bash
cd vs2lab # angenommen hier liegt das vs2lab Repo
pipenv install
```

Bei Bedarf können Details in den ``pipenv`` Docs nachgelesen werden:

- [Pipenv: Python Dev Workflow for
  Humans](https://pipenv.readthedocs.io/en/latest/)

### 2.4. Entwicklungsumgebung

#### 2.4.2. IDEs

Es wird keine explizite Entwicklungsumgebung (IDE) für Python Skripte vorgegeben
(und auch nicht dringend benötigt - es reicht im Prinzip ein Editor). Einige
Möglichkeiten sind:

- [PyCharm](https://www.jetbrains.com/pycharm/) (auch im Pool LKIT vorhanden),
  hat u.a. einen sehr nützlichen Debugger.
- [Atom](https://atom.io) (auch im Pool LKIT vorhanden)
- [Spyder](https://www.spyder-ide.org) (Teil der Anaconda Distribution, s.u.)

#### 2.4.2. IPython (Interactive Python)

Bei der Arbeit mit Python wird nicht immer streng zwischen Entwicklungs- und
Laufzeit von Systemen unterschieden. Entwickler können Teile des Systems wie
Funktionen oder Objekte schon während der Entwicklung interaktiv ausprobieren,
ohne ein explizites 'Hauptprogramm' ablaufen zu lassen. Auch Anwender können die
Funktionen und Objekte von Python Systemen direkt aufrufen, auch ohne klassische
GUI. Dies ist besonders im Bereich von Data Science Systemen üblich.

**IPython** ist ein [Command Line Interpreter
(CLI)](https://en.wikipedia.org/wiki/Command-line_interface) mit
[Read-Eval-Print-Loop
(REPL)](https://en.wikipedia.org/wiki/Read–eval–print_loop) für Python. Damit
wird die interaktive Arbeit mit Python Systemen in besonders leistungsfähiger
und komfortabler Art möglich. Python Befehle werden hier interpretiert und deren
Ergebnis auf dem Bildschirm ausgegeben. Dies kann neben Text auch eine grafische
Ausgabe (z.B. Diagramme) sein und innerhalb von GUI Anwendungen oder Webseiten
eingebettet werden. Mit IPython ist zudem die interaktive Arbeit auf Cluster
Systemen möglich. Näheres über IPython findet sich hier:

- [Jupyter and the future of IPython](https://ipython.org)
- [IPython Documentation](https://ipython.readthedocs.io/en/stable/)

Im VS2 Labor verwenden wir den enormen Umfang der IPython Features kaum. Wir
ersetzen damit lediglich die GUI-Ebene der von uns erstellten verteilten
Systeme. Alle diese Systeme werden entweder als Skripte ausgeführt oder über
eine IPython Erweiterung direkt interaktiv benutzt. Genauer verwenden wir dazu
Jupyter Notebooks. IPython selber braucht deshalb auch nicht installiert werden.

#### 2.4.3. Jupyter

**Jupyter** ermöglicht die interaktive Nutzung von Programmierumgebungen
verschiedener Art im Web Browser.

- [Project Jupyter](https://jupyter.org)

Im Browser können sogenannte *Notebooks* erstellt werden. Ein Notebook ist eine
Mischung von Text ([Markdown](https://de.wikipedia.org/wiki/Markdown)) und Code.
Damit kann die interaktive Nutzung von Python Code erklärt werden. Näheres dazu
findet sich unter folgendem Link:

- [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/)

Im Labor nutzen wir teilweise Jupyter Notebooks zur Erklärung der Beispiele oder
zur Einreichung einer Aufgabe.

Jupyter wird im VS2Lab Repository automatisch installiert, wenn per ``pipenv
install`` die Abhängigkeiten installiert werden. Sie starten den Jupyter
notebook Server wie folgt:

```bash
cd vs2lab # angenommen hier liegt das vs2lab Repo
pipenv run jupiter notebook
```

Es sollte sich ein Browserfenster mit einer Übersicht der Dateien im Ordner
öffnen. Stoppen Sie den Server bei Bedarf mit ``ctrl-c``.

### 2.5. Hinweise zur Installation

#### 2.5.1. Anaconda

Für Python existieren auch komplette Distributionen, die verschiedene Tools
beinhalten, z.B.:

- [Anaconda](https://www.anaconda.com)

Anaconda vereinfacht die Installation und beinhaltet z.B. schon die *Spyder IDE*
und *Jupiter Notebooks*. Zudem verwendet Anaconda eine eigene Lösung für
virtuelle Umgebungen in Python. Es zielt vor allem auf wissenschaftliche
Anwendungen von Python. Das VS2 Labor ist nicht auf Anaconda ausgelegt, sollte
aber darauf übertragbar sein.

### 2.5.2. Troubleshooting

#### GIT

- Bei Problemen mit dem selbst-signierten SSL Zertifikat des GitLab Servers kann
  dessen Verifikation wie folgt umgangen werden:

```bash
git -c http.sslVerify=false clone https://IWI-I-gitlab-1.HS-Karlsruhe.DE:2443/zich0001/vs2lab.git
```

- Bei Problemen mit der HTTPS Verbindung kann das Repository auch per ``ssh``
  'gecloned' werden. Hierzu benötigen Sie ein Benutzerkonto auf dem GitLab
  Server und müssen dort einen Schlüssel hinterlegen. Bitte wenden Sie sich dazu
  bei Bedarf an einen Dozenten.

#### pipenv

- Für alle ``pipenv`` Aufrufe sollten Sie sich im Wurzelverzeichnis (vs2lab)
  befinden.
- Falls die Einrichtung der Umgebung per ``pipenv install``zu Fehlern führt,
  versuchen Sie, die Datei ``Pipfile.lock`` zu löschen.
- Als weitere Möglichkeit können Sie Packages einzeln installieren per ``pipenv
  install <modul>`` (Package Namen stehen im Pipfile)

... to be continued.

## 3. Aufgaben

Die Aufgaben sind in den Unterverzeichnissen des Repositories beschrieben.
