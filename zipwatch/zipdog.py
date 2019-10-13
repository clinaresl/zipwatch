#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# zipdog.py
# Description: zip watcher examines and verifies the contents of zip files against a schema
# -----------------------------------------------------------------------------
#
# Login   <carlos.linares@uc3m.es>
#

"""
zip watcher examines and verifies the contents of zip files against a schema
"""

# globals
# -----------------------------------------------------------------------------
__version__  = '1.0'


# imports
# -----------------------------------------------------------------------------
import argparse                 # argument parsing
import inspect                    # inspect python modules
import os                         # file handling
import sys                        # system accessing
import zipfile                    # zip files management

from pathlib import Path          # path handling

import zwcschema


# functions
# -----------------------------------------------------------------------------

# create a command parser to parse all params passed to the script
# -----------------------------------------------------------------------------
def createArgParser ():
    """create a command parser to parse all params passed to the script"""

    # initialize a parser
    parser = argparse.ArgumentParser (description="zip watcher examines and verifies the contents of zip files against a schema")

    # now, add the arguments

    # Group of mandatory arguments
    mandatory = parser.add_argument_group ("Mandatory arguments", "The following arguments are required")
    mandatory.add_argument ('-f', '--files',
                            required=True,
                            type=str,
                            nargs='+',
                            help="used to provide the location and name of all zip files to examine. Unix filename pattern matching ('*' and '?') is allowed.")

    # Group of optional arguments
    optional = parser.add_argument_group ("Optional arguments", "The following arguments are optional")
    optional.add_argument ('-c', '--configuration',
                            type=str,
                            default="conf.py",
                            help="provides the name of the configuration file to use. By default 'conf.py'")
    optional.add_argument ('-s', '--show-summary',
                           action='store_true',
                           help="if given, a summary with all the information extracted from the zip file is shown")

    # Group of miscellaneous arguments
    misc = parser.add_argument_group ('Miscellaneous')
    misc.add_argument ('-S', '--show-schema',
                       action='store_true',
                       help="shows the schema the contents of zip files are compared with and exit")
    misc.add_argument ('-V', '--version',
                       action='version',
                       version=" %s %s" % (sys.argv [0], __version__),
                       help="output version information and exit")

    # and return the parser
    return parser
    

# verifies the name of the configuration file and returns a valid
# namespace for it
# -----------------------------------------------------------------------------
def checkConfigFile (configFile):
    """verifies the name of the configuration file and returns a valid
       namespace for it

    """

    # create an instance of a path with the given configuration file
    pathconfig = Path (configFile)

    # verify the file exists and it is accessible
    try:
        my_abs_path = pathconfig.resolve (strict=True)

    except FileNotFoundError:

        # if it does not exist
        print ("Fatal error: the file '{0}' does not exist or it is not accessible".format (configFile))
        sys.exit (1)
        
    else:
        
        # yeah, it exists, get then its namespace name
        return os.path.splitext (os.path.basename (configFile))[0]

    
# returns the contents of the specified list from the given component. The
# component should exist, otherwise the result is undefined
# -----------------------------------------------------------------------------
def accessList (module, component):
    """returns the contents of the specified list from the given component. The
       component should exist, otherwise the result is undefined

    """

    # create python statements and execute them within an empty context
    command = """import {0}

lstHandler = {0}.{1}
""".format (module, component)
    context = dict ()
    exec (command, context)

    # now, return the contents of the list
    return context["lstHandler"]
    

# verifies the given component names a list from the given module
# -----------------------------------------------------------------------------
def checkList (module, component):
    """verifies the given component names a list from the given module

    """

    # create python statements and execute them within an empty context
    command = """import inspect
import {0}

{1}_exists = hasattr({0}, \"{1}\")
{1}_is_a_list = {1}_exists and isinstance ({0}.{1}, list)
""".format (module, component)
    context = dict ()
    exec (command, context)

    # now, retrive from the context whether: first, the component exists and
    # second, it is defined as a list
    return context["{0}_exists".format (component)] and context["{0}_is_a_list".format (component)]
    

# verifies the given component names a function from the given module
# -----------------------------------------------------------------------------
def checkFunction (module, component):
    """verifies the given component names a function from the given module

    """

    # create python statements and execute them within an empty context
    command = """import inspect
import {0}

{1}_exists = hasattr({0}, \"{1}\")
{1}_is_function = {1}_exists and inspect.isfunction ({0}.{1})
""".format (module, component)
    context = dict ()
    exec (command, context)

    # now, retrive from the context whether: first, the component exists and
    # second, it is defined as a function
    return context["{0}_exists".format (component)] and context["{0}_is_function".format (component)]
    

# verifies the contents of the configFile, i.e., that all necessary functions
# and data structures are given
# -----------------------------------------------------------------------------
def verifyConfigFile (configFile):
    """verifies the contents of the configFile, i.e., that all necessary functions
       and data structures are given

    """

    # check the existence of the list schemaSpec
    if not checkList (configFile, "schemaSpec"):
        print (" Fatal error: the component 'schemaSpec' has not been found in module '{0}'".format (configFile))
        sys.exit (1)

    # verify that all functions given in the schema specification are also implemented
    for ischema in accessList (configFile, "schemaSpec"):

        if len (ischema) != 4:
            print (" Fatal error: the schema '{0}' from 'schemaSpec' has an incorrect number of arguments".format (ischema))
            sys.exit (1)

        # note that while the schema should consist of precisely four arguments,
        # it is possible to give the empty string as an if-then function
        if ischema[2] and not checkFunction (configFile, ischema[2]):
            print (" Fatal error: the if-then function '{0}' has not been found in module '{1}'".format (ischema[2], configFile))
            sys.exit (1)

        # likewise, it is also allowed to specify the empty string as an else
        # function
        if ischema[3] and not checkFunction (configFile, ischema[3]):
            print (" Fatal error: the if-else function '{0}' has not been found in module '{1}'".format (ischema[3], configFile))
            sys.exit (1)
    
    # check the existence of the mandatory functions
    for icomponent in ["preamble", "setUp", "showSummary", "tearDown", "epilogue"]:
    
        if not checkFunction (configFile, icomponent):
            print (" Fatal error: the component '{0}' has not been found in module '{1}'".format (icomponent, configFile))
            sys.exit (1)
    

# main
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # --initialization

    # first of all, verify just if show-schema has been requested
    if '--show-schema' in sys.argv or \
       '-S' in sys.argv:
        print (schema)
        sys.exit (0)

    # invoke the parser and parse all commands
    params = createArgParser ().parse_args ()

    # check the configuration file and verify its contents
    configFile = checkConfigFile (params.configuration)
    verifyConfigFile (configFile)

    # invoke the preamble before starting the whole process
    command = """import {0}
{0}.preamble ()""".format (configFile)
    exec (command)        
        
    # for all files given in the command-line
    for ifile in params.files:

        print (" Processing '{0}' ...".format (ifile))
        print ("---------------------------------------------------------------")

        # list the contents of this file
        with zipfile.ZipFile (ifile) as zipstream:

            # execute the pramble of the configuration file
            command = """import {0}
{0}.setUp ()""".format (configFile)
            exec (command)
            
            # create a schema from the specification given in the
            # configuration file
            schema = zwcschema.ZWCSchema (zipstream, accessList (configFile, "schemaSpec"), configFile)
    
            # evaluate the contents of this zip file against the schema
            schema.evaluate (zipstream.namelist ())

            # execute also the tearDown
            command = "{0}.tearDown ()".format (configFile)
            eval (command)
            
            # if requested, show a summary with all the information extracted
            # from the zip file
            if (params.show_summary):

                command = "{0}.showSummary ()".format (configFile)
                eval (command)
        
    # invoke the epilogue after the whole process
    command = """import {0}
{0}.epilogue ()""".format (configFile)
    exec (command)        
        

                
# Local Variables:
# mode:python
# fill-column:80
# End:
