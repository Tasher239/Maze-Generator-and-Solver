import unittest
from unittest.mock import patch
from utils.user_methods import UserMethods
from utils.cell import Cell
from utils.maze import Maze


class TestInvalidInputs(unittest.TestCase):
    @patch("builtins.input", side_effect=["52"])
    def test_valid_integer_input(self, mock_input):
        # сразу корректный ввод числа
        result = UserMethods.get_integer_input("Введите число: ")
        self.assertEqual(result, 52)

    @patch("builtins.input", side_effect=["invalid", ""])
    def test_empty_string_and_invalid_input(self, mock_input):
        # проверяем, что результат корректный (вводится некорректного ввода и пустой строки (=автоматический выбор))
        result = UserMethods.get_integer_input("Введите число: ")
        self.assertEqual(result, None)

    @patch("builtins.input", side_effect=["not a number", "another invalid", "52"])
    def test_non_integer_input(self, mock_input):
        # вводится 2 раза не числ и потом число
        result = UserMethods.get_integer_input("Введите число: ")
        self.assertEqual(result, 52)


class TestGetPointInMaze(unittest.TestCase):
    def setUp(self):
        self.good_surface = False
        self.bad_surface = False
        self.width = 4
        self.height = 4
        self.maze = Maze(
            self.width,
            self.height,
            self.good_surface,
            self.bad_surface,
            Cell(0, 0, 0),
            Cell(3, 3, 0),
        )

    @patch("builtins.input", side_effect=["1", "2"])  # Корректный ввод
    def test_valid_point_input(self, mock_input):
        result = UserMethods.get_point_in_maze(self.maze, "Start")
        self.assertEqual(result.i, 0)
        self.assertEqual(result.j, 1)

    @patch("builtins.input", side_effect=["", ""])  # Случайный ввод
    @patch(
        "random.randint", return_value=2
    )  # Предполагаем, что случайное значение будет 2
    def test_random_point_input(self, mock_random, mock_input):
        result = UserMethods.get_point_in_maze(self.maze, "Random")
        self.assertEqual(result.i, 1)  # Индекс 2, так как 1 (случайный) - 1 = 1
        self.assertEqual(result.j, 1)  # Индекс 2, так как 1 (случайный) - 1 = 1

    def test_is_valid_point(self):
        valid_point = Cell(1, 1, 0)
        invalid_point = Cell(5, 5, 0)
        self.assertTrue(self.maze.is_valid_point(valid_point.i, valid_point.j))
        self.assertFalse(self.maze.is_valid_point(invalid_point.i, invalid_point.j))


class TestGetMazeDimensions(unittest.TestCase):
    @patch("builtins.input", side_effect=["10", "15"])  # Корректный ввод
    def test_valid_dimensions(self, mock_input):
        width, height = UserMethods.get_maze_dimensions()
        self.assertEqual(width, 10)
        self.assertEqual(height, 15)

    @patch("builtins.input", side_effect=["", ""])  # Случайный ввод
    @patch(
        "random.randint", side_effect=[7, 12]
    )  # Предполагаем, что случайные значения будут 7 и 12
    def test_random_dimensions(self, mock_random, mock_input):
        width, height = UserMethods.get_maze_dimensions()
        self.assertEqual(width, 7)
        self.assertEqual(height, 12)

    @patch("builtins.input", side_effect=["-5", "10"])  # Некорректный ввод для ширины
    def test_negative_width(self, mock_input):
        with patch("builtins.print") as mock_print:
            width, height = UserMethods.get_maze_dimensions()
            mock_print.assert_called_with("Ширина не может быть отрицательной!\n")
            self.assertIsNone(width)
            self.assertIsNone(height)

    @patch("builtins.input", side_effect=["10", "-3"])  # Некорректный ввод для высоты
    def test_negative_height(self, mock_input):
        with patch("builtins.print") as mock_print:
            width, height = UserMethods.get_maze_dimensions()
            mock_print.assert_called_with("Высота не может быть отрицательной!\n")
            self.assertIsNone(width)
            self.assertIsNone(height)
