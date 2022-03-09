#pylint: disable=line-too-long
'''
    Collections come in lists, but how do you look them up?
    This way!
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

import concurrent.futures
import logging
import multiprocessing
import weakref

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class CollectionStoreModel(object):
    '''
        I am a cute model of how these can be looked up
    '''
    def __init__(self, parent=None):
        '''setup'''
        # stored by short_name
        self._collist = {}

        # for if you need to look back at the update containing these
        self._parent = None
        if parent != None:
            self._parent = weakref.ref(parent)

        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:   # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __bool__(self):
        '''Am I "true" ie defined?'''
        return bool(self.shortnames)

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    def __eq__(self, other):
        '''Is this _exactly_ equal to another CollectionStoreModel'''
        # we can safely determine we are not eq to None or ()
        if other in [None, ()]:
            return False

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))

        # easy checks early
        if len(self) != len(other):
            return False
        if self.shortnames != other.shortnames:
            return False
        if self.packages != other.packages:
            return False

        for coll in self:
            if self[coll] != other[coll]:
                return False

        return True

    def __len__(self):
        '''what is my length?'''
        return len(self.shortnames)

    def __getitem__(self, key):
        ''' Used for: treating like a dict '''
        return self._collist[key]

    def __delitem__(self, key):
        ''' Used for: removing  like a dict '''
        del self._collist[key]

    def __setitem__(self, key, value):
        '''
             For simply adding a collection (no merge)
        '''
        if not isinstance(value, type(self.Collection())):
            raise TypeError('I can only add ' + str(type(self.Collection())) + ' type objects, not ' + str(type(value)))

        if key != value.short_name:
            raise ValueError('Incorrect shortname, should have been "' + value.short_name + '"')

        self._collist[key] = value

    def __contains__(self, key):
        '''
            Used for: x in object
             this covers hrefs or CollectionModel style objects

             For CollectionModel style objects an exact match is required.
        '''
        try:
            name = key.short_name
            if name in self.shortnames:
                if key == self[name]:
                    return True
        except AttributeError:
            if key in self.shortnames:
                return True
        return False

    def __iter__(self):
        '''Used for: looping though, always sorted by name'''
        for name in self.shortnames:
            yield name

    @property
    def shortnames(self):
        '''Get a list of all 'short names' in use by collections, alpha sorted'''
        names = self._collist.keys()
        names.sort()
        return tuple(names)
    @shortnames.setter
    def shortnames(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def packages(self):
        '''Get a list of all packages in the collection store'''
        logging.debug("Trying to get all packages in collectionstore")
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads)
        results = executor.map(self.__getpkgset, self)

        _pkgset = set()

        for result in results:
            _pkgset = _pkgset.union(result)

        return tuple(_pkgset)
    @packages.setter
    def packages(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    def __getpkgset(self, collname):
        '''A threadsafe way to get this data'''
        return set(self[collname].packages)

    @property
    def filenames(self):
        '''Get a list of all filenames in the collection store'''
        logging.debug("Trying to get all filenames in collectionstore")
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads)
        results = executor.map(self.__getfilenameset, self)

        _fileset = set()

        for result in results:
            _fileset = _fileset.union(result)

        return tuple(_fileset)
    @filenames.setter
    def filenames(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    def __getfilenameset(self, collname):
        '''A threadsafe way to get this data'''
        return set(self[collname].filenames)

