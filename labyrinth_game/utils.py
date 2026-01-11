"""
Игровая логика
"""
from labyrinth_game.constants import ROOMS


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
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

#Функция решения команд
def solve_puzzle(game_state):
    current_room = game_state["current_room"]

    if current_room == "treasure_room":
        attempt_open_treasure(game_state)
        return

    puzzle = ROOMS[current_room]["puzzle"]
    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)

    from labyrinth_game.player_actions import get_input

    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct_answer = answer.strip().lower()

    if user_answer == correct_answer:
        print("Верно!")
        ROOMS[current_room]["puzzle"] = None

        if (
            current_room == "hall"
            and "treasure_key" not in game_state["player_inventory"]
        ):
            game_state["player_inventory"].append("treasure_key")
    else:
        print("Неверно. Попробуйте снова.")

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

    if code == correct_code:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_info["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверно. Попробуйте снова.")