import json


def create_msg(sender, body):
    m = {}
    m['code'] = 1
    m['payload'] = {'from': sender, 'body': body}
    return m
