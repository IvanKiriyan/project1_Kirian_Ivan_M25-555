"""
Базовая механика - действия игрока
"""
from labyrinth_game.constants import ROOMS

def get_input(prompt="> "): #ввод пользователя
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state): #инвентарь игрока
    inventory = game_state['player_inventory']
    if inventory:
        print("\nВаш инвентарь:", ", ".join(inventory))
    else:
        print("\nВаш инвентарь пуст.")

def move_player(game_state, direction): #функция перемещения игрока
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction in exits:
        game_state["current_room"] = exits[direction]
        game_state["steps_taken"] += 1

        from labyrinth_game.utils import describe_current_room

        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name): #функция взятия предмета
    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name): #функция использования предмета
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Стало светлее.")
        return

    if item_name == "sword":
        print("Вы чувствуете уверенность.")
        return

    if item_name == "bronze_box":
        print("Вы открыли шкатулку.")
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
        return

    print("Вы не знаете, как использовать этот предмет.")