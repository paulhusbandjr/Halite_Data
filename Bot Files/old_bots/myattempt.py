import hlt
import logging
from hlt.entity import Planet, Ship

game = hlt.Game("Settler2")
logging.info("Starting my Settler bot!")

def closest_planet(thing):
    entities = game_map.nearby_entities_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if type(ent) == Planet:
                if ent.is_full() == False:
                    if ent.owner == my_id:
                        return ent
                    else:
                        return ent

def closest_enemy_ship(thing):
    entities = game_map.nearby_entities_by_distance(thing)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for ent in entities[ekey]:
            if type(ent) == Ship and ent.owner != game_map.get_me():
                return ent

while True:
    game_map = game.update_map()
    my_id = game.map.get_me()
    command_queue = []
    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue
        for planet in game_map.all_planets():
            if planet.is_owned() and not planet.is_full():
                continue
            planet = closest_planet(ship)
            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
            else:
                navigate_command = ship.navigate(ship.closest_point_to(planet), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
                else:
                    command_queue.append(ship.navigate(ship.closest_point_to(closest_enemy_ship(ship)), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False))
            break
    game.send_command_queue(command_queue)
