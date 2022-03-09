#pylint: disable=line-too-long
'''
    Run me for unit tests!
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
from __future__ import print_function

import os
import sys
import unittest

# Things we use that might be missing
from collections import OrderedDict
from lxml import etree
from yaml import safe_load

if __name__ == '__main__':
    sys.path.insert(0, os.getcwd())

    # The actual XML objects
    from updateinfo.collection.tests import *
    from updateinfo.collection.store.tests import *
    from updateinfo.package.tests import *
    from updateinfo.package.store.tests import *
    from updateinfo.reference.tests import *
    from updateinfo.reference.store.tests import *
    from updateinfo.update.tests import *
    from updateinfo.updateinfo.tests import *

    # Helpful things we provide
    from updateinfo.helpers.tests import *

    print('------------')
    print('Python Search Path:')
    for PATH in sys.path:
        print("  " + PATH)
    print('------------')
    unittest.main()

