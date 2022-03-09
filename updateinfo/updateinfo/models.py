#pylint: disable=line-too-long
'''
    A Updateinfo object should generally resemble this structure
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

from ..update import Update
from ..collection.store import CollectionStore

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class UpdateinfoModel(object):
    ''' This object is a model for the Updateinfo stanzas '''
    Update = Update
    CollectionStore = CollectionStore

    def __init__(self):
        ''' Define the basics '''
        self._updates = {}
        self._xsluri = None
        self._xsduri = None

        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:  # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __bool__(self):
        '''
            For if self: structure
            Basically, it will check to see if this object is sufficiently
            defined to be useful.
        '''
        return bool(len(self))

    def __iter__(self):
        '''Used for: looping'''
        return iter(self.ids)

    def __len__(self):
        '''Used for: len()'''
        return len(self.ids)

    def __getitem__(self, key):
        '''Used for: accessing update items like a dict'''
        return self._updates[key]

    def __delitem__(self, key):
        '''for removing like a dict'''
        del self._updates[key]

    def __setitem__(self, key, value):
        '''
             For simply adding an update (no merge)
        '''
        if not isinstance(value, type(self.Update())):
            raise TypeError('I can only add ' + str(type(self.Update())) + ' type objects, not ' + str(type(value)))

        if key != value.updateid:
            raise ValueError('Incorrect updateid, should have been "' + value.updateid + '"')

        self._updates[key] = value


    def __contains__(self, key):
        '''
            Used for: x in object
             this covers IDs or EntryModel style objects

             For EntryModel style objects an exact match is required.
        '''
        try:
            updateid = key.updateid
            if updateid not in self.ids:
                return False
            if key != self[key.updateid]:
                return False
        except AttributeError:
            updateid = key
            if key not in self.ids:
                return False
        return True

    @property
    def xsluri(self):
        '''Get the xsluri for this xml, using @property'''
        return self._xsluri
    @xsluri.setter
    def xsluri(self, value):
        '''Set the xsluri for this xml, using @property'''
        self._xsluri = value

    @property
    def xsduri(self):
        '''Get the xsduri for this xml, using @property'''
        return self._xsduri
    @xsduri.setter
    def xsduri(self, value):
        '''Set the xsduri for this xml, using @property'''
        self._xsduri = value

    @property
    def ids(self):
        '''Get a list of all update ids in this updateinfo object'''
        logging.debug("Trying to get all updates")
        knownids = self._updates.keys()
        knownids.sort()
        return tuple(knownids)
    @ids.setter
    def ids(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def collection_names(self):
        '''Get a list of all collections known to this updateinfo object'''
        logging.debug("Trying to get all collections")
        colllist = set()
        for update in self:
            colllist = colllist.union(set(self[update].collections.shortnames))
        finallist = list(colllist)
        finallist.sort()
        return tuple(finallist)
    @collection_names.setter
    def collection_names(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def references(self):
        '''Get a list of all references known to this updateinfo object'''
        logging.debug("Trying to get all references")
        reflist = set()
        for update in self:
            reflist = reflist.union(set(self[update].references))
        finallist = list(reflist)
        finallist.sort()
        return tuple(finallist)
    @references.setter
    def references(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def packages(self):
        '''Get a list of all packages in this updateinfo object'''
        logging.debug("Trying to get all packages")
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
    def __getpkgset(self, updateid):
        '''A threadsafe way to get this data'''
        return set(self[updateid].packages)

    @property
    def filenames(self):
        '''Get a list of all packages in this updateinfo object'''
        logging.debug("Trying to get all filenames")
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads)
        results = executor.map(self.__getfilenameset, self)

        _pkgset = set()

        for result in results:
            _pkgset = _pkgset.union(result)

        return tuple(_pkgset)
    @filenames.setter
    def filenames(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")
    def __getfilenameset(self, updateid):
        '''A threadsafe way to get this data'''
        return set(self[updateid].filenames)

