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
                if ent.is_full() == False:
                    return ent

def closest_enemy_ship(thing):
    entities = game_map.nearby_entities_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if type(ent) == Ship and Ship.owner != game_map.get_me():
                return ent

while True:
    game_map = game.update_map()
    command_queue = []
    my_id = game_map.get_me()
    my_ships = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == ship.DockingStatus.UNDOCKED]
    unfilled_planets = [planet for planet in game_map.all_planets() if not planet.is_full()]
#    other_player_ids = [player for player in game_map.all_players()]
#    enemy_ships = [ship for ship in game_map._all_ships() if ship.owner != my_id]
    for ship in my_ships:
        if ship.can_dock(closest_planet(ship)):
            command_queue.append(ship.dock(closest_planet(ship)))
            break
        for planet in unfilled_planets:
            planet = closest_planet(ship)
            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
            else:
                navigate_command = ship.navigate(ship.closest_point_to(planet), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
            break
    game.send_command_queue(command_queue)
