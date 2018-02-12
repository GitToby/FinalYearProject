import csv
import itertools

import axelrod as axl
import axelrod_dojo as axl_dojo
import numpy as np
import os

SEQUENCE_LENGTH = 200
POPULATION_SIZE = 250
GENERATION_LENGTH = 300
MUTATION_FREQUENCY = 0.1
MUTATION_POTENCY = 1

C, D = axl.Action

def getPreMadePop(pop_size: int):
    pop = []

    # Totalities & Handshakes
    handshake_leng = 5
    for start in itertools.product("CD", repeat=handshake_leng):
        pop.append(axl_dojo.CyclerParams(list(start) + [C] * (200 - handshake_leng)))
        pop.append(axl_dojo.CyclerParams(list(start) + [D] * (200 - handshake_leng)))

    # 50-50
    pop.append(axl_dojo.CyclerParams([C] * 100 + [D] * 100))
    pop.append(axl_dojo.CyclerParams([D] * 100 + [C] * 100))

    # Single Change
    for i in range(1, 11):
        pop.append(axl_dojo.CyclerParams([C] * i + [D] * (200 - i)))
        pop.append(axl_dojo.CyclerParams([D] * i + [C] * (200 - i)))

    for i in range(1, 11):
        pop.append(axl_dojo.CyclerParams([C] * (200 - i) + [D] * i))
        pop.append(axl_dojo.CyclerParams([D] * (200 - i) + [C] * i))

    # Matching Tails
    for i in range(1, 6):
        for j in range(1, 6):
            pop.append(axl_dojo.CyclerParams([C] * i + [D] * (200 - (i + j)) + [C] * j))
            pop.append(axl_dojo.CyclerParams([D] * i + [C] * (200 - (i + j)) + [D] * j))

    # Alternating
    pop.append(axl_dojo.CyclerParams([C, D] * 100))
    pop.append(axl_dojo.CyclerParams([D, C] * 100))
    pop.append(axl_dojo.CyclerParams([C, C, D, D] * 50))
    pop.append(axl_dojo.CyclerParams([D, D, C, C] * 50))
    pop.append(axl_dojo.CyclerParams([C, C, C, C, D, D, D, D] * 25))
    pop.append(axl_dojo.CyclerParams([D, D, D, D, C, C, C, C] * 25))
    pop.append(axl_dojo.CyclerParams([C, C, C, C, C, D, D, D, D, D] * 20))
    pop.append(axl_dojo.CyclerParams([D, D, D, D, D, C, C, C, C, C] * 20))

    # Random Filler
    while len(pop) < pop_size:
        random_moves = list(map(axl.Action, np.random.randint(0, 1 + 1, (SEQUENCE_LENGTH, 1))))
        pop.append(axl_dojo.CyclerParams(random_moves))

    return pop


class NewAnalysisRun:
    # options
    opponent_list = []
    output_files = {}
    save_directory = "output/"
    save_prefix = ""
    save_suffix = ""
    global_seed = 0
    overwrite_files = True

    @staticmethod
    def _get_seeded_player_class(player_class):
        class NewClass(player_class):
            def __init__(self, seed=0):
                my_seed = seed  # for pickling
                axl.seed(my_seed)
                super().__init__()

        return NewClass


    def _get_file_name(self, opponent: axl.Player):
        return self.save_directory \
               + self.save_prefix \
               + str(opponent).replace(" ", "_").replace(":", "@").replace("\\", "(") \
               + self.save_suffix \
               + ".csv"

    def add_opponent(self, opponent: axl.Player):
        self.opponent_list.append(opponent)

    def clear_opponent_list(self):
        self.opponent_list = []

    def set_opponent_list(self, new_list: list):
        self.opponent_list = []
        self.opponent_list = new_list

    def set_save_directory(self, new_directory: str):
        self.save_directory = new_directory.split("/")[0] + "/"

    def set_save_prefix(self, new_prefix: str):
        self.save_prefix = new_prefix

    def set_save_suffix(self, new_suffix: str):
        self.save_suffix = new_suffix

    def set_global_seed(self, new_seed: int):
        self.global_seed = new_seed

    def set_file_overwrite_true(self):
        self.overwrite_files = True

    def set_file_overwrite_false(self):
        self.overwrite_files = False

    def start(self):
        print("-------- SETTINGS --------")
        print("SEQUENCE_LENGTH:", SEQUENCE_LENGTH)
        print("POPULATION_SIZE:", POPULATION_SIZE)
        print("GENERATION_LENGTH:", GENERATION_LENGTH)
        print("MUTATION_FREQUENCY:", MUTATION_FREQUENCY)
        print("MUTATION_POTENCY:", MUTATION_POTENCY)
        print()
        print("Save directory is ", "\'" + self.save_directory + "\'")
        print("Global seed is set to", self.global_seed)
        if self.save_prefix == "":
            print("No file prefix was given")
        if self.save_suffix == "":
            print("No file suffix was given")
        print("--------------------------")
        print()
        print("There are", len(self.opponent_list), "opponents to analyse")

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        if self.overwrite_files:
            print("overwriting files before running calculations.")
            for opponent in self.opponent_list:
                opponent_file = self._get_file_name(opponent)
                try:
                    os.remove(opponent_file)
                    print("removed file: " + opponent_file)
                except FileNotFoundError:
                    print("could not remove file: " + opponent_file + " no file found.")
            print("removed all files. \n")

        cycler_objective = axl_dojo.prepare_objective(name="score", turns=20, repetitions=1)
        cycler_kwargs = {
            "sequence_length": SEQUENCE_LENGTH,
            "mutation_probability": MUTATION_FREQUENCY,
            "mutation_potency": MUTATION_POTENCY
        }

        i = 1
        print("Starting analysis...")
        print()
        for opponent in self.opponent_list:
            print(i, "of", len(self.opponent_list), "| Analysing player:", str(opponent), "...")

            global_processes = 20

            # Stochastic players need seeding
            if opponent.classifier['stochastic']:
                opponent = self._get_seeded_player_class(type(opponent))(self.global_seed)
                global_processes = 1


            population = axl_dojo.Population(params_class=axl_dojo.CyclerParams,
                                             params_kwargs=cycler_kwargs,
                                             size=POPULATION_SIZE,
                                             processes=global_processes,
                                             population=getPreMadePop(POPULATION_SIZE),
                                             objective=cycler_objective,
                                             output_filename=self._get_file_name(opponent),
                                             opponents=[opponent],
                                             print_output=False)

            population.run(GENERATION_LENGTH)
            print("{:.2f}% Done.\tSaved to:".format((100 * i) / len(self.opponent_list)),
                  self._get_file_name(opponent))
            self.output_files[str(opponent)] = self._get_file_name(opponent)
            i += 1


if __name__ == "__main__":
    run_one = NewAnalysisRun()
    run_one.set_save_prefix("FINAL-")
    # run_one.set_file_overwrite_false()

    run_one.add_opponent(axl.ZDExtort2())
    # run_one.add_opponent(axl.TitForTat())
    run_one.add_opponent(axl.Adaptive())

    # Stochastic opponents must be run in a separate non pickled instance.
    # run_one.set_opponent_list([x() for x in axl.all_strategies if x.classifier['stochastic']])
    # run_one.set_opponent_list([x() for x in axl.all_strategies])

    # run_one.set_opponent_list([x() for x in axl.all_strategies if not x.classifier['stochastic']])

    run_one.start()
