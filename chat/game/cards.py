import numpy
# normal distribution for good and evil players 2 to 1


# users: list of players
# roles: dict of roles with alignment
def generate_roles(users, roles, ratio=2):
    ready_players = {}
    player_no = 0
    # generate the number of each player based on player qty
    evil = int(len(users) / ratio)
    good = len(users) - evil
    # filter by good and evil roles
    good_roles = []
    evil_roles = []

    for role in roles:
        if roles[role] == 'evil':
            evil_roles.append(role)
        elif roles[role] == 'good':
            good_roles.append(role)

    # assign each player a role
    probability = 1 / (ratio + 1)
    for player in users:
        rdm_prob = numpy.random.uniform()
        player_type = 0
        if rdm_prob <= probability:
            player_type = 0
        else:
            player_type = 1

        if player_type == 0 and evil > 0:
            ready_players[player_no] = {
                'name': player,
                'role': evil_roles[0],
                'status': 1
            }
            player_no += 1

            evil -= 1
        elif player_type == 0 and evil == 0:
            ready_players[player_no] = {
                'name': player,
                'role': good_roles[0],
                'status': 1
            }
            player_no += 1
            good -= 1
        elif player_type == 1 and good > 0:
            ready_players[player_no] = {
                'name': player,
                'role': good_roles[0],
                'status': 1
            }
            player_no += 1
            good -= 1
        elif player_type == 1 and good == 0:
            ready_players[player_no] = {
                'name': player,
                'role': evil_roles[0],
                'status': 1
            }
            player_no += 1
            evil -= 1

    return ready_players


# VALIDATE IF THE VOTES (LIST) EXIST IN USERS (DICT)
def validate_votes(users, votes):
    voted_users = []
    for vote in votes:
        for user in users:
            if user == vote:
                voted_users.append(vote)
    return voted_users


# ALTER A USER (INT) STATUS (INT) IN USERS (DICT)
def alter_user(users, user, status):
    if user in users:
        users[user]['status'] = status
        return users
    else:
        print('user not found')
        return users


# GET HIGHEST VOTED USER IN ALL USERS (DICT) VOTES (LIST)
def select_user(users, votes):
    # get votes in existing users
    voted_users = validate_votes(users, votes)
    votes_p_user = {}
    for vote in voted_users:
        if vote not in voted_users:
            votes_p_user[vote] = 0
        elif vote not in votes_p_user:
            votes_p_user[vote] = 1
        else:
            votes_p_user[vote] += 1
    # search for higest
    highest = 0
    h_user = ''
    for user in votes_p_user:
        if votes_p_user[user] >= highest:
            highest = votes_p_user[user]
            h_user = user

    return (h_user, highest)


# VALIDATE A GAME IF 1 GAME WON BY A SIDE ELSE 0
def validate_game(users):
    good = 0
    evil = 0
    for user in users:
        if users[user]['role'] == 'mafia' and users[user]['status'] == 1:
            evil += 1
        if users[user]['role'] == 'town' and users[user]['status'] == 1:
            good += 1

    if good == 0 or evil == 0:
        return 1
    return 0


# GENERATE THE WINNER WINNER CHICKEN DINNER TEAM
def winner_game(users):
    good = 0
    evil = 0
    for user in users:
        if users[user]['role'] == 'mafia' and users[user]['status'] == 1:
            evil += 1
        if users[user]['role'] == 'town' and users[user]['status'] == 1:
            good += 1

    if good == 0:
        return 'evil'
    elif evil == 0:
        return 'good'
    return 'no winner'


# GET THE USERS (LIST) THAT ARE ALIVE FROM PLAYERS(DICT)
def alive_users(users):
    alive_users = []
    for user in users:
        if users[user]['status'] == 1:
            alive_users.append(users[user]['name']) 

    return alive_users


# data for testing

# users = ['a', 'b', 'c', 'd', 'e']

# roles = {
#     'mafia': 'evil',
#     'town': 'good'
# }

# print(generate_roles(users, roles))

# test_users = generate_roles(users, roles)
# test_votes = [0, 0, 1, 0, 7]
# test_users = alter_user(test_users, 0, 0)

# print(alive_users(test_users))