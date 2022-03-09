#pylint: disable=line-too-long
'''
    A set of helper functions for finding update ids
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

import re

import concurrent.futures
import multiprocessing

def what_update_has_filename(updateinfo_obj, filename):
    '''Which updateids have a given filename?'''
    def __add_if_filename_in(mylist, obj, filename):
        ''' a function we can do in parallel '''
        if filename in obj.filenames:
            mylist.append(obj.updateid)
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    results = []
    for updateid in updateinfo_obj:
        taskpool.submit(__add_if_filename_in, results, updateinfo_obj[updateid], filename)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def what_collection_has_filename(update_obj, filename):
    '''Which collections in this update have a given filename?'''
    def __add_if_filename_in(mylist, obj, filename):
        ''' a function we can do in parallel '''
        if filename in obj.filenames:
            mylist.append(obj.short_name)
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    results = []
    for coll in update_obj.collections:
        taskpool.submit(__add_if_filename_in, results, update_obj.collections[coll], filename)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def what_update_has_package(updateinfo_obj, package):
    '''Which updateids have a given package?'''
    def __add_if_package_in(mylist, obj, package):
        ''' a function we can do in parallel '''
        if package in obj.packages:
            mylist.append(obj.updateid)
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    results = []
    for updateid in updateinfo_obj:
        taskpool.submit(__add_if_package_in, results, updateinfo_obj[updateid], package)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def what_collection_has_package(update_obj, package):
    '''Which collections in this update have a given package?'''
    def __add_if_package_in(mylist, obj, package):
        ''' a function we can do in parallel '''
        if package in obj.packages:
            mylist.append(obj.short_name)
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    results = []
    for coll in update_obj.collections:
        taskpool.submit(__add_if_package_in, results, update_obj.collections[coll], package)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def what_update_has_reference(updateinfo_obj, href):
    '''Which updateids have a given reference href?'''
    def __add_if_refid_in(mylist, obj, href):
        ''' a function we can do in parallel '''
        if href in obj.references:
            mylist.append(obj.updateid)
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    results = []
    for updateid in updateinfo_obj:
        taskpool.submit(__add_if_refid_in, results, updateinfo_obj[updateid], href)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def what_update_has_reference_like(updateinfo_obj, regex):
    '''Which updateids have a given reference that matches regex?'''
    def __add_if_refid_in(mylist, obj, regex):
        ''' a function we can do in parallel '''
        for href in obj.references:
            if re.match(regex, href):
                mylist.append(obj.updateid)
                return
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    if not isinstance(regex, type(re.compile('.'))):
        regex = re.compile(regex)

    results = []
    for updateid in updateinfo_obj:
        taskpool.submit(__add_if_refid_in, results, updateinfo_obj[updateid], regex)

    taskpool.shutdown()
    results.sort()
    return tuple(results)

def all_updates_for_rpm_name(updateinfo_obj, rpmname):
    '''
        Returns a list of updates with the given 'name'
        NOTE: In this instance rpmname is the exact output from
              rpm -q --qf "%{NAME}" yourfile.rpm
    '''
    if not rpmname:
        return ()
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    found = []
    for update in updateinfo_obj:
        for collection in updateinfo_obj[update].collections:
            if update in found:
                break  # pragma: no cover
            for package in updateinfo_obj[update].collections[collection]:
                if update in found:
                    break
                if updateinfo_obj[update].collections[collection][package].name == rpmname:
                    found.append(update)

    taskpool.shutdown()
    retval = list(set(found))
    retval.sort()
    return tuple(retval)

def all_updates_for_rpm_name_and_collection(updateinfo_obj, rpmname, collection_short_name):
    '''
        Returns a list of updates with the given 'name' in a specific collection
        NOTE: In this instance rpmname is the exact output from
              rpm -q --qf "%{NAME}" yourfile.rpm
    '''
    if not rpmname:
        return ()
    taskpool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    found = []
    for update in updateinfo_obj:
        for collection in updateinfo_obj[update].collections:
            if update in found:
                break  # pragma: no cover
            if collection != collection_short_name:
                continue
            for package in updateinfo_obj[update].collections[collection]:
                if update in found:
                    break
                if updateinfo_obj[update].collections[collection][package].name == rpmname:
                    found.append(update)

    taskpool.shutdown()
    retval = list(set(found))
    retval.sort()
    return tuple(retval)

def all_packages_by_update(updateinfo_obj):
    '''
        Returns a dict of
         updateid: [package, package]
    '''
    updates = {}
    for update in updateinfo_obj:
        updates[update] = []
        for package in updateinfo_obj[update].packages:
            updates[update].append(package)

    return updates

