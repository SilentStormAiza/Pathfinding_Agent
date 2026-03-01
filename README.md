# Pathfinding_Agent
Let the Agent Lost in ways!..<br/>
An interactive pathfinding visualization tool that implements Greedy Best-First Search (GBFS) and A* search algorithms with dynamic obstacle handling. Built with Python and Pygame.<br/>

**Features:** <br/>
**Environment:**
- Dynamic Grid Sizing: Configurable grid dimensions (5x5 to 20x20)
- Fixed Start & Goal: Clearly marked start (green) and goal (red) positions
- Random Map Generation: Generate mazes with user-defined obstacle density
- Interactive Map Editor: Three editing modes (Wall/Start/Goal) with simple click-based interface
**Algorithms**
- Greedy Best-First Search (GBFS): Uses only heuristic evaluation f(n) = h(n)
- *A Search: Uses combined evaluation f(n) = g(n) + h(n)
Heuristic Functions:
- Manhattan Distance (4-directional movement)
- Euclidean Distance (diagonal movement)
**Dynamic Mode**
  - Random obstacle spawning during agent transit
- Real-time path detection and replanning
- Efficient recalculation only when path is blocked
**Visualization**
- Frontier Nodes: Highlighted in orange
- Visited Nodes: Highlighted in light blue
- Final Path: Highlighted in yellow
- Start/Goal: Green and red respectively

Real-time Metrics Dashboard
- Nodes Visited
- Path Cost
- Execution Time (ms)
- Current Density setting
- Active algorithm and heuristic

**Installation**<br/>
Prerequisites
- Python 3.6 or higher
- pip package manager

Install required packages<br/>
- pip install pygame numpy
Run the application: python pathfinding_agent.py <br/><br/>

**How to Use**
Initial Setup:
When prompted, enter grid size (5-20)
The application window will open with a 6x6 grid (or your chosen size)

**Controls**
- Mode Selection (Click Buttons)
- Wall Mode: Click on grid cells to toggle walls (gray)
- Start Mode: Click on empty cell to set start position (green)
- Goal Mode: Click on empty cell to set goal position (red)

**Algorithm Selection**
- A* button: Switch to A* search
- GBFS button: Switch to Greedy Best-First Search

**Heuristic Selection**
- Manhattan button: Use Manhattan distance
- Euclidean button: Use Euclidean distance

**Actions**
- Random button: Generate random walls with current density
- Clear button: Clear entire grid
- Find Path button: Find path using selected algorithm
- Dynamic button: Toggle dynamic mode (agent moves automatically)

**Workflow Example:**
- Click Start Mode, then click a cell to set start (green)
- Click Goal Mode, then click another cell to set goal (red)
- Click Wall Mode to add some obstacles
- Click Find Path to see the path
- Click Dynamic to watch the agent navigate with random obstacles
