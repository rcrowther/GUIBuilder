#!/usr/bin/env python3


#! Generally, no errors, need linter
#red
ERROR= '\033[91m'
# yellow
#WARNING= "\033[93m"
WARNING= "\033[33m"
# geeen
INFO= '\033[32m'
#blue
STRUCT= '\033[34m'
RESET= "\033[0m"

def warning(lineNum, msg, advice, data):
    print("{}[Warning]{} Line: {}; {}".format(WARNING, RESET, lineNum, msg))
    print("    ({}):".format(advice))
    print("    {}".format(data))

def error(lineNum, msg, advice, data):
    print("{}[Error]{} Line: {}; {}".format(ERROR, RESET, lineNum, msg))
    print("    ({}):".format(advice))
    print("    {}".format(data))

def getLineNum(text, pos):
  return text.count("\n", 0, pos) + 1

def getLine(text, pos):
  # Drops last char in file, but otherwise ok.
  start = text.rfind("\n", 0, pos)
  end = text.find("\n", pos)
  return text[start + 1: end]
        
def testHeader(title):
    print("\n{}== {}{}".format(STRUCT, title, RESET))
    

## Tests
if __name__ == "__main__":
  Reporter.testHeader("Error Code")
  num = getLineNum("""True, but not\nIn all fairness,\na novelty.""", 32)
  line = getLine("""True, but not\nIn all fairness,\na novelty.""", 32)
  print('Line:{}, "{}"'.format(num, line))
