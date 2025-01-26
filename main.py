from code.classes import grid_edit, output, user_input, auto_start
from code.visualisation import visualisation as vis

#from code.algorithms import ...

if __name__ =="__main__":
    grid_edit_obj=grid_edit()

    path="gates.csv"

    grid_edit_obj = grid_edit()
    user_input_obj = user_input(grid_edit_obj)
    output_obj = output(grid_edit_obj)
    start_obj =start(grid_edit_obj)
    algorithm_obj=algorithm(grid_edit_obj)
            
    start_obj.Auto_start_functie(path)

    # Voeg de wirepaths toe aan de CSV
    output_obj.print_grid()
    output_obj.write_to_csv(grid_edit_obj.wirepaths_list)

    output_obj.costen_berekening()
    user_input_obj.score_request()

    output_obj.visualisatie()
