#!/usr/bin/env python3

import collections
import sys
import Reporter

WidgetTypes = {
  "TopWin",
  "VBox",
  "HBox",
  "Label",
  "Button",
  "IconButton",  
  "EmptyButton",
  "RadioButton" ,
  "CheckButton" ,
  "SelectEntry" ,
  "TextEntry" ,
  "TextArea" ,
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
StackItem = collections.namedtuple('StackItem', 'indent obj')
StackItemEmpty = StackItem(0, None)

def modelLineParse(lineLen, line):
    # Parse an object definition
    # whitespace shoul be previously stripped
    ## Text
    end = lineLen
    start = line.find("|")
    oStr = ""
    if (start != -1):
        oStr = line[start + 1: end]
        end = start
    
    ## Class
    start = line.find(".")
    oClass = ""
    if (start != -1):
        oClass = line[start + 1: end]
        end = start
        
    ## Struct class
    start = line.find("*")
    sClass = ""
    if (start != -1):
        sClass = line[start + 1: end]
        end = start
        
    ## Id   
    start = line.find("#")
    oId = ""
    if (start != -1):
        oId = line[start + 1: end]
        end = start
        
    ## Type
    oType = line[:end]
    
    DObj = DOMObject(otype=oType, oid=oId, sClass=sClass, klass=oClass, oattrs={}, children=[])
    # str as an attribute as it niether key nor group?
    if (oStr):
      DObj.oattrs["text"] = oStr
    return DObj
    
            
def modelParse(text):
    # The init setup is to stack an anchor Obj called 'Root', then set 
    # the indent high. Whatever the initial indent, it will be lower, so
    # the anchor is unstacked and set as the current parent.
    treeRoot = DOMObject(otype="Root", oid="", sClass="", klass="", oattrs={}, children=[])
    currentParent = treeRoot
    objStack = [StackItem(-99, currentParent)]
    indent = sys.maxsize
    for l in iter(text.splitlines()):
        initLen = len(l) 
        lStripLine = l.strip()
        lStriplineLen = len(lStripLine) 
        # if empty line...
        if (lStriplineLen == 0):
            continue
        newIndent = initLen - lStriplineLen

        DObj = modelLineParse(lStriplineLen, lStripLine)

        #print(str(newIndent))
        #print(str(DObj))
        
        # Add object to object model, adjusting
        # parents if necessary
        ## is Child
        if (newIndent > indent):
            objStack.append(StackItem(indent, currentParent))
            lastObj = currentParent.children[-1]
            if (not (lastObj.otype in containerNames)):
                implicitBox = DOMObject(otype="VBox", oid="", sClass="", klass="", oattrs={}, children=[])
                currentParent.children.append(implicitBox)
                lastObj = implicitBox
            currentParent = lastObj
            indent = newIndent
            
        ## revert to parents
        if (newIndent < indent):
          oldParent = StackItemEmpty
          while(True):
            oldParent = objStack.pop()
            if (oldParent.indent <= newIndent):
              break
          currentParent = oldParent.obj
          indent = newIndent
            
        ## else is sibling. Now...
        currentParent.children.append(DObj)
    return treeRoot


#! Two linters, one on src, one on model
def modelParseLint(text):
  # Assume no interest in indenting
  idStash = []
  for idx, l in enumerate(iter(text.splitlines())):
    lineNum = idx + 1
    lStripLine = l.strip()
    lStriplineLen = len(lStripLine) 
    # if empty line...
    if (lStriplineLen == 0):
      continue

    obj = modelLineParse(lStriplineLen, lStripLine)
    #print(obj)
    # unidentified type
    # if (not obj.otype):
      # error(
        # lineNum,
        # "No selector type",
        # "values will be ignored, structure disrupted",
        # '"{}"'.format(l)
        # )         

    # Also covers accidental appeareence of 'Root'
    oType = obj.otype
    if (oType and not(oType in WidgetTypes)):
       Reporter.error(
         lineNum,
         "Selector type failed to match a known type",
         "values will case a compile error",
      '  "{}"'.format(oType)
         )      
      
    #  duplicate id
    oId = obj.oid
    if (oId):
      if (oId in idStash):
          Reporter.error(
            lineNum,
            "Id used twice",
            "styles will probably be applied to second instance, but undefined",
            '"{}"'.format(oId)
            )
      idStash.append(oId)


# For linting
#? warnnings about
# "TextArea",
# "Label",
# or annoying
TextObjects = {
  "Button",
  "RadioButton" ,
  "CheckButton" ,
  "SelectEntry" ,
  }
  
def modelLintRec(children):
  for obj in children:
    # text objects have/need text
    oType  = obj.otype
    if (oType in TextObjects and (not("text" in obj.oattrs ))):
      Reporter.error(
        "Unknown",
        "This object needs text for definition",
        "other objects may take optional text, these need text",
        '{}'.format(obj)
        )
    # radios have osClass for grouping
    if (oType == "RadioButton" and  (not obj.sClass)):
      Reporter.error(
        "Unknown",
        "RadioButton needs a structure class for definition",
        "GUI will not function",
        '{}'.format(obj)
        )
    modelLintRec(obj.children)
  
def modelLint(objModel):
  # Some checks on data consistency
  # To be run *after* style population
  modelLintRec(objModel.children)



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
    lineNum = Reporter.getLineNum(text, start)
    Reporter.warning(
      lineNum,
      "failed to parse a style selector",
      "declaration will be ignored",
      '"{}"'.format(text)
      )
  if (selector.oType and(not selector.oType in WidgetTypes)):
    lineNum = Reporter.getLineNum(text, start)
    Reporter.warning(
      lineNum,
      "Selector type failed to match a known type",
      "declaration will be ignored",
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
      lineNum = Reporter.getLineNum(text, start)
      Reporter.warning(
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
          lineNum = Reporter.getLineNum(text, aOpen)
          line = Reporter.getLine(text, aOpen)
          Reporter.warning(
            lineNum,
            "missing close bracket",
            "following definitions will be unused",
            '{}'.format(line)
            )
      if (aOpen == -1 or (aClose != -1 and aClose < aOpen)):
          lineNum = Reporter.getLineNum(text, aClose)
          line = Reporter.getLine(text, aClose)
          Reporter.warning(
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
          lineNum = Reporter.getLineNum(text, aOpen)
          line = Reporter.getLine(text, aOpen)
          Reporter.warning(
            lineNum,
            "missing close bracket",
            "following definitions will be unused",
            '{}'.format(line)
            )
    
        if (aOpen == -1 or (aClose != -1 and aClose < aOpen)):
          lineNum = Reporter.getLineNum(text, aClose)
          line = Reporter.getLine(text, aClose)
          Reporter.warning(
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


def lint(modelText, styleText):
  modelParseLint(modelText)
  styleLint(styleText)
  #! should only continue if not overwhelmed by errors
  objectModel = Parser.modelParse(demoGUIStructure)
  styleModel = Parser.styleParse(demoGUIStyle)
  stylePopulate(objectModel, styleModel)
  modelLint(objectModel)

        
def prettyPrintRec(obj, indent):
    if (obj.oid):
        print("{}{} {{id:{}}}".format(indent, obj.otype, obj.oid))
    if (not obj.oid):        
        print("{}{}".format(indent, obj.otype))
    for child in obj.children:
        prettyPrintRec(child, indent + "  ")
        
def prettyPrint(obj):
    indent = ""
    prettyPrintRec(obj, indent)


  
## Tests
if __name__ == "__main__":
    
  Reporter.testHeader("ModelParse")
  o = modelParse("""  VBox#support.warning  """)
  print(str(o))
  # over-indexed
  #o = modelParse("""  #support  """, 0, 22)
  #print(str(o))
  
  modelParseLint("VBox\n  Button|Go\n  Button|Stop ")
  # undefined type
  modelParseLint("VBox\n  Button|Go\n  ColourSelect|Stop ")
  # duplicate ids  
  modelParseLint("VBox#truth\n  Button|Go\n  Button#truth|Stop ")
  
  
  modelLint(modelParse("""  VBox#support.warning  """))
  # text objects
  modelLint(modelParse("""  Button|Open\n  Button\n  """))
  # Radio button group
  modelLint(modelParse("""  RadioButton*dir|Left\n  RadioButton^dir|Top\n  RadioButton|Bottom\n  """))
  
  Reporter.testHeader("Style Selector")
  o = styleSelectorParse("""  VBox#support.warning  """, 2, 22)
  print(str(o))
  # over-indexed
  o = styleSelectorParse("""  #support  """, 0, 22)
  print(str(o))

  # Bad selector
  styleSelectorLint("""    """, 0, 22)
  # Non-existing type
  styleSelectorLint("""  ColorWheel  """, 0, 22)
  

  Reporter.testHeader("Style Attrs")
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


  Reporter.testHeader("Attrs Lint")
  # Non-existing type
  styleAttributesLint(""" a{color: blue text:"/url";}  """, 3, 27)


  Reporter.testHeader("Style Parse")
  o = styleParse(""" VBox{color:blue;}  #linkLabel{text:"/url";}  """)
  print(str(o))


  Reporter.testHeader("Style Lint")
  styleLint(""" VBox{color:green;} \n#linkLabel{text:"/url";}  """)
  styleLint(""" HBox{color:green;}  \n#aboutlinks text:"/url"}  """)
  styleLint(""" CheckButton{}  """)
