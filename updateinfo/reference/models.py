#pylint: disable=line-too-long
'''
    A Reference object should generally resemble this structure
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

class ReferenceModel(object):
    '''
        This object is a model for the Reference Updateinfo stanzas
    '''
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        '''
            You can pass all the required values in right here at
            the constructor if you want.

            - href is the URL for the reference
            - refid is the ID number for the reference
            - title is a nice title for the reference (under 65 char please!)
            - reftype is the sort of thing this links to
        '''
        # for clarity define all our internals here, we shortcut to define
        #  right here for simplicity
        self._href = None
        self._refid = None
        self._title = None
        self._reftype = None

        self.href = href
        self.refid = refid
        self.title = title
        self.reftype = reftype

    def __bool__(self):
        '''
            For if self: structure
            Basically, it will check to see if this object is sufficiently
            defined to be useful.
        '''
        if self.href in (None, ''):
            return False
        if self.reftype in (None, ''):
            return False

        # id isn't required so don't abuse that. OK?!
        # title isn't required so don't abuse that. OK?!

        if self.reftype not in ['bugzilla', 'cve', 'fate', 'commit', 'trac', 'other', 'self']:  # pragma: no cover
            raise ValueError("""Reference type not 'fate', 'trac', 'commit',
                                ,'other', 'bugzilla', 'self', or 'cve'""")

        return True

    def __eq__(self, other):
        '''Is this _exactly_ equal to another ReferenceModel?'''
        # we can safely determine we are not eq to None or ()
        if other in [None, ()]:
            return False

        # we can only compare like objects
        if not isinstance(other, ReferenceModel):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))

        if self.href != other.href:
            return False
        if self.refid != other.refid:
            return False
        if self.title != other.title:
            return False
        if self.reftype != other.reftype:
            return False
        return True

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    @property
    def href(self):
        '''Get the url of the reference, using @property'''
        return self._href

    @href.setter
    def href(self, value):
        '''Set the url of the reference, using @property'''
        self._href = value

    @property
    def refid(self):
        '''Get the refid of the reference, using @property'''
        return self._refid

    @refid.setter
    def refid(self, value):
        '''Set the refid of the reference, using @property'''
        self._refid = value

    @property
    def title(self):
        '''Get the title of the reference, using @property'''
        return self._title

    @title.setter
    def title(self, value):
        '''Set the title of the reference, using @property'''
        if value != None:
            value = value.title()
        self._title = value

    @property
    def reftype(self):
        '''Get the reftype of the reference, using @property'''
        return self._reftype

    @reftype.setter
    def reftype(self, value):
        '''Set the reftype of the reference, using @property'''
        if value == None:
            self._reftype = None
            return None

        value = value.lower()

        if value not in ['bugzilla', 'cve', 'fate', 'commit', 'trac', 'other', 'self', None]:
            raise ValueError("Reference type '" + value + "' not 'fate', 'trac', 'commit', 'other', 'bugzilla', 'self', 'cve', or None")

        self._reftype = value

