import csv, os

class user_input:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def score_request(self)->None:
        """print de score van de grid door de bijgehouden waardes van de grid_edit classe te bekijken"""
        print("-----score_request-----")
        print(f"er zijn {self.grid_edit.wirecount} draaden")
        print(f"er zijn {self.grid_edit.wirecrosscount} die overelkaar lopen")
        print(f"dit geeft een score van c={self.grid_edit.score}")
        print("")
    
    def load_gates(self, file_path: str)->None:
            """voegt gates toe in het grid, gebruikt de file path waar de grid locaties staan opgeslagen"""

            print("-----load_gates-----")
            if not os.path.isfile(file_path):
                print(f"Bestand '{file_path}' niet gevonden!")
            else:
                try:
                    with open(file_path, mode='r') as file:
                        csv_reader = csv.reader(file)
                        next(csv_reader)  # sla de eerste regel over

                        for row in csv_reader:
                            if len(row) < 2:
                                print(f"Ongeldige regel in CSV-bestand: {row}")
                                continue


                            try:
                                x=int(row[2])
                                y=int(row[1])
                                z=0
                                self.grid_edit.add_gate(y,x,z)
                            
                            except ValueError:
                                print(f'print:error met waardes in regel:{row}')
                                continue

                    print("Alle gates zijn succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("Fout: Ongeldige waarden in het CSV-bestand.")

            print("")
    
    def load_netlist(self, file_path: str)->None:
            """voegt alle verbindingen tussen de gates toe aan een lijst en geeft deze lijst terug. heeft een file_path nodig met de verbonden gates"""
            connection_list=[]
            print("-----load_netlist-----")


            if not os.path.isfile(file_path):
                print(f"Bestand '{file_path}' niet gevonden!")
            else:
                try:
                    with open(file_path, mode='r') as file:
                        csv_reader = csv.reader(file)
                        next(csv_reader)  # sla de eerste regel over

                        counter=0

                        for row in csv_reader:
                            if len(row) < 2:
                                print(f"(Netlist) Ongeldige regel in CSV-bestand: {row}")
                                continue

                            try:
                                chip_a=int(row[0])
                                chip_b=int(row[1])
                                connection_list.append((chip_a, chip_b))
                                print(f"connectie tussen {chip_a} en {chip_b} succevol ingeladen als {connection_list[counter]}")
                                counter+=1
                            except ValueError:
                                print(f'(Netlist) print:error met waardes in regel:{row}')
                                continue
                        
                        print("Netlist is succesvol geladen uit het CSV-bestand.")
                        print("")
                        return connection_list, counter

                    print("Netlist is succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("(Netlist) Fout: Ongeldige waarden in het CSV-bestand.")
            print("")

    def max_grid_values(self, file_path: str):
        """Bepaal de maximale y-, x-, en z-waarden uit een CSV-bestand.
        Het bestand moet een lijst van coördinaten bevatten.
        Retourneert een tuple (max_y, max_x, max_z)."""
        print("-----max_grid_values-----")
         
        max_y, max_x = 0, 0  # Initiële waarden voor maxima

        if not os.path.isfile(file_path):
            print(f"Bestand '{file_path}' niet gevonden!")
            return max_y, max_x  # Zorg voor een veilige return bij fout

        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Sla de kopregel over

                for row in csv_reader:
                    if len(row) < 2:  # Controleer of er minimaal y en x aanwezig zijn
                        print(f"Ongeldige regel in CSV-bestand: {row}")
                        continue

                    try:
                        y = int(row[1])
                        x = int(row[2])

                        max_y = max(max_y, y)
                        max_x = max(max_x, x)
                        
                    except ValueError:
                        print(f"Fout bij het verwerken van regel: {row}")
                        continue

            max_y = max_y + 1
            max_x = max_x + 1

            self.grid_edit.maximum_x = max_x
            self.grid_edit.maximum_y = max_y

            print(f"Maximale waarden gevonden: y={max_y}, x={max_x}")
            print("")
            return max_y, max_x

        except Exception as e:
            print(f"Fout tijdens het lezen van het bestand: {e}")
            return max_y, max_x  # Zorg voor een veilige return
