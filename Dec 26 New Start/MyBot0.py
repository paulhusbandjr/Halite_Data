"""
Trying again
"""
# import dependencies
import hlt
import logging
import time
from hlt.entity import Ship, Planet
from hlt.game_map import Map, Player

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
            elif type(entity) == Planet:
                continue
            else:
                return actor.navigate(actor.closest_point_to(entity), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Demitroy Set")
logging.info("Demitroy Set")

while True:
    turn_start = time.time()
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    command_queue = []
    ships_to_command = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    for ship in ships_to_command:
        command_hold = get_command(ship)
        if command_hold != None:
            command_queue.append(get_command(ship))
    logging.info(str(time.time() - turn_start))
    game.send_command_queue(command_queue)
