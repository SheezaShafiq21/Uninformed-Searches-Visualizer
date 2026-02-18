# Uninformed-Searches-Visualizer
Uninformed Search Visualizer (Pygame)

An interactive visualization tool built with Python and Pygame to demonstrate classic Uninformed Search Algorithms in Artificial Intelligence.
This project visually shows how different search algorithms explore a grid to find a path from a Start node to a Target node, while avoiding obstacles.

-> Features
20x20 Grid Visualization
Color-coded search states
Step-by-step animated exploration
Strict movement order
Multiple uninformed search algorithms

-> Implemented Algorithms
Key	Algorithm
1	Breadth-First Search (BFS)
2	Depth-First Search (DFS)
3	Uniform Cost Search (UCS)
4	Depth-Limited Search (DLS)
5	Iterative Deepening DFS (IDDFS)
6	Bidirectional Search

->Color Legend
Color	Meaning
.Green	Start Node
. Blue	Target Node
. Red	Wall / Obstacle
. Yellow	Frontier (Open List)
. Gray	Explored Nodes
. Purple	Final Path
. Movement Order (Strict Priority)

The algorithms expand nodes in this exact order:
Up
Right
Bottom
Bottom-Right (Diagonal)
Left
Top-Left (Diagonal)

-> Requirements

Python 3.x
Pygame
Install pygame using:
pip install pygame

->How to Run

Clone the repository:
git clone https://github.com/your-username/uninformed-search-visualizer.git

Navigate to the project folder:
cd uninformed-search-visualizer

Run the program:
python main.py

-> Controls
After running the program, press:
1 → BFS
2 → DFS
3 → UCS
4 → DLS (limit = 15)
5 → IDDFS
6 → Bidirectional Search
Close the window to exit.

-> Educational Purpose
This project is designed for:
Artificial Intelligence courses
Understanding search strategies
Comparing time and space behavior
Visual learning of graph traversal

It clearly demonstrates:

Frontier expansion
Explored nodes
Path reconstruction
Algorithm behavior differences

-> Example Output

Gray cells show explored nodes
Yellow cells show frontier
Purple path shows the final solution
