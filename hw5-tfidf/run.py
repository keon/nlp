from infoRetrieval import *
from utils import createOutput

def run():
  print("Process Query")
  qDocs = parseQuery("Cranfield_collection_HW/cran.qry")
  qToks = tokenize(qDocs, "query")
  qDic = organize(qToks, "query")
  qIdf = idf(qDic, len(qDocs))
  qTf = queryTf(qToks)


  print("Process Abstract Docs")
  absDocs = parseAbsDocs("Cranfield_collection_HW/cran.all.1400")
  absToks = tokenize(absDocs, "abstract")
  absDic = organize(absToks, "abstract")
  absIdf = idf(absDic, len(absDocs))
  absTf = abstractTf(absDic,len(absDocs))

  print("Process Scoring" )
  scoreList = score(qToks, absTf, absIdf, qTf, qIdf)

  print("Saving the Result")
  createOutput("output.txt", scoreList)
  print("all done! results are saved in 'output.txt' file")

if __name__ == "__main__":
  run()
