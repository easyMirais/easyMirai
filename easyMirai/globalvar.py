uri: str = ""
botID: str = ""
key: str = ""
session: str = ""
isSlice: bool = False


class Uri:
    def set(self, value: str):
        global uri
        uri = value
        pass

    @property
    def get(self):
        global uri
        return uri


class BotID:
    def set(self, value: str):
        global botID
        botID = value
        pass

    @property
    def get(self):
        global botID
        return botID


class Key:
    def set(self, value: str):
        global key
        key = value
        pass

    @property
    def get(self):
        global key
        return key


class Session:
    def set(self, value: str):
        global session
        session = value
        pass

    @property
    def get(self):
        global session
        return session


class IsSlice:
    def set(self, value: bool):
        global isSlice
        isSlice = value
        pass

    @property
    def get(self):
        global isSlice
        return isSlice
