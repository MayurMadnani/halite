with open(REPLAY_FILE_PATH, 'rb') as game:
    game_data = game.read()
    game_data = zstd.decompress(game_data)
    game_json_data = json.loads(game_data.decode('utf-8'))
    for frame in game_json_data['frames'][1:300]:
        # destroyed planets, players, spawned players 
        events = frame['events']
        # every planet by id, docked ship(list of ids)
        # production remaining
        # health, owner, 
        planets = frame['planets']
        ships = frame['ships']
        for ship in ships:
            for shipid in ships[ship]:
                print(ships[ship][shipid])