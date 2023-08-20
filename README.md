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
| get_owners                  | GET  | your country's id (-1: isn't for you) | the get owners API |
| get_troops_count            | GET  | the number of troops in this node | the get troops count API |
| get_state                   | GET  | the current state of the game | the get state API |
| get_turn_number             | GET  | the number of the player whose turn it is | the get turn number API |
| [get_adj](#get_adj)         | GET  |
| next_state                  | GET  | the next state of the game | the next state API |
| put_one_troop               | POST | error or success message | the put one troop API |
| put_troop                   | POST | error or success message | the put troop API |
| get_player_id               | GET  | player id | the get player id API |
| attack                      | POST | error or success message | the attack API |
| move_troop                  | POST | error or success message | the move troop API |
| get_strategic_nodes         | GET  | strategic nodes's id | the get strategic nodes API |
| [get_number_of_troops_to_put](#get_number_of_troops_to_put) | GET  | the number of troops to put | the get number of troops to put API |


## APIs description

### / <a name="index"></a> (GET)

this is API is just for test if the server is running or not


output sample:
```json
{
    "message" : "Welcome, server is running"
}
```

-----------------------------------------------------
### get_adj <a name="get_adj"></a> (GET)

this API returns the list of the adjacent nodes of each node

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
### number_of_troops_to_put <a name="get_number_of_troops_to_put"></a> (GET)

this API returns the number of troops that you can put on the map

output sample:
```json
{
    "number_of_troops": 10
}
``` 
------------------------------------------------------


