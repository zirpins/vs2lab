# **Labor 5** -  Mutex-Koordination mit logischen Lamport Uhren

Im fünften Labor steht die Koordination von Prozessen im Mittelpunkt. Konkret
wird ein Algorithmus für den wechselseitigen Ausschluss (engl. *Mutual
Exclusion*, kurz **Mutex**) bei kritischen Sektionen behandelt.

Die gezeigte Variante setzt (einfache) *logische Uhren* ein, um eine eindeutige
Reihenfolge von Anfragen und Genehmigungen für den Eintritt in eine *kritische
Sektion* zu schaffen. Der Algorithmus wurde zuerst von *Leslie Lamport* entwickelt
und stellt eine Erweiterung seines *total geordneten Multicast* dar.

Wir werden den Algorithmus zunächst untersuchen und dann eine Erweiterung dazu
erstellen. Dabei sind die Ziele wie folgt:

- Eigenschaften und Anwendungen logischer und physikalischer Uhren erkennen
- Wechselseitigen Ausschluss anhand eines voll verteilten Ansatzes verstehen
- Mit Absturz-Ausfällen in partiell synchronen Systemen umgehen

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
cd lab5/mutex
```

## 2. Beispiel Implementierung des Lamport Mutex Algorithmus

Als Startpunkt des Labors dient die Implementierung von konkurrierenden Peer
Prozessen eines Systems mit wechselseitigem Ausschluss im Verzeichnis
`vs2lab/lab5/mutex`. Hier sind zwei Skripte interessant:

- `process.py` ist die eigentliche Implementierung der Peers
- `doit.py` organisiert mehrere Peers als Mutex Anwendung

Die Struktur der Implementierung ähnelt Aufgabe 4.

### Mutex Peers `process.py`

Die Klasse `Process` verwendet wieder das `lab_channel` Framework. Hier wird
*Redis* als Message-Oriented-Middleware verwendet. Alle Knoten melden sich an
der Gruppe `proc` an, die vom zentralen Channel abgefragt werden kann.

Prozesse führen die Hauptschleife aus, in der sie periodisch in eine gemeinsame
kritische Sektion eintreten und sich dabei untereinander abstimmen. Sie verfügen
dazu jeweils über eine logische Uhr, die bei eigenen Aktivitäten oder beim
Empfang von Nachrichten angepasst wird. Prozesse verfügen zudem über eine
Warteschlange (Queue) zur Anordnung von Nachrichten zum Ein- und Austritt aus
der kritischen Sektion, die nach ihren logische Zeitstempeln geordnet sind.

Die genaue Funktion entnehmen Sie bitte der kommentierten Implementierung.

### Mutex Anwendung `doit.py`

Das zweite Skript nutzt die Implementierung von Peer Prozessen zum Aufbau eines
Mutex Systems mit simuliertem Knotenausfall. Hierbei kann die Anzahl der Knoten
(`n`) als Konstante angegeben werden.

Das Skript verwendet wieder das [Python `multiprocessing`
Modul](https://docs.python.org/3.7/library/multiprocessing.html), um Knoten als
separate Prozesse mittels  `Spawn` zu starten, was auch unter Windows
funktioniert.

### 2.1. Starten des Systems

`doit.py` baut im aktuellen Zustand ein P2P-System aus koordinierten
Prozessen auf. Nach einer kurzen Pause simuliert das Skript den Absturz eines
Prozesses durch dessen Terminierung. Das voll verteilte Mutex System kann dann
nicht mehr zu einer Einigung kommen und bleibt stehen. Durch Deaktivierung
(Auskommentieren) der Terminierung können Sie das Mutex System kontinuierlich
bei der Abstimmung beobachten.

Einen Test führt man wie folgt aus (Beispiel für Linux/Mac OS; nicht
vergessen, vorher Redis zu starten):

```bash
cd ~/git/vs2lab/lab5/mutex # angenommen hier liegt das vs2lab Repo
pipenv run python doit.py
```

## 3 Aufgabe

Sie sollen nun den Mutex Algorithmus erweitern.

## 3.1 Übersicht

Aktuell kann der Algorithmus nicht mit Absturzausfällen umgehen. Das System
bleibt beim Ausfall eines Knotens nach kurzer Zeit stehen.

Die Aufgabe besteht in der Erweiterung des Mutex Algorithmus zur Maskierung von
Absturzausfällen. Das System soll trotz des simulierten Ausfalls eines Prozesses
kontinuierlich weiterarbeiten.

## 3.2 Aufgabe und Anforderungen kurz und knapp

- Erweitern Sie das Skript `process.py` so, dass es Absturz-Ausfälle anderer
  Teilnehmer bemerkt (woran kann man dies erkennen?)
- Ändern Sie den Koordinationsmechanismus dann so ab, dass ausgefallene Prozesse
  ignoriert werden.
- Durch die zufallsbedingte Ausführung des Systems können sich vielfälltige
  Situationen ergeben. Führen Sie das Skript mehrfach aus, um die
  Stabilität zu testen.
- Verwenden Sie Log-Ausgaben, die die Funktionsweise Ihres Systems zeigen.

### 3.3 Tipps

... stay tuned (Hinweise zur Installation/Konfiguration im Labor-README)

### 3.4 Abgabe

Die Abgabe erfolgt durch Abnahme durch einen Dozenten. Packen Sie den
kompletten Code zudem als Zip Archiv und laden Sie dieses im ILIAS hoch.
