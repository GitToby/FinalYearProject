import os

import axelrod as axl
import axelrod_dojo as axl_dojo
import matplotlib.pyplot as plt
import pandas as pd
import time

C, D = axl.Action


# Cycler ##############################


def runGeneticAlgo(opponent, population_size=20, number_of_game_turns=200, cycle_length=200, generations=150,
                   reset_file=True, mutation_probability=0.1):
    cycler_class = axl_dojo.CyclerParams
    cycler_objective = axl_dojo.prepare_objective(name="score", turns=number_of_game_turns, repetitions=1)
    cycler_kwargs = {
        "sequence_length": cycle_length,
        "mutation_probability": 0.1
    }

    output_file_name = "code/output/" + str(opponent) + ".csv"
    try:
        if reset_file and os.path.isfile(output_file_name):
            os.remove(output_file_name)
            print("reset file: " + output_file_name)
        else:
            print("no file reset")
    finally:
        print("working on:", str(opponent), "|-------|"
                                            "\t population size:", population_size,
              "\t turns:", number_of_game_turns,
              "\tcycle length:", cycle_length,
              "\tgenerations:", generations)

        population = axl_dojo.Population(params_class=cycler_class,
                                         params_kwargs=cycler_kwargs,
                                         size=population_size,
                                         objective=cycler_objective,
                                         output_filename=output_file_name,
                                         opponents=[opponent],
                                         print_output=False)
        population.run(generations)
        print("Analysis Complete")

    return output_file_name, str(opponent)


# Lets use an opponent_list of just one:
opponent_list = [axl.TitForTat(), axl.Alternator(), axl.Defector(), axl.Gradual(), axl.Cycler()]
opponent_list2 = axl.demo_strategies  # to use later

# outfile contains:
# | Gen# | generation mean Score | standard deviation | Best Score | Best Sequence |
col_names = ["generation", "mean_score", "standard_deviation", "best_score", "sequence"]

# Population Size Analysis
run_file_name, run_opponent = runGeneticAlgo(opponent_list[0], population_size=50, number_of_game_turns=100,
                                             cycle_length=10, generations=30, reset_file=True)
populations = [25, 50, 100, 200]

# Tit for Tat population Analysis
df_TitForTat = pd.DataFrame(data=None, columns=col_names)
for pop_size in populations:
    tmp_file_name, x = runGeneticAlgo(opponent_list[0], population_size=pop_size, number_of_game_turns=100,
                                      cycle_length=100, generations=150, reset_file=True)
    tmp_df = pd.read_csv(tmp_file_name, names=col_names)
    tmp_df["population"] = pop_size
    df_TitForTat = df_TitForTat.append(tmp_df, ignore_index=True)
df_TitForTat.to_csv("code/output/df_TitForTat_pop_sizes.csv")

# Altenator Population Analysis
df_Altenator = pd.DataFrame(data=None, columns=col_names)
for pop_size in populations:
    tmp_file_name, x = runGeneticAlgo(opponent_list[1], population_size=pop_size, number_of_game_turns=100,
                                      cycle_length=100, generations=150, reset_file=True)
    tmp_df = pd.read_csv(tmp_file_name, names=col_names)
    tmp_df["population"] = pop_size
    df_Altenator = df_Altenator.append(tmp_df, ignore_index=True)
df_Altenator.to_csv("code/output/df_Altenator_pop_sizes.csv")

# Gradual Population Analysis
df_Gradual = pd.DataFrame(data=None, columns=col_names)
for pop_size in populations:
    tmp_file_name, x = runGeneticAlgo(opponent_list[3], population_size=pop_size, number_of_game_turns=100,
                                      cycle_length=100, generations=150, reset_file=True)
    tmp_df = pd.read_csv(tmp_file_name, names=col_names)
    tmp_df["population"] = pop_size
    df_Gradual = df_Gradual.append(tmp_df, ignore_index=True)
df_Gradual.to_csv("code/output/df_Gradual_pop_sizes.csv")

df1 = pd.read_csv(run_file_name, names=col_names)
df2 = pd.read_csv(run_file_name, names=col_names)

df1.append(df2)

# PLOTTING DATA -----------
mean_scores = df_TitForTat["mean_score"]
best_scores = df_TitForTat["best_score"]
standard_dev = df_TitForTat["standard_deviation"]
generation = df_TitForTat["generation"]

plt.figure(2)
plt.plot

plt.figure(1)
plt.subplot(211)
plt.title("akhskfh")
plt.pl
ot(generation, standard_dev)
plt.ylabel("standard deviation")

plt.subplot(212)
plt.plot(generation, mean_scores)
plt.ylabel("mean score")
plt.plot(generation, best_scores)
plt.ylabel("best/mean scores")

plt.xlabel("Generation")
plt.figure(1).draw
plt.show()

plt.close()


def populationChecker(opponent):
    file_name = "data/" + str(opponent).lower() + "_pop.csv"

    # if the file exists dont run, it takes forever, make sure it exists
    if not os.path.isfile(file_name):
        df_main = pd.DataFrame(data=None, columns=col_names)

        for pop_size in populations:
            start_time = time.clock()
            pop_run = runGeneticAlgo(axl.TitForTat(),
                                     population_size=pop_size,
                                     number_of_game_turns=200,
                                     cycle_length=200,
                                     generations=150,
                                     mutation_probability=0.1,
                                     reset_file=True)
            end_time = time.clock()
            tmp_df = pd.read_csv(pop_run[0], names=col_names)
            tmp_df["population"] = pop_size
            tmp_df["timeTaken"] = end_time - start_time
            df_main = df_main.append(tmp_df, ignore_index=True)

        df_main.to_csv(file_name)
        print("List Complete:", file_name)
        return df_main
    else:
        print("file exists")
        return pd.read_csv(file_name, names=col_names)


x = [1, 2, 3]
y = [1, 2, 3]
size = [0.5, 1, 1.5]
plt.scatter(x, y, size)
