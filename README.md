# Artificial-Intelligence


Note: This project is coded in Python Version 2.7 IDLE. It is designed to only be run in this version. 
If unable to run code, please use the link: https://www.python.org/downloads/release/python-2716/ to download version 2.7.16 IDLE.

This code is designed to imitate the given assignment below.

Created by: Oleg Nochvay

==================================================

The Wumpus world 
Consider the agent and its environment in the Wumpus world. The environment in the Wumpus world consists of a rectangle cave size M x N, built up of square cells (M x N number of cells.) The objects in the environment are: a wumpus, a pile of gold, and a number of pits. Each cell may contain either the wumpus, or the gold, or a pit. The rules of the game are: 

		  Initially the agent is in the top left cell with coordinates [0][0]. This cell does not contain any objects of the environment.  
		
		  The agent moves through the cells with the purpose to find the gold. From a given cell the agent can move North, South, East, or West, provided that it stays within the cave. We assume that the agent knows the dimensions of the cave.  
		
		  The agent has a weapon and can shoot from its current position North, South, East or West.  
		
		  In each cell the agent receives percepts described below. Breeze: if there is a pit in at least one of the surrounding cells Stench: if the wumpus is in one of the surrounding cells Glitter: if the cell contains the pile of gold Scream: if agent's previous action was shooting and the wumpus is dead.  
		
		  The agent dies if it enters a cell with the wumpus or a pit.  
		
		  If the agent enters the cell containing the gold, it picks up the gold and exits (in a  sequence of moves) the cave.  The agent chooses its action based on the percepts received from the environment. Assume that the wumpus does not move. This is a simplified version of the problem as described in AIMA textbook. 
		
		 Part 1. The Environment  
		 
	1.	Design the representation of the environment. Decide on how the agent and the environment objects will be represented. Describe the representation. Give an example.  
	
	2.	Design the representations of the percepts. In what form the environment will send the percepts to the agent? Note that there may be more than one percept at a given step.  
	
	3.	Design and imple me nt the environme nt class. The class will have a method that receives the coordinates of the agent and returns the percepts.  
	
	4.	Design a main method, that will test how the environment returns the percepts. It should get the coordinates form the user, and report the percepts  
	
	a) In the internal representation 

	b) In a user-friendly representation. Make the program run multiple times, so that you can make several tests. 
	CMSC 310 Artificial Intelligence 
	1 
	While working on this project, you will have to make various choices (for example, would the percepts be represented as a list, by an array, by a single variable with different values, by a set of variables?). Please record the choices that you have considered for each task above, your thoughts about each choice and why you made a particular choice. 

	Part 2. The Agent 
		A.	Core Version – stationary wumpus, the agent does not possess a weapon. 
	
	1.	Design the agent class. What would be the agent representation?  What are the available actions of the agent? How would the agent choose an action? How would the action be reported to the Environment?  
	2.	Implement a safe agent – the agent does not take chances. If the agent cannot find a path to the gold, it gives up.  
	3.	Design and implement an algorithm for finding an exit path that skips the cells where the agent had to backtrack.  
	4.	Print the solution as a sequence of cave configurations accompanied with the corresponding move of the agent, e.g.  
	B.	Start a..p.pw ..p..g. ....... ....... Move down ...p.pw a.p..g. ....... .......  
	C.	Improveme nts a. Randomly generated cave  b. Make the wumpus move  
	
	c. Arm the agent. 
====================================================+
