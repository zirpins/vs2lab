# **Labor 4** - Namensauflösung im Chord P2P-System

Das Thema im 4. Labor ist die Auflösung linearer Namen. Wir betrachten dazu die
Systemklasse *verteilter Hash-Tabellen* (Distributed Hash Table - DHT) und
konkret eine vereinfachte Implementierung des **Chord Systems**.

Die Ziele im einzelnen:

- praktische Vorstellung eines Chord P2P-Systems bekommen
- ein Beispiel für Prozess-Migration ausprobieren
- Funktionsweise von Namenssystem und Namensauflösung in Chord verstehen
- Konzepte rekursiver und iterativer Namensauflösung erarbeiten

## 1. Vorbereitung

### 1.1. Software installieren

Für diese Aufgabe werden keine neuen Installationen benötigt, wir brauchen aber
wieder eine laufende Redis Instanz. Der Redis Server wird wie folgt gestartet:

```bash
redis-server
```

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
cd lab4/chord
```

## 2. Beispiel: Implementierung von Chord Ring Knoten

Als Startpunkt des Labors dient eine Implementierung von Chord Knoten im
Verzeichnis `vs2lab/lab4/chord`. Hier sind zwei Skripte interessant:

- `chordnode.py` ist die eigentliche Implementierung der Knoten.
- `doit.py` organisiert mehrere Knoten als P2P Anwendung

### Chord Knoten `chordnode.py`

Die Klasse ChordNode verwendet das `lab_channel` Framework, [das wir schon aus
Aufgabe zwei
kennen](https://iwi-i-gitlab-1.hs-karlsruhe.de:2443/zich0001/vs2lab/tree/master/lab2#221-kommunikation-per-lab_channel).
Hier wird *Redis* (eigentlich ein (NOSQL) Key-Value-Store) als
Message-Oriented-Middleware verwendet.

#### Knoten Management

Alle Knoten melden sich an der Gruppe `node` an, die vom zentralen
Channel abgefragt werden kann. Dies ist eine Vereinfachung gegenüber echten
Peer-to-Peer Systemen, in denen man keine zentrale Registry aller Knoten hat.
Die Verwaltung von kommenden und gehenden Knoten ist jedoch ein Aspekt, der in
diesem Labor nicht im Mittelpunkt steht. Daher wird der zentrale Channel beim
Knoten Management zu Hilfe genommen.

#### Namenssystem

(Lineare) Namen werden vom zentralen Channel bei der Anmeldung zufällig aus
einem konfigurierbaren Wertebereich vergeben. Jeder Knoten unterstützt die
Auflösung von Schlüsseln `key` zum Namen des zuständigen Knotens `succ(key)` mit
der Operation `LOOKUP`. Hierbei wird der bestmögliche nächste Knoten auf dem Weg
zum Ziel aus einer internen *Finger Tabelle* abgeleitet.

Bei einer Namensauflösung müssen mehrere Knoten in einer Sequenz von `LOOKUP`
Aufrufen bis zum letztendlichen Ziel traversiert werden. Dies kann entweder
iterativ durch einen Client Prozess 'von außen' oder rekursiv durch eine
Erweiterung der Knotenlogik realisiert werden. Momentan ist die Steuerung der
Namensauflösung noch nicht implementiert, denn dies wird Inhalt der
Programmieraufgabe sein.

#### Datenverwaltung

in einem DHT speichern die beteiligten Knoten Datenwerte für die verwendeten
Schlüssel. Die dazu notwendige Datenverwaltung ist in diesem Beispiel nicht
realisiert.

### Chord Anwendung `doit.py`

Das zweite Skript nutzt die Implementierung von Chord Knoten zum Aufbau eines
Ring Systems. Hierzu können die Größe des Adressraums in Bit (`m`) und die
Anzahl der Knoten (`n`) als Konstanten oder Parameter angegeben werden.

Das Skript zeigt auch ein interessantes Beispiel für Prozess Migration. Hier
wird das [Python `multiprocessing`
Modul](https://docs.python.org/3.7/library/multiprocessing.html) verwendet, um
Knoten (und einen Client) als separate Prozesse zu starten. Prozesse können per
`Fork` oder `Spawn` erzeugt werden. In letzteren Fall kann dem neuen Prozess ein
Parameter zur Initialisierung übermittelt werden. Dieses Feature erlaubt die
Migration von Prozessen mit Weiterführung des Ausführungszustands auch ohne Fork
unter Windows.

Der verwendete `DummyChordClient` ist nur eine Schablone ohne Logik für den
Aufruf einer Namensauflösung auf einem der Knoten. Dieser Client soll in der
Programmieraufgabe fertiggestellt werden.

### Starten des Systems

Das System baut im aktuellen Zustand lediglich einen Ring auf und beendet diesen
dann sofort wieder. Die Durchführung von Namensauflösungen wird erst in der
Programmieraufgabe realisiert. Am Ende werden die Finger Tabellen aller Knoten
ausgegeben. Einen Test führt man wie folgt aus (Beispiel für Linux/Mac OS; nicht
vergessen, vorher Redis zu starten):

```bash
cd ~/git/vs2lab/lab4/chord # angenommen hier liegt das vs2lab Repo
pipenv run python doit.py
```

## 3 Aufgabe

In der Programmieraufgabe soll die Namensauflösung mit dem Chord System
fertiggestellt werden.

## 3.1 Übersicht

Die Namensauflösung mit Chord erfolgt schrittweise über eine Reihe von Aufrufen
der LOOKUP Funktion einzelner Knoten, die jeweils den besten bekannten Knoten
auf dem Weg zum Ziel liefern, bis dieses Ziel am Ende erreicht ist.

Die Steuerung der einzelnen Schritte kann entweder durch einen zentralen Client
Prozess von außen (iterativ) koordiniert werden oder sich durch die verteilen
Knoten Prozesse selbst rekursiv fortsetzen. **Die Aufgabe besteht darin, die
rekursive Variante zu implementieren.**

## 3.2 Aufgabe und Anforderungen kurz und knapp

- Erweitern Sie die `LOOKUP` Operation von ChordNode so, dass diese für eine
  Anfrage nach Schlüssel `key` direkt `succ(key)` zurückgibt. Falls der
  angefragte Knoten nicht selbst der gesuchte Knoten ist, soll er zu dessen
  Bestimmung eine rekursive `LOOKUP` Anfrage an den besten bekannten Knoten
  machen usw.
- Erweitern Sie ebenfalls die Klasse `DummyChordClient`. Hier soll eine `LOOKUP`
  Anfrage nach einem zufälligen validen Schlüssel an einen ebenfalls zufälligen
  existierenden Knoten erfolgen und der gefundene Name ausgegeben werden.

### 3.3 Tipps

- Bei einer einfachen Rekursion werden alle beteiligten Knoten (bis auf den
  letzten) zu Clients, die jeweils auf eine Antwort warten und diese dann
  weiterreichen, bis am Ende der ursprünglichen Client die Antwort bekommt.
  Alternativ kann die Implementierung endrekursiv erfolgen, dann sendet der
  letzte Knoten die Antwort direkt zum ursprünglichen Client zurück.  

... stay tuned (Hinweise zur Installation/Konfiguration im Labor-README)

### 3.4 Abgabe

Die Abgabe erfolgt durch Abnahme durch einen Dozenten. Packen Sie den kompletten
Code zudem als Zip Archiv und laden Sie dieses im ILIAS hoch.
