

You are an RTS game designer. Here is the game you need to make.

microRTS is a minimalist real-time strategy (RTS) game designed primarily for AI research. It distills core RTS mechanics into a simple framework. Here's a breakdown of its rules:

# Game Objective:
The primary goal in microRTS is to destroy all enemy units and buildings. If neither player achieves this within a fixed number of game ticks, the game ends in a draw.

This is a single player game. You do not have to consider multiplayer or local cooperative. Just consider single player with an AI player.

## Gameplay Fundamentals:

- Real-Time, Simultaneous Turns: Unlike turn-based games, microRTS operates in real-time. Both players issue commands simultaneously, and actions unfold continuously over "game ticks."
- Grid-Based Map: The game is played on a discrete grid, which typically contains resource patches.
- Resources: Resources are essential for building and training units. Workers are the only units capable of gathering them.
- Buildings:
    - Bases: Produce worker units and store collected resources.
    - Barracks: Train military units.

- Units: There are four main types of units:
    - Workers: Weak in combat, but crucial for gathering resources and constructing buildings.
    - Light Units: A type of military unit.
    - Ranged Units: Military units capable of attacking from a distance.
    - Heavy Units: Another type of military unit, generally stronger than light units.
- Combat: Units generally need to be on an adjacent square to an enemy unit or building to attack, with the exception of ranged units. Unit damage can be deterministic or non-deterministic (randomly drawn within a range), depending on the game configuration.


## Key Mechanics:

- Unit Production: Players decide which units to produce, balancing resource constraints with strategic needs (e.g., countering the opponent's army).
- Movement: Units can be commanded to move across the grid.
- Harvesting: Workers can be sent to resource patches to gather resources.
- Returning Resources: Workers return gathered resources to a base.
- Attacking: Units can be commanded to attack enemy units or buildings.

## Winning and Losing:

- Win Condition: Destroy all of the opponent's units and buildings.
- Lose Condition: All of the player's units and buildings are destroyed.

The following are the user's requirements. If there are any conflicts between the user's requirements and the aforementioned requirements, the user's requirements shall take precedence. Please generate a Game Design Document and a Web Game Design Document.

{instruction}