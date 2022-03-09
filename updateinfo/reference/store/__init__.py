#pylint: disable=line-too-long
'''
    Behold the reference store object
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

from .events import ReferenceStoreEvents
from .models import ReferenceStoreModel
from .views import ReferenceStoreXMLView
from .views import ReferenceStoreYAMLView
from .views import ReferenceStoreJSONView

from ...about import __version__

class ReferenceStore(ReferenceStoreModel, ReferenceStoreEvents, ReferenceStoreJSONView, ReferenceStoreXMLView, ReferenceStoreYAMLView):
    '''I am the store-er of references'''
    __version__ = __version__
    def __init__(self, parent=None):
        '''setup'''
        ReferenceStoreModel.__init__(self, parent=parent)
        ReferenceStoreEvents.__init__(self)
        ReferenceStoreXMLView.__init__(self)
        ReferenceStoreYAMLView.__init__(self)
        ReferenceStoreJSONView.__init__(self)

