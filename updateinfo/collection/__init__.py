#pylint: disable=line-too-long
'''
    Each update may have various collections of packages.

    For example, SL5 and SL6 might both need an update for nss,
      but the packages for SL5 are not at all alike.
     So you need one collection for SL5 and another for SL6.
      The SL5 packages might require a restart of services
      while the SL6 ones might require you to relogin.
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

from .models import CollectionModel
from .events import CollectionEvents
from .views import CollectionXMLView
from .views import CollectionYAMLView
from .views import CollectionJSONView

from ..about import __version__

class Collection(CollectionModel, CollectionEvents, CollectionJSONView, CollectionXMLView, CollectionYAMLView):
    '''
        This is an XML representation of an Updateinfo Collection Stanza
         - Contains elements from the classes:
            CollectionModel
            CollectionEvents
            CollectionXMLView
            CollectionYAMLView
            CollectionJSONView
    '''
    __version__ = __version__
    def __init__(self, release_name=None, short_name=None):
        CollectionModel.__init__(self, release_name, short_name)
        CollectionEvents.__init__(self)
        CollectionXMLView.__init__(self)
        CollectionYAMLView.__init__(self)
        CollectionJSONView.__init__(self)

