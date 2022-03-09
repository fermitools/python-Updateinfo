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

import sys
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

import concurrent.futures
import multiprocessing

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

class UpdateinfoEvents(object):
    ''' Actions we can perform to set data within the Model '''
    def __init__(self, force_updatefrom=None, force_status=None, force_releasetitle=None, force_collection_name=None, force_collection_short_name=None):
        '''Catch forced action prep'''
        self._force_updatefrom = None
        self._force_status = None
        self._force_releasetitle = None
        self._force_collection_name = None
        self._force_collection_short_name = None

        self.force_updatefrom = force_updatefrom
        self.force_status = force_status
        self.force_releasetitle = force_releasetitle
        self.force_collection_name = force_collection_name
        self.force_collection_short_name = force_collection_short_name

        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:  # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    @property
    def force_updatefrom(self):
        '''Get the force_updatefrom for this xml, using @property'''
        return self._force_updatefrom
    @force_updatefrom.setter
    def force_updatefrom(self, value):
        '''Set the force_updatefrom for this xml, using @property'''
        self._force_updatefrom = value
        if self._force_updatefrom:
            self._run_forced_updatefrom()

    @property
    def force_status(self):
        '''Get the force_status for this xml, using @property'''
        return self._force_status
    @force_status.setter
    def force_status(self, value):
        '''Set the force_status for this xml, using @property'''
        self._force_status = value
        if self._force_status:
            self._run_forced_status()

    @property
    def force_releasetitle(self):
        '''Get the force_releasetitle for this xml, using @property'''
        return self._force_releasetitle
    @force_releasetitle.setter
    def force_releasetitle(self, value):
        '''Set the force_releasetitle for this xml, using @property'''
        self._force_releasetitle = value
        if self._force_releasetitle:
            self._run_force_releasetitle()

    @property
    def force_collection_name(self):
        '''Get the force_collection_name for this xml, using @property'''
        return self._force_collection_name
    @force_collection_name.setter
    def force_collection_name(self, value):
        '''Set the force_collection_name for this xml, using @property'''
        self._force_collection_name = value
        if self._force_collection_name:
            self._run_forced_collection_name(None)

    @property
    def force_collection_short_name(self):
        '''Get the force_collection_short_name for this xml, using @property'''
        return self._force_collection_short_name
    @force_collection_short_name.setter
    def force_collection_short_name(self, value):
        '''Set the force_collection_short_name for this xml, using @property'''
        self._force_collection_short_name = value
        if self._force_collection_short_name:
            self._run_forced_collection_short_name(None)

    def add(self, update, merge=True):
        '''For adding a new update to this object'''
        if xmletree.iselement(update):
            _tmp = self.Update()
            _tmp.xmletree = update
            update = _tmp

        if not isinstance(update, type(self.Update())):
            raise TypeError('I only store UpdateModel style objects, not ' + str(type(update)))

        if not update.updateid:
            raise ValueError('I require updateid defined')

        logging.debug("Trying to add to updateinfo: update:%s merge:%s", update, merge)

        if self.force_updatefrom:
            update.updatefrom = self.force_updatefrom

        if self.force_status:
            update.status = self.force_status

        if self.force_releasetitle:
            update.releasetitle = self.force_releasetitle

        if self.force_collection_short_name:
            newstore = self._run_forced_collection_short_name(update, update.collections)
            update.collections = newstore

        if self.force_collection_name:
            newstore = self._run_forced_collection_name(update, update.collections)
            update.collections = newstore

        if update.updateid in self:
            if merge:
                if update.updatefrom:
                    self[update.updateid].updatefrom = update.updatefrom
                if update.updatetype:
                    self[update.updateid].updatetype = update.updatetype
                if update.status:
                    self[update.updateid].status = update.status
                if update.schemaversion:
                    self[update.updateid].schemaversion = update.schemaversion

                if update.description:
                    self[update.updateid].description = update.description
                if update.issued_date:
                    self[update.updateid].issued_date = update.issued_date
                if update.severity:
                    self[update.updateid].severity = update.severity
                if update.summary:
                    self[update.updateid].summary = update.summary
                if update.title:
                    self[update.updateid].title = update.title

                if update.releasetitle:
                    self[update.updateid].releasetitle = update.releasetitle
                if update.update_date:
                    self[update.updateid].update_date = update.update_date
                if update.rights:
                    self[update.updateid].rights = update.rights
                if update.solution:
                    self[update.updateid].solution = update.solution

                if update.reboot_suggested:
                    self[update.updateid].reboot_suggested = update.reboot_suggested
                if update.relogin_suggested:
                    self[update.updateid].relogin_suggested = update.relogin_suggested
                if update.restart_suggested:
                    self[update.updateid].restart_suggested = update.restart_suggested

                with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as executor:
                    for ref in update.references:
                        executor.submit(self[update.updateid].references.add, update.references[ref])
                    for coll in update.collections:
                        executor.submit(self[update.updateid].collections.add, update.collections[coll])

            else:
                raise ValueError('Adding duplicate when merge disabled')
        else:
            self[update.updateid] = update

        if update.updateid in self:
            return True

        raise RuntimeError('Attempted to add entry, but not found after add')  # pragma: no cover

    def create(self, updateid, updatefrom, status, updatetype, title, issued_date,
               description, severity, releasetitle, summary, rights,
               solution, update_date=None, reboot_suggested=False,
               restart_suggested=False, relogin_suggested=False,
               schemaversion='2.0', merge=True):
        '''
            A rather dirty way of adding a new Update without creating
            the object first.
        '''
        logging.debug("Trying to create in updateinfo: updateid:%s updatefrom:%s status:%s updatetype:%s title:%s issued_date:%s description:%s severity:%s releasetitle:%s summary:%s rights:%s solution:%s update_date:%s reboot_suggested:%s restart_suggested:%s relogin_suggested:%s schemaversion:%s merge:%s", updateid, updatefrom, status, updatetype, title, issued_date, description, severity, releasetitle, summary, rights, solution, update_date, reboot_suggested, restart_suggested, relogin_suggested, schemaversion, merge)
        update = self.Update()
        update.updateid = updateid
        update.updatefrom = updatefrom
        update.updatetype = updatetype
        update.status = status
        update.schemaversion = schemaversion
        update.description = description
        update.issued_date = issued_date
        update.severity = severity
        update.summary = summary
        update.title = title
        update.releasetitle = releasetitle
        update.update_date = update_date
        update.rights = rights
        update.solution = solution
        update.reboot_suggested = reboot_suggested
        update.relogin_suggested = relogin_suggested
        update.restart_suggested = restart_suggested

        return self.add(update, merge)

    def remove(self, obj):
        '''
            So you can do self.remove(update), by id or object
        '''
        name = None
        if isinstance(obj, type(self.Update())):
            name = obj.updateid
        elif isinstance(obj, str):
            name = obj
        elif (sys.version_info < (3, 0)):  # pragma: no cover
            # I'm a hack for py2/3 compat!
            if isinstance(obj, unicode):
                name = obj
            else:
                raise ValueError('Pass either updateid or the update object')
        else:
            # cant get here in python2
            raise ValueError('Pass either updateid or the update object')

        logging.debug("Trying to remove from updateinfo: update:%s", obj)
        del self[name]

        if name not in self:
            return True

        raise RuntimeError('Attempted to remove entry, but found after remove')  # pragma: no cover

    def _run_forced_updatefrom(self):
        '''I set all the updatefrom values to what was forced'''
        for update in self:
            self[update].updatefrom = self.force_updatefrom

    def _run_forced_status(self):
        '''I set all the status values to what was forced'''
        for update in self:
            self[update].status = self.force_status

    def _run_force_releasetitle(self):
        '''I set all the release values to what was forced'''
        for update in self:
            self[update].releasetitle = self.force_releasetitle

    def _run_forced_collection_name(self, update, store=None):
        '''I set all the collection names to what was forced'''
        if store:
            newstore = self.CollectionStore(parent=update)
            # just work on the store we passed in
            for coll in store:
                thiscoll = store[coll]
                thiscoll.release_name = self.force_collection_name
                newstore.add(thiscoll)
            return newstore
        else:
            for update in self:
                newstore = self._run_forced_collection_name(self[update], self[update].collections)
                self[update].collections = newstore
            return True

    def _run_forced_collection_short_name(self, update, store=None):
        '''I set all the collection shortnames to what was forced'''
        if store:
            newstore = self.CollectionStore(parent=update)
            # just work on the store we passed in
            for coll in store:
                thiscoll = store[coll]
                thiscoll.short_name = self.force_collection_short_name
                newstore.add(thiscoll)
            return newstore
        else:
            for update in self:
                newstore = self._run_forced_collection_short_name(self[update], self[update].collections)
                self[update].collections = newstore
            return True

