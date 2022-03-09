#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    Collections come in lists, but how do you look them up?
    This way!
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

from .. import Collection
from ...helpers.xmltools import xml_pretty_formatter

import concurrent.futures
import logging
import multiprocessing

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

# for the YAMLView
import yaml

# for the JSONView
import json

class CollectionStoreXMLView(object):
    '''
        I am the XML view of this storage object
    '''
    Collection = Collection

    def __init__(self):
        '''setup'''
        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:   # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    def __str__(self):
        '''
            Simple way of dumping the xml, it is pretty in this mode
        '''
        tree = self.xmletree
        xml_pretty_formatter(tree)
        return xmletree.tostring(tree)

    @property
    def xmletree(self):
        '''
            Get an XML Etree representation of this object, using @property
             you can also set the object from this property
        '''
        xmlobj = xmletree.Element('pkglist')

        for coll in self:
            xmlobj.append(self[coll].xmletree)

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'pkglist':
            raise ValueError('Not the right xml stanza')

        logging.debug("Trying to set collectionstore from xml: %s", xmlobj)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as taskpool:
            for child in xmlobj:
                taskpool.submit(self.__addxmlcoll, child)

        return self

    def __addxmlcoll(self, collxmlobj):
        '''do the collection importing in a thread-able way'''
        newcoll = self.Collection()
        newcoll.xmletree = collxmlobj
        self.add(newcoll)

    @property
    def xml(self):
        '''
            Get the XML representation of this object, using @property
             you can also set the object from this property
        '''
        return xmletree.tostring(self.xmletree)

    @xml.setter
    def xml(self, xmlstring):
        '''Set the object from an XML string, using @property'''
        self.xmletree = xmletree.fromstring(xmlstring)
        return self

class CollectionStoreYAMLView(object):
    '''
        I am the YAML view of this storage object
    '''
    Collection = Collection

    def __init__(self):
        '''setup'''
        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:   # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    @property
    def yaml(self):
        '''
            Get the YAML representation of this object, using @property
             you can also set the object from this property
        '''
        yamldict = {}
        yamldict['collections'] = []

        for coll in self:
            yamlobj = yaml.safe_load(self[coll].yaml)
            yamldict['collections'].append(yamlobj)

        yamltxt = yaml.safe_dump(yamldict)

        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        yamldict = yaml.safe_load(yamlstring)

        if len(yamldict.keys()) != 1:
            raise ValueError('Found more than one object to interpit')

        if 'collections' not in yamldict:
            raise ValueError("Didn't find 'collections' block")

        logging.debug("Trying to set collectionstore from yaml: %s", yamlstring)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as taskpool:
            for coll in yamldict['collections']:
                taskpool.submit(self.__addyamlcoll, coll)

        return self

    def __addyamlcoll(self, coll):
        '''do the collection importing in a thread-able way'''
        newcoll = self.Collection()
        newcoll.yaml = yaml.safe_dump(coll)
        self.add(newcoll)

class CollectionStoreJSONView(CollectionStoreYAMLView):
    '''
        I am the JSON view of this storage object
    '''

    def __init__(self):
        '''setup'''
        CollectionStoreYAMLView.__init__(self)
        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:   # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    @property
    def json(self):
        '''
            Get the JSON representation of this object, using @property
             you can also set the object from this property
        '''
        # this is super lazy, but I'll just take the YAML and
        # convert it over to JSON

        return json.dumps(yaml.safe_load(self.yaml))

    @json.setter
    def json(self, jsonstring):
        '''Set the object from a JSON string, using @property'''
        # this is super lazy, but I'll just take the JSON and
        # convert it over to YAML
        logging.debug("Trying to set collectionstore from json(via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

