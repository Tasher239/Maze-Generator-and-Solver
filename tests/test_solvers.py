import unittest

from maze_solvers.dfs_solver import DfsSolver
from utils.maze import Maze
from utils.cell import Cell
from maze_solvers.bfs_solver import BfsSolver
from maze_solvers.ford_bellman_solver import FordBellmanSolver


class TestPathfindingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.good_surface = False
        self.bad_surface = False
        self.width = 5
        self.height = 5
        self.start_point = Cell(0, 0, 0)
        self.finish_point = Cell(4, 4, 0)

    def get_maze_all_surface(self):
        for good_surface in [False, True]:
            for bad_surface in [False, True]:
                maze = Maze(
                    self.width,
                    self.height,
                    good_surface,
                    bad_surface,
                    self.start_point,
                    self.finish_point,
                )
                """ Вырезаем лабиринт
                       ╔═══════╦═══════════╗
                       ║ A     ║           ║
                       ╠════   ║   ╔════   ║
                       ║       ║   ║       ║
                       ║   ║   ║   ╚═══╗   ║
                       ║   ║           ║   ║
                       ╠═══╝   ╔════   ║   ║
                       ║       ║           ║
                       ║   ║   ║   ════╗   ║
                       ║   ║           ║ B ║
                       ╚═══╩═══════════╩═══╝
                       """
                maze.remove_wall(maze.table[0][0], maze.table[0][1])
                maze.remove_wall(maze.table[0][2], maze.table[0][3])
                maze.remove_wall(maze.table[0][3], maze.table[0][4])
                maze.remove_wall(maze.table[1][0], maze.table[1][1])
                maze.remove_wall(maze.table[1][3], maze.table[1][4])
                maze.remove_wall(maze.table[0][1], maze.table[1][1])
                maze.remove_wall(maze.table[0][2], maze.table[1][2])
                maze.remove_wall(maze.table[0][4], maze.table[1][4])
                maze.remove_wall(maze.table[1][1], maze.table[2][1])
                maze.remove_wall(maze.table[2][1], maze.table[3][1])
                maze.remove_wall(maze.table[3][1], maze.table[4][1])
                maze.remove_wall(maze.table[1][0], maze.table[2][0])
                maze.remove_wall(maze.table[3][0], maze.table[4][0])
                maze.remove_wall(maze.table[3][0], maze.table[3][1])
                maze.remove_wall(maze.table[2][1], maze.table[2][2])
                maze.remove_wall(maze.table[2][2], maze.table[1][2])
                maze.remove_wall(maze.table[1][4], maze.table[2][4])
                maze.remove_wall(maze.table[2][2], maze.table[2][3])
                maze.remove_wall(maze.table[2][3], maze.table[3][3])
                maze.remove_wall(maze.table[3][2], maze.table[3][3])
                maze.remove_wall(maze.table[3][2], maze.table[4][2])
                maze.remove_wall(maze.table[4][1], maze.table[4][2])
                maze.remove_wall(maze.table[2][4], maze.table[3][4])
                maze.remove_wall(maze.table[3][3], maze.table[3][4])
                maze.remove_wall(maze.table[3][4], maze.table[4][4])
                maze.remove_wall(maze.table[4][2], maze.table[4][3])
                maze.start_point = maze.table[self.start_point.i][self.start_point.j]
                maze.finish_point = maze.table[self.finish_point.i][self.finish_point.j]
                yield maze, good_surface

    # BFS - ищет самый короткий маршрут по числу клеток, ему не важны веса => можно тестировать на любой поверхности
    # DFS - ищем самый дорогой путь с учетом весов, причем устойчив к циклам, за счет отслеживания посещенных вершин
    # Ford-Bellman - ищет самый дорогой путь с учетом весов, но не устойчив к циклам положительного веса =>
    # => нужно тестировать без улучшающих поверхностей

    def test_bfs_dfs_solvers(self):
        for maze, has_good_surface in self.get_maze_all_surface():
            print("Исходный лабиринт:")
            print(maze.get_renderer_path())
            bfs_solver = BfsSolver(maze)
            bfs_solver.find_path()
            print("BFS Path:")
            print(maze.get_renderer_path("BFS"))  # Отображаем путь для отладки

            dfs_solver = DfsSolver(maze)
            dfs_solver.find_path()
            print("DFS Path:")
            print(maze.get_renderer_path("DFS"))  # Отображаем путь для отладки

            if not has_good_surface:
                ford_bellman_solver = FordBellmanSolver(maze)
                ford_bellman_solver.find_path()
                print("Ford-Bellman Path:")
                print(maze.get_renderer_path("Ford-Bellman"))

            # Дополнительно можно проверить длину пути, если это необходимо
            # print(maze.paths_dict['DFS'])
            self.assertGreater(
                len(maze.paths_dict["BFS"]), 0, "BFS путь имеет нулевую длину!"
            )
            self.assertGreater(
                len(maze.paths_dict["DFS"]), 0, "DFS путь имеет нулевую длину!"
            )

    def test_optimal_path(self):
        self.good_surface = True
        self.bad_surface = True
        self.width = 2
        self.height = 2
        self.start_point = Cell(0, 0, 0)
        self.finish_point = Cell(1, 1, 0)

        maze = Maze(
            self.width,
            self.height,
            self.good_surface,
            self.bad_surface,
            self.start_point,
            self.finish_point,
        )
        """
        ╔═══════╗
        ║ A   1 ║
        ║       ║
        ║ -1  B ║
        ╚═══════╝
        """
        maze.remove_wall(maze.table[0][0], maze.table[0][1])
        maze.remove_wall(maze.table[0][1], maze.table[1][1])
        maze.remove_wall(maze.table[0][0], maze.table[1][0])
        maze.remove_wall(maze.table[1][0], maze.table[1][1])

        maze.table[0][0].weight = 0
        maze.table[0][1].weight = 1
        maze.table[1][0].weight = -1
        maze.table[1][1].weight = 0

        maze.start_point = maze.table[self.start_point.i][self.start_point.j]
        maze.finish_point = maze.table[self.finish_point.i][self.finish_point.j]

        print()
        print(maze.get_renderer_path())

        bfs_solver = BfsSolver(maze)
        dfs_solver = DfsSolver(maze)
        bfs_solver.find_path()
        dfs_solver.find_path()

        dfs_ans = maze.get_renderer_path("DFS")
        bfs_ans = maze.get_renderer_path("BFS")
        dfs_expected = "".join(
            (
                "╔═══════╗\n",
                "║ A   \033[42;30m→\033[0m ║\n",
                "║   ║   ║\n",
                "║-1   B ║\n",
                "╚═══════╝\n",
            )
        )

        bfs_expected = "".join(
            (
                "╔═══════╗\n",
                "║ A   1 ║\n",
                "║   ║   ║\n",
                "║ \033[42;30m↓\033[0m   B ║\n",
                "╚═══════╝\n",
            )
        )

        print("DFS:\n" + dfs_ans)
        print("BFS:\n" + bfs_ans)

        self.assertEqual(dfs_ans, dfs_expected, "Неверный путь DFS!")
        self.assertEqual(bfs_ans, bfs_expected, "Неверный путь BFS!")
