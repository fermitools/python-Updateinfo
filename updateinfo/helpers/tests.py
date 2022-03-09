#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the helpers
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

import contextlib
import os
import random
import re
import shutil
import subprocess
import tempfile
import unittest

from distutils.version import StrictVersion

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

from .dates import find_old_dates

from .finders import all_packages_by_update
from .finders import all_updates_for_rpm_name
from .finders import all_updates_for_rpm_name_and_collection
from .finders import what_update_has_filename
from .finders import what_update_has_reference
from .finders import what_update_has_reference_like
from .finders import what_collection_has_filename
from .finders import what_update_has_package
from .finders import what_collection_has_package

from .repo import add_xml_to_repo
from .repo import get_xml_from_repo
from .repo import get_package_list_from_repo
from .repo import get_package_list_by_srpm_from_repo
from .repo import get_package_stanza_from_repo

from .suggested import set_suggested

from .xmltools import xml_pretty_formatter
from .xmltools import get_xsl_pi
from .xmltools import add_xsd_uri
from .xmltools import add_comment
from .xmltools import validate

from ..updateinfo import Updateinfo
from ..update import Update
from ..collection import Collection
from ..reference import Reference
from ..package import Package

@contextlib.contextmanager
def keeprealcwd():
    '''I'm just here so we can safely getcwd'''
    curdir = os.getcwd()
    try:
        # nothing
        yield
    finally:
        os.chdir(curdir)

class HelperDateTests(unittest.TestCase):
    '''Make sure the helper date functions work'''
    Updateinfo = Updateinfo
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package
    def pkg_one_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_two_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def ref_one_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def entry_one_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry
    def entry_two_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.issued_date = '2014-01-01'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        return testentry
    def updateinfo_for_test(self):
        '''sample'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())
        return testobj

    def test_old_dates_noarg(self):
        '''do we find super old dates'''
        testobj = self.updateinfo_for_test()

        old = find_old_dates(testobj)

        result = False
        if old == ('1',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="didn't find old dates")

    def test_old_dates_arg(self):
        '''do we find super old dates'''
        testobj = self.updateinfo_for_test()

        old = find_old_dates(testobj, '1999-10-30')

        result = False
        if old == ('1',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="didn't find old dates")

class HelperFindersTests(unittest.TestCase):
    '''Make sure the helper id functions work'''
    Updateinfo = Updateinfo
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package
    def pkg_one_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def pkg_three_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = '2'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def pkg_three_again_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'xxbxbxbx'
        testpkg.version = '2'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def pkg_four_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'somename'
        testpkg.version = '2'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        return testcoll
    def coll_two_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_three_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_three_for_test())
        testcoll.add(self.pkg_three_again_for_test())
        return testcoll
    def coll_four_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_four_for_test())
        return testcoll
    def ref_one_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def ref_three_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='other', href='https://3', refid='3', title='sometext')
        return testref
    def entry_one_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry
    def entry_two_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.issued_date = '2014-01-01'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        testentry.references.add(self.ref_three_for_test())
        return testentry
    def entry_three_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '3'
        testentry.issued_date = '2014-01-01'
        testentry.collections.add(self.coll_three_for_test())
        testentry.references.add(self.ref_three_for_test())
        return testentry
    def entry_four_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '4'
        testentry.issued_date = '2014-01-01'
        testentry.collections.add(self.coll_four_for_test())
        return testentry
    def updateinfo_for_test(self):
        '''sample'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())
        testobj.add(self.entry_three_for_test())
        testobj.add(self.entry_four_for_test())
        return testobj

    def test_what_update_has_filename_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_filename(testobj, 'asdf-jkl-gh.src.rpm')

        result = False
        if found == ('1',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_update_has_filename_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_filename(testobj, 'src.rpm')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_what_collection_has_filename_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_collection_has_filename(testobj['1'], 'asdf-jkl-gh.src.rpm')

        result = False
        if found == ('asdf',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_collection_has_filename_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_collection_has_filename(testobj['1'], 'src.rpm')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_all_packages_by_update(self):
        '''Verify this returns expected data'''
        testobj = self.updateinfo_for_test()
        results = all_packages_by_update(testobj)
        expected = {'1': ['asdf-jkl-gh.src.rpm'], '3': ['aaasdf-2-gh.noarch.rpm', 'xxbxbxbx-2-gh.noarch.rpm'], '2': ['aaasdf-jkl-gh.noarch.rpm'], '4': ['somename-2-gh.noarch.rpm']}
        works = False
        if results == expected:  # pragma: no cover
            works = True
        self.assertTrue(works, msg="didn't get expected output")

    def test_what_update_has_package_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_package(testobj, 'asdf-jkl-gh.src.rpm')

        result = False
        if found == ('1',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_update_has_package_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_package(testobj, 'src.rpm')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_what_collection_has_package_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_collection_has_package(testobj['1'], 'asdf-jkl-gh.src.rpm')

        result = False
        if found == ('asdf',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_collection_has_package_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_collection_has_package(testobj['1'], 'src.rpm')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_what_update_has_reference_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_reference(testobj, 'http://2')

        result = False
        if found == ('2',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_update_has_reference_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_reference(testobj, 'http://3')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_what_update_has_reference_like_has(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_reference_like(testobj, 'http://.*')

        result = False
        if found == ('1','2'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_update_has_reference_like_has_asregex(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_reference_like(testobj, re.compile('http://.*'))

        result = False
        if found == ('1','2'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="didn't find package")

    def test_what_update_has_reference_like_nope(self):
        '''See if files we know are there are where we expect'''
        testobj = self.updateinfo_for_test()

        found = what_update_has_reference(testobj, 'http://\w\w\d')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_all_updates_for_rpm_name_has_one(self):
        '''see if we can find just one update'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name(testobj, 'asdf')

        result = False
        if found == ('1',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="couldn't find one")

    def test_all_updates_for_rpm_name_has_two(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name(testobj, 'aaasdf')

        result = False
        if found == ('2', '3'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="couldn't find multiple")

    def test_all_updates_for_rpm_name_has_none(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name(testobj, 'f')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_all_updates_for_rpm_name_none(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name(testobj, None)

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_all_updates_for_rpm_name_and_collection_has_one(self):
        '''see if we can find just one update'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name_and_collection(testobj, 'asdf', 'asdf')

        result = False
        if found == ('1',):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="couldn't find one")

    def test_all_updates_for_rpm_name_and_collection_has_two(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        testobj['1'].collections['asdf'].add(self.pkg_three_for_test())
        found = all_updates_for_rpm_name_and_collection(testobj, 'aaasdf', 'iop')

        result = False
        if found == ('2', '3'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="couldn't find multiple")

    def test_all_updates_for_rpm_name_and_collection_has_none(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name_and_collection(testobj, 'f', 'iop')

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

    def test_all_updates_for_rpm_name_and_collection_none(self):
        '''see if we can find several updates'''
        testobj = self.updateinfo_for_test()
        found = all_updates_for_rpm_name_and_collection(testobj, None, None)

        result = False
        if found == ():  # pragma: no cover
            result = True

        self.assertTrue(result, msg="found something")

class HelperRepoTests(unittest.TestCase):
    '''Make sure the helper repo functions work'''
    Updateinfo = Updateinfo
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package
    def pkg_one_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_two_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def ref_one_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def entry_one_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry
    def entry_two_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        return testentry
    def updateinfo_for_test(self):
        '''sample'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())
        return testobj

    def test_added_xml_ts_is_old(self):
        '''Make sure added XML is older than old repomd'''
        _cwd = os.getcwd()
        uinfofile = None

        uinfo = self.updateinfo_for_test()
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            os.chdir(tmpdir)
            subprocess.call(['createrepo', '.'], stdout=subprocess.PIPE)

            repo_ts = os.path.getmtime('repodata/repomd.xml')

            add_xml_to_repo(uinfo.xml, '.')

            added_ts = os.path.getmtime('repodata/updateinfo.xml')

        shutil.rmtree(tmpdir)

        result = False
        if added_ts < repo_ts:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='not setting correct timestamps')

    def test_write_to_cwd_repo(self):
        '''try to write to repodata'''
        _cwd = os.getcwd()
        uinfofile = None

        uinfo = self.updateinfo_for_test()
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            os.chdir(tmpdir)
            subprocess.call(['createrepo', '.'], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, '.')

            _fd = open('repodata/repomd.xml', 'r')
            xmlfile = _fd.read()
            _fd.close()

            repomd = xmletree.fromstring(xmlfile)

            xsd_ns = '{http://linux.duke.edu/metadata/repo}'
            text = None
            for repometadata in repomd:
                if 'type' in repometadata.attrib:
                    if repometadata.attrib['type'] == 'updateinfo':
                        for inform in repometadata:
                            if inform.tag == xsd_ns + 'location':
                                uinfofile = inform.attrib['href']

        shutil.rmtree(tmpdir)

        result = False
        if uinfofile == 'repodata/updateinfo.xml.bz2':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='relative write not working')

    def test_write_to_some_repo(self):
        '''try to write to repodata'''
        uinfo = self.updateinfo_for_test()
        uinfofile = None
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir, cleanup=False)

            _fd = open(tmpdir + '/repodata/repomd.xml', 'r')
            xmlfile = _fd.read()
            _fd.close()

            repomd = xmletree.fromstring(xmlfile)

            xsd_ns = '{http://linux.duke.edu/metadata/repo}'
            text = None
            for repometadata in repomd:
                if 'type' in repometadata.attrib:
                    if repometadata.attrib['type'] == 'updateinfo':
                        for inform in repometadata:
                            if inform.tag == xsd_ns + 'location':
                                uinfofile = inform.attrib['href']

        shutil.rmtree(tmpdir)

        result = False
        if uinfofile == 'repodata/updateinfo.xml.bz2':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='abs write not working')

    def test_write_to_tilde_repo(self):
        '''try to write to repodata'''
        uinfo = self.updateinfo_for_test()
        uinfofile = None
        random_suffix = random.uniform(1, 10)
        tmpdir = '~/.__DELETE_ME_some_random_dirname_%s' %(random_suffix)
        try:
            shutil.rmtree(os.path.expanduser(tmpdir))
        except:
            pass

        with keeprealcwd():
            os.mkdir(os.path.expanduser(tmpdir))

            subprocess.call(['createrepo', os.path.expanduser(tmpdir)], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir)

            _fd = open(os.path.expanduser(tmpdir) + '/repodata/repomd.xml', 'r')
            xmlfile = _fd.read()
            _fd.close()

            repomd = xmletree.fromstring(xmlfile)

            xsd_ns = '{http://linux.duke.edu/metadata/repo}'
            text = None
            for repometadata in repomd:
                if 'type' in repometadata.attrib:
                    if repometadata.attrib['type'] == 'updateinfo':
                        for inform in repometadata:
                            if inform.tag == xsd_ns + 'location':
                                uinfofile = inform.attrib['href']

        shutil.rmtree(os.path.expanduser(tmpdir))

        result = False
        if uinfofile == 'repodata/updateinfo.xml.bz2':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='tilde write not working')

    def test_write_to_some_repo_cleanup(self):
        '''try to write to repodata'''
        uinfo = self.updateinfo_for_test()
        uinfofile = None
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir)
            add_xml_to_repo(uinfo.xml, tmpdir, cleanup=True)

            _fd = open(tmpdir + '/repodata/repomd.xml', 'r')
            xmlfile = _fd.read()
            _fd.close()

            repomd = xmletree.fromstring(xmlfile)

            xsd_ns = '{http://linux.duke.edu/metadata/repo}'
            text = None
            for repometadata in repomd:
                if 'type' in repometadata.attrib:
                    if repometadata.attrib['type'] == 'updateinfo':
                        for inform in repometadata:
                            if inform.tag == xsd_ns + 'location':
                                uinfofile = inform.attrib['href']

        shutil.rmtree(tmpdir)

        result = False
        if uinfofile == 'repodata/updateinfo.xml.bz2':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='abs write not working')

    def test_write_to_some_repo_cleanup_filename(self):
        '''try to write to repodata'''
        uinfo = self.updateinfo_for_test()
        uinfofile = None
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir, filename='deleteme')
            add_xml_to_repo(uinfo.xml, tmpdir, filename='deleteme', cleanup=True)

            _fd = open(tmpdir + '/repodata/repomd.xml', 'r')
            xmlfile = _fd.read()
            _fd.close()

            repomd = xmletree.fromstring(xmlfile)

            xsd_ns = '{http://linux.duke.edu/metadata/repo}'
            text = None
            for repometadata in repomd:
                if 'type' in repometadata.attrib:
                    if repometadata.attrib['type'] == 'updateinfo':
                        for inform in repometadata:
                            if inform.tag == xsd_ns + 'location':
                                uinfofile = inform.attrib['href']

        shutil.rmtree(tmpdir)

        result = False
        if uinfofile == 'repodata/deleteme.bz2':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='abs write not working')

    def test_get_from_cwd_repo(self):
        '''try to read from repodata'''
        _cwd = os.getcwd()
        txt = None

        uinfo = self.updateinfo_for_test()
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            os.chdir(tmpdir)

            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir)

            txt = get_xml_from_repo('.')

        shutil.rmtree(tmpdir)

        expected = '''<updates><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''
        result = False
        if txt == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='relative read not working')

    def test_get_from_abs_repo(self):
        '''try to read from repodata'''
        uinfo = self.updateinfo_for_test()
        txt = None
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            add_xml_to_repo(uinfo.xml, tmpdir)

            txt = get_xml_from_repo(tmpdir)

        shutil.rmtree(tmpdir)

        expected = '''<updates><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''
        result = False
        if txt == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='abs read not working')

    def test_get_packages_from_empty_repo(self):
        '''try to read from repodata'''
        tmpdir = tempfile.mkdtemp()
        pkgs = 'bad value'

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_list_from_repo(tmpdir)
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

    def test_get_packages_from_repo(self):
        '''try to read from repodata'''
        tmpdir = tempfile.mkdtemp()
        pkgs = 'bad value'

        with open(os.devnull, 'w') as devnull:
            if os.path.isfile('./docs/samples/sample.spec'):
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            else:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/sample.spec'):
                    raise unittest.SkipTest('Could not find samples/sample.spec')
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', '/usr/share/doc/python-Updateinfo/samples/sample.spec'], stdout=devnull, stderr=devnull)
            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                shutil.copy('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm', tmpdir)
            else:
                shutil.copy('/tmp/RPMS/sample-1-1.1.noarch.rpm', tmpdir)
        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_list_from_repo(tmpdir)
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == ('sample-1-1.1.noarch.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

    def test_get_package_list_by_srpm_from_empty_repo(self):
        '''try to read from repodata'''
        pkgs = 'bad value'
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_list_by_srpm_from_repo(tmpdir)
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == {}:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read srpm package metadata")

    def test_get_package_list_by_srpm_from_repo(self):
        '''try to read from repodata'''
        pkgs = 'bad value'
        tmpdir = tempfile.mkdtemp()

        with open(os.devnull, 'w') as devnull:
            if os.path.isfile('./docs/samples/sample.spec'):
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            else:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/sample.spec'):
                    raise unittest.SkipTest('Could not find samples/sample.spec')
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', '/usr/share/doc/python-Updateinfo/samples/sample.spec'], stdout=devnull, stderr=devnull)

            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                shutil.copy('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm', tmpdir)
            else:
                shutil.copy('/tmp/RPMS/sample-1-1.1.noarch.rpm', tmpdir)
        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_list_by_srpm_from_repo(tmpdir)
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == {'sample-1-1.1.src.rpm': ['sample-1-1.1.noarch.rpm']}:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read srpm package metadata")

    def test_get_package_list_by_srpm_from_repo_w_source(self):
        '''try to read from repodata'''
        pkgs = 'bad value'
        tmpdir = tempfile.mkdtemp()

        with open(os.devnull, 'w') as devnull:
            if os.path.isfile('./docs/samples/sample.spec'):
                subprocess.check_call([ 'rpmbuild', '-bs', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            else:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/sample.spec'):
                    raise unittest.SkipTest('Could not find samples/sample.spec')
                subprocess.check_call([ 'rpmbuild', '-bs', '--define', '%_topdir /tmp/', '/usr/share/doc/python-Updateinfo/samples/sample.spec'], stdout=devnull, stderr=devnull)

            shutil.copy('/tmp/SRPMS/sample-1-1.1.src.rpm', tmpdir)
        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_list_by_srpm_from_repo(tmpdir)
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == {'sample-1-1.1.src.rpm': ['sample-1-1.1.src.rpm']}:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read srpm package metadata")

    def test_get_package_stanza_from_empty_repo(self):
        '''try to read from repodata'''
        pkgs = 'bad value'
        tmpdir = tempfile.mkdtemp()

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_stanza_from_repo(tmpdir, 'nofile')
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

    def test_get_package_stanza_from_repo(self):
        '''try to read from repodata'''
        pkgs = 'bad value'
        tmpdir = tempfile.mkdtemp()

        with open(os.devnull, 'w') as devnull:
            if os.path.isfile('./docs/samples/sample.spec'):
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            else:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/sample.spec'):
                    raise unittest.SkipTest('Could not find samples/sample.spec')
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', '/usr/share/doc/python-Updateinfo/samples/sample.spec'], stdout=devnull, stderr=devnull)

            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                shutil.copy('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm', tmpdir)
            else:
                shutil.copy('/tmp/RPMS/sample-1-1.1.noarch.rpm', tmpdir)
        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            pkgs = get_package_stanza_from_repo(tmpdir, 'nofile')
        shutil.rmtree(tmpdir)

        result = False
        if pkgs == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

    def test_fail_to_get_primaryxml_from_repo(self):
        '''try to read from repodata'''
        tmpdir = tempfile.mkdtemp()
        primary = 'notfound'

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)

            try:
                primary = get_xml_from_repo(tmpdir, mdtype='notfound')
            except ValueError:
                pass
            finally:
                shutil.rmtree(tmpdir)

        result = False
        if primary == 'notfound':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

    def test_fail_to_get_primaryxml_from_repo_ok(self):
        '''try to read from repodata'''
        tmpdir = tempfile.mkdtemp()
        primary = 'notfound'

        with keeprealcwd():
            subprocess.call(['createrepo', tmpdir], stdout=subprocess.PIPE)
            primary = get_xml_from_repo(tmpdir, mdtype='notfound', missingok=True)

        result = False
        if primary == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="couldn't read pkg metadata")

class HelperSuggestedTests(unittest.TestCase):
    '''Make sure suggested, suggests'''
    Updateinfo = Updateinfo
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package
    def pkg_one_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_two_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def ref_one_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def entry_one_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.title = 'asdf'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry
    def entry_two_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.title = 'jkl'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        return testentry
    def updateinfo_for_test(self):
        '''sample'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())
        return testobj

    def test_desktop_restarted(self):
        '''desktop must be restarted'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'the desktop must be restarted'
        set_suggested(testobj['1'])

        self.assertTrue(testobj['1'].relogin_suggested, msg='did not suggest relogin')

    def test_service_restarted(self):
        '''must be restarted'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'the service must be restarted'
        set_suggested(testobj['1'])

        self.assertTrue(testobj['1'].restart_suggested, msg='did not suggest restart')

    def test_system_reboot(self):
        '''must be rebooted'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'your system must be rebooted'
        set_suggested(testobj['1'])

        self.assertTrue(testobj['1'].reboot_suggested, msg='did not suggest reboot')

    def test_system_reboot_other(self):
        '''must be rebooted'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'your system rebooted'
        set_suggested(testobj['1'])

        self.assertTrue(testobj['1'].reboot_suggested, msg='did not suggest reboot')

    def test_no_reboot(self):
        '''must not suggest reboot'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'no important text'
        set_suggested(testobj['1'])

        self.assertFalse(testobj['1'].reboot_suggested, msg='did suggested reboot')

    def test_no_restart(self):
        '''must not suggest restart'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'no important text'
        set_suggested(testobj['1'])

        self.assertFalse(testobj['1'].restart_suggested, msg='did suggested restart')

    def test_no_relogin(self):
        '''must not suggest relogin'''
        testobj = self.updateinfo_for_test()
        testobj['1'].description = 'no important text'
        set_suggested(testobj['1'])

        self.assertFalse(testobj['1'].relogin_suggested, msg='did suggested relogin')



class HelperXMLToolsTests(unittest.TestCase):
    '''Make sure the xml helpers work'''
    Updateinfo = Updateinfo
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package
    def pkg_one_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''sample'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_two_for_test(self):
        '''sample'''
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def ref_one_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        '''sample'''
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def entry_one_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.reboot_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry
    def entry_two_for_test(self):
        '''sample'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        return testentry
    def updateinfo_for_test(self):
        '''sample'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())
        return testobj

    def test_xml_pretty_formatter_ones(self):
        '''does pprint work?'''
        uinfo = self.updateinfo_for_test()

        mytree = uinfo.xmletree
        xml_pretty_formatter(mytree, _ws=' ')

        expected = '''<updates>
 <update from="me@example.com" status="stable" type="security" version="2.0">
  <id>1</id>
  <title />
  <description />
  <issued date="1969-12-31 18:00:00" />
  <reboot_suggested>true</reboot_suggested>
  <pkglist>
   <collection short="asdf">
    <name>jkl</name>
    <package arch="noarch" name="aaasdf" release="gh" version="jkl">
     <filename>aaasdf-jkl-gh.noarch.rpm</filename>
    </package>
    <package arch="src" name="asdf" release="gh" version="jkl">
     <filename>asdf-jkl-gh.src.rpm</filename>
    </package>
   </collection>
  </pkglist>
  <references>
   <reference href="http://1" id="1" title="Asdf" type="bugzilla" />
  </references>
 </update>
 <update from="me@example.com" status="final" type="security" version="2.0">
  <id>2</id>
  <title />
  <description />
  <issued date="1969-12-31 18:00:00" />
  <pkglist>
   <collection short="iop">
    <name>qwe</name>
    <package arch="noarch" name="aaasdf" release="gh" version="jkl">
     <filename>aaasdf-jkl-gh.noarch.rpm</filename>
    </package>
    <package arch="src" name="asdf" release="gh" version="jkl">
     <filename>asdf-jkl-gh.src.rpm</filename>
    </package>
   </collection>
  </pkglist>
  <references>
   <reference href="http://2" id="2" title="Jkl" type="self" />
  </references>
 </update>
</updates>
'''
        got = xmletree.tostring(mytree)
        result = False
        if got == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="pretty print not working")

    def test_xml_pretty_formatter_lots(self):
        '''is the whitespace programable?'''
        uinfo = self.updateinfo_for_test()

        mytree = uinfo.xmletree
        xml_pretty_formatter(mytree, _ws='     ')

        expected = '''<updates>
     <update from="me@example.com" status="stable" type="security" version="2.0">
          <id>1</id>
          <title />
          <description />
          <issued date="1969-12-31 18:00:00" />
          <reboot_suggested>true</reboot_suggested>
          <pkglist>
               <collection short="asdf">
                    <name>jkl</name>
                    <package arch="noarch" name="aaasdf" release="gh" version="jkl">
                         <filename>aaasdf-jkl-gh.noarch.rpm</filename>
                    </package>
                    <package arch="src" name="asdf" release="gh" version="jkl">
                         <filename>asdf-jkl-gh.src.rpm</filename>
                    </package>
               </collection>
          </pkglist>
          <references>
               <reference href="http://1" id="1" title="Asdf" type="bugzilla" />
          </references>
     </update>
     <update from="me@example.com" status="final" type="security" version="2.0">
          <id>2</id>
          <title />
          <description />
          <issued date="1969-12-31 18:00:00" />
          <pkglist>
               <collection short="iop">
                    <name>qwe</name>
                    <package arch="noarch" name="aaasdf" release="gh" version="jkl">
                         <filename>aaasdf-jkl-gh.noarch.rpm</filename>
                    </package>
                    <package arch="src" name="asdf" release="gh" version="jkl">
                         <filename>asdf-jkl-gh.src.rpm</filename>
                    </package>
               </collection>
          </pkglist>
          <references>
               <reference href="http://2" id="2" title="Jkl" type="self" />
          </references>
     </update>
</updates>
'''
        got = xmletree.tostring(mytree)
        result = False
        if got == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="pretty print not working")

    def test_xsl_uri(self):
        '''can I add xsl uris?'''
        xsl_pi = get_xsl_pi('test')
        txt = '''<?xml-stylesheet type="text/xsl" href="test"?>'''

        result = False
        if xmletree.tostring(xsl_pi) == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get xsluri")

    def test_xsd_uri(self):
        '''can I add xsd uris?'''
        uinfo = self.updateinfo_for_test()

        tree = uinfo.xmletree

        tree = add_xsd_uri('test', tree)

        result = False
        if tree.attrib['xsi:schemaLocation'] == 'test':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't find xsd uri, couldn't set it")

    def test_xsl_uri_none(self):
        '''can I add xsl uris?'''

        result = False
        try:
            xsl_pi = get_xsl_pi(None)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Can set xsluri to None")

    def test_xsd_uri_none(self):
        '''can I add xsd uris?'''
        result = False
        try:
            uinfo = self.updateinfo_for_test()
            tree = uinfo.xmletree
            tree = add_xsd_uri(None, tree)
        except ValueError:
            result = True
        self.assertTrue(result, msg="can set xsd uri to None")

    def test_add_xml_comment(self):
        '''can I add xml comments?'''
        uinfo = self.updateinfo_for_test()

        tree = uinfo.xmletree

        tree = add_comment('test', tree)

        txt = xmletree.tostring(tree).rstrip()
        expected = '''<updates><!-- test --><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''

        ok_too = '''<updates><!--test--><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''

        result = False
        if txt == expected or txt == ok_too:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't add comments")

    def test_add_xml_comment_none(self):
        '''can I add xml comments?'''
        result = False
        try:
            uinfo = self.updateinfo_for_test()
            tree = uinfo.xmletree
            tree = add_comment(None, tree)
        except ValueError:
            result = True
        self.assertTrue(result, msg="can add comments None comment")

    def test_add_xml_comment_file(self):
        '''can I add xml comments?'''
        result = False
        tmpdir = tempfile.mkdtemp()
        txtfile= open(tmpdir + '/asdf', 'w')
        txtfile.write('test')
        txtfile.close()

        txtfile= open(tmpdir + '/asdf', 'r')
        uinfo = self.updateinfo_for_test()
        tree = uinfo.xmletree
        tree = add_comment(txtfile, tree)
        txtfile.close()

        txt = xmletree.tostring(tree).rstrip()
        expected = '''<updates><!--test--><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''

        ok_too = '''<updates><!-- test --><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update><update from="me@example.com" status="final" type="security" version="2.0"><id>2</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="iop"><name>qwe</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://2" id="2" title="Jkl" type="self" /></references></update></updates>'''

        result = False
        if txt == expected or txt == ok_too:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="can't add comment as file")

    def test_xsd_works_preformed(self):
        '''Does the XML validate?'''
        from lxml import etree as lxmletree
        txt = '''<updates xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="test"><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><issued date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package epoch="1" arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        result = False
        try:
            try:
                validate(txt, './docs/updateinfo.xsd')
            except IOError:  # pragma: no cover
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/updateinfo.xsd'):
                    raise unittest.SkipTest('Could not find updateinfo.xsd')

                validate(txt, '/usr/share/doc/python-Updateinfo/updateinfo.xsd')
            result = True
        except lxmletree.DocumentInvalid:  # pragma: no cover
            pass
        self.assertTrue(result, msg="can't validate")

    def test_xsd_works_uinfo_sample_fedora(self):
        '''Does the sample XML validate?'''
        from lxml import etree as lxmletree

        try:
            _fd = open('./docs/samples/Fedora-updateinfo.xml', 'r')
        except IOError:  # pragma: no cover
            if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/Fedora-updateinfo.xml'):
                raise unittest.SkipTest('Could not find Fedora-updateinfo.xml')
            _fd = open('/usr/share/doc/python-Updateinfo/samples/Fedora-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        result = True
        try:
            validate(txt, './docs/updateinfo.xsd')
        except IOError:  # pragma: no cover
            try:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/updateinfo.xsd'):
                    raise unittest.SkipTest('Could not find updateinfo.xsd')

                validate(txt, '/usr/share/doc/python-Updateinfo/updateinfo.xsd')
            except lxmletree.DocumentInvalid:
                result = False
        except lxmletree.DocumentInvalid:  # pragma: no cover
            result = False
        self.assertTrue(result, msg="can't validate")

    def test_xsd_works_uinfo_sample_epel(self):
        '''Does the sample XML validate?'''
        from lxml import etree as lxmletree

        try:
            _fd = open('./docs/samples/EPEL6-updateinfo.xml', 'r')
        except IOError:  # pragma: no cover
            if not os.path.isfile('/usr/share/doc/python-Updateinfo/samples/EPEL6-updateinfo.xml'):
                raise unittest.SkipTest('Could not find EPEL6-updateinfo.xml')
            _fd = open('/usr/share/doc/python-Updateinfo/samples/EPEL6-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        result = True
        try:
            validate(txt, './docs/updateinfo.xsd')
        except IOError:  # pragma: no cover
            try:
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/updateinfo.xsd'):
                    raise unittest.SkipTest('Could not find updateinfo.xsd')
                validate(txt, '/usr/share/doc/python-Updateinfo/updateinfo.xsd')
            except lxmletree.DocumentInvalid:
                result = False
        except lxmletree.DocumentInvalid:  # pragma: no cover
            result = False
        self.assertTrue(result, msg="can't validate")

    def test_xsd_works_uinfo_made(self):
        '''Does the sample XML validate?'''
        from lxml import etree as lxmletree

        uinfo = self.updateinfo_for_test()

        result = True
        try:
            try:
                validate(uinfo.xml, './docs/updateinfo.xsd')
            except IOError:  # pragma: no cover
                if not os.path.isfile('/usr/share/doc/python-Updateinfo/updateinfo.xsd'):
                    raise unittest.SkipTest('Could not find updateinfo.xsd')
                validate(uinfo.xml, '/usr/share/doc/python-Updateinfo/updateinfo.xsd')
            except lxmletree.DocumentInvalid:  # pragma: no cover
                result = False
        except lxmletree.DocumentInvalid:  # pragma: no cover
            result = False

        self.assertTrue(result, msg="can't validate")

