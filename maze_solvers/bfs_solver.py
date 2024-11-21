from utils.maze import Maze
from utils.cell import Cell
from collections import deque
from maze_solvers.base_solver import BaseSolver


class BfsSolver(BaseSolver):
    """Класс поиска пути методом обхода в ширину (BFS)"""

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.solver_name = "BFS"
        self.visited: set = set()
        self.path: list[Cell] = []

    def find_path(self) -> None:
        queue = deque([self.maze.start_point])
        self.visited.add((self.maze.start_point.i, self.maze.start_point.j))
        self.parent[(self.maze.start_point.i, self.maze.start_point.j)] = None

        while queue:
            current_cell = queue.popleft()
            if current_cell == self.maze.finish_point:
                self._restore_path()
                break
            # добавляем в очередь обхода не посещенных соседей текущей ячейки, в которых можно попасть
            for neighbor in self.maze.get_neighbors(current_cell):
                if (
                    neighbor.i,
                    neighbor.j,
                ) not in self.visited:
                    queue.append(neighbor)
                    self.visited.add((neighbor.i, neighbor.j))
                    self.parent[(neighbor.i, neighbor.j)] = current_cell
        self.maze.paths_dict[self.solver_name] = self.path
        return None

    def _restore_path(self) -> None:
        """По родителям восстанавливает путь от конечной точки до начальной"""
        current = self.maze.finish_point
        while current:
            self.path.append(current)
            current = self.parent[(current.i, current.j)]
        self.path.reverse()
        return None
