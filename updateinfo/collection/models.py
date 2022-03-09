#pylint: disable=line-too-long
'''
    A Collection object should generally resemble this structure
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

from ..package import Package

import os

class CollectionModel(object):
    '''
        This object is a model for the Collection Updateinfo stanzas
    '''
    Package = Package
    def __init__(self, release_name=None, short_name=None):
        '''
            Define the basics
        '''
        self._release_name = None
        self._short_name = None

        self._pkglist = {}

        if release_name:
            self.release_name = release_name
        if short_name:
            self.short_name = short_name

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __bool__(self):
        '''
            For if self: structure
            Basically, it will check to see if this object is sufficiently
            defined to be useful.
        '''
        # no packages, nothing to collect
        if not self.packages:
            return False

        # Need one, but not necessarily both of these
        if self.release_name in (None, '') and self.short_name in (None, ''):
            return False

        return True

    def __eq__(self, other):
        '''Is this _exactly_ equal to another CollectionModel?'''
        # we can safely determine we are not eq to None or empty
        if other in [None, '', (), [], {}]:
            return False

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))

        if self.release_name != other.release_name:
            return False
        if self.short_name != other.short_name:
            return False
        if len(self) != len(other):
            return False

        mypkgs = []
        mypkgs.extend(iter(self))

        otherpkgs = []
        otherpkgs.extend(iter(other))

        if mypkgs != otherpkgs:
            return False

        for pkg in mypkgs:
            if self[pkg] != other[pkg]:
                return False

        return True

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    def __iter__(self):
        '''
            Used for: looping though packages,
             always sorted by alpha so the order is consistent
        '''
        pkglist = list(self.filenames)
        pkglist.sort()
        for pkg in self.filenames:
            yield pkg

    def __len__(self):
        '''
           Used for: len()
        '''
        return len(self.filenames)

    def __getitem__(self, key):
        '''
           Used for: treating the packages like a dict
        '''
        return self._pkglist[key]

    def __delitem__(self, key):
        '''
           Used for: removing the packages like a dict
        '''
        del self._pkglist[key]

    def __setitem__(self, key, value):
        '''
            For simply adding a package (no merge)
        '''
        if not isinstance(value, type(self.Package())):
            raise TypeError('I can only add ' + str(type(self.Package())) + ' type objects, not ' + str(type(value)))

        if key != value.filename:
            raise ValueError('Incorrect filename, should have been "' + value.filename + '"')

        self._pkglist[key] = value


    def __contains__(self, key):
        '''
            Used for: x in object
             this covers filenames or PackageModel style objects

             For PackageModel style objects an exact match is required.
        '''
        try:
            filename = key.filename
            if filename in self:
                if key == self[filename]:
                    return True
        except AttributeError:
            if key in self.filenames:
                return True
        return False

    @property
    def release_name(self):
        '''Get the release_name of this collection, using @property'''
        return self._release_name

    @release_name.setter
    def release_name(self, value):
        '''Set the release_name of this collection, using @property'''
        self._release_name = value

    @property
    def short_name(self):
        '''Get the short_name of this collection, using @property'''
        return self._short_name

    @short_name.setter
    def short_name(self, value):
        '''Set the short_name of this collection, using @property'''
        self._short_name = value

    @property
    def packages(self):
        '''Get a list of all packages in the collection, no path names'''
        pkgs = []
        for item in self:
            pkgs.append(os.path.basename(item))
        return tuple(pkgs)
    @packages.setter
    def packages(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def filenames(self):
        '''Get a list of all the filenames in the collection'''
        pkgs = []
        for item in self._pkglist.keys():
            pkgs.append(item)
        return tuple(pkgs)
    @filenames.setter
    def filenames(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

