import xml.etree.ElementTree as ET
import json

# I apologize to anyone who ends up reading this awful code.
def parse(xml):
    root = ET.fromstring(xml)
    namespaces = {"torznab": "http://torznab.com/schemas/2015/feed"}
    items = []
    for item in root.findall("./channel/item"):
        item_dict = {
            "title": ET.tostring(item.find("title"), encoding="utf8").decode("utf8"),
            "link": ET.tostring(item.find("guid"), encoding="utf8").decode("utf8"),
            "indexer": ET.tostring(item.find("jackettindexer"), encoding="utf8").decode("utf8"),
            "commentsLink": ET.tostring(item.find("comments"), encoding="utf8").decode("utf8"),
            "date": ET.tostring(item.find("pubDate"), encoding="utf8").decode("utf8"),
            "size": ET.tostring(item.find("size"), encoding="utf8").decode("utf8"),
            "magnet": ET.tostring(item.find("link"), encoding="utf8").decode("utf8"),
            "seeders": 0,
            "peers": 0,
        }
        # Add annoying torznab stuff
        torznab_stuff = item.findall("torznab:attr", namespaces=namespaces)
        for attr in torznab_stuff:
            if attr.attrib["name"] == "seeders":
                item_dict["seeders"] = int(attr.attrib["value"])
            elif attr.attrib["name"] == "peers":
                item_dict["peers"] = int(attr.attrib["value"])
        items.append(item_dict)
    
    # Probably very inefficient cleaning up of strings
    for item in items:
        for key in item:
            # Make sure it only runs if string
            if isinstance(item[key], str):
                # Remove extra xml description line
                item[key] = item[key][38:]
                # Remove start tag
                item[key] = item[key][item[key].find(">"):]
                item[key] = item[key][1:]
                # Remove end tag
                item[key] = item[key][:item[key].find("<")]
            # Make the size an integer or it will annoy me
            if key == "size":
                item[key] = int(item[key])
    
    # return the JSON
    return items
