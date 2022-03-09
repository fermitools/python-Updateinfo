#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the Collection class!
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

from .models import CollectionModel
from .events import CollectionEvents
from .views import CollectionXMLView
from .views import CollectionYAMLView
from .views import CollectionJSONView
from . import Collection as UpdateinfoCollection

from .. import Package as UinfoPackage

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

######################
# Classes for test inheritance
######################
class CollectionE(CollectionModel, CollectionEvents):
    '''example inheritance'''
    def __init__(self, release_name=None, short_name=None):
        CollectionModel.__init__(self, release_name, short_name)
        CollectionEvents.__init__(self)

class CollectionX(CollectionModel, CollectionEvents, CollectionXMLView):
    '''example inheritance'''
    def __init__(self, release_name=None, short_name=None):
        '''example init'''
        CollectionModel.__init__(self, release_name, short_name)
        CollectionEvents.__init__(self)
        CollectionXMLView.__init__(self)

class CollectionY(CollectionModel, CollectionEvents, CollectionYAMLView):
    '''example inheritance'''
    def __init__(self, release_name=None, short_name=None):
        '''example init'''
        CollectionModel.__init__(self, release_name, short_name)
        CollectionEvents.__init__(self)
        CollectionYAMLView.__init__(self)

class CollectionJ(CollectionModel, CollectionEvents, CollectionJSONView):
    '''example inheritance'''
    def __init__(self, release_name=None, short_name=None):
        '''example init'''
        CollectionModel.__init__(self, release_name, short_name)
        CollectionEvents.__init__(self)
        CollectionJSONView.__init__(self)
######################

class CollectionModelTests(unittest.TestCase):
    '''
        Test the Model for sanity
    '''
    Package = UinfoPackage
    Collection = CollectionModel

    def simple_add(self, obj, packageobj):
        '''The model doesn't have add logic, so make some for test use'''
        if not isinstance(packageobj, self.Package):  # pragma: no cover
            raise TypeError('I can only add PackageModel type objects')
        obj._pkglist[packageobj.filename] = packageobj

        if packageobj.filename in obj:
            return True

        raise RuntimeError('Attempted to add package to collection, but not found after add')  # pragma: no cover

    def simple_pkg(self):
        '''Here is a standard looking Package'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        return testpkg

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

    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.Collection()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_def_at_constructor_name(self):
        ''' Can I define at the constructor?  '''
        result = False
        testcoll = self.Collection(release_name='asdf')
        if testcoll.release_name == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I cannot define release_name at self.Collection()__init_')

    def test_name(self):
        ''' Can I define release_name?  '''
        result = False
        testcoll = self.Collection()
        testcoll.release_name = 'asdf'
        if testcoll.release_name == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I cannot define release_name')

    def test_def_at_constructor_shortname(self):
        ''' Can I define at the constructor?  '''
        result = False
        testcoll = self.Collection(short_name='asdf')
        if testcoll.short_name == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I cannot define release_name at self.Collection()__init_')

    def test_shortname(self):
        ''' Can I define short_name?  '''
        result = False
        testcoll = self.Collection()
        testcoll.short_name = 'asdf'
        if testcoll.short_name == 'asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I cannot define short_name')

    def test_bool_unset(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection()
        self.assertFalse(testcoll, msg='Seems I am true when undef')

    def test_bool_short_only(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(short_name='asdf')
        self.assertFalse(testcoll, msg='Seems I am true when short only')

    def test_bool_release_only(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(release_name='asdf')
        self.assertFalse(testcoll, msg='Seems I am true when release only')

    def test_bool_all_names(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        self.assertFalse(testcoll, msg='Seems I am true when names are set')

    def test_bool_pkg_only(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection()

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertFalse(testcoll, msg='Seems I am true when Ive a package and no names')

    def test_bool_pkg_blank_short_name(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(short_name='')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertFalse(testcoll, msg='Seems I am true when Ive a package and no names')

    def test_bool_pkg_blank_release_name(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(release_name='')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertFalse(testcoll, msg='Seems I am true when Ive a package and no names')

    def test_bool_pkg_blank_names(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(short_name='', release_name='')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertFalse(testcoll, msg='Seems I am true when Ive a package and no names')

    def test_bool_pkg_and_name_only(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(release_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertTrue(testcoll, msg='Seems I am False when Ive a name and a package')

    def test_bool_pkg_and_short_name_only(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertTrue(testcoll, msg='Seems I am False when Ive a name and a package')

    def test_bool_pkg_and_names(self):
        ''' Am I true when I should be?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        self.assertTrue(testcoll, msg='Seems I am False when Ive all names and a package')

    def test_eq_to_none(self):
        ''' Should not be eq to None'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == None: # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_to_empty(self):
        ''' Should not be eq to '' '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == '': # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_to_empty_tuple(self):
        ''' Should not be eq to ()'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == (): # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_to_empty_list(self):
        ''' Should not be eq to []'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == (): # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_to_empty_dict(self):
        ''' Should not be eq to {}'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == {}: # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_not_bad_pkg(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.arch = 'noarch'

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll == testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_not_bad_name(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='adf', short_name='asdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll == testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_not_bad_shortname(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='sdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll == testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_not_len(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if testcoll == testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_not_pkg(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        testpkg2 = self.simple_pkg()
        testpkg2.srpm = 'asdfasdfsadf'

        self.simple_add(testcoll2, testpkg2)

        result = False
        if testcoll == testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am eq when not really')

    def test_eq_when_eq(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll == testcoll2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I am not eq when I really am')

    def test_eq_to_weird(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        result = False
        try:
            if testcoll == 0:
                pass  # pragma: no cover
        except TypeError:
            result = True
        self.assertTrue(result, msg='Seems I am not eq when I really am')

    def test_ne_when_not_bad_pkg(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.arch = 'noarch'

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll != testcoll2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I am eq when not really')

    def test_ne_when_not_bad_name(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='adf', short_name='asdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll != testcoll2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I am eq when not really')

    def test_ne_when_not_bad_shortname(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='sdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll != testcoll2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I am eq when not really')

    def test_ne_when_eq(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testcoll2 = self.Collection(release_name='asdf', short_name='asdf')

        self.simple_add(testcoll2, testpkg)

        result = False
        if testcoll != testcoll2:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='Seems I am not eq when I really am')

    def test_ne_to_weird(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        result = False
        try:
            if testcoll != 0:
                pass  # pragma: no cover
        except TypeError:
            result = True
        self.assertTrue(result, msg='Seems I am not eq when I really am')


    def test_iter(self):
        ''' does eq fail when it should?  '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)
        pkglist = ['asdf-jkl-gh.src.rpm']
        found = []
        for item in testcoll:
            found.append(item)

        result = False
        if pkglist == found:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems __iter__ not working')

    def test_len_none(self):
        ''' does len(coll) work '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        if len(testcoll) == 0:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems __len__ not working for empty')

    def test_len_one(self):
        ''' does len(coll) work '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        self.simple_add(testcoll, testpkg)

        result = False
        if len(testcoll) == 1:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems __len__ not working for not empty')

    def test_getitem_has(self):
        ''' can we fetch like a dict'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        self.simple_add(testcoll, testpkg)

        trial = testcoll['asdf-jkl-gh.src.rpm']

        result = False
        if testpkg == trial:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I couldnt fetch like a dict')

    def test_getitem_not_found(self):
        ''' do we error on missing keys like a dict'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        try:
            testcoll['asdf-jkl-gh.src.rpm']
        except KeyError:
            result = True
        self.assertTrue(result, msg='Seems I dont raise KeyError on missing keys')

    def test_contains_has_filename(self):
        '''test in'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        result = False
        if 'asdf-jkl-gh.src.rpm' in testcoll:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='__contains__ doesnt work on package names')

    def test_contains_has_package(self):
        '''test in'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        result = False
        if testpkg in testcoll:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='__contains__ doesnt work on package type')

    def test_contains_doesnt_have_package(self):
        '''test in'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.epoch = '3'

        result = False
        if testpkg2 in testcoll:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='__contains__ doesnt do full compaire on pkg objects')

    def test_contains_no_has_filename(self):
        '''test in'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        self.simple_add(testcoll, testpkg)

        result = False
        if 'asdf-jkl-ghj.src.rpm' in testcoll:
            result = True  # pragma: no cover
        self.assertFalse(result, msg='__contains__ doesnt work on package names')

class CollectionEventsTests(CollectionModelTests):
    '''
        Test the Events for sanity
    '''
    Collection = CollectionE

    def test_add_can(self):
        '''check add method'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.epoch = None

        testcoll.add(testpkg)

        result = False
        if testpkg in testcoll:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='cant CollectionEvents.add()')

    def test_duplicate_add(self):
        '''check add method'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()

        testcoll.add(testpkg2)

        result = False
        if testpkg in testcoll:  # pragma: no cover
            if len(testcoll) == 1:
                result = True

        self.assertTrue(result, msg='adding duplicates duplicates')

    def test_duplicate_add_again(self):
        '''check add method'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.filename = testpkg.filename
        testpkg2.epoch = '1'
        testpkg2.srpm = 'testing'
        testpkg2.src_repo_base = '/path/'
        testpkg2.builddate = 0
        testpkg2.reboot_suggested = True
        testpkg2.restart_suggested = True
        testpkg2.relogin_suggested = True
        testpkg2.sums['md5'] = 'asdf'

        testcoll.add(testpkg2)

        result = False
        if testpkg in testcoll:  # pragma: no cover
            if len(testcoll) == 1:
                result = True

        self.assertTrue(result, msg='adding duplicates duplicates')

    def test_duplicate_add_less_interesting(self):
        '''check add method'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        testpkg2 = self.Package()
        testpkg2.filename = testpkg.filename
        testpkg2.srpm = 'testing'
        testpkg2.src_repo_base = '/path/'
        testpkg2.reboot_suggested = True
        testpkg2.restart_suggested = True
        testpkg2.relogin_suggested = True
        testpkg2.sums['md5'] = 'asdf'

        testcoll.add(testpkg2)

        result = False
        if testpkg.filename in testcoll:  # pragma: no cover
            if len(testcoll) == 1:
                result = True

        self.assertTrue(result, msg='adding duplicates duplicates')

    def test_duplicate_looking_filenames_first(self):
        '''Try adding a second package with a similar name, but different path'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.filename = 'Packages/asdf-jkl-gh.src.rpm'
        testcoll.add(testpkg2)

        result = False
        if testpkg.filename in testcoll:  # pragma: no cover
            if len(testcoll) == 2:
                result = True

        self.assertTrue(result, msg='adding duplicate under path failes')

    def test_duplicate_looking_filenames_second(self):
        '''Try adding a second package with a similar name, but different path'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.filename = 'Packages/asdf-jkl-gh.src.rpm'

        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testcoll.add(testpkg2)

        result = False
        if testpkg.filename in testcoll:  # pragma: no cover
            if len(testcoll) == 2:
                result = True

        self.assertTrue(result, msg='adding duplicate under path failes')

    def test_duplicate_add_nomerge(self):
        '''check add method'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        result = False
        try:
            testcoll.add(testpkg, merge=False)
        except ValueError:
            result = True

        self.assertTrue(result, msg="adding duplicates when I shouldn't")

    def test_add_two(self):
        '''check add method lets you have more than one'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.name = 'asdff'
        testcoll.add(testpkg2)

        result = False
        if testpkg in testcoll:  # pragma: no cover
            if testpkg2 in testcoll:
                result = True

        self.assertTrue(result, msg='cant set two items CollectionEvents.add()')

    def test_cant_add_flat_txt(self):
        '''Make sure I can only add valid things'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')
        test = 'asdf'

        result = False
        try:
            testcoll.add(test)
        except TypeError:
            result = True

        self.assertTrue(result, msg='can add non-Package types')

    def test_add_from_file_no_file_exists(self):
        '''Try to add from an existing file'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        try:
            testcoll.add_filename('/tmp/filenotfound', readfile=True)
        except IOError:
            result = True
        self.assertTrue(result, msg="Did not try to open file for adding")

    def test_add_filename(self):
        '''Try to add just a filename'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testcoll.add_filename('afilename')

        result = False
        if 'afilename' in testcoll:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Did not add filename")

    def test_add_xmlobj(self):
        '''Try to add a package via its xml etree'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg.xmletree)

        result = False
        if testcoll.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="cant add via xmlobj")

    def test_remove_by_obj(self):
        '''Make sure remove works'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        testcoll.remove(testpkg)
        if testpkg not in testcoll:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='cant remove by obj')

    def test_remove_by_filename(self):
        '''Make sure remove works'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        testcoll.remove(testpkg.filename)
        if testpkg.filename not in testcoll:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='cant remove by filename')

    def test_remove_by_filename_str(self):
        '''Make sure remove works'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        testcoll.remove(str(testpkg.filename))
        if testpkg.filename not in testcoll:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='cant remove by filename')


    def test_remove_by_nonsense_int(self):
        '''Make sure remove works'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        try:
            testcoll.remove(12345)
        except ValueError:
            result = True

        self.assertTrue(result, msg='remove accepts weird values')

    def test_delitem_has(self):
        ''' del items like a dict'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        del testcoll['asdf-jkl-gh.src.rpm']
        if 'asdf-jkl-gh.src.rpm' not in testcoll:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Seems I cant remove packages with del')

    def test_delitem_not_found(self):
        ''' del items like a dict, missing raises KeyError'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        try:
            del testcoll['asdf-jkl-gh.src.rpm']
        except KeyError:
            result = True

        self.assertTrue(result, msg='Seems removing with del on non-real doesnt raise KeyError')

    def test_setitem(self):
        ''' __setitem__ makes overrides easier '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        result = False
        testcoll['asdf-jkl-gh.src.rpm'] = testpkg
        if testpkg in testcoll:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='__setitem__ should accept packages, didnt')

    def test_setitem_cant_filename(self):
        ''' __setitem__ not implemented '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        result = False
        try:
            testcoll['asdfjkl-gh.src.rpm'] = testpkg
        except ValueError:
            result = True
        self.assertTrue(result, msg='__setitem__ took a weird filename')

    def test_setitem_cant_weird(self):
        ''' __setitem__ not implemented '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        result = False
        try:
            testcoll['asdfjkl-gh.src.rpm'] = 'asdf'
        except TypeError:
            result = True
        self.assertTrue(result, msg='__setitem__ took a weird arg')

    def test_packages_attrib(self):
        ''' see if I can get my packages '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        if testcoll.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='packages property not working')

    def test_packages_basename(self):
        '''make sure it strips to basename'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.filename = 'thingy/asdf-jkl-gh.src.rpm'
        testcoll.add(testpkg)

        result = False
        if testcoll.packages == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='packages property not working')

    def test_packages_attrib_sorted(self):
        ''' see if I can get my packages '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.name = 'aaasdf'
        testcoll.add(testpkg2)

        result = False
        if testcoll.packages == ('aaasdf-jkl-gh.src.rpm', 'asdf-jkl-gh.src.rpm'):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='packages property not sorted')

    def test_packages_attrib_ro(self):
        ''' see if I can get my packages '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        try:
            testcoll.packages = ('asdf-jkl-gh.src.rpm',)
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg='__setitem__ should raise NotImplementedError, didnt')

    def test_filenames_attrib(self):
        ''' see if I can get my filenames '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False
        if testcoll.filenames == ('asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='filenames property not working')

    def test_filenames_not_basename(self):
        '''make sure it strips to basename'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testpkg.filename = 'thingy/asdf-jkl-gh.src.rpm'
        testcoll.add(testpkg)

        result = False
        if testcoll.filenames == ('thingy/asdf-jkl-gh.src.rpm',):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='filenames property not working')

    def test_filenames_attrib_sorted(self):
        ''' see if I can get my filenames '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.name = 'aaasdf'
        testcoll.add(testpkg2)

        result = False
        if testcoll.filenames == ('aaasdf-jkl-gh.src.rpm', 'asdf-jkl-gh.src.rpm'):
            result = True
        self.assertTrue(result, msg='filenames property not sorted')

    def test_filenames_attrib_ro(self):
        ''' see if I can get my filenames '''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        result = False
        try:
            testcoll.filenames = ('asdf-jkl-gh.src.rpm',)
        except NotImplementedError:
            result = True
        self.assertTrue(result, msg='__setitem__ should raise NotImplementedError, didnt')


class CollectionXMLViewTests(CollectionModelTests):
    ''' Test the XML View for sanity '''
    Collection = CollectionX

    def test_as_str(self):
        '''does the xml pprint correctly'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        ppoutput = '''<collection short="asdf">
  <name>asdf</name>
  <package arch="src" name="asdf" release="gh" version="jkl">
    <filename>asdf-jkl-gh.src.rpm</filename>
  </package>
</collection>
'''

        result = False
        if str(testcoll) == ppoutput:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='pprint doesnt look right')

    def test_get_xml(self):
        '''get some xml'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        result = False
        if testcoll.xml == '<collection short="asdf"><name>asdf</name><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='as xml isnt right')

    def test_get_xml_short_only(self):
        '''get some xml'''
        testcoll = self.Collection(short_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        result = False
        if testcoll.xml == '<collection short="asdf"><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='as xml isnt right')

    def test_get_xml_release_only(self):
        '''get some xml'''
        testcoll = self.Collection(release_name='asdf')

        testpkg = self.simple_pkg()

        testcoll.add(testpkg)

        result = False
        if testcoll.xml == '<collection><name>asdf</name><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='as xml isnt right')


    def test_set_xml(self):
        '''set some xml'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        string = '<collection short="asdf"><name>asdf</name><package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package></collection>'

        result = False
        testcoll.xml = string

        if testcoll.xml == string:  # pragma: no cover
            result = True

        self.assertTrue(result, msg='cant set from xml')

    def test_get_xml_obj(self):
        '''get xml etree'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False

        if testcoll.xmletree.tag == 'collection':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='get xml obj for collection')

    def test_get_xml_obj_is_element(self):
        '''get xml etree'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        result = False

        if xmletree.iselement(testcoll.xmletree):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='get xml obj for collection')

    def test_set_xml_obj(self):
        '''set xml etree'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        testcoll2 = self.Collection()

        result = False
        testcoll2.xmletree = testcoll.xmletree

        if testcoll == testcoll2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='cant set from xmlobj')

    def test_set_xml_obj_bad_tag(self):
        '''set xml etree'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        testcoll2 = self.Collection()

        xmltree = testcoll.xmletree
        xmltree.tag = 'asdf'

        result = False
        try:
            testcoll2.xmletree = xmltree
        except ValueError:
            result = True

        self.assertTrue(result, msg='can set from bad xmlobj')

class CollectionYAMLViewTests(CollectionModelTests):
    ''' Test the YAML View for sanity '''
    Collection = CollectionY

    def test_get_yaml(self):
        '''Can i get a basic YAML version?'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        txt = '''asdf:
- {release_name: asdf}
- asdf-jjkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jjkl}
- asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        if testcoll.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="basic yaml failed")

    def test_get_yaml_norelease_name(self):
        '''Can i get a basic YAML version?'''
        testcoll = self.Collection(short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        txt = '''asdf:
- asdf-jjkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jjkl}
- asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        if testcoll.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="basic yaml failed")

    def test_get_yaml_noshort_name(self):
        '''Can i get a basic YAML version?'''
        testcoll = self.Collection(release_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        txt = '''asdf:
- {release_name: asdf}
- asdf-jjkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jjkl}
- asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        if testcoll.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="basic yaml failed")

    def test_get_yaml_no_name(self):
        '''Can i get a basic YAML version?'''
        testcoll = self.Collection()

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        result = False
        try:
            txt = testcoll.yaml
        except ValueError:
            result = True

        self.assertTrue(result, msg="basic yaml failed")

    def test_set_from_yaml_a(self):
        '''Can I set from some YAML?'''
        testcoll = self.Collection()

        txt = '''asdf:
- {release_name: asdf}
- asdf-jjkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jjkl}
- asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        testcoll.yaml = txt
        if testcoll.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="set from yaml failed")

    def test_set_from_yaml_b(self):
        '''Can I set from some YAML?'''
        testcoll = self.Collection()

        txt = '''asdf:
  - {release_name: asdf}
  - asdf-jjkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jjkl}
  - asdf-jkl-gh.src.rpm: {arch: src, name: asdf, release: gh, version: jkl}
'''

        result = False
        testcoll.yaml = txt
        if testcoll.release_name == 'asdf':  # pragma: no cover
            if len(testcoll) == 2:
                result = True

        self.assertTrue(result, msg="set from yaml failed")

    def test_set_from_yaml_bad(self):
        '''Can I set from some YAML?'''
        testcoll = self.Collection()

        txt = '''asdf:
  packages:
  - asdf-jjkl-gh.src.rpm: {arch: src, epoch: '1', name: asdf, release: gh, version: jjkl}
  - asdf-jkl-gh.src.rpm: {arch: src, epoch: '1', name: asdf, release: gh, version: jkl}
  release_name: asdf
jkl:
  packages:
  - asdf-jjkl-gh.src.rpm: {arch: src, epoch: '1', name: asdf, release: gh, version: jjkl}
'''

        result = False
        try:
            testcoll.yaml = txt
        except ValueError:
            result = True

        self.assertTrue(result, msg="set from yaml got weird")

class CollectionJSONViewTests(CollectionModelTests):
    ''' Test the JSON View for sanity '''
    Collection = CollectionJ

    def test_get_json_a(self):
        '''get json'''
        testcoll = self.Collection(release_name='asdf', short_name='asdf')

        testpkg = self.simple_pkg()
        testcoll.add(testpkg)

        testpkg2 = self.simple_pkg()
        testpkg2.version = 'jjkl'
        testcoll.add(testpkg2)

        expected = '{"asdf": [{"release_name": "asdf"}, {"asdf-jjkl-gh.src.rpm": {"release": "gh", "version": "jjkl", "arch": "src", "name": "asdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}'
        result = False
        if testcoll.json == expected:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Can't get JSON")

    def test_set_json_a(self):
        '''set json'''
        testcoll = self.Collection()

        testcoll.json = '{"asdf": [{"release_name": "asdf"}, {"asdf-jjkl-gh.src.rpm": {"release": "gh", "version": "jjkl", "arch": "src", "name": "asdf"}}, {"asdf-jkl-gh.src.rpm": {"release": "gh", "version": "jkl", "arch": "src", "name": "asdf"}}]}'
        result = False
        if len(testcoll) == 2:  # pragma: no cover
            if testcoll['asdf-jkl-gh.src.rpm'].name == 'asdf':
                if testcoll['asdf-jjkl-gh.src.rpm'].arch == 'src':
                    if testcoll.release_name == 'asdf':
                        if testcoll.short_name == 'asdf':
                            result = True

        self.assertTrue(result, msg="Can't set from JSON")


class CollectionTests(CollectionEventsTests, CollectionXMLViewTests, CollectionYAMLViewTests, CollectionJSONViewTests):
    '''
        Test the default object for sanity
    '''
    Collection = UpdateinfoCollection

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.Collection.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

