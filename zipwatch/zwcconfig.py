#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# zwcconfig.py
# Description: Configuration files
# -----------------------------------------------------------------------------
#
# Login   <carlos.linares@uc3m.es>
#

"""
Configuration files
"""

# imports
# -----------------------------------------------------------------------------
import os                       # file handling
import re                       # matching regular expressions
import sys                      # system accessing

from pathlib import Path        # path handling


# -----------------------------------------------------------------------------
# ZWCConfigFile
#
# Definition of a config file for driving the behaviour of zipwatch
# -----------------------------------------------------------------------------
class ZWCConfigFile:
    """Definition of a config file for driving the behaviour of zipwatch

    """

    def __init__ (self, configFile):
        """registers a configuration file to be used with zipwatch"""

        # copy the attributes
        self._config = configFile

        # now, check it exists and if it does then access its namespace
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
            self._namespace = os.path.splitext (os.path.basename (configFile))[0]
        

    def __getattr__ (self, key):
        """executes the function named by 'key' with no parameters in this configuration
           file and returns the resulting context

        """

        command = """{0}.{1} ()""".format (self._namespace, key)
        return self.execute (command)


    def getConfigFile (self):
        """return the configuration file used for defining this instance"""

        return self._config
    

    def getNamespace (self):
        """return the namespace of this configuration file"""

        return self._namespace
    
        
    def getList (self, component):
        """return the contents of the specified component from this configuration
           file. The component should exist, and it should be defined as a list;
           otherwise the result is undefined

        """

        # create python statements and execute them within an empty context
        command = """lstHandler = {0}.{1}""".format (self._namespace, component)
        return self.execute (command) ["lstHandler"]

    
    def checkList (self, component):
        """verifies that the given component is defined in this configuration file as a list"""

        # create python statements and execute them within an empty context
        command = """{1}_exists = hasattr({0}, \"{1}\")
{1}_is_a_list = {1}_exists and isinstance ({0}.{1}, list)""".format (self._namespace, component)
        context = self.execute (command)

        # now, retrive from the context whether: first, the component exists and
        # second, it is defined as a list
        return context["{0}_is_a_list".format (component)]
        

    def checkFunction (self, component):
        """verifies the given component names a function defined in this configuration file

        """

        # create python statements and execute them within an empty context
        command = """import inspect
{1}_exists = hasattr({0}, \"{1}\")
{1}_is_function = {1}_exists and inspect.isfunction ({0}.{1})""".format (self._namespace, component)
        context = self.execute (command)

        # now, retrive from the context whether: first, the component exists and
        # second, it is defined as a function
        return context["{0}_exists".format (component)] and context["{0}_is_function".format (component)]
    

    def verify (self):
        """verifies the contents of this configFile, i.e., that all necessary functions
           and data structures are given.

           The following items are mandatory:

           * Lists:
                contentSpec - With the specification of all expected matches

           * Functions:
                preamble
                setup
                tearDown
                epilogue
                onSummary
                onError

                In addition, all if-then and if-else functions registered in the
                schema should be given in this configuration file

        """

        # check the existence of the list contentSpec
        if not self.checkList ("contentSpec"):
            print (" Fatal error: the component 'contentSpec' has not been found in module '{0}'".format (self._config))
            sys.exit (1)

        # verify that all functions given in the schema specification are also implemented
        for ischema in self.getList ("contentSpec"):

            if len (ischema) != 3:
                print (" Fatal error: the schema '{0}' from 'contentSpec' has an incorrect number of arguments".format (ischema))
                sys.exit (1)

            # note that while the schema should consist of precisely three
            # arguments, it is possible to give the empty string as an if-then
            # function
            if ischema[1] and not self.checkFunction (ischema[1]):
                print (" Fatal error: the if-then function '{0}' has not been found in module '{1}'".format (ischema[1], self._config))
                sys.exit (1)

            # likewise, it is also allowed to specify the empty string as an else
            # function
            if ischema[2] and not self.checkFunction (ischema[2]):
                print (" Fatal error: the if-else function '{0}' has not been found in module '{1}'".format (ischema[2], self._config))
                sys.exit (1)

        # check the existence of the mandatory functions
        for icomponent in ["preamble", "setUp", "tearDown", "epilogue", "onSummary", "onError"]:

            if not self.checkFunction (icomponent):
                print (" Fatal error: the component '{0}' has not been found in module '{1}'".format (icomponent, self._config))
                sys.exit (1)
    

    def onError (self, message):
        """automatically invoke the 'onError' service provided in the configuration file
           of this instance

        """
        
        command = """{0}.onError (message)""".format (self._namespace, message)
        context = {
            'message' : message
        }
        self.execute (command, context)

                
    def execute (self, command, context=dict ()):
        """executes the given comman within the given context. It returns the resulting
               context
        
        """

        # just execute the given command within the configuration file by
        # prepending an import statement to it and return the resulting context
        command = """import {0}
{1}""".format (self._namespace, command)
        exec (command, context)
        
        return context
            

        
            
# Local Variables:
# mode:python
# fill-column:80
# End:
