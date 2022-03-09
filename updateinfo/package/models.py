#pylint: disable=line-too-long
'''
    A Package object should generally resemble this structure
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

from .store import PackageSumStore

import datetime
import sys

class PackageModel(object):
    '''
        This object is a model for the Package Updateinfo stanzas
    '''
    PackageSumStore = PackageSumStore
    def __init__(self):
        '''
            Define the basics
        '''
        self._filename = None
        self._name = None
        self._epoch = None
        self._version = None
        self._release = None
        self._arch = None
        self._srpm = None
        self._src_repo_base = None

        # not really in the xml, but you may want this data....
        self._builddate = None

        # seen this here too.....
        self._reboot_suggested = False
        self._restart_suggested = False
        self._relogin_suggested = False

        self.sums = self.PackageSumStore()

        self.filename = None
        self.name = None
        self.epoch = None
        self.version = None
        self.release = None
        self.arch = None
        self.srpm = None
        self.src_repo_base = None
        self.builddate = None
        self.reboot_suggested = False
        self.restart_suggested = False
        self.relogin_suggested = False

    def __bool__(self):
        '''
            For if self: structure
            Basically, it will check to see if this object is sufficiently
            defined to be useful.
        '''
        if self.name == None:
            return False
        if self.version == None:
            return False
        if self.release == None:
            return False
        if self.arch == None:
            return False
        return True

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __eq__(self, other):
        '''Are the packages equal (not checking sums or urls)'''
        # we can safely determine we are not eq to None or empty things
        if other in ['', None, (), [], {} ]:
            return False

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)) + ' ->' + str(other))

        if self.name != other.name:
            return False
        if self.version != other.version:
            return False
        if self.release != other.release:
            return False
        if self.arch != other.arch:
            return False
        if self.srpm != other.srpm:
            return False
        if self.reboot_suggested != other.reboot_suggested:
            return False
        if self.restart_suggested != other.restart_suggested:
            return False
        if self.relogin_suggested != other.relogin_suggested:
            return False

        if self.epoch != other.epoch:
            return False

        return True

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    @property
    def filename(self):
        '''return what this RPM should be named'''
        if self._filename:
            return self._filename
        if not self:
            raise ValueError('Missing required values for automatic filename')
        filename = self.name + '-' + self.version + '-' + self.release + '.' + self.arch + '.rpm'
        return filename
    @filename.setter
    def filename(self, value):
        '''explicitly set the filename for this package'''
        if value:
            value = value.lstrip().rstrip()
        self._filename = value

    @property
    def name(self):
        '''Get the name using @property'''
        return self._name
    @name.setter
    def name(self, value):
        '''Set the name using @property'''
        self._name = value

    @property
    def epoch(self):
        '''Get the epoch using @property'''
        if self._epoch == None:
            # I am an ugly, ugly, ugly hack
            # I support both python 2 and python 3 as a result
            if (sys.version_info > (3, 0)):  # pragma: no cover
                return str(0)
            else:  # pragma: no cover
                return unicode(0)

        return self._epoch
    @epoch.setter
    def epoch(self, value):
        '''Set the epoch using @property'''
        if value == None:
            value = 0

        if isinstance(value, int) or isinstance(value, long):
            # I am an ugly, ugly, ugly hack
            # I support both python 2 and python 3 as a result
            if (sys.version_info > (3, 0)):  # pragma: no cover
                value = str(value)
            else:  # pragma: no cover
                value = unicode(value)

        # I am an ugly, ugly, ugly hack
        # I support both python 2 and python 3 as a result
        if (sys.version_info < (3, 0)):
            if isinstance(value, str):
                value = unicode(value)
        if not value.isnumeric():
            raise ValueError('epoch must be numeric, not ' + value)

        self._epoch = value

    @property
    def version(self):
        '''Get the version using @property'''
        return self._version
    @version.setter
    def version(self, value):
        '''Set the version using @property'''
        self._version = value

    @property
    def release(self):
        '''Get the release using @property'''
        return self._release
    @release.setter
    def release(self, value):
        '''Set the release using @property'''
        self._release = value

    @property
    def arch(self):
        '''Get the arch using @property'''
        return self._arch
    @arch.setter
    def arch(self, value):
        '''Set the arch using @property'''
        self._arch = value

    @property
    def srpm(self):
        '''Get the srpm using @property'''
        return self._srpm
    @srpm.setter
    def srpm(self, value):
        '''Get the srpm using @property'''
        self._srpm = value

    @property
    def src_repo_base(self):
        '''Get the src_repo_base using @property'''
        return self._src_repo_base
    @src_repo_base.setter
    def src_repo_base(self, value):
        '''Set the src_repo_base using @property'''
        if value != None:
            if not value.endswith('/'):
                value = value + '/'
        self._src_repo_base = value

    @property
    def builddate(self):
        '''Get the builddate using @property'''
        return self._builddate
    @builddate.setter
    def builddate(self, builddate):
        '''Set the builddate using @property'''
        if builddate == None:
            self._builddate = None
        elif isinstance(builddate, datetime.datetime):
            self._builddate = builddate
        else:
            # raises TypeError if this isn't of the right sort
            builddate = datetime.datetime.fromtimestamp(builddate)
            self._builddate = builddate

    @property
    def reboot_suggested(self):
        '''Get the reboot_suggested using @property'''
        return self._reboot_suggested
    @reboot_suggested.setter
    def reboot_suggested(self, value):
        '''Get the reboot_suggested using @property'''
        self._reboot_suggested = bool(value)

    @property
    def restart_suggested(self):
        '''Get the restart_suggested using @property'''
        return self._restart_suggested
    @restart_suggested.setter
    def restart_suggested(self, value):
        '''Get the restart_suggested using @property'''
        self._restart_suggested = bool(value)

    @property
    def relogin_suggested(self):
        '''Get the relogin_suggested using @property'''
        return self._relogin_suggested
    @relogin_suggested.setter
    def relogin_suggested(self, value):
        '''Get the relogin_suggested using @property'''
        self._relogin_suggested = bool(value)

