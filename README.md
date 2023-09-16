# Entitled Opinions archive

Browse at [cristobal.nfshost.com/entitled-opinions](https://cristobal.nfshost.com/entitled-opinions)


## How to replicate

Download the Entitled Opinions podcast RSS feed [here](https://web.stanford.edu/dept/fren-ital/opinions/podcast/opinions.xml)
and save it as `entitled-opinions.xml`

`1_parse_xml.py` will extract the key information from the XML using the Python
built-in `html.minidom` and save it as `entitled-opinions.json`.

`2_download_and_transcribe.py` will read the saved json and download the audio
files for each episode. It will then convert the `.mp3` files into 16 kHz
`.wav` to be processed with `whisper-cpp`.

`whisper-cpp` must be installed somewhere in system. The path to the binary is
hard-coded in the python file above.  The fastest and lowest quality model was
used, though higher quality can be done by changing the model size and being
patient.

This generates a local file structure with the episode transcripts. The
recording Unix timestamp is used as a unique identifier for each episode.

```
├── 1_parse_xml.py
├── 2_download_and_transcribe.py
├── 3_generate_html.py
│
├── entitled-opinions.xml
├── entitled-opinions.json
│
└── episodes
    ├── 1126670400
    │   ├── audio.mp3
    │   ├── audio.wav
    │   └── transcript-tiny.vtt
    ├── 1126929600
    │   ├── audio.mp3
```

`3_generate_html.py` then reads this file structure and creates an index.html
file for each episode, as well as an homepage (`index.html`) and reference
index (`index2.html`). For this reference index, we ignore common words present
in `10000-most-common-words.txt`.

```
├── index.html
├── index2.html
└── episodes
    ├── 1126670400
    │   ├── index.html
    │   ├── audio.mp3
    │   ├── audio.wav
    │   └── transcript-tiny.vtt
    ├── 1126929600
    │   ├── index.html
```

The output can be previewed locally by running a web-server, e.g.
`python3 -m http.server`

Alternatively, it can be hosted on a web provider, e.g.
[Nearly Free Speech](https://nearlyfreespeech.net)
