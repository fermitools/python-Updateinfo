#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    Read in the repodata from an existing yum repo and its existing
    updateinfo.xml file.

    Basically this extracts the information from the yum repo and list
    packages without an update id.
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
from updateinfo.helpers.repo import get_xml_from_repo, get_package_list_from_repo

if __name__ == '__main__':
    import textwrap, pprint
    from argparse import ArgumentParser

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__))

    PARSER.add_argument('--repobase', help='Where is the repo located?')

    ARGS = PARSER.parse_args()

    MYUPDATEINFO = Updateinfo()
    TXT = get_xml_from_repo(ARGS.repobase, mdtype='updateinfo')
    MYUPDATEINFO.xml = TXT

    LISTED_PACKAGES = set(MYUPDATEINFO.packages)
    REPO_PACKAGES = set(get_package_list_from_repo(ARGS.repobase))

    UNLISTED_PACKAGES = REPO_PACKAGES.difference(LISTED_PACKAGES)

    pprint.pprint(UNLISTED_PACKAGES)

