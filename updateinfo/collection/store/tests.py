#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the CollectionStore class!
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

import unittest

from distutils.version import StrictVersion

from .events import CollectionStoreEvents
from .models import CollectionStoreModel
from .views import CollectionStoreXMLView
from .views import CollectionStoreYAMLView
from .views import CollectionStoreJSONView
from . import CollectionStore as UpdateinfoCollectionStore

from ... import Collection
from ... import Package

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree


######################
# Classes for test inheritance
######################
class CollectionStoreE(CollectionStoreModel, CollectionStoreEvents):
    '''Example inheritance'''
    def __init__(self, parent=None):
        CollectionStoreModel.__init__(self, parent)
        CollectionStoreEvents.__init__(self)

class CollectionStoreV(CollectionStoreModel, CollectionStoreEvents, CollectionStoreXMLView):
    '''Example inheritance'''
    def __init__(self, parent=None):
        CollectionStoreModel.__init__(self, parent)
        CollectionStoreEvents.__init__(self)
        CollectionStoreXMLView.__init__(self)

class CollectionStoreY(CollectionStoreModel, CollectionStoreEvents, CollectionStoreYAMLView):
    '''Example inheritance'''
    def __init__(self, parent=None):
        CollectionStoreModel.__init__(self, parent)
        CollectionStoreEvents.__init__(self)
        CollectionStoreYAMLView.__init__(self)

class CollectionStoreJ(CollectionStoreModel, CollectionStoreEvents, CollectionStoreJSONView):
    '''Example inheritance'''
    def __init__(self, parent=None):
        CollectionStoreModel.__init__(self, parent)
        CollectionStoreEvents.__init__(self)
        CollectionStoreJSONView.__init__(self)
######################

class CollectionStoreModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    CollectionStore = CollectionStoreModel
    Collection = Collection
    Package = Package

    @staticmethod
    def simpleadd(store, coll):
        '''a simple add'''
        store._collist[coll.short_name] = coll

    def pkg_one_for_test(self):
        '''testpkg'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg
    def pkg_two_for_test(self):
        '''testpkg'''
        testpkg = self.Package()
        testpkg.name = 'aaasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'noarch'
        return testpkg

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
        if str(type(self.Package())) == "<class 'updateinfo.package.Package'>":
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_package_store(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Package.PackageSumStore())) == "<class 'updateinfo.package.store.PackageSumStore'>":  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.CollectionStore()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_undef_at_constructor(self):
        '''Must I define things?'''
        result = False
        try:
            teststore = self.CollectionStore('asdf')
        except TypeError:
            result = True
        self.assertTrue(result, msg="It seems I can define things")

    def test_bool_false(self):
        '''Am I false when I should be?'''
        teststore = self.CollectionStore()
        self.assertFalse(teststore, msg="it seems I'm true when undef")

    def test_bool_true(self):
        '''Am I true when I should be?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        self.assertTrue(teststore, msg="it seems I'm false when def")

    def test_len_empty(self):
        '''Am I len 0 when I should be?'''
        teststore = self.CollectionStore()

        result = False
        if len(teststore) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Len is not 0")

    def test_len_def(self):
        '''Am I len 1 when I should be?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if len(teststore) == 1:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Len is not 1")

    def test_getitem_can(self):
        '''Can I get collections by name?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if teststore['asdf']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="cannot get coll by name")

    def test_getitem_cannot(self):
        '''Can I get collections by name?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        try:
            thing = teststore['aaaasdf']
        except KeyError:
            result = True

        self.assertTrue(result, msg="getitem does something weird")

    def test_contains_does_name(self):
        '''Can I find things by name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains by name not working")

    def test_contains_does_obj(self):
        '''Can I find things by name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if testcoll in teststore:
            result = True
        self.assertTrue(result, msg="contains by obj not working")

    def test_contains_doesnt_name(self):
        '''Can I find things by name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if 'aaa' not in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains by name not working")

    def test_contains_doesnt_obj(self):
        '''Can I find things by name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)
        testcoll2 = self.Collection(release_name='aasdf', short_name='aasdf')

        result = False
        if testcoll2 not in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="contains by obj not working")

    def test_iter(self):
        '''Can I loop through'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)
        found = []
        for item in teststore:
            found.append(item)

        result = False
        if found == ['asdf']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="iter not working")

    def test_eq_is(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="eq not working for eq")

    def test_eq_isnt_short_name(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='aasdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:
            result = True   # pragma: no cover

        self.assertFalse(result, msg="eq when not")

    def test_eq_isnt_release_name(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='aasdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:
            result = True  # pragma: no cover

        self.assertFalse(result, msg="eq when not")

    def test_eq_isnt_len(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        testcoll3 = self.Collection(release_name='aasdf', short_name='aasdf')

        self.simpleadd(teststore, testcoll)
        self.simpleadd(teststore, testcoll3)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        testpkg = self.pkg_two_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:
            result = True  # pragma: no cover

        self.assertFalse(result, msg="eq when not")

    def test_eq_isnt_coll_pkg(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        testpkg = self.pkg_two_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:
            result = True  # pragma: no cover

        self.assertFalse(result, msg="eq when not")

    def test_eq_isnt_pkg(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_two_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        result = False
        if teststore == teststore2:
            result = True  # pragma: no cover

        self.assertFalse(result, msg="eq when not")

    def test_eq_cant(self):
        '''is eq working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        try:
            if teststore == testcoll:
                pass  # pragma: no cover
        except TypeError:
            result = True

        self.assertTrue(result, msg="eq not working for weird")

    def test_ne_is(self):
        '''is ne working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        self.assertFalse((teststore != teststore2), msg="ne not working for eq")

    def test_ne_isnt(self):
        '''is ne working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        teststore2 = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_two_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore2, testcoll)

        self.assertTrue((teststore != teststore2), msg="ne not working for eq")

    def test_ne_cant(self):
        '''is ne working?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        try:
            if teststore != testcoll:
                pass  # pragma: no cover
        except TypeError:
            result = True

        self.assertTrue(result, msg="ne not working for weird")

    def test_contains_has(self):
        '''Does x in y work?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if 'asdf' in teststore:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="__contains__ not working?")

    def test_contains_nope(self):
        '''Does x in y work?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        self.simpleadd(teststore, testcoll)

        result = False
        if 'asxxxdf' in teststore:
            result = True  # pragma: no cover

        self.assertFalse(result, msg="__contains__ working on things not there?")

    def test_shortnames_empty(self):
        '''Can I see my shortnames'''
        teststore = self.CollectionStore()

        result = False
        if teststore.shortnames == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="shortnames not working")

    def test_shortnames(self):
        '''Can I see my shortnames'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        self.simpleadd(teststore, testcoll)

        result = False
        if teststore.shortnames == ('asdf',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="shortnames not working")

    def test_shortnames_sorted(self):
        '''Can I see my shortnames'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        self.simpleadd(teststore, testcoll)

        testcoll2 = self.Collection(release_name='aasdf', short_name='aasdf')
        self.simpleadd(teststore, testcoll2)

        result = False
        if teststore.shortnames == ('aasdf', 'asdf',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="shortnames not sorted")

    def test_shortnames_ro(self):
        '''Can I write to shortnames'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore.shortnames = 'asdf'
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Seems I can write to shortnames")

    def test_packages(self):
        '''Can I see my packages'''
        teststore = self.CollectionStore()

        # the actual add logic happens in Events, we just check if the
        # property is there

        result = False
        if teststore.packages == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I don't have a packages property")

    def test_packages_ro(self):
        '''Can I write to my packages'''
        teststore = self.CollectionStore()

        # the actual add logic happens in Events, we just check if the
        # property is there

        result = False
        try:
            teststore.packages = []
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Seems I can write to packages property")

    def test_filenames(self):
        '''Can I see my filenames'''
        teststore = self.CollectionStore()

        # the actual add logic happens in Events, we just check if the
        # property is there

        result = False
        if teststore.filenames == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I don't have a filenames property")

    def test_filenames_ro(self):
        '''Can I write to my filenames'''
        teststore = self.CollectionStore()

        # the actual add logic happens in Events, we just check if the
        # property is there

        result = False
        try:
            teststore.filenames = []
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg="Seems I can write to filenames property")

class CollectionStoreEventTests(CollectionStoreModelTests):
    ''' Test the Events for sanity '''
    CollectionStore = CollectionStoreE

    def test_setitem_bad_item(self):
        '''Don't support setitem'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore['asdf'] = 'asdf'
        except TypeError:
            result = True
        self.assertTrue(result, msg="Seems I can __setitem__ to something weird")

    def test_setitem_good_item(self):
        '''Don't support setitem'''
        teststore = self.CollectionStore()

        result = False
        teststore['asdf'] = self.Collection(short_name='asdf')

        if 'asdf' in teststore:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Seems I can't __setitem__ to some collection")

    def test_setitem_good_item_bad_name(self):
        '''Don't support setitem'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore['af'] = self.Collection(short_name='asdf')
        except ValueError:
            result = True

        self.assertTrue(result, msg="Seems I can __setitem__ with bad names")

    def test_add_invalid(self):
        '''Simple invalid add'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore.add('asdf')
        except TypeError:
            result = True
        self.assertTrue(result, msg="Seems I can add weird stuff")

    def test_add_valid(self):
        '''Simple add'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add")

    def test_add_release_name(self):
        '''Simple add'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add")

    def test_add_all_names(self):
        '''Simple add'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add")

    def test_add_valid_two_pkg(self):
        '''Simple add with two packages'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add")

    def test_add_almost_valid_two_pkg(self):
        '''Add with two packages and force set of short_name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if testcoll.short_name in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add with limited names")

    def test_add_invalid_two_pkg(self):
        '''Add with two packages and force set of short_name'''
        teststore = self.CollectionStore()
        testcoll = self.Collection()
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)

        result = False
        try:
            teststore.add(testcoll)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems I can add with no names")

    def test_add_package_to_two_diff_collections(self):
        '''Make sure we can have the same package in two different collections'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        testcoll2 = self.Collection(short_name='jkl')
        testcoll2.add(testpkg)
        testcoll2.add(testpkg2)
        teststore.add(testcoll2)

        result = False
        if testpkg in teststore['asdf']:  # pragma: no cover
            if testpkg in teststore['jkl']:
                if testpkg2 in teststore['asdf']:
                    if testpkg2 in teststore['jkl']:
                        result = True
        self.assertTrue(result, msg="Seems I cant add the same package to different collections")


    def test_add_via_xmlobj(self):
        '''Try to add a package via its xml etree'''
        teststore = self.CollectionStore()
        testcoll = self.Collection('asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)

        teststore.add(testcoll.xmletree)

        result = False
        if 'asdf' in teststore:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems I cant add via xmlobj")

    def test_add_has_pkg_names(self):
        '''Make sure the collection package names bubble up'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        teststore.add(testcoll)

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        result = False
        if teststore.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems packages not right")

    def test_pkg_added_after_coll_to_store(self):
        '''
            Make sure .packages has the right names when
             the package is added after the collection
        '''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        teststore.add(testcoll)

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        result = False
        if teststore.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems packages not right")

    def test_pkg_added_before_coll_to_store(self):
        '''
            Make sure .packages has the right names when
             the package is before the collection
        '''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        teststore.add(testcoll)

        result = False
        if teststore.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems packages not right")

    def test_add_has_pkg_names_sorted(self):
        '''Make sure the collection package names bubble up'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if teststore.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems packages not sorted")

    def test_add_has_filenames_names(self):
        '''Make sure the collection package names bubble up'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        teststore.add(testcoll)

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        result = False
        if teststore.filenames == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems filenames not right")

    def test_filenames_added_after_coll_to_store(self):
        '''
            Make sure .filenames has the right names when
             the package is added after the collection
        '''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        teststore.add(testcoll)

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        result = False
        if teststore.filenames == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems filenames not right")

    def test_filenames_added_before_coll_to_store(self):
        '''
            Make sure .filenames has the right names when
             the package is before the collection
        '''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')

        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)

        teststore.add(testcoll)

        result = False
        if teststore.filenames == ('asdf-jkl-gh.src.rpm',):
            result = True
        self.assertTrue(result, msg="Seems filenames not right")

    def test_add_has_filenames_names_sorted(self):
        '''Make sure the collection package names bubble up'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if teststore.filenames == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems filenames not sorted")

    def test_add_duplicates_merge(self):
        '''Duplicates should be merged'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        testcoll2 = self.Collection(release_name='asdf')
        testpkg2 = self.pkg_two_for_test()
        testcoll2.add(testpkg2)
        teststore.add(testcoll2)

        result = False
        if len(teststore) == 1:  # pragma: no cover
            if teststore.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):
                if teststore[testcoll.short_name].release_name == 'asdf':
                    result = True
        self.assertTrue(result, msg="Seems duplicates arent merged")

    def test_add_duplicates_merge_all_names(self):
        '''Duplicates should be merged'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        testcoll2 = self.Collection(short_name='asdf', release_name='asdf')
        testpkg2 = self.pkg_two_for_test()
        testcoll2.add(testpkg2)
        teststore.add(testcoll2)

        result = False
        if len(teststore) == 1:  # pragma: no cover
            if teststore.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):
                if teststore[testcoll.short_name].release_name == 'asdf':
                    result = True
        self.assertTrue(result, msg="Seems duplicates arent merged")

    def test_add_duplicates_merge_short_names(self):
        '''Duplicates should be merged'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        testcoll2 = self.Collection(short_name='asdf')
        testpkg2 = self.pkg_two_for_test()
        testcoll2.add(testpkg2)
        teststore.add(testcoll2)

        result = False
        if len(teststore) == 1:  # pragma: no cover
            if teststore.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):
                if teststore[testcoll.short_name].short_name == 'asdf':
                    result = True

        self.assertTrue(result, msg="Seems duplicates arent merged")

    def test_add_duplicates_merge_release_names(self):
        '''Duplicates should be merged'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        testcoll2 = self.Collection(release_name='asdf')
        testpkg2 = self.pkg_two_for_test()
        testcoll2.add(testpkg2)
        teststore.add(testcoll2)

        result = False
        if len(teststore) == 1:  # pragma: no cover
            if teststore.packages == ('aaasdf-jkl-gh.noarch.rpm', 'asdf-jkl-gh.src.rpm'):
                if teststore[testcoll.short_name].release_name == 'asdf':
                    result = True
        self.assertTrue(result, msg="Seems duplicates arent merged")

    def test_add_duplicates_merge_disabled(self):
        '''Duplicates should be merged'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf')
        testpkg = self.pkg_one_for_test()
        testcoll.add(testpkg)
        teststore.add(testcoll)

        testcoll2 = self.Collection(release_name='asdf')
        testpkg2 = self.pkg_two_for_test()
        testcoll2.add(testpkg2)

        result = False
        try:
            teststore.add(testcoll2, merge=False)
        except ValueError:
            result = True

        self.assertTrue(result, msg="Seems merge is wrong")

    def test_new_coll_can(self):
        '''Make sure the 'new' method works'''
        teststore = self.CollectionStore()
        teststore.create('asdf', 'jkl')
        testpkg = self.pkg_one_for_test()
        teststore['jkl'].add(testpkg)

        result = False
        if teststore.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems create() doesn't work")

    def test_new_coll_can_short_only(self):
        '''Make sure the 'new' method works'''
        teststore = self.CollectionStore()
        teststore.create(short_name='jkl')
        testpkg = self.pkg_one_for_test()
        teststore['jkl'].add(testpkg)

        result = False
        if teststore.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems create() doesn't work")

    def test_new_coll_cant(self):
        '''Make sure the 'new' method requires stuff'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore.create()
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems create() doesn't work")

    def test_remove_cant_null(self):
        '''We shouldn't be able to remove 'null' collections'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore.remove(self.Collection())
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems remove() on a null collection is odd")

    def test_remove_cant_weird(self):
        '''Make sure the 'new' method requires stuff'''
        teststore = self.CollectionStore()

        result = False
        try:
            teststore.remove(1)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems remove() on a weird value is odd")

    def test_remove_can_name(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        teststore.remove(testcoll.short_name)
        if len(teststore) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems remove isn't right")

    def test_remove_can_name_str(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        teststore.remove(str(testcoll.short_name))
        if len(teststore) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems remove isn't right")

    def test_remove_can_obj(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)

        result = False
        teststore.add(testcoll)
        teststore.remove(testcoll)

        if len(teststore) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems remove isn't right")

    def test_remove_updates_pkglist(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)

        result = False
        teststore.add(testcoll)
        teststore.remove(testcoll)

        if teststore.packages == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems remove doesn't clean up list")

    def test_remove_cant(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        try:
            teststore.remove('xxxxxxxxxxxxxx')
        except KeyError:
            result = True
        self.assertTrue(result, msg="Seems remove isn't right")

    def test_remove_bad_type(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        try:
            teststore.remove(0)
        except ValueError:
            result = True
        self.assertTrue(result, msg="Seems remove isn't right")

    def test_del_can(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        del teststore[testcoll.short_name]
        if len(teststore) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems __del__ isn't right")

    def test_del_can_check_packages(self):
        '''make sure I can remove things'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        del teststore[testcoll.short_name]
        if teststore.packages == ():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Seems __del__ isn't right")

    def test_del_cant(self):
        '''try to remove what doesn't exist should be bad'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(release_name='asdf')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        try:
            del teststore['xxxxxxxxxxx']
        except KeyError:
            result = True
        self.assertTrue(result, msg="Seems __del__ isn't right")

class CollectionStoreXMLViewTests(CollectionStoreModelTests):
    ''' Test the XMLView for sanity '''
    CollectionStore = CollectionStoreV

    def test_pprint(self):
        '''Do I get pretty output'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        text = '''<pkglist>
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
'''
        result = False
        if str(teststore) == text:  # pragma: no cover
            result = True
        self.assertTrue(True, msg="I don't pprint")

    def test_get_xml(self):
        '''Do I get raw xml output'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        text = '<pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist>'

        result = False
        if teststore.xml == text:  # pragma: no cover
            result = True
        self.assertTrue(True, msg="my xml is broken")

    def test_set_xml(self):
        '''Can I set from xml?'''
        teststore = self.CollectionStore()

        text = '<pkglist><collection short="asdf"><name>jkl</name><package arch="noarch" name="aaasdf" release="gh" version="jkl"><filename>aaasdf-jkl-gh.noarch.rpm</filename></package><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection></pkglist>'

        teststore.xml = text
        result = False
        if teststore.shortnames == ('asdf',):  # pragma: no cover
            result = True
        self.assertTrue(True, msg="cant set from xml")

    def test_get_xmlobj(self):
        '''Do I get the xmletree I want?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if teststore.xmletree.tag == 'pkglist':  # pragma: no cover
            result = True
        self.assertTrue(True, msg="cant get xmletree")

    def test_get_xmlobj_is_element(self):
        '''Do I get the xmletree I want?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        result = False
        if xmletree.iselement(teststore.xmletree):  # pragma: no cover
            result = True
        self.assertTrue(True, msg="cant get xmletree")

    def test_set_xmlobj(self):
        '''Can i set from an xmletree?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        teststore2 = self.CollectionStore()

        teststore2.xmletree = teststore.xmletree

        result = False
        if teststore2.shortnames == ('asdf',):  # pragma: no cover
            result = True
        self.assertTrue(True, msg="cant set xmletree")

    def test_set_bad_xmlobj(self):
        '''Do I get the xmletree I want?'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        teststore2 = self.CollectionStore()

        xmltree = teststore.xmletree
        xmltree.tag = 'xxxxxxxxx'

        result = False
        try:
            teststore2.xmletree = xmltree
        except ValueError:
            result = True
        self.assertTrue(True, msg="can set xmletree from bad xml")

class CollectionStoreYAMLViewTests(CollectionStoreModelTests):
    ''' Test the YAMLView for sanity '''
    CollectionStore = CollectionStoreY

    def test_get_yaml_a(self):
        '''Can I get the basic YAML'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll.add(testpkg2)
        teststore.add(testcoll)

        txt = '''collections:
- asdf:
  - {release_name: jkl}
  - aaasdf-jkl-gh.noarch.rpm: {arch: noarch, name: aaasdf, release: gh, version: jkl}
  - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        if teststore.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="basic yaml failed")

    def test_get_yaml_b(self):
        '''Can I get the basic YAML'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testcoll2 = self.Collection(short_name='jkl', release_name='gh')
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll2.add(testpkg2)
        teststore.add(testcoll)
        teststore.add(testcoll2)

        txt = '''collections:
- asdf:
  - {release_name: jkl}
  - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
- jkl:
  - {release_name: gh}
  - aaasdf-jkl-gh.noarch.rpm: {arch: noarch, name: aaasdf, release: gh, version: jkl}
'''

        result = False
        if teststore.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="basic yaml failed")

    def test_set_yaml_a(self):
        '''Can I set from YAML?'''
        teststore = self.CollectionStore()

        txt = '''collections:
- asdf:
    - {release_name: jkl}
    - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
- jkl:
    - {release_name: gh}
    - aaasdf-jkl-gh.noarch.rpm: {arch: noarch, name: aaasdf, release: gh,
        version: jkl}
'''

        result = False
        teststore.yaml = txt
        if len(teststore) == 2:  # pragma: no cover
            if len(teststore['asdf']) == 1:
                if len(teststore['jkl']) == 1:
                    result = True
        self.assertTrue(result, msg="basic yaml failed")

    def test_set_yaml_bad(self):
        '''Can I set from YAML?'''
        teststore = self.CollectionStore()

        txt = '''collectbions:
- asdf:
    - {release_name: jkl}
    - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
- jkl:
    - {release_name: gh}
    - aaasdf-jkl-gh.noarch.rpm: {arch: noarch, name: aaasdf, release: gh,
        version: jkl}
'''

        result = False
        try:
            teststore.yaml = txt
        except ValueError:
            result = True
        self.assertTrue(result, msg="set yaml takes weird")

    def test_set_yaml_bad_b(self):
        '''Can I set from YAML?'''
        teststore = self.CollectionStore()

        txt = '''collections:
- asdf:
    - {release_name: jkl}
    - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
- jkl:
    - {release_name: gh}
    - aaasdf-jkl-gh.noarch.rpm: {arch: noarch, name: aaasdf, release: gh,
        version: jkl}
collectinons:
- asdf:
    - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        try:
            teststore.yaml = txt
        except ValueError:
            result = True
        self.assertTrue(result, msg="set yaml takes weird")

class CollectionStoreJSONViewTests(CollectionStoreModelTests):
    ''' Test the YAMLView for sanity '''
    CollectionStore = CollectionStoreJ

    def test_get_json_a(self):
        '''get some JSON'''
        teststore = self.CollectionStore()
        testcoll = self.Collection(short_name='asdf', release_name='jkl')
        testpkg = self.pkg_one_for_test()
        testcoll2 = self.Collection(short_name='jkl', release_name='gh')
        testpkg2 = self.pkg_two_for_test()
        testcoll.add(testpkg)
        testcoll2.add(testpkg2)
        teststore.add(testcoll)
        teststore.add(testcoll2)

        expected = '{"collections": [{"asdf": [{"release_name": "jkl"}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}, {"jkl": [{"release_name": "gh"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}]}]}'
        result = False
        if teststore.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get JSON")

    def test_set_json_a(self):
        '''set from JSON'''
        teststore = self.CollectionStore()
        teststore.json = '{"collections": [{"asdf": [{"release_name": "jkl"}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}, {"jkl": [{"release_name": "gh"}, {"aaasdf-jkl-gh.noarch.rpm": {"release": "gh", "version": "jkl", "arch": "noarch", "name": "aaasdf"}}]}]}'

        result = False
        if len(teststore) == 2:  # pragma: no cover
            if len(teststore['asdf']) == 1:
                if len(teststore['jkl']) == 1:
                    result = True

        self.assertTrue(result, msg="Can't set from JSON")

class CollectionStoreTests(CollectionStoreEventTests, CollectionStoreXMLViewTests, CollectionStoreYAMLViewTests, CollectionStoreJSONViewTests):
    ''' Test the default object for sanity '''
    CollectionStore = UpdateinfoCollectionStore

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.CollectionStore.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

