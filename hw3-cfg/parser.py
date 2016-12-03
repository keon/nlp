from nltk import pos_tag, word_tokenize, CFG
import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> DT NG
NP -> NNS
NG -> JJ NG
NG -> NN
NG -> NNS
NG -> NN NN
VP -> VBP PP
NP -> NP PP
PP -> IN NP
DT -> "Any"
DT -> "the"
JJ -> "habitable"
NNS -> "areas"
NN -> "border"
NN -> "region"
IN -> "in"
VPB -> "are"
""")

# NNS -> 'areas' | 'Scientists'
# DT -> 'Any' | 'any'
# JJ -> 'habitable'
# DT -> 'the'
# NN -> 'border' | 'planet' | 'region'
# IN -> 'in' | 'that' | 'on'
# VPB -> 'are' | 'think'


# S -> NP VP
# VP -> VBP SBAR
# SBAR -> IN S
# NP -> NP PP
# NP -> DT NG
# NP -> NNS | NN
# NP -> DT JJ NNS PP
# NG -> JJ NG
# NG -> NNS | NN
# NG -> NN NN
# VP -> VBP PP
# PP -> IN NP

sent = "Any habitable areas are in the border region".split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
    print(tree)