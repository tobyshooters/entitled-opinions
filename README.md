# How it works

Download the Entitled Opinions XML and save it as `entitled-opinions.xml`

`1_parse_xml.py` will extract the key information from the XML using the Python
built-in `html.minidom` and save the relevant data at `entitled-opinions.json`.

`2_download_and_transcribe.py` will read the saved json and download the audio
files from the host specified in the podcast XML. It will then convert the
`.mp3` files into 16 kHz `.wav` to be processed with `whisper-cpp`, which must
be installed somewhere in system.

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
index (`index2.html`).

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

This can be previewed locally by running a web-server, e.g.
`python3 -m http.server`

Alternatively, it can be hosted on a web provider, e.g. nearlyfreespeech.net
