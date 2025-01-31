# Chips & Circuits

Groepsproject voor de minor Programmeren met het vak Algoritme & Heuristieken, waarbij wij de beste manier onderzochten om in een chip alle gates uit de netlist op een efficiënte manier met elkaar te verbinden in een grid van maximaal 8 verdiepingen hoog, zonder draden te laten overlappen. Dit moet worden gedaan zonder dat er kruisingen van draden optreden. Indien er een kruising optreedt, worden er extra kosten toegevoegd. De draden kunnen bewegen naar noord, zuid, oost, west, maar ook omhoog of omlaag tussen verschillende lagen van de chip.

# Team TJK - Programmeurs

* Tygo Berghuis

* Keenan Kesser

* Joey Oehlers

### Nodig voor code

De betreffende code is geschreven in Python 3. In requirements.txt staat alles wat noodzakelijk is om de code optimaal te runnen. Installatie is mogelijk met pip op de volgende manier: 

"""

pip install -r requirements.txt

"""

Mocht onverhoopt de code niet draaien met deze installaties of kun je de installaties niet installeren, probeer dan eerst een aparte omgeving te maken voor deze instellingen.

### Structuur

In de mainfolder bevinden zich verschillende subfolders en bestanden:

* main.py - Hiermee voer je het programma uit.

* requirements.txt - hierin staan alle benodigdheden om de code succesvol te draaien

* Code - Hierin staan de verschillende codeonderdelen van het programma, 

  zoals de algoritmes en heuristieken, de visualisatie en de classes.

* Data - Hierin bevinden zich alle datafiles, zoals de netlist en de gates en de resultatenmap waarin gegenereerde informatie zit bij het runnen van de verschillende algoritmes - Bijna alle csv-bestanden zijn verwijderd vanwege het geheugen. Ook worden hier de csv-bestanden opgeslagen die het programma produceert in output.csv en data.csv.

* Scripts - alle scripts die gebruikt worden om het programma te laten draaien

* Presentaties - alle netlists zoals gegeven in de opdracht

### Programma draaien

Voer de volgende command in de terminal in om het programma te laten draaien

(Zorg dat je in de juiste map zit in de terminal)

"""

python3 main.py

"""

In de terminal zal gevraagd worden naar het aantal iteraties

voer in hoeveel iteraties je wil doen.

Het beste resultaat van de run wordt opgeslagen en weergegeven.

Alle iteraties worden bewaard in data.csv totdat je de code opnieuw runt.

Alle output die het programma produceert, komt in de onderstaande map:

"""

/data

"""

# Uitleg algoritmes

## A*-pathfinding

Het algoritme vindt een valide oplossing door over de netlist heen te loopen en voor iedere combinatie aan gates een pad te vinden. Dat pad vindt het door te starten bij de coördinaten van de eerste gate. Hij berekent dan voor de buurcoördinaten, met een Manhattan Distance-heuristiek, de kosten om naar de coördinaten van de tweede gate te gaan. Hij randomizeert ook de lijst van neighbors waar hij over loopt om wat variatie in het pad te creëren. Hij doet de kosten en coördinaten van alle buren in een prioriteitslijst en gaat dan de goedkoopste optie als eerste af, terwijl hij bijhoudt waar hij vandaan komt. Dit wordt herhaald totdat hij bij het eindpunt is gekomen. Dan reconstrueert hij het pad terug naar het begin en maakt hij een wire aan en past dat aan in het grid. Dit wordt herhaald voor elke combinatie in de netlist.

## Hill Climber

Het Hill Climber-algoritme is een algoritme dat draden tussen gates weghaalt en opnieuw probeert te leggen in een andere volgorde. Dit kan bepaalde draden uit de knop halen en helpt bij het vinden van een valide oplossing. Nadat het alle draden heeft verbonden, als dat niet direct gebeurt, gaat het door met het herleggen van draden en zoekt het een zo'n best mogelijke oplossing. Dit doet het door de oplossing van de best gevonden score te gebruiken om draden weg te halen, tot het een betere vindt. Op dit moment werkt alleen de hill_climber_nc, omdat hij moeite had met de parallelle draden weghalen en controleren. Hij werkt nu door in de main een aantal draden op te geven die het weghaalt elke loop en een aantal minuten dat hij moet loopen. Hij blijft zolang loopen en geeft het beste resultaat, de beste score of de meeste verbonden draden. Let op de seed; hij doet nu niks 100% random, maar volgens de seed. 

## mh_nc

Dit is het standaard A*-algoritme om paden te vinden, maar dit kan geen kruisingen aanmaken.

## netlist_reorder

Dit pakt informatie van de netlist en reordert deze, gebaseerd op hoe belangrijk de connectie is. Hoe belangrijk de connectie is, wordt gebaseerd op de afstand tot het midden, de afstand tot de andere gate en hoeveel draden verbonden zijn aan deze gate. Deze laatste waarde telt 5X meer dan de andere twee. Dat komt omdat dat meer valide oplossingen genereerde.

# Dank

* Alle TA's van de minor programmeren 

* Martijn, Jelle, Wouter 

* Onze begeleiders - Jacob en Jona

