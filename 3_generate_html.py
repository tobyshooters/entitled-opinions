import os
import re
import json
import unicodedata
from collections import defaultdict


eps = json.load(open("opinions.json", "r"))

references = defaultdict(set)
ignored_words = open("10000-most-common-words.txt", "r").read().split("\n")

header = """
<head>
    <meta charset="UTF-8">
</head>

<style> 
    body {
        margin: 22px;
    } 
    th, td {
        padding-right: 11px;
        text-align: left;
        vertical-align: top;
    }
</style>
"""

toc = header + """
<p>
    <a href="https://entitled-opinions.com/">Entitled Opinions</a>
    <br>hosted by Robert Pogue Harrison
    <br>archive by <a href="https://reduct.video">Reduct</a>
</p>

<table>
"""

for ts, ep in eps.items():

    txf = f"./episodes/{ts}/transcript-medium.vtt"

    if not os.path.exists(txf):
        txf = f"./episodes/{ts}/transcript-tiny.vtt"
        if not os.path.exists(txf):
            continue

    title = unicodedata.normalize("NFKD", ep["title"])
    txt = unicodedata.normalize("NFKD", open(txf, "r").read())

    toc += f"""
<tr>
    <td>{ep["date"]}</td>
    <td><a href="./episodes/{ts}">{title}</a></td>
</tr>
"""

    episode = header + f"""
<div>
    <a href="../..">table of contents</a>
</div>
<div style="width: 600px">
    <p>{ep['date']}</p>
    <p>{ep['title']}</p>
    <p><img style="width: 600px" src="{ep['image']}"></img></p>
    <p>{ep['description']}</p>
</div>

<div>
    <a href="./transcript-tiny.vtt">download transcript [vtt]</a>
</div>

<div>
    <audio controls id="a" src="{ep['url']}" style="width: 600px; height: 50px; padding: 22px 0px;"></audio>
</div>

<table>
"""

    for line in txt.split("\n\n"):
        m = re.findall(r"\d\d:\d\d:\d\d.\d\d\d", line)
        if len(m) != 2:
            continue

        text = line.split("\n")[1]

        tss = [int(x) for x in m[0].split(".")[0].split(":")]
        seek = tss[0] * 60 * 60 + tss[1] * 60 + tss[2]

        episode += f"""
<tr>
    <td style="width: 100px;"><a href="javascript:;" onclick="const el = document.getElementById('a'); el.currentTime = {seek}; el.play();">{m[0]}</a></td>
    <td style="width: 500px;"><div>{text}</div></td>
</tr>
        """

        simple = text.encode("ascii", "ignore").decode("ascii").lower()
        for word in simple.split(" "):

            word = word.strip(" .,;:-—!?\"\'()[]{}")
            for suffix in ["'s", "n't", "'re", "'ve", "'ll"]:
                if word[-len(suffix):] == suffix:
                    word = word[-len(suffix):]

            if word and len(word) > 3:
                references[word].add(f"./episodes/{ts}")

    episode += """
</table>
    """

    with open(f"./episodes/{ts}/index.html", "w") as f:
        f.write(episode)


toc += """
</table>

<br/>

<div><a href="./index2.html">transcript index</a></div>
<div><a href="./opinions.json">episode metadata</a></div>
<div><a href="./opinions.xml">podcast xml</a></div>
<div><a href="https://github.com/tobyshooters/entitled-opinions">how it's made</a></div>
"""

with open("./index.html", "w") as f:
    f.write(toc)


def build_table(html, counts):
    html += """
    <table style="font-family: monospace; white-space: nowrap;">
    <tr> <th>word</th> <th>#</th> <th>episodes</th> </tr>
    """
    for word, locs in counts:
        html += f"""<tr><td>{word}</td><td>{len(locs)}</td><td>"""
        for idx, loc in enumerate(locs):
            if idx < 5:
                html += f"""<a href="{loc}">[{idx + 1}]</a>"""
            else:
                html += "..."
                break
        html += "</tr>"
    html += "</table>"
    return html


alphabetical = sorted(references.items(), key=lambda kv: kv[0])

# less words!
merged = defaultdict(set)
prev_word = alphabetical[0][0]
for word, locs in alphabetical:
    if word in ignored_words:
        continue
    for postfix in ["s", "d", "ly", "ally", "n"]:
        if word == prev_word + postfix:
            word = prev_word
            break
    else:
        prev_word = word
    merged[word].update(locs)
alphabetical = merged.items()

by_counts = sorted(alphabetical, key=lambda kv: -len(kv[1]))

search = header + """
<div style="margin-bottom: 22px;">
    <a href="../..">table of contents</a>
</div>
<div style="display: flex; width: 400px;">
"""
search = build_table(search, alphabetical)
search = build_table(search, by_counts)
search += "</div>"


with open("./index2.html", "w") as f:
    f.write(search)
