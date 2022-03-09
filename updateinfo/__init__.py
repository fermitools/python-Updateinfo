'''
    This package provides a few classes to make generation of the updateinfo.xml
    file much simpler.

    In theory.

    If you want to be able to be sure you are making valid xml
     you will need the lxml python module.  The functions
     do not enforce the xsd without it.  And even then you
     can disable it if you want.

    Simply importing this package should get you all the classes you need
     into your local namespace.

     Updateinfo
     Update
     Reference
     Collection
     Package
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

# import basics so that you can just use things with clean names

# for python3 compat
from __future__ import unicode_literals
from __future__ import absolute_import

from .collection import Collection
from .package import Package
from .reference import Reference
from .update import Update
from .updateinfo import Updateinfo
