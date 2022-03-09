#pylint: disable=line-too-long,attribute-defined-outside-init
'''
    I am the output methods for an Update model
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
from ..helpers.yamltools import yaml_represent_ordereddict

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

class UpdateXMLView(object):
    '''
        This object provides an XML interface for the Update Updateinfo stanzas
    '''
    def __init__(self):
        '''Nothing to do here'''
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
        xmlobj = xmletree.Element('update')

        if self.updatetype not in (None, ''):
            xmlobj.attrib['type'] = self.updatetype

        if self.updatefrom not in (None, ''):
            xmlobj.attrib['from'] = self.updatefrom

        if self.status not in (None, ''):
            xmlobj.attrib['status'] = self.status

        if self.schemaversion not in (None, ''):
            xmlobj.attrib['version'] = self.schemaversion

        id_obj = xmletree.Element('id')
        if self.updateid != None:
            id_obj.text = self.updateid
        xmlobj.append(id_obj)

        # mandatory even if null according to pulp
        title_obj = xmletree.Element('title')
        if self.title not in (None, ''):
            title_obj.text = self.title
        xmlobj.append(title_obj)

        # mandatory even if null according to pulp
        description_obj = xmletree.Element('description')
        if self.description not in (None, ''):
            description_obj.text = self.description
        xmlobj.append(description_obj)

        if self.severity not in (None, ''):
            severity_obj = xmletree.Element('severity')
            severity_obj.text = self.severity
            xmlobj.append(severity_obj)

        if self.summary not in (None, ''):
            summary_obj = xmletree.Element('summary')
            summary_obj.text = self.summary
            xmlobj.append(summary_obj)

        if self.rights not in (None, ''):
            rights_obj = xmletree.Element('rights')
            rights_obj.text = self.rights
            xmlobj.append(rights_obj)

        if self.solution not in (None, ''):
            solution_obj = xmletree.Element('solution')
            solution_obj.text = self.solution
            xmlobj.append(solution_obj)

        if self.releasetitle not in (None, ''):
            release_obj = xmletree.Element('release')
            release_obj.text = self.releasetitle
            xmlobj.append(release_obj)

        if self.issued_date not in (None, ''):
            issued_date_obj = xmletree.Element('issued')
            issued_date_obj.attrib['date'] = str(self.issued_date)
            xmlobj.append(issued_date_obj)
        elif self.updateid and self.updatefrom and self.updatetype and self.status and self.title and self.description:
            issued_date_obj = xmletree.Element('issued')
            issued_date_obj.attrib['date'] = '1970-01-01 00:00:00'
            xmlobj.append(issued_date_obj)

        if self.update_date not in (None, ''):
            update_date_obj = xmletree.Element('updated')
            update_date_obj.attrib['date'] = str(self.update_date)
            xmlobj.append(update_date_obj)

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

        xmlobj.append(self.collections.xmletree)
        xmlobj.append(self.references.xmletree)

        return xmlobj

    @xmletree.setter
    def xmletree(self, xmlobj):
        '''Set the object from an XML Etree object, using @property'''
        if xmlobj.tag != 'update':
            raise ValueError('Wrong xml schema')

        logging.debug("Trying to set update from xml: %s", xmlobj)

        if 'status' in xmlobj.attrib:
            self.status = xmlobj.attrib['status']
        if 'from' in xmlobj.attrib:
            self.updatefrom = xmlobj.attrib['from']
        if 'type' in xmlobj.attrib:
            self.updatetype = xmlobj.attrib['type']

        for subtree in xmlobj:
            if subtree.tag == 'id':
                self.updateid = subtree.text
            elif subtree.tag == 'title':
                self.title = subtree.text
            elif subtree.tag == 'severity':
                self.severity = subtree.text
            elif subtree.tag == 'issued':
                self.issued_date = subtree.attrib['date']
            elif subtree.tag == 'updated':
                self.update_date = subtree.attrib['date']
            elif subtree.tag == 'description':
                self.description = subtree.text
            elif subtree.tag == 'release':
                self.releasetitle = subtree.text
            elif subtree.tag == 'summary':
                self.summary = subtree.text
            elif subtree.tag == 'solution':
                self.solution = subtree.text
            elif subtree.tag == 'rights':
                self.rights = subtree.text
            elif subtree.tag == 'reboot_suggested':
                if subtree.text in ('true', 'True', True):
                    self.reboot_suggested = True
            elif subtree.tag == 'restart_suggested':
                if subtree.text in ('true', 'True', True):
                    self.restart_suggested = True
            elif subtree.tag == 'relogin_suggested':
                if subtree.text in ('true', 'True', True):
                    self.relogin_suggested = True
            elif subtree.tag == 'pkglist':
                self.collections.xmletree = subtree
            elif subtree.tag == 'references':
                self.references.xmletree = subtree

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
        if xmlstring:
            self.xmletree = xmletree.fromstring(xmlstring)
        return self

class UpdateOrderedDictView(object):
    '''
        This object provides an OrderedDict for the YAML interface
    '''
    def __init__(self):
        '''Nothing to do here'''
        pass

    @property
    def ordereddict(self):
        ''' This just returns the object with its properties in the right order'''
        yamldict = OrderedDict()

        if self.title:
            yamldict['title'] = self.title
        if self.updateid:
            yamldict['updateid'] = self.updateid
        if self.issued_date:
            yamldict['issued_date'] = self.issued_date
        if self.update_date:
            yamldict['update_date'] = self.update_date
        if self.releasetitle:
            yamldict['releasetitle'] = self.releasetitle
        if self.updatetype:
            yamldict['updatetype'] = self.updatetype
        if self.severity:
            yamldict['severity'] = self.severity

        if self.summary:
            yamldict['summary'] = self.summary
        if self.description:
            yamldict['description'] = self.description
        if self.solution:
            yamldict['solution'] = self.solution
        if self.reboot_suggested:
            yamldict['reboot_suggested'] = self.reboot_suggested
        if self.relogin_suggested:
            yamldict['relogin_suggested'] = self.relogin_suggested
        if self.restart_suggested:
            yamldict['restart_suggested'] = self.restart_suggested

        if self.collections:
            yamlobj = yaml.safe_load(self.collections.yaml)
            yamldict['collections'] = yamlobj['collections']

        if self.references:
            yamlobj = yaml.safe_load(self.references.yaml)
            yamldict['references'] = yamlobj['references']
        if self.updatefrom:
            yamldict['updatefrom'] = self.updatefrom
        if self.status:
            yamldict['status'] = self.status
        if self.rights:
            yamldict['rights'] = self.rights

        return yamldict

class UpdateYAMLView(UpdateOrderedDictView):
    '''
        This object provides an YAML interface for the Update Updateinfo stanzas
    '''
    def __init__(self):
        '''Nothing to do here'''
        UpdateOrderedDictView.__init__(self)

    @property
    def yaml(self):
        '''
            Get the YAML representation of this object, using @property
             you can also set the object from this property
        '''
        # Teach PyYAML what an OrderedDict is
        yaml.SafeDumper.add_representer(OrderedDict, lambda dumper, value: yaml_represent_ordereddict(dumper, u'tag:yaml.org,2002:map', value))
        yamltxt = yaml.safe_dump(self.ordereddict, default_flow_style=False)

        return yamltxt

    @yaml.setter
    def yaml(self, yamlstring):
        '''Set the object from a YAML string, using @property'''
        yamldict = yaml.safe_load(yamlstring)
        logging.debug("Trying to set update from yaml: %s", yamlstring)

        if 'title' in yamldict:
            self.title = yamldict['title']
        if 'updateid' in yamldict:
            self.updateid = yamldict['updateid']
        if 'issued_date' in yamldict:
            self.issued_date = yamldict['issued_date']
        if 'update_date' in yamldict:
            self.update_date = yamldict['update_date']
        if 'releasetitle' in yamldict:
            self.releasetitle = yamldict['releasetitle']
        if 'updatetype' in yamldict:
            self.updatetype = yamldict['updatetype']
        if 'severity' in yamldict:
            self.severity = yamldict['severity']

        if 'summary' in yamldict:
            self.summary = yamldict['summary']
        if 'description' in yamldict:
            self.description = yamldict['description']
        if 'solution' in yamldict:
            self.solution = yamldict['solution']

        if 'reboot_suggested' in yamldict:
            self.reboot_suggested = yamldict['reboot_suggested']
        if 'relogin_suggested' in yamldict:
            self.relogin_suggested = yamldict['relogin_suggested']
        if 'restart_suggested' in yamldict:
            self.restart_suggested = yamldict['restart_suggested']


        if 'collections' in yamldict:
            colldict = {}
            colldict['collections'] = yamldict['collections']
            self.collections.yaml = yaml.safe_dump(colldict)

        if 'references' in yamldict:
            refdict = {}
            refdict['references'] = yamldict['references']
            self.references.yaml = yaml.safe_dump(refdict)

        if 'updatefrom' in yamldict:
            self.updatefrom = yamldict['updatefrom']
        if 'status' in yamldict:
            self.status = yamldict['status']
        if 'rights' in yamldict:
            self.rights = yamldict['rights']

        return self

class UpdateJSONView(UpdateYAMLView):
    '''
        I am the JSON view of this Update object
    '''

    def __init__(self):
        '''setup'''
        UpdateYAMLView.__init__(self)

    @property
    def json(self):
        '''
            Get the JSON representation of this object, using @property
             you can also set the object from this property
        '''
        # this is super lazy, but I'll just take the YAML and
        # convert it over to JSON
        yamldict = yaml.safe_load(self.yaml)
        # datetime doesn't convert to JSON, :( fix it here
        if 'issued_date' in yamldict:
            yamldict['issued_date'] = yamldict['issued_date'].strftime('%Y-%m-%d %H:%M:%S')
        if 'update_date' in yamldict:
            yamldict['update_date'] = yamldict['update_date'].strftime('%Y-%m-%d %H:%M:%S')

        return json.dumps(yamldict)

    @json.setter
    def json(self, jsonstring):
        '''Set the object from a JSON string, using @property'''
        # this is super lazy, but I'll just take the JSON and
        # convert it over to YAML
        logging.debug("Trying to set update from json(via yaml): %s", jsonstring)
        self.yaml = yaml.safe_dump(json.loads(jsonstring))

        return self

