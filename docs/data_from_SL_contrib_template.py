#!/usr/bin/env python
#PYTHON_ARGCOMPLETE_OK
#pylint: disable=line-too-long
'''
    This reads in a directory of SL_contrib_templates and makes an updateinfo
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
import re

try:
    import xml.etree.cElementTree as xmletree
except ImportError:
    import xml.etree.ElementTree as xmletree

import yaml

from updateinfo import Updateinfo
from updateinfo import Update

from updateinfo.helpers.repo import get_package_list_from_repo
from updateinfo.helpers.repo import get_xml_from_repo
from updateinfo.helpers.repo import add_xml_to_repo

from updateinfo.helpers.suggested import set_suggested

from updateinfo.helpers.xmltools import add_comment
from updateinfo.helpers.xmltools import get_xsl_pi
from updateinfo.helpers.xmltools import xml_pretty_formatter

if __name__ == '__main__':
    import textwrap
    from argparse import ArgumentParser

    # Allowing these to be set from either a config or commandline
    # requires some additional magic
    DEFAULTS = {
        'yamlin': None,
        'repobase': None,
        'collection': 'sl-addons',
        'collectionreleasename': "Scientific Linux 6 Addons",
        'updatefrom': 'me@example.com',
        'updatemd': False,
        'debug': False,
        'xsluri': None,
        'quiet': False,
        'readold': True,
        'pretty': False,
        'packagechecksum': 'sha256',
        'print': False,
        'commentfile': None,
        'status': 'stable',
        'updatetype': 'newpackage',
        'cveurlprefix': 'http://cve.mitre.org/cgi-bin/cvename.cgi?name=',
        'severityurlprefix': 'http://cve.mitre.org/cgi-bin/cvename.cgi?name=',
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
                        help="Should I print debugging info?")
    PARSER.add_argument('--yamlin',
                        help='Where are the SL_contrib_templates at?')
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
    PARSER.add_argument('--cveurlprefix', help='What should I prefix CVEs with?')
    PARSER.add_argument('--severityurlprefix',
                        help='What should I prefix severity ratings with?')
    PARSER.add_argument('--packagechecksum',
                        help='What checksum should I use for packages (el5 needs sha)?')
    #pylint: disable=star-args
    PARSER.set_defaults(**DEFAULTS)

    ARGS = PARSER.parse_args(REMAINING_ARGS)

    if not (ARGS.yamlin or ARGS.repobase):
        PARSER.error('You must set yamlin and repobase')

    MYUPDATEINFO = Updateinfo()

    if ARGS.readold:
        MYUPDATEINFO.xml = get_xml_from_repo(ARGS.repobase)

    PKGS = get_package_list_from_repo(ARGS.repobase)
    MYPKGLIST = MYUPDATEINFO.filenames
    for RPMNAME in PKGS:
        if RPMNAME in MYPKGLIST:
            continue
        # these are loose files, so start with where it should be
        # but look in everything until we are satisfied
        PROBABLY_THISONE = re.sub(r'\.(src|noarch|i.86|x86_64)\.rpm$', '', os.path.basename(RPMNAME))
        YAMLFILES = os.listdir(ARGS.yamlin)
        YAMLFILES.insert(0, PROBABLY_THISONE + '.yaml')

        THISID = None
        TEMPLATE = None
        FOUND = False
        for FILENAME in YAMLFILES:
            if THISID:
                continue
            if not FILENAME.endswith('.yaml'):
                continue
            if not os.path.isfile(ARGS.yamlin + '/' + FILENAME):
                if ARGS.debug:
                    print("No such file: " + ARGS.yamlin + '/' + FILENAME)
                continue

            _FD = open(ARGS.yamlin + '/' + FILENAME, 'r')
            TEMPLATE = yaml.safe_load(_FD.read())
            _FD.close()

            for RPMLIST in TEMPLATE['rpms']:
                for COLL in RPMLIST:
                    if os.path.basename(RPMNAME) in RPMLIST[COLL]:
                        FOUND = True
                    if RPMNAME in RPMLIST[COLL]:
                        FOUND = True
            if not FOUND:
                continue

            THISID = FILENAME.replace('.yaml', '')

        if THISID:
            if THISID not in MYUPDATEINFO:

                STATUS = ARGS.status
                if not TEMPLATE['production_ready']:
                    STATUS = 'prerelease'

                UPDATETYPE = ARGS.updatetype
                SEVERITY = None
                if 'update_type' in TEMPLATE:
                    UPDATETYPE = TEMPLATE['update_type']
                if TEMPLATE['security_update']:
                    UPDATETYPE = 'security'
                    SEVERITY = TEMPLATE['security_update']

                UPDATEFROM = ARGS.updatefrom
                for PERSON in TEMPLATE['submitted_by']:
                    if PERSON['primary_contact']:
                        UPDATEFROM = PERSON['email']

                MYUPDATE = Update()
                MYUPDATE.updateid = THISID
                MYUPDATE.updatefrom = UPDATEFROM
                MYUPDATE.status = STATUS
                MYUPDATE.updatetype = UPDATETYPE
                MYUPDATE.title = TEMPLATE['package']
                MYUPDATE.issued_date = TEMPLATE['release_date']
                MYUPDATE.severity = SEVERITY

                MYUPDATE.description = TEMPLATE['release_description']
                MYUPDATE = set_suggested(MYUPDATE)

                MYUPDATEINFO.add(MYUPDATE)

            if ARGS.collection not in MYUPDATEINFO[THISID].collections:
                MYUPDATEINFO[THISID].collections.create(release_name=ARGS.collectionreleasename, short_name=ARGS.collection)

            MYUPDATEINFO[THISID].collections[ARGS.collection].add_filename(RPMNAME, checksum=ARGS.packagechecksum, readfile=True)

            if TEMPLATE['fixed_bugs'] not in (False, None, 'False', 'None'):
                for BUG in TEMPLATE['fixed_bugs']:
                    MYUPDATEINFO[THISID].references.create(BUG['type'], BUG['url'], BUG['id'], BUG['summary'])
            if TEMPLATE['fixed_cves'] not in (False, None, 'False', 'None'):
                for BUG in TEMPLATE['fixed_cves']:
                    MYUPDATEINFO[THISID].references.create('cve', ARGS.cveurlprefix + BUG['id'], BUG['id'], BUG['summary'])
            if TEMPLATE['release_announcement'] not in (False, None, 'False', 'None'):
                MYUPDATEINFO[THISID].references.create('self', TEMPLATE['release_announcement'], THISID, 'Release Announcement')
            if MYUPDATEINFO[THISID].updatetype == 'security' and MYUPDATEINFO[THISID].severity:
                MYUPDATEINFO[THISID].references.create('other', ARGS.severityurlprefix + MYUPDATEINFO[THISID].severity, MYUPDATEINFO[THISID].severity, 'Issue Severity Classification')
        else:
            if ARGS.debug:
                print("No ID found for: " + RPMNAME)

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

