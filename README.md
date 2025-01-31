# Chips & Circuits
Groepsproject voor de minor Programmeren met het vak Algoritme & Heuristieken waarbij wij de beste manier onderzochten om in een chip alle gates uit de netlist op een efficiente manier met elkaar te verbinden in een grid van maximaal 8 verdiepingen hoog zonder draden te laten overlappen. Dit moet worden gedaan zonder dat er kruisingen van draden optreden. Indien er een kruising optreedt, wordt er extra kosten toegevoegd. De draden kunnen bewegen naar noord, zuid, oost west, maar ook omhoog of omlaag tussen verschillende lagen van de chip.

# Team TJK - Programmeurs
* Tygo Berghuis
* Keenan Kesser
* Joey Oehlers

### Nodig voor code
De betreffende code is geschreven in Python 3. In requirements.txt staat alles wat noodzakelijk is om de code optimaal te runnen. Installatie is mogelijk met pip op de volgende manier: 
"""
pip install -r requirements.txt
"""

Mocht onverhoopt de code niet draaien met deze installaties of kun je de installaties niet installeren probeer dan eerst een aparte omgeving te maken voor deze instellingen.

### Structuur
In de mainfolder bevinden zich verschillende subfolders en bestanden:

* main.py - Hiermee voer je het programma uit.
* requirements.txt - hierin staan alle benodigdheden om de code succesvol te draaien
* Code - Hierin staan de verschillende code onderdelen van hert programma, 
  zoals de algoritmes en heurstieken, de visualisatie en de classes.
* Data - Hierin bevinden zich alle datafiles zoals de netlist en de gates 
  en de resultatenmap waarin gegenereerde informatie zit bij het runnen 
  van de verschillende algoritmes - De csv bestanden zijn verwijderd vanwege het geheugen.
  Ook worden hier de csv bestanden opgeslagen die het programma produceert 
  in output.csv en data.csv.
* Scripts - alle scripts die gebruikt worden om het programma te laten draaien
* Presentaties - alle netlists zoals gegeven in de opdracht

### Programma draaien

Voer de volgende command in de terminal om het programma te laten draaien
(Zorg dat je in de juiste map zit in de terminal)

"""
python3 main.py
"""

In de terminal zal gevraagd worden naar het aantal iteraties
`voer in hoeveel iteraties je wil doen.
Het beste resultaat van de run wordt opgeslagen en weergegeven.
alle iteraties worden bewaard in data.csv totdat je de code opnieuw runt.

alle output die het programma produceert komt in de onderstaande map:
"""
/data
"""

# Uitleg algoritmes





# Dank
* Alle TA's van de minor programmeren 
* Martijn, Jelle, Wouter 
* Onze begeleiders - Jacob & Jona


