"""
Игровая логика
"""
import math  #усложнение логики

from labyrinth_game.constants import ROOMS


#Рандомизация путешествия
def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)

#Добавлены ловушки
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]
    if inventory:
        idx = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(idx)
        print("Вы потеряли предмет:", lost_item)
        return

    roll = pseudo_random(game_state["steps_taken"], 10)
    if roll < 3:
        print("Вы получили смертельный урон. Игра окончена.")
        game_state["game_over"] = True
    else:
        print("Вы уцелели.")

#Неслучайные случайности
def random_event(game_state):
    chance = pseudo_random(game_state["steps_taken"], 10)
    if chance != 0:
        return

    event_type = pseudo_random(game_state["steps_taken"] + 1, 3)
    current_room = game_state["current_room"]
    room_info = ROOMS[current_room]

    if event_type == 0:
        print("Вы нашли на полу монетку.")
        room_info["items"].append("coin")
        return

    if event_type == 1:
        print("Вы слышите шорох.")
        if "sword" in game_state["player_inventory"]:
            print("Вы размахиваете мечом и отпугиваете существо.")
        return

    if event_type == 2:
        if (
            current_room == "trap_room" and "torch" 
            not in game_state["player_inventory"]
        ):
            print("В темноте вы не замечаете механизм под ногами...")
            trigger_trap(game_state)

def describe_current_room(game_state): #Описание комнат
    current_room = game_state["current_room"]
    room_info = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room_info["description"])

    if room_info["items"]:
        print("Заметные предметы:", ", ".join(room_info["items"]))

    print("Выходы:", ", ".join(room_info["exits"].keys()))

    if room_info["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")

#Вывод вспомогательных команд
def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")

#Функция решения команд
def solve_puzzle(game_state):
    current_room = game_state["current_room"]
    puzzle = ROOMS[current_room]["puzzle"]

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)

    from labyrinth_game.player_actions import get_input

    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct_answer = str(answer).strip().lower()

    acceptable = {correct_answer}
    if correct_answer == "10":
        acceptable.add("десять")

    if user_answer in acceptable:
        print("Верно!")
        ROOMS[current_room]["puzzle"] = None

        rewards = {
            "hall": "treasure_key",
        }
        reward = rewards.get(current_room)
        if reward and reward not in game_state["player_inventory"]:
            game_state["player_inventory"].append(reward)
        return

    print("Неверно. Попробуйте снова.")
    if current_room == "trap_room":
        trigger_trap(game_state)

#Логика победы
def attempt_open_treasure(game_state):
    current_room = game_state["current_room"]
    room_info = ROOMS[current_room]

    if "treasure_chest" not in room_info["items"]:
        print("Загадок здесь нет.")
        return

    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_info["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    from labyrinth_game.player_actions import get_input

    choice = get_input("Сундук заперт. Ввести код? (да/нет) ").strip().lower()
    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    code = get_input("Ваш ответ: ").strip()
    puzzle = room_info["puzzle"]
    correct_code = puzzle[1] if puzzle else ""

    acceptable = {str(correct_code).strip().lower()}
    if str(correct_code).strip().lower() == "10":
        acceptable.add("десять")

    if code.strip().lower() in acceptable:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_info["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверно. Попробуйте снова.")