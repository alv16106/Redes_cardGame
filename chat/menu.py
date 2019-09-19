options = {
  '/cr <name> <max_players>': 'Create Room',
  '/jr <room>': 'Join Room',
  '/whisper <user>': 'Send private message',
  '/kill <int>': 'Kill user, only available for mafia',
  '/execute <int>': 'Vote for the user to kill',
  '/rooms': 'Show all rooms,',
  '/h': 'Help'
}
NOT_FOUND = ' not found, please try again (/h for help on available commands)'


def showOptions(args=''):
    print('Commands')
    # Iterate over options
    for key, value in options.items():
        print(key + ': ' + value)
    print('\n')


def menu(functions):
    """ Show menu for the first time and update isFirst flag so that the menu
    knows further usages of showOptions are in a different term possition """
    print('\nGet ready to play MAFIA! You will need to choose a nickname,' +
          ' then join or create a room \n')
    print('Once you are in a room, you can chat with the other players but' +
          ' will have to wait for the room to reach the number of players' +
          ' defined by the creator \n')
    print('Once in a game you are asigned a role, good or evil. If you are' +
          ' evil you can vote for a person to die at night with your evil ' +
          'compatriots, else, you will vote at daytime for someone you ' +
          'suspect is evil to die. \n Village wins when there are no more ' +
          'evil oponents, evil wins when they overpower the villagers \n')
    input('Press any key to continue...')
    showOptions()
    isFirst = False
    functions['h'] = showOptions
    while True:
        # get input from user
        message = input(':')
        # see if it is a command. If not, send message to current conversation
        if message.startswith('/'):
            command = message.strip().split()[0][1:]
            # is in command list?
            if command in functions:
                arg = message[2 + len(command):]
                functions[command](arg)
            else:
                print('Command ' + command + NOT_FOUND)
        else:
            functions['send_message'](message)
