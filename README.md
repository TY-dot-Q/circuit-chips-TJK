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
  van de verschillende algoritmes - Bijna alle csv bestanden zijn verwijderd vanwege het geheugen.
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


## hill climber
De hill climber algortime is een algortime dat draden tussen gates weghaalt en opnieuw probeert te leggen in een andere volgorde
Dit kan bepaalde draden uit de knop halen en helpt met het vinden van een valide oplossing.
nadat het alle draden heeft verbonden als dat niet direct gebeurt, gaat het door met het herleggen van draden en zoekt het een zo'n best mogelijke oplossing.
Dit doet het door de beste gevonden score oplossing te gebruiken om draden weg te halen tot het een betere vindt.

Op dit moment werkt alleen de hill_climber_nc omdat hij moeite had met de parallel draden weghalen en controleren

Hij werkt nu door in de main een x aantal draden op te geven die het weghaalt elke loop en een aantal minuten dat hij moet loopen
hij blijft zolang loopen en geeft het beste resultaat, of score of meeste verbonden draden. 

let op de seed hij doet nu niks 100% random maar volgens de seed. 

## mh_nc
dit is de standaard A* algortime om paden te vinden maar deze kan geen kruisingen aanmakken.

## netlist_reorder
dit pakt informatie van de netlist en her orderd deze gebaseerd op hoe belangrijk de connectie is. 
hoe belangrijk de connectie is wordt gebasseerd op de afstand tot het midden, afstand tot de andere gate en hoeveel draden verbonden zijn aan deze gate deze waarde telt 5X meer
dan de andere twee omdat het helpt met valide oplossingen te genereren



# Dank
* Alle TA's van de minor programmeren 
* Martijn, Jelle, Wouter 
* Onze begeleiders - Jacob & Jona


