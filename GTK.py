#!/usr/bin/env python3


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
     
if __name__ == "__main__":
