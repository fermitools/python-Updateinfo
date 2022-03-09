#!/usr/bin/env python
#pylint: disable=line-too-long
'''
    A set of helper functions for dealing with updateinfo's xml
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

try:
    import xml.etree.cElementTree as xmletree
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as xmletree

def xml_pretty_formatter(elem, level=0, _ws='  '):
    '''
        This function Source:
        http://effbot.org/zone/element-lib.htm#prettyprint
        Copyright EFF
    '''
    i = "\n" + level*_ws
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + _ws
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_pretty_formatter(elem, level+1, _ws)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def get_xsl_pi(xsluri):
    '''
         returns a ProcessingInstruction with the xsl uri
    '''
    if not xsluri:
        raise ValueError('xsluri must not be None')

    xsl_text = 'type="text/xsl" href="' + xsluri + '"'
    xsl_pi = xmletree.ProcessingInstruction('xml-stylesheet', text=xsl_text)

    return xsl_pi

def add_xsd_uri(xsduri, xmlobj):
    '''Add the xsduri to the top element in the xmletree you pass in'''
    if not xsduri:
        raise ValueError('xsluri must not be None')

    xmlobj.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    xmlobj.set('xsi:schemaLocation', xsduri)

    return xmlobj

def add_comment(comment, xmlobj):
    '''Add the listed comment under the top element in the xmletree you pass in'''
    if not comment:
        raise ValueError('comment must not be None')
    if hasattr(comment, 'read'):
        comment = comment.read()

    xmlcomment = xmletree.Comment(comment)
    xmlobj.insert(0, xmlcomment)

    return xmlobj

def validate(xmlstring, xsdfile):
    '''Verify the XML validates against the XSD'''
    from lxml import etree as lxmletree

    xsd_schema = lxmletree.XMLSchema(lxmletree.parse(xsdfile))
    xml_parser = lxmletree.XMLParser(schema=xsd_schema)

    # will raise if something is wrong
    lxmletree.fromstring(xmlstring, xml_parser)

    return True

if __name__ == '__main__':  # pragma: no cover
    import textwrap
    from argparse import ArgumentParser

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__))

    PARSER.add_argument('filename', nargs='+',
                        help='What should be parsed?  List however many')

    PARSER.add_argument('--validate', action='store_true',
                        default=False, help='Should we validate the xml?')

    ARGS = PARSER.parse_args()

    if ARGS.validate:
        for FILE in ARGS.filename:
            _FD = open(FILE, 'r')
            validate(_FD.read(), '/usr/share/doc/python-Updateinfo/updateinfo.xsd')

