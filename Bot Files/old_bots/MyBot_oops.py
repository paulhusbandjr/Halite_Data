"""
Current Experiment Build
"""
import hlt
import logging
from hlt.entity import Planet, Ship
from hlt.game_map import Map, Player

game = hlt.Game("Experiment")
logging.info("Starting my new code bot!")

def closest_planet(thing):
    entities = game_map.nearby_entities_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if type(ent) == Planet:
                if ent.owner == game_map.get_me():
                    if ent.is_full = False:
                        return ent
                else:
                    return ent

def get_command(thing):
    if type(closest_planet(thing)) == Planet:
        planet = closest_planet(thing)
    if thing.can_dock(planet) and (planet.owner == None or planet.owner == game_map.get_me()):
#        logging.info(str(thing.id) + "Can Dock")
        return thing.dock(planet)
    if planet.owner == game_map.get_me() and planet.is_full() == False:
        return thing.navigate(thing.closest_point_to(planet), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
    if planet.owner == None:
        return thing.navigate(thing.closest_point_to(planet), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)
    if planet.owner != game_map.get_me():
        for enemy in planet.all_docked_ships():
            return thing.navigate(thing.closest_point_to(enemy), game_map, speed = int(hlt.constants.MAX_SPEED), ignore_ships = False)

while True:
    game_map = game.update_map()
    command_queue = []
    my_ship_list = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
#    unfilled_planets = [planet for planet in game_map.all_planets() if not planet.is_full()]
#    logging.info(unfilled_planets)
#    other_player_ids = [player for player in game_map.all_players()]
#    enemy_ships = [ship for ship in game_map._all_ships() if ship.owner != my_id]
    for ship in my_ship_list:
        if get_command(ship) == None:
            continue
#        logging.info(get_command(ship))
        command_queue.append(get_command(ship))
    #logging.info(command_queue)
    game.send_command_queue(command_queue)
