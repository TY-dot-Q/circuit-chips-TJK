from code.classes.grid_edit import grid_edit
from code.classes.user_input import user_input
from code.visualisation import visualisation as vis
from code.visualisation.visualisation import output
from code.classes.auto_start import auto_functions
from code.algorithms.manhattan_distance import ManhattanDistance as MD
from code.algorithms.netlist_reorder import netlist_reordering
from code.algorithms.hill_climber import hil_climber
from code.algorithms.crossless.hill_climber_nc import hil_climber_nc
from code.algorithms.crossless.mh_nc import mh_nc

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

    hil_climber_nc_obj=hil_climber_nc(grid_edit_obj)
    mh_nc_obj=mh_nc(grid_edit_obj)
    
    # Path van de grid en netlist die je wilt oplossen.
    grid_path="data/chip_0/print_0.csv"
    netlist_path="data/chip_0/netlist/netlist_1.csv"
    name_file = "data/test.csv"

    # maakt file weer leeg
    open(name_file, 'w').close()
    
    # maak de grid aan        
    start_obj.Auto_start_functie(grid_path)


    #----------------Netlist passer------------------------
    netlist_list=netlist_reorder_obj.netlist_reorder(netlist_path)
    #netlist_list=user_input_obj.load_netlist(netlist_path)
    
    
    

    #----------------No cross finder-----------------------
    reset_wires = 2 #hoeveel wires je per keer wilt laten verwijderen en opnieuw leggen
    reloop_time = 5 # de hoeveelheid tijd in minuten dat het opnieuw gaat lopen
    mh_nc_obj.netlist_looper(netlist_list)
    hil_climber_nc_obj.start_hill_climb(reset_wires, netlist_list, reloop_time)

    #----------------Manhatten distance---------------------
    #algorithm_obj.netlist_looper(netlist_list)


    #----------------Hill climber---------------------------
    # reset_wires = 5 #hoeveel wires je per keer wilt laten verwijderen en opnieuw leggen
    # reloop_time = 5 # de hoeveelheid tijd in minuten dat het opnieuw gaat lopen
    #hil_climber_obj.start_hill_climb(reset_wires, netlist_list, reloop_time) #wertk nog niet

    #-----------------resulten------------------------------
    #wirecount = grid_edit_obj.update_wirecount()
    # succes = grid_edit_obj.check_all_overlaps() 
    #grid_edit_obj.find_wirecross() 
    #match_wires = user_input_obj.match_wirepaths_to_nets(netlist_list)
    # scores bepalen
    #output_obj.costen_berekening(wirecount)
    #print(grid_edit_obj.score)
    #user_input_obj.score_request(wirecount)

    #----------------visualisatie----------------------------
    
    # print de grid in de terminal
    
    output_obj.print_grid() 

    
    #output_obj.output_to_csv(match_wires, netlist_path)

    # schrijf de resultaten naar het bestand wirepaths.csv
    #output_obj.write_to_csv(wirecount, name_file)
   
    # 3d visualisatie
    output_obj.visualisatie()
    
    # ----------------iteration runner----------------------------
    # Run the algorithm for a number of iterations
   # max_iterations = 100000
   # iterations = input("Hoeveel iteraties wil je runnen?: ")
    #while not iterations.isdigit() or int(iterations) > max_iterations:
        #iterations = input("Voer een geldig getal in tussen 1 en 100000: ")
   ## iterations = int(iterations)
   # for i in range(iterations):
        #grid_edit_obj.reset_grid()  # Reset the grid while keeping the gates in place

        # Run the algorithm on the netlist
        #algorithm_obj.netlist_looper(netlist_list)

        # Calculate wire count and wire crossings
        #wirecount = grid_edit_obj.update_wirecount()
        #grid_edit_obj.find_wirecross() 

        # Compute cost and score
        #output_obj.costen_berekening(wirecount)
        #user_input_obj.match_wirepaths_to_nets(netlist_list)
        #output_obj.write_to_csv(wirecount, name_file)
        #print(grid_edit_obj.valide_counter, grid_edit_obj.netlist_counter)

        #print(f"Iteration {i+1} Score: {grid_edit_obj.score}")

    # Sla resultaten op in een csv en visualiseer
   # row = output_obj.search_row(name_file)
    #output_obj.load_best_result(name_file, row)
    #match_wires = user_input_obj.match_wirepaths_to_nets(netlist_list)
    #output_obj.output_to_csv(match_wires, netlist_path)
    #output_obj.visualisatie() 