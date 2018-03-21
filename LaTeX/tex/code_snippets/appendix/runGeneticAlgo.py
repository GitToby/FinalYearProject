def runGeneticAlgo(opponent, population_size=150, number_of_game_turns=200, cycle_length=200, generations=250,
                   mutation_probability=0.1, mutation_potency=1, reset_file=True):
    cycler_class = axl_dojo.CyclerParams
    cycler_objective = axl_dojo.prepare_objective(name="score", turns=number_of_game_turns, repetitions=1)
    cycler_kwargs = {
        "sequence_length": cycle_length,
        "mutation_probability":mutation_probability,
        "mutation_potency":mutation_potency
    }

    output_file_name = "data/" + str(opponent).replace(" ","_") + ".csv"
    try:
        if reset_file and os.path.isfile(output_file_name):
            os.remove(output_file_name)
    finally:
        print(str(opponent), 
              "|| pop size:", population_size,
              "\tturns:", number_of_game_turns,
              "\tcycle len:", cycle_length,
              "\tgens:", generations,
              "\tmut. rate:",mutation_probability,
              "\t, potency:",mutation_potency)
        
        axl.seed(1)
            
        population = axl_dojo.Population(params_class=cycler_class,
                                         params_kwargs=cycler_kwargs,
                                         size=population_size,
                                         objective=cycler_objective,
                                         processes=0,
                                         output_filename=output_file_name,
                                         opponents=[opponent],
                                         print_output=False)
        population.run(generations)
        print("\tAnalysis Complete:",output_file_name)
    # Store the file name and opponent name as a tuple
    return output_file_name, str(opponent)