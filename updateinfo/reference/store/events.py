#pylint: disable=line-too-long,attribute-defined-outside-init
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

import sys
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

class ReferenceStoreEvents(object):
    '''
        I am the behavioral logic
    '''
    def __init__(self):
        '''setup'''
        pass

    def add(self, ref, merge=True):
        '''add a reference to the list'''
        if xmletree.iselement(ref):
            _tmp = self.Reference()
            _tmp.xmletree = ref
            ref = _tmp

        if not isinstance(ref, type(self.Reference())):
            raise TypeError('I can only add ReferenceModel type objects')

        if not ref.href:
            raise ValueError('No href specified')
        if not ref.reftype:
            raise ValueError('No reftype specified')

        logging.debug("Trying to add reference:%s merge:%s", ref, merge)

        if ref.href in self:
            if merge:
                self[ref.href] = self._merge_attributes(self[ref.href], ref)
            else:
                raise ValueError('Adding duplicate when merge disabled')
        else:
            self[ref.href] = ref

        if ref.href in self:
            return True

        raise RuntimeError('Attempted to add ref, but not found after add')  # pragma: no cover

    def create(self, reftype=None, href=None, refid=None, title=None, merge=True):
        '''Add a new reference to this store'''
        logging.debug("Trying to create reference: reftype=%s, href=%s, refid=%s, title=%s", reftype, href, refid, title)
        ref = self.Reference(reftype=reftype, href=href, refid=refid, title=title)
        return self.add(ref, merge)

    def remove(self, obj):
        '''so you can do a remove'''
        href = None
        if isinstance(obj, type(self.Reference())):
            href = obj.href
        elif isinstance(obj, str):
            href = obj
        elif (sys.version_info < (3, 0)):
            # I'm a hack for py2/3 compat!
            if isinstance(obj, unicode):
                href = obj
            else:
                raise ValueError('Pass either the href, or the ref object to remove')
        else:
            # I can't get here in python2
            raise ValueError('Pass either the href, or the ref object to remove')  # pragma: no cover

        logging.debug("Trying to remove reference:%s", obj)
        del self[href]

        if href not in self:
            return True

        raise RuntimeError('Attempted to remove ref, but found after remove')  # pragma: no cover

    @staticmethod
    def _merge_attributes(existing, ref):
        '''
            Attributes in the 'ref' will, if defined, override the existing ones
        '''
        if ref.refid:
            existing.refid = ref.refid
        if ref.title:
            existing.title = ref.title
        if ref.reftype:
            existing.reftype = ref.reftype

        return existing
