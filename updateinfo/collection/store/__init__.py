#pylint: disable=line-too-long
'''
    Behold the collection store object
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

from .events import CollectionStoreEvents
from .models import CollectionStoreModel
from .views import CollectionStoreXMLView
from .views import CollectionStoreYAMLView
from .views import CollectionStoreJSONView

from ...about import __version__

class CollectionStore(CollectionStoreModel, CollectionStoreEvents, CollectionStoreJSONView, CollectionStoreXMLView, CollectionStoreYAMLView):
    '''I am the store-er of collections'''
    __version__ = __version__
    def __init__(self, parent=None):
        '''setup'''
        CollectionStoreModel.__init__(self, parent=parent)
        CollectionStoreEvents.__init__(self)
        CollectionStoreXMLView.__init__(self)
        CollectionStoreYAMLView.__init__(self)
        CollectionStoreJSONView.__init__(self)

