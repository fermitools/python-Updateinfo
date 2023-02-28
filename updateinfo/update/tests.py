#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the Update class!
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

import datetime
import unittest

from distutils.version import StrictVersion

from collections import OrderedDict

from .models import UpdateModel
from .events import UpdateEvents
from .views import UpdateXMLView
from .views import UpdateYAMLView
from .views import UpdateJSONView
from . import Update as UpdateinfoUpdate

from ..collection import Collection
from ..reference import Reference
from ..package import Package

from ..reference.store import ReferenceStore
from ..collection.store import CollectionStore

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

######################
# Classes for test inheritance
######################
class UpdateE(UpdateModel, UpdateEvents):
    '''example inheritance'''
    def __init__(self):
        UpdateModel.__init__(self)
        UpdateEvents.__init__(self)

class UpdateX(UpdateModel, UpdateEvents, UpdateXMLView):
    '''example inheritance'''
    def __init__(self):
        UpdateModel.__init__(self)
        UpdateEvents.__init__(self)
        UpdateXMLView.__init__(self)

class UpdateY(UpdateModel, UpdateEvents, UpdateYAMLView):
    '''example inheritance'''
    def __init__(self):
        UpdateModel.__init__(self)
        UpdateEvents.__init__(self)
        UpdateYAMLView.__init__(self)

class UpdateJ(UpdateModel, UpdateEvents, UpdateJSONView):
    '''example inheritance'''
    def __init__(self):
        UpdateModel.__init__(self)
        UpdateEvents.__init__(self)
        UpdateJSONView.__init__(self)
######################

class UpdateModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    Update = UpdateModel
    Package = Package
    Collection = Collection
    CollectionStore = CollectionStore
    Reference = Reference
    ReferenceStore = ReferenceStore

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
        testpkg.sums['md5'] = 'd41d8cd98f00b204e9800998ecf8427e'
        testpkg.sums['sha1'] = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
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

    def test_update_collectionstore(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore())) == "<class 'updateinfo.collection.store.CollectionStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collectionstore_collection(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection())) == "<class 'updateinfo.collection.Collection'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collectionstore_collection_package(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection.Package())) == "<class 'updateinfo.package.Package'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collectionstore_collection_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collection(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection())) == "<class 'updateinfo.collection.Collection'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collection_package(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection.Package())) == "<class 'updateinfo.package.Package'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_collection_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.CollectionStore.Collection.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_referencestore(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.ReferenceStore())) == "<class 'updateinfo.reference.store.ReferenceStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_update_referencestore_reference(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Update.ReferenceStore.Reference())) == "<class 'updateinfo.reference.Reference'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collectionstore(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.CollectionStore())) == "<class 'updateinfo.collection.store.CollectionStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collectionstore_collection(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.CollectionStore.Collection())) == "<class 'updateinfo.collection.Collection'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collectionstore_collection_package(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.CollectionStore.Collection.Package())) == "<class 'updateinfo.package.Package'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_collectionstore_collection_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.CollectionStore.Collection.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

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

    def test_referencestore(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.ReferenceStore())) == "<class 'updateinfo.reference.store.ReferenceStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_referencestore_reference(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.ReferenceStore.Reference())) == "<class 'updateinfo.reference.Reference'>":  # pragma: no cover
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
            testref = self.Update()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_construct_arg(self):
        '''Do I take args to construct?'''
        result = False
        try:
            testentry = self.Update('asdf')
        except TypeError:
            result = True
        self.assertTrue(result, msg='Seems I take args to construct')

    def test_bool_undef(self):
        '''When undef am I False?'''
        testentry = self.Update()

        self.assertFalse(testentry, msg='Seems I am true when undef')

    def test_bool_almost_def_status(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False

        if testentry:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am true when underdef')

    def test_bool_almost_def_bad_status(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = True
        try:
            testentry._status = 'false'
            if testentry:  # pragma: no cover
                pass
        except:
            result = False

        self.assertFalse(result, msg='Seems I am true when underdef')

    def test_bool_almost_def_from(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse(testentry, msg='Seems I am true when underdef')

    def test_bool_almost_def_from_blank(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.updatefrom = ''
        testentry.status = 'stable'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse(testentry, msg='Seems I am true when underdef')

    def test_bool_almost_def_type(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse(testentry, msg='Seems I am true when underdef')

    def test_bool_almost_def_bad_type_injected(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = True

        try:
            testentry._updatetype = 'false'
            if testentry:  # pragma: no cover
                pass
        except:
            result = False

        self.assertFalse(result, msg='Seems I am true when underdef')

    def test_bool_almost_def_id(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am true when underdef')

    def test_bool_almost_def_id_blank(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.updateid = ''
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am true when underdef')

    def test_bool_almost_def_date(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse(testentry, msg='Seems I am true when underdef')

    def test_bool_almost_def_coll(self):
        '''When under def am I False?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0

        self.assertFalse(testentry, msg='Seems I am true when underdef')

    def test_bool_def(self):
        '''When def am I True?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertTrue(testentry, msg='Seems I am False when def')

    def test_eq_none(self):
        '''am I rightly not eq None??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == None), msg='Seems I am eq, should not be')

    def test_eq_empty(self):
        '''am I rightly not eq '' ??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == ''), msg='Seems I am eq, should not be')

    def test_eq_empty_tuple(self):
        '''am I rightly not eq () ??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == ()), msg='Seems I am eq, should not be')

    def test_eq_empty_list(self):
        '''am I rightly not eq [] ??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == []), msg='Seems I am eq, should not be')

    def test_eq_empty_dict(self):
        '''am I rightly not eq {} ??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == {}), msg='Seems I am eq, should not be')

    def test_eq_is(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.collections.add(self.coll_one_for_test())

        self.assertTrue((testentry == testentry2), msg='Seems I am not eq, should be')

    def test_eq_is_everything(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        self.assertTrue((testentry == testentry2), msg='Seems I am not eq, should be')

    def test_eq_is_empty(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry2 = self.Update()
        self.assertTrue((testentry == testentry2), msg='Seems I am not eq, should be')

    def test_eq_isn(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.updateid = '2'
        testentry2.issued_date = 0
        testentry2.collections.add(self.coll_one_for_test())

        self.assertFalse((testentry == testentry2), msg='Seems I am eq, shouldnt be')

    def test_ne_is(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.collections.add(self.coll_one_for_test())

        result = False
        if testentry != testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am not eq, should be')

    def test_eq_isnt_id(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '2'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_from(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@exmple.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_type(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'bugfix'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_status(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_schema(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '2'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_desc(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'txt'
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_issued(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 1
        testentry.update_date = 0
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_severity(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'important'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_summ(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a ummary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_title(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_releasetitle(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'rlease title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_update(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 1
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_right(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'eist'
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

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_solution(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 's'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_reboot(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_restart(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_relogin(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'critical'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_collection(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_isnt_references(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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
        testentry.references.add(self.ref_two_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.schemaversion = '1'
        testentry2.updateid = '1'
        testentry2.issued_date = 0
        testentry2.update_date = 0
        testentry2.description = 'text'
        testentry2.rights = 'exist'
        testentry2.solution = 'solved'
        testentry2.severity = 'critical'
        testentry2.summary = 'a summary'
        testentry2.title = 'a title'
        testentry2.releasetitle = 'release title'
        testentry2.reboot_suggested = True
        testentry2.restart_suggested = True
        testentry2.relogin_suggested = True
        testentry2.collections.add(self.coll_one_for_test())
        testentry2.references.add(self.ref_one_for_test())

        result = False
        if testentry == testentry2:  # pragma: no cover
            result = True

        self.assertFalse(result, msg='Seems I am eq, should not be')

    def test_eq_weird(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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
        testentry.references.add(self.ref_two_for_test())

        result = False
        try:
            if testentry == 'asdf':  # pragma: no cover
                pass
        except TypeError:
            result = True

        self.assertTrue(result, msg='Seems I am eq, should not be')

    def test_ne_weird(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.update_date = 0
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
        testentry.references.add(self.ref_two_for_test())

        result = False
        try:
            if testentry != 'asdf':  # pragma: no cover
                pass
        except TypeError:
            result = True

        self.assertTrue(result, msg='Seems I am eq, should not be')

    def test_ne_isnt(self):
        '''am I rightly eq??'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        testentry2.status = 'stable'
        testentry2.updatefrom = 'me@example.com'
        testentry2.updatetype = 'security'
        testentry2.updateid = '2'
        testentry2.issued_date = 0
        testentry2.collections.add(self.coll_one_for_test())

        result = False
        if testentry != testentry2:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='Seems I am eq, shouldnt be')

    def test_get_status(self):
        '''Make sure we can read the status'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.status:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the status")

    def test_set_status_stable(self):
        '''Make sure we can set the status'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.status == 'stable':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the status")

    def test_set_status_testing(self):
        '''Make sure we can set the status'''
        testentry = self.Update()
        testentry.status = 'testing'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.status == 'testing':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the status")

    def test_set_status_final(self):
        '''Make sure we can set the status'''
        testentry = self.Update()
        testentry.status = 'final'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.status == 'final':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the status")

    def test_set_status_bad(self):
        '''Make sure we can set the status'''
        testentry = self.Update()
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.status = 'undef'
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems I can set the status to weird things")

    def test_get_updatefrom(self):
        '''Make sure we can read the updatefrom'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatefrom:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the updatefrom")

    def test_set_updatefrom(self):
        '''Make sure we can set the updatefrom'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatefrom == 'me@example.com':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the updatefrom")

    def test_get_updatetype(self):
        '''Make sure we can read the updatetype'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the updatetype")

    def test_set_updatetype(self):
        '''Make sure we can set the updatetype'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'security':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the updatetype")

    def test_get_updateid(self):
        '''Make sure we can read the updateid'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updateid:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the updateid")

    def test_set_updateid(self):
        '''Make sure we can set the updateid'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updateid == '1':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the updateid")

    def test_get_issued_date(self):
        '''Make sure we can read the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the issued_date")

    def test_set_issued_date_none(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = None
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't unset the issued_date")

    def test_set_issued_date_int(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.fromtimestamp(0):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_datetime(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = datetime.datetime.fromtimestamp(0)
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.fromtimestamp(0):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_date(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = datetime.date(1970, 2, 3)
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if str(testentry.issued_date) == '1970-02-03 00:00:00':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_tstamp(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '2014-01-23 13:41:55'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('2014-01-23 13:41:55', '%Y-%m-%d %H:%M:%S'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_tzstamp_zone(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '2014-01-23 13:41:55 UTC'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('2014-01-23 13:41:55', '%Y-%m-%d %H:%M:%S'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_tzstamp_a(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '2014-01-23 13:41:55 +0000'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('2014-01-23 13:41:55', '%Y-%m-%d %H:%M:%S'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_tzstamp_b(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '2014-01-23 13:41:55 -0600'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('2014-01-23 13:41:55', '%Y-%m-%d %H:%M:%S'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")


    def test_set_issued_date_dstamp(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '2014-01-23'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('2014-01-23', '%Y-%m-%d'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_usadstamp(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '01/23/2014'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.issued_date == datetime.datetime.strptime('01/23/2014', '%m/%d/%Y'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the issued_date")

    def test_set_issued_date_bad(self):
        '''Make sure we can set the issued_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.issued_date = 'Can"t Parse'
        except ValueError:
            result = True

        self.assertTrue(result, msg="Seems I can set the issued_date to bad data")

    def test_get_schemaversion(self):
        '''Make sure we can read the schemaversion'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.schemaversion:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the schemaversion")

    def test_set_schemaversion(self):
        '''Make sure we can set the schemaversion'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.schemaversion = '2'

        result = False
        if testentry.schemaversion == '2':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the schemaversion")

    def test_get_description(self):
        '''Make sure we can read the description'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.description == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the description")

    def test_set_description(self):
        '''Make sure we can set the description'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.description = 'text'

        result = False
        if testentry.description == 'text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the description")

    def test_set_description_nl(self):
        '''Make sure we can set the description'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.description = 'text\r'

        result = False
        if testentry.description == 'text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I accept dos line endings")

    def test_get_summary(self):
        '''Make sure we can read the summary'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.summary == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the summary")

    def test_set_summary(self):
        '''Make sure we can set the summary'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.summary = 'text'

        result = False
        if testentry.summary == 'text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the summary")

    def test_get_title(self):
        '''Make sure we can read the title'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.title == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the title")

    def test_set_title(self):
        '''Make sure we can set the title'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.title = 'text'

        result = False
        if testentry.title == 'Text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the title")

    def test_set_title_none(self):
        '''Make sure we can set the title'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.title = None

        result = False
        if testentry.title == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't unset the title")

    def test_get_releasetitle(self):
        '''Make sure we can read the releasetitle'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.releasetitle == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the releasetitle")

    def test_set_releasetitle(self):
        '''Make sure we can set the releasetitle'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.releasetitle = 'text'

        result = False
        if testentry.releasetitle == 'Text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the releasetitle")

    def test_set_releasetitle_empty(self):
        '''Make sure we can set the releasetitle'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.releasetitle = None

        result = False
        if testentry.releasetitle == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't unset the releasetitle")

    def test_get_rights(self):
        '''Make sure we can read the rights'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.rights == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the rights")

    def test_set_rights(self):
        '''Make sure we can set the rights'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.rights = 'text'

        result = False
        if testentry.rights == 'text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the rights")

    def test_get_solution(self):
        '''Make sure we can read the solution'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.solution == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the solution")

    def test_set_solution(self):
        '''Make sure we can set the solution'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.solution = 'text'

        result = False
        if testentry.solution == 'text':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the solution")

    def test_get_update_date(self):
        '''Make sure we can read the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the update_date")

    def test_set_update_date_none(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = None
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't unset the update_date")

    def test_set_update_date_int(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == datetime.datetime.fromtimestamp(0):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the update_date")

    def test_set_update_date_datetime(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = datetime.datetime.fromtimestamp(0)
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == datetime.datetime.fromtimestamp(0):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the update_date")

    def test_set_update_date_tstamp(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = '2014-01-23 13:41:55'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == datetime.datetime.strptime('2014-01-23 13:41:55', '%Y-%m-%d %H:%M:%S'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the update_date")

    def test_set_update_date_dstamp(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = '2014-01-23'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == datetime.datetime.strptime('2014-01-23', '%Y-%m-%d'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the update_date")

    def test_set_update_date_usadstamp(self):
        '''Make sure we can set the update_date'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.update_date = '01/23/2014'
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.update_date == datetime.datetime.strptime('01/23/2014', '%m/%d/%Y'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the update_date")

    def test_set_recommended(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'recommended'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'recommended':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_security(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'security'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'security':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_optional(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'optional'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'optional':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_feature(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'feature'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'feature':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_bugfix(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'bugfix'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'bugfix':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_enhancement(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'enhancement'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'enhancement':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_newpackage(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.updatetype = 'newpackage'
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.updatetype == 'newpackage':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_set_bad_type(self):
        '''Make sure we can set the right types'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.updatetype = 'bad value'
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems I can't set the type")

    def test_get_severity(self):
        '''Make sure we can read the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.severity == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't read the severity")

    def test_set_severity_none(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = None

        result = False
        if testentry.severity == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't unset the severity")

    def test_set_severity_critical(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'critical'

        result = False
        if testentry.severity == 'critical':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_important(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'important'

        result = False
        if testentry.severity == 'important':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_moderate(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'moderate'

        result = False
        if testentry.severity == 'moderate':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_low(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'low'

        result = False
        if testentry.severity == 'low':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_low_bugfix(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'bugfix'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'low'

        result = False
        if testentry.severity == 'low':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")


    def test_set_severity_low_cap(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'Low'

        result = False
        if testentry.severity == 'low':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_moderate_cap(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'Moderate'

        result = False
        if testentry.severity == 'moderate':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_important_cap(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'Important'

        result = False
        if testentry.severity == 'important':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_critical_cap(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'Critical'

        result = False
        if testentry.severity == 'critical':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_none_lc(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry.severity = 'none'

        result = False
        if testentry.severity == None:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set the severity")

    def test_set_severity_bad(self):
        '''Make sure we can set the severity'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.severity = 'invalid'
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems I can set the severity to weird things")

    def test_get_reboot_suggested(self):
        '''Make sure we can read reboot_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False

        self.assertFalse(testentry.reboot_suggested, msg="Seems reboot_suggested defaults to True")

    def test_set_reboot_suggested(self):
        '''Make sure we can set reboot_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.reboot_suggested = True

        self.assertTrue(testentry.reboot_suggested, msg="Seems reboot_suggested can't be set")

    def test_set_reboot_suggested_weird(self):
        '''Make sure we can set reboot_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.reboot_suggested = ('aasdf')

        self.assertTrue(testentry.reboot_suggested, msg="Seems reboot_suggested can't be set by iference")

    def test_get_relogin_suggested(self):
        '''Make sure we can read relogin_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False

        self.assertFalse(testentry.relogin_suggested, msg="Seems relogin_suggested defaults to True")

    def test_set_relogin_suggested(self):
        '''Make sure we can set relogin_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.relogin_suggested = True

        self.assertTrue(testentry.relogin_suggested, msg="Seems relogin_suggested can't be set")

    def test_set_relogin_suggested_weird(self):
        '''Make sure we can set relogin_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.relogin_suggested = ('aasdf')

        self.assertTrue(testentry.relogin_suggested, msg="Seems relogin_suggested can't be set by iference")

    def test_get_restart_suggested(self):
        '''Make sure we can read restart_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False

        self.assertFalse(testentry.restart_suggested, msg="Seems restart_suggested defaults to True")

    def test_set_restart_suggested(self):
        '''Make sure we can set restart_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.restart_suggested = True

        self.assertTrue(testentry.restart_suggested, msg="Seems restart_suggested can't be set")

    def test_set_restart_suggested_weird(self):
        '''Make sure we can set restart_suggested'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        testentry.restart_suggested = ('aasdf')

        self.assertTrue(testentry.restart_suggested, msg="Seems restart_suggested can't be set by iference")

    def test_collections_right_thing(self):
        '''Make sure the collections container is one'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if isinstance(testentry.collections, self.CollectionStore):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="self.CollectionStore isn't one")

    def test_collection_store_noset(self):
        '''Don't assign weird stuff to this'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.collections = ''
        except TypeError:
            result = True
        self.assertTrue(result, msg="I can set collectionstore to weird things")

    def test_collection_store_set(self):
        '''Do assign rational stuff stuff to this'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0

        testcoll = self.CollectionStore(parent=testentry)
        testcoll.add(self.coll_one_for_test())

        testentry.collections = testcoll
        result = False
        if 'asdf' in testentry.collections:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="I can't set collectionstore to newstore")

    def test_reference_right_thing(self):
        '''Make sure the reference container is one'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if isinstance(testentry.references, self.ReferenceStore):  # pragma: no cover
            result = True

    def test_reference_store_noset(self):
        '''Don't assign weird stuff to this'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.references = ''
        except TypeError:
            result = True
        self.assertTrue(result, msg="I can messup referencesstore")

    def test_reference_store_set(self):
        '''Don't assign weird stuff to this'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testref = self.ReferenceStore(parent=testentry)
        testref.add(self.ref_one_for_test())
        testentry.references = testref

        result = False
        if 'http://1' in testentry.references:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="I can't set referencesstore to new store")

    def test_packages_undef(self):
        '''make sure packages is undef when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0

        result = False
        if testentry.packages == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="packages metadata is messedup")

    def test_packages_def(self):
        '''make sure packages is def when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="packages metadata is messedup")

    def test_packages_def_two(self):
        '''make sure packages is def when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())
        testentry.collections.add(self.coll_two_for_test())

        result = False
        if testentry.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="packages metadata is messedup")

    def test_packages_ro(self):
        '''make sure packages read only'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.packages = []
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="packages is read/write")

    def test_filenames_undef(self):
        '''make sure filenames is undef when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0

        result = False
        if testentry.filenames == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="filenames metadata is messedup")

    def test_filenames_def(self):
        '''make sure filenames is def when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.filenames == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="filenames metadata is messedup")

    def test_filenames_def_two(self):
        '''make sure filenames is def when it should be'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())
        testentry.collections.add(self.coll_two_for_test())

        result = False
        if testentry.filenames == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="filenames metadata is messedup")

    def test_filenames_ro(self):
        '''make sure filenames read only'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.filenames = []
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="filenames is read/write")


    def test_collections_shortnames(self):
        '''make sure collections.shortnames is there'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0

        result = False
        if testentry.collections.shortnames == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="collections.shortnames is missing")

class UpdateEventsTests(UpdateModelTests):
    ''' Test the Events for sanity '''
    Update = UpdateE

    def test_no_add(self):
        '''Is the add() method an error'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.add('asdf')
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg='Seems add() exists')

    def test_no_remove(self):
        '''Is the remove() method an error'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        try:
            testentry.remove('asdf')
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg='Seems remove() exists')

class UpdateXMLViewTests(UpdateModelTests):
    ''' Test the XMLView for sanity '''
    Update = UpdateX

    def test_pprint(self):
        '''Can I be pretty printed?'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())

        text = '''<update from="me@example.com" status="stable" type="security" version="2.0">
  <id>1</id>
  <title />
  <description />
  <issued date="1969-12-31 18:00:00" />
  <pkglist>
    <collection short="asdf">
      <name>jkl</name>
      <package arch="noarch" name="aaasdf" release="gh" version="jkl">
        <filename>aaasdf-jkl-gh.noarch.rpm</filename>
        <sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum>
        <sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum>
      </package>
      <package arch="src" name="asdf" release="gh" version="jkl">
        <filename>asdf-jkl-gh.src.rpm</filename>
      </package>
    </collection>
  </pkglist>
  <references />
</update>
'''

        result = False
        if str(testentry) == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't pprint")

    def test_get_xml_a(self):
        '''get the raw xml'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())

        text = '''<update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename><sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum><sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references /></update>'''

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't get raw xml")

    def test_get_xml_b(self):
        '''get the raw xml'''
        testentry = self.Update()
        testentry.schemaversion = None

        text = '<update><id /><title /><description /><pkglist /><references /></update>'
        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get raw xml")

    def test_get_xml_c(self):
        '''get raw xml'''
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

        text = '''<update from="me@example.com" status="stable" type="security" version="1"><id>1</id><title>A Title</title><description>text</description><severity>critical</severity><summary>a summary</summary><rights>exist</rights><solution>solved</solution><release>Release Title</release><issued date="1969-12-31 18:00:00" /><updated date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename><sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum><sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update>'''

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get raw xml")

    def test_get_xml_d(self):
        '''get raw xml'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
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

        text = '''<update from="me@example.com" status="stable" type="security" version="1"><id>1</id><title>A Title</title><description>text</description><severity>critical</severity><summary>a summary</summary><rights>exist</rights><solution>solved</solution><release>Release Title</release><issued date="1970-01-01 00:00:00" /><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename><sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum><sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update>'''

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get raw xml")

    def test_get_xml_e(self):
        '''get raw xml'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'bugfix'
        testentry.schemaversion = '1'
        testentry.updateid = '1'
        testentry.description = 'text'
        testentry.rights = 'exist'
        testentry.solution = 'solved'
        testentry.severity = 'moderate'
        testentry.summary = 'a summary'
        testentry.title = 'a title'
        testentry.releasetitle = 'release title'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())

        text = '''<update from="me@example.com" status="stable" type="bugfix" version="1"><id>1</id><title>A Title</title><description>text</description><severity>moderate</severity><summary>a summary</summary><rights>exist</rights><solution>solved</solution><release>Release Title</release><issued date="1970-01-01 00:00:00" /><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename><sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum><sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update>'''

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get raw xml")


    def test_set_xml_none(self):
        '''Set xml when empty'''
        testentry = self.Update()
        testentry.xml = ''

    def test_set_xml_a(self):
        '''set from raw xml'''
        testentry = self.Update()

        text = '<update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title /><description /><issued date="1969-12-31 18:00:00" /><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references /></update>'

        testentry.xml = text

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't set from raw xml")

    def test_set_xml_b(self):
        '''set from raw xml'''
        testentry = self.Update()

        text = '<update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title>A Title</title><description>text</description><severity>critical</severity><summary>a summary</summary><rights>exist</rights><solution>solved</solution><release>Release Title</release><issued date="1969-12-31 18:00:00" /><updated date="1969-12-31 18:00:00" /><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update>'

        testentry.xml = text
        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from raw xml")

    def test_set_xml_c(self):
        '''set from raw xml'''
        testentry = self.Update()

        text = '<update version="2.0"><id /><pkglist /><references /><reboot_suggested>false</reboot_suggested><restart_suggested>false</restart_suggested><relogin_suggested>false</relogin_suggested></update>'

        testentry.xml = text

        result = False
        if testentry.xml == '<update version="2.0"><id /><title /><description /><pkglist /><references /></update>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from raw xml")

    def test_set_xml_nil(self):
        '''set from raw xml'''
        testentry = self.Update()

        text = '<update />'

        testentry.xml = text

        result = False
        if testentry.xml == '<update version="2.0"><id /><title /><description /><pkglist /><references /></update>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from raw xml")


    def test_get_xmlobj(self):
        '''can I get an xmletree object'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if testentry.xmletree.tag == 'update':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get xmlobj")

    def test_get_xmlobj_is_element(self):
        '''can I get an xmletree object'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        result = False
        if xmletree.iselement(testentry.xmletree):  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get xmlobj")

    def test_set_xmlobj(self):
        '''can I set from an xmletree object'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        testentry2.xmletree = testentry.xmletree

        result = False
        if testentry2.status == 'stable':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from xmlobj")

    def test_set_bad_xmlobj(self):
        '''can I set from an xmletree object'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = 0
        testentry.collections.add(self.coll_one_for_test())

        testentry2 = self.Update()
        tree = testentry.xmletree
        tree.tag = 'asdf'

        result = False

        try:
            testentry2.xmletree = tree
        except ValueError:
            result = True

        self.assertTrue(result, msg="Seems I can set from bad xmlobj")

    def test_all_attribs_print(self):
        '''make sure all attributes are in the xml output'''
        testentry = self.Update()
        testentry.status = 'stable'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.updateid = '1'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        testentry.title = 'asdf'
        testentry.severity = 'important'
        testentry.update_date = '1971-12-31 18:00:02'
        testentry.description = 'description'
        testentry.releasetitle = 'release title'
        testentry.summary = 'summary'
        testentry.solution = 'solution'
        testentry.rights = 'rights'
        testentry.reboot_suggested = True
        testentry.restart_suggested = True
        testentry.relogin_suggested = True

        text = '''<update from="me@example.com" status="stable" type="security" version="2.0"><id>1</id><title>Asdf</title><description>description</description><severity>important</severity><summary>summary</summary><rights>rights</rights><solution>solution</solution><release>Release Title</release><issued date="1969-12-31 18:00:00" /><updated date="1971-12-31 18:00:02" /><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename><sum type="md5">d41d8cd98f00b204e9800998ecf8427e</sum><sum type="sha">da39a3ee5e6b4b0d3255bfef95601890afd80709</sum></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist><references><reference href="http://1" id="1" title="Asdf" type="bugzilla" /></references></update>'''

        result = False
        if testentry.xml == text:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems something didn't print")

class UpdateYAMLViewTests(UpdateModelTests):
    ''' Test the YAML View for sanity '''
    Update = UpdateY

    def test_has_orderedict(self):
        '''Do I have my weird ordered dict property?'''
        testentry = self.Update()
        result = False
        if isinstance(testentry.ordereddict, OrderedDict):
            result = True
        self.assertTrue(result, msg='Seems I dont have my orderedict')

    def test_get_yaml_a(self):
        '''Can I get some basic YAML?'''
        testentry = self.Update()
        testentry.updateid = '1'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.status = 'stable'
        testentry.description = 'I am'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.severity = 'important'
        testentry.summary = 'summary'
        testentry.title = 'title'
        testentry.releasetitle = 'releasetitle'
        testentry.update_date = '1969-12-31 21:25:45'
        testentry.rights = 'rights'
        testentry.solution = 'solution'
        testentry.reboot_suggested = True
        testentry.relogin_suggested = True
        testentry.restart_suggested = True

        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())

        txt = '''title: Title
updateid: '1'
issued_date: 1969-12-31 18:00:00
update_date: 1969-12-31 21:25:45
releasetitle: Releasetitle
updatetype: security
severity: important
summary: summary
description: I am
solution: solution
reboot_suggested: true
relogin_suggested: true
restart_suggested: true
collections:
- asdf:
  - release_name: jkl
  - aaasdf-jkl-gh.noarch.rpm:
      arch: noarch
      name: aaasdf
      release: gh
      sums:
        md5: d41d8cd98f00b204e9800998ecf8427e
        sha: da39a3ee5e6b4b0d3255bfef95601890afd80709
      version: jkl
  - asdf-jkl-gh.src.rpm:
      arch: src
      name: asdf
      release: gh
      version: jkl
- iop:
  - release_name: qwe
  - aaasdf-jkl-gh.noarch.rpm:
      arch: noarch
      name: aaasdf
      release: gh
      sums:
        md5: d41d8cd98f00b204e9800998ecf8427e
        sha: da39a3ee5e6b4b0d3255bfef95601890afd80709
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
- http://2:
    refid: '2'
    title: Jkl
    type: self
updatefrom: me@example.com
status: stable
rights: rights
'''

        result = False
        if testentry.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I can't get YAML")

    def test_set_yaml_a(self):
        '''Can I set from YAML?'''
        testentry = self.Update()

        txt = '''updateid: '1'
updatefrom: me@example.com
updatetype: security
status: stable
description: "I am some\\ntext it\\nis\\nso true"
issued_date: 1969-12-31 18:00:00
severity: important
summary: summary
title: Title
releasetitle: Releasetitle
update_date: 1971-02-14 17:00:00
rights: rights
solution: solution
reboot_suggested: true
relogin_suggested: true
restart_suggested: true
collections:
- asdf:
  - asdf-jkl-gh.src.rpm
- iop:
  - release_name: qwe
  - aaasdf-jkl-gh.noarch.rpm:
      arch: noarch
      name: aaasdf
      release: gh
      version: jkl
  - awesome-jkl-gh.src.rpm
references:
- http://1:
    refid: '1'
    title: Asdf
    type: bugzilla
- http://2:
    refid: '2'
    title: Jkl
    type: self
'''

        desc = '''I am some
text it
is
so true'''

        testentry.yaml = txt

        result = False
        if testentry.updateid == '1':  # pragma: no cover
            if testentry.updatefrom == 'me@example.com':
                if testentry.updatetype == 'security':
                    if testentry.status == 'stable':
                        if testentry.description == desc:
                            if testentry.issued_date == datetime.datetime.strptime('1969-12-31 18:00:00', '%Y-%m-%d %H:%M:%S'):
                                if testentry.severity == 'important':
                                    if testentry.summary == 'summary':
                                        if testentry.title == 'Title':
                                            if testentry.releasetitle == 'Releasetitle':
                                                if testentry.update_date == datetime.datetime.strptime('1971-02-14 17:00:00', '%Y-%m-%d %H:%M:%S'):
                                                    if testentry.rights == 'rights':
                                                        if testentry.solution == 'solution':
                                                            if testentry.reboot_suggested:
                                                                if testentry.relogin_suggested:
                                                                    if testentry.restart_suggested:
                                                                        if len(testentry.collections) == 2:
                                                                            if len(testentry.collections['iop']) == 2:
                                                                                if testentry.collections['iop'].release_name == 'qwe':
                                                                                    if len(testentry.references) == 2:
                                                                                        if testentry.references['http://1'].refid == '1':
                                                                                            result = True

        self.assertTrue(result, msg="Seems I can't set from YAML")

    def test_get_yaml_b(self):
        '''Can I get YAML?'''
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

        txt = '''title: A Title
updateid: '1'
issued_date: 1969-12-31 18:00:00
update_date: 1969-12-31 18:00:00
releasetitle: Release Title
updatetype: security
severity: critical
summary: a summary
description: text
solution: solved
reboot_suggested: true
relogin_suggested: true
restart_suggested: true
collections:
- asdf:
  - release_name: jkl
  - aaasdf-jkl-gh.noarch.rpm:
      arch: noarch
      name: aaasdf
      release: gh
      sums:
        md5: d41d8cd98f00b204e9800998ecf8427e
        sha: da39a3ee5e6b4b0d3255bfef95601890afd80709
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
rights: exist
'''
        result = False
        if testentry.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get YAML")

    def test_set_yaml_b(self):
        '''Can I set from YAML?'''
        testentry = self.Update()
        txt = '''title: A Title
updateid: '1'
issued_date: 1969-12-31 18:00:00
update_date: 1969-12-31 18:00:00
releasetitle: Release Title
updatetype: security
severity: critical
summary: a summary
description: text
solution: solved
reboot_suggested: true
relogin_suggested: true
restart_suggested: true
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
rights: exist
'''

        testentry.yaml = txt
        result = False
        if testentry.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from YAML")

    def test_get_yaml_nil(self):
        '''Can I get YAML?'''
        testentry = self.Update()

        txt = '''{}
'''
        result = False
        if testentry.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get YAML")

    def test_set_yaml_nil(self):
        '''Can I set from YAML?'''
        testentry = self.Update()

        txt = '''{}
'''
        result = False
        testentry.yaml = txt
        if testentry.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from empty YAML")


class UpdateJSONViewTests(UpdateModelTests):
    ''' Test the JSON view for sanity '''
    Update = UpdateJ

    def test_get_json_a(self):
        testentry = self.Update()
        testentry.updateid = '1'
        testentry.updatefrom = 'me@example.com'
        testentry.updatetype = 'security'
        testentry.status = 'stable'
        testentry.description = 'I am'
        testentry.issued_date = '1969-12-31 18:00:00'
        testentry.severity = 'important'
        testentry.summary = 'summary'
        testentry.title = 'title'
        testentry.releasetitle = 'releasetitle'
        testentry.update_date = '1969-12-31 21:25:45'
        testentry.rights = 'rights'
        testentry.solution = 'solution'
        testentry.reboot_suggested = True
        testentry.relogin_suggested = True
        testentry.restart_suggested = True

        testentry.collections.add(self.coll_one_for_test())
        testentry.references.add(self.ref_one_for_test())
        testentry.collections.add(self.coll_two_for_test())
        testentry.references.add(self.ref_two_for_test())

        result = False

        expected = '{"status": "stable", "description": "I am", "updatetype": "security", "relogin_suggested": true, "restart_suggested": true, "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}, {"http://2": {"type": "self", "refid": "2", "title": "Jkl"}}], "issued_date": "1969-12-31 18:00:00", "update_date": "1969-12-31 21:25:45", "severity": "important", "rights": "rights", "updatefrom": "me@example.com", "title": "Title", "solution": "solution", "summary": "summary", "updateid": "1", "releasetitle": "Releasetitle", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "arch": "noarch", "version": "jkl", "sums": {"sha": "da39a3ee5e6b4b0d3255bfef95601890afd80709", "md5": "d41d8cd98f00b204e9800998ecf8427e"}, "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}, {"iop": [{"release_name": "qwe"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "arch": "noarch", "version": "jkl", "sums": {"sha": "da39a3ee5e6b4b0d3255bfef95601890afd80709", "md5": "d41d8cd98f00b204e9800998ecf8427e"}, "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "reboot_suggested": true}'

        if testentry.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="I can't get JSON")

    def test_set_json_a(self):
        testentry = self.Update()

        testentry.json = '{"status": "stable", "description": "I am", "updatetype": "security", "relogin_suggested": true, "restart_suggested": true, "references": [{"http://1": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}, {"http://2": {"type": "self", "refid": "2", "title": "Jkl"}}], "issued_date": "1969-12-31 18:00:00", "update_date": "1969-12-31 21:25:45", "severity": "important", "rights": "rights", "updatefrom": "me@example.com", "title": "Title", "solution": "solution", "summary": "summary", "updateid": "1", "releasetitle": "Releasetitle", "collections": [{"asdf": [{"release_name": "jkl"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}, {"iop": [{"release_name": "qwe"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}], "reboot_suggested": true}'
        result = False
        if testentry.updateid == '1':  # pragma: no cover
            if testentry.updatefrom == 'me@example.com':
                if testentry.updatetype == 'security':
                    if testentry.status == 'stable':
                        if testentry.description == 'I am':
                            if testentry.issued_date == datetime.datetime.strptime('1969-12-31 18:00:00', '%Y-%m-%d %H:%M:%S'):
                                if testentry.severity == 'important':
                                    if testentry.summary == 'summary':
                                        if testentry.title == 'Title':
                                            if testentry.releasetitle == 'Releasetitle':
                                                if testentry.update_date == datetime.datetime.strptime('1969-12-31 21:25:45', '%Y-%m-%d %H:%M:%S'):
                                                    if testentry.rights == 'rights':
                                                        if testentry.solution == 'solution':
                                                            if testentry.reboot_suggested:
                                                                if testentry.relogin_suggested:
                                                                    if testentry.restart_suggested:
                                                                        if len(testentry.collections) == 2:
                                                                            if len(testentry.collections['iop']) == 2:
                                                                                if testentry.collections['iop'].release_name == 'qwe':
                                                                                    if len(testentry.references) == 2:
                                                                                        if testentry.references['http://1'].refid == '1':
                                                                                            result = True
        self.assertTrue(result, msg="Seems I can't set from JSON")

    def test_get_json_nil(self):
        '''Can I get JSON?'''
        testentry = self.Update()

        txt = '''{}'''
        result = False
        if testentry.json == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't get JSON")

    def test_set_json_nil(self):
        '''Can I set from JSON?'''
        testentry = self.Update()

        txt = '''{}'''
        result = False
        testentry.json = txt
        if testentry.json == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't set from empty JSON")


class UpdateTests(UpdateEventsTests, UpdateXMLViewTests, UpdateYAMLViewTests, UpdateJSONViewTests):
    ''' Test the default object for sanity '''
    Update = UpdateinfoUpdate

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.Update.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

