from classes import user_input

class netlist_reordering:
    def netlist_reorder(self, file_path):
        """reorderd de net list, vraagt zelf de netlist op"""
        user_input_obj = user_input(self.grid_edit)

        netlist, counter = user_input_obj.load_netlist(file_path)
        
        gate_count_list=[]
        max_y=0
        max_x=0

        for items in range(len(netlist)):
            chip_a=netlist[items][0]
            chip_b=netlist[items][1]

            gate_count_list.append(netlist[items][0])
            gate_count_list.append(netlist[items][1])

            y1, x1, z1=self.grid_edit.gate_dict[netlist[items][0]]
            y2, x2, z2=self.grid_edit.gate_dict[netlist[items][1]]

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
            y1, x1, z1=self.grid_edit.gate_dict[netlist[items][0]]
            y2, x2, z2=self.grid_edit.gate_dict[netlist[items][1]]

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

        print(f"orginele list --- {netlist}")
        print(f"nieuwe list ----- {return_list}")
        
        return return_list