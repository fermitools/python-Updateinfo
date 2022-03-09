#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    Read in the repodata from an existing yum repo and generate an updateinfo
    for that repo based on an existing yum repo with the source rpms in it.

    Basically this extracts the information based on the filename in <package>,
    but generates new information for the rpms within the repo.
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

import ConfigParser
import os

try:
    import xml.etree.cElementTree as xmletree
except ImportError:
    import xml.etree.ElementTree as xmletree

from updateinfo import Updateinfo

from updateinfo.helpers.repo import get_package_list_by_srpm_from_repo
from updateinfo.helpers.repo import get_package_stanza_from_repo
from updateinfo.helpers.repo import get_xml_from_repo
from updateinfo.helpers.repo import add_xml_to_repo

from updateinfo.helpers.xmltools import add_comment
from updateinfo.helpers.xmltools import get_xsl_pi
from updateinfo.helpers.xmltools import xml_pretty_formatter

if __name__ == '__main__':
    import textwrap
    from argparse import ArgumentParser

    # Allowing these to be set from either a config or commandline
    # requires some additional magic
    DEFAULTS = {
        'sourcerepo': None,
        'repobase': None,
        'collection': 'MyCollection',
        'collectionreleasename': None,
        'updatefrom': 'me@example.com',
        'updatemd': False,
        'xsluri': None,
        'quiet': False,
        'readold': True,
        'pretty': False,
        'print': False,
        'commentfile': None,
        'status': 'stable',
        'updatetype': 'newpackage',
        'packagechecksum': 'sha256',
    }

    CONFPARSER = ArgumentParser(add_help=False)
    CONFPARSER.add_argument('--configfile', metavar='CONFIG.INI',
                            help="Set options from config file (in [DEFAULT])")

    ARGS, REMAINING_ARGS = CONFPARSER.parse_known_args()
    if ARGS.configfile:
        CFG = ConfigParser.SafeConfigParser()
        CFG.read(ARGS.configfile)
        DEFAULTS = dict(list(DEFAULTS.items()) + list(dict(CFG.items('DEFAULT')).items()))

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__),
                            parents=[CONFPARSER])
    PARSER.add_argument('--sourcerepo',
                        help='Where is the source yum repo')
    PARSER.add_argument('--repobase',
                        help='Where is the yum repo we are looking at?')
    PARSER.add_argument('--collection',
                        help='What collection do we store the packages in?')
    PARSER.add_argument('--collectionreleasename',
                        help='What is the release name of this collection?')
    PARSER.add_argument('--updatefrom', metavar=DEFAULTS['updatefrom'].upper(),
                        help='Who are these updates from?')
    PARSER.add_argument('--commentfile', type=file, dest='comment',
                        metavar='/PATH/TO/FILE',
                        help="Add this file's content as an XML comment")
    PARSER.add_argument('--updatemd', action='store_true',
                        help="Should I update that repodata when I'm done?")
    PARSER.add_argument('--xsluri',
                        help='Should I add an XSL uri, to where?')
    PARSER.add_argument('--status', help='Set status to?')
    PARSER.add_argument('--updatetype', help='Set updatetype to?')
    PARSER.add_argument('--quiet', action='store_true',
                        help="Should I print out status information?")
    PARSER.add_argument('--no-import', action='store_false', dest='readold',
                        help="Skip importing any existing updateinfo")
    PARSER.add_argument('--pretty', action='store_true',
                        help='Should the output be pretty')
    PARSER.add_argument('--print', action='store_true',
                        help='Should the output be printed to stdout')
    PARSER.add_argument('--packagechecksum',
                        help='What checksum should I use for packages (el5 needs sha)?')
    #pylint: disable=star-args
    PARSER.set_defaults(**DEFAULTS)

    ARGS = PARSER.parse_args(REMAINING_ARGS)

    if not (ARGS.sourcerepo or ARGS.repobase):
        PARSER.error('You must set sourcerepo and repobase')

    MYUPDATEINFO = Updateinfo()

    if ARGS.readold:
        MYUPDATEINFO.xml = get_xml_from_repo(ARGS.repobase)

    PKGS = get_package_list_by_srpm_from_repo(ARGS.repobase)
    for SRPMNAME in PKGS:
        THISID = os.path.basename(SRPMNAME.replace('.src.rpm', ''))
        if THISID not in MYUPDATEINFO:
            SRCSTANZA = get_package_stanza_from_repo(ARGS.sourcerepo, SRPMNAME)
            if not SRCSTANZA:
                continue
            DESC = SRCSTANZA.find('./{http://linux.duke.edu/metadata/common}description').text
            MYUPDATEINFO.create(THISID, ARGS.updatefrom, ARGS.status,
                                ARGS.updatetype,
                                'new package: ' + THISID,
                                0,
                                DESC,
                                None, None, None, None,
                                None, None, False, False, False)
        if ARGS.collection not in MYUPDATEINFO[THISID].collections:
            MYUPDATEINFO[THISID].collections.create(release_name=ARGS.collectionreleasename, short_name=ARGS.collection)

        for PACKAGENAME in PKGS[SRPMNAME]:
            MYUPDATEINFO[THISID].collections[ARGS.collection].add_filename(ARGS.repobase + '/' + PACKAGENAME, checksum=ARGS.packagechecksum, readfile=True)

    if not ARGS.quiet:
        THESEPKGS = []
        for PKG in PKGS:
            THESEPKGS.append(os.path.basename(PKG))
        NOTFOUND = list(set(THESEPKGS) - set(MYUPDATEINFO.packages))

        NOTFOUND.sort()
        for PKG in NOTFOUND:
            print(PKG)

    XMLOBJ = MYUPDATEINFO.xmletree

    if ARGS.comment:
        XMLOBJ = add_comment(ARGS.comment.read(), XMLOBJ)
    if ARGS.pretty:
        xml_pretty_formatter(XMLOBJ)

    XMLTXT = xmletree.tostring(XMLOBJ)
    if ARGS.xsluri:
        XSLURI = xmletree.tostring(get_xsl_pi(ARGS.xsluri))
        XMLTXT = XSLURI + '\n' + XMLTXT

    if ARGS.updatemd:
        add_xml_to_repo(XMLTXT, ARGS.repobase, sumtype=ARGS.packagechecksum)

    if ARGS.print:
        print(XMLTXT)

