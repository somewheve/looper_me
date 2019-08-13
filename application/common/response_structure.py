import json


def true_return(msg='', data=''):
    return {
        'success': True,
        'msg': msg,
        'data': data
    }


def false_return(msg='', data=''):
    return {
        'success': False,
        'msg': msg,
        'data': data
    }
