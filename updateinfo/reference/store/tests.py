#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the Reference class!
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

from .events import ReferenceStoreEvents
from .models import ReferenceStoreModel
from .views import ReferenceStoreXMLView
from .views import ReferenceStoreYAMLView
from .views import ReferenceStoreJSONView
from . import ReferenceStore as UpdateinfoReferenceStore
from .. import Reference

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

######################
# Classes for test inheritance
######################
class ReferenceStoreE(ReferenceStoreModel, ReferenceStoreEvents):
    '''example inherit'''
    def __init__(self):
        '''example init'''
        ReferenceStoreModel.__init__(self)
        ReferenceStoreEvents.__init__(self)

class ReferenceStoreX(ReferenceStoreModel, ReferenceStoreEvents, ReferenceStoreXMLView):
    '''example inherit'''
    def __init__(self):
        '''example init'''
        ReferenceStoreModel.__init__(self)
        ReferenceStoreEvents.__init__(self)
        ReferenceStoreXMLView.__init__(self)

class ReferenceStoreY(ReferenceStoreModel, ReferenceStoreEvents, ReferenceStoreYAMLView):
    '''example inherit'''
    def __init__(self):
        '''example init'''
        ReferenceStoreModel.__init__(self)
        ReferenceStoreEvents.__init__(self)
        ReferenceStoreYAMLView.__init__(self)

class ReferenceStoreJ(ReferenceStoreModel, ReferenceStoreEvents, ReferenceStoreJSONView):
    '''example inherit'''
    def __init__(self):
        '''example init'''
        ReferenceStoreModel.__init__(self)
        ReferenceStoreEvents.__init__(self)
        ReferenceStoreJSONView.__init__(self)
######################

class ReferenceStoreModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    ReferenceStore = ReferenceStoreModel
    Reference = Reference

    @staticmethod
    def simpleadd(store, ref):
        '''lame quick and dirty add operation'''
        store._reflist[ref.href] = ref

    def test_reference(self):
        '''Make sure we are testing the right one'''
        result = False
        if str(type(self.Reference())) == "<class 'updateinfo.reference.Reference'>":    # pragma: no cover
            result = True
        self.assertTrue(result, msg='Wrong Object')

    def test_def_at_constructor(self):
        ''' Must I define at the constructor?  '''
        result = False
        try:
            teststore = self.ReferenceStore()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg="It seems I must define things")

    def test_bool_false(self):
        '''Am I false when I should be?'''
        teststore = self.ReferenceStore()
        self.assertFalse(teststore, msg="it seems I'm true when undef")

    def test_bool_true(self):
        '''Am I true when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        self.assertTrue(teststore, msg="it seems I'm false when def")

    def test_eq_is(self):
        '''Am I eq when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        teststore2 = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore2, testref)

        result = False
        if teststore == teststore2:    # pragma: no cover
            result = True
        self.assertTrue(result, msg="eq not working right")

    def test_eq_isnt(self):
        '''Am I eq when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        teststore2 = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asadf')
        self.simpleadd(teststore2, testref)

        result = False
        if teststore == teststore2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="eq not working right")

    def test_eq_weird(self):
        '''Am I eq when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        try:
            if teststore == testref:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg="eq not working right")

    def test_ne_is(self):
        '''Am I ne when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        teststore2 = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore2, testref)

        self.assertFalse((teststore != teststore2), msg="ne not working right")

    def test_ne_isnt(self):
        '''Am I ne when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        teststore2 = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asadf')
        self.simpleadd(teststore2, testref)

        self.assertTrue((teststore != teststore2), msg="eq not working right")

    def test_ne_weird(self):
        '''Am I ne when I should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        try:
            if teststore != testref:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg="ne not working right")

    def test_len_zero(self):
        '''Is my len zero when it should be?'''
        teststore = self.ReferenceStore()

        result = False
        if len(teststore) == 0:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my len is messed up")

    def test_len_one(self):
        '''Is my len zero when it should be?'''
        teststore = self.ReferenceStore()

        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if len(teststore) == 1:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my len is messed up")

    def test_as_dict_keyerror(self):
        '''When looking for bad keys, do I raise key error?'''
        teststore = self.ReferenceStore()

        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        try:
            thing = teststore['nourl']
        except KeyError:
            result = True

        self.assertTrue(result, msg="it seems my __getitem__ is messed up")

    def test_as_dict_ok(self):
        '''When looking by key, do I work?'''
        teststore = self.ReferenceStore()

        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        self.assertTrue(teststore['http://'], msg="it seems my __getitem__ is messed up")

    def test_contains_by_ref_ok(self):
        '''Is it 'in' as it should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if testref.href in teststore:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my __contains__ is messed up")

    def test_contains_by_obj_ok(self):
        '''Is it 'in' as it should be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if testref in teststore:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my __contains__ is messed up")

    def test_contains_by_ref_notok(self):
        '''Is it 'in' as it shouldn't be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if 'http:///' not in teststore:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my __contains__ is messed up")

    def test_contains_by_obj_notok(self):
        '''Is it 'in' as it shouldn't be?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='bugzilla', href='http:///', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if testref2 not in teststore:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my __contains__ is messed up")

    def test_iter(self):
        '''does iter work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        found = []
        for ref in teststore:
            found.append(ref)

        if found == ['http://']:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems my __iter__ is messed up")

    def test_urls(self):
        '''does the urls property show the urls?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if teststore.urls == ('http://',):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems urls doesn't work")

    def test_urls_ro(self):
        '''The URLS are a readonly set, make sure'''
        teststore = self.ReferenceStore()
        result = False
        try:
            teststore.urls = ('http://',)
        except NotImplementedError:
            result = True

        self.assertTrue(result, msg="it seems urls is read-write")

    def test_urls_sorted(self):
        '''does the urls property show the urls sorted correctly?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='bugzilla', href='aahttp://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)
        self.simpleadd(teststore, testref2)

        result = False
        if teststore.urls == ('aahttp://', 'http://'):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems urls isn't sorted")

    def test_reftypes(self):
        '''does the reftypes property work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)

        result = False
        if teststore.reftypes == ('bugzilla',):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems reftypes doesn't work")

    def test_reftypes_ro(self):
        '''The URLS are a readonly set, make sure'''
        teststore = self.ReferenceStore()
        result = False
        try:
            teststore.reftypes = ('bugzilla',)
        except NotImplementedError:
            result = True

        self.assertTrue(result, msg="it seems reftypes is read-write")

    def test_reftypes_dedupe(self):
        '''does the reftypes property work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='bugzilla', href='aahttp://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)
        self.simpleadd(teststore, testref2)

        result = False
        if teststore.reftypes == ('bugzilla',):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems reftypes doesn't dedupe")

    def test_reftypes_sorted(self):
        '''does the reftypes property work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='aahttp://', refid='1', title='asdf')
        self.simpleadd(teststore, testref)
        self.simpleadd(teststore, testref2)

        result = False
        if teststore.reftypes == ('bugzilla', 'self'):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems reftypes isn't sorted")

    def test_has_byreftype_prop(self):
        '''basically this should always pass, we check the struct in events'''
        teststore = self.ReferenceStore()

        result = False
        if teststore.byreftype == {}:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems byreftype isn't a property")

    def test_byreftype_ro(self):
        '''make sure this is ro'''
        teststore = self.ReferenceStore()

        result = False
        try:
            teststore.byreftype = ()
        except NotImplementedError:
            result = True

        self.assertTrue(result, msg="it seems byreftype is read-write")

class ReferenceStoreEventTests(ReferenceStoreModelTests):
    ''' Test the Events for sanity '''
    ReferenceStore = ReferenceStoreE

    def test_add(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')

        result = False
        teststore.add(testref)
        if len(teststore) == 1:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems add doesn't work")

    def test_add_xmlobj(self):
        '''Does add xmlobj work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')

        result = False
        teststore.add(testref.xmletree)
        if len(teststore) == 1:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems add doesn't work")

    def test_add_duplicate(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')

        result = False
        teststore.add(testref)
        teststore.add(testref2)
        if len(teststore) == 1:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems adding duplicates duplicates")

    def test_add_duplicate_min(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(href='http://', reftype='self')

        result = False
        teststore.add(testref)
        teststore.add(testref2)
        if len(teststore) == 1:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems adding duplicates duplicates")

    def test_add_duplicate_merge_fails(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')

        result = False
        teststore.add(testref)
        try:
            teststore.add(testref2, merge=False)
        except ValueError:
            result = True

        self.assertTrue(result, msg="it seems trying to merge when disabled fails")

    def test_add_duplicate_merge(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='http://', refid='1', title='asdf')

        result = False
        teststore.add(testref)
        teststore.add(testref2)
        if teststore['http://'].reftype == 'self':    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems trying to merge fails")

    def test_add_duplicate_merge_everything(self):
        '''Does add work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='http://', refid='2', title='What')

        result = False
        teststore.add(testref)
        teststore.add(testref2)
        if teststore['http://'].reftype == 'self':    # pragma: no cover
            if teststore['http://'].refid == '2':
                if teststore['http://'].title == 'What':
                    result = True

        self.assertTrue(result, msg="it seems trying to merge fails")

    def test_add_fails(self):
        '''Does add fail when it should?'''
        teststore = self.ReferenceStore()

        result = False
        try:
            teststore.add(None)
        except TypeError:
            result = True

        self.assertTrue(result, msg="it seems add is too friendly")

    def test_add_fails_also(self):
        '''Does add fail when it should?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', refid='1', title='asdf')

        result = False
        try:
            teststore.add(testref)
        except ValueError:
            result = True

        self.assertTrue(result, msg="it seems add is too friendly")

    def test_add_fails_as_well(self):
        '''Does add fail when it should?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(href='http://', refid='1', title='asdf')

        result = False
        try:
            teststore.add(testref)
        except ValueError:
            result = True

        self.assertTrue(result, msg="it seems add is too friendly")

    def test_new_can(self):
        '''Does create() make a new reference'''
        teststore = self.ReferenceStore()

        teststore.create(reftype='self', href='http://', refid='1', title='asdf')
        result = False
        if teststore['http://'].reftype == 'self':    # pragma: no cover
            result = True

        self.assertTrue(result, msg="it seems new doesnt work")

    def test_new_cannot(self):
        '''Does create() make a new reference'''
        teststore = self.ReferenceStore()

        result = False
        try:
            teststore.create()
        except ValueError:
            result = True

        self.assertTrue(result, msg="it seems new is too friendly")

    def test_byreftype(self):
        '''Does byreftype have the structure we want?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='https://', refid='1', title='asdf')
        teststore.add(testref)
        teststore.add(testref2)

        result = False
        if teststore.byreftype.keys() == ['bugzilla', 'self']:    # pragma: no cover
            if len(teststore.byreftype['bugzilla']) == 1:
                if len(teststore.byreftype['self']) == 1:
                    result = True

        self.assertTrue(result, msg="byreftype struct bad")

    def test_setitem_fails(self):
        '''set like a dict makes little sense here'''
        teststore = self.ReferenceStore()

        result = False
        try:
            teststore['asdf'] = 'asdf'
        except TypeError:
            result = True

        self.assertTrue(result, msg="I set like a dict poorly?")

    def test_setitem_works(self):
        '''set like a dict makes little sense here'''
        teststore = self.ReferenceStore()

        result = False
        teststore['http://'] = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        if 'http://' in teststore:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I dont set like a dict?")

    def test_setitem_bad_url(self):
        '''set like a dict makes little sense here'''
        teststore = self.ReferenceStore()

        result = False
        try:
            teststore['https://'] = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        except ValueError:
            result = True

        self.assertTrue(result, msg="I set like a dict with bad urls?")

    def test_remove_can_byurl(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        teststore.remove(testref.href)
        if len(teststore) == 0:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't remove()")

    def test_remove_can_byurl_str(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        teststore.remove(str(testref.href))
        if len(teststore) == 0:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't remove()")

    def test_remove_can_byobj(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        teststore.remove(testref)
        if len(teststore) == 0:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't remove()")

    def test_remove_cannot(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        try:
            teststore.remove(0)
        except ValueError:
            result = True

        self.assertTrue(result, msg="remove() accepts weird things")

    def test_remove_like_dict(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        del teststore[testref.href]
        if len(teststore) == 0:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't remove()")

    def test_bad_remove_like_dict(self):
        '''Make sure remove works'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        try:
            del teststore['asdfasdf']
        except KeyError:
            result = True

        self.assertTrue(result, msg="I got weird stuff out of del?")

class ReferenceStoreXMLViewTests(ReferenceStoreModelTests):
    ''' Test the Events for sanity '''
    ReferenceStore = ReferenceStoreX

    def test_as_str(self):
        '''does pprint work?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        pprint = '''<references>
  <reference href="http://" id="1" title="Asdf" type="bugzilla" />
</references>
'''
        result = False
        if str(teststore) == pprint:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't pprint")

    def test_get_xmlobj(self):
        '''Do I get a rational XML obj?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        if teststore.xmletree.tag == 'references':    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I got a weird xml obj?")

    def test_get_xmlobj_is_element(self):
        '''Do I get a rational XML obj?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        if xmletree.iselement(teststore.xmletree):    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I got a weird not xml element obj?")

    def test_set_xmlobj(self):
        '''Do can I set from XML obj?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        teststore2 = self.ReferenceStore()

        teststore2.xmletree = teststore.xmletree

        result = False
        if teststore2.xmletree.tag == 'references':    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I cant set from xmlobj?")

    def test_set_bad_xmlobj(self):
        '''Do I check for rational xmlobj?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        teststore2 = self.ReferenceStore()

        xmltree = teststore.xmletree
        xmltree.tag = 'asdf'
        result = False

        try:
            teststore2.xmletree = xmltree
        except ValueError:
            result = True

        self.assertTrue(result, msg="I can set from a weird xmlobj?")

    def test_get_xml(self):
        '''Do I get a rational XML?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        result = False
        if teststore.xml == '<references><reference href="http://" id="1" title="Asdf" type="bugzilla" /></references>':    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I got a weird xml obj?")

    def test_set_xml(self):
        '''Do can I set from XML obj?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        teststore2 = self.ReferenceStore()

        teststore2.xml = teststore.xml

        result = False
        if teststore2.xmletree.tag == 'references':
            result = True

        self.assertTrue(result, msg="I cant set from xmlobj?")

class ReferenceStoreYAMLViewTests(ReferenceStoreModelTests):
    ''' Test the Events for sanity '''
    ReferenceStore = ReferenceStoreY

    def test_get_yaml_a(self):
        '''Do i get good YAML?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        teststore.add(testref)

        txt = '''references:
- http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        if teststore.yaml == txt:    # pragma: no cover
            result = True
        self.assertTrue(result, msg="I couldn't get yaml?")

    def test_get_yaml_b(self):
        '''Do i get good YAML?'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='aahttp://', refid='1', title='asdf')
        teststore.add(testref)
        teststore.add(testref2)

        txt = '''references:
- aahttp://: {refid: '1', title: Asdf, type: self}
- http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        if teststore.yaml == txt:    # pragma: no cover
            result = True
        self.assertTrue(result, msg="I couldn't get yaml?")

    def test_set_yaml_a(self):
        '''Can I set this from YAML?'''
        teststore = self.ReferenceStore()

        txt = '''references:
- aahttp://: {refid: '1', title: Asdf, type: self}
- http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        teststore.yaml = txt
        if len(teststore) == 2:    # pragma: no cover
            if teststore.yaml == txt:
                result = True
        self.assertTrue(result, msg="I couldn't set from yaml?")

    def test_set_yaml_bad(self):
        '''Can I set this from YAML?'''
        teststore = self.ReferenceStore()

        txt = '''aahttp://: {refid: '1', title: Asdf, type: self}
http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        try:
            teststore.yaml = txt
        except ValueError:
            result = True

        self.assertTrue(result, msg="I can set weird things")

    def test_set_yaml_bad_b(self):
        '''Can I set this from YAML?'''
        teststore = self.ReferenceStore()

        txt = '''refere:
- aahttp://: {refid: '1', title: Asdf, type: self}
- http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        try:
            teststore.yaml = txt
        except ValueError:
            result = True

        self.assertTrue(result, msg="I can set weird things")

class ReferenceStoreJSONTests(ReferenceStoreModelTests):
    ''' Test the JSON view for sanity '''
    ReferenceStore = ReferenceStoreJ

    def test_get_json_a(self):
        '''Get some JSON'''
        teststore = self.ReferenceStore()
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref2 = self.Reference(reftype='self', href='aahttp://', refid='1', title='asdf')

        teststore.add(testref)
        teststore.add(testref2)

        expected = '{"references": [{"aahttp://": {"type": "self", "refid": "1", "title": "Asdf"}}, {"http://": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}]}'
        result = False
        if teststore.json == expected:    # pragma: no cover
            result = True

        self.assertTrue(result, msg="I can't get JSON")

    def test_set_json_a(self):
        '''Set from JSON'''
        teststore = self.ReferenceStore()

        teststore.json = '{"references": [{"aahttp://": {"type": "self", "refid": "1", "title": "Asdf"}}, {"http://": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}]}'
        result = False
        if len(teststore) == 2:    # pragma: no cover
            if teststore['http://'].refid == '1':
                if teststore['aahttp://'].reftype == 'self':
                    result = True

        self.assertTrue(result, msg="I can't set from JSON")


class ReferenceStoreTests(ReferenceStoreEventTests, ReferenceStoreXMLViewTests, ReferenceStoreYAMLViewTests, ReferenceStoreJSONTests):
    '''Test the default object'''
    ReferenceStore = UpdateinfoReferenceStore

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.ReferenceStore.__version__):    # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")
