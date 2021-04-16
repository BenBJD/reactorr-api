import xml.etree.ElementTree as ET
import json

# There MUST be a nicer way to convert xml to json
# Converts the xml results from torznab into nice friendly json


def parse_results(xml):
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


# And again for the indexers
def parse_indexers(xml):
    root = ET.fromstring(xml)
    items = []
    for item in root:
        item_dict = {
            "title": "",
            "categories": []
        }

        # Add categories
        for category in item.findall("./caps/categories/category"):
            item_dict["categories"].append({
                "id": category.attrib["id"],
                "name": category.attrib["name"]
            })
        
        # Add title
        title = ET.tostring(item.find("title"), encoding="utf8").decode("utf8")
        # Remove extra xml description line
        title = title[38:]
        # Remove start tag
        title = title[title.find(">"):]
        title = title[1:]
        # Remove end tag
        title = title[:title.find("<")]
        item_dict["title"] = title
        items.append(item_dict)
    # return the JSON
    return items
