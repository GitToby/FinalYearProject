import axelrod as axl
import axelrod_dojo as axl_dojo

C, D = axl.Action

# Cycler ##############################
cycler_objective = axl_dojo.prepare_objective(name="score", turns=20, repetitions=1)

# Lets use an opponent_list of just one:
opponent_list = [axl.TitForTat()]
cycler = axl_dojo.CyclerParams

# params to pass through
cycler_kwargs = {
    "sequence_length": 10
}

population = axl_dojo.Population(params_class=cycler,
                                 params_kwargs=cycler_kwargs,
                                 size=20,
                                 bottleneck=1,
                                 objective=cycler_objective,
                                 output_filename="output/cyclerOutput.csv",
                                 opponents=opponent_list)

cycler_generations = 20
population.run(cycler_generations)

