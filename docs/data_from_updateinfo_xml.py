#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    Read in the repodata from an existing yum repo and generate an updateinfo
    for that repo based on an existing updateinfo.xml file.

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
import sys

import concurrent.futures
import multiprocessing

try:
    import xml.etree.cElementTree as xmletree
except ImportError:
    import xml.etree.ElementTree as xmletree

from updateinfo import Updateinfo

from updateinfo.helpers.finders import all_packages_by_update
from updateinfo.helpers.finders import what_collection_has_package

from updateinfo.helpers.repo import get_package_list_from_repo
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
        'debug': False,
        'sourcexml': None,
        'repobase': None,
        'collection': None,
        'collectionreleasename': None,
        'status': None,
        'updatetype': None,
        'updatefrom': None,
        'updatemd': False,
        'xsluri': None,
        'quiet': False,
        'readold': True,
        'releasedate': None,
        'releasetitle': 'Scientific Linux',
        'pretty': False,
        'print': False,
        'commentfile': None,
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

    PARSER.add_argument('--debug', action='store_true',
                        help='Print out a log of activities')
    PARSER.add_argument('--sourcexml',
                        help='Where is the source updateinfo.xml')
    PARSER.add_argument('--repobase',
                        help='Where is the yum repo we are looking at?')
    PARSER.add_argument('--collection',
                        help='What collection do we store the packages in?')
    PARSER.add_argument('--collectionreleasename',
                        help='What is the release name of this collection?')
    PARSER.add_argument('--releasedate',
                        metavar=str(DEFAULTS['releasedate']).upper(),
                        help='What date should new updates have set?')
    PARSER.add_argument('--releasetitle',
                        metavar=str(DEFAULTS['releasetitle']).upper(),
                        help='What release are ALL packages in this update for?')
    PARSER.add_argument('--updatefrom', help='Who are these updates from?')
    PARSER.add_argument('--status', help='Set status to?')
    PARSER.add_argument('--updatetype', help='Set updatetype to?')
    PARSER.add_argument('--commentfile', type=file, dest='comment',
                        metavar='/PATH/TO/FILE',
                        help="Add this file's content as an XML comment")
    PARSER.add_argument('--updatemd', action='store_true',
                        help="Should I update that repodata when I'm done?")
    PARSER.add_argument('--xsluri',
                        help='Should I add an XSL uri, to where?')
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
    PARSER.add_argument('--forcenames', action='store_true',
                        help="Should I force STATUS, UPDATEFROM, RELEASETITLE, COLLECTIONRELEASENAME, and COLLECTION?")


    #pylint: disable=star-args
    PARSER.set_defaults(**DEFAULTS)

    ARGS = PARSER.parse_args(REMAINING_ARGS)

    if not ARGS.sourcexml:
        PARSER.error('You must set sourcexml')
    if not ARGS.repobase:
        PARSER.error('You must set repobase')

    MYUPDATEINFO = Updateinfo()

    if ARGS.readold:
        if ARGS.debug:
            print('Reading in old updateinfo', file=sys.stderr)
        MYUPDATEINFO.xml = get_xml_from_repo(ARGS.repobase)
        if ARGS.debug:
            print('Old updateinfo contains ' + str(len(MYUPDATEINFO)) + ' updates', file=sys.stderr)

    if ARGS.debug:
        print('Reading in SOURCE xml:' + ARGS.sourcexml , file=sys.stderr)
    SOURCE = Updateinfo()
    _FD = open(os.path.expanduser(ARGS.sourcexml), 'r')
    SOURCE.xml = _FD.read()
    _FD.close()
    if ARGS.debug:
        print('Source contains: ' + str(SOURCE.filenames), file=sys.stderr)

    if ARGS.readold:
        if ARGS.debug:
            print("Ensuring lookups in SOURCE don't obliterate old data", file=sys.stderr)
            for UPDATE in MYUPDATEINFO:
                SOURCE.add(MYUPDATEINFO[UPDATE])

    os.chdir(ARGS.repobase)

    if ARGS.debug:
        print('Getting package list from : ' + str(ARGS.repobase), file=sys.stderr)
    PKGS = get_package_list_from_repo(ARGS.repobase)

    if ARGS.debug:
        print('Getting package list from any existing updateinfo', file=sys.stderr)
    MYPKGLIST = MYUPDATEINFO.packages

    if ARGS.debug:
        print('Building quick lookup dict', file=sys.stderr)
    MYUPDATELIST = all_packages_by_update(SOURCE)

    with concurrent.futures.ThreadPoolExecutor(multiprocessing.cpu_count()) as POOL:
        for PACKAGENAME in PKGS:
            if os.path.basename(PACKAGENAME) in MYPKGLIST:
                if ARGS.debug:
                    print(PACKAGENAME + ' already in updateinfo', file=sys.stderr)
                continue
            if ARGS.debug:
                print(PACKAGENAME + ' to be added', file=sys.stderr)
            THISID = []
            for _ID in MYUPDATELIST:
                if os.path.basename(PACKAGENAME) in MYUPDATELIST[_ID]:
                    THISID.append(_ID)

            if not THISID:
                if ARGS.debug:
                    print('WARNING: ' + PACKAGENAME + ' has no id', file=sys.stderr)
                continue
            if ARGS.debug:
                print('Found: ' + PACKAGENAME + ' in ' + str(THISID), file=sys.stderr)

            # if in multiple ids, pick on - why not the first one.....
            THISID = THISID[0]
            if THISID not in MYUPDATEINFO:
                if ARGS.debug:
                    print('Creating: ' + THISID, file=sys.stderr)
                if ARGS.updatefrom:
                    UPDATEFROM = ARGS.updatefrom
                else:
                    UPDATEFROM = SOURCE[THISID].updatefrom
                if ARGS.status:
                    STATUS = ARGS.status
                else:
                    STATUS = SOURCE[THISID].status
                if ARGS.updatetype:
                    UPDATETYPE = ARGS.updatetype
                else:
                    UPDATETYPE = SOURCE[THISID].updatetype

                if ARGS.releasedate:
                    RELEASEDATE = ARGS.releasedate
                else:
                    RELEASEDATE = SOURCE[THISID].issued_date

                MYUPDATEINFO.create(SOURCE[THISID].updateid,
                                    UPDATEFROM,
                                    STATUS,
                                    UPDATETYPE,
                                    SOURCE[THISID].title,
                                    RELEASEDATE,
                                    SOURCE[THISID].description,
                                    SOURCE[THISID].severity,
                                    SOURCE[THISID].releasetitle,
                                    SOURCE[THISID].summary,
                                    SOURCE[THISID].rights,
                                    SOURCE[THISID].solution,
                                    SOURCE[THISID].update_date,
                                    SOURCE[THISID].reboot_suggested,
                                    SOURCE[THISID].restart_suggested,
                                    SOURCE[THISID].relogin_suggested)

            if ARGS.collection:
                THISCOLL = ARGS.collection
                THISCOLLNAME = ARGS.collectionreleasename
            else:
                try:
                    THISCOLL = what_collection_has_package(SOURCE[THISID], PACKAGENAME)[0]
                    THISCOLLNAME = SOURCE[THISID].collections[THISCOLL].release_name
                except IndexError:
                    raise IndexError('Could not find collection for ' + str(PACKAGENAME) + ' in ' + str(THISID))

            if THISCOLL not in MYUPDATEINFO[THISID].collections:
                if ARGS.debug:
                    print('Creating: ' + THISID + ' collection ' + THISCOLL, file=sys.stderr)
                MYUPDATEINFO[THISID].collections.create(THISCOLLNAME, THISCOLL)

            if ARGS.debug:
                print('Adding: ' + THISID + ' collection ' + THISCOLL + ' ' + PACKAGENAME, file=sys.stderr)
            POOL.submit(MYUPDATEINFO[THISID].collections[THISCOLL].add_filename, PACKAGENAME, checksum=ARGS.packagechecksum, readfile=True)
            MYPKGLIST = MYUPDATEINFO.packages

            MYUPDATEINFO[THISID].references = SOURCE[THISID].references

    if ARGS.debug:
        print('Done with data insert', file=sys.stderr)

    if ARGS.forcenames:
        if ARGS.debug:
            print('Forcing Names:', file=sys.stderr)
            print('  Forcing status: ' + str(ARGS.status), file=sys.stderr)
            print('  Forcing updatefrom: ' + str(ARGS.updatefrom), file=sys.stderr)
            print('  Forcing collection(short): ' + str(ARGS.collection), file=sys.stderr)
            print('  Forcing collection(release): ' + str(ARGS.collectionreleasename), file=sys.stderr)
            print('  Forcing update release title: ' + str(ARGS.releasetitle), file=sys.stderr)
        if ARGS.status:
            MYUPDATEINFO.force_status = ARGS.status
        if ARGS.updatefrom:
            MYUPDATEINFO.force_updatefrom = ARGS.updatefrom
        if ARGS.collectionreleasename:
            MYUPDATEINFO.force_collection_name = ARGS.collectionreleasename
        if ARGS.collection:
            MYUPDATEINFO.force_collection_short_name = ARGS.collection
        if ARGS.releasetitle:
            MYUPDATEINFO.force_releasetitle = ARGS.releasetitle

    if not ARGS.quiet:
        THESEPKGS = []
        for PKG in PKGS:
            THESEPKGS.append(os.path.basename(PKG))
        NOTFOUND = list(set(THESEPKGS) - set(MYUPDATEINFO.packages))

        NOTFOUND.sort()
        print('<!-- ----------Not Found------------------')
        for PKG in NOTFOUND:
            print(PKG)
        print('------------------------------------- --!>')

    if ARGS.debug:
        print('Making xml', file=sys.stderr)

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

