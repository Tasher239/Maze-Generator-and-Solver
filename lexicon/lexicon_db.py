import enum


# Основные команды игры
class GameCommands(enum.StrEnum):
    HELLO = enum.auto()  # Информация об игре
    MENU = enum.auto()  # Главное меню
    WRONG_COMMAND = enum.auto()  # Неверная команда
    EXIT = enum.auto()  # Выход из игры


class CommandValidationAnswer(enum.StrEnum):
    WRONG_COMMAND = enum.auto()


class Command(enum.Enum):
    GENERATE_MAZE = "1"  # Команда для генерации лабиринта
    EXIT = "2"  # Команда для выхода


class SolversType(enum.Enum):
    BFS = "1"
    FORD_BELLMAN = "2"
    DFS = "3"


class GeneratorType(enum.Enum):
    KRUSKAL = "1"
    PRIM = "2"
    GROWING_FOREST = "3"


game_process_commands = {
    GameCommands.HELLO: ("Добро пожаловать в 'Лабиринты'!\n"),
    GameCommands.MENU: (
        "Введите 1 - сгенерировать лабиринт\n" "Введите 2 - выйти из игры\n>> "
    ),
    GameCommands.WRONG_COMMAND: "Введена неверная команда!\n",
    GameCommands.EXIT: "Выход из игры. До свидания!\U0001F44B\n",
}
