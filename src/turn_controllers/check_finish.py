# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

import json
import datetime
import os
import random

def check_finish(main_game):
    # find the number of strategic nodes for each player    
    players_strategic_nodes_count = []
    for player in main_game.players.values():
        number_of_strategic_nodes = 0
        for node in player.nodes:
            if node.is_strategic:
                number_of_strategic_nodes += 1
        players_strategic_nodes_count.append(number_of_strategic_nodes)
        
    # check if the game is finished
    if main_game.turn_number >= int(main_game.config["number_of_turns"]):
        # check if there is a player with the most strategic nodes
        max_strategic_nodes = max(players_strategic_nodes_count)
        # if there is just one player with the most strategic nodes
        if players_strategic_nodes_count.count(max_strategic_nodes) == 1:
            if main_game.debug:
                main_game.print("player won because of having the most strategic nodes")
            game_finished(main_game, players_strategic_nodes_count.index(max_strategic_nodes))
            return 

        # find players with the most strategic nodes
        player = [main_game.players[i] for i in range(len(main_game.players)) if players_strategic_nodes_count[i] == max_strategic_nodes]


        # find the player with the most nodes
        number_of_nodes = []
        for player in players:
            number_of_nodes.append(len(player.nodes))
            
        # if there is just one player with the most nodes
        if number_of_nodes.count(max(number_of_nodes)) == 1:
            if main_game.debug:
                main_game.print("player won because of having the most nodes among players with the most strategic nodes")
            game_finished(main_game, number_of_nodes.index(max(number_of_nodes)))
            return 
        
        players = [players[i] for i in range(len(players)) if number_of_nodes[i] == max(number_of_nodes)]

        # find the player with the most troops
        players_troops_count = []
        for player in players:
            players_troops_count.append(sum([i.number_of_troops for i in player.nodes]))

        # if there is just one player with the most troops
        if players_troops_count.count(max(players_troops_count)) == 1:
            if main_game.debug:
                main_game.print("player won because of having the most troops among players with the most strategic nodes and normal nodes")
            game_finished(main_game, players_troops_count.index(max(players_troops_count)))
            return
        
        # choose a random player from the players with the most troops
        players = [players[i] for i in range(len(players)) if players_troops_count[i] == max(players_troops_count)]
        if main_game.debug:
            main_game.print("player won because of random choice")
        game_finished(main_game, random.choice(players).id)
        return

    # check if there is a player with enough strategic nodes to win    
    for i in range(len(players_strategic_nodes_count)):
        if players_strategic_nodes_count[i] >= int(main_game.config["number_of_strategic_nodes_to_win"]):
            if main_game.debug:
                main_game.print("player won because of having enough strategic nodes")
            game_finished(main_game, i)
            return

def game_finished(main_game, winner_id):
    # finish the game
    # make log folder if it does not exist
    if not os.path.exists("log"):
        os.makedirs("log")
    # generate and save the main_game.log file into a json file in the log folder
    with open("log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json", "w") as log_file:
        json.dump(main_game.log, log_file)
    
    # generate and save an export from main_game object and save in the result log folder 
    # generate export 
    export = dict()
    export['node_owners'] = [i.owner.id if i.owner != None else -1 for i in main_game.nodes.values()]
    export['troop_count'] = [i.number_of_troops for i in main_game.nodes.values()]
    export['turn_number'] = main_game.turn_number
    export['winner_id'] = winner_id
    # add the number of strategic nodes for each player
    for player in main_game.players.values():
        export['player'+str(player.id)+" strategic nodes"] = len([i for i in player.nodes if i.is_strategic]) 

    # make result_log folder if it does not exist
    if not os.path.exists("result_log"):
        os.makedirs("result_log")

    # save the export in the result log folder
    with open("result_log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json", "w") as result_log_file: 
        json.dump(export, result_log_file)


    # write debug_logs in the text file in the debug_log folder
    if main_game.debug:
        # make debug_log folder if it does not exist
        if not os.path.exists("debug_log"):
            os.makedirs("debug_log")
        with open("debug_log/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt", "w") as debug_log_file:
            debug_log_file.write(main_game.debug_logs)
    main_game.finish_func()
