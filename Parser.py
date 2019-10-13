#!/usr/bin/env python3

import collections
import sys


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
        
WidgetTypes = {
  "TopWin",
  "VBox",
  "HBox",
  "Label",
  "RadioButton" ,
  "CheckButton" ,
  "SelectEntry" ,
  "TextEntry" ,
  "TextArea" ,
  "LabelButton",
  "PageBox",
  #"StatusBar",
  }
  
DOMObject = collections.namedtuple('DOMObject', 'otype oid sClass klass oattrs children')
DOMObjectEmpty = DOMObject(otype="Empty", oid="none", sClass="none", klass="none", oattrs={}, children=[])


# for detection of implicit boxes
containerNames = [
  "TopWin",
  "VBox", 
  "HBox",
  "PageBox", 
  #"StatusBar", 
  "DropBox"
  ]
  

#! No errors considered
def modelParse(text):
    # The init setup is to stack an anchor Obj called 'Root', then set 
    # the indent high. Whatever the initial indent, it will be low, so
    # the anchor is unstacked and set as the current parent.
    treeRoot = DOMObject(otype="Root", oid="", sClass="", klass="", oattrs={}, children=[])
    currentParent = treeRoot
    objStack = [currentParent]
    indent = sys.maxsize
    for l in iter(text.splitlines()):
        initLen = len(l) 
        lStripLine = l.lstrip()
        lStriplineLen = len(lStripLine) 
        # if empty line...
        if (lStriplineLen == 0):
            continue
        newIndent = initLen - lStriplineLen

        # Parse the object
        #! change to 'start'
        ## Text
        end = lStriplineLen
        strIdx = lStripLine.find("|")
        oStr = ""
        if (strIdx != -1):
            oStr = lStripLine[strIdx + 1: end]
            end = strIdx

        ## Class
        start = lStripLine.find(".")
        oClass = ""
        if (start != -1):
            oClass = lStripLine[start + 1: end]
            end = start
            
        ## Struct class
        start = lStripLine.find("*")
        sClass = ""
        if (start != -1):
            sClass = lStripLine[start + 1: end]
            end = start
            
        ## Id   
        idIdx = lStripLine.find("#")
        oId = ""
        if (idIdx != -1):
            oId = lStripLine[idIdx + 1: end]
            end = idIdx
            
        ## Type
        oType = lStripLine[:end]
        
        DObj = DOMObject(otype=oType, oid=oId, sClass=sClass, klass=oClass, oattrs={}, children=[])
        # str as an attribute as it niether key nor group?
        if (oStr):
          DObj.oattrs["text"] = oStr
        
        #print(str(newIndent))
        #print(str(DObj))
        
        # Add object to object model, adjusting
        # parents if necessary
        ## is Child
        if (newIndent > indent):
            objStack.append(currentParent)
            lastObj = currentParent.children[-1]
            if (not (lastObj.otype in containerNames)):
                implicitBox = DOMObject(otype="VBox", oid="", sClass="", klass="", oattrs={}, children=[])
                currentParent.children.append(implicitBox)
                lastObj = implicitBox
            currentParent = lastObj
            indent = newIndent
            
        ## revert to parents
        if (newIndent < indent):
            currentParent = objStack.pop()
            indent = newIndent
            
        ## else is sibling. Now...
        currentParent.children.append(DObj)
    return treeRoot




# Style parser
StyleSelector = collections.namedtuple('StyleSelector', 'oType oId oClass')
    
def styleSelectorParse(text, start, end):
  # Whitespace allowed on ends
  sEnd = end
  sStart = text.find(".", start, sEnd)
  oClass = ""
  if (sStart != -1):
    oClass = text[sStart + 1: sEnd] 
    sEnd = sStart
            
  sStart = text.find("#", start, sEnd)
  oId = ""
  if (sStart != -1):
    oId = text[sStart + 1: sEnd] 
    sEnd = sStart
    
  oType = ""
  if (sEnd > 0):
    oType = text[start: sEnd]

  return StyleSelector(oType.strip(), oId.strip(), oClass.strip())

def styleSelectorLint(text, start, end):
  selector = styleSelectorParse(text, start, end)
  if (not (selector.oType or selector.oId or selector.oClass)):
    lineNum = getLineNum(text, start)
    warning(
      lineNum,
      "failed to parse a style selector",
      "values will be ignored",
      '"{}"'.format(text)
      )
  if (selector.oType and(not selector.oType in WidgetTypes)):
    lineNum = getLineNum(text, start)
    warning(
      lineNum,
      "Selector type failed to match a known type",
      "values will be ignored",
      '"{}"'.format(text)
      )

def styleAttributesParse(text, start, end):
  # get values
  # assumed no backets (''end' on closing bracket)
  attrDict = {}

  aStart = start
  aEnd = text.find(";", start)
  while (aEnd < end and aEnd != -1):
    assoc = text.find(":", aStart, aEnd)
    if (assoc != -1):
      k = text[aStart : assoc].strip()
      v = text[assoc + 1 : aEnd].strip()
      attrDict[k] = v
    aStart = aEnd + 1
    aEnd = text.find(";", aStart)
  return attrDict

def styleAttributesLint(text, start, end):
  oAttrs = styleAttributesParse(text, start, end)
  for k,v in oAttrs.items():
    if (v.find(":") != -1):
      lineNum = getLineNum(text, start)
      warning(
        lineNum,
        "colon found in a value",
        "maybe a missing semi-colon?",
        '"{}":"{}"'.format(k, v)
        )

## Hash(category -> Hash(id -> Hash(attr -> value ...)))
StyleModel = collections.namedtuple('StyleModel', 'typeStyles idStyles classStyles')

def styleParse(text):
  typeStyles = {}
  idStyles = {}
  classStyles = {}
  
  sStart = 0
  aOpen = text.find("{")
  aClose = text.find("}")
  while((aOpen != -1) and (aOpen < aClose)):
    selector = styleSelectorParse(text, sStart, aOpen)
    sAttrs = styleAttributesParse(text, aOpen + 1, aClose)
    #print(str(selector))
    #print(str(sAttrs))
    
    # allocate results (even if no selector)
    typeStyles[selector.oType] = sAttrs
    idStyles[selector.oId] = sAttrs
    classStyles[selector.oClass] = sAttrs
    
    sStart = aClose + 1
    aOpen = text.find("{", sStart)
    aClose = text.find("}", sStart)
    
  # silently delete empty selectors (which have been overriding)
  typeStyles.pop("", None)
  idStyles.pop("", None)
  classStyles.pop("", None)
  
  return StyleModel(typeStyles, idStyles, classStyles)


def styleLint(text):
  sStart = 0
  aOpen = text.find("{")
  aClose = text.find("}")
  #print(str(aOpen))
  #print(str(aClose))
  # EOF case
  if (not(aClose == -1 and aOpen == -1)):
      if (aClose == -1):
          lineNum = getLineNum(text, aOpen)
          line = getLine(text, aOpen)
          warning(
            lineNum,
            "missing close bracket",
            "following definitions will be unused",
            '{}'.format(line)
            )
      if (aOpen == -1 or (aClose != -1 and aClose < aOpen)):
          lineNum = getLineNum(text, aClose)
          line = getLine(text, aClose)
          warning(
            lineNum,
            "missing open bracket",
            "preceeding definitions will be unused",
            '{}'.format(line)
            )
  # relies on -1 if aClose not found
  while((aOpen!= -1) and (aOpen < aClose)):
    selector = styleSelectorLint(text, sStart, aOpen)
    sAttrs = styleAttributesLint(text, aOpen + 1, aClose)
    
    sStart = aClose + 1
    aOpen = text.find("{", sStart)
    aClose = text.find("}", sStart)
    #print(str(aOpen))
    #print(str(aClose))
    # EOF case
    if (not(aClose == -1 and aOpen == -1)):
        if (aClose == -1):
          lineNum = getLineNum(text, aOpen)
          line = getLine(text, aOpen)
          warning(
            lineNum,
            "missing close bracket",
            "following definitions will be unused",
            '{}'.format(line)
            )
    
        if (aOpen == -1 or (aClose != -1 and aClose < aOpen)):
          lineNum = getLineNum(text, aClose)
          line = getLine(text, aClose)
          warning(
            lineNum,
            "missing sopen bracket",
            "preceeding definitions will be unused",
            '{}'.format(line)
            )

## Style populate
def stylePopulateRec(obj, styleModel):
    oId = obj.oid
    if oId in styleModel.idStyles:
        obj.oattrs.update( styleModel.idStyles[oId] )
    oType = obj.otype
    if oType in styleModel.typeStyles:
        obj.oattrs.update( styleModel.typeStyles[oType] )
    oClass = obj.klass
    if oClass in styleModel.classStyles:
        obj.oattrs.update( styleModel.classStyles[oClass] )
    for child in obj.children:
        stylePopulateRec(child, styleModel)

def stylePopulate(objectModel, styleModel):
    stylePopulateRec(objectModel, styleModel)

## Tests
def testHeader(title):
    print("\n{}== {}{}".format(STRUCT, title, RESET))
    
if __name__ == "__main__":
  testHeader("Error Code")
  num = getLineNum("""True, but not\nIn all fairness,\na novelty.""", 32)
  line = getLine("""True, but not\nIn all fairness,\na novelty.""", 32)
  print('Line:{}, "{}"'.format(num, line))
  

  testHeader("Style Selector")
  o = styleSelectorParse("""  VBox#support.warning  """, 2, 22)
  print(str(o))
  # over-indexed
  o = styleSelectorParse("""  #support  """, 0, 22)
  print(str(o))

  # Bad selector
  styleSelectorLint("""    """, 0, 22)
  # Non-existing type
  styleSelectorLint("""  ColorWheel  """, 0, 22)
  

  testHeader("Style Attrs")
  o = styleAttributesParse(""" a{color:blue; text:"/url";}  """, 3, 27)
  print(str(o))
  # missing assoc
  o = styleAttributesParse(""" a{color blue; text:"/url";}  """, 3, 27)
  print(str(o))
  # missing semi-colon
  o = styleAttributesParse(""" a{color: blue text:"/url";}  """, 3, 27)
  print(str(o))
  # missing formatting
  o = styleAttributesParse(""" a{color blue text "/url"}  """, 3, 27)
  print(str(o))


  testHeader("Attrs Lint")
  # Non-existing type
  styleAttributesLint(""" a{color: blue text:"/url";}  """, 3, 27)


  testHeader("Style Parse")
  o = styleParse(""" VBox{color:blue;}  #linkLabel{text:"/url";}  """)
  print(str(o))


  testHeader("Style Lint")
  styleLint(""" VBox{color:green;} \n#linkLabel{text:"/url";}  """)
  styleLint(""" HBox{color:green;}  \n#aboutlinks text:"/url"}  """)
  styleLint(""" CheckButton{}  """)
