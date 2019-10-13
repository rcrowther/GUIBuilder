#!/usr/bin/env python3

import os
import collections
import sys

import Parser

#! implicits == bad idea
#! robuster parsers
#! Convert attrs to funcs
#! working markup a challenge
#! make into callable module
#! Selector box definitions?
#! external wiring?
#! PrettyPrint as original form?
#! Spacing padding borders...
#! linter


DOMObject = collections.namedtuple('DOMObject', 'otype oid sClass klass oattrs children')
DOMObjectEmpty = DOMObject(otype="Empty", oid="none", sClass="none", klass="none", oattrs={}, children=[])

#! Generally, no errors, need linter
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
      Button#sendButton
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
    Button#sendButton
  StatusBar
    TextBox#status
"""
"""
TopWin|Builder Demo
    VBox#container
        Label.warning|example label
        Button#sendButton|Sad Cafe
        TextEntry
        TextArea
        SelectEntry
        CheckButton|Default Encoding
        RadioButton*group1|Left
        RadioButton*group1|Right
        RadioButton*group1|Offboard
"""

demoGUIStructure = """
  TopWin|Builder Demo
    VBox
      PageBox#pages
        VBox|info
          Label|trigger
        VBox|options
          CheckButton|null force
          CheckButton|zero force
      Button|Open
"""

demoGUIStyle = """
    #win {text: ""PhotoEmailer"}
    TopWin {padding: 30;}
    #dropArea {type: images}
    #dropicon {url:""/nice/image/icon.png"}
    #dropInstructions { text: ""choose a photo or add it here"}
    #container {background-color: light-blue; padding: 30;}
    #pages {pos: left;}
    #fileList {h: expand; v: shrink; }
    #dropArea {h: expand; max-height: 20%; font-size:large; font-weight:bold; }
    #sendButton {font-size: large; background-color: mid-blue; color: white;}
"""

# for detection of implicit boxes
containerNames = [
  "TopWin",
  "VBox", 
  "HBox",
  "PageBox", 
  #"StatusBar", 
  "DropBox"
  ]

# #! No errors considered
# def modelParse(text):
    # # The init setup is to stack an anchor Obj called 'Root', then set 
    # # the indent high. Whatever the initial indent, it will be low, so
    # # the anchor is unstacked and set as the current parent.
    # treeRoot = DOMObject(otype="Root", oid="", sClass="", klass="", oattrs={}, children=[])
    # #treeRoot = DOMObjectEmpty
    # currentParent = treeRoot
    # objStack = [currentParent]
    # indent = sys.maxsize
    # for l in iter(text.splitlines()):
        # initLen = len(l) 
        # lStripLine = l.lstrip()
        # lStriplineLen = len(lStripLine) 
        # # if empty line...
        # if (lStriplineLen == 0):
            # continue
        # newIndent = initLen - lStriplineLen

        # # Parse the object
        # #! change to 'start'
        # ## Text
        # end = lStriplineLen
        # strIdx = lStripLine.find("|")
        # oStr = ""
        # if (strIdx != -1):
            # oStr = lStripLine[strIdx + 1: end]
            # end = strIdx

        # ## Class
        # start = lStripLine.find(".")
        # oClass = ""
        # if (start != -1):
            # oClass = lStripLine[start + 1: end]
            # end = start
            
        # ## Struct class
        # start = lStripLine.find("*")
        # sClass = ""
        # if (start != -1):
            # sClass = lStripLine[start + 1: end]
            # end = start
            
        # ## Id   
        # idIdx = lStripLine.find("#")
        # oId = ""
        # if (idIdx != -1):
            # oId = lStripLine[idIdx + 1: end]
            # end = idIdx
            
        # ## Type
        # oType = lStripLine[:end]
        
        # DObj = DOMObject(otype=oType, oid=oId, sClass=sClass, klass=oClass, oattrs={}, children=[])
        # # str as an attribute as it niether key nor group?
        # if (oStr):
          # DObj.oattrs["text"] = oStr
        
        # #print(str(newIndent))
        # #print(str(DObj))
        
        # # Add object to object model, adjusting
        # # parents if necessary
        # ## is Child
        # if (newIndent > indent):
            # objStack.append(currentParent)
            # lastObj = currentParent.children[-1]
            # if (not (lastObj.otype in containerNames)):
                # implicitBox = DOMObject(otype="VBox", oid="", sClass="", klass="", oattrs={}, children=[])
                # currentParent.children.append(implicitBox)
                # lastObj = implicitBox
            # currentParent = lastObj
            # indent = newIndent
            
        # ## revert to parents
        # if (newIndent < indent):
            # currentParent = objStack.pop()
            # indent = newIndent
            
        # ## else is sibling. Now...
        # currentParent.children.append(DObj)
    # return treeRoot
        
        
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
    

def codeOpen(b):
    b.append(
"""#include<gtk/gtk.h>

void buildGUI() {
  /* Auto generated code. Heedless change generates turmoil */
""")

def codeClose(b):
    b.append(
"""}

int main(int argc, char **argv) {
  gtk_init(&argc, &argv);
  /*  gtk_window_set_title(GTK_WINDOW(win), "Hello there"); */

  buildGUI();

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


# for variable names
GTKWidgetBaseNames = {
  "TopWin": ["win", 0],
  "VBox": ["vbox", 0],
  "HBox": ["hbox", 0],
  "Label": ["label", 0],
  "Button" : ["btn", 0],
  "IconButton" : ["icon_btn", 0],
  "EmptyButton" : ["empty_btn", 0],
  "CheckButton" : ["check_btn", 0],
  "RadioButton" : ["radio_btn", 0],
  "SelectEntry" : ["select_entry", 0],
  "TextEntry" : ["text_entry", 0],
  "TextArea" : ["text_area", 0],
  "PageBox": ["page_box", 0],
  #"Page": ["page", 0],
  #"StatusBar": ["statusbar", 0],
  }

def newVariableName(oType):
  data = GTKWidgetBaseNames[oType]
  name = data[0] + str(data[1])
  data[1] = data[1] + 1
  return name
   
   
#! With the complexities of radiobuttons,
# the below has become sadly un-dry.

# groupname (sClass) -> last_var_in_group
RadioGroups = {}
  
def TopWin(b, obj, varname):
  b.append('    {} = gtk_window_new(GTK_WINDOW_TOPLEVEL);'.format(varname))
def VBox(b, obj, varname):
  b.append('    {} = gtk_box_new(GTK_ORIENTATION_VERTICAL, 1);'.format(varname))
def HBox(b, obj, varname):
  b.append('    {} = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 1);'.format(varname))
def Label(b, obj, varname):
  b.append('    {} = gtk_label_new ("{}");'.format(varname, obj.oattrs["text"]))

def Button(b, obj, varname):
  b.append('    {} = gtk_button_new_with_label ("{}");'.format(varname, obj.oattrs["text"]))
def IconButton(b, obj, varname):
  b.append('    {} = gtk_button_new ();'.format(varname))
def EmptyButton(b, obj, varname):
  b.append('    {} = gtk_button_new ();'.format(varname))
def RadioButton(b, obj, varname):
  b.append('    {} = gtk_radio_button_new_with_label (NULL, "{}");'.format(varname, obj.oattrs["text"]))
  groupName = obj.sClass
  if (groupName in RadioGroups):
    src_varname = RadioGroups[groupName]
    b.append("    gtk_radio_button_join_group (GTK_RADIO_BUTTON ({}), GTK_RADIO_BUTTON ({}));".format(varname, src_varname))
  else:
    RadioGroups[groupName] = varname
        
def CheckButton(b, obj, varname):
  b.append('    {} = gtk_check_button_new_with_label ("{}");'.format(varname, obj.oattrs["text"]))

def TextEntry(b, obj, varname):
  b.append('    {} = gtk_entry_new ();'.format(varname))
def TextArea(b, obj, varname):
  b.append('    {} = gtk_text_view_new ();'.format(varname))
def SelectEntry(b, obj, varname):
  b.append('    {} = gtk_combo_box_new ();'.format(varname))
  
def PageBox(b, obj, varname):
  b.append('    {} = gtk_notebook_new ();'.format(varname))

# def Page(b, obj, varname):
  # labelName = varname + "_label"
  # b.append('    Label * {} = gtk_label_new ("{}");'.format(labelName, obj.oattrs["text"]))
  # bodyName = varname + "_body"
  # b.append('    Box * {} = gtk_box_new (GTK_ORIENTATION_VERTICAL, 1);'.format(bodyName))
  # #b.append('    gtk_notebook_append_page (GTK_NOTEBOOK({}), {},"{}");'.format(varname, bodyName, labelName))
  
  
WidgetCreate = {
  "TopWin": TopWin,
  "VBox": VBox,
  "HBox": HBox,
  "Label" : Label,
  "TextEntry" : TextEntry,
  "TextArea" : TextArea,
  "SelectEntry" : SelectEntry,
  "Button": Button,
  "IconButton": IconButton,
  "EmptyButton": EmptyButton,
  "RadioButton": RadioButton,
  "CheckButton": CheckButton,
  "PageBox" : PageBox,
  #"Page" : Page, 
  #"StatusBar":  StatusBar,
  }


#NB Save for linter
# ObjCreatedWithText = [
  # #"TextArea",
  # "Label",
  # "Button",
  # "RadioButton",
  # "CheckButton",
  # ]
  
GTKContainers = [
  #NB dont pack topwin :)
  "TopWin",
  "EmptyButton",
  #"PageBox",
  ]


GTKBoxes = [
  "VBox",
  "HBox",
  ]

GTKPosition = {
    "left": "GTK_POS_LEFT",
    "right": "GTK_POS_RIGHT",
    "top": "GTK_POS_TOP",
    "bottom": "GTK_POS_BOTTOM",
        }
        
def notebookPos(k, v):
    return "    gtk_notebook_set_tab_pos(GTK_NOTEBOOK({}), GTK_POS_LEFT);".format(k, GTKPosition[v])

#! convert to funcs
WidgetAttributeCode = {
  "TopWin" : {
    "text" : '    gtk_window_set_title(GTK_WINDOW({}), "{}");',
    "padding": "    gtk_container_set_border_width(GTK_CONTAINER({}), {});"
    },
  "Label" : {
  #? colors
        },    
  "VBox" : {
    "padding": "    gtk_container_set_border_width(GTK_CONTAINER({}), {});"
    },
  "HBox" : {
    "padding": "    gtk_container_set_border_width(GTK_CONTAINER({}), {});"
    },
  "TextEntry" : {
    },   
  "TextArea" : {
    #! No, not that simple, its a buffer
    },  
  "Button" : {
#? colors
        },
  "CheckButton" : {
        },  
  "PageBox" : {
    #"pos": notebookPos,
    "pos": "    gtk_notebook_set_tab_pos(GTK_NOTEBOOK({}), GTK_POS_LEFT);"
        },
}


  
def widgetDeclarations(obj, statementBuilder, parentObj, parentVar, varname):
  # Create widget
  # joined with newline---so this makes a one newline separator
  statementBuilder.append("")
  WidgetCreate[obj.otype](statementBuilder, obj, varname)

  # Add attributes. 
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
  elif (parentObj.otype == "PageBox"):
    labelName = varname + "_label"
    statementBuilder.append('    GtkWidget * {} = gtk_label_new ("{}");'.format(labelName, obj.oattrs["text"]))
    statementBuilder.append("    gtk_notebook_append_page (GTK_NOTEBOOK({}), GTK_WIDGET({}), GTK_WIDGET({}));".format(parentVar, varname, labelName))

  else:
    #? else do nothing?
    warning("'{}#{}' not recognised as a container".format(parentObj.otype, parentObj.oid),"'{}#{}' is unpacked".format(obj.otype, obj.oid))
  
        
def buildCodeRec(obj, b, statementBuilder, parentObj, parentVar):
  for child in obj.children:
    varname = newVariableName(child.otype)
    b.append("    GtkWidget *{};".format(varname))
    #(obj, statementBuilder, parentObj, parentVar, varname)
    widgetDeclarations(child, statementBuilder, obj, parentVar, varname)
    buildCodeRec(child, b, statementBuilder, obj, varname)
        

def buildCode(objModel):
    # Works naturally from child of objModel
    b = []
    statementBuilder = []
    buildCodeRec(objModel, b, statementBuilder, DOMObjectEmpty, "")
    
    statementBuilder.append("\n")
    statementBuilder.append('    g_signal_connect(win0, "destroy", G_CALLBACK(gtk_main_quit), NULL);')
    statementBuilder.append("    gtk_widget_show_all(win0);")

    # append statements after declarations
    b.extend(statementBuilder)
    return b
        


"""
MAIN
"""
filename = "main.c"
b = []

objectModel = Parser.modelParse(demoGUIStructure)

def printObj(obj, depth):
    print(str(depth))
    print(obj.name)

styleModel = Parser.styleParse(demoGUIStyle)
print(styleModel)
Parser.stylePopulate(objectModel, styleModel)

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
