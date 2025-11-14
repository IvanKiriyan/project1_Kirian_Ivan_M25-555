from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    current_room = game_state['current_room']
    room_info = ROOMS['current_room']

    print(f"\n== {current_room.upper()} ==")
    print(room_info['description'])

    if room_info['items']:
        print("Заметные предметы:", ", ".join(room_info['items']))

    exits = room_info['exits']
    print("Выходы:", ", ".join(exits.keys()))

    if room_info['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
