#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# zwcschema.py
# Description: defines the schema the contents of a zip file are compared with
# -----------------------------------------------------------------------------
#
# Login   <carlos.linares@uc3m.es>
#

"""
defines the schema the contents of a zip file are compared with
"""

# imports
# -----------------------------------------------------------------------------
import re                       # matching regular expressions
import sys                      # system accessing
import zipfile                  # zip files management

# -----------------------------------------------------------------------------
# ZWCSchemaComponent
#
# Definition of a single component of a schema
# -----------------------------------------------------------------------------
class ZWCSchemaComponent:
    """Definition of a single component of a schema

    """

    def __init__ (self, configFile, regexp, if_then, if_else):
        """registers a single component with:

        configFile - configuration file given as a Python module

        regexp - regular expression to be verified. It might contain
                 groups to be used by other functions

        if_then - action to take in case of matching

        if_else - action to take in case of no matching

        """

        # copy the attributes
        (self._configFile, self._regexp, self._if_then, self._if_else) = \
            (configFile, regexp, if_then, if_else)

        # and initialize the number of matches to zero
        self._matches = 0


    def __str__ (self):
        """return a human readable version of this component"""

        stream = """ configFile : {0}
 regexp     : {1}
 if_then    : {2}
 if_else  : {3}""".format (self._configFile, self._regexp, self._if_then, self._if_else)

        return stream


    def get_regexp (self):
        """return the regexp of this component"""

        return self._regexp
    

    def get_matches (self):
        """return the number of matches of this component"""

        return self._matches
    

    def set_matches (self, value):
        """set the number of matches of this component to the given value"""

        self._matches = value
    

    def evaluate (self, instance):
        """returns whether the given instance is verified by this
           component. If so, the number of matches is incremented

        """

        # apply the regular expression of this component to this
        # instance
        m = re.match (self._regexp, instance)

        # if necessary, update the number of matches
        if m:
            self._matches += 1

        # finally return whether there was a match or not
        return m != None

    def executeIfThen (self, zipstream, content):
        """execute the if-then registered function of this component for the content
           that matched it and the zipstream from where it was extracted

        """

        # just execute the if-then function registered in this component. For
        # this create a context with the values of all parameters passed to the
        # if-then function
        command = """import {0}
{0}.{1} (zipstream, regexp, content, matches)""".format (self._configFile, self._if_then)
        context = {
            'zipstream' : zipstream,
            'regexp' : self._regexp,
            'content' : content,
            'matches' : self._matches
        }
        
        exec (command, context)
    

    def executeIfElse (self):
        """execute the if-else registered function of this component for the content
           that matched it and the zipstream from where it was extracted

        """

        # just execute the if-then function registered in this component. For
        # this create a context with the values of all parameters passed to the
        # if-then function
        command = """import {0}
{0}.{1} (component)""".format (self._configFile, self._if_else)
        context = {
            'component' : self
        }
        
        exec (command, context)
    

# -----------------------------------------------------------------------------
# ZWCSchema
#
# Definition of a schema to use for verifying the contents of a zip file
# -----------------------------------------------------------------------------
class ZWCSchema:

    """Definition of a schema to use for verifying the contents of a zip file"""

    def __init__ (self, zipstream, schema, configFile):
        """Initializes a schema for processing a zipfile from the contents of a list of
           tuples using those definitions specified in the given configuration file

        """

        # error checking - verify that the zipstream is an instance of a zipfile
        if not isinstance (zipstream, zipfile.ZipFile):
            print (" Fatal error: the zipstream is not an instance of zipfile")
            sys.exit (1)
        
        # error checking - verify that the given schema is a list
        if not isinstance (schema, list):
            print (" Fatal error: the schema '{0}' has not been given as a list".format (schema))
            sys.exit (1)

        # and also that it is not empty
        if not len (schema):
            print (" Fatal error: empty schemas are just worthless!")
            sys.exit (1)
        
        # error checking - verify now that all items of the schema are given as
        # tuples with precisely three items each
        for ischema in schema:
            if not isinstance (ischema, tuple):
                print (" Fatal error: the component '{0}' has not been given as a tuple".format (ischema))
                sys.exit (1)

            if len (ischema) != 3:
                print (" Fatal error: the component '{0}' has an incorrect number of arguments".format (ischema))
                sys.exit (1)

        # copy the zipstream and the configuration file
        self._zipstream = zipstream
        self._configFile = configFile

        # create a container with schema components of all tuples given in the
        # schema
        self._components = list ()
        for ischema in schema:
            self._components.append (ZWCSchemaComponent (configFile,
                                                         ischema[0], ischema[1], ischema[2]))
            

    def __str__ (self):
        """provides a human readable version of this schema"""

        stream = ""
        for component in self._components:
            stream += component.__str__ () + "\n\n"

        return stream

    
    def evaluate (self, contents):
        """return whether the given contents are compliant with this schema"""

        # -- error checking - verify that the contents are given as a list of
        #                     strings
        if not isinstance (contents, list):
            print (" Fatal error: the contents '{0}' have not been given as a list".format (contents))
            sys.exit (1)

        for icontent in contents:
            if not isinstance (icontent, str):
                print (" Fatal error: the content '{0}' is not a string".format (icontent))
                sys.exit (1)
        
        # evaluation is done in cooperation with the components of the
        # schema. While the components verify whether a specific content matches
        # it, it is the schema which takes care of consistency as a whole
        for icontent in contents:                            # for each content

            for icomponent in self._components:            # for each component

                # if this component matches this content
                if icomponent.evaluate (icontent):

                    # if this component matched this content, then apply its
                    # if-then function if any was given
                    icomponent.executeIfThen (self._zipstream, icontent)
                    break

        # verify whether there are components of this schema that have not matched
        for icomponent in self._components:

            # if this specific component never matched any entry of the zip file
            # invoke its if-else function
            if not icomponent.get_matches () and icomponent._if_else:

                icomponent.executeIfElse ()
            
            
# Local Variables:
# mode:python
# fill-column:80
# End:
