"""
Trying again
"""
# import dependencies
import hlt
import logging
from hlt.entity import Ship, Planet, Position
from hlt.game_map import Map, Player
import time
import math

def closest_ally(warrior):
    ally_list = game_map.nearby_entities_by_distance(warrior)
    ekeys = sorted(ally_list.keys())
    for ekey in ekeys:
        for entity in ally_list[ekey]:
            if type(entity) == Planet or entity.owner != game_map.get_me():
                continue
            elif entity != warrior:
                return entity
            else:
                continue

def closest_enemy(warrior):
    enemy_list = game_map.nearby_entities_by_distance(warrior)
    ekeys = sorted(enemy_list.keys())
    for ekey in ekeys:
        for entity in enemy_list[ekey]:
            if type(entity) == Planet or entity.owner == game_map.get_me():
                continue
            if entity.owner != game_map.get_me():
                return entity
            else:
                continue

def closest_planet(colonizer):
    planet_list = game_map.nearby_entities_by_distance(colonizer)
    ekeys = sorted(planet_list.keys())
    for ekey in ekeys:
        for entity in planet_list[ekey]:
            if type(entity) == Ship or entity.is_full() == True:
                continue
            elif entity.owner == game_map.get_me() and entity.is_full() == False:
                return entity
            elif entity.owner == None:
                return entity
            else:
                continue

def turn_setup():
    command_queue = []
    ships_to_command = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    my_docked_ships = len([ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.DOCKED])
    avg_docked_ships = len([ship for ship in game_map._all_ships() if ship.docking_status == Ship.DockingStatus.DOCKED])/len(game_map.all_players())
#    logging.info("Number of ships = " + str(len(ships_to_command)))
#    if avg_docked_ships > 0:
#        logging.info("My production = " + str(my_docked_ships))
#        logging.info("Average production = " + str(avg_docked_ships))
#        logging.info("My production divided by average production = " + str(my_docked_ships/avg_docked_ships))
    for ship in ships_to_command:
        command_hold = get_command(ship)
        if command_hold != None:
            command_queue.append(command_hold)
    logging.info("Turn Time = " + str(time.time()-turn_start))
    game.send_command_queue(command_queue)

def waypoint(mover, target):
    distance = int(game_map.width**(1/2))
    target_x = math.cos(math.radians(mover.calculate_angle_between(target))) * distance
    target_y = math.sin(math.radians(mover.calculate_angle_between(target))) * distance
    return Position(mover.x + target_x, mover.y + target_y)

def get_command(actor):
    entity_list = game_map.nearby_entities_by_distance(actor)
    ekeys = sorted(entity_list.keys())
    for ekey in ekeys:
        for entity in entity_list[ekey]:
            if entity.owner == game_map.get_me() or entity.owner == None:
                if type(entity) == Ship or entity.is_full():
                    continue
                elif actor.can_dock(entity):
                    return actor.dock(entity)
                else:
                    return actor.navigate(actor.closest_point_to(entity), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
            elif type(entity) == Planet and entity.is_full() == False:
                return actor.navigate(actor.closest_point_to(entity), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
            else:
                wingman = closest_ally(actor)
                if type(wingman) == Ship:
                    if actor.calculate_distance_between(entity) < actor.calculate_distance_between(wingman):
                        return actor.navigate(actor.closest_point_to(wingman), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
                return actor.navigate(actor.closest_point_to(entity), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

game = hlt.Game("Demitroy Current Upload")
logging.info("Demitroy Current Upload")

while True:
    turn_start = time.time()
    game_map = game.update_map()
    turn_setup()
