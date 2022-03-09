#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    A package object has many parts, this is some output types
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
import sys

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

class PackageXMLView(object):
    '''
        This object provides an XML interface for the Package Updateinfo stanzas
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
        xmlobj = xmletree.Element('package')
        if self.epoch:
            if self.epoch not in ['0', 0]:
                xmlobj.attrib['epoch'] = self.epoch

        if self.name:
            xmlobj.attrib['name'] = self.name

        if self.version:
            xmlobj.attrib['version'] = self.version

        if self.release:
            xmlobj.attrib['release'] = self.release

        if self.arch:
            xmlobj.attrib['arch'] = self.arch

        if self.srpm:
            if self.src_repo_base:
                xmlobj.attrib['src'] = self.src_repo_base + self.srpm
            else:
                xmlobj.attrib['src'] = self.srpm

        if self.reboot_suggested:
            reboot_obj = xmletree.Element('reboot_suggested')
            reboot_obj.text = 'true'
            xmlobj.append(reboot_obj)
        if self.restart_suggested:
            restart_obj = xmletree.Element('restart_suggested')
            restart_obj.text = 'true'
            xmlobj.append(restart_obj)
        if self.relogin_suggested:
            relogin_obj = xmletree.Element('relogin_suggested')
            relogin_obj.text = 'true'
            xmlobj.append(relogin_obj)

        package_obj = xmletree.Element('filename')
        package_obj.text = self.filename
        xmlobj.append(package_obj)

        if self.sums:
            for checksum in self.sums:
                checksum_obj = xmletree.Element('sum')
                checksum_obj.attrib['type'] = checksum
                checksum_obj.text = self.sums[checksum]
                xmlobj.append(checksum_obj)

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'package':
            raise ValueError('Wrong XML Schema')

        logging.debug("Trying to set package from xml: %s", xmlobj)

        if 'epoch' in xmlobj.keys():
            # I am an ugly, ugly, ugly hack
            # I support both python 2 and python 3 as a result
            if (sys.version_info > (3, 0)):  # pragma: no cover
                self.epoch = str(xmlobj.attrib['epoch'])
            else:  # pragma: no cover
                self.epoch = unicode(xmlobj.attrib['epoch'])
        if 'name' in xmlobj.keys():
            self.name = xmlobj.attrib['name']
        if 'version' in xmlobj.keys():
            self.version = xmlobj.attrib['version']
        if 'release' in xmlobj.keys():
            self.release = xmlobj.attrib['release']
        if 'arch' in xmlobj.keys():
            self.arch = xmlobj.attrib['arch']
        if 'src' in xmlobj.keys():
            self.srpm = xmlobj.attrib['src']
            self.src_url_base = os.path.dirname(self.srpm)
            self.srpm = os.path.basename(self.srpm)

        for subtree in xmlobj:
            if subtree.tag == 'filename':
                self.filename = subtree.text
            elif subtree.tag == 'sum':
                self.sums[subtree.attrib['type']] = subtree.text
            elif subtree.tag == 'reboot_suggested':
                if subtree.text in ('true', 'True', True):
                    self.reboot_suggested = True
            elif subtree.tag == 'restart_suggested':
                if subtree.text in ('true', 'True', True):
                    self.restart_suggested = True
            elif subtree.tag == 'relogin_suggested':
                if subtree.text in ('true', 'True', True):
                    self.relogin_suggested = True

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

class PackageYAMLView(object):
    '''
        This object provides a YAML interface for the Package Updateinfo stanzas
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
        yamldict[self.filename] = {}

        if self.epoch:
            if self.epoch not in ['0', 0]:
                yamldict[self.filename]['epoch'] = self.epoch
        if self.name:
            yamldict[self.filename]['name'] = self.name
        if self.version:
            yamldict[self.filename]['version'] = self.version
        if self.release:
            yamldict[self.filename]['release'] = self.release
        if self.arch:
            yamldict[self.filename]['arch'] = self.arch
        if self.srpm:
            yamldict[self.filename]['srpm'] = self.srpm
        if self.reboot_suggested:
            yamldict[self.filename]['reboot_suggested'] = self.reboot_suggested
        if self.restart_suggested:
            yamldict[self.filename]['restart_suggested'] = self.restart_suggested
        if self.relogin_suggested:
            yamldict[self.filename]['relogin_suggested'] = self.relogin_suggested
        if self.sums:
            yamldict[self.filename]['sums'] = {}
            for checksum in self.sums:
                yamldict[self.filename]['sums'][checksum] = self.sums[checksum]

        yamltxt = yaml.safe_dump(yamldict)

        # if we have no sub attributes, just make me some text, not a dict
        if not yamldict[self.filename].keys():
            yamltxt = self.filename


        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        yamldict = yaml.safe_load(yamlstring)

        # no attribs, no need to define as a dict
        if (sys.version_info < (3, 0)):
            # I'm a hack for py2/3 compat!
            if isinstance(yamldict, unicode):  # pragma: no cover
                self.filename = yamldict
                return self
        if isinstance(yamldict, str):
            self.filename = yamldict
            return self

        if len(yamldict.keys()) != 1:
            raise ValueError('Found more than one object to interpit')

        logging.debug("Trying to set package from yaml: %s", yamlstring)

        filename = yamldict.keys()[0]

        if yamldict[filename] == None:
            yamldict[filename] = {}

        if 'epoch' in yamldict[filename]:
            self.epoch = yamldict[filename]['epoch']
        if 'name' in yamldict[filename]:
            self.name = yamldict[filename]['name']
        if 'version' in yamldict[filename]:
            self.version = yamldict[filename]['version']
        if 'release' in yamldict[filename]:
            self.release = yamldict[filename]['release']
        if 'arch' in yamldict[filename]:
            self.arch = yamldict[filename]['arch']
        if 'srpm' in yamldict[filename]:
            self.srpm = yamldict[filename]['srpm']
        if 'reboot_suggested' in yamldict[filename]:
            self.reboot_suggested = yamldict[filename]['reboot_suggested']
        if 'restart_suggested' in yamldict[filename]:
            self.restart_suggested = yamldict[filename]['restart_suggested']
        if 'relogin_suggested' in yamldict[filename]:
            self.relogin_suggested = yamldict[filename]['relogin_suggested']

        if 'sums' in yamldict[filename]:
            for checksum in yamldict[filename]['sums']:
                self.sums[checksum] = yamldict[filename]['sums'][checksum]

        try:
            if self.filename != filename:
                self.filename = filename
        except ValueError:
            self.filename = filename

        return self

class PackageJSONView(PackageYAMLView):
    '''
        I am the JSON view of this package object
    '''

    def __init__(self):
        '''setup'''
        PackageYAMLView.__init__(self)

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
        logging.debug("Trying to set package from json(via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

