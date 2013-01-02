# Author: Sam Hopkins, 2012

# This script builds the website by merging a template file and content files.
# To add a new file, add an entry to PAGES, add a file <your_file>.content to
# src/, and if you want to be able to link to it, add an entry to the navbar,
# which lives in src/globals.
#
# Must be run from the top level directory -- i.e. run
#
#     python scripts/build.py

# Various possible improvements:
#   --build links and navbar for you
#   --?

import re
import os
import shutil
import sys

# location of source files
SRC_PATH = os.path.abspath('./src')

# location of destination files 
# (remove or add 'test' to build to the sandbox or build to prod)
DST_PATH = os.path.abspath('./')

# list of pages to build, and with what template
PAGES = {
          'index' : 'main', 
          'research' : 'main',
          'notes' : 'main',
          'school' : 'main',
          'personal' : 'main'
        }

# location of global content
GLOBAL_PATH = os.path.abspath('./src/globals')

# useful regexes
var_use_regex = r'(\$)(.*)(\$)'
var_decl_regex = r'(\@BEGIN\s*)(.*)(:)([^\@]*)(\@END)'

# singleton for global declarations
_globals = None

# reads declarations in src and returns them in a dict
def load_decls(src):
  env = {}
  for m in re.finditer(var_decl_regex, src):
    env[m.group(2)] = m.group(4)
  return env

# singleton
def get_globals():
  global _globals
  if _globals == None:
    try: 
      global_handle = open(GLOBAL_PATH, 'r')
      _globals = load_decls(global_handle.read())
    except IOError:
      print 'Error opening globals file'
  return _globals

def build_page(page):
  print 'building ' + page + '.html with template ' + PAGES[page] + '.template'

  try:
    # open files
    template_handle = open(os.path.abspath(
        os.path.join(SRC_PATH, PAGES[page] + '.template')), 'r')
    content_handle = open(os.path.abspath(os.path.join(SRC_PATH, page + '.content')), 'r')
    env = load_decls(content_handle.read())
    env.update(get_globals()) # Note: this makes globals shadow locals, I think.
    dest_path = os.path.abspath(os.path.join(DST_PATH, page + '.html'))
    dest_handle = open(dest_path, 'w')

    for line in template_handle.readlines():
      newline = line
      for m in re.finditer(var_use_regex, line):
        var_name = m.group(2)
        newline = line.replace(m.group(0), env[var_name])
      dest_handle.write(newline)

    template_handle.close()
    content_handle.close()
    dest_handle.close()

    os.chmod(dest_path, 0755)

  except IOError:
    print 'Error opening file for ' + page + '. Aborting this page.'

def main():
  print 'building website...'
  for page in PAGES.keys():
    build_page(page)
  print 'done!'

if __name__ == '__main__':
  sys.exit(main())
