from code.classes.user_input import user_input

class auto_functions:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Auto_start_functie(self, user_path) ->None:
            """
            Maakt automatisch een grid aan, neemt de gatelist als input om de max coordinaten te bepalen
            """
            user_input_obj = user_input(self.grid_edit)

            #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
            
            max_y, max_x = user_input_obj.max_grid_values(user_path)
            #print(max_x, max_y)
            self.grid_edit.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
            
            # user_path=input("geef de file path op: ")
            user_input_obj.load_gates(user_path)

    def wire_list_laying(self, connection_list):
        """gaat over de opgegeven wire list en gebruikt een andere functie (nu connect_two_gates) om de draden te verbinden"""

        wire_path_count=0

        for wire_path_count in range(len(connection_list)):
            chip_a =connection_list[wire_path_count][0]
            chip_b =connection_list[wire_path_count][1]
            self.connect_two_gates(chip_a, chip_b, wire_path_count)

            wire_path_count+=1