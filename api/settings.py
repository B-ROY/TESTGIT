#coding=utf-8
import os

def load_settings(settings, debug=True, **kwargs):
    pass
def check_settings(settings):
    pass

# before   0f85eb25881ddd5c31f715542ae856c3

cookie_secret = 'a3643412085026643529f7fe032646c8'

def load_tonardo_settings(tonardo_settings={}):
    tonardo_settings.update({
            'cookie_secret': cookie_secret,
    })

