#pylint: disable=line-too-long
'''
    References come in lists, but how do you look them up?
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

import logging
import weakref

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .. import Reference as UinfoReference

class ReferenceStoreModel(object):
    '''
        I am a cute model of how these can be looked up
    '''
    Reference = UinfoReference
    def __init__(self, parent=None):
        '''setup'''
        # for if you need to look back at the update containing these
        self._parent = None

        self._reflist = {}
        self._byreftype = {}

        if parent != None:
            self._parent = weakref.ref(parent)

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __bool__(self):
        '''Am I "true" ie defined?'''
        return bool(self.urls)

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    def __eq__(self, other):
        '''Is this _exactly_ equal to another ReferenceStoreModel'''
        # we can safely determine we are not eq to None or ()
        if other in [None, ()]:
            return False

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))

        if self.urls != other.urls:
            return False

        for ref in self:
            if self[ref] != other[ref]:
                return False
        return True

    def __len__(self):
        '''what is my length?'''
        return len(self.urls)

    def __getitem__(self, key):
        '''
           Used for: treating like a dict
        '''
        return self._reflist[key]

    def __delitem__(self, key):
        '''
           Used for: removing  like a dict
        '''
        del self._reflist[key]

    def __setitem__(self, key, value):
        '''
             For simply adding a reference (no merge)
        '''
        if not isinstance(value, type(self.Reference())):
            raise TypeError('I can only add ' + str(type(self.Reference())) + ' type objects, not ' + str(type(value)))

        if key != value.href:
            raise ValueError('Incorrect href, should have been "' + value.href + '"')

        self._reflist[key] = value

    def __contains__(self, key):
        '''
            Used for: x in object
             this covers hrefs or ReferenceModel style objects

             For ReferenceModel style objects an exact match is required.
        '''
        try:
            href = key.href
            if href in self.urls:
                if key == self[href]:
                    return True
        except AttributeError:
            if key in self.urls:
                return True
        return False

    def __iter__(self):
        '''Used for: looping though, always sorted by url'''
        for ref in self.urls:
            yield ref

    @property
    def urls(self):
        '''Get a list of all defined urls, always sorted by url'''
        logging.debug("Trying to get all urls in refstore")
        urls = self._reflist.keys()
        urls.sort()
        return tuple(urls)
    @urls.setter
    def urls(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def reftypes(self):
        '''Get a list of all defined types, always sorted by alpha'''
        logging.debug("Trying to get all types in refstore")
        reftypes = set()
        for ref in self:
            reftypes.add(self[ref].reftype)
        reftypes = list(reftypes)
        reftypes.sort()
        return tuple(reftypes)
    @reftypes.setter
    def reftypes(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def byreftype(self):
        '''
            A dict of known refs with the following structure
            self.byreftype[reftype] = (ReferenceModel, ReferenceModel, ReferenceModel)
        '''
        _byreftype = {}

        for reftype in self.reftypes:
            _byreftype[reftype] = []

        for href in self.urls:
            _byreftype[self[href].reftype].append(self[href])

        for reftype in _byreftype:
            _byreftype[reftype] = tuple(_byreftype[reftype])
        return _byreftype

    @byreftype.setter
    def byreftype(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

