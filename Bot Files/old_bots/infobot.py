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
    distance = thing.calculate_distance_between(enemy_ship)
    if distance < lrad + 5:
        return thing.navigate(thing.closest_point_to(enemy_ship), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
    planet = closest_planet(thing)
    if thing.can_dock(planet):
        return thing.dock(planet)
    if type(planet) == Planet:
        return thing.navigate(thing.closest_point_to(planet), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
    return thing.navigate(thing.closest_point_to(enemy_ship), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

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
    game.send_command_queue(command_queue)
