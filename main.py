import os
import time

from argparser import argparser
from commander import exec_command
from exceptions import BombDetonation, CellOutOfRange, NotEnoughFlags, QuitGame
from field import Field
from printer import print_field


def main():
    """Обработчик игры."""
    args = argparser.parse_args()

    if args.help:
        print_rules()

    field = Field(width=args.width, height=args.height)
    field.set_bombs(bombs_count=args.bombs_count)

    start_time = time.time()

    while True:
        print_field(field)
        while True:
            command = input("\n> Введите координаты клетки: ")
            try:
                exec_command(command, field)
            except QuitGame:
                clear_screen()
                exit(0)
            except CellOutOfRange:
                print("Неверные координаты клетки!")
            except NotEnoughFlags:
                print("Недостаточно флагов для открытия соседей!")
            except BombDetonation:
                print("К сожалению, вы взорвались!")
                time.sleep(3)
                exit(0)
            else:
                break

        clear_screen()
        if field.is_win():
            break

    end_time = time.time()
    elapsed_time = int(end_time - start_time)

    template = get_congratulation_template(elapsed_time)
    print(template.format(elapsed_time=elapsed_time))


def print_rules():
    """Вывод правил игры."""
    with open("rules.txt", encoding="u8") as f:
        print(f.read())


def clear_screen():
    """Исполнение команды очистки консоли."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_congratulation_template(elapsed_time: int) -> str:
    """
    Получение шаблона при победе,
    в зависимости от окончания числа секунд игры.
    """
    if 11 <= elapsed_time <= 19 or elapsed_time % 10 in (0, 5, 6, 7, 8, 9):
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунд!"
    elif elapsed_time % 10 in (2, 3, 4):
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунды!"
    elif elapsed_time % 10 == 1:
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунду!"

    return template


if __name__ == "__main__":
    main()
