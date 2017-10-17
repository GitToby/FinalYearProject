# This is a scratch file with sections of code that could be considered useful but are not part of a build.

import itertools
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
tornPlayers = list()
tornPlayers.append(axl.Alternator())
tornPlayers.append(axl.EvolvedFSM4())
tornPlayers.append(axl.Darwin())
tornPlayers.append(axl.Prober())

print()
print("---TOURNAMENT---")
print("players:")
print(tornPlayers)

torn = axl.Tournament(tornPlayers)

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

tornPlayers2 = [axl.GradualKiller(),
                axl.Alternator(),
                axl.TrickyDefector(),
                axl.Appeaser(),
                axl.TitForTat()]

torn2 = axl.Tournament(tornPlayers2, turns=3, repetitions=1)
outcome2 = torn2.play(keep_interactions=True)

pp.pprint(outcome2.summarise())


def printList(L):
    for x in L:
        print(x)


printList(itertools.product(["x", "y"], "ab"))

int(2.5)

x = 165040491235


def isBetween(bottom, top, n):
    print("looking between: ", bottom, " & ", top, "| step: ", n)
    loops = 0
    for j in range(bottom, top, n):
        if j >= x:
            print("found ", j, ">=x     | loops:", loops)
            return j
        loops = loops + 1
    print("k not found")


n1 = 100000
n2 = 100
n3 = 1
a = isBetween(1, 20000000000000, n1)
b = isBetween(a - n1, a, n2)
c = isBetween(b - n2, b, n3)

for i in range(1, 200000000000):
    if i == x:
        print("found ", i, "==x")
