import nltk
import string
from nltk.corpus import stopwords
from math import exp, expm1
import math

class Query:
  def __init__(self,ID,query):
    self.ID = ID
    self.query = query

  def __str__(self):
    return(self.ID, self.query)

  def tokenize(self):
    stopset = [word for word in stopwords.words('english')]
    stop_punc = list(string.punctuation)
    stops = stopset+stop_punc
    tokens = nltk.wordpunct_tokenize(self.query)
    tokens = [w for w in tokens if w.lower() not in stops ]
    filteredToks = []
    for token in tokens:
      if not (token.isdigit() or token[0] == "-" and token[1:].isdigit()):
        filteredToks.append(token)
    return filteredToks

