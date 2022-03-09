#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    The various bits of action/logic we can perform are listed as a mixin here
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

import os
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

class CollectionEvents(object):
    '''
        Actions we can perform to set data within the Model
    '''
    def __init__(self):
        '''Nothing to do here'''
        pass

    def add(self, packageobj, merge=True):
        '''
            So you can do collection.add(pkgobject)
        '''
        if xmletree.iselement(packageobj):
            _tmp = self.Package()
            _tmp.xmletree = packageobj
            packageobj = _tmp

        if not isinstance(packageobj, self.Package):
            raise TypeError('I can only add ' + str(type(self.Package)) + ' type objects, not ' + str(type(packageobj)))

        logging.debug("Trying to add package to collection package:%s merge:%s", packageobj, merge)

        if packageobj.filename in self.filenames:
            if merge:
                self[packageobj.filename] = self._merge_attributes(self[packageobj.filename], packageobj)
            else:
                raise ValueError('Adding duplicate when merge disabled')

        self[packageobj.filename] = packageobj

        if packageobj.filename in self:
            return True

        raise RuntimeError('Attempted to add package to collection, but not found after add')  # pragma: no cover

    def add_filename(self, filename, readfile=False, merge=True, checksum=None):
        '''
            So you can do
              collection.add_filename('my.rpm')
              collection.add_filename('/path/to/my.rpm', readfile=True)
        '''
        logging.debug("Trying to add filename to collection filename:%s readfile:%s merge=%s checksum:%s", filename, readfile, merge, checksum)
        newpkg = self.Package()
        newpkg.filename = filename
        if readfile:
            newpkg.filename = os.path.basename(filename)
            newpkg.set_from_file(filename, checksum=checksum)

        self.add(newpkg, merge=merge)

    def remove(self, packageobj):
        '''
            So you can do collection.remove(pkg)
        '''
        filename = None
        if isinstance(packageobj, self.Package):
            filename = packageobj.filename
        elif isinstance(packageobj, str):
            filename = packageobj
        elif (sys.version_info < (3, 0)):
            # I'm a hack for py2/3 compat!
            if isinstance(packageobj, unicode):
                filename = packageobj
            else:
                raise ValueError('Pass either the filename, or the package object to remove')
        else:  # pragma: no cover
            # we never get here in python2....
            raise ValueError('Pass either the filename, or the package object to remove')

        logging.debug("Trying to remove package:%s", packageobj)
        del self[filename]

        if filename not in self:
            return True

        raise RuntimeError('Attempted to remove package from collection, but found after del')  # pragma: no cover

    @staticmethod
    def _merge_attributes(existing, packageobj):
        '''
            Attributes in the 'packageobj' will, if defined, override the existing ones
        '''
        if packageobj.name:
            existing.name = packageobj.name
        if packageobj.epoch:
            existing.epoch = packageobj.epoch
        if packageobj.version:
            existing.version = packageobj.version
        if packageobj.release:
            existing.release = packageobj.release
        if packageobj.arch:
            existing.arch = packageobj.arch
        if packageobj.srpm:
            existing.srpm = packageobj.srpm
        if packageobj.src_repo_base:
            existing.src_repo_base = packageobj.src_repo_base
        if packageobj.builddate:
            existing.builddate = packageobj.builddate
        if packageobj.reboot_suggested:
            existing.reboot_suggested = packageobj.reboot_suggested
        if packageobj.restart_suggested:
            existing.restart_suggested = packageobj.restart_suggested
        if packageobj.relogin_suggested:
            existing.relogin_suggested = packageobj.relogin_suggested

        for chksum in packageobj.sums:
            existing.sums[chksum] = packageobj.sums[chksum]

        return existing
