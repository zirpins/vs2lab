# **Labor 3** - Kommunikation über Nachrichten mit ZeroMQ

Im dritten Labor untersuchen wir eine konkrete Technik der
*Nachrichtenkommunikation*. Dabei werden zunächst drei Beispiele der wichtigsten
Kommunikationsmuster mit dem [ZeroMQ Framework](http://zeromq.org) (0MQ)
betrachtet. Eines davon, das *Paralel Pipeline* Muster, bildet in der Folge die
Grundlage der Programmieraufgabe. Dabei wird ein einfaches System für die
verteilte Datenverarbeitung realisiert, das dem Grundprinzip von MapReduce
Algorithmen aus der bekannten [Hadoop
Plattform](https://de.wikipedia.org/wiki/Apache_Hadoop) entspricht.

Allgemeine **Ziele** dieses Labors:

- Untersuchung höherwertiger Dienste zur Nachrichtenkommunikation
- Kennenlernen verschiedener Kommunikationsmuster
- Anwendung des verbreiteten ZeroMQ Frameworks
- Veranschaulichung von Konzepten der Massendatenverarbeitung

## 1. Vorbereitung

### 1.1. Software installieren

Für diese Aufgabe werden keine neuen Installationen benötigt.

### 1.2. Projekt aktualisieren

Aktualisieren Sie die Kopie des VS2Lab Repositories auf Ihrem Arbeitsrechner aus
dem lokalen Netz der Hochschule oder über VPN (alle Beispiele für Linux/Mac):

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
git add . # ggf. eigene Änderungen vormerken
git commit -m 'update' # ggf eigene Änderungen per Commit festschreiben
git checkout master # branch auswählen (falls nicht schon aktiv)
git pull # aktualisieren
```

### 1.3. Python Umgebung installieren

Hier hat sich nichts geändert. Ggf. aktualisieren wie folgt:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
pipenv update
```

### 1.4. Beispielcode für diese Aufgabe

Wechseln Sie auf Ihrem Arbeitsrechner in das Unterverzeichnis dieser Aufgabe:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
cd lab3
```

## 2. Beispiele: einfache und erweiterte Kommunikationsmuster

Das Labor beginnt mit einigen Beispielen zum Messaging mit 0MQ. Die Beispiele
zeigen die drei gängigsten 0MQ-Muster.

Allgemeine Beschreibungen der Muster und der dazugehörigen 0MQ Sockets finden
sich z.B. hier:

- [Request-Reply: Ask and Ye Shall
  Receive](http://zguide.zeromq.org/py:all#Ask-and-Ye-Shall-Receive)
- [Publish-Subscribe: Getting the Message
  Out](http://zguide.zeromq.org/py:all#Getting-the-Message-Out)
- [Parallel Pipeline: Divide and
  Conquer](http://zguide.zeromq.org/py:all#Divide-and-Conquer)

### 2.1. Request-Reply

Das erste Beispiel zeigt, wie die gängige Request-Reply Kommunikation mit 0MQ
*Request-* und *Reply-Sockets* gegenüber den einfachen Berkeley Sockets
vereinfacht werden kann. 0MQ verwendet dabei Nachrichten statt Streams und es
wird keine Angabe der Übertragungsgröße benötigt. Ein Request Socket des Client
wird jeweils mit einem Reply Socket des Server gekoppelt.

Sie starten Server und Client nach dem nun schon bekannten Muster in zwei
Terminals.

#### Terminal1

```bash
cd ~/git/vs2lab/lab3/zmq1 # angenommen hier liegt das vs2lab Repo
pipenv run python server.py
```

#### Terminal2

```bash
cd ~/git/vs2lab/lab3/zmq1 # angenommen hier liegt das vs2lab Repo
pipenv run python client.py
```

Wir wollen nun noch etwas experimentieren. Zunächst schauen wir uns an, was es
bedeutet, dass 0MQ asynchron arbeitet. Probieren Sie dazu folgende Kombination
aus:

1. Terminal1: `pipenv run python client.py`
2. Terminal2: `pipenv run python server.py`

Die Kopplung von je zwei Sockets können Sie durch folgendes erweiterte
Experiment nachverfolgen:

1. Terminal1: `pipenv run python client.py`
2. Terminal2: `pipenv run python client1.py`
3. Terminal3: `pipenv run python server.py`

**Aufgabe Lab3.1:** Erklären Sie das Verhalten der Systeme in den beiden
Experimenten.

### 2.2. Publish-Subscribe

Mit dem Publish-Subscribe Muster lässt sich *1-n Kommunikation* (ein Sender, n
Empfänger) realisieren. Zudem können Nachrichten nach Themen gefiltert werden.

Wechseln Sie zunächst in das entsprechende Verzeichnis:

```bash
cd ~/git/vs2lab/lab3/zmq2 # angenommen hier liegt das vs2lab Repo
```

#### Experiment1

1. Terminal1: `pipenv run python server.py`
2. Terminal2: `pipenv run python client.py`
3. Terminal3: `pipenv run python client.py`

#### Experiment 2

1. Terminal1: `pipenv run python server.py`
2. Terminal2: `pipenv run python client.py`
3. Terminal3: `pipenv run python client1.py`

**Aufgabe Lab3.2:** Erklären Sie das Verhalten der Systeme in den beiden
Experimenten.

### 2.3. Parallel Pipeline

Das letzte Beispiel zeigt die Verteilung von Nachrichten von mehreren Sendern
auf mehrere Empfänger. Sogenannte 'Farmer' (`tasksrc.py`) erstellen Aufgaben
('Tasks') die von einer Menge von 'Workern' (`taskwork.py`) verarbeitet werden.
Die Tasks eines Farmers können an jeden Worker gehen und Worker akzeptieren
Tasks von jedem Farmer. Bei mehreren Alternativen Farmer/Worker Prozessen werden
die Tasks gleichverteilt.

`tasksrc.py` wird mit der Farmer-ID (1 oder 2) als Parameter gestartet. Jede
Farmer-ID darf nur einmal verwendet werden, da sie einen *PUSH-Socket* bindet.

`taskwork.py` wird mit der Worker-ID (beliebig) als Parameter gestartet. Die
Worker-ID dient nur der Anzeige. Es können beliebig viele Worker gestartet
werden, die jeweils mit ihrem *PULL-Sockets* die beiden Farmer kontaktieren.

Wechseln Sie zunächst in das entsprechende Verzeichnis:

```bash
cd ~/git/vs2lab/lab3/zmq3 # angenommen hier liegt das vs2lab Repo
```

Gehen sie nun wie folgt vor:

#### Experiment1

1. Terminal1: `pipenv run python tasksrc.py 1`
2. Terminal2: `pipenv run python tasksrc.py 2`
3. Terminal3: `pipenv run python taskwork.py 1`

#### Experiment 2

1. Terminal1: `pipenv run python taskwork.py 1`
2. Terminal2: `pipenv run python taskwork.py 2`
3. Terminal3: `pipenv run python tasksrc.py 1`

**Aufgabe Lab3.3:** Erklären Sie das Verhalten der Systeme in den beiden
Experimenten.

## 3 Aufgabe

In der Programmieraufgabe soll das Parallel Pipeline Muster verwendet werden, um
die verteilte Verarbeitung von Textdaten zu realisieren.

## 3.1 Übersicht

Wir wollen das berühmte **Wordcount** Beispiel für *Hadoop MapReduce* mit 0MQ
nachprogrammieren (näherungsweise). Das Prinzip ist wie folgt:

- Das verteilte System besteht aus einem zentralen 'Split'-Prozess ('Splitter'),
  einer variablem Menge von 'Map'-Prozessen ('Mapper') und einer festen Menge
  von 'Reduce'-Prozessen ('Reducer').
- Der Splitter lädt aus einer Datei zeilenweise Sätze aus und verteilt sie als
  Nachrichten gleichmäßig an die die Mapper.
- Ein Mapper nimmt jeweils Sätze entgegen. Jeder Satz wird dann zunächst in
  seine Wörter zerlegt. Schließlich ordnet der Mapper jedes Wort nach einem
  festen Schema genau einem der Reducer zu und sendet es als Nachricht an
  diesen.
- Ein Reducer sammelt die an ihn geschickten Wörter ein und zählt sie. Beachten
  sie: durch das feste zuordnungsschema kommen alle gleichen Wörter beim selben
  Reducer an und dieser Zählt 'seine' Wörter also garantiert komplett. Das
  Gesamtergebnis ergibt sich aus der Vereinigung der Teilergebnisse aller
  Reducer.

## 3.2 Aufgabe und Anforderungen kurz und knapp

Sie sollen die oben beschriebenen Prozesse als Python Skripte implementieren und
die Kommunikation zwischen diesen mit dem 0MQ Parallel Pipeline Muster
realisieren. Verwenden Sie:

- einen Splitter
- drei Mapper
- zwei Reducer

Der Splitter kann entweder eine Datei lesen oder die Sätze zufällig generieren.
Der Reducer soll bei jeder Aktualisierung den aktuellen Zähler des neuen Wortes
ausgeben.

### 3.3 Tipps

Neben dem dritten Beispiel liefert die Beschreibung in

- [Parallel Pipeline: Divide and
  Conquer](http://zguide.zeromq.org/py:all#Divide-and-Conquer)

ein nützliches Beispiel, an dem Sie sich orientieren können.

... stay tuned (Hinweise zur Installation/Konfiguration im Labor-README)

### 3.4 Abgabe

Die Abgabe erfolgt durch Abnahme durch einen Dozenten. Packen Sie den kompletten
Code zudem als Zip Archiv und laden Sie dieses im ILIAS hoch.
