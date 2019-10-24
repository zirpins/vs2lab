# **Labor 2** - Kommunikation per Remote Procedure Call (RPC)

Das zweite Labor beschäftigt sich hauptsächlich mit **RPC-Kommunikation** in
verschiedenen Varianten. Ein erstes Beispiel zeigt eine einfache
RPC-Implementierung im Detail und nutzt dabei einen generischen
**Kommunikationskanal (Channel)** den wir später noch öfter verwenden werden.
Ein zweites Beispiel zeigt kurz die Anwendung des speziellen RPC-Frameworks
**RPyC**. Die Programmieraufgabe beschäftigt sich mit der Erweiterung der
einfachen RPC-Implementierung um **asynchrone RPCs**.

Allgemeine **Ziele** dieses Labors:

- *Verständnis* von **RPCs** und deren *Anwendung*
- Fähigkeit zur *Implementierung* von **RPC-Middleware**
- Kennenlernen des **`lab_channel` Mechanismus**
- Verständnis von **Client Threads**
- Verwendung des Python **`threading` Moduls**

## 1. Vorbereitung

### 1.1. Software installieren

Sie haben in der
[Vorbereitung von Aufgabe1](https://iz-gitlab-01.hs-karlsruhe.de/IWI-I/vs2lab/tree/master/lab1#1-vorbereitung)
bereits eine Umgebung mit Git, Python 3, Pipenv, IDE/Editor und Jupyter
eingerichtet.

Nun kommt noch eine Komponente hinzu. Installieren Sie bitte zusätzlich

- **Redis** (ein verbreiteter NOSQL Key-Value-Datastore)

Orientieren Sie sich zur Einrichtung der Umgebung an der [Beschreibung im VS2lab
README](https://iz-gitlab-01.hs-karlsruhe.de/IWI-I/vs2lab/tree/master#222-redis-erst-ab-aufgabe-2).

### 1.2. Projekt clonen und/oder aktualisieren

Erstellen Sie eine Kopie des VS2Lab Repositories auf Ihrem Arbeitsrechner aus
dem lokalen Netz der Hochschule oder über VPN (alle Beispiele für Linux/Mac)

```bash
mkdir -p ~/git # Verzeichnis für Git Projekte (optional)
cd ~/git
git clone https://iz-gitlab-01.hs-karlsruhe.de/IWI-I/vs2lab.git
```

Falls schon vorhanden aktualisieren Sie das Repository wie folgt:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
git pull
```

Bei Problemen siehe [Troubleshooting im VS2lab
README](https://iz-gitlab-01.hs-karlsruhe.de/IWI-I/vs2lab/tree/master#252-tipps-und-troubleshooting).

### 1.3. Python-Umgebung installieren

Falls nicht schon geschehen, wechseln Sie in das Verzeichnis des Repositories
und installieren Sie die vorgegebenen Packages in eine virtuelle Umgebung für
Python.

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
pipenv install
```

### 1.4. Beispielcode für diese Aufgabe

Wechseln Sie auf Ihrem Arbeitsrechner in das Unterverzeichnis dieser Aufgabe:

```bash
cd ~/git/vs2lab # angenommen hier liegt das vs2lab Repo
cd lab2
```

## 2. Beispiele für RPC-Kommunikation

Das Labor beginnt mit zwei Beispielen zur RPC-Kommunikation.

### 2.1. Anwendung von RPCs auf *Sprachebene* mit dem **rpyc**-Framework

Zunächst wollen wir ein 'echtes' RPC-Framework benutzen. Das Beispiel dient zur
Veranschaulichung von RPCs auf der Sprachebene, die die Kommunikation in
verteilten Systemen fast komplett verstecken und sehr einfach benutzbar machen.

Sie können das Beispiel ausprobieren und bei Interesse damit experimentieren.
Für die spätere Programmieraufgabe wird es nicht gebraucht.

Das Beispiel finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/rpyc
$ ls -l
-rw-r--r--  1 zirpins  staff  635 Oct 26 13:26 client.py
-rw-r--r--  1 zirpins  staff   34 Oct 25 20:21 constRPYC.py
-rw-r--r--  1 zirpins  staff  385 Oct 30 09:38 context.py
-rw-r--r--  1 zirpins  staff  583 Oct 26 13:26 server.py
```

Die Datei `server.py` enthält den Server-Prozess, der die Funktionen seiner
`DBList` Klasse als *Service* entfernt nutzbar macht. Der Client-Prozess in
`client.py` ruft diese Operationen des Services über eine Server-Verbindung
direkt auf.

Für Client und Server besteht kein wesentlicher Unterschied zur Programmierung
mit normalen Objekten. Die Verteilung wird durch das Framework transparent
gemacht.

Wie alle Dateien mit Prefix `const` enthält `constRPYC.py` Konstanten, die in
mehreren anderen Skripten verwendet werden (vornehmlich Adressen und
Kodierungen). Das Skript `context.py` dient hier (und in fast jedem Beispiel)
zur Einbindung des `lib` Package auf der obersten Ebene des Repositories.

Zum Ausprobieren starten Sie erst den Server und dann den Client.

```bash
cd ~/git/vs2lab/lab2/rpyc
pipenv run python server.py
```

In anderem Terminal:

```bash
cd ~/git/vs2lab/lab2/rpyc
pipenv run python client.py
```

Detaillierte Informationen zu RPyC finden Sie hier:

- [RPyC - Transparent, Symmetric Distributed
  Computing](https://rpyc.readthedocs.io/en/latest/)
- Für unser Beispiel: [Part 3: Services and New Style
  RPyC](https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html)

### 2.2. Implementierung einer einfachen *RPC-Middleware*

Wir betrachten nun die Realisierung eines RPC-Systems auf der Middleware-Ebene.
Das Beispiel finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/rpc
$ ls -l
-rwxr-xr-x  1 zirpins  staff     22 Oct 30 20:16 constRPC.py
-rw-r--r--  1 zirpins  staff    385 Oct 30 09:38 context.py
-rwxr-xr-x  1 zirpins  staff   1840 Oct 30 20:22 rpc.py
-rw-r--r--  1 zirpins  staff    225 Oct 30 20:22 runcl.py
-rw-r--r--  1 zirpins  staff    269 Oct 30 20:16 runsrv.py
```

Die RPC-Implementierung befindet sich in ``rpc.py`` mit Klassen für Client- und
Server-Stubs. Die Stubs erstellen Nachrichten für Request sowie Reply und
übertragen diese Nachrichten über einen Kommunikationskanal.

#### 2.2.1. Kommunikation per `lab_channel`

Der Kommunikationskanal wird im Modul `vs2lab/lib/lab_channel.py` implementiert.
`lab_channel` stellt einen Dienst für *persistente asynchrone Kommunikation*
bereit. Dazu benutzt das Modul eine *Redis Datenbank*, auf der Warteschlangen
für Nachrichten gespeichert werden. Das Modul wird detailliert in der
Dokumentation [The Channel Package](../docs/channel.pdf) beschrieben.

Ein Beispiel zur allgemeinen Verwendung finden Sie hier:

```bash
$ cd ~/git/vs2lab/lab2/channel
$ ls -l
-rw-r--r--  1 zirpins  staff  1336 Oct 30 18:21 channel.py
-rw-r--r--  1 zirpins  staff   385 Oct 30 18:21 context.py
-rw-r--r--  1 zirpins  staff   108 Oct 26 14:07 runcl.py
-rw-r--r--  1 zirpins  staff   287 Oct 30 18:21 runsrv.py
```

Zum Ausprobieren starten Sie erst Redis, dann den Server und schließlich den
Client.

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

Nun können wir noch das eigentliche RPC-Beispiel ausprobieren. Falls Sie den
Redis-Server im Channel-Beispiel gestartet haben, können Sie diesen weiter
verwenden, sonst starten Sie den Server jetzt (siehe oben).

Client- und Server-Prozesse werden durch `runcl.py` und `runsrv.py` realisiert.
Die Prozesse verwenden die in `rpc.py` bereitgestellten Stubs. Sie werden wie
üblich in getrennten Terminals gestartet:

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

## 3 Aufgabe

In der Programmieraufgabe sollen Sie nun das System aus Beispiel 2.2. zu einem
**asynchronen RPC** weiterentwickeln.

### 3.1 Übersicht

Der RPC aus Beispiel 2.2. ist synchron, d.h. der Client-Prozess wartet nach dem
Operationsaufruf, bis das Ergebnis vom Server-Prozess zurückgesendet wurde. Wenn
die Ausführung der Operation aufwendig ist, muss der Client-Prozess dabei ggf.
lange warten. In manchen fällen kann es sich lohnen, diese Wartezeit für andere
Aktivitäten zu nutzen.

Bei einem asynchronen RPC erfolgt die Synchronisierung von Client und Server
sofort nach Annahme eines Requests durch den Server, indem dieser eine
Bestätigung (**ACK**nowledgement) zurücksendet. Der Client kann nun mit anderen
Aktivitäten fortfahren. Wenn der Server das Ergebnis fertiggestellt hat, sendet
er es zum Client zurück. Im Client-Prozess kann dann z.B. eine Callback Funktion
aufgerufen werden, die das Ergebnis verarbeitet.

Erweitern Sie nun die Client- und Server-Klassen so, dass diese den oben
beschriebenen Ablauf implementieren. Nutzen Sie dabei den `lab_channel`, um die
zusätzliche Kommunikation des Acknowledgements zu realisieren.

Um nicht beim Warten auf die Server-Antworten den Client-Prozess zu blockieren,
gibt es verschiedene Möglichkeiten. Wir haben in der Vorlesung **Threads**
behandelt, um solche Blockaden zu vermeiden. Dies sollen Sie hier anwenden und
einen Python Thread verwenden, der die Kommunikation abwickelt.

#### 3.1.1. Das Python `threading` Modul

Threads werden in Python durch das `threading` Modul realisiert. Das Skript
`vs2lyb/lab2/threading/async_zip.py` zeigt ein kleines Beispiel zur Verwendung
von Threads und wird wie folgt gestartet:

```bash
cd ~/git/vs2lab/lab2/threading
pipenv run python async_zip.py
```

Python Threads erlauben zwar keine echte Parallelität der Ausführung, sind aber
gerade bei blockierenden I/O-Aufrufen sehr nützlich, da Sie die abwechselnde
Ausführung von I/O- und weiteren Anweisungen ohne Wartezeit erlauben.

Die ``threading``-API ist hier dokumentiert:

- threading ([thread-based
  parallelism](https://docs.python.org/3/library/threading.html))

### 3.2 Aufgabe und Anforderungen kurz und knapp

- Erweitern Sie Client- und Server-Klassen des RPC-Beispiels in `rpc/rpc.py` so, 
  dass sie den Ablauf eines asynchronen RPC realisieren.
- Passen Sie auch die dazugehörigen Client- und Server-Skripte des RPC-Beispiels 
  `rpc/runcl.py` und `rpc/runsrv.py` entsprechend an.
- Die schon vorhandenen Append-Funktion kann beibehalten werden, nur eben
  asynchron.
- Pausieren Sie den Server nach der Bestätigung des Requests für 10 Sekunden, um
  eine lange Ausführungszeit zu simulieren.
- Verwenden Sie im Client einen Thread zum Warten und Reagieren auf
  Server-Antworten.
- Machen Sie im Client einige Ausgaben auf der Konsole, um zu zeigen, dass er
  während des Wartens aktiv ist.
- Am Ende soll der Client das Ergebnis des RPC auf der Konsole ausgeben.

### 3.3 Tipps

... stay tuned (Hinweise zur Installation/Konfiguration im Labor-README)

### 3.4 Abgabe

Die Abgabe erfolgt durch Abnahme durch einen Dozenten. Packen Sie den kompletten
Code zudem als Zip Archiv und laden Sie dieses im ILIAS hoch.
