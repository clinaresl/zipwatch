# Introduction #

`zipwatch` is a small Python utility used to verify the contents of
zip files and to trigger actions according to their contents, either
because some or found, or because they are not found.


# Dependencies #

`zipwatch` requires Python 3.6 or greater. Other than this, it does
not have any other external dependencies but those explicitly required
by *configuration files* ---see more below.


# Install #

To install the latest version of “zipwatch”:

```bash
pip install "zipwatch"
```

To install a specific version:

```bash
pip install "zipwatch==1.4"
```

To install greater than or equal to one version and less than another:

```bash
pip install "zipwatch>=1,<2"
```

To install a version that’s "compatible" with a certain version: 4

```bash
pip install "zipwatch~=1.4.2"
```

In this case, this means to install any version "==1.4.*" version that’s also ">=1.4.2".

Upgrade an already installed "SomeProject" to the latest from PyPI:

```bash
pip install --upgrade SomeProject
```

# Documentation #

`zipwatch.py` implements a simple workflow which combines information
from a *configuration file*. This configuration file should provide
the following data structure:

* `contentSpec`: it is a list of tuples, each one with three elements:

  + *Regular expression*: if any entry of the zip file matches the
    given regexp, then the *if-then* function declared in this tuple
    is automatically executed
	
  + *If-then function*: function to be automatically invoked in case
    the given regexp matches any entry from the zip file
	
  + *If-else function*: function to be automatically invoked in case
    no entry from the zip file matches this regexp
	
For example, the following entry:

```python
    # warn the user in case (s)he is submitting metadata
    ("(__MACOSX|\._Store)", -1,
     "metadata",
     "")
```

expects directories with the words `__MACOSX` or `._Store` and if they
ever appear, a function called `metadata` is invoked. In case no entry
from the zip file matches this regular expression, no funcdtion is
invoked as `""` was specified as an *if-else* function.

*If-then* functions registered through a *specification schema* are
automatically invoked with the following parameters:

* *zipstream*: it is an instance of `zipFile.ZipFile` with information
  of the zip file
* *regexp*: regular expression matched given as a string
* *content*: specific content found in the zip file that matched the
  regular expression
* *matches*: number of matches of this component

*If-else* functions are automatically invoked with:

* *component*: it is an instance of `zwcschema.ZWCSchemaComponent`
  with information of the component that never matched any content of
  the zip file.

In addition, the configuration file should provide the definition of
the following functions:

* `preamble ()`: to be invoked only once at the beginning of the session
* `setUp ()`: to be invoked before examining the contents of the next zip
  file. It is thus invoked once for each zip file
* `showSummary ()`: to be invoked once if and only if the user requests a
  summary to be shown
* `tearDown ()`: to be invoked after examining the contents of the last
  zip file. It is thus invoked once for each zip file
* `epilogue ()`: to be invoked once as soon as the whole process is over

All these functions take no arguments (as explicitly shown
above). They must be provided so that if they are not necessary they
should contain the single statement `pass`. They are all automatically
invoked by `zipwatch` in the following order:

1. Before starting to process any zip file, `preamble ()` is
   invoked. This function serves to prepare data structures. It is
   therefore invoked only once
2. Before start processing the next zip file, `setUp ()` is
   invoked. Thus, it is invoked as many times as zip files are
   processed.
3. While processing a zip file, various *if-then* and *if-else*
   functions can be invoked according to whether the entries of the
   zip file match or not the entries specified in the *schema
   specification* set up with `contentSpec`.
4. Immediately after processing a zip file, `tearDown ()` is
   invoked. It is then invoked as many times as `setUp ()`.
5. Once all zip files have been processed, `epilogue ()` is invoked
   only once.
   
In addition, `zipwatch.py` honours the directive `--show-summary`
which is implemented just invoking the function `showSummary ()` that
has to be be provided by the configuration file.

By default, `zipwatch.py` expects a configuration file `conf.py` to be
readily available. However, it is possible to provide any arbitrary
configuration file with the directive `--configuration`. A few
examples are shown below.


# Examples #

While `zipwatch` can be used to customize the process of any zip
files, `zipdog.py` is a script distributed with it. The following
examples refer all to this script. All files shown in the examples are
distributed under the directory `examples/`.

In its simplest form, `zipdog` is invoked specifyiing a zip file:

```bash
$ ./zipdog.py --files examples/file-1.zip
 Processing examples/'file-1.zip' ...
---------------------------------------------------------------
 Warning: the folder with the third part 'parte-3/' has not been found
          this does not invalidate your .zip file but be warned that you will not be awarded with
          the extra point granted for doing this part of the lab assignment
```

which uses by default the configuration file `conf.py`. As it can be
seen, `zipdog.py` automatically determines that this specific script
is correct, even if there are some files missing ---expected under a
directory named `parte-3`.

In case a zip file is found to be invalid (because it does not match
the rules given in the *specification schema* of the *configuration
file*), execution immediately halts with a message warning the user:

```bash
$ ./zipdog.py --files examples/file-0.zip 
 Processing 'examples/file-0.zip' ...
---------------------------------------------------------------
 Fatal error: either you did not provide the report in pdf format or you put it in a different
              location. Make sure to locate the pdf report in the root directory. The name should
              adhere to the regular expression given below

 Regular expression: p1-(?P<nia1>\d{6})-(?P<nia2>\d{6})/(?P<nia3>\d{6})-(?P<nia4>\d{6})\.pdf$
 Example           : p1-346089-330696/346089-330696.pdf

 INVALID ZIP FILE!
```

But this is true only when using the default configuration file,
`conf.py`. 

Finally, `zipwatch` is distributed with the following directives:

* `--help`: shows a help banner and exits
* `--version`: shows version information and exit


# License #

`zipwatch` is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

`zipwatch` is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with `zipwatch`.  If not, see <http://www.gnu.org/licenses/>.


# Author #

Carlos Linares Lopez <carlos.linares@uc3m.es>

