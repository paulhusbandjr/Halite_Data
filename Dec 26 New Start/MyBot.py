import hlt, logging, time, math
from hlt.entity import Ship, Planet, Position
from hlt.game_map import Map, Player

def turn_setup():
    command_queue = []
    my_ships = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    for ship in my_ships:
        hold_command = get_command(ship)
        if hold_command != None:
            command_queue.append(hold_command)
    logging.info("Turn Time = " + str(time.time() - turn_start))
    game.send_command_queue(command_queue)

def get_command(actor):
    target_planet = get_planet(actor)
    enemy_ship = get_ship(actor)
    if actor.calculate_distance_between(enemy_ship) < game_map.width**(1/2):
        return movement(actor, enemy_ship, game_map)
    elif type(target_planet) == Planet:
        if actor.can_dock(target_planet):
            return actor.dock(target_planet)
        else:
            return movement(actor, actor.closest_point_to(target_planet), game_map)
    else:
        return movement(actor, enemy_ship, game_map)

def movement(mover, target, game_map, speed = hlt.constants.MAX_SPEED, avoid_obstacles = True, max_corrections = 90, angular_step = 1, ignore_ships = False, ignore_planets = False):
    new_step = angular_step * 2
    if max_corrections <= 0:
        return None
    distance = min(speed, mover.calculate_distance_between(target))
    angle = mover.calculate_angle_between(target)
    target_pos = waypoint(mover, target)
    ignore = () if not (ignore_ships or ignore_planets) \
        else Ship if (ignore_ships and not ignore_planets) \
        else Planet if (ignore_planets and not ignore_ships) \
        else Entity
    if avoid_obstacles and game_map.obstacles_between(mover, target_pos, ignore):
        for obstacle in game_map.obstacles_between(mover, target_pos, ignore):
            if mover.calculate_angle_between(obstacle) > angle:
                dx = math.cos(math.radians(angle - angular_step)) * distance
                dy = math.sin(math.radians(angle - angular_step)) * distance
                new_pos = Position(mover.x + dx, mover.y + dy)
                return movement(mover, new_pos, game_map, max_corrections = max_corrections - 1)
            else:
                dx = math.cos(math.radians(angle + angular_step)) * distance
                dy = math.sin(math.radians(angle + angular_step)) * distance
                new_pos = Position(mover.x + dx, mover.y + dy)
                return movement(mover, new_pos, game_map, max_corrections = max_corrections - 1)
    if not game_map.obstacles_between(mover, target_pos, ignore):
        return mover.thrust(distance, angle)

def waypoint(mover, target):
    angle = mover.calculate_angle_between(mover.closest_point_to(target))
    return Position(mover.x + math.cos(math.radians(angle)) * hlt.constants.MAX_SPEED,
                    mover.y + math.sin(math.radians(angle)) * hlt.constants.MAX_SPEED)

def get_ship(mover):
    entities = game_map.nearby_entities_by_distance(mover)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for entity in entities[ekey]:
            if type(entity) != Ship:
                continue
            else:
                if entity.owner == game_map.get_me():
                    continue
                else:
                    return entity

def get_planet(observer):
    entities = game_map.nearby_entities_by_distance(observer)
    ekeys = sorted(entities.keys())
    for ekey in ekeys:
        for entity in entities[ekey]:
            if type(entity) != Planet:
                continue
            else:
                if entity.is_full() == True:
                    continue
                elif entity.owner == None or entity.owner == game_map.get_me():
                    return entity
                else:
                    continue

game = hlt.Game("Jan 6, 2018")
logging.info("Jan 6, 2018")

while True:
    turn_start = time.time()
    game_map = game.update_map()
    turn_setup()
