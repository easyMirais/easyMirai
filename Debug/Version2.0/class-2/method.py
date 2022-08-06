class Init:
    def __init__(self):
        self.Qid = None

    def send(self, Qid):
        return mode(Qid)


class mode:
    def __init__(self, Qid):
        self.Qid = Qid

    def text(self, text):
        return types(text, self.Qid)


class types:
    def __init__(self, context, Qid):
        self.Qid = Qid
        self.content = context

    @property
    def friend(self):
        print(self.content, self.Qid)
        return "mian"
