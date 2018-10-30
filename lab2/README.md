# Labor 2 Kommunikation per Remote Procedure Call (RPC)

## 1. Vorbereitung
### 1.1. Software installieren

Sie haben in [Aufgabe 1](https://IWI-I-gitlab-1.HS-Karlsruhe.DE:2443/zich0001/vs2lab/tree/master/Aufgabe1#21-software-installieren) 
bereits eine Umgebung mit Git, Python 3, Pipenv, IDE/Editor und Jupyter eingerichtet.

Nun kommt noch eine Komponente hinzu. Installieren Sie bitte zusätzlich die 

- **Redis** (ein verbreiteter NOSQL Key-Value-Datastore)

Orientieren Sie sich zur Einrichtung der Umgebung an der Beschreibung im 
[VS2lab README](https://IWI-I-gitlab-1.HS-Karlsruhe.DE:2443/zich0001/vs2lab#222-redis-erst-ab-aufgabe-2).

### 1.2. Projekt clonen und/oder aktualisieren

Erstellen Sie eine Kopie des VS2Lab Repositories auf Ihrem Arbeitsrechner 
(aus dem lokalen Netz der Hochschule oder über VPN):

```
$ git clone https://IWI-I-gitlab-1.HS-Karlsruhe.DE:2443/zich0001/vs2lab.git
```

Falls schon vorhanden aktualisieren Sie das Repository wie folgt:

```
$ cd vs2lab # angenommen hier liegt das vs2lab Repo
$ git pull
```

Bei Problemen siehe Troubleshooting im 
[VS2lab README](https://localhost:2443/zich0001/vs2lab/tree/master#252-troubleshooting)

### 1.3. Python Umgebung installieren

Wechseln Sie in das Verzeichnis des Repositories und installieren Sie die 
vorgegebenen Packages in eine virtuelle Umgebung für Python.

```
$ cd vs2lab # angenommen hier liegt das vs2lab Repo
$ pipenv install
```

### 1.4. Beispielcode für diese Aufgabe

Wechseln Sie auf Ihrem Arbeitsrechner in das Unterverzeichnis dieser Aufgabe:

```
$ cd vs2lab # angenommen hier liegt das vs2lab Repo
$ cd Aufgabe2
```

## Beispiele für RPC Kommunikation

### 1. Einfache "Datenbank" mit *RPC* zum Anhängen von Daten
### 2. Erweiterte Variante der "Datenbank" mit *Marshalling*
### 3. RPC auf *Sprachebene* mit **rpyc**
### 4. Implementierung *portabler Referenzen* mit Sockets


## 2 Einführung


## 3 Aufgabe
### 3.1 Übersicht
### 3.2 Weitere Anforderungen
### 3.3 Tipps
### 3.4 Abgabe
