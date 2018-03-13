from code import full_analysis as fa


import axelrod as axl

run = fa.NewAnalysisRun(mutation_frequency=0.33)
run.save_file_prefix = "example-"

run.add_opponent(axl.TitForTat())
run.add_opponent(axl.Random())
run.add_opponent(axl.Grudger())

run.start()
