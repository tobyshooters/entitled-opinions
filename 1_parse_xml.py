import xml.dom.minidom
import json
import datetime


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def parseField(node, field):
    return getText(e.getElementsByTagName(field)[0].childNodes)


def parseTime(s):
    return datetime.datetime.strptime(s, '%a, %d %b %Y %H:%M:%S +0000')


doc = xml.dom.minidom.parse("entitled-opinions.xml")

output = {}
for e in doc.getElementsByTagName("item"):
    t = parseTime(parseField(e, "pubDate"))
    ts = t.strftime("%s")
    output[ts] = {
        "title": parseField(e, "title"),
        "description": parseField(e, "description"),
        "url": e.getElementsByTagName("enclosure")[0].getAttribute("url"),
        "date": t.strftime("%m/%d/%Y")
    }


with open("entitled-opinions.json", "w") as f:
    json.dump(output, f, indent=2)
