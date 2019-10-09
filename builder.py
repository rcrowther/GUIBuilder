#!/usr/bin/env python3

import os


import collections

#! Root to make Window too (so attributes added)
#! want Tabs,
#! working markup a challenge
#! grouping radio buttons challenge
#! make into callable module
#! Selector box definitions?
#! external wiring?
#! PrettyPrint as original form?
#! Spacing padding borders...

DOMObject = collections.namedtuple('DOMObject', 'otype oid klass oattrs children')
ERROR= '\033[91m'
#WARNING= "\033[93m"
WARNING= "\033[33m"
INFO= '\033[32m'
RESET= "\033[0m"

def warning(msg, data):
    print("{}[Warning]{} {}:".format(WARNING, RESET, msg))
    print("    {}".format(data))

def error(msg, data):
    print("{}[Error]{} {}:".format(ERROR, RESET, msg))
    print("    {}".format(data))

""" 
gui.structure(""
WindowMain#win
  VBox#container
    TextList#fileList
    DropBox#dropArea
      Icon#dropicon
      TextBox#dropInstructions
      LabelButton#sendButton
    StatusBar
      TextBox#status
"
)
"""
"""
demoGUIStructure = 
VBox#container
  TextList#fileList
  DropBox#dropArea
    Icon#dropicon
    TextBox#dropInstructions
    LabelButton#sendButton
  StatusBar
    TextBox#status
"""
demoGUIStructure = """
VBox#container
    Label|example label
    LabelButton#sendButton|Sad Cafe
    TextEntry
    TextArea
    SelectEntry
    CheckButton|Default Encoding
    RadioButton|Left
    RadioButton|Right
    RadioButton|Offboard
"""

demoGUIStyle = """
    #win {text: ""PhotoEmailer"}
    #dropArea {type: images}
    #dropicon {url:""/nice/image/icon.png"}
    #dropInstructions { text: ""choose a photo or add it here"}
    #container {background-color: light-blue; orientation:vertical; }
    #fileList {h: expand; v: shrink; }
    #dropArea {h: expand; max-height: 20%; font-size:Large; font-weight:bold; }
    #sendButton {font-size: large; background-color: mid-blue; color: white;}
"""

# for detection of implicit boxes
containerNames = [
  "VBox", 
  "HBox", 
  #"StatusBar", 
  "DropBox"
  ]

#! No errors considered
def modelParse(text):
    treeRoot = DOMObject(otype="Root", oid="", klass="", oattrs={}, children=[])
    currentParent = treeRoot
    objStack = [currentParent]
    indent = 0
    for l in iter(text.splitlines()):
        initLen = len(l) 
        lStripLine = l.lstrip()
        lStriplineLen = len(lStripLine) 
        # if empty line...
        if (lStriplineLen == 0):
            continue
        newIndent = initLen - lStriplineLen

        # Parse the object
        end = lStriplineLen
        strIdx = lStripLine.find("|")
        oStr = ""
        if (strIdx != -1):
            oStr = lStripLine[strIdx + 1: end]
            end = strIdx
        idIdx = lStripLine.find("#")
        oId = ""
        if (idIdx != -1):
            oId = lStripLine[idIdx + 1: end]
            end = idIdx
        oType = lStripLine[:end]
        
            
            
        # oType = lStripLine[0, idIdx]
        # oId = ""

        # parsedObject = lStripLine.split("#")
        # oType = parsedObject[0]
        # oId = ""
        # if (len(parsedObject) > 1):
            # parsedObject = lStripLine.split("|")
            # oId = parsedObject[1] 
        DObj = DOMObject(otype=oType, oid=oId, klass="", oattrs={}, children=[])
        # str as an attribute as it niether key nor group?
        if (oStr):
          DObj.oattrs["text"] = oStr
        
        #print(str(newIndent))
        #print(str(DObj))
        
        if (newIndent > indent):
            objStack.append(currentParent)
            lastObj = currentParent.children[-1]
            if (not (lastObj.otype in containerNames)):
                implicitBox = DOMObject(otype="VBox", oid="", klass="", oattrs={}, children=[])
                currentParent.children.append(implicitBox)
                lastObj = implicitBox
            currentParent = lastObj
            indent = newIndent
            
        if (newIndent < indent):
            currentParent = objStack.pop()
            indent = newIndent
            
        currentParent.children.append(DObj)
    return treeRoot
        
        
def objectModelppRec(obj, indent):
    if (obj.oid):
        print("{}{} {{id:{}}}".format(indent, obj.otype, obj.oid))
    if (not obj.oid):        
        print("{}{}".format(indent, obj.otype))
    for child in obj.children:
        objectModelppRec(child, indent + "  ")
        
def objectModelpp(obj):
    indent = ""
    objectModelppRec(obj, indent)

# def treeWalkerTopDownRec(obj, func, depth):
    # func(obj, depth)
    # for child in obj.children:
        # treeWalkerTopDownRec(child, func, depth + 1)
        
# def treeWalkerTopDown(obj, func):
    # depth = 0
    # treeWalkerTopDownRec(obj, func, depth)
    

def stylePopulateRec(obj, styleModel):
    oid = obj.oid
    if oid in styleModel:
        obj.oattrs.update( styleModel[oid] )
    for child in obj.children:
        stylePopulateRec(child, styleModel)
        
def stylePopulate(tree, styleModel):
    stylePopulateRec(tree, styleModel)


def styleParse(styleTxt):
    # Hash(id -> Hash(attr -> value ...))
    styleModel = {}
    for entry in iter(styleTxt.split("}")):
        lsEntry = entry.lstrip()
        # if empty line...
        if (not lsEntry):
            continue
        parsedStyle = lsEntry.split("{")
        
        # parse id
        #! cheap solution
        oId = parsedStyle[0].split("#")[1].rstrip()
        if not oId:
            warning("failed to parse style identifier", lsEntry)
            continue
        
        #print(str(parsedStyle))
        #print(str(oId))
                
        #parse attr dict
        attrDict ={}
        for attrEntry in parsedStyle[1].split(";"):
            sAttrEntry = attrEntry.strip()
            if not sAttrEntry:
                continue
            parsedAttrEntry = sAttrEntry.split(":")
            if not len(parsedAttrEntry) == 2:
                warning("failed to parse style attributes", sAttrEntry)
                continue
            attrId = parsedAttrEntry[0].rstrip()
            attrValue = parsedAttrEntry[1].lstrip()
            
            attrDict[attrId] = attrValue
            
        #NB: appended as the model parses 'text' attribute
        if not(oId in styleModel):
            styleModel[oId] = {}
        styleModel[oId].update(attrDict)
    #print(styleModel)
    return styleModel

    
def codeOpen(b):
    b.append(
"""#include<gtk/gtk.h>

void buildGUI(GtkWidget *win) {
  /* Auto generated code. Heedless change generates turmoil */
""")

def codeClose(b):
    b.append(
"""
}

int main(int argc, char **argv) {
  GtkWidget *win;
  gtk_init(&argc, &argv);
  win = gtk_window_new(GTK_WINDOW_TOPLEVEL);
  /*  gtk_window_set_title(GTK_WINDOW(win), "Hello there"); */

  buildGUI(win);

  g_signal_connect(win, "destroy", G_CALLBACK(gtk_main_quit), NULL);
  gtk_widget_show_all(win);
  gtk_main();
}
""")

"""
  entry1 = gtk_entry_new();
  gchar *str = "<b>ZetCode</b>, knowledge only matters";
  gtk_label_set_markup(GTK_LABEL(label), str);
title = gtk_label_new("Windows");
  wins = gtk_text_view_new();
    cb = gtk_check_button_new_with_label("Show title");
      statusbar = gtk_statusbar_new();
"""

       
#GTKWidgetAttribute = {
#"orientation": "GtkOrientation orientation"
#}

# for variable nabes
GTKWidgetBaseNames = {
  "VBox": ["vbox", 0],
  "HBox": ["hbox", 0],
  "Label": ["label", 0],
  "RadioButton" : ["radio_btn", 0],
  "CheckButton" : ["check_btn", 0],
  "SelectEntry" : ["select_entry", 0],
  "TextEntry" : ["text_entry", 0],
  "TextArea" : ["text_area", 0],
  "LabelButton": ["label_btn", 0],
  #"StatusBar": ["statusbar", 0],
  }

def newVariableName(oType):
  data = GTKWidgetBaseNames[oType]
  name = data[0] + str(data[1])
  data[1] = data[1] + 1
  return name
   
GTKWidgetCreate = {
  "VBox": "= gtk_box_new(GTK_ORIENTATION_VERTICAL, 1);",
  "HBox": "= gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 1);",
  "Label" : '= gtk_label_new ("{}");',
  "TextEntry" : "= gtk_entry_new ();",
  "TextArea" : "= gtk_text_view_new ();",
  "SelectEntry" : "= gtk_combo_box_new ();",
  "LabelButton": '= gtk_button_new_with_label ("{}");',
  "RadioButton": '= gtk_radio_button_new_with_label (NULL, "{}");',
  "CheckButton": '= gtk_check_button_new_with_label ("{}");',
  #"StatusBar": "= gtk_statusbar_new();",
  }

ObjCreatedWithText = [
  #"TextArea",
  "Label",
  "LabelButton",
  "RadioButton",
  "CheckButton",
  ]
  
GTKContainers = [
  "Root",
  #"LabelButton",
  ]


GTKBoxes = [
  "VBox",
  "HBox",
  ]

WidgetAttributeCode = {
      
#  "TopWindow"??? : {
#    "text" : "    gtk_window_set_title(GTK_WINDOW({}), {});"
#    },
    #Label
  "Label" : {
  #? colors
    #"text": "    gtk_label_set_text(GTK_LABEL({}), {});"
        },    
    #Box
  "VBox" : {
  #? colors
  #! GTK_ORIENTATION_HORIZONTAL GTK_ORIENTATION_VERTICAL
    #"orientation": "    gtk_orientable_set_orientation(GTK_BOX({}), {});"
    },
  "HBox" : {
  #? colors
  #! GTK_ORIENTATION_HORIZONTAL GTK_ORIENTATION_VERTICAL
    #"orientation": "    gtk_orientable_set_orientation(GTK_BOX({}), {});"
    },
    #Entry
  "TextEntry" : {
    #"text": "    gtk_entry_set_text(GTK_ENTRY({}), {});"
    },   
  "TextArea" : {
    #! No, not that simple, its a buffer
    #"text": "    gtk_textview_set_text(GTK_ENTRY({}), {});"
    },  
  "LabelButton" : {
#? colors
    #"text": "    gtk_button_set_label(GTK_BUTTON({}), {});"
        },
  "CheckButton" : {
    #"text": "    gtk_button_set_label(GTK_BUTTON({}), {});"
        },  
}


  
def widgetDeclarations(obj, statementBuilder, parentObj, parentVar, varname):
  # Create widget
  createStatement = GTKWidgetCreate[obj.otype]
  if (obj.otype in ObjCreatedWithText):
      txt = obj.oattrs.get("text", "")
      createStatement = createStatement.format(txt)
  statementBuilder.append("    {} {}".format(varname, createStatement))

  # Add attributes. 
  #! Like button text would be a start
  #gtk_container_add(label).
  #! Window title?
  #! respect text color? if not background?
  #! and orientation of boxes?
  # box_set_orientation (GTK_ORIENTATION_VERTICAL)
  if obj.otype in WidgetAttributeCode:
      attributeCodes = WidgetAttributeCode[obj.otype]
      attributesWithCode = obj.oattrs.keys() & attributeCodes.keys()
      for attr in attributesWithCode:
        code = attributeCodes[attr].format(varname, obj.oattrs[attr])
        statementBuilder.append(code)
        
  # Pack widget
  if (parentObj.otype in GTKContainers):
    statementBuilder.append("    gtk_container_add(GTK_CONTAINER({}), {});".format(parentVar, varname))
  elif (parentObj.otype in GTKBoxes):
    statementBuilder.append("    gtk_box_pack_start(GTK_BOX({}), {}, TRUE, TRUE, 0);".format(parentVar, varname))
  else:
    #? else do nothing?
    warning("'{}#{}' not recognised as a container".format(parentObj.otype, parentObj.oid),"'{}#{}' is unpacked".format(obj.otype, obj.oid))
  

        
        
def buildCodeRec(obj, b, statementBuilder, parentObj, parentVar):
  #if (obj.otype in GTKWidgetBaseNames):  
  varname = newVariableName(obj.otype)
  b.append("    GtkWidget *{};".format(varname))
  widgetDeclarations(obj, statementBuilder, parentObj, parentVar, varname)
  for child in obj.children:
    buildCodeRec(child, b, statementBuilder, obj, varname)
        

def buildCode(objModel):
    b = []
    statementBuilder = []
    buildCodeRec(objModel.children[0], b, statementBuilder, objModel, "win")
    b.append("\n")
    b.extend(statementBuilder)
    return b
    
def write(b):
    #if (obj.otype == "Box"):
        
    b.append(
"""
    void buildGUI(GtkWidget *win) {
      GtkWidget *vbox;
      GtkWidget *settings;
      
  vbox = gtk_box_new(TRUE, 1);
  gtk_container_add(GTK_CONTAINER(win), vbox);
   // GtkWidget *btn = gtk_button_new_with_label("Click Me!");
 // gtk_container_add(GTK_CONTAINER(halign), button);
  settings = gtk_button_new_with_label("Settings");
  gtk_box_pack_start(GTK_BOX(vbox), settings, TRUE, TRUE, 0);
      }
"""
)

"""
MAIN
"""
filename = "main.c"
b = []

objectModel = modelParse(demoGUIStructure)

def printObj(obj, depth):
    print(str(depth))
    print(obj.name)
#OMpp(DOM)

#treeWalkerTopDown(DOM, printObj)
#stylePopulate(DOM, demoGUIStyle)
styleModel = styleParse(demoGUIStyle)
stylePopulate(objectModel, styleModel)

print(str(objectModel))
objectModelpp(objectModel)

codeOpen(b)

codeBuilder = buildCode(objectModel)

b.extend(codeBuilder)
#code = "\n".join(codeBuilder)
#print(code)


#print(b)

codeClose(b)

#print(getVariableName("Box"))
#print(getVariableName("Box"))
#print(getVariableName("Box"))

with open (filename, "w") as f:
    f.write("\n".join(b))     
path = os.path.abspath(filename)
print("gui code written to {}".format(path))
