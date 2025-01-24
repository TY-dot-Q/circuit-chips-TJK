from classes import user_input

class auto_start:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Auto_start_functie(self, user_path) ->None:
            """
            deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
            """
            user_input_obj = user_input(self.grid_edit)

            #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
            
            max_y, max_x = user_input_obj.max_grid_values(user_path)
            print(max_x, max_y)
            self.grid_edit.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
            
            # user_path=input("geef de file path op: ")
            user_input_obj.load_gates(user_path)