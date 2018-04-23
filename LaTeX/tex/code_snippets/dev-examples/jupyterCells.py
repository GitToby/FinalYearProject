
# -------- CELL 1 --------
# The ! means 'run this as a bash script' 
! pip install axelrod
! pip install axelrod-dojo
! wget https://raw.githubusercontent.com/GitToby/FinalYearProject/master/code/full_analysis.py

# -------- CELL 2 --------
import axelrod as axl
import full_analysis as fa

run = fa.NewAnalysisRun(population_size=40)

run.add_opponent(axl.TitForTat())
run.add_opponent(axl.Random())
run.add_opponent(axl.Grudger())

run.start()