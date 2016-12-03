from hmm import *
from viterbi import *
from score import *

def main():
    hmm = HMM()
    hmm.generate('./data/WSJ_02-21.pos')
    # hmm.generate('./data/xaa.pos')
    V = Viterbi()
    V.run(hmm.states,'./data/WSJ_24.words', './data/WSJ_24_response.pos')
    score ('./data/WSJ_24.pos','./data/WSJ_24_response.pos')
    # V.viterbi(hmm.states,'./data/WSJ_23.words', './data/WSJ_23.pos')

if __name__ == "__main__":
    main()
