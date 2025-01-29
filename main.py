from code.classes.grid_edit import grid_edit
from code.classes.user_input import user_input
from code.visualisation import visualisation as vis
from code.visualisation.visualisation import output
from code.classes.auto_start import auto_functions
from code.algorithms.manhattan_distance import ManhattanDistance as MD
from code.algorithms.netlist_reorder import netlist_reordering
from code.algorithms.hill_climber import hil_climber

if __name__ == "__main__":
    #-----------------setup-------------------------------

    # maakt een instantie van grid edit aan en geeft dit door aan andere classes
    grid_edit_obj = grid_edit()

    user_input_obj = user_input(grid_edit_obj)
    output_obj = output(grid_edit_obj)
    start_obj = auto_functions(grid_edit_obj)
    algorithm_obj= MD(grid_edit_obj)
    netlist_reorder_obj=netlist_reordering(grid_edit_obj)
    hil_climber_obj=hil_climber(grid_edit_obj)
    
    # Path van de grid en netlist die je wilt oplossen.
    grid_path="data/chip_1/print_1.csv"
    netlist_path="data/chip_1/netlist/netlist_2.csv"

    # maak de grid aan        
    start_obj.Auto_start_functie(grid_path)


    #----------------Netlist passer------------------------
    netlist_list=netlist_reorder_obj.netlist_reorder(netlist_path)
    #netlist_list=user_input_obj.load_netlist(netlist_path)
    

    #----------------Manhatten distance---------------------
    algorithm_obj.netlist_looper(netlist_list)


    #----------------Hill climber---------------------------
    reset_wires = 5 #hoeveel wires je per keer wilt laten verwijderen en opnieuw leggen
    reloop_time = 5 # de hoeveelheid tijd in minuten dat het opnieuw gaat lopen
    #hil_climber_obj.start_hill_climb(reset_wires, netlist_list, reloop_time) #wertk nog niet

    #-----------------resulten------------------------------
    wirecount = grid_edit_obj.update_wirecount()
    succes = grid_edit_obj.check_all_overlaps() 
    grid_edit_obj.find_wirecross() 

    # scores bepalen
    output_obj.costen_berekening(wirecount)
    user_input_obj.score_request(wirecount)

    #----------------visualisatie----------------------------
    
    # print de grid in de terminal
    
    #output_obj.print_grid() 

    # schrijf de resultaten naar het bestand wirepaths.csv
    #output_obj.write_to_csv(grid_edit_obj.wirepaths_list, grid_edit_obj.overlapping_lijst, wirecount)
   
    # 3d visualisatie
    output_obj.visualisatie()
