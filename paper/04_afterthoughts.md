# Bedienungsanleitung
Um die Software selbst zu benutzen, gibt es zwei Möglichkeiten:

1. Die erste und einfachere Möglichkeit ist es, die Version, die auf meinem Server läuft, zu verwenden. Aus dieser stammen auch meine Grafiken. Sie kann allerdings teilweise sehr langsam sein (mehrere 10 Minuten Wartezeit), da der verwandte Server sehr leistungsschwach ist. Hierfür muss einfach in einem aktuellen Webbrowser (ich empfehle Firefox) die Adresse `wasistlos.tk` aufgerufen werden.
Nun sollte eine Übersicht erscheinen, die alle möglichen Visualisierungen und eine Einstellungsseite mit jeweils einem Icon aufrufbar macht. Behält man die Maus unbewegt mehrere Sekunden über einem Icon, erscheint ein kleiner Erklärungstext zu jeder Visualisierung.
2. Die zweite Möglichleit ist, alle Komponenten auf einem lokalen Computer laufen lassen. Hierfür wird ein Computer mit unixoidem Betriebssystem (z.B. Linux oder macOS), den Softwarepaketen Docker und GNU-Make und einem Internetanschluss benötigt. Um die Software zu starten, muss zunächst der Inhalt des USB-Sticks, welcher sich im Anhang befindet, auf den betreffenden Computer kopiert werden und ein Terminal in dem Ordner, in dem sich nun der Inhalt des Sticks befindet, geöffnet werden. In diesem muss nun der Befehl `make` ausgeführt werden. Danach muss noch `make restore` ausgeführt werden, um den bereits von mir gesammelten, beigefügten Datensatz in die lokale Datenbank zu kopieren. Nun kann wie in Möglichkeit 1 fortgefahren werden, nur dass als Adresse statt `wasistlos.tk` `localhost` verwendet werden muss. \todo{fix domain}

# Fazit
Insgesamt fand ich meine Halbjahresarbeit sehr interessant. Anfangs ging es mir nur darum, Wortwolken, wie sie im Spiegel zu finden waren, für verschiedene andere Zeitungen zu erstellen. Dies weitete sich dann aber relativ schnell aus und ich begann, mit anderen Möglichkeiten der Auswertung und Visualisierung zu experimentieren. Einen großen Teil der Arbeit, die ich in die Halbjahresarbeit steckte, steckte ich in die Entwicklung dieses Systems, das die verschiedenen Visualisierungen ermöglicht. Für mich war es persönlich eine gute Herausforderung, die Möglichkeit zur Analyse zu entwickeln. Diese ermöglicht es dann jedem selbst, die eigentliche Analyse nach eigenen Parametern durchzuführen und dementsprechend seine eigenen Schlüsse ziehen. Beispielhaft habe ich auch einige Analysen durcheführt und sie interpretiert, um einen Denkanstoß zu geben und die sehr vielfältigen Möglichkeiten zu demonstrieren.

Mit der Auswertungssoftware bin ich alles in allem sehr zufrieden. Besonders die sehr flexible und modulare Architektur ermöglicht auch Wiederverwendbarkeit der Codes in weiteren Datenanalyseprojekten. Das softwaretechnisch größte Problem, die Geschwindigkeit, ließe sich wahrscheinlich relativ einfach durch ein Austauschen der Datenbank, durch etwas Passenderes, das Zwischenergebnisse speichert, lösen. Insgesamt sind im Rahmen des Projekts ungefähr 1000 Zeilen Code entstanden und ich habe auch auf der technischen Seite vieles Neues gelernt. So habe ich zum Beispiel zum ersten Mal Docker verwendet und NoSQL-Datenbanken verstanden.

Mit meinem eigentlichen Ergebnis, der Analysesoftware, kann nun der interessierte Leser seine eigenen Schlüsse ziehen und die aktuelle Nachrichtenlage aus einer statistischen Metaperspektive betrachten, womit ich mein Ziel erreicht habe.

\pagebreak

# Quellen

\todo{dates}
