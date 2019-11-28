#!/usr/bin/env python3

import os
import sys
import argparse

import ObjectModel
import Object
import GTK
from Object import WidgetTypes


#? implicits == bad idea
#? use equals, not bar
#? Detect select mark in ObjectModel, not GTK
#! generate a stub file (or socket:) )
#! File browser
#! Spacing padding borders...
#! cleanup GTK file
#! Root warning is annoying
#! empty struct makes code error
#! comments for both config files

def generateModel(structText, styleText, renderType):
    # Use for calls, this is the API.
    # For lint() see ObjectModel    
    # Make model and populate with any style
    objectModel = ObjectModel.modelParse(structText)
    styleModel = ObjectModel.styleParse(styleText)
    ObjectModel.stylePopulate(objectModel, styleModel)     
    return objectModel
       
def lint(structText, styleText):
    ObjectModel.lint(structText, styleText)


def prettyPrintModel(structText, styleText, renderType):
    objectModel = generateModel(structText, styleText, renderType)   
    Object.prettyPrint(objectModel)  
    
def treePrintModel(structText, styleText, renderType):
    objectModel = generateModel(structText, styleText, renderType)   
    print(objectModel) 
          
def modelThenRender(structText, styleText, renderType):
    # Use for calls, this is the API.
    # For lint() see ObjectModel    
    # Make model and populate with any style
    objectModel = generateModel(structText, styleText, renderType)   
    
    # render
    o = ""
    if renderType == 'GTK':
        o = GTK.render(objectModel)
    return o
    

"""
MAIN
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="build code to display GUIs")

    # codeType
    parser.add_argument(
        "-v",
        "--verbose", 
        help="talk about what is being done",
        action="store_true"
        )
    parser.add_argument(
        "-r",
        "--render-type", 
        help="choice of rendering types",
        choices=['GTK'],
        default='GTK'
        )
    parser.add_argument(
        "-l",
        "--lint", 
        help="test config files for (some) errors",
        action="store_true"
        )
    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        default="main.c",
        help="file name for output",
        )
        
    parser.add_argument(
        "-p",
        '--pretty-print',
        help="Print the model constructed from the parser",
        action="store_true"
        )
    parser.add_argument(
        "-t",
        '--tree',
        help="Print the model constructed from the parser",
        action="store_true"
        )
    parser.add_argument(
        '--widgets',
        help="List available widget names",
        action="store_true"
        )
    parser.add_argument(
        '-ss',
        '--style-src',
        type=str,
        default = "",
        help="input configuration file for builder",
        )
    parser.add_argument(
        'STRUCTURE_SOURCE',
        type=argparse.FileType('r'),
        help="input configuration file for builder",
        )
                
    args = parser.parse_args()

    #print(args)
    
    if (args.widgets):
      for widget in WidgetTypes:
        print("    {}".format(widget))      
      sys.exit()
        
    # Resolve style source if stated (or default to empty)
    if (args.style_src):
      with open(args.style_src) as f:
        args.style_src = f.read()
          
    if args.lint:
        lint(args.STRUCTURE_SOURCE.read(), args.style_src)
        if (args.verbose):
          print('lint done')
        sys.exit()

    if args.pretty_print:
        prettyPrintModel(args.STRUCTURE_SOURCE.read(), args.style_src, args.render_type)
        sys.exit()
        
    if args.tree:
        treePrintModel(args.STRUCTURE_SOURCE.read(), args.style_src, args.render_type)
        sys.exit()
                    
    if (not(args.lint)):
        o = modelThenRender(
          args.STRUCTURE_SOURCE.read(), 
          args.style_src, 
          args.render_type
          )
        with open(args.destination, "w") as f:
          f.write(o)
          
        if (args.verbose):
           print('done')
