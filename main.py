from code.classes.grid_edit import grid_edit
from code.classes.user_input import user_input
from code.visualisation import visualisation as vis
from code.visualisation.visualisation import output
from code.classes.auto_start import auto_functions
from code.algorithms.manhattan_distance import ManhattanDistance as MD

if __name__ == "__main__":
    grid_edit_obj = grid_edit()

    path="print_0.csv"

    user_input_obj = user_input(grid_edit_obj)
    output_obj = output(grid_edit_obj)
    start_obj = auto_functions(grid_edit_obj)
    algorithm_obj= MD(grid_edit_obj)
            
    start_obj.Auto_start_functie(path)

    # Voeg de wirepaths toe aan de CSV
    output_obj.print_grid()
    output_obj.write_to_csv(grid_edit_obj.wirepaths_list)

    output_obj.costen_berekening()
    user_input_obj.score_request()

    output_obj.visualisatie()
