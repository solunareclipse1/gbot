class player(object):
    def __init__(self):
        ## Player variables, exposed to bot
        self.queue = []
        self.connectedChannel = None
        self.nowPlaying = None