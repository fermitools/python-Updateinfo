#pylint: disable=line-too-long
'''
    For an update you can supply an external website that details
    the reason for this update more clearly than you can within the xml.
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

from .models import ReferenceModel
from .events import ReferenceEvents
from .views import ReferenceXMLView
from .views import ReferenceYAMLView
from .views import ReferenceJSONView

from ..about import __version__

class Reference(ReferenceModel, ReferenceEvents, ReferenceJSONView, ReferenceXMLView, ReferenceYAMLView):
    '''
        This is an XML representation of an Updateinfo Reference Stanza
         - Contains elements from the classes:
            ReferenceModel
            ReferenceEvents
            ReferenceXMLView
            ReferenceYAMLView
            ReferenceJSONView
    '''
    __version__ = __version__
    def __init__(self, reftype=None, href=None, refid=None, title=None):
        ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
        ReferenceEvents.__init__(self)
        ReferenceXMLView.__init__(self)
        ReferenceYAMLView.__init__(self)
        ReferenceJSONView.__init__(self)
