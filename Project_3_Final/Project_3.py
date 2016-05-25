import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint
import operator
import re

filename = 'sydney_sample.osm'
top_20keys = []
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# ------------------------------------------
#		Main
# ------------------------------------------

def main():
    if False:
        '''find out the frequency for all tags in file'''
        print_all_tags(filename)

    if False:
        '''list out the top 20 keys with the most frequency in each tag'''
        print_top_keys(filename)

    if False:
        '''find the first 20 unique values for each top key'''
        MAX_COUNT = 20
        top_keys = ['highway', 'source', 'name', 'building', 'created_by', 'oneway', 'maxspeed',
                    'addr:street', 'amenity', 'surface', 'foot', 'leisure', 'layer', 'bicycle',
                    'ref', 'source:name', 'service', 'railway', 'landuse', 'operator']

        pprint(key_values(top_keys, MAX_COUNT))

    if False:
        '''correct maxspeed values'''
        improve_maxspeed(filename)

    if True:
        '''correct street names'''
        improve_street_names(filename)


# ------------------------------------------
#	        Functions
# ------------------------------------------


def count_tags(filename):
    ''' Count total number of each tag '''
    osm_file = open(filename, "r")
    tag_types = {}

    for event, elem in ET.iterparse(filename):

        if elem.tag not in tag_types:
            tag_types[elem.tag] = 1
        else:
            tag_types[elem.tag] += 1

    return tag_types


def count_keys(filename):
    ''' Count total number of each key '''
    osm_file = open(filename, "r")
    key_types = {}

    for event, elem in ET.iterparse(filename):
        # only parse all key name under tag element
        if elem.tag == "tag" and 'k' in elem.attrib:
            v = elem.get('k')
            if v not in key_types:
                key_types[v] = 1
            else:
                key_types[v] += 1

    return key_types


'''print all tag function'''
def print_all_tags(filename):
    tags = count_tags(filename)
    pprint(tags)


'''collect and print top keys from each tag'''
def print_top_keys(filename, keyNum=20):
    keys = count_keys(filename)

    # sort keys
    sorted_keys = sorted(keys.items(), key=operator.itemgetter(1))
    sorted_keys.reverse()

    # print top 20 keys
    for i in range(0, keyNum):
        top_20keys.append
        print sorted_keys[i][0]


def key_values(top_keys, Max):
    result = {k: [] for k in top_keys}
    # parse file
    osm_file = open(filename, "r")

    for event, elem in ET.iterparse(filename):

        # only parse all key name under tag element
        if elem.tag == "tag" and 'k' in elem.attrib and 'v' in elem.attrib:
            k_val = elem.get('k')
            v_val = elem.get('v')
            # find 20 unique values of the key
            if k_val in top_keys and len(result[k_val]) < Max and v_val not in result[k_val]:
                result[k_val].append(v_val)
    return result


"""Max Speed"""
def is_maxspeed_name(elem):
    return (elem.attrib['k'] == "maxspeed")


def update_speed(speed):

    """
    Only accept values if it is integer, otherwise convert string to integer base on its value,
    ignore undefined string and special character string
    """
    try:
        int(speed)
    except:
        if speed == 'signals':
            # default value for signal sign will be 80
            new_sp = 80
            print speed, "=>", new_sp
        elif 'knots' in speed or 'mph' in speed:
            # split string and convert speed number to integer value
            new_sp = int(speed.split()[0]) * 2
            print speed, "=>", new_sp
        else:
            # ignore other values, e.g. ";" and 'undefined'
            pass


def improve_maxspeed(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_maxspeed_name(tag):
                    val = tag.attrib['v']
                    update_speed(val)

    osm_file.close()


"""Update Satreet Name"""
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Highway",
            "Place", "Parade", "Square", "Lane", "Road", "Trail",
            "Parkway", "Commons", "Row", "East", "West", "Esplanade", "Crescent"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "st": "Street",
           "St.": "Street",
           "Ave.": "Avenue",
           "Av.": "Avenue",
           "Hwy": "Highway",
           "Ave": "Avenue",
           "Rd.": "Road",
           "Rd": "Road"
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            # remove street type that is equal to itself
            if street_name != street_type:
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
    p = name.split()
    if p[-1] in mapping:
        p[-1] = mapping[p[-1]]
        name = " ".join(p)

    return name


def improve_street_names(filename):
    st_types = audit(filename)

    pprint(dict(st_types))
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


if __name__ == '__main__':
    main()
