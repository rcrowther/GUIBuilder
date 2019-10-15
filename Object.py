import collections

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
  
  
new = collections.namedtuple('DOMObject', 'otype oid sClass klass oattrs children')
empty = new(otype=None, oid=None, sClass=None, klass=None, oattrs={}, children=[])

#! not right with select and expand marks. Add those too?
def prettyPrintRec(b, indent, obj):
    b.append(indent)
    if (obj.otype):
       b.append(obj.otype)
    if (obj.oid):
       b.append("#") 
       b.append(obj.oid)
    if (obj.klass):
       b.append(".") 
       b.append(obj.klass)
    if (obj.sClass):
       b.append("*") 
       b.append(obj.sClass)
    if ('text' in obj.oattrs):
       b.append("|") 
       b.append(obj.oattrs["text"])
    b.append("\n")
    for child in obj.children:
        prettyPrintRec(b, indent + "  ", child)
        
def prettyPrint(obj):
    indent = ""
    b = []
    prettyPrintRec(b, indent, obj)
    print("".join(b))
