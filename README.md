# DLRG-Prüfungsfragenkataloge Schwimmen & Rettungsschwimmen

Dieses Projekt besteht aus zwei Teilen. Einem [Crawler](#fragen-crawler), der alle Prüfungsfragen der DLRG im Bereich Schwimmen und Rettungsschwimmen herunterlädt und einem [Webserver](#ansichts-server), der die heruntergeladenen visuell aufbereitet.

## Installation

Das Repository kann mit über die GitHub-Oberfläche oder den Befehle `git clone (https://github.com/shoneg/DLRG-Pruefungsfragenkataloge-Schwimmen-Rettungsschwimmen.git)` heruntergeladen werden.

Zur Ausführung der Skripte muss python3 installiert sein. Außerdem sind die Module `argparser`, `requests`, `regex` und `Flask` erforderlich. Diese Module können wie folgt installiert werden:

```bash
pip install argparse
pip install requests
pip install regex
pip install Flask
```

Bevor der [Ansichts-Server](#ansichts-server) erstmals gestartet wird, muss einmalig der [Fragen-Crawler](#fragen-crawler) für den Fragen-Download genutzt werden.

## Fragen-Crawler

Der Fragen-Crawler lädt Prüfungsfragen der DLRG im Bereich Schwimmen und Rettungsschwimmen herunter. Eine DLRG eigene Nutzeroberfläche als Prüfungsquiz ist unter [https://www.dlrg.de/informieren/ausbildung/pruefungsfragenquiz/](https://www.dlrg.de/informieren/ausbildung/pruefungsfragenquiz/) verfügbar.

Der Crawler kann mittels `python3 fragen_download.py` gestartet werden. Wird er so ausgeführt, lädt er die Fragen zu allen Katalogen herunter. Mit der Option `-h` werden die folgenden möglichen Optionen kurz beschrieben:

```txt
usage: fragen_download.py [-h] [-w WIEDERHOLUNGEN] [-p PFAD] [-k KATALOG [KATALOG ...]]

DLRG Fragen abrufen und speichern

options:
  -h, --help            show this help message and exit
  -w WIEDERHOLUNGEN, --wiederholungen WIEDERHOLUNGEN
                        Anzahl der Wiederholungen (Standard: 100)
  -p PFAD, --pfad PFAD  Speicherpfad für Dateien (Standard: ./fragen)
  -k KATALOG [KATALOG ...], --kataloge KATALOG [KATALOG ...]
                        Fragenkataloge auswählen (Standard: Alle)

KATALOGE=
Juniorretter (J)
Deutsches_Rettungsschwimmabzeichen_Bronze (DRSAB)
Deutsches_Rettungsschwimmabzeichen_Silber (DRSAS)
Deutsches_Rettungsschwimmabzeichen_Gold (DRSAG)
Lehrscheininhaber (L)
Deutsches_Schnorcheltauchabzeichen (DSTA)
Ausbilder_Schwimmen (AS)
Ausbilder_Rettungsschwimmen (ARS)
Ausbildungsassistent_Schwimmen (AAS)
Ausbildungsassistent_Rettungsschwimmen (AARS)
```

Je nach genutzten Optionen und Internetanbindung, kann er Prozess zwischen wenigen Sekunden bis zu einigen Stunden in Anspruch nehmen. Bei den Standardoptionen und einer Download-Rate von 50 MBit/s ist eine Laufzeit von etwa 15 Minuten zu erwarten. Es gibt keine Fortschrittsanzeige, lediglich wird am Ende die Anzahl der heruntergeladenen Fragen angezeigt.

Es folgen weiterführende Erläuterungen zu einzelnen Optionen:

### Wiederholungen

Bei jeder Anfrage an den Server werden jeweils 20 zufällige Fragen mit zugehörigen Informationen zur Verfügung gestellt. Um sicherzustellen, dass alle Fragen abgerufen werden, müssen sehr viele Anfragen gestellt werden. Umso mehr Anfragen gestellt werden, desto länger ist die Laufzeit des Programms, aber desto höher ist die Wahrscheinlichkeit, dass alle Fragen gefunden werden. Eine 100 %ige Sicherheit, dass alle Fragen gefunden werden gibt es nicht. Stand Januar 2024 scheint es über alle [Fragenkataloge](#kataloge) hinweg insgesamt 630 Fragen zu geben.

### Kataloge

Kataloge entsprechen den Prüfungsfragenquizzen, die auf der DLRG-Website zur Auswahl stehen. Jedes Quiz bzw. jeder Katalog hat eigene Fragen, wobei viele Fragen auch in mehreren Katalogen gelistet sind. Für den Fall, dass nur die Fragen zu bestimmten Quizzen benötigt werden, können diese mit der Option `--kataloge` angegeben werden. Hinter der Option können die Kataloge in Lang- oder Kurzform als leerzeichenseparierte Liste angegeben werden. Um alle Fragen herunterzuladen, muss die Option beim start weggelassen werden.

## Ansichts-Server

![Bilder der Website. Überschrift ist "DLRG Fragen Filter". Es folgen zwei Filter als Drop-Down-Menüs: Für "Datei wählen" ist "Ausbilder-Rettungsschwimmen" ausgewählt, für "Kapitel wählen" "Die DLRG als Verein". Darunter folgen der Anzeige Optionen, mit Check-Boxen, die alle aktiviert sind: Frage anzeigen, Antwort Anzeigen, Kapitel anzeigen. Darunter ist ein blauer Button "Filter anwenden". Nun folgend drei Kästen mit je einer Frage, drei Antworten und einer Kapitalangabe. Die erste Frage lautet: "Welche der Aufgaben der DLRG stehen unter anderem in der Satzung?" Die Antworten dazu sind: "Ausbildung im Schwimmen und in der Selbstrettung, Aus- und Fortbildung in Erster Hilfe und im Sanitätswesen", "Landgebundener Rettungsdienst, Luftrettung, Tiefseetauchen" und "Rettung Schiffbrüchiger, Rettungssport, Katastrophenschutz"; als Kapitel ist "RS 1.2 - Die DLRG als Verein (FragenID: 69)" angegeben.](./beispielbild.png)

In der obenstehenden Abbildung ist ein Beispiel zu sehen wie, die mit dem [Crawler](#fragen-crawler) heruntergeladenen Fragen, gefiltert und angezeigt werden können.

Der Server kann mit dem Befehl `python3 fragen_ansichts_server/__main__.py` gestartet werden. Der Seite ist dann unter [http://localhost:5000](http://localhost:5000) verfügbar. Es wird empfohlen, die Website in einem chromiumbasierten Browser zu nutzen. So werden für eine ausgewählte Datei die Kapitel, in denen es Fragen gibt hervorgehoben.

Mit der Option `--port` kann der Port geändert werden. Mit der Option `--fragen` kann der Pfad zu dem Ordner mit den, mit dem [Crawler](#fragen-crawler) heruntergeladenen Fragen, angegeben werden. Die Optionen und weitere Erläuterungen, können mit der Option `-h` angezeigt werden.

## Transparenz- und Nutzungshinweise

- Teile des Quellcodes wurden mit ChatGPT generiert.

- Es gelten die Nutzungsbedingungen von [www.dlrg.de](https://www.dlrg.de).
