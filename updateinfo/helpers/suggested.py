#pylint: disable=line-too-long
'''
    A set of helper functions for dealing with suggesting things
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

def set_suggested(update_obj):
    '''
        Look for some commonly used strings to indicate we should be setting
        suggested reboot/restart/relogin
    '''
    if 'system must be rebooted' in update_obj.description:
        update_obj.reboot_suggested = True
    elif 'system rebooted' in update_obj.description:
        update_obj.reboot_suggested = True
    elif 'must be restarted' in update_obj.description:
        update_obj.restart_suggested = True
    if 'desktop must be restarted' in update_obj.description:
        update_obj.relogin_suggested = True

    return update_obj
