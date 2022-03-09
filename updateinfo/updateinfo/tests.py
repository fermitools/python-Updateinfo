#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the Updateinfo class!
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

import os
import unittest

from distutils.version import StrictVersion

from .models import UpdateinfoModel
from .events import UpdateinfoEvents
from .views import UpdateinfoXMLView
from .views import UpdateinfoYAMLView
from .views import UpdateinfoJSONView
from . import Updateinfo as UpdateinfoUpdateinfo

from ..update import Update
from ..collection import Collection
from ..reference import Reference
from ..package import Package

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

######################
# Classes for test inheritance
######################
class UpdateinfoE(UpdateinfoModel, UpdateinfoEvents):
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        UpdateinfoModel.__init__(self)
        UpdateinfoEvents.__init__(self, force_updatefrom=force_updatefrom, force_status=force_status, force_releasetitle=force_releasetitle, force_collection_name=force_collection_name, force_collection_short_name=force_collection_short_name)

class UpdateinfoX(UpdateinfoModel, UpdateinfoEvents, UpdateinfoXMLView):
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        UpdateinfoModel.__init__(self)
        UpdateinfoEvents.__init__(self, force_updatefrom=force_updatefrom, force_status=force_status, force_releasetitle=force_releasetitle, force_collection_name=force_collection_name, force_collection_short_name=force_collection_short_name)
        UpdateinfoXMLView.__init__(self)

class UpdateinfoY(UpdateinfoModel, UpdateinfoEvents, UpdateinfoYAMLView):
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        UpdateinfoModel.__init__(self)
        UpdateinfoEvents.__init__(self, force_updatefrom=force_updatefrom, force_status=force_status, force_releasetitle=force_releasetitle, force_collection_name=force_collection_name, force_collection_short_name=force_collection_short_name)
        UpdateinfoYAMLView.__init__(self)

class UpdateinfoJ(UpdateinfoModel, UpdateinfoEvents, UpdateinfoJSONView):
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        UpdateinfoModel.__init__(self)
        UpdateinfoEvents.__init__(self, force_updatefrom=force_updatefrom, force_status=force_status, force_releasetitle=force_releasetitle, force_collection_name=force_collection_name, force_collection_short_name=force_collection_short_name)
        UpdateinfoJSONView.__init__(self)
######################

class UpdateinfoModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    Updateinfo = UpdateinfoModel
    Update = Update
    Collection = Collection
    Reference = Reference
    Package = Package

    def pkg_one_for_test(self):
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg
    def coll_one_for_test(self):
        testcoll = self.Collection(release_name='jkl', short_name='asdf')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def coll_two_for_test(self):
        testcoll = self.Collection(release_name='qwe', short_name='iop')
        testcoll.add(self.pkg_one_for_test())
        testcoll.add(self.pkg_two_for_test())
        return testcoll
    def ref_one_for_test(self):
        testref = self.Reference(reftype='bugzilla', href='http://1', refid='1', title='asdf')
        return testref
    def ref_two_for_test(self):
        testref = self.Reference(reftype='self', href='http://2', refid='2', title='jkl')
        return testref
    def entry_one_for_test(self):
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
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '2'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())
        return testentry
    def entry_one_merge_for_test(self):
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.update_date = '1969-12-31 18:00:00'
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        return testentry

    @staticmethod
    def simpleadd(store, update):
        store._updates[update.updateid] = update
        return store

    def test_collection(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Collection())) == "<class 'updateinfo.collection.Collection'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collection_package(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Collection.Package())) == "<class 'updateinfo.package.Package'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collection_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Collection.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_package(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Package())) == "<class 'updateinfo.package.Package'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True

        self.assertTrue(result, msg='Wrong Object')

    def test_reference(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Reference())) == "<class 'updateinfo.reference.Reference'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')


    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.Updateinfo()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_init_with_args(self):
        '''make sure we take no args'''
        result = False
        try:
            testobj = self.Updateinfo('asdf')
        except TypeError:
            result = True
        msg = str(type(self.Updateinfo)) + " accepts args to init"
        self.assertTrue(result, msg=msg)

    def test_bool_undef(self):
        '''make sure undef is false'''
        testobj = self.Updateinfo()
        self.assertFalse(testobj, msg="undef is somehow true")

    def test_bool_def(self):
        '''make sure undef is false'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.assertTrue(testobj, msg="def is somehow false")

    def test_iter(self):
        '''make sure we can loop right'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        found = []
        for thing in testobj:
            found.append(thing)

        result = False
        if found == ['1']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="iter not working right")

    def test_len_undef(self):
        '''make sure len is sane'''
        testobj = self.Updateinfo()

        result = False
        if len(testobj) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="len not working right")

    def test_len_def(self):
        '''make sure len is sane'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if len(testobj) == 1:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="len not working right")

    def test_getitem_def(self):
        '''make sure getitem can get item'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj['1'].updateid == '1':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="getitem not working right")

    def test_getitem_undef(self):
        '''make sure getitem can't get things that don't exist'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        try:
            thing = testobj['3']
        except KeyError:
            result = True
        self.assertTrue(result, msg="getitem not working right")

    def test_contains_does_byid(self):
        '''make sure contains works as expected'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if '1' in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains not working right")

    def test_contains_does_byobj(self):
        '''make sure contains works as expected'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if self.entry_one_for_test() in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains not working right")

    def test_contains_doesnt_byid(self):
        '''make sure contains works as expected'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if '2' not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains not working right")

    def test_contains_doesnt_byobj(self):
        '''make sure contains works as expected'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if self.entry_two_for_test() not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains not working right")

    def test_contains_doesnt_bysimilarobj(self):
        '''make sure contains works as expected'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        entry = self.entry_one_for_test()
        entry.status = 'final'

        result = False
        if entry not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains not working right")

    def test_get_xsluri(self):
        '''make sure we can get the xsluri'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj.xsluri == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get xsluri or default is not None")

    def test_set_xsluri(self):
        '''make sure we can set the xsluri'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        testobj.xsluri = 'asdf'

        result = False
        if testobj.xsluri == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set xsluri")

    def test_get_xsduri(self):
        '''make sure we can get the xsduri'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj.xsduri == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get xsduri or default is not None")

    def test_set_xsduri(self):
        '''make sure we can set the xsduri'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        testobj.xsduri = 'asdf'

        result = False
        if testobj.xsduri == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set xsduri")

    def test_get_packages(self):
        '''test that we can get all packages contained'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get packages")

    def test_get_packages_two_updates(self):
        '''test that we can get all packages contained'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        if testobj.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get packages")

    def test_packages_ro(self):
        '''make sure the packages property is RO'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        try:
            testobj.packages = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Can set packages to something weird")

    def test_get_filenames(self):
        '''test that we can get all filenames contained'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj.filenames == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get filenames")

    def test_get_filenames_two_updates(self):
        '''test that we can get all filenames contained'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        if testobj.filenames == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get filenames")

    def test_filenames_ro(self):
        '''make sure the filenames property is RO'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        try:
            testobj.filenames = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Can set filenames to something weird")

    def test_get_ids_works(self):
        '''test that we can get our known ids'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        if testobj.ids == ('1', '2'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get known ids")

    def test_get_ids_sorted(self):
        '''test that we can get our known ids'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_two_for_test())
        self.simpleadd(testobj, self.entry_one_for_test())

        result = False
        if testobj.ids == ('1', '2'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get known ids")

    def test_ids_is_ro(self):
        '''test that known ids is RO'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        try:
            testobj.ids = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Can set known ids")

    def test_get_collections(self):
        '''Can we get our collections'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        if testobj.collection_names == ('asdf', 'iop'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't get known collection_names")

    def test_collections_is_ro(self):
        '''Can we set our collections'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        try:
            testobj.collection_names = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Can set known collection_names")

    def test_get_references(self):
        '''Can we get our references'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        if testobj.references == ('http://1', 'http://2'):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't get known references")

    def test_references_is_ro(self):
        '''Can we set our collections'''
        testobj = self.Updateinfo()
        self.simpleadd(testobj, self.entry_one_for_test())
        self.simpleadd(testobj, self.entry_two_for_test())

        result = False
        try:
            testobj.references = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Can set known references")

class UpdateinfoEventsTests(UpdateinfoModelTests):
    ''' Test the Events for sanity '''
    Updateinfo = UpdateinfoE

    def test_init_with_args(self):
        '''make sure we take args'''
        result = False
        testobj = self.Updateinfo('asdf')
        result = True
        self.assertTrue(result, msg="I accept args to init")

    def test_can_init_force_updatefrom(self):
        '''Can init setup force_updatefrom'''
        testobj = self.Updateinfo(force_updatefrom='somevalue')
        result = False
        if testobj.force_updatefrom == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_updatefrom")

    def test_can_get_force_updatefrom(self):
        '''Can i read force_updatefrom'''
        testobj = self.Updateinfo()

        result = False
        if testobj.force_updatefrom == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get force_updatefrom, or bad default")

    def test_can_set_force_updatefrom(self):
        '''Can i set force_updatefrom'''
        testobj = self.Updateinfo()

        testobj.force_updatefrom = 'somevalue'
        result = False
        if testobj.force_updatefrom == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_updatefrom")

    def test_can_init_force_status(self):
        '''Can init setup force_status'''
        testobj = self.Updateinfo(force_status='somevalue')
        result = False
        if testobj.force_status == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_status")

    def test_can_get_force_status(self):
        '''Can i read force_status'''
        testobj = self.Updateinfo()

        result = False
        if testobj.force_status == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get force_status, or bad default")

    def test_can_set_force_status(self):
        '''Can i set force_status'''
        testobj = self.Updateinfo()

        testobj.force_status = 'somevalue'
        result = False
        if testobj.force_status == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_status")

    def test_can_init_force_releasetitle(self):
        '''Can init setup force_releasetitle'''
        testobj = self.Updateinfo(force_releasetitle='somevalue')
        result = False
        if testobj.force_releasetitle == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_releasetitle")

    def test_can_get_force_releasetitle(self):
        '''Can i read force_releasetitle'''
        testobj = self.Updateinfo()

        result = False
        if testobj.force_releasetitle == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get force_releasetitle, or bad default")

    def test_can_set_force_releasetitle(self):
        '''Can i set force_releasetitle'''
        testobj = self.Updateinfo()

        testobj.force_releasetitle = 'somevalue'
        result = False
        if testobj.force_releasetitle == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_releasetitle")

    def test_can_init_force_collection_name(self):
        '''Can init setup force_collection_name'''
        testobj = self.Updateinfo(force_collection_name='somevalue')
        result = False
        if testobj.force_collection_name == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_collection_name")

    def test_can_get_force_collection_name(self):
        '''Can i read force_collection_name'''
        testobj = self.Updateinfo()

        result = False
        if testobj.force_collection_name == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get force_collection_name, or bad default")

    def test_can_set_force_collection_name(self):
        '''Can i set force_collection_name'''
        testobj = self.Updateinfo()

        testobj.force_collection_name = 'somevalue'
        result = False
        if testobj.force_collection_name == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_collection_name")

    def test_can_init_force_collection_short_name(self):
        '''Can init setup fforce_collection_short_name'''
        testobj = self.Updateinfo(force_collection_short_name='somevalue')
        result = False
        if testobj.force_collection_short_name == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_collection_short_name")

    def test_can_get_force_collection_short_name(self):
        '''Can i read force_collection_short_name'''
        testobj = self.Updateinfo()

        result = False
        if testobj.force_collection_short_name == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get force_collection_short_name, or bad default")

    def test_can_set_force_collection_short_name(self):
        '''Can i set force_collection_short_name'''
        testobj = self.Updateinfo()

        testobj.force_collection_short_name = 'somevalue'
        result = False
        if testobj.force_collection_short_name == 'somevalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set force_collection_short_name")

    def test_can_add(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        if '1' in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't add")

    def test_can_add_dict(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj['1'] = self.entry_one_for_test()

        result = False
        if '1' in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't add as dict")

    def test_cant_add_dict(self):
        '''Does add work?'''
        testobj = self.Updateinfo()

        result = False
        try:
            testobj['4'] = self.entry_one_for_test()
        except ValueError:
            result = True
        self.assertTrue(result, msg="Can add as dict bad id")

    def test_cant_add_dict_weird(self):
        '''Does add work?'''
        testobj = self.Updateinfo()

        result = False
        try:
            testobj['4'] = 'asdf'
        except TypeError:
            result = True
        self.assertTrue(result, msg="Can add as dict weird stuff")

    def test_can_add_xmletree(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        thisone = self.entry_one_for_test()
        testobj.add(thisone.xmletree)

        result = False
        if '1' in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't add")

    def test_can_add_bad_obj(self):
        '''If the object is not good enough, do we error'''
        testobj = self.Updateinfo()
        testentry = self.entry_one_for_test()

        testentry.updateid = None

        result = False
        try:
            testobj.add(testentry)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Can add bad things")

    def test_can_add_merge(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_one_for_test())

        result = False
        if '1' in testobj:  # pragma: no cover
            if len(testobj) == 1:
                result = True
        self.assertTrue(result, msg="Can't add merge")

    def test_can_add_merge_massive(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_one_merge_for_test())

        result = False
        if '1' in testobj:  # pragma: no cover
            if len(testobj) == 1:
                result = True
        self.assertTrue(result, msg="Can't add merge")

    def test_can_add_merge_minimal(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testupdate = self.Update()
        testupdate.updateid = '1'
        testupdate.schemaversion = None
        testobj.add(testupdate)

        result = False
        if '1' in testobj:  # pragma: no cover
            if len(testobj) == 1:
                result = True
        self.assertTrue(result, msg="Can't add merge")

    def test_cannot_add_merge(self):
        '''Does add work?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        try:
            testobj.add(self.entry_one_for_test(), merge=False)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Merge behaves badly")

    def test_add_weird(self):
        '''Can I add weird things?'''
        testobj = self.Updateinfo()

        result = False
        try:
            testobj.add('asdf')
        except TypeError:
            result = True
        self.assertTrue(result, msg="Can add weird things")

    def test_add_check_force_updatefrom_init(self):
        '''Does force_updatefrom work when set at init'''
        testobj = self.Updateinfo(force_updatefrom='checkit')
        testobj.add(self.entry_one_for_test())

        result = False
        if testobj['1'].updatefrom == 'checkit':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_updatefrom")

    def test_add_check_force_updatefrom_later(self):
        '''Does force_updatefrom work when set later'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.force_updatefrom = 'checkit'

        result = False
        if testobj['1'].updatefrom == 'checkit':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_updatefrom")

    def test_add_check_force_status_init(self):
        '''Does force_status work when set at init'''
        testobj = self.Updateinfo(force_status='testing')
        testobj.add(self.entry_one_for_test())

        result = False
        if testobj['1'].status == 'testing':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_status")

    def test_add_check_force_status_later(self):
        '''Does force_status work when set later'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.force_status = 'testing'

        result = False
        if testobj['1'].status == 'testing':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_status")

    def test_add_check_force_releasetitle_init_simple(self):
        '''Does force_releasetitle work when set at init'''
        testobj = self.Updateinfo(force_releasetitle='Checkme')
        testobj.add(self.entry_one_for_test())

        result = False
        if testobj['1'].releasetitle == 'Checkme':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_releasetitle")

    def test_add_check_force_releasetitle_later_simple(self):
        '''Does force_releasetitle work when set later'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.force_releasetitle = 'Checkme'

        result = False
        if testobj['1'].releasetitle == 'Checkme':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_releasetitle")

    def test_add_check_force_releasetitle_init_not_simple(self):
        '''Does force_releasetitle work when set at init'''
        testobj = self.Updateinfo(force_releasetitle='checkme')
        testobj.add(self.entry_one_merge_for_test())

        result = False
        if testobj['1'].releasetitle == 'Checkme':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_releasetitle")

    def test_add_check_force_releasetitle_later_not_simple(self):
        '''Does force_releasetitle work when set later'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_merge_for_test())
        testobj.force_releasetitle = 'Checkme'

        result = False
        if testobj['1'].releasetitle == 'Checkme':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_releasetitle")

    def test_add_check_force_collection_short_name_init(self):
        '''Does force_collection_short_name work when set at init'''
        testobj = self.Updateinfo(force_collection_short_name='testing')
        testobj.add(self.entry_one_for_test())

        result = False
        if 'testing' in testobj['1'].collections:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_collection_short_name")

    def test_add_check_force_collection_short_name_later(self):
        '''Does force_collection_short_name work when set later'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.force_collection_short_name = 'testing'

        result = False
        if 'testing' in testobj['1'].collections:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_collection_short_name")

    def test_add_check_force_collection_name_init(self):
        '''Does force_collection_name work when set at init'''
        testobj = self.Updateinfo(force_collection_name='testing', force_collection_short_name='testing')
        testobj.add(self.entry_one_for_test())

        result = False
        if testobj['1'].collections['testing'].release_name == 'testing':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_collection_name")

    def test_add_check_force_collection_name_later(self):
        '''Does force_collection_name work when set later'''
        testobj = self.Updateinfo(force_collection_short_name='testing')
        testobj.add(self.entry_one_for_test())
        testobj.force_collection_name = 'testing'

        result = False
        if testobj['1'].collections['testing'].release_name == 'testing':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't force_collection_name")

    def test_new_can(self):
        '''Can i make anonymous new entries?'''
        testobj = self.Updateinfo()
        testobj.create('1', 'from', 'final', 'enhancement', 'title', '1969-12-31 18:00:00', 'asdf', 'Important', 'rtitle', 'sum', 'righton', 'solved')

        txt = '''<update from="from" status="final" type="enhancement" version="2.0"><id>1</id><title>Title</title><description>asdf</description><severity>important</severity><summary>sum</summary><rights>righton</rights><solution>solved</solution><release>Rtitle</release><issued date="1969-12-31 18:00:00" /><pkglist /><references /></update>'''
        result = False
        if testobj['1'].xml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't make new anonymously")

    def test_del_can(self):
        '''Can I remove like a dict'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        del testobj['1']
        if '1' not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't delete like a dict")

    def test_del_cant(self):
        '''Can I remove like a dict'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        try:
            del testobj['111']
        except KeyError:
            result = True
        self.assertTrue(result, msg="Can't delete like a dict")

    def test_remove_can_byid(self):
        '''Can I remove byid'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        testobj.remove('1')
        if '1' not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't remove byid")

    def test_remove_can_byid_str(self):
        '''Can I remove byid'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        testobj.remove(str(1))
        if '1' not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't remove byid")

    def test_remove_can_obj(self):
        '''Can I remove byid'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        testobj.remove(self.entry_one_for_test())
        if '1' not in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't remove byobj")

    def test_remove_weird(self):
        '''When I try to remove wrong type, explode'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        try:
            testobj.remove(0)
        except ValueError:
            result = True
        self.assertTrue(result, msg="I can remove weird stuff")

    def test_remove_cant_byid(self):
        '''Can I remove byid'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        try:
            testobj.remove('3')
        except KeyError:
            result = True
        self.assertTrue(result, msg="Can remove bogus ids")

    def test_remove_cant_byobj(self):
        '''Can I remove byid'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        try:
            testobj.remove(self.entry_two_for_test())
        except KeyError:
            result = True
        self.assertTrue(result, msg="Can remove bogus objects")

class UpdateinfoXMLViewTests(UpdateinfoModelTests):
    ''' Test the XMLView for sanity '''
    Updateinfo = UpdateinfoX

    def test_init_with_args(self):
        '''make sure we take args'''
        result = False
        testobj = self.Updateinfo('asdf')
        result = True
        self.assertTrue(result, msg="I accept args to init")

    def test_pprint(self):
        '''Can I pretty print the object'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        text = '''<updates>
  <update from="me@example.com" status="stable" type="security" version="2.0">
    <id>1</id>
    <title />
    <description />
    <issued date="1969-12-31 18:00:00" />
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
</updates>
'''
        result = False
        if str(testobj) == text:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't pprint")

    def test_get_xml(self):
        '''Can I get the raw xml'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        text = '''<updates><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        result = False
        if testobj.xml == text:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get raw xml")

    def test_has_xsluri(self):
        '''Can I add an xsluri'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.xsluri = 'test'

        text = '''<?xml-stylesheet type="text/xsl" href="test"?>
<updates><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        result = False
        if testobj.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't get raw xml with xsl uri")

    def test_pprint_has_xsl(self):
        '''Can I add an xsluri'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.xsluri = 'test'

        text = '''<?xml-stylesheet type="text/xsl" href="test"?>
<updates>
  <update from="me@example.com" status="stable" type="security" version="2.0">
    <id>1</id>
    <title />
    <description />
    <issued date="1969-12-31 18:00:00" />
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
</updates>
'''

        result = False
        if str(testobj) == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't get raw xml with xsl uri")


    def test_has_xsduri(self):
        '''Can I add an xsduri'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.xsduri = 'test'

        text = '''<updates xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="test"><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        result = False
        if testobj.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't set xsd uri")

    def test_set_xml_none(self):
        '''Can I set from empty xml'''
        testobj = self.Updateinfo()
        testobj.xml = ''

    def test_set_xml(self):
        '''Can I set from the raw xml'''
        testobj = self.Updateinfo()

        text = '''<updates><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        testobj.xml = text

        result = False
        if self.entry_one_for_test() in testobj:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from raw xml")

    def test_set_xml_sample_fedora(self):
        '''Can I read in the Fedora sample xml file?'''
        testobj = self.Updateinfo()

        if not os.path.isfile('./docs/samples/Fedora-updateinfo.xml'):  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find Fedora sample from ' + os.getcwd())
            else:
                raise ValueError('Could not find Fedora sample from ' + os.getcwd())

        _fd = open('./docs/samples/Fedora-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        testobj.xml = txt
        result = False
        if len(testobj) > 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from Fedora sample")

    def test_get_xml_sample_fedora_packages(self):
        '''Can I read in the Fedora sample xml file?'''
        testobj = self.Updateinfo()

        if not os.path.isfile('./docs/samples/Fedora-updateinfo.xml'):  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find Fedora sample from ' + os.getcwd())
            else:
                raise ValueError('Could not find Fedora sample from ' + os.getcwd())

        _fd = open('./docs/samples/Fedora-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        testobj.xml = txt
        result = False
        if testobj.packages:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from Fedora sample")

    def test_set_xml_sample_epel(self):
        '''Can I read in the EPEL sample xml file?'''
        testobj = self.Updateinfo()

        if not os.path.isfile('./docs/samples/EPEL6-updateinfo.xml'):  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find EPEL sample from ' + os.getcwd())
            else:
                raise ValueError('Could not find Fedora sample from ' + os.getcwd())

        _fd = open('./docs/samples/EPEL6-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        testobj.xml = txt
        result = False
        if len(testobj) > 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from EPEL sample")

    def test_get_xml_sample_epel_packages(self):
        '''Can I read in the EPEL sample xml file?'''
        testobj = self.Updateinfo()

        if not os.path.isfile('./docs/samples/EPEL6-updateinfo.xml'):  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find EPEL sample from ' + os.getcwd())
            else:
                raise ValueError('Could not find Fedora sample from ' + os.getcwd())

        _fd = open('./docs/samples/EPEL6-updateinfo.xml', 'r')
        txt = _fd.read()
        _fd.close()

        testobj.xml = txt
        result = False
        if testobj.packages:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from EPEL sample")

    def test_set_xml_has_xsd(self):
        '''Can I set from an xml with an xsduri'''
        testobj = self.Updateinfo()

        text = '''<updates xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="test"><update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update></updates>'''

        testobj.xml = text

        result = False
        if self.entry_one_for_test() in testobj:  # pragma: no cover
            if testobj.xsduri == 'test':
                result = True
        self.assertTrue(result, msg="Can't set from raw xml with an xsd")

    def test_get_xmlobj(self):
        '''Can I get the xmletree object'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        if testobj.xmletree.tag == 'updates':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get xmletree")

    def test_get_xmlobj_is_element(self):
        '''Can I get the xmletree object'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        result = False
        if xmletree.iselement(testobj.xmletree):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get xmletree")

    def test_set_xmlobj(self):
        '''Can I set from the xmletree object'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        testobj2 = self.Updateinfo()

        testobj2.xmletree = testobj.xmletree

        result = False
        if self.entry_one_for_test() in testobj2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't set from xmlobj")

    def test_set_xmlobj_bad_obj(self):
        '''Can I set from the wrong xmletree object'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())

        testobj2 = self.Updateinfo()

        xmltree = testobj.xmletree
        xmltree.tag = 'nope'

        result = False
        try:
            testobj2.xmletree = xmltree
        except ValueError:
            result = True
        self.assertTrue(result, msg="Can set from bad xmlobj")

class UpdateinfoYAMLViewTests(UpdateinfoModelTests):
    ''' Test the YAMLView for sanity '''
    Updateinfo = UpdateinfoY

    def test_init_with_args(self):
        '''make sure we take args'''
        result = False
        testobj = self.Updateinfo('asdf')
        result = True
        self.assertTrue(result, msg="I accept args to init")

    def test_get_yaml(self):
        '''Can i get some basic YAML?'''
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())

        txt = '''- updateid: '1'
  issued_date: 1969-12-31 18:00:00
  updatetype: security
  collections:
  - asdf:
    - release_name: jkl
    - aaasdf-jkl-gh.noarch.rpm:
        arch: noarch
        name: aaasdf
        release: gh
        version: jkl
    - asdf-jkl-gh.src.rpm:
        arch: src
        name: asdf
        release: gh
        version: jkl
  references:
  - http://1:
      refid: '1'
      title: Asdf
      type: bugzilla
  updatefrom: me@example.com
  status: stable
- updateid: '2'
  issued_date: 1969-12-31 18:00:00
  updatetype: security
  collections:
  - iop:
    - release_name: qwe
    - aaasdf-jkl-gh.noarch.rpm:
        arch: noarch
        name: aaasdf
        release: gh
        version: jkl
    - asdf-jkl-gh.src.rpm:
        arch: src
        name: asdf
        release: gh
        version: jkl
  references:
  - http://2:
      refid: '2'
      title: Jkl
      type: self
  updatefrom: me@example.com
  status: stable
'''

        result = False
        if testobj.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get YAML")

    def test_set_yaml(self):
        '''Can i set some from basic YAML?'''
        testobj = self.Updateinfo()

        txt = '''- updateid: '1'
  issued_date: 1969-12-31 18:00:00
  updatetype: bugfix
  collections:
  - asdf:
    - release_name: jkl
    - aaasdf-jkl-gh.noarch.rpm:
        arch: noarch
        name: aaasdf
        release: gh
        version: jkl
    - asdf-jkl-gh.src.rpm:
        arch: src
        name: asdf
        release: gh
        version: jkl
  references:
  - http://1:
      refid: '1'
      title: Asdf
      type: bugzilla
  updatefrom: me@example.com
  status: stable
- title: Awesome Title
  updateid: '2'
  issued_date: 1969-12-31 18:00:00
  updatetype: enhancement
  collections:
  - iop:
    - release_name: qwe
    - aaasdf-jkl-gh.noarch.rpm:
        arch: noarch
        name: aaasdf
        release: gh
        version: jkl
    - asdf-jkl-gh.src.rpm:
        arch: src
        name: asdf
        release: gh
        version: jkl
  references:
  - http://2:
      refid: '2'
      title: Jkl
      type: self
  updatefrom: me@example.com
  status: final
'''
        testobj.yaml = txt
        result = False
        if testobj.yaml == txt:  # pragma: no cover
            if len(testobj) == 2:
                if testobj['1'].updatetype == 'bugfix':
                    if testobj['2'].title == 'Awesome Title':
                        if len(testobj['2'].collections) == 1:
                            if len(testobj['1'].references) == 1:
                                if len(testobj['1'].references) == 1:
                                    result = True
        self.assertTrue(result, msg="can't set YAML")

class UpdateinfoJSONTests(UpdateinfoModelTests):
    ''' Test the JSON view for sanity '''
    Updateinfo = UpdateinfoJ

    def test_init_with_args(self):
        '''make sure we take args'''
        result = False
        testobj = self.Updateinfo('asdf')
        result = True
        self.assertTrue(result, msg="I accept args to init")

    def test_get_json_a(self):
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_for_test())
        testobj.add(self.entry_two_for_test())

        expected = '[{"status": "stable", "updateid": "1", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}], "updatefrom": "me@example.com", "updatetype": "security", "issued_date": "1969-12-31 18:00:00"}, {"status": "stable", "updateid": "2", "collections": [{"iop": [{"release_name": "qwe"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "references": [{"http://2": {"type": "self", "refid": "2", "title": "Jkl"}}], "updatefrom": "me@example.com", "updatetype": "security", "issued_date": "1969-12-31 18:00:00"}]'
        result = False
        if testobj.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get JSON")

    def test_set_json_a(self):
        testobj = self.Updateinfo()

        testobj.json = '[{"status": "stable", "updateid": "1", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}], "updatefrom": "me@example.com", "updatetype": "security", "issued_date": "1969-12-31 18:00:00"}, {"status": "stable", "updateid": "2", "collections": [{"iop": [{"release_name": "qwe"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "references": [{"http://2": {"type": "self", "refid": "2", "title": "Jkl"}}], "updatefrom": "me@example.com", "updatetype": "security", "issued_date": "1969-12-31 18:00:00"}]'
        result = False
        if len(testobj) == 2:  # pragma: no cover
            if testobj['1'].status == 'stable':
                if testobj['2'].updatefrom == 'me@example.com':
                    if len(testobj['2'].collections) == 1:
                        if len(testobj['1'].references) == 1:
                            if len(testobj['1'].references) == 1:
                                result = True

        self.assertTrue(result, msg="can't set from JSON")

    def test_get_json_b(self):
        testobj = self.Updateinfo()
        testobj.add(self.entry_one_merge_for_test())

        expected = '[{"status": "stable", "description": "text", "updatetype": "security", "relogin_suggested": true, "restart_suggested": true, "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}], "issued_date": "1969-12-31 18:00:00", "update_date": "1969-12-31 18:00:00", "severity": "critical", "rights": "exist", "updatefrom": "me@example.com", "title": "A Title", "solution": "solved", "summary": "a summary", "updateid": "1", "releasetitle": "Release Title", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "reboot_suggested": true}]'
        result = False
        if testobj.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get JSON")

    def test_get_json_c(self):
        testobj = self.Updateinfo()

        result = False
        if testobj.json == '[]':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get JSON")

    def test_get_json_d(self):
        testobj = self.Updateinfo()
        entry = self.entry_one_merge_for_test()
        entry.issued_date = None
        testobj.add(entry)

        expected = '[{"status": "stable", "description": "text", "updatetype": "security", "relogin_suggested": true, "restart_suggested": true, "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}], "update_date": "1969-12-31 18:00:00", "severity": "critical", "rights": "exist", "updatefrom": "me@example.com", "title": "A Title", "solution": "solved", "summary": "a summary", "updateid": "1", "releasetitle": "Release Title", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "reboot_suggested": true}]'
        result = False
        if testobj.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get JSON")


class UpdateinfoTests(UpdateinfoEventsTests, UpdateinfoXMLViewTests, UpdateinfoYAMLViewTests, UpdateinfoJSONTests):
    ''' Test the default object for sanity '''
    Updateinfo = UpdateinfoUpdateinfo

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.Updateinfo.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

