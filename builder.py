#!/usr/bin/env python3

import os
import sys
import argparse

import ObjectModel
import GTK
from Object import WidgetTypes


#! implicits == bad idea
#! Convert attrs to funcs
#! external wiring?
#! PrettyPrint as original form?
#! Spacing padding borders...
#! cleanup GTK file
#! Root warning is annoying
#! empty struct makes code error
#! only one Topwin
#! comments for both config files
#! labels need text, even if nothing. Or default?
#? HBox homogenous
#! need an indicator for expanding pack value

 
        
def generateOutput(structText, styleText, renderType):
    # Use for calls, this is the API.
    # For lint() see ObjectModel    
    # Make model and populate with any style
    objectModel = ObjectModel.modelParse(structText)
    styleModel = ObjectModel.styleParse(styleText)
    ObjectModel.stylePopulate(objectModel, styleModel)    
    
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
        help="output file",
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
        ObjectModel.lint(args.STRUCTURE_SOURCE.read(), args.style_src)

    if (not(args.lint)):
        o = generateOutput(
          args.STRUCTURE_SOURCE.read(), 
          args.style_src, 
          args.render_type
          )
        with open(args.destination, "w") as f:
          f.write(o)
          
    if (args.verbose):
        print('done')
