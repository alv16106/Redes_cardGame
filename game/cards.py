import numpy

# normal distribution for good and evil players 2 to 1


# users: list of players
# roles: dict of roles with alignment
def generate_roles(users, roles, ratio=2):
    ready_players = []
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
            ready_players.append([player, evil_roles[0]])
            evil -= 1
        elif player_type == 0 and evil == 0:
            ready_players.append([player, good_roles[0]])
            good -= 1
        elif player_type == 1 and good > 0:
            ready_players.append([player, good_roles[0]])
            good -= 1
        elif player_type == 1 and good == 0:
            ready_players.append([player, evil_roles[0]])
            evil -= 1

    return ready_players


users = ['a', 'b', 'c', 'd', 'e']

roles = {
    'mafia': 'evil',
    'town': 'good'
}

print(generate_roles(users, roles))
