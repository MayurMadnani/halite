import hlt
from collections import OrderedDict
game = hlt.Game("MyBot-Python")
chooseClosest = False
largestPlanet=None
while True:
    game_map = game.update_map()
    command_queue = []
    team_ships = game_map.get_me().all_ships()
    lookedup_planets=[]
    for shipid,ship in enumerate(game_map.get_me().all_ships()):
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned() and entities_by_distance[distance][0] not in lookedup_planets]
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]
        if not chooseClosest:
            if largestPlanet is None:
                largestPlanet = max(closest_empty_planets, key=lambda planet: planet.radius)
        # If there are any empty planets, let's try to mine!
        if len(closest_empty_planets) > 0:
            #added randomness for planet
            target_planet = closest_empty_planets[0] if chooseClosest else largestPlanet
            lookedup_planets.append(target_planet)
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigate_command = team_ships[shipid].navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False,
                            ignore_planets=False)
                if navigate_command:
                    command_queue.append(navigate_command)

        # FIND SHIP TO ATTACK!
        elif len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = team_ships[shipid].navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED))
            if navigate_command:
                command_queue.append(navigate_command)
    game.send_command_queue(command_queue)
    chooseClosest = True
    # TURN END
# GAME END
