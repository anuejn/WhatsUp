# Idee
## Nuzen
## Mögliche weitere Verwendung

# Konzept
## Verschiedene Anzätze
## Dikussion

# Technische Umsezung
* Docker!!!1!
  * build + tests
* Klare Unterteilung:
  * Datensammler
    * In Python geschrieben
    * Crawlen hauptsächlich rss-feeds
  * MongoDB
    * noSQL-Datenbank
    * Map/Reduce-Querys
    * zuerst Mongo, dann Couch, dann Mongo
  * Http Middleware
    * stellt MongoDB über HTTP bereit
    * Clinets können eigene Map/Reduce Anfragen an die Datenbank stellen
      * - langsam
      * + flexibel
      * -> kleine datenmengen, daher ok
  * Frontend
    * 3d.js visualisierung
    * einfache API zur DB
    * einfache umstrukturierbarkeit
## Vorgehen
## Probleme
## Leztendliche Umsetzung

# Beobachtungen
## Evaluation des Verfahrens
## Verschiedene Zeitungen im Vergleich

#Fazit
