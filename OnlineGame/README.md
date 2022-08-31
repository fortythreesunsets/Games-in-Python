# ONLINE ROCK, PAPER, SCISSORS
Made in Python using Pygame following [this tutorial](https://youtu.be/_fx7FQ3SP0U) by Tech with Tim

Each player has to chose simultaneously rock, paper or scissors 

* Rock breaks scissors
* Paper covers rock
* Scissors cuts paper

If both players choose the same shape, the game is tied and is usually immediately replayed to break the tie.

## Instructions
1. Change `server = "192.168.0.00"` on server.py. Get the IPv4 address from cmd -> ipconfig (server.py has to be running in the machine that has this IP)
2. Run server.py (In PyCharm: Run > Edit configuration > change the configuration to server to run this script)
3. Change `self.server = "192.168.0.00"` in network.py to the same ip address in server.py
4. Run network.py (In PyCharm: Run > Edit configuration > change the configuration to network to run this script)
5. Run client.py (In PyCharm: Run > Edit configuration > change the configuration to client to run this script)
6. To have 2 client windows at the same time: Run > Edit Configurations and make sure "Allow Parallel Run" is checked
