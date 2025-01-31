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
    #-----------------SETUP-------------------------------
    """
    Gelieve de setup niet te veranderen tenzij je de chips en/of netlist
    wil veranderen!!!
    Om werking van alle algoritmes te bewerkstellingen
    """
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
    
    # Paden van de grid en netlist die je wilt oplossen.
    """
    Verander hier de chip en/of netlist waarvan je de oplossing wil genereren
    """
    grid_path="data/chip_1/print_1.csv"
    netlist_path="data/chip_1/netlist/netlist_1.csv"

    # Pad voor output opslag -> beste resultaat.
    name_file = "data/data.csv"

    # maakt file weer leeg
    open(name_file, 'w').close()
    
    # maak de grid aan        
    start_obj.Auto_start_functie(grid_path)

    # netlist reorder heuristiek
    netlist_list=netlist_reorder_obj.netlist_reorder(netlist_path)
    netlist_list=user_input_obj.load_netlist(netlist_path)
    
    
    #----------------ALGORITMES----------------------------
    #***************** No cross finder **********************
    """
    Dit algoritme gebruikt een hill climber die ten koste van alles
    kruisingen voorkomt
    """

    """
    # hoeveel wires je per keer wilt laten verwijderen en opnieuw leggen
    reset_wires_amount = 3 #default = 3

    # de hoeveelheid tijd in minuten dat het opnieuw gaat lopen
    reloop_time = 30 # default = 30 

    # A* algoritme met effectieve hillclimber algoritme
    mh_nc_obj.netlist_looper(netlist_list)
    optimum=hil_climber_nc_obj.start_hill_climb(reset_wires_amount, netlist_list, reloop_time)"""


    #********************* Hill climber *************************
    """
    Dit algoritme is een hill climber die wel kruisingen aangaat
    Deze werkt nog niet optimaal
    """

    """
    # hoeveel wires je per keer wilt laten verwijderen en opnieuw leggen
    reset_wires = 3 # default = 3

    # de hoeveelheid tijd in minuten dat het opnieuw gaat lopen
    reloop_time = 30 # default = 30 
    hil_climber_obj.start_hill_climb(reset_wires, netlist_list, reloop_time)"""

    # ************* Manhattan Distance met iteration runner*********
    """
    Dit algoritme zoekt het kortste pad met aanvullende heuristieken
    Dit algoritme legt maar een netwerk, dus voor beste oplossing moeten 
    meerdere iteraties gedaan worden
    """
    # Run the algorithm for a number of iterations
    max_iterations = 10000
    iterations = input("Hoeveel iteraties wil je runnen?: ")
    while not iterations.isdigit() or int(iterations) > max_iterations:
        iterations = input("Voer een geldig getal in tussen 1 en 100000: ")
    iterations = int(iterations)
    for i in range(iterations):
        grid_edit_obj.reset_grid()  # Reset the grid while keeping the gates in place

        # Run the algorithm on the netlist
        algorithm_obj.netlist_looper(netlist_list)

    #---------------RESULTATEN GENEREREN----------------------
    """
    Zorgt dat alle parameters en het genereren van de output 
    succesvol verlopen. Dus ook deze niet aanpassen!!!
    """

    # berekent aantal draden en kruisingen
    wirecount = grid_edit_obj.update_wirecount()
    grid_edit_obj.find_wirecross() 

    # kosten en scores berekenen
    output_obj.costen_berekening(wirecount)
    user_input_obj.match_wirepaths_to_nets(netlist_list)
    output_obj.write_to_csv(wirecount, name_file)

    # Sla resultaten op in csv en visualiseer
    output_obj.load_best_result(name_file)
    match_wires = user_input_obj.match_wirepaths_to_nets(netlist_list)
    output_obj.output_to_csv(match_wires, netlist_path)
    output_obj.visualisatie() 