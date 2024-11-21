from lexicon.lexicon_db import game_process_commands, GameCommands, Command
from utils.cleen_screen import clear_screen
from utils.user_methods import UserMethods


def main() -> None:
    print(game_process_commands[GameCommands.HELLO])

    while command_id := input(game_process_commands[GameCommands.MENU]):
        try:
            command = Command(command_id.strip())
        except ValueError:
            clear_screen()
            print(game_process_commands[GameCommands.WRONG_COMMAND])
            continue
        UserMethods.process_command(command)


if __name__ == "__main__":
    main()
