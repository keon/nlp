def createOutput(fileName, scores):
  with open(fileName, "w") as f:
    for score in scores:
      for tup in score:
        string = ""
        for t in tup:
          string = string + str(t) + " "
        f.write(string + "\n")
    f.close()

