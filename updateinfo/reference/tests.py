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

from .models import ReferenceModel
from .events import ReferenceEvents
from .views import ReferenceXMLView
from .views import ReferenceYAMLView
from .views import ReferenceJSONView
from . import Reference as UpdateinfoReference

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

######################
# Classes for test inheritance
######################
class ReferenceEventTest(ReferenceModel, ReferenceEvents):
    '''example inherit'''
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        '''example init'''
        ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
        ReferenceEvents.__init__(self)

class ReferenceXML(ReferenceModel, ReferenceXMLView):
    '''example inherit'''
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        '''example init'''
        ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
        ReferenceXMLView.__init__(self)

class ReferenceYAML(ReferenceModel, ReferenceYAMLView):
    '''example inherit'''
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        '''example init'''
        ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
        ReferenceYAMLView.__init__(self)

class ReferenceJ(ReferenceModel, ReferenceJSONView):
    '''example inherit'''
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        '''example init'''
        ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
        ReferenceJSONView.__init__(self)
######################

class ReferenceModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    Reference = ReferenceModel

    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.Reference()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_def_at_constructor(self):
        ''' Can I define the ref at the constructor?  '''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        result = False
        if testref.reftype == 'bugzilla':  # pragma: no cover
            if testref.href == 'http://':
                if testref.refid == '1':
                    if testref.title == 'Asdf':
                        result = True
        self.assertTrue(result, msg='Failed to define self.Reference() at __init__')

    def test_undef_is_false(self):
        ''' Is an entry with no attribs False?  It should be!  '''
        testref = self.Reference()
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='undef self.Reference() is True, should be False')

    def test_by_hand_def_is_true(self):
        ''' Is an entry with all attribs True? It should be '''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='def self.Reference() is False, should be True')

    def test_minimum_def_by_hand_is_true(self):
        ''' Is an entry with minimum attribs True? It should be '''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='min def self.Reference() is False, should be True')

    def test_minimum_def_by_init_is_true(self):
        ''' Is an entry with minimum attribs True? It should be '''
        testref = self.Reference(reftype='bugzilla', href='http://')
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='min def self.Reference() is False, should be True')

    def test_undef_if_no_url(self):
        ''' Is an entry without a url False? It should be '''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='no url is undef self.Reference(), got True')

    def test_undef_if_url_empty(self):
        ''' Is an entry without a url False? It should be '''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = ''
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='no url is undef self.Reference(), got True')

    def test_undef_if_no_type(self):
        ''' Is an entry without a url False? It should be '''
        testref = self.Reference()
        testref.href = 'http://'
        result = False
        if testref:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='no type is undef self.Reference(), got True')

    def test_raise_if_bad_type_on_init(self):
        ''' Is an entry with a bad type and exception? It should be '''
        result = False
        try:  # pragma: no cover
            testref = self.Reference(reftype='bad')
        except ValueError:
            result = True

        self.assertTrue(result, msg='Bad type does not raise exception')

    def test_raise_if_bad_type_on_by_hand(self):
        ''' Is an entry with a bad type and exception? It should be '''
        result = False
        try:
            testref = self.Reference()
            testref.reftype = 'bad'
            if testref:  # pragma: no cover
                result = False
        except ValueError:
            result = True

        self.assertTrue(result, msg='Bad type does not raise exception')

    def test_property_get_href(self):
        ''' Can I get the href property'''
        testref = self.Reference(href='http://')
        result = False
        if testref.href == 'http://':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not fetch href property')

    def test_property_set_href(self):
        ''' Can I set the href property'''
        testref = self.Reference(href='http://')
        testref.href = 'newvalue'
        result = False
        if testref.href == 'newvalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set href property')

    def test_property_get_refid(self):
        ''' Can I get the refid property'''
        testref = self.Reference(refid='1')
        result = False
        if testref.refid == '1':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not fetch refid property')

    def test_property_set_refid(self):
        ''' Can I set the refid property'''
        testref = self.Reference(refid='1')
        testref.refid = 'newvalue'
        result = False
        if testref.refid == 'newvalue':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set refid property')

    def test_property_get_title_init_sets_case(self):
        ''' Can I get the title property'''
        testref = self.Reference(title='asdf')
        result = False
        if testref.title == 'Asdf':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not fetch title property')

    def test_property_set_title(self):
        ''' Can I set the title property'''
        testref = self.Reference(title='asdf')
        testref.title = 'newvalue'
        result = False
        if testref.title.title() == 'newvalue'.title():  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set title property')

    def test_property_set_title_check_case(self):
        ''' Can I set the title property'''
        testref = self.Reference(title='asdf')
        testref.title = 'newvalue'
        result = False
        if testref.title == 'newvalue':  # pragma: no cover
            result = False
        elif testref.title == 'newvalue'.title():  # pragma: no cover
            result = True
        self.assertTrue(result, msg='ref title case not set correctly')

    def test_property_get_reftype(self):
        ''' Can I get the reftype property'''
        testref = self.Reference(reftype='bugzilla')
        result = False
        if testref.reftype == 'bugzilla':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not fetch reftype property')

    def test_property_set_reftype_self(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'self'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_bugzilla(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'bugzilla'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_cve(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'cve'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_fate(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'fate'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_commit(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'commit'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_trac(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'trac'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_other(self):
        ''' Can I set the reftype property'''
        testref = self.Reference(href='http://')
        testref.reftype = 'other'
        result = False
        if testref.reftype:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_case(self):
        ''' Can I set the reftype property'''
        testref = self.Reference()
        testref.reftype = 'SELF'
        result = False
        if testref.reftype == 'self':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Could not set reftype property')

    def test_property_set_reftype_badly(self):
        ''' Can I set the reftype property'''
        testref = self.Reference()
        result = False
        try:
            testref.reftype = 'bad'
        except ValueError:
            result = True
        self.assertTrue(result, msg='Could set reftype property badly')

    def test_eq_is_eq(self):
        '''Does eq work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        result = False
        if testref == testotherref:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Two equal refs were not equal')

    def test_eq_is_not_eq_refid(self):
        '''Does eq work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='http://', refid='2', title='asdf')
        result = True
        if testref == testotherref:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='Two not equal refs were equal')

    def test_eq_is_not_eq_title(self):
        '''Does eq work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='bdbdbdb')
        result = True
        if testref == testotherref:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='Two not equal refs were equal')

    def test_eq_is_not_eq_href(self):
        '''Does eq work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='https://', refid='1', title='asdf')
        result = True
        if testref == testotherref:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='Two not equal refs were equal')

    def test_eq_is_not_eq_type(self):
        '''Does eq work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='self', href='http://', refid='1', title='asdf')
        result = True
        if testref == testotherref:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='Two not equal refs were equal')

    def test_eq_is_not_valid(self):
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        weirdthing = 'asdfasdfasdf'
        result = False
        try:
            if testref == weirdthing:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg='I can compare weird stuff')

    def test_ne_is_not_eq(self):
        '''Does ne work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        result = True
        if testref != testotherref:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='Two equal refs were not equal')

    def test_ne_eq_is_not_not_eq(self):
        '''Does ne work as expected'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testotherref = self.Reference(reftype='bugzilla', href='http://', refid='2', title='asdf')
        result = False
        if testref != testotherref:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Two not equal refs were equal')

    def test_ne_is_not_valid(self):
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        weirdthing = 'asdfasdfasdf'
        result = False
        try:
            if testref != weirdthing:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg='I can compare weird stuff')

class ReferenceEventsTests(ReferenceModelTests):
    ''' Test the Events out '''
    Reference = ReferenceEventTest

class ReferenceXMLViewTests(ReferenceModelTests):
    ''' Test the XML interface for sanity '''
    Reference = ReferenceXML

    def test_as_str(self):
        '''is the str version an xml string?'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        result = False
        if str(testref) == '<reference href="http://" id="1" title="Asdf" type="bugzilla" />':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get reference as str')

    def test_get_xml(self):
        '''Can I get the object as XML?'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        result = False
        if testref.xml == '<reference href="http://" id="1" title="Asdf" type="bugzilla" />':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get reference xml')

    def test_get_xml_min(self):
        '''Can I get the object as XML?'''
        testref = self.Reference(reftype='bugzilla', href='http://')
        result = False
        if testref.xml == '<reference href="http://" type="bugzilla" />':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get reference xml')

    def test_set_xml(self):
        '''Can I set the object from XML?'''
        testref = self.Reference()
        testref.xml = '<reference href="http://" id="1" title="Asdf" type="bugzilla" />'
        result = False
        if testref.refid == '1':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to set reference from xml')

    def test_set_xml_min_true(self):
        '''Can I set the object from XML?'''
        testref = self.Reference()
        testref.xml = '<reference href="http://" type="bugzilla" />'
        result = False
        if testref.reftype == 'bugzilla':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to set reference from xml')

    def test_get_xmlobj(self):
        '''Can I get the object as XMLEtree?'''
        testref = self.Reference(reftype='bugzilla', href='http://', refid='1', title='asdf')
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'
        result = False
        if testref.xmletree.tag == 'reference':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get reference xmlobj')

    def test_get_xmlobj_is_element(self):
        '''Can I get the object as XMLEtree?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'
        result = False
        if xmletree.iselement(testref.xmletree):  # pragma: no cover
            result = True

        self.assertTrue(result, msg='Failed to get reference xmlobj element')

    def test_set_xmlobj(self):
        '''Can I set the object from XMLEtree?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'
        testref2 = self.Reference()

        testref2.xmletree = testref.xmletree

        result = False
        if testref2.refid == '1':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to set reference from xmlobj')

    def test_set_xmlobj_bad_tag(self):
        '''Can I set the object from XMLEtree?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'
        testref2 = self.Reference()

        xmltree = testref.xmletree
        xmltree.tag = 'asdf'

        result = False
        try:
            testref2.xmletree = xmltree
        except ValueError:
            result = True

        self.assertTrue(result, msg='can set ref from bad xmlobj')

class ReferenceYAMLViewTests(ReferenceModelTests):
    ''' Test the YAML interface for sanity '''
    Reference = ReferenceYAML

    def test_get_yaml_a(self):
        '''Does basic yaml text come back?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'

        txt = '''http://: {refid: '1', title: Asdf, type: bugzilla}
'''
        result = False
        if testref.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="text isn't right")

    def test_get_yaml_b(self):
        '''Does basic yaml text come back?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.title = 'asdf'

        txt = '''http://: {title: Asdf, type: bugzilla}
'''
        result = False
        if testref.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="text isn't right")

    def test_get_yaml_c(self):
        '''Does basic yaml text come back?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'

        txt = '''http://: {type: bugzilla}
'''
        result = False
        if testref.yaml == txt:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="text isn't right")

    def test_set_from_yaml_a(self):
        '''Can I set from some YAML?'''
        testref = self.Reference()

        txt = "http://: {refid: '1', title: Asdf, type: bugzilla}"

        testref.yaml = txt
        result = False
        if testref.href == "http://":  # pragma: no cover
            if testref.refid == "1":
                if testref.title == "Asdf":
                    if testref.reftype == "bugzilla":
                        result = True
        self.assertTrue(result, msg="set from YAML didn't work")

    def test_set_from_yaml_b(self):
        '''Can I set from some YAML?'''
        testref = self.Reference()

        txt = "http://: {refid: '1', type: bugzilla}"

        testref.yaml = txt
        result = False
        if testref.href == "http://":  # pragma: no cover
            if testref.refid == "1":
                if testref.title == None:
                    if testref.reftype == "bugzilla":
                        result = True
        self.assertTrue(result, msg="set from YAML didn't work")

    def test_set_from_yaml_c(self):
        '''Can I set from some YAML?'''
        testref = self.Reference()

        txt = "http://: {type: bugzilla}"

        testref.yaml = txt
        result = False
        if testref.href == "http://":  # pragma: no cover
            if testref.refid == None:
                if testref.title == None:
                    if testref.reftype == "bugzilla":
                        result = True
        self.assertTrue(result, msg="set from YAML didn't work")


    def test_cant_set_from_bad(self):
        '''Can I set from some YAML?'''
        testref = self.Reference()

        txt = """http://: {refid: '1', type: bugzilla}
https://sdf: {refid: '2'}"""

        result = False
        try:
            testref.yaml = txt
        except ValueError:
            result = True
        self.assertTrue(result, msg="set from YAML takes weird stuff")

class ReferenceJSONViewTests(ReferenceModelTests):
    ''' Test the JSON interface for sanity '''
    Reference = ReferenceJ

    def test_get_json_a(self):
        '''Can I get some JSON?'''
        testref = self.Reference()
        testref.reftype = 'bugzilla'
        testref.href = 'http://'
        testref.refid = '1'
        testref.title = 'asdf'

        expected = '{"http://": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}'
        result = False
        if testref.json == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Can't get JSON")

    def test_set_json_a(self):
        '''Can I set from some JSON?'''
        testref = self.Reference()

        testref.json = '{"http://": {"type": "bugzilla", "refid": "1", "title": "Asdf"}}'
        result = False
        if testref.reftype == 'bugzilla':  # pragma: no cover
            if testref.href == 'http://':
                if testref.refid == '1':
                    if testref.title == 'Asdf':
                        result = True
        self.assertTrue(result, msg="Can't set from JSON")

class ReferenceTests(ReferenceEventsTests, ReferenceXMLViewTests, ReferenceYAMLViewTests, ReferenceJSONViewTests):
    ''' Test the default imported ReferenceObject '''
    Reference = UpdateinfoReference

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.Reference.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

