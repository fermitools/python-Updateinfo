#pylint: disable=line-too-long
'''
    I'm the top level thing!
     Oh the objects I embed
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

from .events import UpdateinfoEvents
from .models import UpdateinfoModel
from .views import UpdateinfoXMLView
from .views import UpdateinfoYAMLView
from .views import UpdateinfoJSONView

from ..about import __version__

class Updateinfo(UpdateinfoModel, UpdateinfoEvents, UpdateinfoJSONView, UpdateinfoXMLView, UpdateinfoYAMLView):
    '''
        This is a representation of an Updateinfo XML
         - Contains elements from the classes:
            UpdateinfoModel
            UpdateinfoEvents
            UpdateinfoXMLView
            UpdateinfoYAMLView
            UpdateinfoJSONView
    '''
    __version__ = __version__
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        UpdateinfoModel.__init__(self)
        UpdateinfoEvents.__init__(self, force_updatefrom=force_updatefrom, force_status=force_status, force_releasetitle=force_releasetitle, force_collection_name=force_collection_name, force_collection_short_name=force_collection_short_name)
        UpdateinfoXMLView.__init__(self)
        UpdateinfoYAMLView.__init__(self)
        UpdateinfoJSONView.__init__(self)

