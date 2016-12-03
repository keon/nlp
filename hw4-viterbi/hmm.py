from state import State

class HMM:
    def __init__(self):
        self.states = []

    def generate(self, datasetName):
        with open(datasetName, 'r') as dataset:
            data = dataset.readlines()
            self.states = [State("START"), State("END")]
            currentIdx = 0
            for i, row in enumerate(data):
                if not i or data[i-1]=='':
                    curState = self.states[0]
                    curState.count += 1
                    state = 'START'
                row = row.rstrip('\n')
                previousIdx = currentIdx
                if row == '':
                    currentIdx = 1
                    curState = self.states[currentIdx]
                    state = 'END'
                else:
                    token, state = row.split('\t')
                # add current word to previous state
                preState = self.states[previousIdx]
                preState.transition[state] = preState.transition.get(state,0) + 1
                if state == 'END':
                    continue
                # add current word to current state
                flag = False
                length = len(self.states)
                for i in range(length):
                    curState = self.states[i]
                    if curState.state == state:
                        currentIdx = i
                        flag = True
                        curState.count += 1
                        curState.emission[token] = curState.emission.get(token,0) + 1
                if not flag:
                    curState = State(state)
                    curState.count += 1
                    currentIdx = length
                    curState.emission[token] = curState.emission.get(token,0) + 1
                    self.states.append(curState)


