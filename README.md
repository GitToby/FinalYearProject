# FinalYearProject

~~This is the edit for github to make Vince happy.~~ <br>
This is the edit for github to make Toby happy in the future.
 
Things I've done so far:
- Read a bunch of stuff
    - the articles ~~below~~ in the issues section.
    - ch.1 and ch.2 of the book *The Complexity of Cooperation*
    - bits of documentation
- Learned the multi version can be modeled as a group of people eating 
- Worked through some examples (see scratch code file)
- Looked into the Dojo and pulled it down as a dev package for editing
- Learned archetype is spelled like arc-he-type

## Definitions
* ___Game___ - A sequence of moves between 2 players that has a winner at the end (len(game) describes the length of 
a game)
* ___Round___ - ??a pair of moves for 2 player in a game??
* ___C___ - Cooperation move for a single player
* ___D___ - Defect move for a single player
* ___Sequence___ - result of two or more moves, written as: [CCDCCD]
* ___Strategy___ - A named way of playing a game. e.g. Cooperator() : will alway play C


## Main problem
Here I will look into the problem that I have been asked to solve.
#### Problem:
*Given a certain opponent, O, (with a provided strategy, S) what is the best possible sequence of moves, in a game of n 
turns, made by my strategy to maximise my players score?*

Examples of solutions include:

Opponent  | Sequence
----------|---------
Cooperator| [DDDDDDDD...]
Defector  | [DDDDDDDD...]
TitForTat | [CCCCCCCC...]


How do we generate this sequence for each opponent?  we will use a sequence Archetype:

>The sequence archetype will use the |X Something X| player for our strategy each time, only editing the 
 input to improve our score. To this model we can apply an optimised input of length n (tbd) to the player, this 
 sequence, as per the design of the strategy will then be repeated until the games end(if n = len(game) then we are
 just calculating the sequence for the whole game). 
>
>The input sequence itself will be created using a genetic optimisation. Starting with a set of randomly generated 
 sequences, we will have each one play the opponent and return with a score. These sequences will be ranked and the 
 lowest x% will be discarded, resulting in a fitter, but smaller, population than before. This smaller population will
 then create offspring using a |X TBD method X| pairing algorithm before mutating with |X TBD method X|. This new set
 of offspring will be included in the next scoring round and the process repeats for k number of rounds
>
>This sequence of Play-Rank-Create-LOOP will be the basis of creating the optimal strategy for each other opponent. 
