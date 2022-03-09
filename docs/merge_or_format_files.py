#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    This is a simple script which will merge all the updateinfo args you
    pass in and print them.

    You can pretty print or YAML format if you want.
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

from updateinfo.updateinfo import Updateinfo
from updateinfo.update import Update

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
    PARSER.add_argument('--isindividual', action='store_true',
                        default=False, help='Are the source files single Updates?')
    PARSER.add_argument('--isyaml', action='store_true',
                        default=False, help='Are the source files YAML instead of XML')
    PARSER.add_argument('--pretty', action='store_true',
                        default=False, help='Should the output be pretty xml')
    PARSER.add_argument('--yamlout', action='store_true',
                        default=False, help='Should the output be pretty YAML')

    ARGS = PARSER.parse_args()

    MYUPDATEINFO = Updateinfo()

    for FILE in ARGS.filename:
        TMPNAME = Updateinfo()
        with open(FILE, 'r') as _FD:
            TXT = _FD.read()

        if ARGS.isindividual:
            TMP = Update()
            if ARGS.isyaml:
                TMP.yaml = TXT
            else:
                TMP.xml = TXT
            TMPNAME.add(TMP)
        else:
            if ARGS.isyaml:
                TMPNAME.yaml = TXT
            else:
                TMPNAME.xml = TXT

        merge_updateinfo(MYUPDATEINFO, TMPNAME)

    if ARGS.pretty:
        print(MYUPDATEINFO)
    else:
        if ARGS.yamlout:
            print(MYUPDATEINFO.yaml)
        else:
            print(MYUPDATEINFO.xml)

