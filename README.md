# Shotest-Path Finding Algorithm Visualization


This project is a visualization of the A* Path Finding Algorithm using Pygame. It allows users to set start and end points, create barriers, and observe the pathfinding process in real-time.

## Features

- **Interactive Grid**: Click to set start, end, and barrier points.
- **Visualization**: Watch the A* algorithm in action as it finds the shortest path.
- **Reset Functionality**: Clear the grid and start over at any time.

## Requirements

- Python 3.x
- Pygame

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/astar-pathfinding.git
    ```

2. **Navigate to the project directory**:
    ```sh
    cd astar-pathfinding
    ```

3. **Install Pygame**:
    ```sh
    pip install pygame
    ```

## Usage

1. **Run the script**:
    ```sh
    python astar.py
    ```

2. **Interact with the grid**:
    - **Left Click**:
        - Set the start point (orange).
        - Set the end point (turquoise).
        - Create barriers (black).
    - **Right Click**:
        - Remove the start point, end point, or barriers.
    - **Press SPACE**: Start the algorithm.
    - **Press C**: Clear the grid.

## How It Works

The A* algorithm uses a priority queue to explore nodes. It calculates the cost of each node using the formula `f(n) = g(n) + h(n)`, where:
- `g(n)` is the cost from the start node to the current node.
- `h(n)` is the heuristic cost estimate from the current node to the end node.

The algorithm continues to explore nodes until it finds the shortest path from the start to the end point.

## File Structure

- `astar.py`: The main script containing the implementation of the A* algorithm and the Pygame visualization.
- `README.md`: This readme file.

## Contributing

1. Fork the repository.
2. Create your feature branch:
    ```sh
    git checkout -b feature/AmazingFeature
    ```
3. Commit your changes:
    ```sh
    git commit -m 'Add some AmazingFeature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/AmazingFeature
    ```
5. Open a pull request.

## License

Distributed under the MIT License. See
