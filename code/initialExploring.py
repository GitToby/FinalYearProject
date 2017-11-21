import os
import time

import axelrod as axl
import axelrod_dojo as axl_dojo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

C, D = axl.Action

interesting_opponents = [axl.TitForTat(), axl.Alternator(), axl.Grudger(), axl.Random(), axl.EvolvedFSM16(),
                         axl.CollectiveStrategy()]
col_names = ["generation", "mean_score", "standard_deviation", "best_score", "sequence"]


def runGeneticAlgo(opponent, population_size=150, number_of_game_turns=200, cycle_length=200, generations=250,
                   mutation_probability=0.1, mutation_potency=1, reset_file=True):
    cycler_class = axl_dojo.CyclerParams
    cycler_objective = axl_dojo.prepare_objective(name="score", turns=number_of_game_turns, repetitions=1)
    cycler_kwargs = {
        "sequence_length": cycle_length,
        "mutation_probability": mutation_probability,
        "mutation_potency": mutation_potency
    }

    output_file_name = "data/" + str(opponent).replace(" ", "_") + ".csv"
    try:
        if reset_file and os.path.isfile(output_file_name):
            os.remove(output_file_name)
    finally:
        print(str(opponent),
              "|| pop size:", population_size,
              "\tturns:", number_of_game_turns,
              "\tcycle len:", cycle_length,
              "\tgens:", generations,
              "\tmut. rate:", mutation_probability,
              "\t, potency:", mutation_potency)

        axl.seed(1)

        population = axl_dojo.Population(params_class=cycler_class,
                                         params_kwargs=cycler_kwargs,
                                         size=population_size,
                                         objective=cycler_objective,
                                         output_filename=output_file_name,
                                         opponents=[opponent],
                                         print_output=False)
        population.run(generations)
        print("\tAnalysis Complete:", output_file_name)
    # Store the file name and opponent name as a tuple
    return output_file_name, str(opponent)


# ------------------------------POPULATION SIZE
populations = [25, 50, 100, 150, 200, 250, 500]


def populationChecker(opponent):
    # make a nice file name
    file_name = "data/" + str(opponent).replace(" ", "_").replace(":", "_").lower() + "_pop.csv"

    # if the file exists dont run, it takes forever, make sure it exists
    if not os.path.isfile(file_name):
        df_main = pd.DataFrame(data=None, columns=col_names)

        for pop_size in populations:
            start_time = time.clock()
            pop_run = runGeneticAlgo(opponent,
                                     population_size=pop_size,
                                     number_of_game_turns=200,
                                     cycle_length=200,
                                     generations=150,
                                     mutation_probability=0.1,
                                     reset_file=True)
            end_time = time.clock()
            tmp_df = pd.read_csv(pop_run[0], names=col_names)
            tmp_df["population"] = pop_size
            tmp_df["time_taken"] = end_time - start_time
            df_main = df_main.append(tmp_df, ignore_index=True)

        df_main.to_csv(file_name)
        print("List Complete:", file_name)
        return df_main
    else:
        print("file already exists, no calcs to do.")
        file_df = pd.read_csv(file_name)
        # remove first column
        file_df = file_df[list(file_df)[1:]]
        return file_df


df_TitForTat_pop = populationChecker(axl.TitForTat())
df_Alternator_pop = populationChecker(axl.Alternator())
df_Grudger_pop = populationChecker(axl.Grudger())
df_Random_pop = populationChecker(axl.Random())
df_Evolved_pop = populationChecker(axl.EvolvedFSM16())
df_Collective_pop = populationChecker(axl.CollectiveStrategy())

mutation_pop_dict = {"Tit For Tat": df_TitForTat_pop,
                     "Alternator": df_Alternator_pop,
                     "Grudger": df_Grudger_pop,
                     "Random": df_Random_pop,
                     "Evolved FSM16": df_Evolved_pop,
                     "Collective Stratergy": df_Collective_pop}

# PLOT
working_dict = mutation_pop_dict

f, axs = plt.subplots(2, 3, sharex=False, figsize=(20, 25))
f.suptitle("Improvments on best score over 150 generations with different initial populations")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("population"):
        axs[i % 2, i % 3].plot(df["generation"], df["best_score"], label=lab)
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Generations', ylabel='Best Score')
    axs[j % 2, j % 3].legend()

f.savefig('plots/initial_pop/ini_pop score all opponents.png')

# ------------------------------ GENERATION LENGTH
generation_list = [50, 150, 250, 350, 450, 500]


def generationSizeChecker(opponent):
    file_name = "data/" + str(opponent).replace(" ", "_").replace(":", "_").lower() + "_generation.csv"

    if not os.path.isfile(file_name):
        df_main = pd.DataFrame(data=None, columns=col_names)

        for gens in generation_list:
            start_time = time.clock()
            pop_run = runGeneticAlgo(opponent,
                                     population_size=150,
                                     number_of_game_turns=200,
                                     cycle_length=200,
                                     generations=gens,
                                     mutation_probability=0.1,
                                     reset_file=True)
            end_time = time.clock()
            tmp_df = pd.read_csv(pop_run[0], names=col_names)
            tmp_df["generations"] = gens
            tmp_df["time_taken"] = end_time - start_time
            tmp_df["opponent"] = str(opponent)
            tmp_df["best_score_diff"] = np.append([0], np.diff(tmp_df["best_score"]))
            df_main = df_main.append(tmp_df, ignore_index=True)

        df_main.to_csv(file_name)
        print("List Complete:", file_name)
        return df_main
    else:
        print("file ", file_name, " already exists, no calcs to do.")
        file_df = pd.read_csv(file_name)
        # remove first column
        file_df = file_df[list(file_df)[1:]]
        return file_df


df_TitForTat_gen = generationSizeChecker(axl.TitForTat())
df_Alternator_gen = generationSizeChecker(axl.Alternator())
df_Grudger_gen = generationSizeChecker(axl.Grudger())
df_Random_gen = generationSizeChecker(axl.Random())
df_Evolved_gen = generationSizeChecker(axl.EvolvedFSM16())
df_Collective_gen = generationSizeChecker(axl.CollectiveStrategy())

mutation_gen_dict = {"Tit For Tat": df_TitForTat_gen,
                     "Alternator": df_Alternator_gen,
                     "Grudger": df_Grudger_gen,
                     "Random": df_Random_gen,
                     "Evolved FSM16": df_Evolved_gen,
                     "Collective Stratergy": df_Collective_gen}

# PLOT
working_dict = mutation_gen_dict

f, axs = plt.subplots(2, 3, sharex=False, sharey=True, figsize=(20, 20))
f.suptitle("Average increase of score vs # of generations")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("generations"):
        axs[i % 2, i % 3].scatter(lab, df["best_score_diff"].mean(), label="{:3.0f} generations".format(lab))
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Total generations', ylabel='Best Score')
    axs[j % 2, j % 3].legend()

f.savefig('plots/gen_len/gen_len avg diff all opponents.png')

# PLOT2
working_dict = mutation_gen_dict

f, axs = plt.subplots(2, 3, sharex=False, figsize=(20, 20))
f.suptitle("Max best score vs # of generations coloured by time")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("generations"):
        axs[i % 2, i % 3].scatter(lab, df["best_score"].max(), label="{:3.0f} generations".format(lab))
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Total generations', ylabel='Best Score')
    axs[j % 2, j % 3].legend()

f.savefig('plots/gen_len/gen_len best score all opponents.png')

# ------------------------------ MUTATION POTENCY
mutation_potency_list = [1, 2, 3, 5, 10, 15, 20]


def mutationPotencyChecker(opponent):
    file_name = "data/" + str(opponent).replace(" ", "_").replace(":", "_").lower() + "_mutation_potency.csv"

    if not os.path.isfile(file_name):
        df_main = pd.DataFrame(data=None, columns=col_names)

        for potency in mutation_potency_list:
            start_time = time.clock()
            pot_run = runGeneticAlgo(opponent,
                                     population_size=150,
                                     number_of_game_turns=200,
                                     cycle_length=200,
                                     generations=250,
                                     mutation_probability=0.1,
                                     mutation_potency=potency,
                                     reset_file=True)
            end_time = time.clock()
            tmp_df = pd.read_csv(pot_run[0], names=col_names)
            tmp_df["mutation_potency"] = potency
            tmp_df["time_taken"] = end_time - start_time
            tmp_df["opponent"] = str(opponent)
            tmp_df["best_score_diff"] = np.append([0], np.diff(tmp_df["best_score"]))
            df_main = df_main.append(tmp_df, ignore_index=True)

        df_main.to_csv(file_name)
        print("List Complete:", file_name)
        return df_main
    else:
        print("file ", file_name, " already exists, no calcs to do.")
        file_df = pd.read_csv(file_name)
        # remove first column
        file_df = file_df[list(file_df)[1:]]
        return file_df


df_TitForTat_potency = mutationPotencyChecker(axl.TitForTat())
df_Alternator_potency = mutationPotencyChecker(axl.Alternator())
df_Grudger_potency = mutationPotencyChecker(axl.Grudger())
df_Random_potency = mutationPotencyChecker(axl.Random())
df_Evolved_potency = mutationPotencyChecker(axl.EvolvedFSM16())
df_Collective_potency = mutationPotencyChecker(axl.CollectiveStrategy())

mutation_potency_dict = {"Tit For Tat": df_TitForTat_potency,
                         "Alternator": df_Alternator_potency,
                         "Grudger": df_Grudger_potency,
                         "Random": df_Random_potency,
                         "Evolved FSM16": df_Evolved_potency,
                         "Collective Stratergy": df_Collective_potency}

# PLOT
working_dict = mutation_potency_dict

f, axs = plt.subplots(2, 3, sharex=False, figsize=(20, 25))
f.suptitle("")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("mutation_potency"):
        axs[i % 2, i % 3].plot(df["generation"], df["best_score"], label=lab)
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Generations', ylabel='Best Score')
    axs[j % 2, j % 3].legend()

f.savefig('plots/mutation_pot/mut_pot all opponents.png')

# PLOT2
working_dict = mutation_potency_dict

f, axs = plt.subplots(2, 3, sharex=False, sharey=True, figsize=(20, 25))
f.suptitle("")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("mutation_potency"):
        axs[i % 2, i % 3].scatter(lab, df["best_score_diff"].mean(), label=lab)
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Mutation Potency', ylabel='Best Score Diff')
    axs[j % 2, j % 3].axhline(0)
    axs[j % 2, j % 3].legend()

f.savefig('plots/mutation_pot/mut_pot score diff all opponents.png')

# ------------------------------ MUTATION FREQ
mutation_frequency_list = [0.1, 0.15, 0.2, 0.25]


def mutationFrequencyChecker(opponent):
    file_name = "data/" + str(opponent).replace(" ", "_").replace(":", "_").lower() + "_mutation_frequency.csv"

    if not os.path.isfile(file_name):
        df_main = pd.DataFrame(data=None, columns=col_names)

        for freq in mutation_frequency_list:
            start_time = time.clock()
            pot_run = runGeneticAlgo(opponent,
                                     population_size=150,
                                     number_of_game_turns=200,
                                     cycle_length=200,
                                     generations=250,
                                     mutation_probability=freq,
                                     mutation_potency=1,
                                     reset_file=True)
            end_time = time.clock()
            tmp_df = pd.read_csv(pot_run[0], names=col_names)
            tmp_df["mutation_frequency"] = freq
            tmp_df["time_taken"] = end_time - start_time
            tmp_df["opponent"] = str(opponent)
            tmp_df["best_score_diff"] = np.append([0], np.diff(tmp_df["best_score"]))
            df_main = df_main.append(tmp_df, ignore_index=True)

        df_main.to_csv(file_name)
        print("List Complete:", file_name)
        return df_main
    else:
        print("file ", file_name, " already exists, no calcs to do.")
        file_df = pd.read_csv(file_name)
        # remove first column
        file_df = file_df[list(file_df)[1:]]
        return file_df


df_TitForTat_freq = mutationFrequencyChecker(axl.TitForTat())
df_Alternator_freq = mutationFrequencyChecker(axl.Alternator())
df_Grudger_freq = mutationFrequencyChecker(axl.Grudger())
df_Random_freq = mutationFrequencyChecker(axl.Random())
df_Evolved_freq = mutationFrequencyChecker(axl.EvolvedFSM16())
df_Collective_freq = mutationFrequencyChecker(axl.CollectiveStrategy())

mutation_freq_dict = {"Tit For Tat": df_TitForTat_freq,
                      "Alternator": df_Alternator_freq,
                      "Grudger": df_Grudger_freq,
                      "Random": df_Random_freq,
                      "Evolved FSM16": df_Evolved_freq,
                      "Collective Stratergy": df_Collective_freq}

# PLOT
working_dict = mutation_freq_dict

f, axs = plt.subplots(2, 3, sharex=False, figsize=(20, 30))
f.suptitle("")

a = 0
for opponent in working_dict:
    axs[a % 2, a % 3].set_title(opponent)
    a += 1

i = 0
for opponet in working_dict:
    for lab, df in working_dict.get(opponet).groupby("mutation_frequency"):
        axs[i % 2, i % 3].plot(df["generation"], df["best_score"], label=lab)
    i += 1

for j in range(len(working_dict)):
    axs[j % 2, j % 3].set(xlabel='Generations', ylabel='Best Score')
    axs[j % 2, j % 3].legend()

f.savefig('plots/mutation_freq/mut_freq all opponents.png')
