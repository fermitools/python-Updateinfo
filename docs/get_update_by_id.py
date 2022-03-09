#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    This script will simply print out updates whose ID matches the regex
'''
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Version 0.2 by Pat Riehecky <riehecky@fnal.gov> for Scientific Linux
# Copyright (2019).  Fermi Research Alliance, LLC.

# for python3 compat
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import re

from updateinfo.updateinfo import Updateinfo
from updateinfo.helpers.repo import get_xml_from_repo

def read_updateinfo_xml_from_repo(repobase):
    ''' Get an updateinfo file, parse it and return the resulting object'''
    txt = get_xml_from_repo(repobase, mdtype='updateinfo')

    updateinfo_obj = Updateinfo()
    updateinfo_obj.xml = txt

    return updateinfo_obj

def read_updateinfo_xml_from_file(filename):
    ''' Open an updateinfo file, parse it and return the resulting object'''
    with open(filename, 'r') as _fd:
        txt = _fd.read()

    updateinfo_obj = Updateinfo()
    updateinfo_obj.xml = txt

    return updateinfo_obj

def read_updateinfo_yaml_from_file(filename):
    ''' Open an updateinfo file, parse it and return the resulting object'''
    with open(filename, 'r') as _fd:
        txt = _fd.read()

    updateinfo_obj = Updateinfo()
    updateinfo_obj.yaml = txt

    return updateinfo_obj

def merge_updateinfo(primary, add_these):
    '''merge in the elements from add_these into the primary object'''
    for update in add_these:
        primary.add(add_these[update])

    return primary


if __name__ == '__main__':
    import textwrap
    from argparse import ArgumentParser

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__))

    PARSER.add_argument('filename', nargs='+',
                        help='What should be parsed?  List however many')
    PARSER.add_argument('--regex', default='.',
                        help='What do I filter against?')
    PARSER.add_argument('--isyaml', action='store_true',
                        default=False, help='Are the source files YAML instead of XML')

    ARGS = PARSER.parse_args()

    MYUPDATEINFO = Updateinfo()

    for FILE in ARGS.filename:
        if ARGS.isyaml:
            TMPNAME = read_updateinfo_yaml_from_file(FILE)
        else:
            if FILE.startswith('http') or FILE.startswith('ftp://'):
                TMPNAME = read_updateinfo_xml_from_repo(FILE)
            else:
                TMPNAME = read_updateinfo_xml_from_file(FILE)
        merge_updateinfo(MYUPDATEINFO, TMPNAME)

    MYRE = re.compile(ARGS.regex)

    print('<updates>')
    for UPDATE in MYUPDATEINFO:
        if re.search(MYRE, MYUPDATEINFO[UPDATE].updateid):
            print(MYUPDATEINFO[UPDATE])
    print('</updates>')

