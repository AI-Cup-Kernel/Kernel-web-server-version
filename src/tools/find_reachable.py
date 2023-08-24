ans = []
mark = []

def DFS(node_id, main_game, player_id):
    global ans
    global mark
    mark[node_id] = 1
    ans.append(node_id)
    for node in main_game.nodes[node_id].adj_main_map:
        if mark[node.id] == 0 and node.owner != None and node.owner.id == player_id:
            DFS(node.id, main_game, player_id)


def find_reachable(node_id, main_game):
    global ans
    global mark

    mark = [0 for i in range(len(main_game.nodes))]
    ans.clear()
    if main_game.nodes[node_id].owner == None:
        return ans
    DFS(node_id, main_game, main_game.nodes[node_id].owner.id)
    return ans 