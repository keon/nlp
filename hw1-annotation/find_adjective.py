from nltk import pos_tag, word_tokenize
import nltk

with open('state_of_the_union.txt') as f:
    for lines in f:
        text = word_tokenize(lines)
        p = pos_tag(text)
        # print(p)
        for items in p:
            if items[1] == "JJ" or items[1] == "JJR" or items[1] == "JJS":
                print(items[0], ", ", items[1])
