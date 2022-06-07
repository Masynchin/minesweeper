import os
from argparser import argparser
from commands import Commands
from console import Console
from field import Field
from game import Game, TimedGame


def main():
    """Точка входа в игру."""
    args = argparser.parse_args()
    if args.help:
        print_rules()

    field = Field(width=args.width, height=args.height)
    field.set_bombs(bombs_count=args.bombs_count)
    commands = Commands()
    console = Console(os.name)
    game = Game(commands, field, console)
    TimedGame(game, console).run()


def print_rules():
    """Вывод правил игры."""
    with open("rules.txt", encoding="u8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
