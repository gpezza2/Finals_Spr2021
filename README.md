# Battleships
My final project was a variation of battleships using the Salvo ruleset. Major variation is in the shape of the ships.
Typical Battleships ships are simple straight lines making it easy to track shots resulting in a sink.

The ships in this variation include odd shapes with holes in the middle and offset lines.

The AI in this implementation is rather naive and simply tracks existing hits and uses them to base subsequent shots.

##Algorithmic analysis of AI
The main section that constituted the AI for the game is the "choose_sector" function. This function is what the AI uses to determine where it will be firing.

At the very top of the function is a process that updates the queue of registered hits to remove any points that have been "cleared" meaning all squares around it have been fired at.
If we assume _m_ to be the number of hits that have been registered at a certain point, we could expect that process to be _O(m)_ as the for loop simply iterates through all points in the queue.


The first part of the function simply chooses a point at random from a matrix (list of lists).
assuming _n_ is equal to height * width and assuming the time complexity of random.choice is at worst _O(n)_ (source: https://stackoverflow.com/questions/40143157/big-o-complexity-of-random-choicelist-in-python3)

The next part looks at a queue of registered hits and uses that as a starting point and fires at all coordinates around that point. Since the game is turn-based, only one statement will be executed per shot.
These statements should all be _O(1)_ as they are only assignment operations and comparisons.

As such the linear operations are the ones we would focus and we see we can expect a _O(n+m)_ for the choose_sector function.

