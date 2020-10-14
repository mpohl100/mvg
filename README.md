# Goal
The goal of this project is to create an algorithm which can automatically deduce a driving schedule for public transportation networks by examining the topology of the network.
This algorithm is meant to be used by railway networks for transporting humans or economic goods. Furthermore the algorithm can be used by self driving car networks in big cities to plan how many cars shall be used to transport a certain number of people.
The algorithm is still under construction but it already works well for the local Munich subway network. 
Further ideas are needed and any help is appreciated.

# Usage
The prototype is written in python3 and requires the libraries networkx and tkinter to work properly.
You can run the software by running the following command in the folder mvg:

python3 mvg_sim.py -f data/MUC_SBahn.json data/MUC_UBahn.json
    -v 1:   will print out the delays of all the trains after 1440 minutes of simulating the network. Also the stations where most of the delay was created will be displayed.
    -d yes: the schedule of the trains of the network will be deduced by examining the topology of the network.
    -s yes: the driving of the trains will be shown in a network animation
    -p 5: every possible route in the network will be travelled by 5 people. The average travel and waiting times of the people will be printed at the end of the simulation.

