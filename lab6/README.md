# **Labor 6** - Fehlertoleranz bei atomaren Commitment Protokollen

Im sechsten (und letzten) Labor betrachten wir die Thematik der
**Fehlertoleranz** in verteilten Systemen am Beispiel **atomarer Commitment
Protokolle**.

Ziel solcher Commit Potokolle ist die Durchführung einer gemeinsamen
*Transaktion*, die sich aus verschiedenen *Teiltransaktionen* mehrere Teilnehmer
zusammensetzt. Es soll sichergestellt werden, dass am Ende entweder alle oder
keine der Teiltransaktionen wirksam werden (d.h., die übergeordnete Transaktion
wird dadurch unteilbar bzw. *atomar*). Die Herausforderung liegt darin, diese
Eigenschaft auch dann zu garantieren, wenn einzelne Teilnehmer wärend der
Protokollausführung ausfallen.

Typischerweise basieren verteilte Commit Protokolle auf einer *zentralisierten
Organisation* mit einem *Koordinator* und mehreren *Teilnehmern* (es gibt aber
auch andere Varianten). Die beteiligten Prozesse einigen sich dann im Zuge
mehrerer *Phasen* (bestehend jeweils aus einer Anfrage des Koordinators und den
Antworten der Teilnehmer) auf den Ausgang der Transaktion.

Die verbreitetste Variante der Commit Protokolle ist das **2-Phasen Commit
Protokoll** (2PC). Es kommt mit zwei Phasen aus, um bei allen möglichen
Ausfällen einen inkonsistenten Ausgang der Transaktion zu verhindern. Allerdings
ist es (in seltenen Fällen) möglich, dass das Protokoll dauerhaft blockiert.
Diesen Nachteil hat das **3-Phasen Commit Protokoll** (3PC) nicht, das jedoch
durch eine dritte Phase etwas aufwändiger ist.

Wir wollen in diesem Labor die Funktionsweise des 2PC-Protokolls anhand eines
gegebenen Prototyps nachvollziehen und dessen Abläufe inklusive möglicher
Blockaden untersuchen. Im Anschluss sollen Sie den Prototypen erweitern und das
3PC-Protokoll implementieren.

## 1. Vorbereitung

### 1.1. Software installieren

Für diese Aufgabe werden keine neuen Installationen benötigt, wir brauchen aber
wieder eine laufende Redis Instanz. Der Redis Server wird wie folgt gestartet:

```bash
redis-server
```

### 1.2. Projekt clonen und/oder aktualisieren

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
cd lab6/2pc
```

## 2. Beispielhafte 2PC Implementierung

Als Startpunkt des Labors dient die Implementierung des 2-Phasen Commit
Protokolls im Verzeichnis `vs2lab/lab6/2pc`. Hier sind drei Skripte interessant:

- `2pc.py` organisiert Teilnehmer und Koordinator als verteilte Anwendung.
- `coordinator.py` ist die Implementierung eines **2PC-Koordinators**.
- `participant.py` ist die Implementierung eines **2PC-Teilnehmers**.

Die Struktur der Implementierung ähnelt den Aufgaben 4 und 5.

Das Skript `stablelog.py` repräsentiert einen **persisten Log**, der zur
Wiederherstellung nach Abstürzen genutzt werden könnte (was wir hier aber nicht
näher betrachten). Log Ausgaben werden in den Ordner `stablelogs` geschrieben.

### 2.1 Koordinator `coordinator.py`

Die Klasse `Coordinator` verwendet das bekannte `lab_channel` Framework. Hier wird
*Redis* als Message-Oriented-Middleware verwendet. Der Knoten meldet sich an der
Gruppe `coordinator` an und kann dort vom zentralen Channel abgefragt werden.

Der Koordinator steuert die Phasen des 2PC-Protokolls in schrittweiser Abfolge
eines Zustandsautomaten innerhalb seiner zentralen `run` Methode.

Vor und nach dem `VOTE_REQUEST` werden zufällige Abstürze simuliert. Ein Recovery
Protokoll zur Wiederherstellung des Koordinators wird aber nicht unterstützt.

Die genaue Funktion entnehmen Sie bitte der kommentierten Implementierung.

### 2.2 Teilnehmer `participant.py`

Die Klasse `Participant` verwendet natürlich auch das `lab_channel` Framework.
Die Knoten melden sich an der Gruppe `participant` an.

Der Teilnehmer durchläuft die Phasen des 2PC-Protokolls in schrittweiser Abfolge
eines Zustandsautomaten innerhalb seiner zentralen  `run` Methode. Für die
Durchführung der lokalen Transaktion wird ein zufälliger Misserfolg simuliert.
Ein Ausfall von Teilnehmern wird nicht berücksichtigt.

Bei Ausfall des Koordinators wird eine verteilte Terminierung durchgeführt, bei
der sich die Teilnehmer abstimmen. Hier ist jedoch im ungünstigsten Fall eine
Blockade möglich. Dieser Algorithmus unterstützt partiell synchrones Verhalten,
denn verspätete Koordinator Nachrichten würden akzeptiert werden.

Die genaue Funktion entnehmen Sie bitte der kommentierten Implementierung.

### 2PC Anwendung `2pc.py`

Das dritte Skript nutzt die Implementierungen von Koordinator und Teilnehmern
zum Aufbau eines verteilten Commitment Systems mit simuliertem Knotenausfall des
Koordinators. Hierbei kann die Anzahl der Knoten (`n`) als Konstante angegeben
werden.

Das Skript verwendet das [Python `multiprocessing`
Modul](https://docs.python.org/3.7/library/multiprocessing.html), um Knoten als
separate Prozesse mittels  `Spawn` zu starten, was auch unter Windows
funktioniert.

### 2.1. Starten des Systems

`2pc.py` baut ein verteiltes System mit einem Koordinator und `n` Teilnehmern auf.
Zufallsbedingt simuliert das Koordinator-Skript den Absturz durch vorzeitige
Beendigung der zentralen Funktion. Teilnehmer-Skripte simulieren zufallsbedingte
Misserfolge der lokalen Transaktionen. Die resultierenden Situationen können
meist bis zu einer globalen Einigung geführt werden. Manchmal ergibt sich aber
auch eine Blockade. Starten Sie das System mehrfach, um verschiedene Fälle zu
beobachten.

Einen Test führt man wie folgt aus (Beispiel für Linux/Mac OS; nicht vergessen,
vorher Redis zu starten):

```bash
cd ~/git/vs2lab/lab6/2pc # angenommen hier liegt das vs2lab Repo
pipenv run python 2pc.py
```

## 3 Aufgabe

Sie sollen nun selbst ein atomares Commitment Protokoll implementieren (wobei
Sie sich an dem gegebenen Prototypen orientieren können).

### 3.1 Übersicht

Wie Sie gesehen haben, kann es beim 2PC-Protokoll zu Blockaden kommen, wenn alle
noch laufenden Teilnehmer für Commit votieren aber der Koordinator ausgefallen
ist. Die verbleibenden Teilnehmer können dann nicht eigenständig entscheiden,
denn ein ggf. ebenfalls ausgefallener Teilnehmer könnte nach seiner
Wiederherstellung schon entweder einen Commit oder einen Abort durchgeführt
haben. Die verschiedenen gleichzeitigen Möglichkeiten finaler Zustandsübergänge
machen den Ausgang der Transaktion ungewiss.

Genau diese Situation behebt das **3-Phasen Commit Protokoll** durch Einführung
eines *zusätzlichen Zustands* `PRECOMMIT`. Dieser repräsentiert eine
*vorläufige* Einigung, die nur noch zum Commit führen kann, die aber noch nicht
vollzogen ist. Dadurch haben Teilnehmer in jeder Situation eine eindeutige
Möglichkeit zum Abschluss der Transaktion.

Sie sollen eine vereinfachte Implementierung des 3PC-Protokolls erstellen und
damit die zuvor beim 2PC gesehene Blockade beheben.

### 3.2 Three Phase Commit (3PC)

**3PC** ist ein **nicht blockierendes atomares Commitment Protokoll**. Eine
kompakte Zusammenfassung folgt unten. Diese soll in der Aufgabe implementiert
werden. Details finden Sie in der Literatur [1, Seite 443 ff].

#### 3.2.1 Protokollablauf

Das Protokoll besteht aus folgenden Schritten:

- **Phase 1a:** Koordinator `C` startet in Zustand `INIT`, sendet dann `VOTE_REQUEST` an Teilnehmer `P_i, i ∈ [1;n]` und betritt Zustand `WAIT`.
- **Phase 1b:** `P_i` startet in Zustand `INIT`, wartet auf `VOTE_REQUEST` von `C` und führt dann seine lokale Transaktion durch.
  - Bei Erfolg der lokalen Transaktion betritt `P_i` Zustand `READY` und sendet `VOTE_COMMIT` an `C`.
  - Bei Misserfolg der lokalen Transaktion betritt `P_i` Zustand `ABORT`, sendet `VOTE_ABORT` an `C` und terminiert.
- **Phase 2a:** `C` empfängt im Zustand `WAIT` Antworten aller `P_i`.
  - Sind alle Antworten `VOTE_COMMIT`, dann betritt `C` Zustand `PRECOMMIT` und sendet `PREPARE_COMMIT` an alle `P_i`.
  - Ist eine Antwort `VOTE_ABORT`, dann betritt `C` Zustand `ABORT`, sendet `GLOBAL_ABORT` an alle `P_i` und terminiert.
- **Phase 2b:** `P_i` empfängt im Zustand `READY` Nachricht von `C`.
  - Ist die Nachricht `PREPARE_COMMIT`, dann betritt `P_i` Zustand `PRECOMMIT` und sendet `READY_COMMIT` an `C`.
  - Ist die Nachricht `GLOBAL_ABORT`, dann betritt `P_i` Zustand `ABORT` und terminiert.
- **Phase 3a:** `C` empfängt im Zustand `PRECOMMIT` Antworten aller `P_i`.
  - Sind alle Antworten `READY_COMMIT`, dann betritt `C` Zustand `COMMIT` und sendet `GLOBAL_COMMIT` an alle `P_i`.
- **Phase 3b:** `P_i` empfängt im Zustand `PRECOMMIT` Nachricht von `C`.
  - Ist die Nachricht `GLOBAL_COMMIT`, dann betritt `P_i` Zustand `COMMIT` und terminiert.

#### 3.2.2 Verhalten bei Ausfällen

Falls ein Prozess (Koordinator oder Teilnehmer) ausfällt, können die
verbleibenden Prozesse die Transaktion stets zum Abschluss führen. Dieser
Vorgang wird durch **Terminierungsprotokolle** definiert. Die
**Wiederherstellung** ausgefallener Prozesse ist ein weiterer Aspekt, den wir
hier nicht näher betrachten wollen.

##### 3.2.2.a Terminierungsprotokolle bei Ausfall von Teilnehmern

Nach dem Zeitpunkt des Ausfalls eines Teilnehmers unterscheidet man zwei Fälle.

1. Koordinator `C` ist in Zustand `WAIT` und ein Teilnehmer `P_i` fällt aus.
   - `C` betritt Zustand `ABORT` und sendet `GLOBAL_ABORT` an alle Teilnehmer.
2. Koordinator `C` ist in Zustand `PRECOMMIT` und ein Teilnehmer `P_i` fällt aus.
   - `C` betritt Zustand `COMMIT` und sendet `GLOBAL_COMMIT` an alle Teilnehmer.

##### 3.2.2.b Terminierungsprotokolle bei Ausfall des Koordinators

Nach dem Zeitpunkt des Koordinatorausfalls unterscheidet man drei Fälle.

1. Teilnehmer `P_i` ist in Zustand `INIT` und Koordinator `C` fällt aus.
   - `P_i` wechselt in Zustand `ABORT` und terminiert.
2. `P_i` ist in Zustand `READY` und `C` fällt aus.
   - Alle Teilnehmer sind im Zustand `INIT`, `READY`, `ABORT` oder `PRECOMMIT`.
   - Ein Teilnehmer `P_k` wird als neuer Koordinator bestimmt und terminiert die globale Transaktion.
3. `P_i` ist in Zustand `PRECOMMIT` und `C` fällt aus.
   - Alle Teilnehmer sind im Zustand `READY`, `PRECOMMIT` oder `COMMIT`.
   - Ein Teilnehmer `P_k` wird als neuer Koordinator bestimmt und terminiert die globale Transaktion.

Die Terminierung der globalen Transaktion erfolgt durch einen neuen Koordinator.
Ein Teilnehmer `P_k` übernimmt diese Rolle, der in Zustand `WAIT`, `PRECOMMIT`,
`COMMIT` oder `ABORT` sein kann (je nach seinem vorherigen Zustand als
Teilnehmer).

`P_k` sendet seinen Zustand an alle `P_i`. `P_i` in späterem Zustand ignorieren
dies, ansonsten schließen sie zum Zustand von `P_k` auf (d.h. sie wechseln in
den jeweils korrespondierenden Zustand eines Teilnehmers) und senden
entsprechende Nachrichten an `P_k`. Dann verfährt `P_k` wie folgt:

- **Fall 1:** `P_k` ist in Zustand `WAIT`.
  - Alle Teilnehmer sind im Zustand `INIT`, `READY`, `ABORT` oder `PRECOMMIT`.
  - `P_k` betritt Zustand `ABORT` und sendet `GLOBAL_ABORT` an alle `P_i`.
  - `P_i` in Zustand `PRECOMMIT` dürfen (nur) bei Terminierung in Zustand `ABORT` wechseln.
- **Fall 2:** `P_k` ist in Zustand `PRECOMMIT`.
  - Alle Teilnehmer sind im Zustand `READY`, `PRECOMMIT` oder `COMMIT`.
  - `P_k` betritt Zustand `COMMIT` und sendet `GLOBAL_COMMIT` an alle `P_i`.
- **Fall 3:** `P_k` ist in Zustand `COMMIT` oder `ABORT`.
  - Nach dem initialen Aufschließen sind alle Teilnehmer im gleichen finalen Zustand.

### 3.2 Aufgabe und Anforderungen kurz und knapp

- **Mindestanforderung**
  - Implementieren Sie den *grundlegenden Ablauf* (Zustandsautomaten) des zentralisierten 3PC-Protokolls.
- **Lösungsversuch**
  - Berücksichtigen Sie die *Terminierung* des Protokolls nach dem Ausfall von Prozessen.
  - Verwenden Sie für die Terminierung nach Koordinatorausfall den gezeigten Ansatz mit neuem Koordinator.
  - Zeigen Sie die Funktion der Terminierung anhand von simulierten Abstürzen.
- **Abgrenzung**
  - *Nachrichtenverlust* sowie *multiple Abstürze* können ignoriert werden.
  - *Wiederherstellung* ausgefallener Prozesse kann ignoriert werden.

### 3.3 Tipps

- Verwenden Sie die Implementierung des 2PC-Protokolls als Ausgangsbasis.
- Für die Bestimmung eines neuen Koordinators können Sie eine deterministische
  Zuweisung verwenden (z.B. der Teilnehmer mit der kleinsten Id). Ein
  verteilter Wahlalgorithmus ist nicht nötig.

... stay tuned (Hinweise zur Installation/Konfiguration im Labor-README)

### 3.4 Abgabe

Die Abgabe erfolgt durch Abnahme durch einen Dozenten. Packen Sie den kompletten
Code zudem als Zip Archiv und laden Sie dieses im ILIAS hoch.

## 4 Literatur

[1] M.T. Özsu and P. Valduriez, Principles of Distributed Database Systems:
Third Edition, 723 DOI 10.1007/978-1-4419-8834-8_18, Springer Science+Business
Media, LLC 2011, aus dem HsKA Netz zum freien Download:
[link.springer.com/book/10.1007/978-1-4419-8834-8](https://link.springer.com/book/10.1007/978-1-4419-8834-8)
