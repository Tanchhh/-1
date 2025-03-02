map_width = 10
map_height = 10


def create_map(width, height):
    game_map = [['.' for _ in range(width)] for _ in range(height)]
    door_side = (width + height) // 2 % 4  
    if door_side == 0:  # top
        door_x, door_y = width // 2, 0
    elif door_side == 1:  
        door_x, door_y = width // 2, height - 1
    elif door_side == 2:  
        door_x, door_y = 0, height // 2
    else:  # right
        door_x, door_y = width - 1, height // 2
    game_map[door_y][door_x] = 'Ξ'  
    return game_map, door_x, door_y

def render_map(game_map):
    for row in game_map:
        print(' '.join(row))
    print()

print("Выберите тип карты:")
print("1. Стандартная карта 5x5")
print("2. Генерация пользовательской карты")

choice = input("Введите номер варианта: ")
if choice == '1':
    map_width = 5
    map_height = 5
    game_map, door_x, door_y = create_map(map_width, map_height)
elif choice == '2':
    try:
        map_width = int(input("Введите ширину карты: "))
        map_height = int(input("Введите высоту карты: "))
        if map_width < 3 or map_height < 3:
            print("Минимальный размер карты должен быть 3x3.")
            exit()
        game_map, door_x, door_y = create_map(map_width, map_height)
    except ValueError:
        print("Неверный ввод размеров карты.")
        exit()
else:
    print("Неверный выбор.")
    exit()

player_x = map_width // 2
player_y = map_height // 2
while game_map[player_y][player_x] == 'Ξ': 
    player_x = (player_x + 1) % map_width
    player_y = (player_y + 1) % map_height
game_map[player_y][player_x] = '@'

player_hp = 10
player_mp = 5
player_armor = 2
player_damage = 3
player_level = 1
player_experience = 0
inventory = []
enemy_x = -1  
enemy_y = -1
enemy_hp = 5
enemy_armor = 1
enemy_damage = 2
enemy_level = 1
enemy_alive = False
spawn_counter = 0  

def move_player(dx, dy, game_map):
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy

    if 0 <= new_x < map_width and 0 <= new_y < map_height:
        underlying_symbol = game_map[new_y][new_x]

        if game_map[player_y][player_x] == 'Ξ' or game_map[player_y][player_x] == 'E':
            game_map[player_y][player_x] = game_map[player_y][player_x]
        else:
            game_map[player_y][player_x] = '.'

        player_x = new_x
        player_y = new_y

        if underlying_symbol == '.':
            game_map[new_y][new_x] = '@'
        elif underlying_symbol == 'Ξ' or underlying_symbol == 'E':
            game_map[new_y][new_x] = '@'
            
def calculate_damage(attacker_damage, defender_armor):
    damage = max(0, attacker_damage - defender_armor)
    return damage

def attack_enemy():
    global enemy_hp, player_hp, player_experience
    damage = calculate_damage(player_damage, enemy_armor)
    enemy_hp -= damage
    print(f"Вы нанесли {damage} урона врагу. У врага осталось {enemy_hp} HP.")
    if enemy_hp <= 0:
        print("Вы победили!")
        player_experience += 5  
        level_up()
        return True
    return False

def enemy_attack():
    global player_hp
    damage = calculate_damage(enemy_damage, player_armor)
    player_hp -= damage
    print(f"Враг нанес вам {damage} урона. У вас осталось {player_hp} HP.")
    if player_hp <= 0:
        print("Вы проиграли!")
        exit()

def pick_item(item):
    inventory.append(item)
    print(f"Вы подобрали {item}.")

def level_up():
    global player_level, player_damage, player_hp
    if player_experience >= 10:  
        player_level += 1
        player_hp += 5
        player_damage += 2
        print(f"Вы достигли уровня {player_level}! Теперь у вас {player_hp} HP и {player_damage} DMG.")

def open_door():
    print("Вы вошли в дверь!")

def get_enemy_spawn_position(edge):
    if edge == 'top':
        return (0, map_width // 2) 
    elif edge == 'bottom':
        return (map_height - 1, map_width // 2)  
    elif edge == 'left':
        return (map_height // 2, 0)  
    elif edge == 'right':
        return (map_height // 2, map_width - 1)  

def respawn_enemy(game_map):
    global enemy_hp, enemy_x, enemy_y, enemy_level, enemy_damage, enemy_armor, enemy_alive, spawn_counter
    enemy_level = player_level  
    enemy_hp = 5 + enemy_level * 2  #
    enemy_damage = 2 + enemy_level  
    enemy_armor = 1 + enemy_level // 2  
    enemy_alive = True  

    edges = ['top', 'bottom', 'left', 'right']
    edge = edges[spawn_counter % len(edges)]
    new_position = get_enemy_spawn_position(edge)

    while game_map[new_position[0]][new_position[1]] != '.':
        spawn_counter += 1
        edge = edges[spawn_counter % len(edges)]
        new_position = get_enemy_spawn_position(edge)

    enemy_x, enemy_y = new_position
    game_map[enemy_y][enemy_x] = 'E'
    print(f"Враг респавнится на новой позиции: ({enemy_x}, {enemy_y}).")
    spawn_counter += 1  

while True:
    render_map(game_map)
    print(f"Ваше здоровье: {player_hp}, Инвентарь: {inventory}, Уровень: {player_level}, Опыт: {player_experience}")
    move = input("Введите направление (w-вверх, s-вниз, a-влево, d-вправо, attack-атаковать, pick-подобрать предмет, enter-войти в дверь): ")

    if move == 'w':
        move_player(0, -1, game_map)
    elif move == 's':
        move_player(0, 1, game_map)
    elif move == 'a':
        move_player(-1, 0, game_map)
    elif move == 'd':
        move_player(1, 0, game_map)
    elif move == 'attack':
        if enemy_alive and enemy_x == player_x and enemy_y == player_y: 
            if attack_enemy():
                enemy_alive = False  
                game_map[enemy_y][enemy_x] = 'E' 
                continue
            enemy_attack()
        else:
            print("Нет врага для атаки!")
    elif move == 'pick':
        if game_map[player_y][player_x] == 'I':  
            pick_item("Золотая монета")  
            game_map[player_y][player_x] = '.' 
        else:
            print("Нет предметов для подбора!")
    elif move == 'enter':
        if player_x == door_x and player_y == door_y:  
            open_door()
            if not enemy_alive:  
                respawn_enemy(game_map)
        else:
            print("Вы не можете войти в эту дверь!")
    else:
        print("Неверный ввод.")