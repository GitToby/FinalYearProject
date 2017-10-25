import axelrod as axl
import axelrod_dojo as axl_dojo

C, D = axl.Action

# Cycler ##############################
cycler_objective = axl_dojo.prepare_objective(name="score", turns=10, repetitions=1)

# Lets use an opponent_list of just one:
opponent_list = [axl.TitForTat()]
cycler = axl_dojo.CyclerParams

# params to pass through
cycler_kwargs = {
    "sequence_length": 50
}

population = axl_dojo.Population(params_class=cycler,
                                 params_kwargs=cycler_kwargs,
                                 size=20,
                                 objective=cycler_objective,
                                 output_filename="cyclerOutput.csv",
                                 opponents=opponent_list)

axl.seed(0)
cycler_generations = 4
population.run(cycler_generations)


# FSM Example ##############################
# fsm_objective = axl_dojo.prepare_objective(name="score", turns=10, repetitions=1)
# fsm_opponents = [axl.TitForTat(), axl.Alternator(), axl.Defector()]
#
# fsm = axl_dojo.FSMParams
# kwargs = {"num_states": 2}
#
# axl.seed(1)
# pop = axl_dojo.Population(params_class=fsm,
#                           params_kwargs=kwargs,
#                           size=20,
#                           objective=fsm_objective,
#                           output_filename="training_output.csv",
#                           opponents=fsm_opponents,
#                           bottleneck=2,
#                           mutation_probability=0)
#
# generations = 4
# pop.run(generations)
###########################################
