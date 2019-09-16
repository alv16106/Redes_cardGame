# Game workflow
# 1) get all the players
# 2) get all the players a role and number
# 3) start the game loop

#     game loop:
#         a)day 35 sec (all chat)
#         b)execute 15 sec (/execute 5)
#         c)night
#             good 35 + 15 sec (nothing)
#             evil 35 sec (private chat)
#                  15 sec (/kill 5)
import time
import cards

IN_GAME = 0
MAX_PLAYERS = 3
SIGN_IN_PLAYERS = []
ASSIGNED_PLAYERS = {}
VALID_ROLES = {
    'mafia': 'evil',
    'town': 'good'
}
VOTES = []


def get_players():
    # broadcast a msg now recieving subscriptions for the game
    print("Reciving players")
    # check if registered players equals the maximum stipulated start 
    if len(SIGN_IN_PLAYERS) == MAX_PLAYERS:
        # announce to the players that game is starting
        print("Game starting")
        return 1
    else:
        return 0


def player_roles():
    ROLED_PLAYERS = cards.generate_roles(SIGN_IN_PLAYERS, VALID_ROLES)
    # show each player its role
    for player in ROLED_PLAYERS:
        # data in player
        print(ROLED_PLAYERS[player]['name'])
        print(ROLED_PLAYERS[player]['role'])
        print(ROLED_PLAYERS[player]['status'])
    return 0


def game(current_stage='DAY'):
    if current_stage == 'DAY':
        # enable all chat

        print("DAY\n")
        time.sleep(35)
        # Change current_stage
        return 'EXECUTE'
    if current_stage == 'EXECUTE':
        # enable /execute option

        print("EXECUTE PHASE\n")
        print("type '/execute <number>' to vote\n")
        time.sleep(15)
        # execute a player
        user, votes = cards.select_user(ASSIGNED_PLAYERS, VOTES)
        print("USER: " + str(user) + " EXECUTED WITH IMPUNITY BY" + str(votes))
        # change the current player roster
        ASSIGNED_PLAYERS = cards.alter_user(ASSIGNED_PLAYERS, user, 0)
        VOTES = []
        # Change current stage
        return 'NIGHT'
    if current_stage == 'NIGHT':
        # enable /execute option

        print("NIGHT\n")
        print("type '/kill <number>' to vote\n")
        time.sleep(35)
        # kill a player
        user, votes = cards.select_user(ASSIGNED_PLAYERS, VOTES)
        print("USER: " + str(user) + " BUTCHERED BY EVIL\n")
        # change the current player roster
        ASSIGNED_PLAYERS = cards.alter_user(ASSIGNED_PLAYERS, user, 0)
        VOTES = []
        # Change current stage
        return 'DAY'


while IN_GAME == 0:
    time.sleep(5)
    SIGN_IN_PLAYERS.append('testplayer')
    IN_GAME = get_players()

# assign roles only once
ASSIGNED_PLAYERS = cards.generate_roles(SIGN_IN_PLAYERS, VALID_ROLES)
print(ASSIGNED_PLAYERS)
current_stage = 'EXECUTE'

while IN_GAME == 1:
    if cards.validate_game(ASSIGNED_PLAYERS) == 0:
        current_stage = game(current_stage)
    else:
        break
