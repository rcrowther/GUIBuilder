#!/usr/bin/env python3

import Object



def codeOpen(b):
    b.append(
"""#include <gtk/gtk.h>
#include "test_callbacks.h"

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

WidgetBaseNames = {
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
  #"StatusBar": ["statusbar", 0],
  }


def newVariableName(oType):
  data = WidgetBaseNames[oType]
  name = data[0] + str(data[1])
  data[1] = data[1] + 1
  return name
   
   
#! With the complexities of radiobuttons,
# the below has become sadly un-dry.

FontSizeToPango = {
    "tiny" :  'xx-small',
    "smaller": 'x-small',
    "small": 'small', 
    "normal": 'medium',
    "large":'large', 
    "larger": 'x-large', 
    "huge":'xx-large',
    }

FontWeightToPango = {
    "lighter": 'ultralight',
    "light": 'light', 
    "normal":'normal', 
    "bold": 'bold', 
    "bolder": 'ultrabold',
    }

def markupCreate(oattrs):
  b = []
  if ("font-size" in oattrs):
      b.append('size=\\"{}\\"'.format(FontSizeToPango[oattrs["font-size"]]))
  if ("font-style" in oattrs):
      b.append('style=\\"{}\\"'.format(oattrs["font-style"]))
  if ("font-weight" in oattrs):
      b.append('weight=\\"{}\\"'.format(FontWeightToPango[oattrs["font-weight"]]))
  if ("font-color" in oattrs):
      # For colour, remove the '-' for X11
      b.append('foreground=\\"{}\\"'.format(oattrs["font-color"].replace("-", "")))
  text = oattrs.get("text", "")
  return "<span {}>{}</span>".format(" ".join(b), text)
  
# groupname (sClass) -> last_var_in_group
RadioGroups = {}
  
def TopWinCreate(b, obj, varname):
  b.append('    {} = gtk_window_new(GTK_WINDOW_TOPLEVEL);'.format(varname))
def VBoxCreate(b, obj, varname):
  b.append('    {} = gtk_box_new(GTK_ORIENTATION_VERTICAL, 1);'.format(varname))
def HBoxCreate(b, obj, varname):
  b.append('    {} = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 1);'.format(varname))
def LabelCreate(b, obj, varname):
  b.append('    {} = gtk_label_new (NULL);'.format(varname))
  oattrs = obj.oattrs
  markup =  markupCreate(oattrs)
  b.append('    gtk_label_set_markup (GTK_LABEL({}), "{}");'.format(varname, markup))

def ButtonCreate(b, obj, varname):
  b.append('    {} = gtk_button_new_with_label ("{}");'.format(varname, obj.oattrs["text"]))
  b.append('    g_signal_connect(GTK_BUTTON({}), "clicked", G_CALLBACK(on_button_clicked), NULL);'.format(varname))
def IconButtonCreate(b, obj, varname):
  b.append('    {} = gtk_button_new ();'.format(varname))
  b.append('    GtkWidget *image = gtk_image_new_from_file ("{}");'.format(obj.oattrs["text"]))
  b.append('    gtk_button_set_image (GTK_BUTTON({}), image);'.format(varname))
  b.append('    g_signal_connect(GTK_BUTTON({}), "clicked", G_CALLBACK(on_button_clicked), NULL);'.format(varname))
def EmptyButtonCreate(b, obj, varname):
  b.append('    {} = gtk_button_new ();'.format(varname))
def RadioButtonCreate(b, obj, varname):
  s = obj.oattrs["text"]
  active = False
  if (s[0] == "!"):
      s = s[0:]
      active = True
  b.append('    {} = gtk_radio_button_new_with_label (NULL, "{}");'.format(varname, s))
  groupName = obj.sClass
  if (groupName in RadioGroups):
    src_varname = RadioGroups[groupName]
    b.append("    gtk_radio_button_join_group (GTK_RADIO_BUTTON ({}), GTK_RADIO_BUTTON ({}));".format(varname, src_varname))
  else:
    RadioGroups[groupName] = varname
  if (active):
    b.append("    gtk_toggle_button_set_active (GTK_TOGGLE_BUTTON ({}), TRUE);".format(varname))
   
def CheckButtonCreate(b, obj, varname):
  s = obj.oattrs["text"]
  active = False
  if (s[0] == "!"):
      s = s[0:]
      active = True    
  b.append('    {} = gtk_check_button_new_with_label ("{}");'.format(varname, s))
  if (active):
    b.append("    gtk_toggle_button_set_active (GTK_TOGGLE_BUTTON ({}), TRUE);".format(varname))
   
def TextEntryCreate(b, obj, varname):
  b.append('    {} = gtk_entry_new ();'.format(varname))
def TextAreaCreate(b, obj, varname):
  b.append('    {} = gtk_text_view_new ();'.format(varname))
def SelectEntryCreate(b, obj, varname):
  b.append('    {} = gtk_combo_box_text_new ();'.format(varname))
  entryTexts = obj.oattrs["text"].split(";")
  activeIdx = 0
  for i,e in enumerate(entryTexts):
    o = e
    if (e[0] == "!"):
      o = e[0:]
      activeIdx = i
    b.append('    gtk_combo_box_text_append (GTK_COMBO_BOX_TEXT({}), "{}", "{}");'.format(varname, i, o))
  b.append('    gtk_combo_box_set_active(GTK_COMBO_BOX({}), {});'.format(varname, activeIdx))

def PageBoxCreate(b, obj, varname):
  b.append('    {} = gtk_notebook_new ();'.format(varname))

# def Page(b, obj, varname):
  # labelName = varname + "_label"
  # b.append('    Label * {} = gtk_label_new ("{}");'.format(labelName, obj.oattrs["text"]))
  # bodyName = varname + "_body"
  # b.append('    Box * {} = gtk_box_new (GTK_ORIENTATION_VERTICAL, 1);'.format(bodyName))
  # #b.append('    gtk_notebook_append_page (GTK_NOTEBOOK({}), {},"{}");'.format(varname, bodyName, labelName))
  
  
WidgetCreate = {
  "TopWin": TopWinCreate,
  "VBox": VBoxCreate,
  "HBox": HBoxCreate,
  "Label" : LabelCreate,
  "TextEntry" : TextEntryCreate,
  "TextArea" : TextAreaCreate,
  "SelectEntry" : SelectEntryCreate,
  "Button": ButtonCreate,
  "IconButton": IconButtonCreate,
  "EmptyButton": EmptyButtonCreate,
  "RadioButton": RadioButtonCreate,
  "CheckButton": CheckButtonCreate,
  "PageBox" : PageBoxCreate,
  #"Page" : PageCreate, 
  #"StatusBar":  StatusBarCreate,
  }
  
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
    return "    gtk_notebook_set_tab_pos(GTK_NOTEBOOK({}), {});".format(k, GTKPosition[v])

def setPadding(k, v):
    return "    gtk_container_set_border_width(GTK_CONTAINER({}), {});".format(k, v)

def setTitle(k, v):
    return '    gtk_window_set_title(GTK_WINDOW({}), "{}");'.format(k, v)
      
#! convert to funcs
WidgetAttributeCode = {
  "TopWin" : {
    "text" : setTitle,
    "padding": setPadding,
    },
  "Label" : {
        },
  "VBox" : {
    "padding": setPadding,
    },
  "HBox" : {
    "padding": setPadding,
    },
  "TextEntry" : {
    },
  "TextArea" : {
    #! No, not that simple, its a buffer
    },
  "Button" : {
        },
  "CheckButton" : {
        },  
  "PageBox" : {
    "pos": notebookPos
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
      # Get valid attributes 
      attributesWithCode = obj.oattrs.keys() & attributeCodes.keys()
      for attr in attributesWithCode:
        #code = attributeCodes[attr].format(varname, obj.oattrs[attr])
        code = attributeCodes[attr](varname, obj.oattrs[attr])
        statementBuilder.append(code)
        
  # Pack widget
  if (parentObj.otype in GTKContainers):
    statementBuilder.append("    gtk_container_add(GTK_CONTAINER({}), {});".format(parentVar, varname))
  elif (parentObj.otype in GTKBoxes):
    statementBuilder.append("    gtk_box_pack_start(GTK_BOX({}), {}, FALSE, FALSE, 0);".format(parentVar, varname))
    # what most people want for expansion
    #statementBuilder.append("    gtk_box_pack_start(GTK_BOX({}), {}, TRUE, TRUE, 0);".format(parentVar, varname))
  elif (parentObj.otype == "PageBox"):
    labelName = varname + "_label"
    statementBuilder.append('    GtkWidget * {} = gtk_label_new ("{}");'.format(labelName, obj.oattrs["text"]))
    statementBuilder.append("    gtk_notebook_append_page (GTK_NOTEBOOK({}), GTK_WIDGET({}), GTK_WIDGET({}));".format(parentVar, varname, labelName))

  #else:
    #? else do nothing?
    #warning("'{}#{}' not recognised as a container".format(parentObj.otype, parentObj.oid),"'{}#{}' is unpacked".format(obj.otype, obj.oid))
  
        
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
    buildCodeRec(objModel, b, statementBuilder, Object.empty, "")
    
    statementBuilder.append("\n")
    statementBuilder.append('    g_signal_connect(win0, "destroy", G_CALLBACK(gtk_main_quit), NULL);')
    statementBuilder.append("    gtk_widget_show_all(win0);")

    # append statements after declarations
    b.extend(statementBuilder)
    return b
     

def render(objectModel):
  b = []
  codeOpen(b)
  codeBuilder = buildCode(objectModel)
  b.extend(codeBuilder)
  #print(code)
  #print(b)
  codeClose(b)
  return "\n".join(b)
  
  
#if __name__ == "__main__":
