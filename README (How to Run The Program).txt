A few notes about the use of the code:

The main function is in ludo_game.py, so it may be necessary to run the program through there depending on your development environment.

To have the agents play a game, simply click anywhere in the green space to the right of the board, and watch them go!

There is code for having a series of games played, but there is drastic slowdown that comes from reloading the Tkinter window, so that behavior has been shut off. If you wish to play multiple games, it is recommended to simply restart the program with each game.

The Q table that was created from the learning phase is excluded, as its size was 22 GB and did not fit on the upload for eLC. However, the policy file is included, and since learning is toggled off, the rational agents will simply act based on the policy.

The current settings have it so that there are 2 random players (red and blue) and 2 rational players (green and yellow). If you search for "randoms = 2" in ludo_game.py and change that to any number from 0 to 4, you can choose the number of random players, and the rational players will be (4 - random players). Additionally, the assignment of the random players goes counterclockwise from red, and then the rational players go counterclockwise from there (thus red to blue, and then green to yellow).

If the code seems hard to follow, it was built off of someone else's simulator, which did cause us a lot of grief. Maybe we should have made our own like the team that implemented Pacman!