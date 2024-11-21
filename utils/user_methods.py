import random
from typing import Optional, Tuple
from lexicon.lexicon_db import game_process_commands, GameCommands, Command
from maze_generators.base_generator import BaseGenerator
from maze_solvers.base_solver import BaseSolver
from utils.maze import Maze
from utils.cell import Cell
from maze_generators.kruskal_generator import KruskalGenerator
from maze_generators.prim_generator import PrimGenerator
from maze_solvers.bfs_solver import BfsSolver
from maze_solvers.ford_bellman_solver import FordBellmanSolver
from lexicon.lexicon_db import SolversType, GeneratorType
from maze_generators.forest_generator import GrowingForestGenerator
from maze_solvers.dfs_solver import DfsSolver
from utils.cleen_screen import clear_screen


class UserMethods:
    @staticmethod
    def get_integer_input(prompt: str) -> Optional[int]:
        """Запрашивает и возвращает корректное целое число или None"""
        while True:
            try:
                value = input(prompt).strip()
                if value:
                    return int(value)
                return None
            except ValueError:
                print("Некорректное значение! Попробуйте еще раз.")

    @staticmethod
    def get_point_in_maze(maze: Maze, point_name: str) -> Cell:
        """Запрашивает и возвращает координаты точки в лабиринте"""
        while True:
            i = UserMethods.get_integer_input(
                f"Номер строки {point_name} точки (или Enter для случайного): "
            )
            j = UserMethods.get_integer_input(
                f"Номер столбца {point_name} точки (или Enter для случайного): "
            )

            if i is None:
                i = random.randint(1, maze.height)
            if j is None:
                j = random.randint(1, maze.width)

            i -= 1
            j -= 1

            if maze.is_valid_point(i, j):
                return maze.table[i][j]
            else:
                print("Некорректные координаты точки! Попробуйте еще раз.")

    @staticmethod
    def get_maze_dimensions() -> Tuple[int | None, int | None]:
        """Запрашивает и возвращает размеры лабиринта"""
        print("Введите размеры лабиринта (или Enter для случайного размера)")
        width = UserMethods.get_integer_input("Введите ширину лабиринта: ")
        if not width:
            width = random.randint(5, 20)
        if width < 0:
            print("Ширина не может быть отрицательной!\n")
            return None, None

        height = UserMethods.get_integer_input("Введите высоту лабиринта: ")
        if not height:
            height = random.randint(5, 20)
        if height < 0:
            print("Высота не может быть отрицательной!\n")
            return None, None

        return width, height

    @staticmethod
    def choice_surface_type(mes1: str, mes2: str) -> bool:
        """Запрашивает тип поверхности"""
        while True:
            surface = input(
                f"\nДобавлять {mes1} поверхности (поверхности, за прохождение по которым {mes2} очки)? Enter для автоматического выбора\n1. Да\n2. Нет\n>> "
            )
            match surface:
                case "1":
                    return True
                case "2":
                    return False
                case "":
                    return random.choice([True, False])
                case _:
                    print("Некорректный ввод!")

    @staticmethod
    def get_surface_type() -> Tuple[bool, bool]:
        """Запрашивает и возвращает типы поверхностей"""
        good_surface = UserMethods.choice_surface_type("улучшающие", "начисляются")
        bad_surface = UserMethods.choice_surface_type("ухудшающие", "снимаются")

        return good_surface, bad_surface

    @staticmethod
    def get_maze_generator(
        width: int, height: int, good_surface: bool, bad_surface: bool
    ) -> BaseGenerator | None:
        """Генерирует лабиринт выбранным алгоритмом"""
        generators_lst = ["Крускала", "Прима", "Выращивание леса"]
        algorithms_menu = "\n".join(
            f"{i + 1}. {algo}" for i, algo in enumerate(generators_lst)
        )
        generator_id = input(
            f"\nВыберите тип генератора лабиринта:\n{algorithms_menu}\n>> "
        )

        try:
            generator = GeneratorType(generator_id)
        except ValueError:
            print("Некорректный тип генератора!")
            return None

        match generator:
            case GeneratorType.KRUSKAL:
                return KruskalGenerator(
                    width,
                    height,
                    good_surface,
                    bad_surface,
                    Cell(-1, -1, 0),
                    Cell(-1, -1, 0),
                )
            case GeneratorType.PRIM:
                return PrimGenerator(
                    width,
                    height,
                    good_surface,
                    bad_surface,
                    Cell(-1, -1, 0),
                    Cell(-1, -1, 0),
                )
            case GeneratorType.GROWING_FOREST:
                return GrowingForestGenerator(
                    width,
                    height,
                    good_surface,
                    bad_surface,
                    Cell(-1, -1, 0),
                    Cell(-1, -1, 0),
                )
            case _:
                return None

    @staticmethod
    def get_maze_solver(maze: Maze) -> BaseSolver | None:
        # Выбор алгоритма поиска пути
        algorithms_lst = ["BFS", "Ford-Bellman", "DFS"]
        algorithms_menu = "\n".join(
            f"{i + 1}. {algo}" for i, algo in enumerate(algorithms_lst)
        )
        solver_id = input(f"Выберите алгоритм поиска пути:\n{algorithms_menu}\n>> ")

        try:
            solver = SolversType(solver_id)
        except ValueError:
            print("Некорректный выбор алгоритма!")
            return None

        match solver:
            case SolversType.BFS:
                return BfsSolver(maze)
            case SolversType.FORD_BELLMAN:
                return FordBellmanSolver(maze)
            case SolversType.DFS:
                return DfsSolver(maze)
            case _:
                return None

    @staticmethod
    def process_maze_solver(maze: Maze) -> None:
        solver = UserMethods.get_maze_solver(maze)
        if not solver:
            print("Выбран некорректный алгоритм поиска пути!")
            return
        if solver.solver_name not in maze.paths_dict:
            solver.find_path()
        print(maze.get_renderer_path(solver.solver_name))
        print(
            f"Набрано очков: {sum(cell.weight for cell in maze.paths_dict[solver.solver_name])}"
        )
        return None

    @staticmethod
    def solve_maze_another_algorithm(maze: Maze) -> None:
        while True:
            print("Решить другим алгоритмом?\n1. Да\n2. Нет")
            choice = input()
            match choice:
                case "1":
                    UserMethods.process_maze_solver(maze)
                case "2":
                    return None
                case _:
                    print("Некорректный ввод")

    @staticmethod
    def process_command(command):
        match command:
            case Command.GENERATE_MAZE:
                width, height = UserMethods.get_maze_dimensions()
                if width is None or height is None:
                    return

                good_surface, bad_surface = UserMethods.get_surface_type()
                generator = UserMethods.get_maze_generator(
                    width, height, good_surface, bad_surface
                )

                if not generator:
                    return
                maze = generator.generate()
                print(maze.get_renderer_path())

                # Ввод стартовой и конечной точек
                print("Введите начальную точку (Enter для случайного выбора)")
                maze.start_point = UserMethods.get_point_in_maze(maze, "начальной")

                print("Введите конечную точку (Enter для случайного выбора)")
                maze.finish_point = UserMethods.get_point_in_maze(maze, "конечной")

                UserMethods.process_maze_solver(maze)
                UserMethods.solve_maze_another_algorithm(maze)

            case Command.EXIT:
                clear_screen()
                print(game_process_commands[GameCommands.EXIT])
                exit(0)
            case _:
                clear_screen()
                print(game_process_commands[GameCommands.WRONG_COMMAND])
