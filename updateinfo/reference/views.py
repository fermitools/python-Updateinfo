#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    I am a mixin for the ReferenceModel object.

    I add XML in/out options.

    usage:
    class myclass(ReferenceModel, ReferenceXMLView):
        def __init__(self, reftype=None, href=None, refid=None, title=None):
            ReferenceModel.__init__(self, reftype=reftype, href=href, refid=refid, title=title)
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

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from ..helpers.xmltools import xml_pretty_formatter

# for the XMLView
try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

# for the YAMLView
import yaml

# for the JSONView
import json

class ReferenceXMLView(object):
    '''
        This object provides an XML interface for the Reference Updateinfo stanzas
    '''
    def __init__(self):
        '''I'm just a collection of in/out put methods'''
        pass

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
        xmlobj = xmletree.Element('reference')

        if self.title:
            xmlobj.attrib['title'] = self.title
        if self.refid:
            xmlobj.attrib['id'] = self.refid

        xmlobj.attrib['type'] = self.reftype
        xmlobj.attrib['href'] = self.href

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'reference':
            raise ValueError('Wrong xml schema')

        logging.debug("Trying to set reference from xml: %s", xmlobj)

        if 'title' in xmlobj.attrib:
            self.title = xmlobj.attrib['title']

        if 'type' in xmlobj.attrib:
            self.reftype = xmlobj.attrib['type']

        if 'id' in xmlobj.attrib:
            self.refid = xmlobj.attrib['id']

        if 'href' in xmlobj.attrib:
            self.href = xmlobj.attrib['href']

        return self

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

class ReferenceYAMLView(object):
    '''
        This object provides a YAML interface for the Reference Updateinfo stanzas
    '''
    def __init__(self):
        '''I'm just a collection of in/out put methods'''
        pass

    @property
    def yaml(self):
        '''
            Get the YAML representation of this object, using @property
             you can also set the object from this property
        '''
        yamldict = {}
        yamldict[self.href] = {}

        yamldict[self.href]['type'] = self.reftype

        if self.title:
            yamldict[self.href]['title'] = self.title
        if self.refid:
            yamldict[self.href]['refid'] = self.refid

        yamltxt = yaml.safe_dump(yamldict)

        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        yamldict = yaml.safe_load(yamlstring)

        if len(yamldict.keys()) != 1:
            raise ValueError('Found more than one object to interpit')

        logging.debug("Trying to set reference from yaml: %s", yamlstring)

        self.href = yamldict.keys()[0]

        self.reftype = yamldict[self.href]['type']
        if 'title' in yamldict[self.href]:
            self.title = yamldict[self.href]['title']
        if 'refid' in yamldict[self.href]:
            self.refid = yamldict[self.href]['refid']

        return self

class ReferenceJSONView(ReferenceYAMLView):
    '''
        I am the JSON view of this reference object
    '''

    def __init__(self):
        '''setup'''
        ReferenceYAMLView.__init__(self)

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
        logging.debug("Trying to set reference from json(via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

