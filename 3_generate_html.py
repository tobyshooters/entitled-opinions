import os
import re
import json
import unicodedata
from collections import defaultdict


eps = json.load(open("opinions.json", "r"))

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

<p>
    <a href="./index2.html">index of word occurences</a></div>
</p>

<table>
"""

references = defaultdict(set)

for ts, ep in eps.items():

    txf = f"./episodes/{ts}/transcript-medium.vtt"

    if not os.path.exists(txf):
        txf = f"./episodes/{ts}/transcript-tiny.vtt"
        if not os.path.exists(txf):
            continue

    title = unicodedata.normalize("NFKD", ep["title"])
    txt = unicodedata.normalize("NFKD", open(txf, "r").read())

    print(f"Processing {title}")

    toc += f"""
<tr>
    <td>{ep["date"]}</td>
    <td><a href="./episodes/{ts}">{title}</a></td>
</tr>
"""

    og_title = f"{title}—Entitled Opinions {ep['date']}"

    episode = header + f"""
<head>
    <title>{og_title}</title>
    <meta property="og:title" content="{og_title}" />
    <meta property="og:description" content="{ep['description']}" />
    <meta property="og:url" content="https://cristobal.nfshost.com/entitled-opinions/episodes/{ts}" />
    <meta property="og:image" content="{ep['image']}" />
</head>

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
    <td id="{seek}" style="width: 100px;">
        <a href="javascript:;" onclick="const el = document.getElementById('a'); el.currentTime = {seek}; el.play(); window.location.hash = {seek}">
            {m[0]}
        </a>
    </td>
    <td style="width: 500px;">
        <div>
            {text}
        </div>
    </td>
</tr>
        """

        simple = text.encode("ascii", "ignore").decode("ascii").lower()
        for word in simple.split(" "):

            word = word.strip(" .,;:-—!?\"\'()[]{}")
            for suffix in ["'s", "n't", "'re", "'ve", "'ll"]:
                if word[-len(suffix):] == suffix:
                    word = word[-len(suffix):]

            if word and len(word) > 3:
                references[word].add(ts)

    episode += """
</table>
    """

    with open(f"./episodes/{ts}/index.html", "w") as f:
        f.write(episode)


toc += """
</table>

<br/>

<div>pirated, with care and respect</div>
<div>
    <a href="./opinions.json">metedata</a>
    <a href="./opinions.xml">xml</a>
    <a href="https://github.com/tobyshooters/entitled-opinions">source code</a>
</div>

"""

with open("./index.html", "w") as f:
    f.write(toc)


def chart(count, step=16, largest=200):
    count = max(2, int(100 * count / largest))
    bar_chunks, remainder = divmod(int(count * 8 / step), 8)
    bar = '█' * bar_chunks
    if remainder > 0:
        bar += chr(ord('█') + (8 - remainder))
    return bar


def build_table(html, counts):
    html += """
    <table style="font-family: monospace; white-space: nowrap;">
    <tr> <th>word</th> <th>#</th> <th>episodes</th> </tr>
    """

    largest = max(len(eps) for _, eps in counts)

    all_eps = set()
    for _, word_eps in counts:
        all_eps.update(word_eps)
    all_eps = sorted(list(all_eps))

    for word, word_eps in counts:
        N = len(word_eps)
        bar = chart(N, largest=largest)

        html += f"""<tr><td>{word}</td><td>{bar} {N}</td><td style="font-family: sans-serif">"""

        for ep in all_eps:
            if ep in word_eps:
                href = f"./episodes/{ep}"
                html += f"""<a style="text-decoration: none; background-color: blue;" href="{href}">·</a>"""
            else:
                html += "·"

        html += "</tr>"
    html += "</table>"
    return html


print("Building index tables")

# prune words!
alphabetical = sorted(references.items(), key=lambda kv: kv[0])
ignored_words = open("10000-most-common-words.txt", "r").read().split("\n")

merged = defaultdict(list)
prev_word = alphabetical[0][0]
for word, eps in alphabetical:
    if word in ignored_words:
        continue
    for postfix in ["s", "d", "ly", "ally", "n", "ed", "ing", "r"]:
        if word == prev_word + postfix:
            word = prev_word
            break
    merged[word].extend(eps)
    prev_word = word

alphabetical = merged.items()
by_counts = sorted(alphabetical, key=lambda kv: -len(kv[1]))

search = header + """
<div style="margin-bottom: 22px;">
    <a href="../..">table of contents</a>
</div>

<div style="margin-bottom: 22px;">
    index of word occurences
</div>

<div style="margin-bottom: 22px;">
    <span id="counts"></span>
    sorted by frequency</br>
    <a href="#alphabetical">sort alphabetically</a>
</div>
"""

search = build_table(search, by_counts)

search += """
<div style="margin: 22px 0px;">
    <span id="alphabetical"></span>
    sorted alphabetically</br>
    <a href="#counts">sort by frequency</a>
</div>
"""
search = build_table(search, alphabetical)

search += "</div>"


with open("./index2.html", "w") as f:
    f.write(search)
