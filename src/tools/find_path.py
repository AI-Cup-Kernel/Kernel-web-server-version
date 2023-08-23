mark = []

def DFS(u, v, main_game, player_id):
    global mark
    mark[u] = 1
    if u == v:
        return True, [v]
    path = []
    for node in main_game.nodes[u].adj_main_map:
        if mark[node.id] == 0 and node.owner != None and node.owner.id == player_id:
            res, path = DFS(node.id, v, main_game, player_id)
            if res:
                path = [u] + path
                return True, path
    return False, []
                


def find_path(u, v, main_game, player_id):
    global mark
    # find a path from node u to node v that all the nodes in the path are owned by the player
    # return the path as a list of nodes
    # if there is no path return None
    mark = [0 for i in range(len(main_game.nodes))]
    return DFS(u, v, main_game, player_id)
    

    

