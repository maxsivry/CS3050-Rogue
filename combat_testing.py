import project_constants as constants
from classes.actor import Player
from classes.enemy import Enemy

hero = Player()

enemies = []
enemies.append(Enemy())
enemies.append(Enemy())

while (hero.is_alive and len(enemies) > 0):
    works = False
    target = -1
    print("The number of enemies is currently",len(enemies))
    while not works:
        works = True
        try:
            target = int(input("Attack enemy number: "))
            target -= 1
        except ValueError:
            print("doesn't work")
            works = False
        try:
            if target >= 0:
                hero.attack(enemies[target])
            else:
                print("No one there")
                works = False
        except IndexError:
            print("No one there")
            works = False

    new_enemies = []
    for enemy in enemies:
        if enemy.is_alive:
            if hero.is_alive:
                enemy.take_turn(hero, 0)
            new_enemies.append(enemy)
    enemies = new_enemies
    print("")