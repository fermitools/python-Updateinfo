#pylint: disable=line-too-long
'''
    A Update object should generally resemble this structure
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

import datetime
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from ..reference.store import ReferenceStore
from ..collection.store import CollectionStore

class UpdateModel(object):
    '''
        This object is a model for the Update Updateinfo stanzas
    '''
    ReferenceStore = ReferenceStore
    CollectionStore = CollectionStore

    def __init__(self):
        ''' Define the basics '''
        self._updateid = None
        self._updatefrom = None
        self._updatetype = None
        self._status = None
        self._schemaversion = None

        self._description = None
        self._issued_date = None
        self._severity = None
        self._summary = None
        self._title = None

        self._releasetitle = None
        self._update_date = None
        self._rights = None
        self._solution = None

        self._reboot_suggested = None
        self._relogin_suggested = None
        self._restart_suggested = None

        self._collections = self.CollectionStore(parent=self)
        self._references = self.ReferenceStore(parent=self)

        self.schemaversion = '2.0'
        self.reboot_suggested = False
        self.relogin_suggested = False
        self.restart_suggested = False

    def __nonzero__(self):
        '''Python2 compat function'''
        return type(self).__bool__(self)

    def __bool__(self):
        '''Am I sufficiently defined'''
        # release name might be in collection, so it isn't required
        #
        # A title is not actually required..... :(
        # A description is not actually required..... :(
        # A severity is not actually required for security errata ..... :(
        # A reference is not actually required..... :(
        if self.status in (None, '', 0, '0') or self.updatefrom in (None, ''):
            return False
        if self.updatetype in (None, '', 0, '0') or self.updateid in (None, ''):
            return False
        if self.issued_date == None:
            return False

        if self.updatetype not in ['recommended', 'security', 'optional', 'feature', 'bugfix', 'enhancement', 'newpackage']:
            raise ValueError("Update type '" + str(self.updatetype) + "'not 'recommended' ,'security', 'optional', 'feature', 'bugfix', 'enhancement', or 'newpackage'")

        if self.status not in ['stable', 'prerelease', 'testing', 'final']:
            raise ValueError("Status type '" + str(self.status) + "' not 'stable', 'prerelease', 'testing' or 'final'")

        if not self.collections:
            return False

        return True

    def __eq__(self, other):
        '''Is this _exactly_ equal to another UpdateModel?'''
        # we can safely determine we are not eq to None or ()
        if other in [None, '', (), [], {}]:
            return False

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))

        if self.updateid != other.updateid:
            return False
        if self.updatefrom != other.updatefrom:
            return False
        if self.updatetype != other.updatetype:
            return False
        if self.status != other.status:
            return False
        if self.schemaversion != other.schemaversion:
            return False

        if self.description != other.description:
            return False
        if self.issued_date != other.issued_date:
            return False
        if self.severity != other.severity:
            return False
        if self.summary != other.summary:
            return False
        if self.title != other.title:
            return False

        if self.releasetitle != other.releasetitle:
            return False
        if self.update_date != other.update_date:
            return False
        if self.rights != other.rights:
            return False
        if self.solution != other.solution:
            return False

        if self.reboot_suggested != other.reboot_suggested:
            return False
        if self.relogin_suggested != other.relogin_suggested:
            return False
        if self.restart_suggested != other.restart_suggested:
            return False

        if self.references != other.references:
            return False
        if self.collections != other.collections:
            return False

        return True

    def __ne__(self, other):
        ''' see __eq__()'''
        # we can safely determine we are not eq to None or ()
        if other in [None, ()]:
            return True

        # we can only compare like objects
        if not isinstance(other, type(self)):
            raise TypeError("I only work on " + str(type(self)) + " type objects, not " + str(type(other)))
        return not self.__eq__(other)

    @property
    def status(self):
        '''Get the status of this entry, using @property'''
        return self._status

    @status.setter
    def status(self, value):
        '''
            Set the status of this entry, using @property

            For setting
               <update status="xxxxxx">

            Should this be consistant throughout the whole file?
            That depends....
        '''
        if value not in ['stable', 'prerelease', 'testing', 'final']:
            raise ValueError("Status type '"+ value + "' not 'stable', 'prerelease', 'testing' or 'final'")

        self._status = value

    @property
    def updatefrom(self):
        '''Get the updatefrom of this entry, using @property'''
        return self._updatefrom

    @updatefrom.setter
    def updatefrom(self, value):
        '''
            Set the updatefrom of this entry, using @property

            For setting
               <update from="xxxxxx">

            Should this be consistant throughout the whole file?
            That depends....
        '''
        self._updatefrom = value

    @property
    def updatetype(self):
        '''Get the updatetype of this entry, using @property'''
        return self._updatetype

    @updatetype.setter
    def updatetype(self, value):
        '''
            Set the updatetype of this entry, using @property

            For setting
               <update type="xxxxxx">
        '''
        if value not in ['recommended', 'security', 'optional', 'feature', 'bugfix', 'enhancement', 'newpackage']:
            raise ValueError("""Update type not 'recommended' ,'security', 'optional', 'feature', 'bugfix', 'enhancement', or 'newpackage'""")

        self._updatetype = value

    @property
    def schemaversion(self):
        '''Get the schemaversion of this entry, using @property'''
        return self._schemaversion

    @schemaversion.setter
    def schemaversion(self, value):
        '''Set the schemaversion of this entry, using @property'''
        self._schemaversion = value

    @property
    def releasetitle(self):
        ''' Get the releasetitle of this entry, using @property '''
        return self._releasetitle

    @releasetitle.setter
    def releasetitle(self, value):
        '''
           Set the releasetitle of this entry, using @property
            If all the collections in this update have a common release, set it here
        '''
        if value != None:
            value = value.title()
        self._releasetitle = value

    @property
    def updateid(self):
        '''Get the updateid of this entry, using @property'''
        return self._updateid

    @updateid.setter
    def updateid(self, value):
        '''Set the updateid of this entry, using @property'''
        self._updateid = value

    @property
    def title(self):
        '''Get the title of this entry, using @property'''
        return self._title

    @title.setter
    def title(self, value):
        '''Set the title of this entry, using @property'''
        if value != None:
            value = value.title()
        self._title = value

    @property
    def severity(self):
        '''Get the severity of this entry, using @property'''
        return self._severity

    @severity.setter
    def severity(self, value):
        '''
            Set the severity of this entry, using @property

            Severity should be one of: critical, important, moderate, low
        '''
        if value != None:
            value = value.lower()
            if value not in ('critical', 'important', 'moderate', 'low', 'none'):
                raise ValueError('Severity should be one of: critical, important, moderate, low, or None not: ' + str(value) + ' for ' + str(self.updateid))
        if value == 'none':
            value = None

        self._severity = value

    @property
    def issued_date(self):
        '''Get the issued_date of this entry, using @property'''
        return self._issued_date

    @issued_date.setter
    def issued_date(self, issued_datetime):
        '''
            Set the issued_date of this entry, using @property

            Note, this shoule be in format
                    2011-10-25 16:03:34
                 or 2011-10-25 16:03:34 TZ
                 or 2011-10-25 16:03:34 +0000
                 or 2011-10-25
                 or epoch time
                 or a datetime.date object
                 or a datetime.datetime object
        '''
        if issued_datetime == None:
            self._issued_date = None
        elif isinstance(issued_datetime, int):
            # epoch time
            self._issued_date = datetime.datetime.fromtimestamp(issued_datetime)
        elif isinstance(issued_datetime, datetime.datetime):
            self._issued_date = issued_datetime
        elif isinstance(issued_datetime, datetime.date):
            self._issued_date = datetime.datetime.combine(issued_datetime, datetime.time())
        else:
            try:
                self._issued_date = datetime.datetime.strptime(issued_datetime, '%Y-%m-%d %H:%M:%S %z')
            except ValueError:
                try:
                    self._issued_date = datetime.datetime.strptime(issued_datetime, '%Y-%m-%d %H:%M:%S %Z')
                except ValueError:
                    try:
                        self._issued_date = datetime.datetime.strptime(issued_datetime, '%Y-%m-%d')
                    except ValueError:
                        try:
                            self._issued_date = datetime.datetime.strptime(issued_datetime, '%m/%d/%Y')
                        except ValueError:
                            try:
                                self._issued_date = datetime.datetime.strptime(issued_datetime, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                mydate = ' '.join(issued_datetime.split(' ', 2)[:2])
                                self._issued_date = datetime.datetime.strptime(mydate, '%Y-%m-%d %H:%M:%S')

        if issued_datetime != None:
            if not isinstance(self._issued_date, datetime.datetime):
                raise ValueError("Could not parse out date:" + issued_datetime)

    @property
    def update_date(self):
        '''Get the update_date of this entry, using @property'''
        return self._update_date

    @update_date.setter
    def update_date(self, update_datetime):
        '''
           Set the update_date of this entry, using @property
            Note, this shoule be in format
                    2011-10-25 16:03:34
                 or 2011-10-25
                 or epoch time
                 or a datetime.datetime object
        '''
        if update_datetime == None:
            self._update_date = None
        elif isinstance(update_datetime, int):
            # epoch time
            self._update_date = datetime.datetime.fromtimestamp(update_datetime)
        elif isinstance(update_datetime, datetime.datetime):
            self._update_date = update_datetime
        else:
            try:
                self._update_date = datetime.datetime.strptime(update_datetime, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    self._update_date = datetime.datetime.strptime(update_datetime, '%Y-%m-%d')
                except ValueError:
                    self._update_date = datetime.datetime.strptime(update_datetime, '%m/%d/%Y')
        if update_datetime != None:
            if not isinstance(self._update_date, datetime.datetime):
                raise ValueError("Could not parse out date:" + update_datetime)

    @property
    def description(self):
        '''Get the description of this entry, using @property'''
        return self._description

    @description.setter
    def description(self, value):
        '''Set the description of this entry, using @property'''
        if value != None:
            value = value.replace('\r', '')
        self._description = value

    @property
    def solution(self):
        '''Get the solution of this entry, using @property'''
        return self._solution

    @solution.setter
    def solution(self, value):
        '''Set the solution of this entry, using @property'''
        self._solution = value

    @property
    def rights(self):
        '''Get the rights of this entry, using @property'''
        return self._rights

    @rights.setter
    def rights(self, value):
        '''Set the rights of this entry, using @property'''
        self._rights = value

    @property
    def summary(self):
        '''Get the summary of this entry, using @property'''
        return self._summary

    @summary.setter
    def summary(self, value):
        '''Set the summary of this entry, using @property'''
        self._summary = value

    @property
    def reboot_suggested(self):
        '''Get the reboot_suggested of this entry, using @property'''
        return self._reboot_suggested

    @reboot_suggested.setter
    def reboot_suggested(self, value):
        '''Set the reboot_suggested of this entry, using @property'''
        self._reboot_suggested = bool(value)

    @property
    def restart_suggested(self):
        '''Get the restart_suggested of this entry, using @property'''
        return self._restart_suggested

    @restart_suggested.setter
    def restart_suggested(self, value):
        '''Set the restart_suggested of this entry, using @property'''
        self._restart_suggested = bool(value)

    @property
    def relogin_suggested(self):
        '''Get the relogin_suggested of this entry, using @property'''
        return self._relogin_suggested

    @relogin_suggested.setter
    def relogin_suggested(self, value):
        '''Set the relogin_suggested of this entry, using @property'''
        self._relogin_suggested = bool(value)

    @property
    def references(self):
        '''Get the references of this entry, using @property'''
        logging.debug("Trying to get all references in updateid:%s ", self.updateid)
        return self._references

    @references.setter
    def references(self, value):
        '''Set the references of this entry, using @property'''
        if not isinstance(value, type(self._references)):
            raise TypeError("You must set me to a " + str(type(self._references)) + " not a " + str(type(value)))
        self._references = value

    @property
    def collections(self):
        '''Get the collections of this entry, using @property'''
        logging.debug("Trying to get all collections in updateid:%s ", self.updateid)
        return self._collections

    @collections.setter
    def collections(self, value):
        '''Set the collections of this entry, using @property'''
        if not isinstance(value, type(self._collections)):
            raise TypeError("You must set me to a " + str(type(self._collections)) + " not a " + str(type(value)))
        self._collections = value

    @property
    def packages(self):
        '''Get a list of all packages in this updateinfo object'''
        logging.debug("Trying to get all packages in updateid:%s ", self.updateid)
        return self.collections.packages
    @packages.setter
    def packages(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

    @property
    def filenames(self):
        '''Get a list of all filenames in this updateinfo object'''
        logging.debug("Trying to get all filenames in updateid:%s ", self.updateid)
        return self.collections.filenames
    @filenames.setter
    def filenames(self, value):
        '''Raise error'''
        raise NotImplementedError("This is a Read Only property")

