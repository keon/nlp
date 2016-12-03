class State:
    def __init__(self, state):
        self.state = state
        self.count = 0
        self.transition = {}
        self.emission = {}
