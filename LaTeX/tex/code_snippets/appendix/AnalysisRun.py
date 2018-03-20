class NewAnalysisRun:
    # default options
    opponent_list = []
    output_files = {}
    save_directory = "output/"
    save_file_prefix = ""
    save_file_suffix = ""
    global_seed = 0
    overwrite_files = True
    stochastic_seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, sequence_length=20,
                 population_size=25,
                 generation_length=20,
                 mutation_frequency=0.1,
                 mutation_potency=1):
        self.sequence_length = sequence_length
        self.population_size = population_size
        self.generation_length = generation_length
        self.mutation_frequency = mutation_frequency
        self.mutation_potency = mutation_potency

    def get_pre_made_pop(self, pop_size: int):
        pop = []

        # Totalities & Handshakes
        handshake_leng = 5
        for start in itertools.product("CD", repeat=handshake_leng):
            pop.append(axl_dojo.CyclerParams(
                list(start) + [C] * (200 - handshake_leng)))
            pop.append(axl_dojo.CyclerParams(
                list(start) + [D] * (200 - handshake_leng)))

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
                pop.append(axl_dojo.CyclerParams(
                    [C] * i + [D] * (200 - (i + j)) + [C] * j))
                pop.append(axl_dojo.CyclerParams(
                    [D] * i + [C] * (200 - (i + j)) + [D] * j))

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
            random_moves = list(map(axl.Action, np.random.randint(
                0, 1 + 1, (self.sequence_length, 1))))
            pop.append(axl_dojo.CyclerParams(random_moves))

        return pop

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
            + self.save_file_prefix \
            + str(opponent).replace(" ", "_").replace(":", "@").replace("\\", "(") \
            + self.save_file_suffix \
            + ".csv"

    def add_opponent(self, opponent: axl.Player):
        # Stochastic players need re-seeding
        if opponent.classifier['stochastic']:
            for seed in self.stochastic_seeds:
                self.opponent_list.append(
                    self._get_seeded_player_class(type(opponent))(seed))
        # Otherwise its fine to just add them
        else:
            self.opponent_list.append(opponent)

    def clear_opponent_list(self):
        self.opponent_list = []

    def set_opponent_list(self, new_list: list):
        self.opponent_list = list()
        self.opponent_list = new_list

    def set_save_directory(self, new_directory: str):
        if new_directory[0] == "/":
            new_directory = new_directory[1:]

        self.save_directory = new_directory.split("/")[0] + "/"

    def start(self):
        print("-------- RUNNING ANALYSIS --------")
        print("SEQUENCE_LENGTH:", self.sequence_length)
        print("POPULATION_SIZE:", self.population_size)
        print("GENERATION_LENGTH:", self.generation_length)
        print("MUTATION_FREQUENCY:", self.mutation_frequency)
        print("MUTATION_POTENCY:", self.mutation_potency)
        print()
        print("Save directory is ", "\'" + self.save_directory + "\'")
        print("Global seed is set to", self.global_seed)
        if self.save_file_prefix == "":
            print("No file prefix was given")
        if self.save_file_suffix == "":
            print("No file suffix was given")
        print("--------------------------")
        print()
        print("There are", len(self.opponent_list), "opponents to analyse")

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        if self.overwrite_files:
            print("Overwriting files during run")

        cycler_objective = axl_dojo.prepare_objective(
            name="score", turns=self.sequence_length, repetitions=1)
        cycler_kwargs = {
            "sequence_length": self.sequence_length,
            "mutation_probability": self.mutation_frequency,
            "mutation_potency": self.mutation_potency
        }

        i = 1
        print("Starting analysis...")
        print()
        for opponent in self.opponent_list:
            print(i, "of", len(self.opponent_list),
                  "| Analysing player:", str(opponent), "...")

            if self.overwrite_files:
                opponent_file = self._get_file_name(opponent)
                try:
                    os.remove(opponent_file)
                    print("\tremoved file: " + opponent_file)
                except FileNotFoundError:
                    print("\tcould not remove file: " + opponent_file)

            population = axl_dojo.Population(params_class=axl_dojo.CyclerParams,
                                             params_kwargs=cycler_kwargs,
                                             size=self.population_size,
                                             processes=1,
                                             population=self.get_pre_made_pop(
                                                 self.population_size),
                                             objective=cycler_objective,
                                             output_filename=self._get_file_name(
                                                 opponent),
                                             opponents=[opponent])

            population.run(self.generation_length, print_output=False)
            print("{:.2f}% Done.\tSaved to:".format((100 * i) / len(self.opponent_list)),
                  self._get_file_name(opponent))
            self.output_files[str(opponent)] = self._get_file_name(opponent)
            i += 1
