# Kernel-web-server-version
AI-Cup kernel that communicate with client with Rest API 
## Description
This is a web game where artificial intelligence programmers can participate and compete with each other by writing code for robots that try to win. The game is based on the Risk and the objective is to create the best robot possible to win against other players.
## Requirements
To participate in this game, you need to install Flask, requests and jwt, which is as follows:
```markdown
pip install -r requirements.txt
```

## How to run

to run server you just need to run the ```run.py``` file

## List of APIs
| API                         | Type |
| :-:                         | :-:  |
| [/](#index)               | GET  |
| [get_owners](#get_owners)                  | GET  | your nodes id (-1: isn't for you) | the get owners API |
| [get_troops_count](#get_troops_count)            | GET  | the number of troops in this node | the get troops count API |
| [get_state](#get_state)                   | GET  | the current state of the game | the get state API |
| [get_turn_number](#get_turn_number)             | GET  | the number of the player whose turn it is | the get turn number API |
| [get_adj](#get_adj)         | GET  | all adjacent nodes for each node | the get adjacent API |
| [next_state](#next_state)                  | GET  | the next state of the game | the next state API |
| [put_one_troop](#put_one_troop) | POST | error or success message| the put one troop API |
| [put_troop](#put_troop)     | POST | error or success message | the put troop API |
| [get_player_id](#get_player_id)               | GET  | player id | the get player id API |
| [attack](#attack)              | POST | error or success message | the attack API |
| [move_troop](#move_troop) | POST | error or success message | the move troop API |
| [get_strategic_nodes](#get_strategic_nodes)         | GET  | strategic nodes id | the get strategic nodes API |
| [get_number_of_troops_to_put](#get_number_of_troops_to_put) | GET  | the number of troops to put | the get number of troops to put API |
| [get_reachable](#get_reachable)               | GET | nodes to which the owner can transfer troops from id_node | the get reachable API |
| [fort](#fort) | POST|

## APIs description

### /get_owners <a name="get_owners"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /get_troops_count <a name="get_troops_count"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /get_state <a name="get_state"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /get_turn_number <a name="get_turn_number"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### / <a name="index"></a>
#### (GET)

this is API is just for test if the server is running or not


output sample:
```json
{
    "message" : "Welcome, server is running"
}
```

-----------------------------------------------------
### /get_adj <a name="get_adj"></a>
#### (GET)

this API returns the list of adjacent nodes for each node

output sample:
```json
{
    "1": [2, 3, 4],
    "2": [1, 3],
    "3": [1, 2, 4],
    "4": [1, 3, 5],
    "5": [4]
}

```
-----------------------------------------------------
### /next_state <a name="next_state"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /get_number_of_troops_to_put <a name="get_number_of_troops_to_put"></a> 
#### (GET)

this API returns the number of troops that you can put on the map

output sample:
```json
{
    "number_of_troops": 10
}
``` 
------------------------------------------------------
### /put_one_troop <a name="put_one_troop"></a>
#### (POST)

at the beginning the game gives you some troops to put on the map, players can put one troop in each turn this is the init state of the game 

input sample:
```json
{
    "node_id": 1
}
```

output sample1:
```json
{
    "message":"troop added successfully"
}
```

output sample2:
```json
{
    "error":"You can not put more than one troop in a turn"
}
```
------------------------------------------------------
### /put_troop <a name="put_troop"></a>
#### (POST)

at the beginning of each turn you can put some troops on the map, you can use this API to choose the node that you want to put your troops and the number of troops that you want to put on that node

input sample:
```json
{
    "node_id": 1,
    "number_of_troops": 2
}
```

output sample1:
```json
{
    "message":"troop added successfully"
}
```

output sample2:
```json
{
    "error":"This node is already owned by another player"
}
```

------------------------------------------------------
### /get_player_id <a name="get_player_id"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /attack <a name="attack"></a>
#### (POST)

you can use this API to attack a node with your node 

input sample:
```json
{
    "attacking_id": 1,
    "target_id": 2,
    "fraction": 0.5
}
```
rules: 
    - the attacking_id node must be adjacent to the target_id node
    - the attacking_id node must be owned by you
    - the target_id node must be owned by another player

output sample1:
```json
{
    "message":"attack is successful"
}
```

output sample2:
```json
{
    "error":"fraction is not provided"
}
```

------------------------------------------------------
### /move_troop <a name="move_troop"></a>
#### (POST)

you can use this API to move your troops from one node to another node 

input sample:
```json
{
    "source": 1,
    "destination": 2,
    "troop_count": 2
}
```
rules: 
    - between source and destination nodes must be a path that you own all of the nodes in that path
    - the source node must have enough troops to move 
    - at least one troop must stay in the source node
    - you should own both of the source and destination nodes
    - you can just move your troops once in each turn

output sample1:
```json
{
    "message":"troops moved successfully"
}
```

output sample2:
```json
{
    "error":"troop_count is not provided"
}
```
------------------------------------------------------
### /get_strategic_nodes <a name="get_strategic_nodes"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /get_reachable <a name="get_reachable"></a>
#### (GET)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
### /fort <a name="fort"></a>
#### (POST)

this API returns 

input sample:
```json
{

}
```

output sample:
```json
{

}

```
-----------------------------------------------------
