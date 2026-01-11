"""
Базовая механика - действия игрока
"""

from labyrinth_game.constants import ROOMS


#Обработка команд
def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
#Инвентарь игрока
def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("\nВаш инвентарь:", ", ".join(inventory))
    else:
        print("\nВаш инвентарь пуст.")

#Функция перемещения игрока
def move_player(game_state, direction):
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    if next_room == "treasure_room":
        if "rusty_key" in game_state["player_inventory"]:
            print("Вы используете найденный ключ, " \
            "чтобы открыть путь в комнату сокровищ.")
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    from labyrinth_game.utils import describe_current_room, random_event

    describe_current_room(game_state)
    random_event(game_state)

#Функция взятия предмета
def take_item(game_state, item_name):
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

#Функция использования предметов
def use_item(game_state, item_name):
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