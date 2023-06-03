from steam import Steam
from decouple import config
import json

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

def search_user_by_name(name):
    user = steam.users.search_user(name)
    if user != 'No match':
        return extension(user['player'])
    else:
        return 0
def search_user_by_id(name):
    user = steam.users.get_user_details(name)
    if user != 'No match':
        return extension(user['player'])
    else:
        return 0
    
def search_user(name):
    if search_user_by_name(name):
        return search_user_by_name(name)
    elif name.isdigit() and search_user_by_id(name):
        return search_user_by_id(name)
    else:
        return 0
    
def extension(user):
    temp = steam.users.get_user_steam_level(user['steamid'])
    
    if temp:
        user['player_level'] = str(temp['player_level'])
    temp = steam.users.get_owned_games(user['steamid'])
    if temp:
        user['owned_games'] = temp['game_count']
    return user

def search_game(name):
    return steam.apps.search_games(name)['apps'][:5]

def get_game(game):
    game = game.split()
    id = game[0]
    if len(game) == 1:
        price = -1
    elif len(game) == 2:
        price = game[1]
    else:
        price = 0
    game = steam.apps.get_app_details(id)
    game = json.loads(game)
    if game[str(id)]['success']:
        game = game[str(id)]['data']
        game["price"] = price
        return game
    else:
        return -1