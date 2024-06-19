class SessionID:
    def __init__(self, host):
        self.host = host

    def __str__(self):
        return str(self.host).replace(":", ".")
