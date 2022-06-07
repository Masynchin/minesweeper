from argparser import argparser
from commands import Commands
from field import Field
from game import Game


def main():
    """Точка входа в игру."""
    args = argparser.parse_args()
    if args.help:
        print_rules()

    field = Field(width=args.width, height=args.height)
    field.set_bombs(bombs_count=args.bombs_count)
    commands = Commands()
    game = Game(commands, field)
    game.run()


def print_rules():
    """Вывод правил игры."""
    with open("rules.txt", encoding="u8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
