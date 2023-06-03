from languages import *
import datetime
def parse_user(user, lang):
    if lang == RU:
        message = f'Имя игрока: {user["personaname"]}\n'
        if "realname" in user:
            message += f'Настоящее имя: {user["realname"]}\n'
        if "loccountrycode" in user:
            message += f'Страна: {user["loccountrycode"]}\n'
        if "lastlogoff" in user:
            if user["personastate"] == 1:
                message += 'В сети\n'
            elif user["personastate"] >= 2:
                message += 'Нет на месте\n'
            else:
                message += f'Дата последнего выхода: {datetime.datetime.fromtimestamp(user["lastlogoff"]).strftime("%d-%m-%Y %H:%M:%S")}\n'
        if "timecreated" in user:
            message += f'Дата создания аккаунта: {datetime.datetime.fromtimestamp(user["timecreated"]).strftime("%d-%m-%Y %H:%M:%S")}\n'
        if "player_level" in user:
            message += f'Уровень игрока: {user["player_level"]}\n'
        if "owned_games" in user:
            message += f'Количество игр: {user["owned_games"]}\n'
        message += f'SteamID: {user["steamid"]}\n'
    elif lang == EN:
        message = f'Player name: {user["personaname"]}\n'
        if "realname" in user:
            message += f'Real name: {user["realname"]}\n'
        if "loccountrycode" in user:
            message += f'Country: {user["loccountrycode"]}\n'
        if "lastlogoff" in user:
            if user["personastate"] == 1:
                message += 'Online\n'
            elif user["personastate"] >= 2:
                message += 'AFK\n'
            else:
                message += f'Last logoff: {datetime.datetime.utcfromtimestamp(user["lastlogoff"] + 10800)}\n'
        if "timecreated" in user:
            message += f'Created account: {datetime.datetime.utcfromtimestamp(user["timecreated"] + 10800)}\n'
        if "player_level" in user:
            message += f'Player level: {user["player_level"]}\n'
        if "owned_games" in user:
            message += f'Number of games: {user["owned_games"]}\n'
        message += f'SteamID: {user["steamid"]}\n'
    return message, user['avatarfull']

def parse_game(game, lang):
    if lang == RU:
        message = f'Название игры: {game["name"]}\n'
        if game['price'] == -1:
            message += 'Не продаётся\n'
        elif game['price'] == 0:
            message += 'Бесплатно\n'
        else:
            message += f'Цена: {game["price"]}\n'
        if 'metacritic' in game:
            message += f'Оценка на Metacritic: {game["metacritic"]["score"]}\n'
        if "developers" in game:
            message += f'Разработчики: {", ".join(game["developers"])}\n'
        if "publishers" in game:
            message += f'Издатель: {", ".join(game["publishers"])}\n'
        if "required_age" in game:
            message += f'Требуемый возраст: {game["required_age"]}\n'
        if 'release_date' in game:
            if game['release_date']['coming_soon']:
                message += 'Игра в раннем доступе\n'
            message += f'Дата выхода: {game["release_date"]["date"]}\n'
    elif lang == EN:
        message = f'Game name: {game["name"]}\n'
        if game['price'] == -1:
            message += 'Free\n'
        elif game['price'] == 0:
            message += 'Free\n'
        else:
            message += f'Price: {game["price"]}\n'
        if 'metacritic' in game:
            message += f'Metacritic score: {game["metacritic"]["score"]}\n'
        if "developers" in game:
            message += f'Developers: {", ".join(game["developers"])}\n'
        if "publishers" in game:
            message += f'Publishers: {", ".join(game["publishers"])}\n'
        if "required_age" in game:
            message += f'Required age: {game["required_age"]}\n'
        if 'release_date' in game:
            if game['release_date']['coming_soon']:
                message += 'Coming soon\n'
            message += f'Release date: {game["release_date"]["date"]}\n'
    

    return message, game['header_image']