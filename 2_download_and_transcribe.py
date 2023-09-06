import os
import subprocess
import json
import requests
import unicodedata

def run(p):
    subprocess.run(p.split(" "))


eps = json.load(open("entitled-opinions.json", "r"))
for ts, ep in eps.items():
    t = unicodedata.normalize("NFKD", ep["title"])

    txf = f"./episodes/{ts}/transcript-tiny"
    if os.path.exists(txf + ".vtt"):
        print("Skipping", t)
        continue

    os.makedirs(f"./episodes/{ts}", exist_ok=True)

    print("Requesting", t)
    audio = requests.get(ep["url"])

    print("Writing", t)
    src = f'./episodes/{ts}/audio.mp3'
    with open(src, 'wb') as f:
        f.write(audio.content)

    print("Re-encoding", t)
    tgt = src.replace('mp3', 'wav')
    run(f"ffmpeg -y -i {src} -acodec pcm_s16le -ac 1 -ar 16000 {tgt}")

    print("Transcribing", t)
    wcpp = "../whisper.cpp"
    run(f"{wcpp}/main -f {tgt} --model {wcpp}/models/ggml-tiny.en.bin --output-vtt --output-file {txf}")
