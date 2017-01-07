# Idee
* ich -> Programmieren
* ich -> politisch
  * eig TR website
* ich -> Zeitung -> klo -> spiegel -> wortwolke
* wie funktionieren Zeitungen?
* anschpruchsvoll
* -> was denken medien
* anwendungsmöglichkeinten

In meiner Freizeit programmiere ich gerne. Ich mag es, Probleme mit Computern oder anderen technischen Geräten zu lösen. Auch gewinne ich hierbei oft neue Erkenntnisse, da man sich beim Programmieren unkonventionell mit den Dingen beschäftigen muss: Man muss mehr in Strukturen denken, muss versuchen einem Computer, der kein Verständnis von Sinn oder Inhalt hat, das Problem nur in logischen Zusammenhängen zu beschreiben. Somit kann mithilfe eines Computerprogramms fast nie eine wirkliche Lösung für ein Problem oder eine Antwort auf eine Frage gefunden werden, allerdings können Computer einem Menschen helfen, eine bestimmte Aufgabe besser, schneller oder einfacher zu erledigen.

Besonders interessant finde ich es immer dann, diese Macht, die wir uns mit der Programmierung von Computern geben können, zu verwenden, wenn wir sie nutzen um neue Einblicke in unsere Umwelt zu erlangen. Auch hier gilt zwar wieder, dass der Computer eigentlich viel dümmer als wir ist, und keine Zusammenhänge begreifen kann, allerdings stumpfe Aufgaben viel schneller und ausdauernder zu erledigen vermag. Diese Kombination aus Eigenschaften ermöglicht es, große Datensätze mit mathematischen Methoden zu analysieren und die Ergebnisse für Menschen ansprechend aufzubereiten. Bei dieser Aufbereitung bietet sich eine optische Darstellung an, da die Augen des Menschen das Sinnesorgan sind, das am schnellsten Daten erfassen kann [spiegelminig]. Es bietet sich also an, empirische Daten grafisch aufzubereiten, sprich Datenvisualisierung zu betreiben.

Relativ schnell war mir also klar, das ich mich mit Datenvisualisierung beschäftigen will. Anfangs war allerdings nicht ganz klar, welchen Datensatz ich auf welche Aspekte hin untersuchen will. Eines Tages nahm ich dann eine Ausgabe des Spiegels zur Hand und sah auf der ersten Seite eine sogenannte Wortwolke. Diese Form der Darstellung fand ich sofort sehr ansprechend.

\iffalse

Am Anfang dieser Halbjahresarbeit stand die Idee, die aktuelle Nachrichtenlage visuell sichtbar zu machen. Dies sollte möglichst intuitiv und aufschlussreich sein. Außerdem

Hierbei können verschiedenen Analysen vorgenommen werden. All diese sind nicht trivial, da immer versucht erden muss aus einem Feließtext, also einem Format, mit dem Computer eigentlich nichts anfangen können Informationen zu gewinnen und zu veranschaulichen. Hierbei ist eine besondere Herausforderung, dass dies alles passieren muss, obwohl der Computer eigentlich über kein versändniss von "Sinn" verfügt. Aus diesem Grund müssen statistische Verfahren als Hilfsmittel zur Hand gezogen werden, die es dem Menschen, der die Daten letztenendes interpretiert ermöglichen Informationen aus der Datenmenge zu ziehen.
\fi

# Die Auswahl der Zeitungen
\iffalse
1. Spiegel.de
2. Bild.de
3. Focus.de
4. Welt.de
5. Zeit.de
6. Faz.net



AGOF November 2014: Die Top 50 der Nachrichten-Websites
Unique User	November vs. Oktober
1	Bild.de	16,91	-0,17	-1,0%
2	Focus Online	13,65	0,31	2,3%
3	Spiegel Online	11,43	0,19	1,7%
4	Die Welt	9,56	0,31	3,4%
5	Süddeutsche.de	7,41	-0,56	-7,0%
6	stern.de	6,45	0,43	7,1%
7	Zeit Online	5,78	0,10	1,8%
8	n-tv.de	4,69	0,17	3,8%
9	FAZ.net	4,54	-0,54	-10,6%
10	N24.de	4,07	1,19	41,3%
11	RP Online	3,22	-0,04	-1,2%
12	tagesspiegel.de	2,68	0,08	3,1%
13	Handelsblatt Online	2,59	-0,13	-4,8%
14	Huffington Post	2,53	-0,26	-9,3%
15	Der Westen	2,49	-0,02	-0,8%
16	manager-magazin.de	2,35	0,43	22,4%
17	Frankfurter Rundschau online	2,10	-0,13	-5,8%
18	Abendblatt.de	2,05	-0,23	-10,1%
19	taz.de	1,65	0,28	20,4%
20	WirtschaftsWoche Online	1,51	-0,23	-13,2%
21	Augsburger Allgemeine Online	1,47	-0,11	-7,0%
22	Express Online	1,43	-0,08	-5,3%
23	Berliner Morgenpost	1,41	0,08	6,0%
24	Merkur-Online	1,34	-0,16	-10,7%
25	Badische Zeitung Online	1,30	0,00	0,0%

http://meedia.de/2015/01/29/agof-news-top-50-n24-zahlen-explodieren-auch-manager-magazin-und-taz-mit-riesen-plus/
\fi

## Ein Wort über Bild.de

# Konzeptioneller Aufbau

![Der Aufbau des Gesamtsystems](img/aufbau.png){#fig:aufbau}

Nun gilt es sich ein System auszudenken, welches die Daten der Ausgewählten Zeitungen periodisch herunterlädt und die gesammelten Ergebnisse für spätere Analyse abspeichert. Dieser schritt ist ein sehr wichtiger, der gut bedacht sein muss, da
\todo{more}

Dieses System sieht am Ende aus wie in Abb. @fig:aufbau.
