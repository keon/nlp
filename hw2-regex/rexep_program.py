import re

def put_brackets():
    pass

def dollar_re(content):
    expression = "(\$[\s]?([\d\,]+)([\.\d*](\d*))?([\s]?(thousand|million|billion|trillion))?)|(((three|half)[\s]?)?([\w\.\,]+)([\s]*(dollars|dollar)))"

    count = regex_find(expression, content, "output_dollar", "dollar")
    print("dollar count: ", count)


def phone_re(content):
    expression = "(\d{3})[-\.\s]?(\d{3})[-\.\s]?(\d{4})|(\(\d{3}\))\s*((\d{3})[-\.\s]?(\d{4})|(\d{3})[-\.\s]?(\d{4}))"
    count = regex_find(expression, content, "output_phone", "phone")
    print("phone count: ", count)


def regex_find(expression, content, output_file, list_file):
    count = 0
    with open(list_file, "w") as f, \
         open(output_file, "w") as o:
        edited = content;
        for i, m in enumerate(re.finditer(expression, content, re.M)):
            match = m.group(0)
            edited = edited[:m.start(0) + (2*i)] + "[" + match  + "]" \
                     + edited[m.end(0) + (2*i):]
            f.write(match + "\n")
            count += 1
        o.write(edited);
    return(count)

if __name__ == "__main__":
    # fileName = "all-OANC.txt"
    fileName = "test_dollar_phone_corpus.txt"
    with open(fileName) as f:
        content = f.read()
        dollar_re(content)
        phone_re(content)


