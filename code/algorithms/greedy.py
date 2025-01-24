class greedy:
    def greedy_connect(self, chip_a, chip_b, wire_path_count):
        """zoekt de kortste pad tussen twee punten en legt hier dan draden tussen
        dit wordt terug gegeven in een lijst, de lijst die hij ontvangt is de volgorde aan punt verbindingen die hij eerst gaat leggen"""
        #todo:
        #zorg dat de andere gates niet worden opgegeten
        #zorg dat het niet over andere draden heen gaat
        #zorg de draden duidelijk in een list worden neergezet

        #grid_edit
        #zorg dat je een list aan wires weg kan halen

        #algo 
        #zorg dat je een specifieke lijn opnieuw kan leggen

        
        current_wire_nr=0

        complete_wire_list=[]

        y1, x1, z1 = self.grid_edit.gate_dict[chip_a]
        y2, x2, z2 = self.grid_edit.gate_dict[chip_b]

        print("")
        print("")
        print(f"Nieuwe connect gates ----{wire_path_count}------")

        print("Dit is de check of de grid leeg is:",len(self.grid_edit.grid))

        print(f"chip_nr ={chip_a} met waarde: y={y1}, x={x1}, z={z1}")
        print(f"chip_nr ={chip_b} met waarde: y={y2}, x={x2}, z={z2}")

        cy, cx , cz = y1, x1, z1 

        while cy != y2 or cx != x2 or cz != z2:

            dif_y = cy-y2
            dif_x = cx-x2
            dif_z = cz-z2

            pos_change_y=0
            pos_change_x=0
            pos_change_z=0

            print(f"dif_y ={dif_y} -- dif_x={dif_x} -- dif_z={dif_z}")

            if dif_y <0:
                pos_change_y=1
            elif dif_y>0:
                pos_change_y=-1

            if dif_x <0:
                pos_change_x=1
            elif dif_x>0:
                pos_change_x=-1
            
            if dif_z <0:
                pos_change_z=1
            elif dif_z>0:
                pos_change_z=-1

            print(f"pos change y =({pos_change_y}), pos change x =({pos_change_y}), pos change z=({pos_change_z}) ")

            #probeer dichterbij te komen op de y-as
            if cy!=y2:
                #check of er op de volgende stap niet al iets is
                if self.grid_edit.gate_dict[cy+pos_change_y]!=0:
                    #verander de huidige coordinaten en voeg de wire toe aan de lijst
                    cy+=pos_change_y

                #check of de volgende plek een wire is
                #if self.grid_edit.gate_dict[cy+pos_change_y]=="+":
                    #print("nothing")

            elif cx!=x2:
                check = cx+pos_change_x
                print(f"check value{check}")
                if self.grid_edit.gate_dict[cx+pos_change_x]!=0:
                    #verander de huidige coordinaten en voeg de wire toe aan de lijst
                    cx+=pos_change_x

                #check of de volgende plek een wire is
                #if self.grid_edit.gate_dict[cx+pos_change_x]=="+":
                    #print("nothing")

            elif cz!=z2:
                if self.grid_edit.gate_dict[cz+pos_change_z]!=0:
                    #verander de huidige coordinaten en voeg de wire toe aan de lijst
                    cz+=pos_change_z

                #check of de volgende plek een wire is
                #if self.grid_edit.gate_dict[cz+pos_change_z]=="+":
                    #print("nothing")
            
            self.grid_edit.add_wire(cy, cx, cz)
            complete_wire_list.append(([wire_path_count],[current_wire_nr],([cy, cx, cz ])))

            current_wire_nr+=1

            print(f"{current_wire_nr}")
            print("")

        print(f"Current wire path = {wire_path_count}")
    
        #print(complete_wire_list[wire_path_count-1])