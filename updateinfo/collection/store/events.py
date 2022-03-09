#pylint: disable=line-too-long,attribute-defined-outside-init
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

import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

from .. import Collection as UinfoCollection

class CollectionStoreEvents(object):
    '''
        I am the behavioral logic
    '''
    Collection = UinfoCollection
    def __init__(self):
        '''setup'''
        pass

    def add(self, coll, merge=True):
        '''add a collection to the list'''
        if xmletree.iselement(coll):
            _tmp = self.Collection()
            _tmp.xmletree = coll
            coll = _tmp

        if not isinstance(coll, type(self.Collection())):
            raise TypeError('I can only add ' + str(type(self.Collection())) + ' type objects, not ' + str(type(coll)))

        if coll.short_name == None:
            if coll.release_name == None:
                raise ValueError('I require short_name set for distinguishing')
            else:
                coll.short_name = coll.release_name

        logging.debug("Trying to add collection: short:%s, release:%s merge:%s", coll.short_name, coll.release_name, merge)

        if coll.short_name in self.shortnames:
            if merge:
                if coll.release_name:
                    self[coll.short_name].release_name = coll.release_name
                for pkg in coll:
                    self[coll.short_name].add(coll[pkg])
            else:
                raise ValueError('Adding duplicate when merge disabled')
        else:
            self[coll.short_name] = coll

        if coll.short_name in self:
            return True

        raise RuntimeError('Attempted to add coll, but not found after add')  # pragma: no cover

    def create(self, release_name=None, short_name=None, merge=True):
        '''Make a new collection and add it to the store'''
        logging.debug("Trying to create collection: short:%s, release:%s merge:%s", short_name, release_name, merge)
        coll = self.Collection(release_name=release_name, short_name=short_name)
        return self.add(coll, merge)

    def remove(self, obj):
        '''so you can do a remove'''
        name = None
        if isinstance(obj, type(self.Collection())):
            name = obj.short_name
        elif isinstance(obj, str):
            name = obj
        elif (sys.version_info < (3, 0)):
            # I'm a hack for py2/3 compat!
            if isinstance(obj, unicode):
                name = obj
            else:
                raise ValueError('Pass either short_name or the coll object')
        else:  # pragma: no cover
            # we never get here in python2....
            raise ValueError('Pass either short_name or the coll object')

        if name == None:
            raise ValueError('Pass either short_name or the coll object')

        logging.debug("Trying to delete collection:%s", obj)
        del self[name]

        if name not in self:
            return True

        raise RuntimeError('Attempted to remove coll, but found after remove')  # pragma: no cover

