# Generalised connect four engine
This program includes an interactive environment from which all the different search algorithms can be used on top of various other interesting features. I also wrote a [paper](docs/paper.pdf) explaining how everything works.

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
0 1 2 3 4 5 6

X > ?

[0-n): make move
u undo: undo last move
ab alphabeta [d t]: make alphabeta move
nx negamax [d t]: make negamax move
in insane [d t]: make insane move
r random [n]: make n random moves
h heuristic: choose heuristic
n new [w h n]: new game
l load seq: load game
a automove: toggle automove
m mirror: mirror the board
sl shiftl: shift the board left
sr shiftr: shift the board right
c count: print movecount
p print: print board
q quit: quit the maker
? help: show this help

X > ...
```
