import hlt, logging, time, math
from hlt.entity import Ship, Planet, Position
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
                    return movement(actor, waypoint(actor, entity), game_map)
            elif type(entity) == Planet and entity.owner != None and entity.owner != game_map.get_me():
                continue
            elif type(entity) == Planet:
                return movement(actor, waypoint(actor, entity), game_map)
            else:
                return movement(actor, waypoint(actor, entity), game_map)

def waypoint(mover, target):
    distance = min(hlt.constants.MAX_SPEED, mover.calculate_distance_between(mover.closest_point_to(target)))
    angle = mover.calculate_angle_between(mover.closest_point_to(target))
    pos_x = math.cos(math.radians(angle)) * distance
    pos_y = math.sin(math.radians(angle)) * distance
    test_pos = Position(mover.x + pos_x, mover.y + pos_y)
    return test_pos

def combat(warrior):
    bogie = closest_enemy(warrior)
    wingman = closest_ally(warrior)
    squadron = len([ship for ship in game_map._all_ships() if ship.owner == game_map.get_me() and ship.calculate_distance_between(warrior) < 7])
    if squadron > 4:
        return movement(warrior, warrior.closest_point_to(bogie), game_map)
    if type(wingman) == Ship:
        if wingman.calculate_distance_between(bogie) > 5:
            return movement(warrior, warrior.closest_point_to(wingman), game_map)
        else:
            return movement(warrior, warrior.closest_point_to(bogie), game_map)
    else:
        return movement(warrior, warrior.closest_point_to(bogie), game_map)

def turn_setup():
    command_queue = []
    my_ships = [ship for ship in game_map.get_me().all_ships() if ship.docking_status == Ship.DockingStatus.UNDOCKED]
    for ship in my_ships:
        command_hold = get_command(ship)
        if command_hold != None:
            command_queue.append(command_hold)
    logging.info("Turn Time = " + str(time.time() - turn_start))
    game.send_command_queue(command_queue)

def movement(mover, target, game_map, speed = hlt.constants.MAX_SPEED, avoid_obstacles=True, max_corrections=90, angular_step=1,
             ignore_ships=False, ignore_planets=False):
    new_step = angular_step
    if max_corrections <= 0:
        return None
    if max_corrections < 90:
        if angular_step > 0:
            new_step = angular_step * (-1)
        elif angular_step < 0:
            new_step = angular_step * (-1) + 1
    distance = mover.calculate_distance_between(target)
    angle = mover.calculate_angle_between(target)
    ignore = () if not (ignore_ships or ignore_planets) \
        else Ship if (ignore_ships and not ignore_planets) \
        else Planet if (ignore_planets and not ignore_ships) \
        else Entity
    if avoid_obstacles and game_map.obstacles_between(mover, target, ignore):
        for obstacle in game_map.obstacles_between(mover, target, ignore):
            if mover.calculate_angle_between(target) < mover.calculate_angle_between(obstacle):
                new_target_dx = math.cos(math.radians(angle + angular_step)) * distance
                new_target_dy = math.sin(math.radians(angle + angular_step)) * distance
                new_target = Position(mover.x + new_target_dx, mover.y + new_target_dy)
                return movement(mover, new_target, game_map, speed, True, max_corrections - 1, angular_step = new_step)
            else:
                new_target_dx = math.cos(math.radians(angle - angular_step)) * distance
                new_target_dy = math.sin(math.radians(angle - angular_step)) * distance
                new_target = Position(mover.x + new_target_dx, mover.y + new_target_dy)
                return movement(mover, new_target, game_map, speed, True, max_corrections - 1, angular_step = new_step)
    speed = speed if (distance >= speed) else distance
    return mover.thrust(speed, angle)

"""
def movement(mover, target, game_map, speed = hlt.constants.MAX_SPEED, avoid_obstacles=True, max_corrections=90, angular_step=6,
             ignore_ships=False, ignore_planets=False):
    new_step = angular_step
    if max_corrections <= 0:
        return None
    if max_corrections < 90:
        if angular_step > 0:
            new_step = angular_step * (-1)
        elif angular_step < 0:
            new_step = angular_step * (-1) + 6
    distance = mover.calculate_distance_between(target)
    angle = mover.calculate_angle_between(target)
    ignore = () if not (ignore_ships or ignore_planets) \
        else Ship if (ignore_ships and not ignore_planets) \
        else Planet if (ignore_planets and not ignore_ships) \
        else Entity
    if avoid_obstacles and game_map.obstacles_between(mover, target, ignore):
        new_target_dx = math.cos(math.radians(angle + angular_step)) * distance
        new_target_dy = math.sin(math.radians(angle + angular_step)) * distance
        new_target = Position(mover.x + new_target_dx, mover.y + new_target_dy)
        return movement(mover, new_target, game_map, speed, True, max_corrections - 1, angular_step = new_step)
    speed = speed if (distance >= speed) else distance
    return mover.thrust(speed, angle)
"""

def closest_enemy(warrior):
    entity_list = game_map.nearby_entities_by_distance(warrior)
    ekeys = sorted(entity_list.keys())
    for ekey in ekeys:
        for entity in entity_list[ekey]:
            if type(entity) != Ship or entity.owner == game_map.get_me():
                continue
            else:
                return entity

def closest_ally(warrior):
    entity_list = game_map.nearby_entities_by_distance(warrior)
    ekeys = sorted(entity_list.keys())
    for ekey in ekeys:
        for entity in entity_list[ekey]:
            if type(entity) != Ship or entity.owner != game_map.get_me():
                continue
            else:
                return entity

game = hlt.Game("Demitroy Upload")
logging.info("Demitroy Upload")

while True:
    turn_start = time.time()
    game_map = game.update_map()
    turn_setup()
