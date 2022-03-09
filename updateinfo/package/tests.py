#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the Package class!
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
import hashlib
import os
import subprocess
import unittest

from distutils.version import StrictVersion

from .events import PackageEvents
from .models import PackageModel
from .views import PackageXMLView
from .views import PackageYAMLView
from .views import PackageJSONView
from . import Package as UpdateinfoPackage

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

# for the YAMLView
from yaml import safe_load

######################
# Classes for test inheritance
######################
class PackageE(PackageModel, PackageEvents):
    '''example inherit'''
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        '''example init'''
        PackageModel.__init__(self)
        PackageEvents.__init__(self, localfilename, src_repo_base, defaultsum)

class PackageXML(PackageModel, PackageEvents, PackageXMLView):
    '''example inherit'''
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        '''example init'''
        PackageModel.__init__(self)
        PackageEvents.__init__(self, localfilename, src_repo_base, defaultsum)
        PackageXMLView.__init__(self)

class PackageYAML(PackageModel, PackageEvents, PackageYAMLView):
    '''example inherit'''
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        '''example init'''
        PackageModel.__init__(self)
        PackageEvents.__init__(self, localfilename, src_repo_base, defaultsum)
        PackageYAMLView.__init__(self)

class PackageJ(PackageModel, PackageEvents, PackageJSONView):
    '''example inherit'''
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        '''example init'''
        PackageModel.__init__(self)
        PackageEvents.__init__(self, localfilename, src_repo_base, defaultsum)
        PackageJSONView.__init__(self)
######################

class PackageModelTests(unittest.TestCase):
    ''' Test the Model for sanity '''
    Package = PackageModel

    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.Package()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_if_ndef(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with no attribs I am True')

    def test_if_partial_ndef_name(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_version(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.version = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_name_version(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_release(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.release = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_name_release(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.release = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_name_version_release(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'asdf'
        testpkg.release = 'asdf'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_arch(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.arch = 'noarch'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_name_arch(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.arch = 'noarch'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_if_partial_ndef_name_version_arch(self):
        '''If not defined, am I true?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'asdf'
        testpkg.arch = 'noarch'
        result = False
        if testpkg:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Seems with not enough attribs I am True')

    def test_eq(self):
        '''is eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='eq should be eq, is not')

    def test_eq_none(self):
        ''' Should not be equal to None'''

        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = True

        if testpkg == None:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='eq should not be eq, is')

    def test_eq_empty(self):
        ''' Should not be equal to empty'''

        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = True

        if testpkg == '':  # pragma: no cover
            result = False
        self.assertTrue(result, msg='eq should not be eq, is')

    def test_eq_empty_tuple(self):
        ''' Should not be equal to empty tuple'''

        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = True

        if testpkg == ():  # pragma: no cover
            result = False
        self.assertTrue(result, msg='eq should not be eq, is')

    def test_eq_empty_list(self):
        ''' Should not be equal to empty list'''

        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = True

        if testpkg == []:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='eq should not be eq, is')

    def test_eq_empty_dict(self):
        ''' Should not be equal to empty dict'''

        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = True

        if testpkg == {}:  # pragma: no cover
            result = False
        self.assertTrue(result, msg='eq should not be eq, is')

    def test_eq_not_eq_name(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'iasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_version(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jikl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_release(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gih'
        testpkg2.arch = 'src'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_arch(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'noarch'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_reboot(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'
        testpkg2.reboot_suggested = True

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_restart(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'
        testpkg2.restart_suggested = True

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_relogin(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'
        testpkg2.relogin_suggested = True

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_not_eq_epoch(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'
        testpkg2.epoch = '4'

        result = False

        if testpkg == testpkg2:  # pragma: no cover
            result = True
        self.assertFalse(result, msg='Should be not eq, is not')

    def test_eq_weird(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = False

        try:
            if testpkg == 9:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg='Should be not eq, is not')

    def test_neq(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'

        result = False

        if testpkg != testpkg2:  # pragma: no cover
            # shouldn't get here
            result = True
        self.assertFalse(result, msg='Two packages are eq, so why are the !=?')

    def test_neq_not_eq(self):
        '''is eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'iasdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()
        testpkg2.name = 'asdf'
        testpkg2.version = 'jkl'
        testpkg2.release = 'gh'
        testpkg2.arch = 'src'

        result = False

        if testpkg != testpkg2:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Should be not eq, is not')

    def test_ne_weird(self):
        '''is not eq when it should be?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = False

        try:
            if testpkg != 9:  # pragma: no cover
                pass
        except TypeError:
            result = True
        self.assertTrue(result, msg='Should be not eq, is not')

    def test_auto_filename_if_undef(self):
        '''If not defined, can I get a filename?'''
        result = True
        testpkg = self.Package()
        try:
            testvar = testpkg.filename
        except ValueError:
            result = False
        self.assertFalse(result, msg='Seems with not enough attribs I guess at a filename')

    def test_set_filename(self):
        '''can I set filename?'''
        testpkg = self.Package()
        testpkg.filename = 'asdf'
        result = False
        if testpkg.filename != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set filename")

    def test_set_clean_filename(self):
        '''can I set filename?'''
        testpkg = self.Package()
        testpkg.filename = ' asdf '
        result = False
        if testpkg.filename != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I don't clean the filename")

    def test_default_name(self):
        '''I have a default name right?'''
        testpkg = self.Package()
        result = False
        if testpkg.name != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default name is not None")
    def test_set_name(self):
        '''I have set name right?'''
        testpkg = self.Package()
        testpkg.name = 'asdf'
        result = False
        if testpkg.name != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set name")

    def test_default_epoch(self):
        '''I have a default epoch right?'''
        testpkg = self.Package()
        result = False
        if testpkg.epoch != '0':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default epoch is " + testpkg.epoch + " not 0")

    def test_set_epoch(self):
        '''I have set epoch right?'''
        testpkg = self.Package()
        testpkg.epoch = '2'
        result = False
        if testpkg.epoch != '2':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set epoch")

    def test_set_epoch_is_num(self):
        '''I have set epoch right?'''
        result = False
        testpkg = self.Package()
        try:
            testpkg.epoch = 'asdf'
        except ValueError:
            result = True
        self.assertTrue(result, msg="I can set epoch to a non-number")

    def test_set_epoch_int(self):
        '''I have set epoch right?'''
        testpkg = self.Package()
        testpkg.epoch = 2
        result = False
        if testpkg.epoch != '2':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set epoch")

    def test_set_epoch_long(self):
        '''I have set epoch right?'''
        testpkg = self.Package()
        testpkg.epoch = long(2)
        result = False
        if testpkg.epoch != '2':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set epoch")

    def test_default_version(self):
        '''I have a default version right?'''
        testpkg = self.Package()
        result = False
        if testpkg.version != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default version is not None")

    def test_set_version(self):
        '''I have set version right?'''
        testpkg = self.Package()
        testpkg.version = 'asdf'
        result = False
        if testpkg.version != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set version")

    def test_default_release(self):
        '''I have a default release right?'''
        testpkg = self.Package()
        result = False
        if testpkg.release != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default release is not None")

    def test_set_release(self):
        '''I have set release right?'''
        testpkg = self.Package()
        testpkg.release = 'asdf'
        result = False
        if testpkg.release != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set release")

    def test_default_arch(self):
        '''I have a default arch right?'''
        testpkg = self.Package()
        result = False
        if testpkg.arch != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default arch is not None")

    def test_set_arch(self):
        '''I have set arch right?'''
        testpkg = self.Package()
        testpkg.arch = 'noarch'
        result = False
        if testpkg.arch != 'noarch':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set arch")

    def test_default_srpm(self):
        '''I have a default srpm right?'''
        testpkg = self.Package()
        result = False
        if testpkg.srpm != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default srpm is not None")

    def test_set_srpm(self):
        '''I have set srpm right?'''
        testpkg = self.Package()
        testpkg.srpm = 'asdf'
        result = False
        if testpkg.srpm != 'asdf':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set srpm")

    def test_default_src_repo_base(self):
        '''I have a default src_repo_base right?'''
        testpkg = self.Package()
        result = False
        if testpkg.src_repo_base != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default src_repo_base is not None")

    def test_set_src_repo_base(self):
        '''I have set default src_repo_base right?'''
        testpkg = self.Package()
        testpkg.src_repo_base = 'asdf/'
        result = False
        if testpkg.src_repo_base != 'asdf/':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="I can't set src_repo_base")

    def test_set_src_repo_base_trailing(self):
        '''I have set default src_repo_base right?'''
        testpkg = self.Package()
        testpkg.src_repo_base = 'asdf'
        result = False
        if testpkg.src_repo_base != 'asdf/':  # pragma: no cover
            result = True
        self.assertFalse(result, msg="add trailing / failed")

    def test_default_builddate(self):
        '''I have a default builddate right?'''
        testpkg = self.Package()
        result = False
        if testpkg.builddate != None:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My default builddate is not None")

    def test_builddate_fromtimestamp(self):
        '''I have a set builddate right?'''
        testpkg = self.Package()
        timestamp = datetime.datetime.fromtimestamp(0)
        testpkg.builddate = 0
        result = False
        if testpkg.builddate != timestamp:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My builddate didn't import timestamp right")

    def test_builddate_with_timestamp(self):
        '''I have a set builddate right?'''
        testpkg = self.Package()
        timestamp = datetime.datetime.fromtimestamp(0)
        testpkg.builddate = timestamp
        result = False
        if not isinstance(testpkg.builddate, datetime.datetime):  # pragma: no cover
            result = True
        self.assertFalse(result, msg="My builddate doesn't see I'm a datetime already")

    def test_default_reboot_suggested(self):
        '''I have a default reboot right?'''
        testpkg = self.Package()
        self.assertFalse(testpkg.reboot_suggested, msg="My default state is True, should be False")

    def test_reboot_suggested_true(self):
        '''I have set default reboot right?'''
        testpkg = self.Package()
        testpkg.reboot_suggested = True
        self.assertTrue(testpkg.reboot_suggested, msg="My state is False, should be True")

    def test_reboot_suggested_false(self):
        '''I have set default reboot right?'''
        testpkg = self.Package()
        testpkg.reboot_suggested = False
        self.assertFalse(testpkg.reboot_suggested, msg="My state is True, should be False")

    def test_default_restart_suggested(self):
        '''I have a default restart right?'''
        testpkg = self.Package()
        self.assertFalse(testpkg.restart_suggested, msg="My default state is True, should be False")

    def test_restart_suggested_true(self):
        '''I have set restart right?'''
        testpkg = self.Package()
        testpkg.restart_suggested = True
        self.assertTrue(testpkg.restart_suggested, msg="My state is False, should be True")

    def test_restart_suggested_false(self):
        '''I have set restart right?'''
        testpkg = self.Package()
        testpkg.restart_suggested = False
        self.assertFalse(testpkg.restart_suggested, msg="My state is True, should be False")

    def test_default_relogin_suggested(self):
        '''I have default relogin right?'''
        testpkg = self.Package()
        self.assertFalse(testpkg.relogin_suggested, msg="My default state is True, should be False")

    def test_relogin_suggested_true(self):
        '''I have set relogin right?'''
        testpkg = self.Package()
        testpkg.relogin_suggested = True
        self.assertTrue(testpkg.relogin_suggested, msg="My state is False, should be True")

    def test_relogin_suggested_false(self):
        '''I have set relogin right?'''
        testpkg = self.Package()
        testpkg.relogin_suggested = False
        self.assertFalse(testpkg.relogin_suggested, msg="My state is True, should be False")

    def test_md5_default(self):
        '''md5'''
        testpkg = self.Package()
        result = False
        if testpkg.sums['md5']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_def(self):
        '''md5'''
        testpkg = self.Package()
        result = False
        testpkg.sums['md5'] = 'asdf'
        if testpkg.sums['md5']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_def_fromfile(self):
        '''md5'''
        testpkg = self.Package()
        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.md5(txt).hexdigest()

        result = False
        testpkg.sums['md5'] = '/etc/hosts'
        if testpkg.sums['md5'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_undef(self):
        '''md5'''
        testpkg = self.Package()
        result = False
        testpkg.sums['md5'] = 'asdf'
        del testpkg.sums['md5']
        if testpkg.sums['md5']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_as_prop_default(self):
        '''md5'''
        testpkg = self.Package()
        result = False
        if testpkg.sums.md5:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_as_prop_def(self):
        '''md5'''
        testpkg = self.Package()
        result = False
        testpkg.sums.md5 = 'asdf'
        if testpkg.sums.md5:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_as_prop_def_fromfile(self):
        '''md5'''
        testpkg = self.Package()

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.md5(txt).hexdigest()

        result = False
        testpkg.sums.md5 = '/etc/hosts'
        if testpkg.sums.md5 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")


    def test_sha_default(self):
        '''sha'''
        testpkg = self.Package()
        result = False
        if testpkg.sums['sha']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_def(self):
        '''sha'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha'] = 'asdf'
        if testpkg.sums['sha']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_def_fromfile(self):
        '''sha'''
        testpkg = self.Package()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()

        testpkg.sums['sha'] = '/etc/hosts'
        if testpkg.sums['sha'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_undef(self):
        '''sha'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha'] = 'asdf'
        del testpkg.sums['sha']
        if testpkg.sums['sha']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_as_prop_default(self):
        '''sha'''
        testpkg = self.Package()
        result = False
        if testpkg.sums.sha:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_as_prop_def(self):
        '''sha'''
        testpkg = self.Package()
        result = False
        testpkg.sums.sha = 'asdf'
        if testpkg.sums.sha:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_as_prop_def_fromfile(self):
        '''sha'''
        testpkg = self.Package()

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()

        result = False
        testpkg.sums.sha = '/etc/hosts'
        if testpkg.sums.sha == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")


    def test_sha1_default(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        if testpkg.sums['sha1']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_def(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha1'] = 'asdf'
        if testpkg.sums['sha1']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_def_fromfile(self):
        '''sha1'''
        testpkg = self.Package()
        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        result = False
        testpkg.sums['sha1'] = '/etc/hosts'
        if testpkg.sums['sha1'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_undef(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha1'] = 'asdf'
        del testpkg.sums['sha1']
        if testpkg.sums['sha1']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_as_prop_default(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        if testpkg.sums.sha1:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_as_prop_def(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        testpkg.sums.sha1 = 'asdf'
        if testpkg.sums.sha1:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_as_prop_def_fromfile(self):
        '''sha1'''
        testpkg = self.Package()
        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        result = False
        testpkg.sums.sha1 = '/etc/hosts'
        if testpkg.sums.sha1 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_is_sha(self):
        '''sha1'''
        testpkg = self.Package()
        result = False
        testpkg.sums.sha1 = '/etc/hosts'
        if testpkg.sums.sha1 == testpkg.sums.sha:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be sha")


    def test_sha256_default(self):
        '''sha256'''
        testpkg = self.Package()
        result = False
        if testpkg.sums['sha256']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_def(self):
        '''sha256'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha256'] = 'asdf'
        if testpkg.sums['sha256']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_def_fromfile(self):
        '''sha256'''
        testpkg = self.Package()
        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha256(txt).hexdigest()

        result = False
        testpkg.sums['sha256'] = '/etc/hosts'
        if testpkg.sums['sha256'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_undef(self):
        '''sha256'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha256'] = 'asdf'
        del testpkg.sums['sha256']
        if testpkg.sums['sha256']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_as_prop_default(self):
        '''sha256'''
        testpkg = self.Package()
        result = False
        if testpkg.sums.sha256:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_as_prop_def(self):
        '''sha256'''
        testpkg = self.Package()
        result = False
        testpkg.sums.sha256 = 'asdf'
        if testpkg.sums.sha256:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_as_prop_def_fromfile(self):
        '''sha256'''
        testpkg = self.Package()

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha256(txt).hexdigest()

        result = False
        testpkg.sums.sha256 = '/etc/hosts'
        if testpkg.sums.sha256 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")


    def test_sha512_default(self):
        '''sha512'''
        testpkg = self.Package()
        result = False
        if testpkg.sums['sha512']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_def(self):
        '''sha512'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha512'] = 'asdf'
        if testpkg.sums['sha512']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_def_fromfile(self):
        '''sha512'''
        testpkg = self.Package()

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha512(txt).hexdigest()

        result = False
        testpkg.sums['sha512'] = '/etc/hosts'
        if testpkg.sums['sha512'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_undef(self):
        '''sha512'''
        testpkg = self.Package()
        result = False
        testpkg.sums['sha512'] = 'asdf'
        del testpkg.sums['sha512']
        if testpkg.sums['sha512']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_as_prop_default(self):
        '''sha512'''
        testpkg = self.Package()
        result = False
        if testpkg.sums.sha512:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_as_prop_def(self):
        '''sha512'''
        testpkg = self.Package()
        result = False
        testpkg.sums.sha512 = 'asdf'
        if testpkg.sums.sha512:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_as_prop_def_fromfile(self):
        '''sha512'''
        testpkg = self.Package()

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha512(txt).hexdigest()

        result = False
        testpkg.sums.sha512 = '/etc/hosts'
        if testpkg.sums.sha512 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")


    def test_sum_bad_sumtype(self):
        '''bad sum is error'''
        testpkg = self.Package()
        result = True
        try:
            testpkg.sums['asdf'] = '/etc/hosts'
        except KeyError:
            result = False
        self.assertFalse(result, msg="Can define bad SUM")

    def test_sum_bool(self):
        '''test bool'''
        testpkg = self.Package()
        testpkg.sums['md5'] = '/etc/hosts'
        self.assertTrue(testpkg.sums, msg="Have sum defined, but False")

    def test_multiple_sums(self):
        '''test bool'''
        testpkg = self.Package()
        testpkg.sums['md5'] = '/etc/hosts'
        testpkg.sums['sha'] = '/etc/hosts'
        testpkg.sums['sha256'] = '/etc/hosts'
        self.assertTrue(True, msg="Can't Attach multiple sums")

    def test_sum_keys(self):
        '''test keys'''
        testpkg = self.Package()
        testpkg.sums['md5'] = '/etc/hosts'
        testpkg.sums['sha'] = '/etc/hosts'
        testpkg.sums['sha256'] = '/etc/hosts'
        if not testpkg.sums.keys() == ('md5', 'sha', 'sha256'):  # pragma: no cover
            self.assertTrue(False, msg="Defined sums not provided")

    def test_sum_iter(self):
        '''test iter'''
        testpkg = self.Package()
        testpkg.sums['md5'] = '/etc/hosts'
        testpkg.sums['sha'] = '/etc/hosts'
        testpkg.sums['sha256'] = '/etc/hosts'
        have = []
        result = ['md5', 'sha', 'sha256']
        for tsum in testpkg.sums:
            have.append(tsum)
        if have != result:  # pragma: no cover
            self.assertTrue(False, msg="sums iter not working")

class PackageEventsTests(PackageModelTests):
    '''Test Events work as expected'''
    Package = PackageE

    def test_constructor_args_src_repo(self):
        '''args'''
        result = False
        testpkg = self.Package(src_repo_base='test/')
        if testpkg.src_repo_base == 'test/':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Could not setup " + testpkg.__module__ + " with src_repo arg")

    def test_constructor_args_defsum(self):
        '''args'''
        testpkg = self.Package(defaultsum='md5')
        result = False
        if testpkg._default_sum == 'md5':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Could not setup " + testpkg.__module__ + " with defaultsum arg")

    def test_constructor_args_localfile_no_file_exists(self):
        '''args'''
        result = False
        try:
            testpkg = self.Package(localfilename='/tmp/filenotfound')
        except IOError:
            result = True
        self.assertTrue(result, msg="Did not try to open file for setup")

    def test_constructor_args_localfile_file_exists_has_arch(self):
        '''args'''
        result = False
        if os.path.isfile('./docs/samples/sample.spec'):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                testpkg = self.Package(localfilename='/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm')
                os.remove('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm')
            elif os.path.isfile('/tmp/RPMS/sample-1-1.1.noarch.rpm'):
                testpkg = self.Package(localfilename='/tmp/RPMS/sample-1-1.1.noarch.rpm')
                os.remove('/tmp/RPMS/sample-1-1.1.noarch.rpm')
            else:  # pragma: no cover
                if hasattr(unittest, 'SkipTest'):
                    raise unittest.SkipTest('Could not build sample spec')
                else:
                    return True

            if testpkg.name == 'sample':  # pragma: no cover
                if testpkg.epoch == '0':
                    if testpkg.version == '1':
                        if testpkg.release == '1.1':
                            if testpkg.arch == 'noarch':
                                result = True
        else:  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find sample spec')
            else:
                return True

        self.assertTrue(result, msg="Could not read sample RPM")

    def test_constructor_args_localfile_file_exists_is_srpm(self):
        '''args'''
        result = False
        if os.path.isfile('./docs/samples/sample.spec'):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([ 'rpmbuild', '-bs', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            testpkg = self.Package(localfilename='/tmp/SRPMS/sample-1-1.1.src.rpm')
            os.remove('/tmp/SRPMS/sample-1-1.1.src.rpm')
            if testpkg.name == 'sample':  # pragma: no cover
                if testpkg.epoch == '0':
                    if testpkg.version == '1':
                        if testpkg.release == '1.1':
                            if testpkg.arch == 'src':
                                result = True
        else:  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find sample spec')
            else:
                return True

        self.assertTrue(result, msg="Could not read sample RPM")

    def test_set_from_file_exists(self):
        '''args'''
        result = False
        testpkg = self.Package()
        if os.path.isfile('./docs/samples/sample.spec'):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                testpkg.set_from_file('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm')
                os.remove('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm')
            elif os.path.isfile('/tmp/noarch/sample-1-1.1.noarch.rpm'):
                testpkg.set_from_file('/tmp/noarch/sample-1-1.1.noarch.rpm')
                os.remove('/tmp/RPMS/sample-1-1.1.noarch.rpm')
            else:  # pragma: no cover
                if hasattr(unittest, 'SkipTest'):
                    raise unittest.SkipTest('Could not build sample spec')
                else:
                    return True

            if testpkg.name == 'sample':  # pragma: no cover
                if testpkg.epoch == '0':
                    if testpkg.version == '1':
                        if testpkg.release == '1.1':
                            if testpkg.arch == 'noarch':
                                result = True
        else:  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find sample spec')
            else:
                return True

        self.assertTrue(result, msg="Could not read sample RPM")

    def test_set_from_file_exists_checksum(self):
        '''args'''
        result = False
        testpkg = self.Package()
        if os.path.isfile('./docs/samples/sample.spec'):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([ 'rpmbuild', '-bb', '--define', '%_topdir /tmp/', './docs/samples/sample.spec'], stdout=devnull, stderr=devnull)
            if os.path.isfile('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm'):
                testpkg.set_from_file('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm', checksum='sha')
                os.remove('/tmp/RPMS/noarch/sample-1-1.1.noarch.rpm')
            elif os.path.isfile('/tmp/noarch/sample-1-1.1.noarch.rpm'):
                testpkg.set_from_file('/tmp/noarch/sample-1-1.1.noarch.rpm', checksum='sha')
                os.remove('/tmp/RPMS/sample-1-1.1.noarch.rpm')
            else:  # pragma: no cover
                if hasattr(unittest, 'SkipTest'):
                    raise unittest.SkipTest('Could not build sample spec')
                else:
                    return True

            if testpkg.name == 'sample':  # pragma: no cover
                if testpkg.epoch == '0':
                    if testpkg.version == '1':
                        if testpkg.release == '1.1':
                            if testpkg.arch == 'noarch':
                                result = True
        else:  # pragma: no cover
            if hasattr(unittest, 'SkipTest'):
                raise unittest.SkipTest('Could not find sample spec')
            else:
                return True

        self.assertTrue(result, msg="Could not read sample RPM")


class PackageXMLViewTests(PackageModelTests):
    ''' Test the XML interface for sanity '''
    Package = PackageXML

    def test_as_str_is_pprint(self):
        '''pprint'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        ppoutput = '''<package arch="src" name="asdf" release="gh" version="jkl">
  <filename>asdf-jkl-gh.src.rpm</filename>
</package>
'''
        result = str(testpkg)
        if result != ppoutput:  # pragma: no cover
            self.assertTrue(False, msg="Could not convert to string")

    def test_get_xml(self):
        '''raw xml'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = False
        if testpkg.xml == '<package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Could not get flat xml")

    def test_get_xml_min(self):
        '''raw xml'''
        testpkg = self.Package()
        testpkg.filename = 'asdf-jkl-gh.src.rpm'

        result = False
        if testpkg.xml == '<package><filename>asdf-jkl-gh.src.rpm</filename></package>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Could not get flat xml")

    def test_get_xml_detailed_a(self):
        '''raw xml'''
        testpkg = self.Package()

        testpkg.epoch = '7'
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.srpm = 'filename.rpm'
        testpkg.src_repo_base = '/path/'
        testpkg.reboot_suggested = True
        testpkg.restart_suggested = True
        testpkg.relogin_suggested = True
        testpkg.sums['md5'] = 'asdf'

        result = False
        if testpkg.xml == '<package arch="src" epoch="7" name="asdf" release="gh" src="/path/filename.rpm" version="jkl"><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><filename>asdf-jkl-gh.src.rpm</filename><sum type="md5">asdf</sum></package>':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Could not get flat xml")

    def test_get_xml_detailed_b(self):
        '''raw xml'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.srpm = 'filename.rpm'

        result = False
        if testpkg.xml == '<package arch="src" name="asdf" release="gh" src="filename.rpm" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package>':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Could not get flat xml")

    def test_set_xml_a(self):
        '''raw xml'''
        testpkg = self.Package()
        xmlstring = '<package arch="src" name="asdf" release="gh" version="jkl"><filename>asdf-jkl-gh.src.rpm</filename></package>'
        testpkg.xml = xmlstring
        result = False
        if testpkg.version == 'jkl':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="Could not set from flat xml")

    def test_set_xml_b(self):
        '''Try with really messy xml'''
        testpkg = self.Package()
        xmlstring = '<package arch="src" epoch="7" name="asdf" release="gh" src="/path/filename.rpm" version="jkl"><reboot_suggested>true</reboot_suggested><restart_suggested>true</restart_suggested><relogin_suggested>true</relogin_suggested><filename>asdf-jkl-gh.src.rpm</filename><sum type="md5">asdf</sum></package>'

        testpkg.xml = xmlstring
        result = False
        if testpkg.reboot_suggested:  # pragma: no cover
            if testpkg.version == 'jkl':
                if testpkg.sums['md5'] == 'asdf':
                    result = True
        self.assertTrue(result, msg="Could not set from flat xml")

    def test_set_xml_min(self):
        '''raw xml'''
        testpkg = self.Package()
        testpkg.xml = '<package><filename>asdf-jkl-gh.src.rpm</filename></package>'

        result = False
        if testpkg.xml == '<package><filename>asdf-jkl-gh.src.rpm</filename></package>':  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Could not set from min xml")

    def test_get_xml_obj(self):
        '''xmlobj'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = False
        if testpkg.xmletree.tag == 'package':  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get package xmlobj')

    def test_get_xml_obj_is_element(self):
        '''xmlobj'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        result = False
        if xmletree.iselement(testpkg.xmletree):  # pragma: no cover
            result = True
        self.assertTrue(result, msg='Failed to get package xmlobj')

    def test_set_xml_obj(self):
        '''xmlobj'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()

        testpkg2.xmletree = testpkg.xmletree

        result = False
        if testpkg2.xmletree.tag == 'package':  # pragma: no cover
            result = True

        self.assertTrue(result, msg='Failed to set from package xmlobj')

    def test_set_xml_obj_bad_tag(self):
        '''xmlobj'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'

        testpkg2 = self.Package()

        xmltree = testpkg.xmletree
        xmltree.tag = 'asdf'

        result = False
        try:
            testpkg2.xmletree = xmltree
        except ValueError:
            result = True

        self.assertTrue(result, msg='can set from bad xmlobj')

class PackageYAMLViewTests(PackageModelTests):
    ''' Test the YAML interface for sanity '''
    Package = PackageYAML

    def test_get_yaml_text_a(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.sums['md5'] = 'asdf'

        txt = '''asdf-jkl-gh.src.rpm:
  arch: src
  name: asdf
  release: gh
  sums: {md5: asdf}
  version: jkl
'''
        result = False
        if testpkg.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='YAML txt looks funny')

    def test_get_yaml_text_b(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.sums['md5'] = 'asdf'
        testpkg.sums['sha256'] = 'asdf'

        txt = '''asdf-jkl-gh.src.rpm:
  arch: src
  name: asdf
  release: gh
  sums: {md5: asdf, sha256: asdf}
  version: jkl
'''
        result = False
        if testpkg.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='YAML txt looks funny')

    def test_get_yaml_text_c(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.filename = 'asdf-jkl-gh.src.rpm'

        txt = '''asdf-jkl-gh.src.rpm'''
        result = False
        if testpkg.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='YAML txt looks funny')

    def test_get_yaml_text_d(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.epoch = '7'
        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.srpm = 'filename.rpm'
        testpkg.src_repo_base = '/path/'
        testpkg.reboot_suggested = True
        testpkg.restart_suggested = True
        testpkg.relogin_suggested = True
        testpkg.sums['md5'] = 'asdf'

        txt = '''asdf-jkl-gh.src.rpm:
  arch: src
  epoch: '7'
  name: asdf
  reboot_suggested: true
  release: gh
  relogin_suggested: true
  restart_suggested: true
  srpm: filename.rpm
  sums: {md5: asdf}
  version: jkl
'''
        result = False
        if testpkg.yaml == txt:  # pragma: no cover
            result = True
        self.assertTrue(result, msg='YAML txt looks funny')

    def test_get_yaml_parse_text_a(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.sums['md5'] = 'asdf'

        checkit = safe_load(testpkg.yaml)
        as_str = '''{'asdf-jkl-gh.src.rpm': {'release': 'gh', 'arch': 'src', 'version': 'jkl', 'sums': {'md5': 'asdf'}, 'name': 'asdf'}}'''

        result = False
        if str(checkit) == as_str:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="YAML didn't parse right")

    def test_get_yaml_parse_text_b(self):
        '''can I get back the right looking YAML'''
        testpkg = self.Package()

        testpkg.filename = 'asdf-jkl-gh.src.rpm'

        checkit = safe_load(testpkg.yaml)
        as_str = '''asdf-jkl-gh.src.rpm'''

        result = False
        if str(checkit) == as_str:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="YAML didn't parse right")

    def test_set_from_yaml_a(self):
        '''If I pass you correctly formatted YAML do you setup correctly?'''
        testpkg = self.Package()
        txt = '''asdf-jkl-gh.src.rpm:
  arch: src
  epoch: '1'
  name: asdf
  release: gh
  sums: {md5: asdf, sha256: asdf}
  version: jkl
  srpm: filename.rpm
  reboot_suggested: true
'''

        testpkg.yaml = txt
        result = False
        if testpkg.arch == 'src':  # pragma: no cover
            if testpkg.epoch == '1':
                if testpkg.name == 'asdf':
                    if testpkg.release == 'gh':
                        if testpkg.sums.md5 == 'asdf':
                            if testpkg.sums.sha256 == 'asdf':
                                if testpkg.version == 'jkl':
                                    if testpkg.reboot_suggested:
                                        if testpkg.filename == 'asdf-jkl-gh.src.rpm':
                                            if testpkg.srpm == 'filename.rpm':
                                                result = True
        self.assertTrue(result, msg="YAML didn't convert to obj right")

    def test_set_from_yaml_b(self):
        '''If I pass you correctly formatted YAML do you setup correctly?'''
        testpkg = self.Package()
        txt = '''asdf-jkkl-gh.src.rpm:
  arch: src
  epoch: '1'
  name: asdf
  release: gh
  sums: {md5: asdf, sha256: asdf}
  version: jkl
  reboot_suggested: true
  restart_suggested: true
  relogin_suggested: true
'''

        testpkg.yaml = txt
        result = False
        if testpkg.arch == 'src':  # pragma: no cover
            if testpkg.epoch == '1':
                if testpkg.name == 'asdf':
                    if testpkg.release == 'gh':
                        if testpkg.sums.md5 == 'asdf':
                            if testpkg.sums.sha256 == 'asdf':
                                if testpkg.version == 'jkl':
                                    if testpkg.reboot_suggested:
                                        if testpkg.filename == 'asdf-jkkl-gh.src.rpm':
                                            result = True
        self.assertTrue(result, msg="YAML didn't convert to obj right")

    def test_set_from_yaml_c(self):
        '''If I pass you correctly formatted YAML do you setup correctly?'''
        testpkg = self.Package()
        txt = 'asdf-jkkl-gh.src.rpm'

        testpkg.yaml = txt
        result = False

        if testpkg.filename == 'asdf-jkkl-gh.src.rpm':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="YAML didn't convert to obj right")

    def test_set_from_yaml_d(self):
        '''If I pass you correctly formatted YAML do you setup correctly?'''
        testpkg = self.Package()
        txt = 'asdf-jkkl-gh.src.rpm:'

        testpkg.yaml = txt
        result = False

        if testpkg.filename == 'asdf-jkkl-gh.src.rpm':  # pragma: no cover
            result = True
        self.assertTrue(result, msg="YAML didn't convert to obj right")

    def test_cant_set_from_yaml_b(self):
        '''If I pass you correctly formatted YAML do you setup correctly?'''
        testpkg = self.Package()
        txt = '''aasdf-jkkl-gh.src.rpm:
  arch: src
asdf-jkkl-gh.src.rpm:
  arch: src
  epoch: '1'
  name: asdf
  release: gh
  sums: {md5: asdf, sha256: asdf}
  version: jkl
  reboot_suggested: true
'''

        result = False
        try:
            testpkg.yaml = txt
        except ValueError:
            result = True
        self.assertTrue(result, msg="YAML converts weird things")

class PackageJSONViewTests(PackageModelTests):
    ''' Test the JSON interface for sanity '''
    Package = PackageJ

    def test_get_json_a(self):
        '''First json get test'''
        testpkg = self.Package()

        testpkg.name = 'asdf'
        testpkg.version = 'jkl'
        testpkg.release = 'gh'
        testpkg.arch = 'src'
        testpkg.sums['md5'] = 'asdf'

        expected = '{"asdf-jkl-gh.src.rpm": {"release": "gh", "arch": "src", "version": "jkl", "sums": {"md5": "asdf"}, "name": "asdf"}}'

        result = False
        if testpkg.json == expected:  # pragma: no cover
            result = True

        self.assertTrue(result, msg="Got bad JSON")

    def test_set_json_a(self):
        '''First json test'''
        testpkg = self.Package()

        testpkg.json = '{"asdf-jkl-gh.src.rpm": {"release": "gh", "arch": "src", "version": "jkl", "sums": {"md5": "asdf"}, "name": "asdf"}}'

        result = False
        if testpkg.name == 'asdf':  # pragma: no cover
            if testpkg.version == 'jkl':
                if testpkg.release == 'gh':
                    if testpkg.arch == 'src':
                        if testpkg.sums['md5'] == 'asdf':
                            if testpkg.filename == 'asdf-jkl-gh.src.rpm':
                                result = True
        self.assertTrue(result, msg="Can't set from JSON")

class PackageTests(PackageEventsTests, PackageXMLViewTests, PackageYAMLViewTests, PackageJSONViewTests):
    '''Test default object'''
    Package = UpdateinfoPackage

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.Package.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

