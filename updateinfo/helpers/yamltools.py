#!/usr/bin/env python
#pylint: disable=line-too-long
'''
    A set of helper functions for dealing with PyYAML
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
from __future__ import print_function

import yaml

def yaml_represent_ordereddict(dump, tag, mapping, flow_style=None):
    '''
        For a YAML dump of an OrderedDict
    '''
    value = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)

    if dump.alias_key is not None:
        dump.represented_objects[dump.alias_key] = node

    for item_key, item_value in mapping.items():
        node_key = dump.represent_data(item_key)
        node_value = dump.represent_data(item_value)
        value.append((node_key, node_value))

    return node

if __name__ == '__main__':  # pragma: no cover
    from collections import OrderedDict

    TEST = OrderedDict()
    TEST['x'] = 'x'
    TEST['d'] = 'd'
    TEST['a'] = 'a'
    TEST['c'] = 'c'
    TEST['aa'] = 'aa'
    TEST['ab'] = 'ab'

    yaml.SafeDumper.add_representer(OrderedDict, lambda dumper, value: yaml_represent_ordereddict(dumper, u'tag:yaml.org,2002:map', value))
    print(yaml.safe_dump(TEST))

