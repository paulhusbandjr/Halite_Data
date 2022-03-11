"""
Current Upload Build
"""
import hlt
import logging
import time
from hlt.entity import Planet, Ship
from hlt.game_map import Map, Player

game = hlt.Game("Current")
logging.info("Starting my new code bot!")

def closest_planet(thing):
    entities = game_map.nearby_planets_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if ent.owner == game_map.get_me():
                if ent.is_full() == False:
                    return ent
            else:
                return ent

def closest_enemy_ship(thing):
    entities = game_map.nearby_ship_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if ent.owner != game_map.get_me():
                return ent

def get_command(thing):
    enemy_ship = closest_enemy_ship(thing)
    if thing.calculate_distance_between(enemy_ship) < 20:
        return thing.navigate(thing.closest_point_to(enemy_ship), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
    planet = closest_planet(thing)
    if thing.can_dock(planet):
        return thing.dock(planet)
    return thing.navigate(thing.closest_point_to(planet), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

while True:
    turn_start = time.time()
    game_map = game.update_map()
    command_queue = []
    my_ship_list = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    for ship in my_ship_list:
        if time.time() - turn_start > 1.85:
            break
        if get_command(ship) == None:
            continue
        command_queue.append(get_command(ship))
    game.send_command_queue(command_queue)
