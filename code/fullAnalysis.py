import axelrod as axl
import axelrod_dojo as axl_dojo


class AnalysisRun:
    # options
    opponent_list = []
    print_level = ""
    save_prefix = ""
    save_suffix = ""
    global_seed = 0

    def get_seeded_player_class(self, player_class):
        class NewClass(player_class):
            def __init__(self, seed=0):
                axl.seed(seed)
                super().__init__()

        return NewClass

    def get_file_name(self, opponent):
        return self.save_prefix + str(opponent) + self.save_suffix

    def run(self):
        cycler_objective = axl_dojo.prepare_objective(name="score", turns=20, repetitions=1)
        cycler_kwargs = {
            "sequence_length": 200,
            "mutation_probability": 0.1,
            "mutation_potency": 1
        }

        for opponent in self.opponent_list:
            seeded_opponent = self.get_seeded_player_class(type(opponent))(self.global_seed)

            population = axl_dojo.Population(params_class=axl_dojo.CyclerParams,
                                             params_kwargs=cycler_kwargs,
                                             size=200,
                                             objective=cycler_objective,
                                             output_filename=self.get_file_name(opponent),
                                             opponents=[seeded_opponent])


if __name__ == "__main__":
    run = AnalysisRun()
