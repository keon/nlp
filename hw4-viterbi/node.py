class Node:
    def __init__(self, token, state = None, prob_word_tag = 1, p = 0, prev = None):
        self.token = token
        self.state = state
        self.p_wi_ti = prob_word_tag
        self.p = p
        self.prev = prev


