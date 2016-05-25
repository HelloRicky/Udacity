#Initialisation
import xml.etree.cElementTree as ET
from collections import defaultdict
import cerberus
import codecs
import schema
import pprint
import csv
import re

filename = "sydney_sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#------------------
#Main
#------------------

def main():

    # Iterative Parsing
    if False:
        pprint.pprint(count_tags(filename))

    # Tag Types
    if False:
        pprint.pprint(process_map_key_types(filename))

    # Exploring Users
    if False:
        pprint.pprint(process_map_users(filename))

    # Improving Street Names
    if False:
        improve_street_names(filename)

    # Preparing for Database
    if False:
        process_map_database(filename)

#------------------
#Functions
#------------------

# find out total number for each tag
def count_tags(filename):
    osm_file = open(filename, "r")
    tag_types = {}

    for event, element in ET.iterparse(filename):
        if element.tag not in tag_types:
            tag_types[element.tag] = 1
        else:
            tag_types[element.tag] += 1
    return tag_types

def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']

        if lower.search(k):
            keys["lower"] += 1
        elif lower_colon.search(k):
            keys["lower_colon"] += 1
        elif problemchars.search(k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
        pass

    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
# Improving Street Names
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(element):
    return (element.attrib['k'] == "addr:street")

def audit(filename):
    osm_file = open(filename, "r")
    street_types = defaultdict(set)
    postcode_value = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode_value(tag):
                    print tag.attrib['v']
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

# Improving Postcode value
def is_postcode_value(element):
    return (element.attrib['k'] == "addr:postcode")

if False:
    import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

    OSM_FILE = filename  # Replace this with your osm file
    SAMPLE_FILE = "sample.osm"

    k = 25 # Parameter: take every k-th top level element

    def get_element(osm_file, tags=('node', 'way', 'relation')):
        """Yield element if it is the right type of tag

        Reference:
        http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
        """
        context = iter(ET.iterparse(osm_file, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()


    with open(SAMPLE_FILE, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write('</osm>')
#--------------------------#
# Iterative Parsing
#--------------------------#
def count_tags(filename):
        # YOUR CODE HERE
        osm_file = open(filename, "r")
        tag_types = {}

        for event, elem in ET.iterparse(filename):

            if elem.tag not in tag_types:
                tag_types[elem.tag] = 1
            else:
                tag_types[elem.tag] +=1

        return tag_types

#--------------------------#
# Tag Types
#--------------------------#
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        k = element.attrib['k']

        if lower.search(k):
            keys["lower"] += 1
        elif lower_colon.search(k):
            keys["lower_colon"] += 1
        elif problemchars.search(k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
        pass

    return keys

def process_map_key_types(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

#--------------------------#
# Exploring Users
#--------------------------#
def process_map_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            ids = element.attrib['uid']
            if ids not in users:
                users.add(ids)
        except:
            pass

    return users


#--------------------------#
# Improving Street Names
#--------------------------#
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Highway", "Place", "Parade", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "st": "Street",
            "St.": "Street",
            "Ave.": "Avenue",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping):

    # YOUR CODE HERE
    p = name.split()
    if p[-1] in mapping:
        p[-1] = mapping[p[-1]]
        name = " ".join(p)

    return name

def improve_street_names(filename):
    st_types = audit(filename)

    pprint.pprint(dict(st_types))
    show = 1
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            if show:
                print "--------------------------"
                print "After update names"
                print "--------------------------"
                show = 0
            print name, "=>", better_name

#--------------------------#
# Preparing for Database
#--------------------------#

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""



    if validator.validate(element, schema) is not True:
        print element

        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        for f in element.attrib:
            if f in NODE_FIELDS:
                node_attribs[f] = element.attrib[f]
        for tag in element.iter("tag"):
            key = tag.attrib['k']
            m = PROBLEMCHARS.search(key)
            if m == None:
                detail = {}

                detail['id'] = node_attribs['id']
                detail['value'] = tag.attrib['v']
                if LOWER_COLON.search(key):
                    s = key.split(":")
                    detail['type'] = s[0]
                    detail['key'] = ":".join(s[1:])
                else:
                    detail['key'] = key
                    detail['type'] = default_tag_type


                tags.append(detail)

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':

        for f in element.attrib:
            if f in WAY_FIELDS:
                way_attribs[f] = element.attrib[f]
        for tag in element.iter("tag"):
            key = tag.attrib['k']
            m = PROBLEMCHARS.search(key)
            if m == None:
                detail = {}
                detail['id'] = way_attribs['id']
                detail['value'] = tag.attrib['v']
                if LOWER_COLON.search(key):
                    s = key.split(":")
                    detail['type'] = s[0]
                    detail['key'] = ":".join(s[1:])
                else:
                    detail['key'] = key
                    detail['type'] = default_tag_type


                tags.append(detail)
        pos = 0
        for tag in element.iter("nd"):
            ref = {}

            ref['id'] = way_attribs['id']
            ref['node_id'] = tag.attrib['ref']
            ref['position'] = pos
            pos += 1
            way_nodes.append(ref)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

def process_map_database(file_in, validate = True):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    main()