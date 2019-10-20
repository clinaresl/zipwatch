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
import argparse                   # argument parsing
import sys                        # system accessing
import zipfile                    # zip files management

import zwcconfig
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

    # create a configuration file and verify all its contents
    configFile = zwcconfig.ZWCConfigFile (params.configuration)
    configFile.verify ()

    # invoke the preamble before starting the whole process
    configFile.preamble
        
    # for all files given in the command-line
    for ifile in params.files:

        print (" Processing '{0}' ...".format (ifile))
        print ("---------------------------------------------------------------")

        # list the contents of this file
        with zipfile.ZipFile (ifile) as zipstream:

            # execute the pramble of the configuration file
            configFile.setUp
            
            # create a schema from the specification given in the
            # configuration file
            schema = zwcschema.ZWCSchema (zipstream, configFile.getList ("schemaSpec"), configFile)
    
            # evaluate the contents of this zip file against the schema
            schema.evaluate (zipstream.namelist ())

            # execute also the tearDown
            configFile.tearDown
            
            # if requested, show a summary with all the information extracted
            # from the zip file
            if (params.show_summary):
                configFile.onSummary
        
    # invoke the epilogue after the whole process
    configFile.epilogue
        

                
# Local Variables:
# mode:python
# fill-column:80
# End:
