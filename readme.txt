-------------------------------------------------------------------------------------------------------------
Game Playing Algorithms Assignment : Connect4
-------------------------------------------------------------------------------------------------------------
Name: Prakhar Shankar Sapre
-------------------------------------------------------------------------------------------------------------
UTA Id: XXXXXXXXXX
-------------------------------------------------------------------------------------------------------------

LANUGUAGE : Python

-------------------------------------------------------------------------------------------------------------
INTRODUCTION :

As part of the assignment I have implemented a game playing algorithm using minimax, alpha beta pruning and depth
limited minimax for prediciting the next best possible move in connect4 game.

This game runs in two modes : Interactive Mode and One-Move Mode.

-------------------------------------------------------------------------------------------------------------
STRUCTURE OF THE CODE :

The game uses two python files called maxconnect4.py and MaxConnect4Game.py.
maxconnect4.py file has functions to perform basic operations like taking user inputs and set up the gameboard and
call the AI algorithm to predict next moves.

MaxConnect4Game.py file has the function to perform the AI algorithms and also calculate the evaluation function.

The algorithm is implemented in the function aiPlay() and it uses minimax with alpha-beta pruning.
---------------------------------------------------------------------------------------------------------------
GAME MODES :

Interactive Mode :

$python maxconnect4.py interactive input.txt computer-next/human-next depth.

This mode will be an interactive mode between the human and the computer wherein the human can play his move and the 
computer will predict its move based on the algorithm implemented and finally give us the result as to who won and
who lost.

One-move Mode Syntax :

$python maxconnect4.py one-move input_file output_file depth.
In this mode the computer will predict the next best possible move and make the move given an input state.
------------------------------------------------------------------------------------------------------------------
EVALUATION FUNCTION :

We have implmented a evaluation function for depth limited minimax in order to calculate the utility value which will be used by the 
algorithm to determine the next best possible move.
The computer will choose the highest utlity value it finds while calculating and it will choose the corresponding column to play its
next move.
Firstly it will check if it can get consecutive fours, then threes and lastly twos.
Here we calculate the number of possible fours, threes and twos that the human can make and subtract them from the opponent.

utility_value = (my_fours * 10 + my_threes * 5 + my_twos * 2)- (comp_fours *10 + comp_threes * 5 + comp_twos * 2).
Once the utility values are calculated, the column which has the highest corresponding value is choosen and then the move is played.
---------------------------------------------------------------------------------------------------------------------
DEPTH VS RUNTIME :

DepthVsRuntime excel sheet has the depth and corresponding runtime values. 
Runtime is calculated for the corresponding depth till time reaches 1 minute.

I found that after depth limit 10 the runtime goes beyond 1 minute.
-------------------------------------------------------------------------------------------------------------------