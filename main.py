from code.classes.grid_edit import grid_edit
from code.classes.user_input import user_input
from code.visualisation import visualisation as vis
from code.visualisation.visualisation import output
from code.classes.auto_start import auto_functions
from code.algorithms.manhattan_distance import ManhattanDistance as MD
from code.algorithms.netlist_reorder import netlist_reordering

if __name__ == "__main__":
    #maakt een instancie van grid edit aan en geeft dit door aan andere classes
    grid_edit_obj = grid_edit()
    
    user_input_obj = user_input(grid_edit_obj)
    output_obj = output(grid_edit_obj)
    start_obj = auto_functions(grid_edit_obj)
    algorithm_obj= MD(grid_edit_obj)
    netlist_reorder_obj=netlist_reordering(grid_edit_obj)
    
    
    #Path van de grid en netlist die je wilt oplossen.
    grid_path="data/chip_0/print_0.csv"
    netlist_path="data/chip_0/netlist/netlist_1.csv"

    #maak de grid aan        
    start_obj.Auto_start_functie(grid_path)


    #----------------Netlist reorder-----------------------
    netlist_reorder_obj.netlist_reorder(netlist_path)
    

    #----------------Manhatten distance--------------------
    algorithm_obj.netlist_looper(netlist_path)


    #-----------------resulten------------------------------
    
    succes = grid_edit_obj.check_all_overlaps()
    output_obj.write_to_csv(grid_edit_obj.wirepaths_list, succes) 

    #scoren bepalen
    output_obj.costen_berekening()
    user_input_obj.score_request()
    
    #print de grid in de terminal
    output_obj.print_grid()
   
   #visualtisatie
    output_obj.visualisatie()
