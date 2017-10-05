import pprint as pp

import axelrod as axl

# build players into a tuple (make sure you're constructing the players correctly)
players = (axl.APavlov2011(), axl.AntiCycler())
print("basic players:")
print(players)

# build a match using the Match class; include the number of rounds and the players you've created
match = axl.Match(players=players, turns=50)

# play the match with the .play() method, printing out the result
match.play()

# recall the results of the match using the match.results attribute
print("basic match results")
print(match.result)

# other ways of visualising the match are sparklines; two rows are shown for the two players:
print("sparklines display:")
print(match.sparklines())
# or
print(match.sparklines(c_symbol="X", d_symbol=" "))

# the're are a bunch more interesting scores to see:
print("other values to look into")
print("final score: " + str(match.final_score()))  # this prints the score (sum of game position history)
print("winner: " + str(match.winner()))
# print(match...))


# we can move on to creating tournaments if we need to:
players2 = list()
players2.append(axl.Alternator())
players2.append(axl.EvolvedFSM4())
players2.append(axl.Darwin())
players2.append(axl.Prober())

print()
print("---TOURNAMENT---")
print("players:")
print(players2)

torn = axl.Tournament(players2)

# Playing the tournament leaves us with a outcome result:
outcome = torn.play()
summary = outcome.summarise()

# we can then see the players ranks:
print("tournament winners:")
print(outcome.ranked_names)

# we can even plot results:
plot = axl.Plot(outcome)
plot.boxplot().show()

# using pretty print we can display nicer results
print("pprint examples")
pp.pprint(summary)
