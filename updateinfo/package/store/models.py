#pylint: disable=line-too-long
'''
    A Package object can store some checksums, but I want to control how
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
import os

class PackageModelSumStore(object):
    '''
       I store sums as object attributes, the idea being we
       should keep these things easy, simple, and full of flexibility.

       I am both a dict and a property list.
       I support:
        - md5
        - sha
        - sha384
        - sha256
        - sha512
    '''
    def __init__(self):
        '''setup'''
        self._md5 = None
        self._sha = None
        self._sha256 = None
        self._sha384 = None
        self._sha512 = None

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __getitem__(self, key):
        '''for as a dict'''
        if key == 'md5':
            return self.md5
        elif key == 'sha':
            return self.sha
        elif key == 'sha1':
            return self.sha
        elif key == 'sha256':
            return self.sha256
        elif key == 'sha384':
            return self.sha384
        elif key == 'sha512':
            return self.sha512
        if key not in ('md5', 'sha', 'sha1', 'sha256', 'sha384', 'sha512'):
            raise KeyError("No known sum: " + key)

    def __setitem__(self, key, value):
        '''for as a dict'''
        if key == 'md5':
            self.md5 = value
        elif key == 'sha':
            self.sha = value
        elif key == 'sha1':
            self.sha = value
        elif key == 'sha256':
            self.sha256 = value
        elif key == 'sha384':
            self.sha384 = value
        elif key == 'sha512':
            self.sha512 = value
        if key not in ('md5', 'sha', 'sha1', 'sha256', 'sha384', 'sha512'):
            raise KeyError("No known sum: " + key)

    def __delitem__(self, key):
        '''for as a dict'''
        if key == 'md5':
            self.md5 = None
        elif key == 'sha':
            self.sha = None
        elif key == 'sha1':
            self.sha = None
        elif key == 'sha256':
            self.sha256 = None
        elif key == 'sha384':
            self.sha384 = None
        elif key == 'sha512':
            self.sha512 = None
        if key not in ('md5', 'sha', 'sha1', 'sha256', 'sha384', 'sha512'):
            raise KeyError("No known sum: " + key)

    def __iter__(self):
        '''for a loop through set hashes'''
        defined = []
        if self.md5:
            defined.append('md5')
        if self.sha:
            defined.append('sha')
        if self.sha256:
            defined.append('sha256')
        if self.sha384:
            defined.append('sha384')
        if self.sha512:
            defined.append('sha512')
        return iter(defined)

    def __bool__(self):
        '''
            For if self: structure
            Basically, it will check to see if this object is sufficiently
            defined to be useful.
        '''
        if self.keys():
            return True
        return False

    def keys(self):
        '''For getting all defined sums as a tuple (like a dict)'''
        defined = []
        if self.md5:
            defined.append('md5')
        if self.sha:
            defined.append('sha')
        if self.sha256:
            defined.append('sha256')
        if self.sha384:
            defined.append('sha384')
        if self.sha512:
            defined.append('sha512')
        return tuple(defined)

    @property
    def md5(self):
        '''Return the md5 sum, using @property'''
        return self._md5
    @md5.setter
    def md5(self, value):
        '''Set the md5 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.md5(_fd.read()).hexdigest()
            _fd.close()
        self._md5 = value

    @property
    def sha(self):
        '''Return the sha1 sum, using @property'''
        return self._sha
    @sha.setter
    def sha(self, value):
        '''Set the sha1 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.sha1(_fd.read()).hexdigest()
            _fd.close()
        self._sha = value
    @property
    def sha1(self):
        '''Return the sha1 sum, using @property'''
        return self._sha
    @sha1.setter
    def sha1(self, value):
        '''Set the sha1 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.sha1(_fd.read()).hexdigest()
            _fd.close()
        self._sha = value

    @property
    def sha256(self):
        '''Return the sha256 sum, using @property'''
        return self._sha256
    @sha256.setter
    def sha256(self, value):
        '''Set the sha256 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.sha256(_fd.read()).hexdigest()
            _fd.close()
        self._sha256 = value

    @property
    def sha384(self):
        '''Return the sha384 sum, using @property'''
        return self._sha384
    @sha384.setter
    def sha384(self, value):
        '''Set the sha384 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.sha384(_fd.read()).hexdigest()
            _fd.close()
        self._sha384 = value

    @property
    def sha512(self):
        '''Return the sha512 sum, using @property'''
        return self._sha512
    @sha512.setter
    def sha512(self, value):
        '''Set the sha512 sum either from file or directly, using @property'''
        if value != None and os.path.isfile(value):
            _fd = open(value, 'r')
            value = hashlib.sha512(_fd.read()).hexdigest()
            _fd.close()
        self._sha512 = value
