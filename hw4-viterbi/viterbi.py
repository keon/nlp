from node import Node
import re
import sys
import math

class Viterbi:

    def makeNode(self, states, word, curNodes, tags):
        for s in states:
            if s.state in tags:
                curNode = Node(word,s,1/float(s.count))
                curNodes.append(curNode)

    def get_distribution(self, states, words, i, curNodes, first):
        if first:
            if re.search('\d', words[i]):
                self.makeNode(states, words[i], curNodes, ['CD'])
            elif re.match(r'\w+\-\w+', words[i]):
                self.makeNode(states,words[i],curNodes,['JJ','NNP'])
            elif words[i].isupper():
                if words[i][-1] == 'S':
                    self.makeNode(states,words[i],curNodes,['NNPS'])
                else:
                    self.makeNode(states,words[i],curNodes,['NNP'])
            elif words[i][0].isupper():
                if not i or words[i-1] == '':
                    word = words[i]
                    word = word.lower()
                    for s in states:
                        num = s.emission.get(word,0)
                        if num:
                            curNode = Node(words[i],s,num/float(s.count))
                            curNodes.append(curNode)
                if not len(curNodes):
                    if words[i][-1] == 's':
                        self.makeNode(states,words[i],curNodes,['NNPS'])
                    else:
                        self.makeNode(states,words[i],curNodes,['NNP'])
            elif len(words[i])>2 and words[-2:]=='ly':
                self.makeNode(states,words[i],curNodes,['RB'])
            else:
                for j in range(2,len(states)):
                    s = states[j]
                    if re.match(r'[A-Z\$]+',s.state):
                        curNode = Node(words[i],s,1/float(s.count))
                        curNodes.append(curNode)
        else:
            for j in range(2,len(states)):
                s = states[j]
                if re.match(r'[A-Z\$]+',s.state):
                    curNode = Node(words[i],s,1/float(s.count))
                    curNodes.append(curNode)

    def get_transition(self, prevNodes, curNodes):
        temp_nodes = []
        for curNode in curNodes:
            curState = curNode.state
            max_prob, best_prev = -sys.maxsize, None
            if len(prevNodes)>=1:
                for prevNode in prevNodes:
                    prevState = prevNode.state
                    p_ti_t_pre = prevState.transition.get(curState.state, 0) / float(prevState.count)
                    if p_ti_t_pre:
                        p = math.log10(prevNode.p_wi_ti) + math.log10(p_ti_t_pre) + prevNode.p
                        if p > max_prob:
                            max_prob = p
                            best_prev = prevNode
                curNode.prev = best_prev
                curNode.p = max_prob
            if curNode.prev:
                temp_nodes.append(curNode)
        curNodes = temp_nodes
        return curNodes

    def run(self, states, wordsFileName, responseFileName=None):
        with open(wordsFileName, 'r') as wordsFile, \
                open(responseFileName, 'w') as responseFile:
            words = wordsFile.readlines()
            curNodes = []
            for i in range(len(words)):
                if not i or words[i-1]=='':
                    curNode = Node('', states[0], 1, 1)
                    curNodes = [curNode]
                prevNodes = curNodes
                curNodes = []
                words[i] = words[i].rstrip('\n')
                if words[i] == '':
                    curNode = Node('',states[1], 1)
                    curNodes.append(curNode)
                else:
                    for s in states:
                        num = s.emission.get(words[i],0)
                        if num:
                            curNode = Node(words[i],s,num/float(s.count))
                            curNodes.append(curNode)
                if not len(curNodes):
                    self.get_distribution(states, words, i, curNodes, True)
                curNodes = self.get_transition(prevNodes, curNodes)
                if not len(curNodes):
                    self.get_distribution(states, words, i, curNodes, False)
                curNodes = self.get_transition(prevNodes, curNodes)
                if words[i] == '' and len(curNodes):
                    curNode = curNodes[0]
                    sentences = []
                    while curNode:
                        curState = curNode.state
                        if curState.state not in ['START', 'END']:
                            string = curNode.token+'\t'+curState.state+'\n'
                            sentences.append(string)
                        curNode = curNode.prev
                    for string in sentences[::-1]:
                        responseFile.write(string)
                    responseFile.write('\n')

