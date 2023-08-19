def calculate_number_of_troops(player_id, main_game):
    # calculate the number of troops to give a player at the beginning of a turn
    number_of_nodes = len(main_game.player_turn.nodes)
    score_of_strategic_nodes = sum([i.score_of_strategic for i in main_game.player_turn.nodes if i.is_strategic])
    return (number_of_nodes-9) // 3 + score_of_strategic_nodes
