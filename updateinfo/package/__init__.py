#pylint: disable=line-too-long
'''
    For an update you should supply the packages associated with the update.
    This object captures one of those packages.
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

from .models import PackageModel
from .events import PackageEvents
from .views import PackageXMLView
from .views import PackageYAMLView
from .views import PackageJSONView

from ..about import __version__

class Package(PackageModel, PackageEvents, PackageJSONView, PackageYAMLView, PackageXMLView):
    '''
        This is an XML representation of an Updateinfo Package Stanza
         - Contains elements from the classes:
            PackageModel
            PackageEvents
            PackageXMLView
            PackageYAMLView
            PackageJSONView
    '''
    __version__ = __version__
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        PackageModel.__init__(self)
        PackageEvents.__init__(self, localfilename, src_repo_base, defaultsum)
        PackageXMLView.__init__(self)
        PackageYAMLView.__init__(self)
        PackageJSONView.__init__(self)
