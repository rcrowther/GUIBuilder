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

