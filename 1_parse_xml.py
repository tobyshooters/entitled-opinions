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
    els = node.getElementsByTagName(field)
    return getText(els[0].childNodes)


def parseTime(s):
    """
    Try hard to parse anything in the XML. A little nasty.
    """
    s = " ".join(s.split(" ")[1:5])
    return datetime.datetime.strptime(s, '%d %b %Y %H:%M:%S')


doc = xml.dom.minidom.parse("opinions.xml")

output = {}
for e in doc.getElementsByTagName("item"):
    t = parseTime(parseField(e, "pubDate"))
    ts = t.strftime("%s")[:5]
        
    imgs = e.getElementsByTagName("itunes:image")
    image_url = imgs[0].getAttribute("href") if imgs else ""


    output[ts] = {
        "title": parseField(e, "title"),
        "description": parseField(e, "description"),
        "url": e.getElementsByTagName("enclosure")[0].getAttribute("url"),
        "date": t.strftime("%m/%d/%Y"),
        "image":  image_url
    }


with open("opinions.json", "w") as f:
    json.dump(output, f, indent=2)
