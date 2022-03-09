#pylint: disable=line-too-long,invalid-name,too-many-public-methods,too-few-public-methods,bare-except,unused-variable,no-member,too-many-lines
'''
    I'm the unit tests for the PackageSumStore class!
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

import hashlib
import unittest

from distutils.version import StrictVersion

from .models import PackageModelSumStore
from . import PackageSumStore as UpdateinfoPackageSumStore

class SumPackageModelTests(unittest.TestCase):
    '''
        Test the Model for sanity
    '''
    PackageSumStore = PackageModelSumStore

    def test_can_init(self):
        '''Can I construt the basic object'''
        result = False
        try:
            testref = self.PackageSumStore()
            result = True
        except:  # pragma: no cover
            pass
        self.assertTrue(result, msg='basic init failed')

    def test_md5_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['md5']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['md5'] = 'asdf'
        if sums['md5']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.md5(txt).hexdigest()
        sums['md5'] = '/etc/hosts'
        if sums['md5'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['md5'] = 'asdf'
        del sums['md5']
        if sums['md5']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.md5:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="md5 should be undef now")
    def test_md5_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.md5 = 'asdf'
        if sums.md5:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_md5_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.md5(txt).hexdigest()
        sums.md5 = '/etc/hosts'
        if sums.md5 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="md5 should be def now")
    def test_def_if_md5(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.md5 = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have md5 should be def now")


    def test_sha_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['sha']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha'] = 'asdf'
        if sums['sha']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        sums['sha'] = '/etc/hosts'
        if sums['sha'] == value:
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha'] = 'asdf'
        del sums['sha']
        if sums['sha']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.sha:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha should be undef now")
    def test_sha_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha = 'asdf'
        if sums.sha:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_sha_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        sums.sha = '/etc/hosts'
        if sums.sha == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha should be def now")
    def test_def_if_sha(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have sha should be def now")


    def test_sha1_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['sha1']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha1'] = 'asdf'
        if sums['sha1']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        sums['sha1'] = '/etc/hosts'
        if sums['sha1'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha1'] = 'asdf'
        del sums['sha1']
        if sums['sha1']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.sha1:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha1 should be undef now")
    def test_sha1_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha1 = 'asdf'
        if sums.sha1:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_sha1_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha1(txt).hexdigest()
        sums.sha1 = '/etc/hosts'
        if sums.sha1 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha1 should be def now")
    def test_def_if_sha1(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha1 = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have sha1 should be def now")


    def test_sha256_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['sha256']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha256'] = 'asdf'
        if sums['sha256']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha256(txt).hexdigest()
        sums['sha256'] = '/etc/hosts'
        if sums['sha256'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha256'] = 'asdf'
        del sums['sha256']
        if sums['sha256']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.sha256:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha256 should be undef now")
    def test_sha256_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha256 = 'asdf'
        if sums.sha256:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_sha256_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha256(txt).hexdigest()
        sums.sha256 = '/etc/hosts'
        if sums.sha256 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha256 should be def now")
    def test_def_if_sha256(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha256 = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have sha256 should be def now")


    def test_sha384_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['sha384']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha384 should be undef now")
    def test_sha384_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha384'] = 'asdf'
        if sums['sha384']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha384 should be def now")
    def test_sha384_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha384(txt).hexdigest()
        sums['sha384'] = '/etc/hosts'
        if sums['sha384'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha384 should be def now")
    def test_sha384_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha384'] = 'asdf'
        del sums['sha384']
        if sums['sha384']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha384 should be undef now")
    def test_sha384_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.sha384:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha384 should be undef now")
    def test_sha384_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha384 = 'asdf'
        if sums.sha384:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha384 should be def now")
    def test_sha384_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha384(txt).hexdigest()
        sums.sha384 = '/etc/hosts'
        if sums.sha384 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha384 should be def now")
    def test_def_if_sha384(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha384 = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have sha384 should be def now")


    def test_sha512_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums['sha512']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha512'] = 'asdf'
        if sums['sha512']:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha512(txt).hexdigest()
        sums['sha512'] = '/etc/hosts'
        if sums['sha512'] == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_undef(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums['sha512'] = 'asdf'
        del sums['sha512']
        if sums['sha512']:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_as_prop_default(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        if sums.sha512:  # pragma: no cover
            result = True
        self.assertFalse(result, msg="sha512 should be undef now")
    def test_sha512_as_prop_def(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha512 = 'asdf'
        if sums.sha512:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_sha512_as_prop_def_fromfile(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False

        _fd = open('/etc/hosts', 'r')
        txt = _fd.read()
        _fd.close()
        value = hashlib.sha512(txt).hexdigest()
        sums.sha512 = '/etc/hosts'
        if sums.sha512 == value:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sha512 should be def now")
    def test_def_if_sha512(self):
        '''test sumtype'''
        sums = self.PackageSumStore()
        result = False
        sums.sha512 = 'asdf'
        if sums:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="have sha512 should be def now")


    def test_sum_bad_set_sumtype(self):
        '''test bad sumtype'''
        sums = self.PackageSumStore()
        result = True
        try:
            sums['asdf'] = '/etc/hosts'
        except KeyError:
            result = False
        self.assertFalse(result, msg="Can define bad SUM")

    def test_sum_bad_get_sumtype(self):
        '''test bad key'''
        sums = self.PackageSumStore()
        result = True
        try:
            sometxt = sums['asdf']
        except KeyError:
            result = False
        self.assertFalse(result, msg="Can define bad SUM")

    def test_sum_bad_del_sumtype(self):
        '''test del'''
        sums = self.PackageSumStore()
        result = True
        try:
            del sums['asdf']
        except KeyError:
            result = False
        self.assertFalse(result, msg="Can define bad SUM")

    def test_sum_loops(self):
        '''test loops'''
        sums = self.PackageSumStore()
        sums.md5 = 'asdf'
        sums.sha512 = 'asdf'

        expected = ['md5', 'sha512']
        found = []
        for checksum in sums:
            found.append(checksum)

        result = False
        if found == expected:  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sums not found in order")

    def test_sum_keys(self):
        '''test keys'''
        sums = self.PackageSumStore()
        sums.md5 = 'asdf'
        sums.sha512 = 'asdf'

        expected = ('md5', 'sha512')

        result = False
        if expected == sums.keys():  # pragma: no cover
            result = True
        self.assertTrue(result, msg="sums not found in order")

class SumPackageTests(SumPackageModelTests):
    '''Make sure we inherited right'''
    PackageSumStore = UpdateinfoPackageSumStore

    def test_has_version(self):
        ''' Does __version__ exist '''
        result = False
        if StrictVersion(self.PackageSumStore.__version__):  # pragma: no cover
            result = True
        self.assertTrue(result, msg="can't get __version__")

