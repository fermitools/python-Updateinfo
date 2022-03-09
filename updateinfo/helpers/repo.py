#pylint: disable=line-too-long
'''
    A set of helper functions for dealing with repodata
'''
############################################################
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
############################################################

# for python3 compat
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import tempfile

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree


def add_xml_to_repo(xmltxt, repobase, filename='updateinfo.xml', sumtype='sha256', cleanup=True):
    '''
        Configures the repomd.xml to know about this new updateinfo.xml

        It will remove the old one automatically if you tell it
         what it was called.
    '''
    # this is where modifyrepo.py is kept on SL6
    sys.path.append('/usr/share/createrepo/')
    try:  # pragma: no cover
        #pylint: disable=import-error
        from modifyrepo import RepoMetadata
    except ImportError as error_msg:  # pragma: no cover
        print(' ', file=sys.stderr)
        print("Could not locate modifyrepo.py", file=sys.stderr)
        print("That is odd... should be with createrepo", file=sys.stderr)
        raise ImportError(error_msg)

    if '~' in repobase:
        repobase = os.path.expanduser(repobase)
    if not repobase.startswith('/'):
        repobase = os.path.abspath(repobase)

    if cleanup:
        if os.path.isfile(repobase + '/repodata/updateinfo.xml'):
            os.remove(repobase + '/repodata/updateinfo.xml')
        if os.path.isfile(repobase + '/repodata/' + filename):
            os.remove(repobase + '/repodata/' + filename)
        try:
            inrepomd = get_xml_from_repo(repobase, mdtype='updateinfo')
            if inrepomd:
                os.remove(repobase + '/repodata/' + inrepomd)
        except:
            pass

    _fd = open(repobase + '/repodata/' + filename, 'w')
    _fd.write(xmltxt)
    _fd.close()

    # find the timestamp of repomd.xml, use ten seconds
    # in the past for the timestamp of the added xml file
    # this /should/ make yum/dnf caching happier
    repo_ts = os.path.getmtime(repobase + '/repodata/repomd.xml')
    repo_ts = int(repo_ts - 10)
    os.utime(repobase + '/repodata/' + filename, (repo_ts, repo_ts))

    repomd = RepoMetadata(repobase + '/repodata')
    repomd.compress = True
    repomd.compress_type = 'bz2'
    repomd.checksum_type = sumtype
    repomd.unique_md_filenames = False

    # modifyrepo prints to stdout on its own, catching it
    rightout = sys.stdout
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    # lame, :( cast as str, cf: RHBZ 1181253
    repomd.add(str(repobase + '/repodata/' + filename), mdtype='updateinfo')
    sys.stdout = rightout
    devnull.close()

def get_xml_from_repo(repobase, mdtype='updateinfo', missingok=False):
    '''
        Pass in the repobase and you will get back the text of the
        xml that is tagged as a updateinfo metadata.
        If you set 'missingok', you may get back None if there is no data
    '''
    import urllib2
    if repobase.startswith('http://') or repobase.startswith('https://'):
        repomd_xml = urllib2.urlopen(repobase + '/repodata/repomd.xml')

    elif repobase.startswith('ftp://'):
        repomd_xml = urllib2.urlopen(repobase + '/repodata/repomd.xml')

    else:
        repobase = os.path.expanduser(repobase)
        repobase = os.path.abspath(repobase)
        repomd_xml = open(repobase + '/repodata/repomd.xml', 'r')

    repomd = xmletree.fromstring(repomd_xml.read())
    repomd_xml.close()

    xsd_ns = '{http://linux.duke.edu/metadata/repo}'
    xmlfile = None
    xmlfilename = None
    text = None
    repomdtypes = []
    for repometadata in repomd:
        if 'type' in repometadata.attrib:
            repomdtypes.append(repometadata.attrib['type'])
            if repometadata.attrib['type'] == mdtype:
                for inform in repometadata:
                    if inform.tag == xsd_ns + 'location':
                        xmlfilename = repobase + '/' + inform.attrib['href']

    if not xmlfilename:
        if missingok:
            return None
        else:
            raise ValueError("Could not find metadata for " + mdtype + " in " + repobase + " found " + str(repomdtypes))

    xmlfile = None
    text = None
    if xmlfilename.startswith('http://') or xmlfilename.startswith('ftp://'):
        xmlrequest = urllib2.urlopen(xmlfilename)
        xmlfile = tempfile.NamedTemporaryFile(mode='rw+b')
        xmlfile.write(xmlrequest.read())
        xmlfile.seek(0)
    else:
        # don't have to fetch local files
        xmlfile = open(xmlfilename, 'r')

    if xmlfile:
        with xmlfile:
            if xmlfilename.endswith('.gz'):
                import gzip
                raw_xml = gzip.GzipFile(fileobj=xmlfile)
                text = raw_xml.read()
            elif xmlfilename.endswith('.bz2'):
                import bz2
                text = bz2.decompress(xmlfile.read())
            elif xmlfilename.endswith('.xz'):
                import lzma
                text = lzma.decompress(xmlfile.read())
            else:
                text = xmlfile.read()

    return text

def get_package_list_from_repo(repobase):
    '''
        Pass in your repobase and I'll return a list of packages in it
    '''
    primaryxml = get_xml_from_repo(repobase, mdtype='primary')
    primaryxml_obj = xmletree.fromstring(primaryxml)

    common_ns = '{http://linux.duke.edu/metadata/common}'

    rpm_list = set()

    for element in primaryxml_obj:
        for child in element:
            if child.tag == common_ns + 'location':
                rpm_list.add(os.path.basename(child.attrib['href']))

    return tuple(rpm_list)

def get_package_list_by_srpm_from_repo(repobase):
    '''
        Pass in your repobase and I'll return a dict of packages
        where the SRPM is the key and packages it builds are the value.
    '''
    primaryxml = get_xml_from_repo(repobase, mdtype='primary')
    primaryxml_obj = xmletree.fromstring(primaryxml)

    common_ns = '{http://linux.duke.edu/metadata/common}'
    rpm_ns = '{http://linux.duke.edu/metadata/rpm}'

    rpm_list = {}

    for element in primaryxml_obj:
        package = element.find("./" + common_ns + 'location').attrib['href']
        sourcerpm = element.find(".//" + rpm_ns + 'sourcerpm')
        if package.endswith('.src.rpm'):
            sourcerpm = package
        else:
            try:
                sourcerpm = sourcerpm.text
            except:  # pragma: no cover
                pass

        if sourcerpm not in rpm_list:
            rpm_list[sourcerpm] = []

        rpm_list[sourcerpm].append(package)

    return rpm_list

def get_package_stanza_from_repo(repobase, packagename):
    '''
        Pass in your repobase and the name of the package as listed in
        <location href="" />
        And I'll return the xmletree of that package's stanza.
    '''
    primaryxml = get_xml_from_repo(repobase, mdtype='primary')
    primaryxml_obj = xmletree.fromstring(primaryxml)

    common_ns = '{http://linux.duke.edu/metadata/common}'

    for element in primaryxml_obj:
        for child in element:
            if child.tag == common_ns + 'location':
                if child.attrib['href'].endswith(os.path.basename(packagename)):
                    return element

    return None

