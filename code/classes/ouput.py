import csv
from classes import grid_edit

class write_to_csv:
      
    def write_to_csv(wirepaths_list):
                # Open het CSV-bestand in 'append' mode
                with open('wirepaths.csv', 'a', newline='') as csvfile:
                    kolom = ['nummer', 'pad', 'succes', 'score', 'aantal_wires', 'aantal_kruizingen']
                    writer = csv.DictWriter(csvfile, fieldnames=kolom)

                    # Als het bestand leeg is, schrijf dan eerst de header (kolomnamen)
                    csvfile.seek(0, 2)  # Ga naar het einde van het bestand
                    if csvfile.tell() == 0:  # Als het bestand leeg is
                        writer.writeheader()

                    # Genereer nummer voor de nieuwe rij
                    with open('wirepaths.csv', 'r', newline='') as check_csvfile:
                        reader = csv.reader(check_csvfile)
                        rows = list(reader)
                        nummer = len(rows)  # Nummer is gelijk aan het aantal rijen, zodat het begint bij 1

                        # Dit zijn de andere gegevens die je wilt toevoegen. Pas deze aan op basis van je eigen logica.
                        data = {
                            'nummer': nummer,
                            'pad': str(wirepaths_list),  # Zet de wirepath om in een string
                            'succes': 'ja',  # Voorbeeld, pas aan volgens je logica succes als er geen overlapping is dus twee twee 
                            'score': 100,  # Voorbeeld
                            'aantal_wires': grid_edit.wirecount,  # Aantal items in de wirepath
                            'aantal_kruizingen': grid_edit.wirecrosscount  # Voorbeeld, pas aan volgens je logica
                        }

                        # Schrijf de rij naar het bestand
                        writer.writerow(data)
                        nummer += 1  # Verhoog het nummer voor de volgende rij

                print("CSV-bestand succesvol geschreven.")