#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    I am a mixin for the UpdateinfoModel object.

    I add XML in/out options.

    usage:
    class myclass(UpdateinfoModel, UpdateinfoXMLView):
        def __init__(self)
            UpdateinfoModel.__init__(self)
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
from ..helpers.xmltools import get_xsl_pi
from ..helpers.xmltools import add_xsd_uri
from ..helpers.yamltools import yaml_represent_ordereddict

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
from collections import OrderedDict

# for the JSONView
import json

class UpdateinfoXMLView(object):
    '''
        This object provides an XML interface for the Updateinfo stanzas
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
        xsltxt = ''
        if self.xsluri:
            xsltxt = xmletree.tostring(get_xsl_pi(self.xsluri)) + '\n'
        tree = self.xmletree
        xml_pretty_formatter(tree)
        xmlstring = xmletree.tostring(tree)
        return xsltxt + xmlstring

    @property
    def xmletree(self):
        '''
            Get an XML Etree representation of this object, using @property
             you can also set the object from this property
        '''
        xmlobj = xmletree.Element('updates')

        if self.xsduri:
            xmlobj = add_xsd_uri(self.xsduri, xmlobj)

        for update in self:
            xmlobj.append(self[update].xmletree)

        #if self.xsluri:
        #    raise NotImplementedError('I think this requires lxml?')
        #    xsl_pi = get_xsl_pi(self.xsluri)
        #    xmlobj.addprevious(xsl_pi)

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'updates':
            raise ValueError('Wrong xml schema')

        logging.debug("Trying to set updateinfo from xml: %s", xmlobj)

        if '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation' in xmlobj.attrib:
            self.xsduri = xmlobj.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as taskpool:
            for updatexmlobj in xmlobj:
                taskpool.submit(self.__addxmlupdate, updatexmlobj)

        return self

    def __addxmlupdate(self, updatexmlobj):
        '''A thread-able way to add the updates'''
        newupdate = self.Update()
        newupdate.xmletree = updatexmlobj
        self.add(newupdate)

    @property
    def xml(self):
        '''
            Get the XML representation of this object, using @property
             you can also set the object from this property
        '''
        xsltxt = ''
        if self.xsluri:
            xsltxt = xmletree.tostring(get_xsl_pi(self.xsluri)) + '\n'
        xmlstring = xmletree.tostring(self.xmletree)
        return xsltxt + xmlstring

    @xml.setter
    def xml(self, xmlstring):
        '''Set the object from an XML string, using @property'''
        if xmlstring:
            self.xmletree = xmletree.fromstring(xmlstring)
        else:
            self.xmletree = xmletree.fromstring('<updates />')
        return self

class UpdateinfoYAMLView(object):
    '''
        This object provides an YAML interface for the Updateinfo stanzas
    '''
    def __init__(self):
        '''just basic setup'''
        self.__max_threads = multiprocessing.cpu_count()
        if self.__max_threads > 1:  # pragma: no cover
            # don't crush the box
            self.__max_threads = self.__max_threads - 1

    @property
    def yaml(self):
        '''
            Get the YAML representation of this object, using @property
             you can also set the object from this property
        '''
        updates = []
        for thisupdate in self:
            updates.append(self[thisupdate].ordereddict)

        yaml.SafeDumper.add_representer(OrderedDict, lambda dumper, value: yaml_represent_ordereddict(dumper, u'tag:yaml.org,2002:map', value))

        yamltxt = yaml.safe_dump(updates, default_flow_style=False)
        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        mylist = yaml.safe_load(yamlstring)
        logging.debug("Trying to set updateinfo from yaml: %s", yamlstring)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__max_threads) as taskpool:
            for thisupdate in mylist:
                taskpool.submit(self.__addyamlupdate, thisupdate)

        return self

    def __addyamlupdate(self, thisupdate):
        '''A thread-able way to add the updates'''
        newupdate = self.Update()
        newupdate.yaml = yaml.safe_dump(thisupdate)
        self.add(newupdate)


class UpdateinfoJSONView(UpdateinfoYAMLView):
    '''
        I am the JSON view of this storage object
    '''

    def __init__(self):
        '''setup'''
        UpdateinfoYAMLView.__init__(self)

    @property
    def json(self):
        '''
            Get the JSON representation of this object, using @property
             you can also set the object from this property
        '''
        # this is super lazy, but I'll just take the YAML and
        # convert it over to JSON

        yamldict = yaml.safe_load(self.yaml)
        for thisone in yamldict:
            # datetime doesn't convert to JSON, :( fix it here
            if 'issued_date' in thisone:
                thisone['issued_date'] = thisone['issued_date'].strftime('%Y-%m-%d %H:%M:%S')
            if 'update_date' in thisone:
                thisone['update_date'] = thisone['update_date'].strftime('%Y-%m-%d %H:%M:%S')

        return json.dumps(yamldict)

    @json.setter
    def json(self, jsonstring):
        '''Set the object from a JSON string, using @property'''
        # this is super lazy, but I'll just take the JSON and
        # convert it over to YAML
        logging.debug("Trying to set updateinfo from json(via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

