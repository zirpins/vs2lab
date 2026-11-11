# **Labor 3** - Kommunikation über Nachrichten mit ZeroMQ

Im dritten Labor untersuchen wir eine konkrete Technik der
*Nachrichtenkommunikation*. Dabei werden zunächst drei Beispiele der wichtigsten
Kommunikationsmuster mit dem [ZeroMQ-Framework](http://zeromq.org) (0MQ)
betrachtet, die auch in Kapitel 4 der Vorlesung (Abschnitt „Messaging-Muster in
ZeroMQ“) vorgestellt werden. Eines davon, das *Pipeline*-Muster (bei ZeroMQ:
*Parallel Pipeline*), bildet in der Folge die Grundlage der Programmieraufgabe.
Dabei wird ein einfaches System für die verteilte Datenverarbeitung realisiert,
das dem Grundprinzip der MapReduce-Algorithmen aus der bekannten
[Hadoop-Plattform](https://de.wikipedia.org/wiki/Apache_Hadoop) entspricht.

Allgemeine **Ziele** dieses Labors:

- Untersuchung höherwertiger Dienste zur Nachrichtenkommunikation
- Kennenlernen verschiedener Kommunikationsmuster
- Anwendung des verbreiteten ZeroMQ-Frameworks
- Veranschaulichung von Konzepten der Massendatenverarbeitung

## 1. Vorbereitung

### 1.1. Software installieren

Für diese Aufgabe werden keine neuen Installationen benötigt. Sie arbeiten in der
Umgebung aus den vorherigen Aufgaben (optimalerweise Visual Studio Code mit dem
Dev Container). Das Package `pyzmq` ist Teil der vorgegebenen
Python-Umgebung.

### 1.2. Projekt aktualisieren

Aktualisieren Sie die Kopie des VS2Lab-Repositorys auf Ihrem Arbeitsrechner (alle Beispiele für Linux/Mac):

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
git add . # ggf. eigene Änderungen vormerken
git commit -m 'update' # ggf. eigene Änderungen per Commit festschreiben
git checkout main # Branch auswählen (falls nicht schon aktiv)
git pull # aktualisieren
```

Bei Problemen siehe Troubleshooting im [VS2Lab README](../README.md#25-tipps-und-troubleshooting).

### 1.3. Python-Umgebung installieren

Wechseln Sie in das Verzeichnis des Repositorys. In Visual Studio Code tun Sie dies bitte im Dev Container (d.h. Sie führen für den Ordner `vs2lab` vorher „Reopen in Container“ aus). Im Container liegt das Repository unter `/workspaces/vs2lab`; verwenden Sie dort diesen Pfad statt `~/git/vs2lab`. Die Umgebung hat sich gegenüber den vorherigen Aufgaben nicht geändert. Führen Sie `pipenv install` aus, falls Sie dies noch nicht getan haben oder die Pipfile durch das Update geändert wurde:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
pipenv install
```

### 1.4. Beispielcode für diese Aufgabe

Wechseln Sie auf Ihrem Arbeitsrechner (bzw. im Dev Container) in das Unterverzeichnis dieser Aufgabe:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
cd lab3
```

## 2. Beispiele: einfache und erweiterte Kommunikationsmuster

Das Labor beginnt mit einigen Beispielen zum Messaging mit 0MQ. Die Beispiele
zeigen die drei gängigsten 0MQ-Muster, die in Kapitel 4 der Vorlesung im
Abschnitt „Messaging-Muster in ZeroMQ“ mit je einer Folie vorgestellt werden
(„Request-Reply“, „Publish-Subscribe“, „Pipeline“). Der dortige Code
funktioniert nach demselben Prinzip wie die Beispiele hier.

Allgemeine Beschreibungen der Muster und der dazugehörigen 0MQ-Sockets finden
sich z.B. hier:

- [Request-Reply: Ask and Ye Shall
  Receive](https://zguide.zeromq.org/docs/chapter1/#Ask-and-Ye-Shall-Receive)
- [Publish-Subscribe: Getting the Message
  Out](https://zguide.zeromq.org/docs/chapter1/#Getting-the-Message-Out)
- [Parallel Pipeline: Divide and
  Conquer](https://zguide.zeromq.org/docs/chapter1/#Divide-and-Conquer)

### 2.1. Request-Reply

Das erste Beispiel zeigt, wie die gängige Request-Reply-Kommunikation mit 0MQ
*Request-* und *Reply-Sockets* gegenüber den einfachen Berkeley-Sockets
vereinfacht werden kann. 0MQ verwendet dabei Nachrichten statt Streams und es
wird keine Angabe der Übertragungsgröße benötigt. Ein Request-Socket des Clients
wird jeweils mit einem Reply-Socket des Servers gekoppelt.

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

Beenden lässt sich der Server durch eine Nachricht „STOP“, die `client.py` am
Ende sendet.

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

Mit dem Publish-Subscribe-Muster lässt sich *1-n-Kommunikation* (ein Sender, n
Empfänger) realisieren. Zudem können Nachrichten nach Themen gefiltert werden.
Der Server läuft endlos; beenden Sie ihn nach den Experimenten mit `Strg+C`.

Wechseln Sie zunächst in das entsprechende Verzeichnis:

```bash
cd ~/git/vs2lab/lab3/zmq2 # angenommen hier liegt das vs2lab Repo
```

#### Experiment 1

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

Das letzte Beispiel zeigt das Pipeline-Muster, d.h. die Verteilung von
Nachrichten von mehreren Sendern auf mehrere Empfänger. Sogenannte 'Farmer'
(`tasksrc.py`; in der Vorlesung „Producer“) erstellen Aufgaben ('Tasks'), die von
einer Menge von 'Workern' (`taskwork.py`) verarbeitet werden. Die Tasks eines
Farmers können an jeden Worker gehen und Worker akzeptieren Tasks von jedem
Farmer. Bei mehreren Farmer- bzw. Worker-Prozessen werden die Tasks reihum und
damit gleichmäßig verteilt.

`tasksrc.py` wird mit der Farmer-ID (1 oder 2) als Parameter gestartet. Jede
Farmer-ID darf nur einmal verwendet werden, da sie einen *PUSH-Socket* bindet.

`taskwork.py` wird mit der Worker-ID (beliebig) als Parameter gestartet. Die
Worker-ID dient nur der Anzeige. Es können beliebig viele Worker gestartet
werden, die jeweils mit ihrem *PULL-Socket* die beiden Farmer kontaktieren.
Ein Farmer endet nach 100 Tasks; die Worker laufen endlos und werden mit
`Strg+C` beendet.

Wechseln Sie zunächst in das entsprechende Verzeichnis:

```bash
cd ~/git/vs2lab/lab3/zmq3 # angenommen hier liegt das vs2lab Repo
```

Gehen Sie nun wie folgt vor:

#### Experiment 1

1. Terminal1: `pipenv run python tasksrc.py 1`
2. Terminal2: `pipenv run python tasksrc.py 2`
3. Terminal3: `pipenv run python taskwork.py 1`

#### Experiment 2

1. Terminal1: `pipenv run python taskwork.py 1`
2. Terminal2: `pipenv run python taskwork.py 2`
3. Terminal3: `pipenv run python tasksrc.py 1`

**Aufgabe Lab3.3:** Erklären Sie das Verhalten der Systeme in den beiden
Experimenten.

## 3. Aufgabe

In der Programmieraufgabe soll das Pipeline-Muster (siehe 2.3) verwendet werden,
um die verteilte Verarbeitung von Textdaten zu realisieren.

### 3.1. Übersicht

Wir wollen das berühmte **Wordcount**-Beispiel für *Hadoop MapReduce* mit 0MQ
(näherungsweise) nachprogrammieren. Das Prinzip ist wie folgt:

- Das verteilte System besteht aus einem zentralen 'Split'-Prozess ('Splitter'),
  einer variablen Menge von 'Map'-Prozessen ('Mapper') und einer festen Menge
  von 'Reduce'-Prozessen ('Reducer').
- Der Splitter liest aus einer Datei zeilenweise Sätze ein und verteilt sie als
  Nachrichten gleichmäßig an die Mapper.
- Ein Mapper nimmt jeweils Sätze entgegen. Jeder Satz wird dann zunächst in
  seine Wörter zerlegt. Schließlich ordnet der Mapper jedes Wort nach einem
  festen Schema genau einem der Reducer zu und sendet es als Nachricht an
  diesen.
- Ein Reducer sammelt die an ihn geschickten Wörter ein und zählt sie. Beachten
  Sie: Durch das feste Zuordnungsschema kommen alle gleichen Wörter beim selben
  Reducer an, und dieser zählt 'seine' Wörter also garantiert vollständig. Das
  Gesamtergebnis ergibt sich aus der Vereinigung der Teilergebnisse aller
  Reducer.

### 3.2. Aufgabe und Anforderungen kurz und knapp

Sie sollen die oben beschriebenen Prozesse als Python-Skripte implementieren und
die Kommunikation zwischen diesen mit dem 0MQ-Pipeline-Muster realisieren.
Verwenden Sie:

- einen Splitter
- drei Mapper
- zwei Reducer

Der Splitter kann entweder eine Datei lesen oder die Sätze zufällig generieren.
Der Reducer soll bei jeder Aktualisierung den aktuellen Zählerstand des soeben
gezählten Wortes ausgeben.

### 3.3. Tipps

- Neben dem dritten Beispiel (2.3) liefert die Beschreibung in
  [Parallel Pipeline: Divide and
  Conquer](https://zguide.zeromq.org/docs/chapter1/#Divide-and-Conquer) ein
  nützliches Beispiel, an dem Sie sich orientieren können.
- Die eingebaute Python-Funktion `hash()` liefert für Strings in jedem
  Prozess andere Werte (zufällige Initialisierung pro Prozessstart). Bedenken
  Sie dies, wenn mehrere Prozesse unabhängig voneinander dasselbe Ergebnis
  berechnen müssen.
- Testen Sie zunächst mit einer kleinen Textdatei, bei der Sie das Ergebnis von
  Hand nachzählen können.

### 3.4. Abgabe

Laden Sie den kompletten Code vor dem Abgabetermin als Zip-Archiv in ILIAS hoch. Die Abgabe erfolgt dann durch persönliche Abnahme im Labortermin (Zeitslot über den ILIAS-Buchungspool); ohne Upload erfolgt keine Abnahme. Bei der Abnahme muss jedes Gruppenmitglied den Code erklären können. Den Abgabetermin finden Sie im Ablaufplan.
