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

import logging
import os
import rpm

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class PackageEvents(object):
    '''
        Actions we can perform to set data within the Model
    '''
    def __init__(self, localfilename=None, src_repo_base=None, defaultsum='sha256'):
        '''
            If you want to automatically act on a filename, just pass it in here
        '''
        self.src_repo_base = src_repo_base
        self._default_sum = defaultsum

        if localfilename != None:
            self.set_from_file(localfilename)

    def set_from_file(self, localfilename, checksum=None):
        '''
            Read in the local filename and fill out our model
        '''
        if not checksum:
            checksum = self._default_sum

        logging.debug("Trying to set package from localfile:%s", localfilename)

        _fd = open(localfilename, 'r')
        _ts = rpm.TransactionSet()
        hdr = _ts.hdrFromFdno(_fd)
        _fd.close()

        self.filename = os.path.basename(localfilename)
        self.name = hdr[rpm.RPMTAG_NAME]
        self.epoch = hdr[rpm.RPMTAG_EPOCH]
        self.version = hdr[rpm.RPMTAG_VERSION]
        self.release = hdr[rpm.RPMTAG_RELEASE]
        self.arch = hdr[rpm.RPMTAG_ARCH]
        self.builddate = hdr[rpm.RPMTAG_BUILDTIME]

        if hdr[rpm.RPMTAG_SOURCERPM]:
            self.srpm = hdr[rpm.RPMTAG_SOURCERPM]
            self.arch = hdr[rpm.RPMTAG_ARCH]
        else:
            self.srpm = self.filename
            self.arch = 'src'

        hdr.unload()

        self.sums[checksum] = localfilename

