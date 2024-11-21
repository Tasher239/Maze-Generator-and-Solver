import unittest
from utils.cell import Cell
from maze_generators.kruskal_generator import KruskalGenerator
from maze_generators.prim_generator import PrimGenerator
from maze_generators.forest_generator import GrowingForestGenerator
from random import randint


class TestMazeDisplay(unittest.TestCase):
    def setUp(self):
        # Общие параметры лабиринта для тестов
        self.good_surface = False
        self.bad_surface = False
        self.start_point = Cell(0, 0, 0)
        # Генераторы лабиринтов
        self.generators = [
            ("Prim", PrimGenerator),
            ("Kruskal", KruskalGenerator),
            ("GrowingForest", GrowingForestGenerator),
        ]
        # Разные размеры лабиринтов
        self.sizes = [(4, 4), (5, 5), (10, 10), (15, 15)]

    def test_display_generators(self):
        # Тест отображения лабиринтов для каждого генератора
        for width, height in self.sizes:
            print(
                f"\n------- Тест отображения лабиринтов для размера {width}x{height} -------"
            )
            for name, GeneratorClass in self.generators:
                with self.subTest(generator=name):
                    generator = GeneratorClass(
                        width,
                        height,
                        self.good_surface,
                        self.bad_surface,
                        self.start_point,
                        Cell(randint(1, width - 1), randint(1, height - 1), 0),
                    )
                    maze = generator.generate()
                    display_output = maze.get_renderer_path("")
                    print(f"\n{name} Generator Output:")
                    print(display_output)
                    # Проверка типа и наличия стартовой и конечной точек
                    self.assertIsInstance(display_output, str)
                    self.assertIn("A", display_output)  # Стартовая точка
                    self.assertIn("B", display_output)  # Конечная точка
