players = [axl.DefectorHunter(), axl.SolutionB1(), 
            axl.Willing(), axl.TrickyDefector(), 
            axl.Cycler("C"+"D"*199)]
tournament = axl.Tournament(players,turns=200)
results = tournament.play()

>>> Index, Rank, Name,            Median score, Coop rating, Wins
>>> 0,     0,    Cycler: C1,199,  4.9625,       0.005,       4.0 
>>> 1,     1,    Tricky Defector, 2.23625,      0.2475,      1.5 
>>> 2,     2,    SolutionB1,      1.7675,       0.71775,     2.0 
>>> 3,     3,    Defector Hunter, 1.508125,     0.995,       0.0 
>>> 4,     4,    Willing,         1.5,          0.849,       0.5 

