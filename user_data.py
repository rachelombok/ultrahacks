class UserData:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def muted_words(self):
        if "muted_words" in self.data:
            return self.data['muted_words']
        else:
            return None

    def last_checked_message(self):
        if "last_checked" in self.data:
            return self.data['last_checked']
        else:
            return None