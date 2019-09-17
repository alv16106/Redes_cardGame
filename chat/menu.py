options = {
  '/cr': 'Create Room',
  '/jr': 'Join Room',
  '/whisper': 'Send private message',
  '/kill': 'Kill user, only available for mafia',
  '/execute': 'Vote for the user to kill',
  '/h': 'Help'
}
NOT_FOUND = ' not found, please try again (/h for help on available commands)'


def showOptions(args=''):
    print('Commands')
    # Iterate over options
    for key, value in options.items():
        print(key + ': ' + value)


def menu(functions):
    """ Show menu for the first time and update isFirst flag so that the menu
    knows further usages of showOptions are in a different term possition """
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
