#!/usr/bin/env python3

"""
Основной игровой цикл
"""

from labyrinth_game import player_actions, utils
from labyrinth_game.constants import COMMANDS

game_state = {
    "player_inventory": [], #Инвентарь игрока
    "current_room": "entrance", #Текущая комната
    "game_over": False, #Значения окончания игры
    "steps_taken": 0, #Количество шагов
}

#Обработка команд
def process_command(game_state, command_line, commands):
    command_line = command_line.strip()
    if not command_line:
        return

    parts = command_line.split()
    command = parts[0].lower()
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    directions = {"north", "south", "east", "west"}
    if command in directions:
        player_actions.move_player(game_state, command)
        return

    match command:
        case "look":
            utils.describe_current_room(game_state)
        case "inventory":
            player_actions.show_inventory(game_state)
        case "help":
            utils.show_help(commands)
        case "go":
            if arg:
                player_actions.move_player(game_state, arg)
            else:
                utils.show_help(commands)
        case "take":
            if arg:
                player_actions.take_item(game_state, arg)
            else:
                utils.show_help(commands)
        case "use":
            if arg:
                player_actions.use_item(game_state, arg)
            else:
                utils.show_help(commands)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case "quit" | "exit":
            game_state["game_over"] = True
        case _:
            utils.show_help(commands)

#Приветствие игрока
def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = player_actions.get_input("> ")
        process_command(game_state, command_line, COMMANDS)


if __name__ == "__main__":
    main()