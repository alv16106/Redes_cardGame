
import time
import cards


class Server:
    IN_GAME = 0
    MAX_PLAYERS = 0
    SIGN_IN_PLAYERS = []
    ASSIGNED_PLAYERS = {}
    VALID_ROLES = {}
    VOTES = []

    def __init__(self, max_players, valid_roles, assigned_players):
        self.MAX_PLAYERS = max_players
        self.VALID_ROLES = valid_roles
        self.ASSIGNED_PLAYERS = assigned_players

    def get_players(self):
        # broadcast a msg now recieving subscriptions for the game
        print("Reciving players")
        # check if registered players equals the maximum stipulated strt
        if len(self.SIGN_IN_PLAYERS) == self.MAX_PLAYERS:
            # announce to the players that game is starting
            print("Game starting")
            return 1
        else:
            return 0

    def player_roles(self):
        self.ROLED_PLAYERS = cards.generate_roles(
            self.SIGN_IN_PLAYERS, self.VALID_ROLES
            )
        # show each player its role
        for player in self.ROLED_PLAYERS:
            # data in player
            print(self.ROLED_PLAYERS[player]['name'])
            print(self.ROLED_PLAYERS[player]['role'])
            print(self.ROLED_PLAYERS[player]['status'])
        return 0

    def game(self, current_stage='DAY'):
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
            user, votes = cards.select_user(self.ASSIGNED_PLAYERS, self.VOTES)
            print(
                "USER: " + str(user) + " EXECUTED W/ IMPUNITY BY" + str(votes)
                )
            # change the current player roster
            self.ASSIGNED_PLAYERS = cards.alter_user(
                self.ASSIGNED_PLAYERS, user, 0
                )
            self.VOTES = []
            # Change current stage
            return 'NIGHT'
        if current_stage == 'NIGHT':
            # enable /execute option

            print("NIGHT\n")
            print("type '/kill <number>' to vote\n")
            time.sleep(35)
            # kill a player
            user, votes = cards.select_user(self.ASSIGNED_PLAYERS, self.VOTES)
            print("USER: " + str(user) + " BUTCHERED BY EVIL\n")
            # change the current player roster
            self.ASSIGNED_PLAYERS = cards.alter_user(
                self.ASSIGNED_PLAYERS, user, 0
                )
            self.VOTES = []
            # Change current stage
            return 'DAY'


# los bois que se registarton
temproles = {'mafia': 'evil', 'town': 'good'}
test = ['a', 'b', 'c']
theboys = cards.generate_roles(test, temproles)

servercito = Server(3, temproles, theboys)
print(servercito.ASSIGNED_PLAYERS)

# probar a ver si truena
false_votes = [0, 0, 1]
servercito.VOTES = false_votes
servercito.game('EXECUTE')

# probar a ver si funciono
print(servercito.ASSIGNED_PLAYERS)

# while IN_GAME == 0:
#     time.sleep(5)
#     SIGN_IN_PLAYERS.append('testplayer')
#     IN_GAME = get_players()

# # assign roles only once
# ASSIGNED_PLAYERS = cards.generate_roles(SIGN_IN_PLAYERS, VALID_ROLES)
# print(ASSIGNED_PLAYERS)
# current_stage = 'EXECUTE'

# while IN_GAME == 1:
#     if cards.validate_game(ASSIGNED_PLAYERS) == 0:
#         current_stage = game(current_stage)
#     else:
#         break
