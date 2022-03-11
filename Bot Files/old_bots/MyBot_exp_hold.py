"""
Current Experiment Build
"""
import hlt
import logging
import time
from hlt.entity import Planet, Ship
from hlt.game_map import Map, Player

game = hlt.Game("Experiment")
logging.info("Starting my new code bot!")
start = False

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
    if thing.can_dock(planet):# and (planet.owner == game_map.get_me() or planet.owner == None):
        return thing.dock(planet)
    return thing.navigate(thing.closest_point_to(planet), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

while True:
    turn_start = time.time()
    planet_data = open("planets_loc.txt","a")
    ship_data = open("ship_loc.txt","a")
    game_map = game.update_map()
    if start == False:
        planet_data.write('Map Width, Map Height, Planet ID, Planet X, Planet Y, Planet Radius, Planet Docking Spots' + '\n')
        for planet in game_map.all_planets():
            planet_data.write(str(game_map.width) + ',' + str(game_map.height) + ',' + str(planet.id) + ',' + str(planet.x) + ',' + str(planet.y) + ',' + str(planet.radius) + ',' + str(planet.num_docking_spots) + '\n')
        ship_data.write('Map Width, Map Height, Ship ID, Ship X, Ship Y' + '\n')
        for ship in game_map._all_ships():
            ship_data.write(str(game_map.width) + ',' + str(game_map.height) + ',' + str(ship.id) + ',' + str(ship.x) + ',' + str(ship.y) + '\n')
        start = True
    command_queue = []
    my_ship_list = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    for ship in my_ship_list:
        if time.time() - turn_start > 1.85:
            break
        if get_command(ship) == None:
            continue
        command_queue.append(get_command(ship))
    game.send_command_queue(command_queue)
