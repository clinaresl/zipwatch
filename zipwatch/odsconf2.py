#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# conf.py
# Description: Configuration file for lab assignment #1
# -----------------------------------------------------------------------------
#
# Login   <carlos.linares@uc3m.es>
#

"""
Configuration file for lab assignment #1 (professor version) - Heuristics and Optimization
"""

# imports
# -----------------------------------------------------------------------------
import os                       # file handling
import re                       # matching regular expressions
import sys                      # system accessing

import pyexcel

# CONTENTS
# -----------------------------------------------------------------------------
# This file contains the specification of a schema and other functions that are
# necessary to correctly interpret all components of the schema and also to
# provide a summary of the information extracted from the zip file
#
# A module to be usable by zipwatch should contain all or some of the following
# items with the names given below:
#
# contentSpec: schema definition
#
# functions:
#
#       preamble (optional): to be invoked only once at the beginning of the
#                            session
#       setUp (optional): to be invoked before examining the contents of the
#                         next zip file. It is thus invoked once for each zip
#                         file
#       tearDown (optional): to be invoked after examining the contents of the
#                            last zip file. It is thus invoked once for each zip
#                            file
#       epilogue (optional): to be invoked once as soon as the whole process is
#       over
#       onSummary (mandatory): to be invoked once if and only if the user
#                              requests a summary to be shown
#       onError (mandatory): automatically invoked by zipwatch in case of error,
#                            e.g., invalid zip file. It can be also invoked by
#                            services implemented in this module. It takes only
#                            one argument, an error message
#       onAbort (mandatory): automatically invoked by zipwatch in case of an
#                            error reported by the configuration file, e.g.,
#                            incorrect contents of a zip file
#
# Whether these functions are mandatory or optional is given in the list
# above.
#
# The following list provides a comprehensive view of the arguments
# automatically used in the invocation of each function
#
#
#                      | zipstream | zipfile | msg |
#           -----------+-----------+---------+-----+
#           preamble   |           |         |     |
#           setup      |     x     |         |     |
#           tearDown   |     x     |         |     |
#           epilogue   |           |         |     |
#           -----------+-----------+---------+-----+
#           onSummary  |     x     |         |     |
#           onError    |           |    x    |  x  |
#           onAbort    |           |    x    |     |
#           -----------+-----------+---------+-----+
#
# where
#
#    zipstream: is an instance of the zipstream.ZipStream been watched
#    zipfile  : full path to the zipfile been watched as a string
#    msg      : a descriptive message string
#
# the schema specification might define other functions which should be of
# course defined, i.e., they are mandatory

# SCHEMA DEFINITION:
# -----------------------------------------------------------------------------
# the schema should be given as a list of tuples, each one containing
# the following information:
#
#    1. Regular expression that might be matched by one specific
#       filename/directory in the zip file
#
#    2. if-then action. It is a function provided in this file which should be
#       invoked if a specific file/directory matches the regular expression
#       given in first position.
#
#       These functions receive the following arguments:
#          1. Instance of the zipstream.ZipStream been watched
#          2. Regular expression matched
#          3. Specific content that matched the regular expression
#          4. Number of matches of this component
#
#       If no action should be taken when the regular expression matches any of
#       the contents of the zipfile, None can be given. Otherwise, the
#       corresponding if-then function should be provided in the configuration
#       file.
#
#    3. if-else action. It is a function provided in this file which should be
#       invoked in case no file/directory in the zip file matched the given
#       expression.
#
#       These functions receive the following arguments:
#          1. schema component missing
#
#       In case no matching a specific schema component is a fatal error, the
#       corresponding if-else function should exit automatically, i.e., it is
#       not the responsibility of zipwatch to verify the severity of errors
#
#       If no action should be taken in case of unmatch, None can be
#       given. Otherwise, the corresponding if-else function should be provided
#       in the configuration file.

# IF-THEN ACTIONS
# -----------------------------------------------------------------------------
# if-then actions are ordinary functions that receive the following arguments:
#
#    1. instance of a zipfile.ZipFile used to access the zip file
#    2. Regular expression matched
#    3. Specific content that matched the regular expression
#    4. Number of matches of this component
#
# and can be used to do anything, e.g., registering data in a class that records
# useful information from the zip file

# IF-ELSE ACTIONS
# -----------------------------------------------------------------------------
# if-else actions are ordinary functions that receive the following arguments:
#    1. schema component missing
#
# which is an instance of zwcschema.ZWCSchemaComponent

# preamble
# -----------------------------------------------------------------------------
# this function is optional. If given, it is invoked automatically by zipwatch
# only once before starting processing any zip file.

# setUp
# -----------------------------------------------------------------------------
# this function is optional. If given, it is invoked automatically by zipwatch
# before starting to process the contents of a zipfile. It can be used to
# initialize structures.

# tearDown
# -----------------------------------------------------------------------------
# this function is optional. If given, it is invoked automatically by zipwatch
# after processing the contents of a zipfile. It can be used to clean-up
# structures or to start other processes with the information retrieved from the
# zipfile.

# epilogue
# -----------------------------------------------------------------------------
# this function is optional. If given, it is invoked automatically by zipwatch
# only once after processing all zip files.

# onSummary
# -----------------------------------------------------------------------------
# this function is mandatory and should be provided in this module. It would be
# invoked automatically by zipwatch in case the user explicitly requested seeing
# a summary of all the relevant information extracted from the zip file

# onError
# -----------------------------------------------------------------------------
# this function is mandatory and should be provided in this module. It is
# invoked automatically by zipwatch in case of error, e.g., bad zip file. It
# could be also invoked by services implemented in this module

# onAbort
# -----------------------------------------------------------------------------
# automatically invoked by zipwatch in case of an error reported by the
# configuration file, e.g., incorrect contents of a zip file

# SCHEMA DEFINITION:
# -----------------------------------------------------------------------------
# create the schema specification by hand
contentSpec = [
        
    # report in pdf format
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/(?P<nia3>\d{6})(-(?P<nia4>\d{6}))?\.pdf$',
     "report",
     "reportKO"),
    
    # authors 
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/autores\.txt$',
     "authors",
     "authorsKO"),
    
    # directory of the first part of the lab assignment
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/parte-1/$',
     "part1Directory",
     "part1DirectoryKO"),
    
    # directory with the solutions to the first part of the lab
    # assignment
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/parte-1/.+$',
     "part1File",
     "part1FileKO"),
    
    # directory with the second part of the lab assignment
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/parte-2/$',
     "part2Directory",
     "part2DirectoryKO"),
    
    # directory with the solutions to the second part of the lab
    # assignment
    (r'p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/parte-2/.+$',
     "part2File",
     "part2FileKO"),
    
    # warn the user in case (s)he is submitting metadata
    (r'(__MACOSX|\._Store)',
     "metadata",
     None)
    
]

# Classes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Summary
#
# Records all the relevant information from the zip file
# -----------------------------------------------------------------------------
class Summary:

    # by registering all the information in static data members there
    # is no need to move back and forth instances of this class

    # this class records information of a team which is made of either two
    # students or only one (which is not desired, certainly but that might be
    # eventually the case)
    _nia1 = 0
    _nia2 = None

    _name1 = ""
    _surname1 = ""

    _name2 = ""
    _surname2 = ""

    _report = ""
    
    _part1Directory = False
    _part1Files = []

    _part2Directory = False
    _part2Files = []

    def __str__ (self):
        """provides a human readable version of the contents of this class"""

        stream  = " * NIA1    : {0}\n".format (Summary._nia1)
        stream += " * Surname1: {0}\n".format (Summary._surname1)
        stream += " * Name1   : {0}\n".format (Summary._name1)
        stream += "\n"

        # in case there is a second student registered
        if Summary._nia2:
            stream += " * NIA2    : {0}\n".format (Summary._nia2)
            stream += " * Surname2: {0}\n".format (Summary._surname2)
            stream += " * Name2   : {0}\n".format (Summary._name2)
            stream += "\n"

        stream += " * Report  : {0}\n".format (Summary._report)
        stream += "\n"
    
        folder = "Yes" if Summary._part1Directory else "No"
        stream += " * First part of the lab assignment:\n"
        stream += " \tFolder present: {0}\n".format (folder)
        if Summary._part1Files:
            stream += "\tFiles:\n"
            for ifile in Summary._part1Files:
                stream += "\t\t{0}\n".format (ifile)
        stream += "\n"
    
        folder = "Yes" if Summary._part2Directory else "No"
        stream += " * Second part of the lab assignment:\n"
        stream += " \tFolder present: {0}\n".format (folder)
        if Summary._part2Files:
            stream += "\tFiles:\n"
            for ifile in Summary._part2Files:
                stream += "\t\t{0}\n".format (ifile)
        stream += "\n"
    
        return stream


# -----------------------------------------------------------------------------
# ODSContent
#
# Records all the information to be shown on a single line of the spreadsheet
# -----------------------------------------------------------------------------
class ODSContent:
    """Records all the information to be shown on a single line of the
       spreadsheet"""

    def __init__ (self, nia, surname, name, cspCode, searchCode):
        """records the information to be shown for a single student with information
           extracted from the zip file"""

        # record all attributes
        (self._nia, self._surname, self._name, self._cspCode, self._searchCode) = \
            (nia, surname, name, cspCode, searchCode)

    def get (self):
        """returns a list with the information of this instance"""

        return [self._nia, self._surname, self._name, self._cspCode, self._searchCode]
        

# -----------------------------------------------------------------------------
# ODSContents
#
# Records all the information to be shown on the ods sheet
# -----------------------------------------------------------------------------
class ODSContents:
    """Records all the information to be shown on the ods sheet"""

    _entries = []

    def __add__ (self, other):
        """adds a new entry to this collection"""

        # verify the new entry is given indeed as an instance of ODSContent
        if not isinstance (other, ODSContent):
            print (" Fatal error: ODSContents is a container of instances of ODSContent only!")
        
        self._entries.append (other)
        return self
    
    
    def __str__ (self):
        """provides a human readable version of the contents of this class"""

        stream = ""
        for entry in self._entries:
            stream += "{0}".format (entry)

        return stream

    
# -----------------------------------------------------------------------------
# ODSStatus
#
# Records the status of a single zip file
# -----------------------------------------------------------------------------
class ODSStatus:
    """Records the status of a single zip file"""

    def __init__ (self, zipfile, status):
        """records the status of a single zip file"""

        # record all attributes
        (self._zipfile, self._status) = (zipfile, status)

    def get (self):
        """returns a list with the information of this instance"""

        return [self._zipfile, self._status]
        

# -----------------------------------------------------------------------------
# ODSStatuses
#
# Records the status of all zip files processed so far
# -----------------------------------------------------------------------------
class ODSStatuses:
    """Records the status of all zip files processed so far"""

    _entries = []

    def __add__ (self, other):
        """adds a new entry to this collection"""

        # verify the new entry is given indeed as an instance of ODSStatus
        if not isinstance (other, ODSStatus):
            print (" Fatal error: ODSStatuses is a container of instances of ODSStatus only!")
        
        self._entries.append (other)
        return self
    
    
    def __str__ (self):
        """provides a human readable version of the contents of this class"""

        stream = ""
        for entry in self._entries:
            stream += "{0}".format (entry)

        return stream


# -----------------------------------------------------------------------------
# CheckList
#
# Creates a checklist for evaluating the lab assignments, one for each team
# -----------------------------------------------------------------------------
class CheckList:

    def __init__ (self, nia1, nia2):
        """records the status of a single entry in the checklist"""

        # record all attributes
        (self._nia1, self._nia2) = (nia1, nia2)

    def get (self):
        """returns a list with the information of this instance"""

        return [self._nia1, self._nia2]

    
# -----------------------------------------------------------------------------
# CheckLists
#
# Container for each check list
# -----------------------------------------------------------------------------
class CheckLists:

    _entries = []
    
    def __add__ (self, other):
        """adds a new entry to this collection"""

        # verify the new entry is given indeed as an instance of CheckList
        if not isinstance (other, CheckList):
            print (" Fatal error: CheckLists is a container of instances of CheckList only!")
        
        self._entries.append (other)
        return self
    
    
    def __str__ (self):
        """provides a human readable version of the contents of this class"""

        stream = ""
        for entry in self._entries:
            stream += "{0}".format (entry)

        return stream

    
# Functions
# -----------------------------------------------------------------------------

# verifies the root directory of the specified contents
def verifyRootDirectory (content):
    """verifies the root directory of the specified contents"""

    # match the contents of this content against a regular expression of the
    # root directory
    rootregexp = r'^p2-(?P<nia1>\d{6})(-(?P<nia2>\d{6}))?/'
    m = re.match (rootregexp, content)
    if not m:
        print (" Fatal error: the root directory has not been found")
        print ("              upon decompressing the zip file, all files should be under a directory matching")
        print ("              the regular expression given below")
        print ()
        print (" Regular expression: '{0}'".format (rootregexp))
        print (" Examples          : p2-743902/, p2-346089-330696/")
        print ()
        print (" INVALID ZIP FILE!")

        raise SystemExit

    # if the content matched this expression verify that NIAs are used
    # consistently
    (nia1, nia2) = (m.group ('nia1'), m.group ('nia2'))
    if (Summary._nia1 or Summary._nia2) and \
       ( (Summary._nia1 != nia1 and Summary._nia1 != nia2) or
         (Summary._nia2 != nia1 and Summary._nia2 != nia2) ):
        print (" Fatal error: NIAs are not used consistently")
        print ("              verify the structure of your .zip file and make sure that all directories are")
        print ("              correctly named after the NIAs of each member of the team and that they are")
        print ("              the same used in the 'authors.txt' file")
        print ()

        raise SystemExit

    # finally, if no NIAs have been registered yet, do now
    if not Summary._nia1 and not Summary._nia2:
        (Summary._nia1, Summary._nia2) = (nia1, nia2)
    
# retrieve the name, surname and NIA of a student from the contents of the
# 'authors' file
def getStudentInfo (content):
    """retrieve the name, surname and NIA of a student from the contents of the
       'authors' file

    """

    # parse the contents of this line
    pattern = re.compile (r'\s*(?P<nia>\d{6})\s*(?P<surname>[^,]+),\s+(?P<name>[^\s]+)\s*', re.UNICODE)
    m = re.match (pattern, content.decode ("utf-8", "ignore"))

    # in case the regular expression does not match
    if not m:
        print (" Fatal error: it is not possible to extract the students info from the following line")
        print ("              {0}".format (content))
        print ()
        print ("INVALID ZIP FILE")

        raise SystemExit

    # otherwise, return the fields
    return (m.group ('nia'), m.group ('surname'), m.group ('name'))
    
        
# IF-THEN ACTIONS
# -----------------------------------------------------------------------------

# all if-then functions registered in the schema receive the following args:
#
#    1. instance of a zipfile.ZipFile used to access the zip file
#    2. Regular expression matched
#    3. Specific content that matched the regular expression
#    4. Number of matches of this component
#
# note that all contents certainly match the regexp

# acknowledges the presence of the report
def report (zipstream, regexp, content, matches):
    """acknowledges the presence of the report"""

    # verify the root directory
    verifyRootDirectory (content)
    
    # extract information
    m = re.match (regexp, content)
    (nia1, nia2, nia3, nia4) = (m.group ('nia1'), m.group ('nia2'), m.group ('nia3'), m.group ('nia4'))

    # error checking
    if ((nia1 != nia3 and nia1 != nia4) or
        (nia2 != nia3 and nia2 != nia4)):
        print (" Fatal error: mismatched NIAs in the report. Missed coincidence with the directory name")
        raise SystemExit
        
    # record the presence of the report
    Summary._report = os.path.basename (content)

# acknowledges the presence of the authors file
def authors (zipstream, regexp, content, matches):
    """acknowledges the presence of the authors file"""

    # verify the root directory
    verifyRootDirectory (content)

    # retrieve the contents of the authors file
    with zipstream.open (content) as stream:

        # retrieve the contents of the students ids
        ids = stream.readlines ()

        # and now remove blank lines (those containing only spaces)
        ids = [line for line in ids if line.strip ()]
        
        # if there are not exactly two lines then immediately raise an error
        if not len (ids) or len (ids) > 2:
            print (" Fatal error: the file 'authors.txt' should contain the information of one or two students,")
            print ("              one per line, following the regexp shown below")
            print ()
            print (r' Regexp: \s*(?P<nia1>\d{6})\s*(?P<surname1>[^,]+),\s+(?P<name1>.*)')
            print (" Example: 671342 Turing, Alan")

        # retrieve information from that line
        (nia1, surname1, name1) = getStudentInfo (ids[0])
        if len (ids) > 1:
            (nia2, surname2, name2) = getStudentInfo (ids[1])
        else:
            (nia2, surname2, name2) = (None, "", "")

        # if the content matched this expression verify that NIAs are used
        # consistently
        if (Summary._nia1 and Summary._nia2) and \
           ( (Summary._nia1 != nia1 and Summary._nia1 != nia2) or
             (Summary._nia2 != nia1 and Summary._nia2 != nia2) ):
            print (" Fatal error: NIAs are not used consistently")
            print ("              verify the structure of your .zip file and make sure that all directories are")
            print ("              correctly named after the NIAs of each member of the team and that they are")
            print ("              the same used in the 'authors.txt' file")
            print ()

            raise SystemExit

        # if no NIAs have been registered yet, do now
        if not Summary._nia1 and not Summary._nia2:
            (Summary._nia1, Summary._nia2) = (nia1, nia2)

        # in any case register the students names
        if (Summary._nia1 == nia1):
            (Summary._name1, Summary._surname1) = (name1, surname1)
        
        if (Summary._nia1 == nia2):
            (Summary._name1, Summary._surname1) = (name2, surname2)
        
        if (Summary._nia2 == nia1):
            (Summary._name2, Summary._surname2) = (name1, surname1)
        
        if (Summary._nia2 == nia2):
            (Summary._name2, Summary._surname2) = (name2, surname2)
        

# acknowledges the presence of the folder containing the first part
def part1Directory (zipstream, regexp, content, matches):
    """acknowledges the presence of the folder containing the first part"""

    # verify the root directory
    verifyRootDirectory (content)
    
    # record the presence of the directory with the first part of the
    # lab assignment
    Summary._part1Directory = True

# acknowledges the presence of a file in the folder containing the first part
def part1File (zipstream, regexp, content, matches):
    """acknowledges the presence of a file in the folder containing the first part"""

    # verify the root directory
    verifyRootDirectory (content)
    
    # record the existence of this file in the first part of the lab
    # assignment
    Summary._part1Files.append (os.path.basename (content))

# acknowledges the presence of the folder containing the second part
def part2Directory (zipstream, regexp, content, matches):
    """acknowledges the presence of the folder containing the second part"""

    # verify the root directory
    verifyRootDirectory (content)
    
    # record the presence of the directory with the second part of the
    # lab assignment
    Summary._part2Directory = True

# acknowledges the presence of a file in the folder containing the second part
def part2File (zipstream, regexp, content, matches):
    """acknowledges the presence of a file in the folder containing the second part"""

    # verify the root directory
    verifyRootDirectory (content)
    
    # record the existence of this file in the second part of the lab
    # assignment
    Summary._part2Files.append (os.path.basename (content))

    
# warn the user in case (s)he is submitting metadat
def metadata (zipstream, regexp, content, matches):
    """warn the user in case (s)he is submitting metadata"""

    print (" Warning: your zip file contains metadata (__MACOSX/ and .DS_Store) which are neither required")
    print ("          nor necessary. While this does not invalidate your .zip please seriously consider")
    print ("          excluding those files from your zip. For this it just suffixes using the following")
    print ("          additional arguments to your zip command:")
    print ('                                -x ".*" -x "__MACOSX"')
    print ()
    print (' Example: zip -r ~/p2-346089-330696.zip . -x ".*" -x "__MACOSX"')
    
# IF-ELSE ACTIONS
# -----------------------------------------------------------------------------

# all if-else functions registered in the schema receive the following args:
#
#    1. schema component missing
#
# note that all contents certainly match the regexp

# reports that the report has not been found in its expected location
def reportKO (component):
    """reports that the report has not been found in its expected location"""

    print (" Fatal error: either you did not provide the report in pdf format or you put it in a different")
    print ("              location. Make sure to locate the pdf report in the root directory. The name should")
    print ("              adhere to the regular expression given below")
    print ()
    print (" Regular expression: {0}".format (component.getRegexp ()))
    print (" Example           : p2-346089-330696/346089-330696.pdf")
    print ()
    print (" INVALID ZIP FILE!")

    Summary._report = None
    
# reports that the authors file has not been provided
def authorsKO (component):
    """reports that the authors file has not been provided"""

    print (" Fatal error: either you did not provide the authors file or you put it in a different location.")
    print ("              Make sure to locate the authors file in the root directory. The name should adhere")
    print ("              to the regular expression given below")
    print ()
    print (" Regular expression: {0}".format (component.getRegexp ()))
    print (" Example           : p2-346089-330696/autores.txt")
    print ()
    print (" INVALID ZIP FILE!")

    # this is considered a system error because there is no one to attribute the
    # error so that execution should immediately halt
    raise SystemExit
    
# reports that the folder containing the first part has not been found
def part1DirectoryKO (component):
    """reports that the folder containing the first part has not been found.

       This is not a fatal error, but the user should be warned much the same"""

    print (" Warning: the folder with the first part 'parte-1/' has not been found")
    print ("          this does not invalidate your .zip file but be warned that your first part will score 0")
    print ()

    Summary._part1Directory = False

# reports that the folder containing the first part contains no files
def part1FileKO (component):
    """reports that the folder containing the first part contains no files.

       This is not a fatal error, but the user should be warned much the same"""

    # show the message only in case the directory was found, otherwise, it is
    # obvious there are no files within an unexistent directory! ;)
    if (Summary._part1Directory):
    
        print (" Warning: the folder with the first part 'parte-1/' contains no files")
        print ("          this does not invalidate your .zip file but be warned that your first part will score 0")
        print ()

    Summary._part1Files = []
    
# reports that the folder containing the second part has not been found
def part2DirectoryKO (component):
    """reports that the folder containing the second part has not been found.

       This is not a fatal error, but the user should be warned much the same"""

    print (" Warning: the folder with the second part 'parte-2/' has not been found")
    print ("          this does not invalidate your .zip file but be warned that your second part will score 0")
    print ()

    Summary._part2Directory = False

# reports that the folder containing the second part contains no files
def part2FileKO (component):
    """reports that the folder containing the second part contains no files.

       This is not a fatal error, but the user should be warned much the same"""

    # show the message only in case the directory was found, otherwise, it is
    # obvious there are no files within an unexistent directory! ;)
    if (Summary._part2Directory):
    
        print (" Warning: the folder with the second part 'parte-2/' contains no files")
        print ("          this does not invalidate your .zip file but be warned that your second part will score 0")
        print ()

    Summary._part2Files = []
    

# preamble
# -----------------------------------------------------------------------------
def preamble ():
    """function invoked automatically before starting to process the contents of any
       zipfile"""

    ODSContents._entries = []
    ODSStatuses._entries = []
    

# setUp
# -----------------------------------------------------------------------------
def setUp (zipstream):
    """function invoked automatically before starting to process the contents of a
       zip file"""

    # initialize the static data members of the Summary
    Summary._nia1 = 0
    Summary._nia2 = None

    Summary._name1 = ""
    Summary._surname1 = ""

    Summary._name2 = ""
    Summary._surname2 = ""

    Summary._report = ""
    
    Summary._part1Directory = False
    Summary._part1Files = []

    Summary._part2Directory = False
    Summary._part2Files = []


# tearDown
# -----------------------------------------------------------------------------

# add a new entry to the contents to be shown on the ods file
def tearDown (zipstream):
    """add a new entry to the contents to be shown on the ods file"""

    # --contents of the lab assignment
    odscontents = ODSContents ()
    
    # determine the entries of a new line in the spreadsheet
    cspCode     = "" if Summary._part1Files else "0"
    searchCode  = "" if Summary._part2Files else "0"
    
    odsline1 = ODSContent (Summary._nia1, Summary._surname1, Summary._name1, cspCode, searchCode)
    odscontents = odscontents + odsline1

    # if and only if two members are in this group then create an entry for both
    if Summary._nia2:
        odsline2 = ODSContent (Summary._nia2, Summary._surname2, Summary._name2, cspCode, searchCode)
        odscontents = odscontents + odsline2

    # -- status
    odsstatuses = ODSStatuses ()
    odsstatus = ODSStatus (zipstream.filename, "SUCCESSFUL")
    odsstatuses = odsstatuses + odsstatus

    # -- checklist
    checklists = CheckLists ()
    checklist = CheckList (Summary._nia1, Summary._nia2)
    checklists = checklists + checklist
        
    
# epilogue
# -----------------------------------------------------------------------------
def epilogue ():
    """function invoked automatically after processing the contents of all zip files"""

    # create the contents of an ods file
    contents = [["NIA", "Apellidos", "Nombre",
                 "Modelo", "Implementacion", "Resolucion",
                 "Modelo", "Implementacion", "Resolucion",
                 "Analisis", "Penalizacion", "Total"]]
    
    # for all entries processed so far
    for entry in ODSContents._entries:

        # add the information of this entry
        contents.append ([entry._nia, entry._surname, entry._name,
                          "", entry._cspCode, "",
                          "", entry._searchCode, "",
                          "", "", ""])

    # process now the status of all zip files
    statuses = [["Filename", "Status"]]

    # for all zip files processed so far
    for entry in ODSStatuses._entries:

        # add the status of this zip file 
        statuses.append (entry.get ())

    # save both sheets in the same spreadsheet
    bookdict = {
        'Status' : statuses,
        'Entries': contents
    }
    book = pyexcel.get_book (bookdict = bookdict)
    book.save_as ("report.ods")

    # also, create a checklist for each entry

    # first, get the template
    with open ("templates/template2.org", "rt", encoding='utf-8') as orgstream:
        contents = orgstream.read ()

    # now, open a file to write the checklists
    with open ("reviews.org", "w") as orgstream:

        for entry in CheckLists ()._entries:
            if entry._nia1 and not entry._nia2:
                orgstream.write ("* " + str (entry._nia1))
            else:
                orgstream.write ("* " + str (entry._nia1) + "-" + entry._nia2)
            orgstream.write (contents)        


# onSummary
# -----------------------------------------------------------------------------
def onSummary (zipstream):
    """shows a report summary of all info extracted from the zip file"""

    summary = Summary ()
    print (summary)

    
# onError
# -----------------------------------------------------------------------------
def onError (msg, zipfile):
    """take an action in case of error such as bad zip file"""

    # print the message
    print (" Fatal Error in file {0}: {1}".format (os.path.basename (zipfile), msg))

    # -- status
    odsstatuses = ODSStatuses ()
    odsstatus = ODSStatus (zipfile, "FATAL ERROR")
    odsstatuses = odsstatuses + odsstatus
    
# onAbort
# -----------------------------------------------------------------------------
def onAbort (zipfile):
    """take an action in case this configuration file halted execution"""

    print (" Aborting file {0} ...".format (os.path.basename (zipfile)))

    # -- status
    odsstatuses = ODSStatuses ()
    odsstatus = ODSStatus (zipfile, "ABORTED")
    odsstatuses = odsstatuses + odsstatus
    
    

# Local Variables:
# mode:python
# fill-column:80
# End:
