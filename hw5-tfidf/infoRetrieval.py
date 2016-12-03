import nltk
import string
from nltk.corpus import stopwords
from math import exp, expm1
import math
from query import Query

def parseQuery(filename):
  with open(filename,"r") as f:
    IDS, queries, WS = [], [], []
    new_queries = []
    query_docs = []
    cont = False
    string = ""
    for line in f:
      #print(line)
      if ".I" in line:
        cont = False
        if len(string) > 0:
          queries.append(string)
        string = ""
        part = line.split()
        IDS.append(part[1])
      if ".W" in line:
        cont = True
      if cont == True:
        string = string + line
    if len(string) > 0 :
      queries.append(string)
    for query in queries:
      query = query[2:]
      new_queries.append(query)
    length = len(IDS)
    for count in range(length):
      I = IDS[count]
      qu = new_queries[count]
      query_docs.append(Query(I,qu))
    f.close()
    return query_docs

def parseAbsDocs(filename):
  with open(filename,"r") as f:
    abstracts = []
    string = ""
    cont = False
    for line in f:
      if ".I" in line:
        cont = False
        if len(string)>0:
          abstracts.append(string)
          string = ""
      if ".W" in line:
        cont = True
      if cont == True:
        string = string + line
    if len(string)>0:
      abstracts.append(string)
    new_abstracts = []
    for abst in abstracts:
      abst = abst[2:]
      new_abstracts.append(abst)
    f.close()
    return new_abstracts

def tokenize(docs, docType="query"):
  if docType == "query":
    qToks = []
    for query in docs:
      qToks.append(query.tokenize())
    return qToks
  else:
    absToks = []
    for abstract in docs:
      sentences = nltk.sent_tokenize(abstract)
      toks = []
      for sentence in sentences:
        stopset = [word for word in stopwords.words('english')]
        stop_punc = list(string.punctuation)
        stops = stopset+stop_punc
        tokens = nltk.wordpunct_tokenize(sentence)
        tokens = [w for w in tokens if w.lower() not in stops ]
        filtered_tokens = [x for x in tokens if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
        toks.append(filtered_tokens)
      absToks.append(toks)
    return absToks

def organize(tokens, docType):
  numDocs = len(tokens)
  dic = {}
  count = 0
  for doc in tokens:
    if docType == "query":
      for tok in doc:
        if tok not in dic:
          dic[tok] = [0]*numDocs
          dic[tok][count] = 1
        else:
          dic[tok][count] = dic[tok][count] +1
    if docType == "abstract":
      for sentence in doc:
        for tok in sentence:
          if tok not in dic:
            dic[tok] = [0]* numDocs
            dic[tok][count] = 1
          else:
            dic[tok][count] = dic[tok][count] + 1
    count = count + 1
  return dic

def tfidf(sentence, tfDic, idfDic):
  vector = []
  for token in sentence:
    tf = tfDic.get(token, 0)
    idf = idfDic.get(token, 0)
    vector.append(float(tf*idf))
  return vector

def idf(qDic,totalDocs):
  dic = {}
  for key in qDic:
    numDocs = 0
    for count in qDic[key]:
      if count > 0:
        numDocs = numDocs + 1
    dic[key] = math.log(float(totalDocs) / float(numDocs))
  return dic

def abstractTf(absDic, totalDocs):
  absTf = []
  for count in range(totalDocs):
    dic = {}
    for key in absDic:
      term = absDic[key][count]
      if term > 0:
        dic[key] = term
    absTf.append(dic)
  return absTf

def queryTf(qToks):
  tf = []
  for query in qToks:
    dic = {}
    for token in query:
      if token not in dic:
        dic[token] = 1
      else:
        dic[token] = dic[token] + 1
    for key in dic:
      dic[key] = float(dic[key])
    tf.append(dic)
  return tf


def cosSim(vect1, vect2):
  numerator = 0
  # sos == sum of squares
  sos1, sos2 = 0, 0
  for index in range(len(vect1)):
    numerator = numerator + vect1[index]*vect2[index]
    sos1 = sos1 + math.pow(vect1[index],2)
    sos2 = sos2 + math.pow(vect2[index],2)
  sos1 = math.sqrt(sos1)
  sos2 = math.sqrt(sos2)
  denominator = float(sos1 * sos2)
  divide = 0
  try:
    divide = float(numerator/denominator)
  except:
    divide = 0
  return divide

def score(queries, absTf, absIdf, qTf, qIdf):
  scores = []
  countQ = 0
  for query in queries:
    v1 = tfidf(query, qTf[countQ], qIdf)
    countA = 0
    score_tups = []
    for abstract in absTf:
      v2 = tfidf(query, absTf[countA], absIdf)
      cosine_sim = cosSim(v1,v2)
      out = (countQ + 1, countA + 1, cosine_sim)
      score_tups.append(out)
      countA += 1
    countQ += 1
    scores.append(score_tups)
  sortedScores = []
  for query in scores:
    sortedScore = sorted(query, key=lambda tup: tup[2], reverse = True )
    sortedScores.append(sortedScore)
  return sortedScores
