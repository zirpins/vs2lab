# **Labor 2** - Kommunikation per Remote Procedure Call (RPC)

Das zweite Labor beschäftigt sich hauptsächlich mit **RPC-Kommunikation** in verschiedenen Varianten. Ein erstes Beispiel zeigt eine einfache RPC-Implementierung im Detail und nutzt dabei einen generischen **Kommunikationskanal (Channel)**, den wir später noch öfter verwenden werden.

Ein zweites Beispiel zeigt kurz die Anwendung des speziellen RPC-Frameworks **RPyC**. Ein drittes, optionales Beispiel zeigt mit **gRPC** ein aktuelles RPC-Framework mit Schnittstellenbeschreibung (IDL) und generierten Stubs. Die Programmieraufgabe beschäftigt sich mit der Erweiterung der einfachen RPC-Implementierung um einen **asynchronen RPC mit Callback**.

Allgemeine **Ziele** dieses Labors:

- *Verständnis* von **RPCs** und deren *Anwendung*
- Fähigkeit zur *Implementierung* von **RPC-Middleware**
- Kennenlernen des **`lab_channel`-Mechanismus**
- Verständnis von **Client-Threads**
- Verwendung des Python-Moduls **`threading`**

## 1. Vorbereitung

### 1.1. Software installieren

Sie haben in der [Vorbereitung von Aufgabe 1](../lab1/README.md#1-vorbereitung) bereits eine Umgebung mit Git, Docker, Python 3, Pipenv, IDE/Editor und Jupyter eingerichtet. Optimalerweise haben Sie dies mit Visual Studio Code und der Dev-Containers-Erweiterung realisiert.

In dieser Aufgabe brauchen wir noch eine weitere Komponente:

- **Redis** (ein verbreiteter NoSQL-Key-Value-Store)

Wenn Sie VS Code mit dem Dev Container verwenden, ist Redis schon vorhanden. Andernfalls orientieren Sie sich zur Einrichtung an der [Beschreibung im VS2Lab README](../README.md#222-redis-erst-ab-aufgabe-2).

### 1.2. Projekt klonen und/oder aktualisieren

Erstellen Sie eine Kopie des VS2Lab-Repositorys auf Ihrem Arbeitsrechner (alle Beispiele für Linux/Mac):

```bash
mkdir -p ~/git # Verzeichnis für Git-Projekte (optional)
cd ~/git
git clone https://github.com/zirpins/vs2lab.git
```

Falls Sie es schon haben, aktualisieren Sie das Repository wie folgt:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
git pull
```

Bei Problemen siehe Troubleshooting im [VS2Lab README](../README.md#25-tipps-und-troubleshooting).

### 1.3. Python-Umgebung installieren

Wechseln Sie in das Verzeichnis des Repositorys. In Visual Studio Code tun Sie dies bitte im Dev Container (d.h. Sie führen für den Ordner `vs2lab` vorher „Reopen in Container“ aus). Im Container liegt das Repository unter `/workspaces/vs2lab`; verwenden Sie dort diesen Pfad statt `~/git/vs2lab`. Falls nicht schon geschehen, installieren Sie die vorgegebenen Packages in eine virtuelle Umgebung für Python. Für diese Aufgabe kommen mit `grpcio` und `grpcio-tools` neue Packages hinzu (siehe 2.3), führen Sie `pipenv install` also auch dann aus, wenn Sie die Umgebung schon für Aufgabe 1 eingerichtet haben.

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
pipenv install
```

### 1.4. Beispielcode für diese Aufgabe

Wechseln Sie auf Ihrem Arbeitsrechner (bzw. im Dev Container) in das Unterverzeichnis dieser Aufgabe:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
cd lab2
```

## 2. Beispiele für RPC-Kommunikation

Das Labor beginnt mit drei Beispielen zur RPC-Kommunikation (2.1 und 2.3 sind optional, 2.2 ist die Grundlage der Programmieraufgabe). Hintergrund zu RPC finden Sie in Kapitel 4 (Kommunikation) der Vorlesung.

### 2.1. Anwendung von RPCs auf *Sprachebene* mit dem **RPyC**-Framework (optional)

Zunächst wollen wir ein „echtes“ RPC-Framework benutzen. Das Beispiel dient zur Veranschaulichung von RPCs auf der Sprachebene („sprachbasierte Unterstützung“ in Kapitel 4), die die Kommunikation in verteilten Systemen fast komplett verstecken und sehr einfach benutzbar machen.

Sie können das Beispiel ausprobieren und bei Interesse damit experimentieren. Für die spätere Programmieraufgabe wird es nicht gebraucht.

Das Beispiel finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/rpyc
$ ls
client.py  constRPYC.py  context.py  server.py
```

Die Datei `server.py` enthält den Server-Prozess, der die Funktionen seiner Klasse `DBList` als *Service* entfernt nutzbar macht. Der Client-Prozess in `client.py` ruft diese Operationen des Services über eine Server-Verbindung direkt auf.

Für Client und Server besteht kein wesentlicher Unterschied zur Programmierung mit normalen Objekten. Die Verteilung wird durch das Framework transparent gemacht.

Wie alle Dateien mit Präfix `const` enthält `constRPYC.py` Konstanten, die in mehreren anderen Skripten verwendet werden (vornehmlich Adressen und Kodierungen). Das Skript `context.py` dient hier (und in fast jedem Beispiel) zur Einbindung des `lib` Package auf der obersten Ebene des Repositories.

Zum Ausprobieren starten Sie erst den Server und dann den Client. (Tipp: In einer IDE wie VS Code können Sie `pipenv run` in den Anweisungen weglassen, falls Sie die Pipenv-Umgebung dort als Python-Interpreter festgelegt haben.)

```bash
cd ~/git/vs2lab/lab2/rpyc
pipenv run python server.py
```

In einem anderen Terminal:

```bash
cd ~/git/vs2lab/lab2/rpyc
pipenv run python client.py
```

Detaillierte Informationen zu RPyC finden Sie hier:

- [RPyC - Transparent, Symmetric Distributed Computing](https://rpyc.readthedocs.io/en/latest/)
- Für unser Beispiel: [Part 3: Services and New Style RPyC](https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html)

### 2.2. Implementierung einer einfachen *RPC-Middleware*

Wir betrachten nun die Realisierung eines RPC-Systems auf der Middleware-Ebene. Das Beispiel finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/rpc
$ ls
constRPC.py  context.py  rpc.py  runcl.py  runsrv.py
```

Die RPC-Implementierung befindet sich in `rpc.py` mit Klassen für Client- und Server-Stub. Wie in der Vorlesung (Kapitel 4, „Grundlegende Funktion des RPC“) erstellen die Stubs Nachrichten für Request sowie Reply und übertragen diese Nachrichten über einen Kommunikationskanal. Dieser RPC ist *synchron*: Der Client-Stub wartet nach dem Senden des Requests, bis die Antwort eintrifft.

#### 2.2.1. Kommunikation per `lab_channel`

Der Kommunikationskanal wird im Modul `vs2lab/lib/lab_channel.py` implementiert. `lab_channel` stellt einen Dienst für *persistente asynchrone Kommunikation* bereit. Dazu benutzt das Modul eine *Redis-Datenbank*, auf der Warteschlangen für Nachrichten gespeichert werden. Das Modul wird detailliert in der Dokumentation [The Channel Package](../docs/channel.pdf) beschrieben.

Ein Beispiel zur allgemeinen Verwendung finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/channel
$ ls
channel.py  context.py  runcl.py  runsrv.py
```

Zum Ausprobieren starten Sie erst Redis, dann den Server und schließlich den Client, jeweils in einem eigenen Terminal.

- Terminal 1

```bash
redis-server
```

- Terminal 2

```bash
cd ~/git/vs2lab/lab2/channel
pipenv run python runsrv.py
```

- Terminal 3

```bash
cd ~/git/vs2lab/lab2/channel
pipenv run python runcl.py
```

#### 2.2.2. Zurück zum RPC-Beispiel

Nun können wir noch das eigentliche RPC-Beispiel ausprobieren. Falls Sie den Redis-Server im Channel-Beispiel gestartet haben, können Sie diesen weiter verwenden, sonst starten Sie ihn jetzt (siehe oben).

Client- und Server-Prozess werden durch `runcl.py` und `runsrv.py` realisiert. Die Prozesse verwenden die in `rpc.py` bereitgestellten Stubs. Sie werden wie üblich in getrennten Terminals gestartet:

- Terminal 1

```bash
cd ~/git/vs2lab/lab2/rpc
pipenv run python runsrv.py
```

- Terminal 2

```bash
cd ~/git/vs2lab/lab2/rpc
pipenv run python runcl.py
```

### 2.3. RPC mit Schnittstellenbeschreibung: **gRPC** (optional)

[gRPC](https://grpc.io) ist ein heute weit verbreitetes RPC-Framework, z.B. für die Kommunikation zwischen Microservices. Anders als bei RPyC wird die Schnittstelle sprachunabhängig in einer *Interface Definition Language* (IDL) beschrieben, den **Protocol Buffers**. Der Compiler `protoc` erzeugt daraus Client-Stub und Server-Basisklasse für die gewünschte Programmiersprache. Das Beispiel entspricht der Vorlesungsfolie „RPC heute: gRPC“ (Kapitel 4) und implementiert denselben `DBList`-Dienst wie das RPyC-Beispiel, diesmal mit typisierter Schnittstelle. Für die Programmieraufgabe wird es nicht gebraucht.

Das Beispiel finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/grpc
$ ls
client.py  constGRPC.py  context.py  dblist.proto  server.py  watch.py
```

- `dblist.proto` beschreibt die Schnittstelle: `Append` ist ein normaler (unärer) RPC, `Watch` ein *Server-Streaming*-RPC, der alle gespeicherten und danach jedes neu angehängte Element als eigene Nachricht liefert.
- `server.py` implementiert den Dienst (Klasse `DBList` erbt von der generierten Basisklasse `DBListServicer`) und bearbeitet Aufrufe in einem Thread-Pool.
- `client.py` ruft `Append` einmal synchron mit Deadline (`timeout=1.0`) und einmal asynchron (`future`) auf und zeigt, dass ein falscher Parametertyp schon im Client-Stub auffällt.
- `watch.py` abonniert den Stream von `Watch` für 30 Sekunden.

Die Pakete `grpcio` und `grpcio-tools` sind im `Pipfile` eingetragen. Falls Ihre Umgebung älter ist, installieren Sie sie mit `pipenv install` nach.

Vor dem ersten Start erzeugen Sie die Stubs aus der IDL (und erneut nach jeder Änderung an `dblist.proto`):

```bash
cd ~/git/vs2lab/lab2/grpc
pipenv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dblist.proto
```

Dabei entstehen `dblist_pb2.py` (Nachrichtentypen) und `dblist_pb2_grpc.py` (Client-Stub `DBListStub`, Server-Basisklasse `DBListServicer`). Schauen Sie sich die generierten Dateien kurz an. Sie werden nicht ins Repository eingecheckt (siehe `.gitignore`).

Zum Ausprobieren starten Sie erst den Server:

```bash
cd ~/git/vs2lab/lab2/grpc
pipenv run python server.py
```

In einem zweiten Terminal starten Sie den Watcher:

```bash
cd ~/git/vs2lab/lab2/grpc
pipenv run python watch.py
```

In einem dritten Terminal rufen Sie (mehrfach) den Client auf und beobachten die Ausgaben des Watchers:

```bash
cd ~/git/vs2lab/lab2/grpc
pipenv run python client.py
```

Vergleichen Sie mit dem RPyC-Beispiel: Wo steht die Schnittstelle, wer erzeugt die Stubs, und wann fällt ein Typfehler auf?

Detaillierte Informationen zu gRPC finden Sie hier:

- [gRPC Quick Start für Python](https://grpc.io/docs/languages/python/quickstart/)
- [Protocol Buffers: Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)

## 3. Aufgabe

In der Programmieraufgabe sollen Sie nun das System aus Beispiel 2.2 zu einem **asynchronen RPC mit Callback** weiterentwickeln (vgl. „Asynchroner RPC“ in Kapitel 4).

### 3.1. Übersicht

Der RPC aus Beispiel 2.2 ist synchron, d.h. der Client-Prozess wartet nach dem Operationsaufruf, bis das Ergebnis vom Server-Prozess zurückgesendet wurde. Wenn die Ausführung der Operation aufwendig ist, muss der Client-Prozess dabei ggf. lange warten. In manchen Fällen kann es sich lohnen, diese Wartezeit für andere Aktivitäten zu nutzen.

Bei einem asynchronen RPC erfolgt die Synchronisierung von Client und Server sofort nach Annahme eines Requests durch den Server, indem dieser eine Bestätigung (**ACK**nowledgement) zurücksendet. Der Client kann nun mit anderen Aktivitäten fortfahren. Wenn der Server das Ergebnis fertiggestellt hat, sendet er es zum Client zurück. Im Client-Prozess wird dann eine Callback-Funktion aufgerufen, die das Ergebnis verarbeitet.

Erweitern Sie nun die Client- und Server-Klassen so, dass diese den oben beschriebenen Ablauf implementieren. Nutzen Sie dabei den `lab_channel`, um die zusätzliche Kommunikation des Acknowledgements zu realisieren.

Um beim Warten auf die Server-Antworten den Client-Prozess nicht zu blockieren, gibt es verschiedene Möglichkeiten. Eine davon sind **Threads**: nebenläufige Ausführungsstränge innerhalb eines Prozesses, die sich dessen Speicher teilen. Threads sind Thema von Kapitel 3 (Prozesse) der Vorlesung; die für diese Aufgabe nötigen Grundlagen werden im Labor kurz erklärt und stehen in Abschnitt 3.1.1.

Sie sollen in dieser Aufgabe einen **Thread** verwenden, um auf die Server-Antworten zu warten. Ferner soll die Verarbeitung des Ergebnisses ebenfalls in diesem Thread durch Aufruf einer **Callback-Funktion** erfolgen. Die Callback-Funktion soll der Anwender als Parameter beim RPC-Aufruf mitliefern, z.B. `cl.append(data, db_list, callback)`.

#### 3.1.1. Das Python `threading` Modul

Threads werden in Python durch das Modul `threading` realisiert. Das Skript `lab2/threading/async_zip.py` zeigt ein kleines Beispiel zur Verwendung von Threads und wird wie folgt gestartet:

```bash
cd ~/git/vs2lab/lab2/threading
pipenv run python async_zip.py
```

Die Klasse `AsyncZip` leitet von `threading.Thread` ab. Die Arbeit des Threads steht in der Methode `run()`; `start()` startet sie nebenläufig, `join()` wartet auf das Ende des Threads. Das Hauptprogramm läuft in der Zwischenzeit weiter.

Python-Threads erlauben im Standardinterpreter (CPython) keine echte Parallelität der Ausführung, sind aber gerade bei blockierenden I/O-Aufrufen (z.B. Warten auf eine Nachricht) sehr nützlich, da sie die abwechselnde Ausführung von I/O- und weiteren Anweisungen ohne Wartezeit erlauben.

Die ``threading``-API ist hier dokumentiert:

- [`threading` – Thread-based parallelism](https://docs.python.org/3/library/threading.html)

### 3.2. Aufgabe und Anforderungen kurz und knapp

- Erweitern Sie Client- und Server-Klassen des RPC-Beispiels in `rpc/rpc.py` so, dass sie den Ablauf eines asynchronen RPC realisieren.
- Passen Sie auch die dazugehörigen Client- und Server-Skripte des RPC-Beispiels `rpc/runcl.py` und `rpc/runsrv.py` entsprechend an.
- Die schon vorhandene `append`-Funktion kann beibehalten werden, nur eben asynchron.
- Der Server bestätigt den Request sofort mit einem ACK (über den `lab_channel`).
- Pausieren Sie den Server nach der Bestätigung des Requests für 10 Sekunden, um eine lange Ausführungszeit zu simulieren.
- Verwenden Sie im Client einen Thread zum Warten und Reagieren auf Server-Antworten.
- Verwenden Sie zur Verarbeitung des Ergebnisses eine Callback-Funktion, die der Anwender beim Aufruf mitliefert.
- Machen Sie im Client einige Ausgaben auf der Konsole, um zu zeigen, dass er während des Wartens aktiv ist.
- Am Ende soll der Client das Ergebnis des RPC auf der Konsole ausgeben (in der Callback-Funktion).

### 3.3. Tipps

- Starten Sie Redis, Server und Client wie in 2.2 in getrennten Terminals. `runsrv.py` leert beim Start die Redis-Datenbank; starten Sie also bei Problemen mit alten Nachrichten den Server neu.
- Der Kanal liefert die Nachrichten eines Absenders in der Reihenfolge des Sendens. Der Server schickt erst das ACK, dann (nach der Pause) das Ergebnis; der Client empfängt beides mit `receive_from`.
- `receive_from` blockiert, bis eine Nachricht eintrifft (optional mit `timeout`). Der Client-Aufruf von `append` kehrt nach dem ACK zurück; erst der Thread wartet auf das Ergebnis.
- Die Verbindung zum Kanal gehört zum Prozess, nicht zum Thread: Der Thread im Client kann denselben `Channel` wie der Hauptthread verwenden.
- Lassen Sie den Client-Hauptthread während des Wartens z.B. in einer Schleife mit `time.sleep(1)` Ausgaben machen und warten Sie am Ende mit `join()` auf den Thread, bevor Sie den Client mit `stop()` beenden.
- Den Inhalt der Redis-Warteschlangen können Sie mit `redis-cli` und dem Befehl `monitor` beobachten (siehe [VS2Lab README](../README.md#222-redis-erst-ab-aufgabe-2)).

### 3.4. Abgabe

Laden Sie den kompletten Code vor dem Abgabetermin als Zip-Archiv in ILIAS hoch. Die Abgabe erfolgt dann durch persönliche Abnahme im Labortermin (Zeitslot über den ILIAS-Buchungspool); ohne Upload erfolgt keine Abnahme. Den Abgabetermin finden Sie im Ablaufplan.
