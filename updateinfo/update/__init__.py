#pylint: disable=line-too-long
'''
    Each update requires an entry describing it.  The entry
    has a few parts.  The doc in this module will help you with
    what you need.
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

from .models import UpdateModel
from .events import UpdateEvents
from .views import UpdateXMLView
from .views import UpdateYAMLView
from .views import UpdateJSONView

from ..about import __version__

class Update(UpdateModel, UpdateEvents, UpdateJSONView, UpdateXMLView, UpdateYAMLView):
    '''
        This is an XML representation of an Updateinfo Update Stanza
         - Contains elements from the classes:
            UpdateModel
            UpdateEvents
            UpdateXMLView
            UpdateYAMLView
            UpdateJSONView
    '''
    __version__ = __version__
    def __init__(self):
        UpdateModel.__init__(self)
        UpdateEvents.__init__(self)
        UpdateXMLView.__init__(self)
        UpdateYAMLView.__init__(self)
        UpdateJSONView.__init__(self)

