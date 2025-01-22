import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

gate_nrstart =1

class grid_edit:
    grid=[]
    gate_dict={}
    wire_list=[]
    gate_nr = gate_nrstart
    

    def __init__(self):
        """initaliseer de gridedit class"""
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0

    def grid_create (self, max_y, max_x) -> None:
        """
        creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        """
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(7)]
        print("grid succesfol gemaakt")

    def add_gate (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik x en y coordinaten
        """
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return
    
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = self.gate_nr #voeg de gate toe
            self.gate_dict[self.gate_nr] = (y,x,z)
            print(f"gate met het nummer {self.gate_nr} toegevoegd op de coordinaten y={y}, x={x}, z={z} ---- check: {self.gate_dict[self.gate_nr]} ")
            self.gate_nr +=1
            gate_nrstart
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")

    def gate_amount_count(self):
        grid_edit_obj=grid_edit()

        amount=0

        for item in grid_edit_obj.gate_dict:
            amount+=1
            item+=1

        #print(f"amount{amount}")

        return amount
    
    def add_wire (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        # early stop bij out of bounds 
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return

        if self.grid[z][y][x] ==0 or isinstance(self.grid[z][y][x], int): # als de coordinaten van de grid op een gate staan
            self.grid[z][y][x] = "+" #voeg de wire toe
            self.wirecount+=1
            self.wire_list.append((y,x,z))
            print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
            gate_nr = self.grid[z][y][x]
            if gate_nr not in self.gate_dict:
                self.gate_dict[gate_nr] = (y, x, z)  # Voeg toe aan gate dict
                print(f"Gate nummer {gate_nr} toegevoegd aan gate_dict op coördinaten y={y}, x={x}, z={z}")
            else:
                print(f"Gate nummer {gate_nr} staat al in gate_dict.")
        # als er al een draad is 
        elif self.grid[z][y][x]=="+":
            self.wirecrosscount+=1
            print(f"kruisende draad toegevoegd op de coordinaten y={y}, x={x} z={z} ")
        # als het misgaat
        else:
            print(f"er staat al iets namelijk: \"{self.grid[z][y][x]}\"")

    def connect_gates(self, gate1: int, gate2: int) -> None:
        """
        Verbind twee gates met een draad.
        Gate nummers worden opgegeven als gate1 en gate2. 
        Moet later overgenomen worden door netlist die aangeeft welke gates verbonden zijn
        """
        if gate1 not in self.gate_dict or gate2 not in self.gate_dict:
            print(f"Een of beide gate nummers {gate1} of {gate2} bestaan niet.")
            return

        start = self.gate_dict[gate1]
        end = self.gate_dict[gate2]

        y1, x1, z1 = start
        y2, x2, z2 = end
        
        # Voegt lijn van gate tot eerste punt van pad toe
        self.add_wire(y1, x1, z1)

        '''
        Basis Manhattan-distance "algoritme" voor testen wires leggen
        Algoritme kan met a* vanuit hier worden uitgebreid!
        '''
        current_y, current_x, current_z = y1, x1, z1

        # loop om middelste stuk draad van pad te maken
        while (current_y, current_x, current_z) != (y2, x2, z2):
            # Verplaats in y-as
            if current_y != y2:
                current_y += 1 if current_y < y2 else -1
            # Verplaats in x-as
            elif current_x != x2:
                current_x += 1 if current_x < x2 else -1
            # Verplaats in z-as
            elif current_z != z2:
                current_z += 1 if current_z < z2 else -1

            # Voeg de draad toe op de huidige locatie
            self.add_wire(current_y, current_x, current_z)

        # Voegt lijn van laatste punt van pad tot eindgate toe
        self.add_wire(y2, x2, z2)
        self.wirecount -= 1


    def gate_location(self, nr_check)->int:
        return self.gate_dict[nr_check]
    
    def dichtstbij(self, gate_check, list_iligal_gates):
        """checkt wat de dichstbijzijnde gate is, geeft de gate terug en de afstand"""
        #pak de hoeveelheid gates

        #print("---------------nieuwe dichtstbij check --------------")
        #print("")
        #print(f"gate_check{gate_check}")

        #pak de coordinaten van de gate die wordt gevraagd
        #print(f"gate_check == {gate_check}")
        if gate_check <=0:
            return -1, -1
        
        y,x,z = self.gate_dict[gate_check]
        #print(f"y={y} -- x={x} -- z={z}")
        gate_nr_teller = self.gate_amount_count()

        gate_return=0
        check_optimum=99999999
        #loop de andere gates
        if gate_nr_teller<1:
            #print("te weinig gates om dit uit te voeren")
            return -1, -1

        while gate_nr_teller > 1:
            #print(f"gate_nr_teller={gate_nr_teller}")
            #test of de y,x en z waardes afstand samen groter is dan de vorige (in begin 0)
            if gate_nr_teller!=gate_check & gate_nr_teller not in list_iligal_gates: 
                #print("gaat goed ")
                test_y, test_x, test_z = self.gate_dict[gate_nr_teller]
                #print(f"test_y={test_y} -- test_x={test_x} -- test_z={test_z}")
                v1 = abs(test_y - y)
                v2 = abs(test_x - x) 
                v3 = abs(test_z - z)
                nieuw_optimum=v3+v2+v1
                #print(f"nieuw_optimum={nieuw_optimum}")
                #print(f"check_optimum={check_optimum}")
                
                
                if check_optimum>nieuw_optimum:
                    check_optimum =nieuw_optimum
                    gate_return=gate_nr_teller
                    #print(f"gate_return={gate_return}")
                    #print(f"check_optimum={check_optimum}")
            gate_nr_teller -=1

            
        #print(f"gate_return{gate_return}")
        #print(f"check_optimum{check_optimum}")
        return gate_return, check_optimum
               
class user_input:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def score_request(self, score)-> None:
        print(f"er zijn {self.grid_edit.wirecount} draden")
        print(f"er zijn {self.grid_edit.wirecrosscount} die overelkaar lopen")
        print(f"dit geeft een score van c={score}")
    
    def load_gates(self, file_path: str)-> None:
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            if not os.path.isfile(file_path):
                print(f"Bestand '{file_path}' niet gevonden!")
            else:
                try:
                    with open(file_path, mode='r') as file:
                        csv_reader = csv.reader(file)
                        next(csv_reader)  # sla de eerste regel over

                        for row in csv_reader:
                            if len(row) < 2:
                                print(f"(gatelist) Ongeldige regel in CSV-bestand: {row}")
                                continue

                            try:
                                y=int(row[0])
                                x=int(row[1])
                                z=int(row[2])
                                self.grid_edit.add_gate(y,x,z)
                            except ValueError:
                                print(f'(gatelist) print:error met waardes in regel:{row}')
                                continue

                    print("(gatelist) Alle gates zijn succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("(gatelist) Fout: Ongeldige waarden in het CSV-bestand.")

    def load_netlist(self, file_path: str)->None:
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            connection_list=[]


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
                        
                        return connection_list, counter

                    print("Netlist is succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("(Netlist) Fout: Ongeldige waarden in het CSV-bestand.")

    def max_grid_values(self, file_path: str):
        """Bepaal de maximale y-, x-, en z-waarden uit een CSV-bestand.
        Het bestand moet een lijst van coördinaten bevatten.
        Retourneert een tuple (max_y, max_x, max_z)."""
         
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
                        y = int(row[0])
                        x = int(row[1])

                        max_y = max(max_y, y)
                        max_x = max(max_x, x)
                        max_y=max_y+2
                        max_x=max_x+2
                    except ValueError:
                        print(f"Fout bij het verwerken van regel: {row}")
                        continue

            print(f"Maximale waarden gevonden: y={max_y}, x={max_x}")
            return max_y, max_x

        except Exception as e:
            print(f"Fout tijdens het lezen van het bestand: {e}")
            return max_y, max_x  # Zorg voor een veilige return

class output:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj


    def print_grid (self) -> None:
        """
        print de huidig grid status met gates en verschillende lagen.
        """
        try:
            for z, layer in enumerate(self.grid_edit.grid):
                print(f"Laag {z}")
                for row in layer:
                    print(row)
        except IndexError:
            print("Fout bij het itereren door de grid. Controleer of de dimensies correct zijn.")
        except Exception as e:
            print(f"Onverwachte fout bij het printen van de grid: {e}")
        finally:
            print("Klaar met printen.")        

    def costen_berekening(self)->int:
        """berekent de score van de geplaatste draden"""
        score = (self.grid_edit.wirecount) + 300 * self.grid_edit.wirecrosscount
        return score
    
    def visualisatie(self):
        """
        Visualiseert de gates en wires in een 3D-omgeving.
        Gates worden weergegeven als blauwe punten en wires als rode lijnen.
        """
        # Gebruik het grid_edit object dat is doorgegeven aan de class
        grid_edit_obj = self.grid_edit
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')


        print(grid_edit_obj.gate_dict[2])
        print(grid_edit_obj.gate_nr)
        if not grid_edit_obj.gate_dict:
            print("geen gates in de dict")
            return
        
        # zet gates in visualisatie grid 
        for gate_nr, (y, x, z) in grid_edit.gate_dict.items():
            ax.scatter(x, y, z, color='blue', label=f'Gate {gate_nr}' if gate_nr == 1 else "", s=100)
        
         # maakt lijnen voor pad in visualisatie
        wires = self.grid_edit.wire_list
        if wires:
            wire_x, wire_y, wire_z = zip(*wires)
            
            ax.plot(wire_x, wire_y, wire_z, color='purple', linewidth=2, label='Wire Path')
        else:
            print("Geen wires gevonden")


        # Instellen van ticks met stappen van 1
        ax.set_xticks(range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 2, 1))
        ax.set_yticks(range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]) + 2, 1))
        ax.set_zlim(bottom = 1)
        ax.set_zticks(range(1, 10, 1))

        # correctie om y-as om te draaien 
        '''
        Dit maakt het mogelijk dat de coordinaten 0,0 voor x,y onderaan begint
        '''
        ax.invert_yaxis()
        ax.invert_xaxis()

        # Labels and legend
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title("3D Visualisatie van Gates en Wires")
        ax.legend()

        # Tweak the view
        ax.view_init(elev=30, azim=30)
        plt.show()    

class start:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Auto_start_functie(self, gate_path) ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        
        max_y, max_x = user_input_obj.max_grid_values(gate_path)

        grid_edit_obj.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
        
        # user_path=input("geef de file path op: ")
        user_input_obj.load_gates(gate_path)
        #user_input_obj.load_netlist(netlist_path)

class algorithm:

    def netlist_reorder(self, file_path):
        """reorderd de net list, vraagt zelf de netlist op"""
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)

        netlist, counter = user_input_obj.load_netlist(file_path)
        
        gate_count_list=[]
        max_y=0
        max_x=0

        print(netlist)

        for items in range(len(netlist)):
            chip_a=netlist[items][0]
            chip_b=netlist[items][1]

            gate_count_list.append(netlist[items][0])
            gate_count_list.append(netlist[items][1])

            y1, x1, z1=grid_edit_obj.gate_dict[netlist[items][0]]
            y2, x2, z2=grid_edit_obj.gate_dict[netlist[items][1]]

            #bepaalt de maximale x en y waardes
            if max_y<y1:
                max_y=y1
            if max_y<y2:
                max_y=y2
            if max_x<x1:
                max_x=x1
            if max_x<x2:
                max_x=x2      

        gate_list_count_balance=10
        score_list=[]

        counter=0
        for items in range(len(netlist)):
            #voegt de gates toe aan de list om bij te houden hoevaak hij verbonden is.
            y1, x1, z1=grid_edit_obj.gate_dict[netlist[items][0]]
            y2, x2, z2=grid_edit_obj.gate_dict[netlist[items][1]]

            chip_a=netlist[items][0]
            chip_b=netlist[items][1]

            #telt hoevaak de gates verbonden moeten zijn

            test1= gate_count_list.count(chip_a)
            test2= gate_count_list.count(chip_b)

            conection_amount=gate_list_count_balance-test1-test2

            a1 = abs(x1-(max_x/2))
            a2 = abs(y1-(max_y/2))
            a3 = abs(x2-(max_x/2))
            a4 = abs(y2-(max_y/2))

            afstand_midden = a1+a2+a3+a4

            #checkt de afstand tussen de gates
            v1 = abs(y1 - y2)
            v2 = abs(x1 - x2) 
            v3 = abs(z1 - z2)
            afstand_tussen_gates=v3+v2+v1

            score = afstand_tussen_gates*1 + afstand_midden*1 + conection_amount*1

            print(f"nr({counter}) -- score({score}) -- mid({afstand_midden}) -- tussen gates({afstand_tussen_gates}) -- cons({conection_amount})")

            score_list.append((counter, score))
            counter+=1

        sorted_list = sorted(score_list, key=lambda x: x[1])

        return_list=[]

        counter=0
        for counter in range(len(sorted_list)):
            return_tuple=sorted_list[counter][0]
            return_list.append(netlist[return_tuple])
            counter+=1

        print(f"return list===={return_list}")
        
        return return_list
        
    def gate_verbinding(self, gate_1, gate_2):
        """verbind de 2 gates die worden opgegeven door wires te leggen"""
        y2, x2, z2 = self.gate_dict[gate_2]
        y1, x1, z1 = self.gate_dict[gate_1]

        add_wire_list=[]

        #zorg voor dezelfde y hoogte

        #zorg voor dezelfde x hoogte

        #zorg voor dezelfde z hoogte

        #in elke 
            # check er niet al een wire is

    def gate_nr(self):
        grid_edit_obj=grid_edit()

        amount=0

        for item in grid_edit_obj.gate_dict:
            amount+=1
            item+=1

        print(f"amount{amount}")

        return amount
        

    def use_algorithm(self) ->None:
        #"grid_edit_obj.addgate(5,6,1)" om een gate toe tevoegen
        #"grid_edit_obj.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        min=1
        return "werkt nog niet"

class start_the_code:
    def manual_check():
        grid_edit_obj = grid_edit()
        start_obj =start(grid_edit_obj)
        output_obj=output(grid_edit_obj)
        user_input_obj=user_input(grid_edit_obj)
        algorithm_obj=algorithm()
        
        path_gates="gates.csv"
        path_netlist="netlist.csv"

        start_obj.Auto_start_functie(path_gates)

        nieuw_list=algorithm_obj.netlist_reorder(path_netlist)

        print(nieuw_list)
        
        print("De uiteindelijke grid is:")
        #output_obj.print_grid()

        print(algorithm_obj.use_algorithm())

        #output_obj.costen_berekening()
        #user_input_obj.score_request()

        #output_obj.visualisatie()
    
    manual_check()
