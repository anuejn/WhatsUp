# Idee

In meiner Freizeit programmiere ich gerne. Ich mag es, Probleme mit Computern oder anderen technischen Geräten zu lösen. Auch gewinne ich hierbei oft neue Erkenntnisse, da man sich beim Programmieren unkonventionell mit den Dingen beschäftigen muss: Man muss mehr in Strukturen denken, muss versuchen einem Computer, der kein Verständnis von Sinn oder Inhalt hat, das Problem nur in logischen Zusammenhängen zu beschreiben. Somit kann mithilfe eines Computerprogramms fast nie eine wirkliche Lösung für ein Problem oder eine Antwort auf eine Frage gefunden werden, allerdings können Computer einem Menschen helfen, eine bestimmte Aufgabe besser, schneller oder einfacher zu erledigen.

Besonders interessant finde ich es immer dann, diese Macht, die wir uns mit der Programmierung von Computern geben können, zu verwenden, wenn wir sie nutzen um neue Einblicke in unsere Umwelt zu erlangen. Auch hier gilt zwar wieder, dass der Computer eigentlich viel dümmer als wir ist, und keine Zusammenhänge begreifen kann, allerdings stumpfe Aufgaben viel schneller und ausdauernder zu erledigen vermag. Diese Kombination aus Eigenschaften ermöglicht es, große Datensätze mit mathematischen Methoden zu analysieren und die Ergebnisse für Menschen ansprechend aufzubereiten. Bei dieser Aufbereitung bietet sich eine optische Darstellung an, da die Augen des Menschen das Sinnesorgan sind, das am schnellsten Daten erfassen kann [spiegelminig]. Es bietet sich also an, empirische Daten grafisch aufzubereiten, sprich Datenvisualisierung zu betreiben.

Relativ schnell war mir also klar, das ich mich mit Datenvisualisierung beschäftigen will. Anfangs war allerdings nicht ganz klar, welchen Datensatz ich auf welche Aspekte hin untersuchen werde. Eines Tages nahm ich dann eine Ausgabe des Spiegels zur Hand und sah auf der ersten Seite eine sogenannte Wortwolke, in der oft verwendete Worte größer gedruckt waren, als weniger oft verwandte. Diese Form der Darstellung fand ich sofort sehr ansprechend. Ich entschied mich also dazu, verschiedene Texte über das aktuelle Weltgeschehen, die ich von verschiedenen Online-Zeitungen herunterladen kann, zu analysieren. Diese Analyse wollte ich von Anfang an nicht unbedingt nur auf die Generierung von Wortwolken beschränken, sondern mit dem Datensatz "herumexperimentieren", also gucken, welche interessanten Visualisierungen möglich sind.

Also fing ich an und suchte Zeitungen aus.

# Die Auswahl der Zeitungen
Als das Thema der Halbjahresarbeit feststand musste ich Zeitungen aussuchen, die ich analysieren will. Hierbei orientierte ich mich an einer Studie der Arbeitsgemeinschaft Online Forschung aus dem November 2014. Hierbei ging ich nach der Anzahl der "Unique Users", also quasi der Leser der jeweiligen Nachrichtenseite. Nach dieser Studie @topten sind die 10 Nachrichtenseiten mit den meisten Lesern:

| Rang | Nachrichtenseite | Leser (in Milionen) |
|------|------------------|---------------------|
| 1    | Bild.de          | 16,91               |
| 2    | Focus Online     | 13,65               |
| 3    | Spiegel Online   | 11,43               |
| 4    | Die Welt         | 9,56                |
| 5    | Süddeutsche.de   | 7,41                |
| 6    | stern.de         | 6,45                |
| 7    | Zeit Online      | 5,78                |
| 8    | n-tv.de          | 4,69                |
| 9    | FAZ.net          | 4,54                |
| 10   | N24.de           | 4,07                |

Von diesen Online-Zeitungen habe ich nun Bild.de Focus Online, Spiegel Online ausgewählt. Dies sind die 3 Zeitungen mit den meisten Lesern. Zusätzlich habe ich Süddeutsche.de und Zeit Online ausgewählt, da ich diese Zeitung manchmal selber lese. An dieser Auswahl ist unter anderem sehr interessant, dass sie Nachrichtenquellen verschiedener politischer Ausrichtungen und intellektuellen Anspruchsniveaus enthält. Dies ermöglicht es, am Ende auch Vergleiche zwischen den Zeitungen durchzuführen und eigene Hypothesen leicht zu verifizieren.

# Konzeptioneller Aufbau

Als nächstes galt es, ein System zu konzipieren, welches die Daten der ausgewählten Zeitungen periodisch herunterlädt, vorverarbeitet und die gesammelten Ergebnisse für spätere Analyse abspeichert. Dieser Schritt ist ein sehr wichtiger, der gut bedacht sein muss, da die am Ende durchführbaren Analysen davon abhängen, welche Daten in diesem Schritt erhoben werden. Ich habe mich dazu entschlossen, die Daten, die ich erhebe, in einer Datenbank zu speichern. Auf diese sollten nun kleine Auswertungsprogramme, die verschiedene Visualisierungen generieren, zugreifen. Diese sollten im Webbrowser laufen, da dieser die Programmierung der Visualisierungen vereinfacht und die Visualisierungen sehr portabel macht. Der gesamte Auswertungsprozess sollte jeweils durch diese Visualisierung vorgenommen werden, um einfacheres Experimentieren mit dem Datensatz zu ermöglichen. Um dies möglich zu machen, ist zusätzlich noch ein "Adapter" zwischen Visualisierung und Datenbank notwendig.

Dieses System sieht am Ende aus wie in Abb. @fig:aufbau gezeigt.

![Der Aufbau des Gesamtsystems](img/aufbau.png){#fig:aufbau}

Wie ich dieses System nun umgesetzt habe, ist im nächsten Absatz beschrieben.
