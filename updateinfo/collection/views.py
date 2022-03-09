#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    A Collection object should generally resemble this structure
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

from ..helpers.xmltools import xml_pretty_formatter

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

class CollectionXMLView(object):
    '''
        This object provides an XML interface for the Collection Updateinfo stanzas

        It requires the 'Package' updateinfo class found in package/__init__.py
         if you want a different Package container you can easily write your own view
    '''
    def __init__(self):
        '''I'm just a collection of in/out put methods'''
        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:  # pragma: no cover
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
        xmlobj = xmletree.Element('collection')
        if self.short_name not in (None, ''):
            xmlobj.attrib['short'] = self.short_name
        if self.release_name != None:
            coll_release_name = xmletree.Element('name')
            coll_release_name.text = self.release_name
            xmlobj.append(coll_release_name)

        for pkg in self:
            xmlobj.append(self[pkg].xmletree)

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'collection':
            raise ValueError('Wrong xml schema')

        logging.debug("Trying to set collection from xml: %s", xmlobj)

        if 'short' in xmlobj.attrib:
            self.short_name = xmlobj.attrib['short']

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as taskpool:
            for child in xmlobj:
                if child.tag == 'name':
                    self.release_name = child.text
                elif child.tag == 'package':
                    taskpool.submit(self.__addxmlpackage, child)

        return self

    def __addxmlpackage(self, packagexmlobj):
        '''A thread-able way to add the packages'''
        newpkg = self.Package()
        newpkg.xmletree = packagexmlobj
        self.add(newpkg)

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

class CollectionYAMLView(object):
    '''
        This object provides an YAML interface for the Collection Updateinfo stanzas

        It requires the 'Package' updateinfo class found in package/__init__.py
         if you want a different Package container you can easily write your own view
    '''
    def __init__(self):
        '''Nothing to do here'''
        pass

    @property
    def yaml(self):
        '''
            Get the YAML representation of this object, using @property
             you can also set the object from this property
        '''
        yamldict = {}

        keyname = None

        if self.short_name:
            keyname = self.short_name
        elif self.release_name:
            keyname = self.release_name
        else:
            raise ValueError("No 'name' for this collection")

        yamldict[keyname] = []
        if self.release_name:
            yamldict[keyname].append({'release_name': self.release_name})

        for pkg in self:
            yamlobj = yaml.safe_load(self[pkg].yaml)
            yamldict[keyname].append(yamlobj)

        yamltxt = yaml.safe_dump(yamldict)

        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        yamldict = yaml.safe_load(yamlstring)

        if len(yamldict.keys()) != 1:
            raise ValueError('Found more than one object to interpit')

        logging.debug("Trying to set collection from yaml: %s", yamlstring)

        self.short_name = yamldict.keys()[0]

        for item in yamldict[self.short_name]:
            if isinstance(item, dict):
                if 'release_name' in item:
                    self.release_name = item['release_name']
                else:
                    newpkg = self.Package()
                    newpkg.yaml = yaml.safe_dump(item)
                    self.add(newpkg)
            else:
                newpkg = self.Package()
                newpkg.yaml = yaml.safe_dump(item)
                self.add(newpkg)

        return self

class CollectionJSONView(CollectionYAMLView):
    '''
        I am the JSON view of this collection object
    '''

    def __init__(self):
        '''setup'''
        CollectionYAMLView.__init__(self)

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
        logging.debug("Trying to set collection from json (via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

