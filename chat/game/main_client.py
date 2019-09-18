import time
import game.cards as cards


class Game:
    IN_GAME = 0
    MAX_PLAYERS = 0
    SIGN_IN_PLAYERS = []
    ASSIGNED_PLAYERS = {}
    VALID_ROLES = {}
    VOTES = []

    def __init__(self, max_players, v_roles, a_players, broadcast, private):
        self.MAX_PLAYERS = max_players
        self.VALID_ROLES = v_roles
        self.ASSIGNED_PLAYERS = a_players
        self.current_stage = "DAY"
        self.broadcast = broadcast
        self.private = private

    def run(self):
        self.current_stage = "DAY"
        while self.IN_GAME == 1:
            if cards.validate_game(self.ASSIGNED_PLAYERS) == 0:
                self.current_stage = self.game(self.current_stage)
            else:
                self.IN_GAME = 0
                winner = cards.winner_game(self.ASSIGNED_PLAYERS)
                self.broadcast('SERVER', 'El ganador es: \n' +
                               winner + '!! \n' +
                               'Do /restart to play again')

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

            self.broadcast('SERVER', 'Day time, you have 35 sec to discuss')
            time.sleep(35)
            # Change current_stage
            return 'EXECUTE'
        if current_stage == 'EXECUTE':
            # enable /execute option

            self.broadcast('SERVER', 'DISCUSSION IS OVER, EXECUTE VOTING TIME')
            alive_s, alive = cards.alive_users(self.ASSIGNED_PLAYERS)
            self.broadcast('SERVER', 'THIS PLAYERS ARE STILL ALIVE:\n' +
                           str(alive_s) +
                           " type '/execute <number>' to vote\n You have 15 sec")
            time.sleep(15)
            # execute a player
            user, votes = cards.select_user(self.ASSIGNED_PLAYERS, self.VOTES)
            self.broadcast('SERVER', "USER: " +
                           self.ASSIGNED_PLAYERS[user]['name'] +
                           " EXECUTED W/ IMPUNITY BY" + str(votes))
            self.private('SERVER', 'YOU ARE DEAD!', self.ASSIGNED_PLAYERS[user]['name'])

            # change the current player roster
            self.ASSIGNED_PLAYERS = cards.alter_user(
                self.ASSIGNED_PLAYERS, user, 0
                )
            self.VOTES = []
            # Change current stage
            return 'NIGHT'
        if current_stage == 'NIGHT':
            # enable /execute option

            self.broadcast('SERVER', 'NIGHT, MAFIA HAVE 35 sec TO KILL\n' +
                           "type '/kill <number>' to vote\n")
            alive_s, alive = cards.alive_users(self.ASSIGNED_PLAYERS)
            self.broadcast('SERVER', 'THIS PLAYERS ARE STILL ALIVE:\n' +
                           str(alive_s) +
                           " type '/execute <number>' to vote\n You have 15 sec")
            time.sleep(35)
            # kill a player
            user, votes = cards.select_user(self.ASSIGNED_PLAYERS, self.VOTES)
            self.broadcast('SERVER', "USER: " +
                           self.ASSIGNED_PLAYERS[user]['name'] +
                           " BUTCHERED BY EVIL\n")
            self.private('SERVER', 'YOU ARE DEAD!', self.ASSIGNED_PLAYERS[user]['name'])
            # change the current player roster
            self.ASSIGNED_PLAYERS = cards.alter_user(
                self.ASSIGNED_PLAYERS, user, 0
                )
            self.VOTES = []
            # Change current stage
            return 'DAY'


""" # los bois que se registarton
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
print(servercito.ASSIGNED_PLAYERS) """

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
