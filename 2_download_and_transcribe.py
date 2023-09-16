import os
import subprocess
import json
import requests
import unicodedata

wcpp = "../whisper.cpp"
model = "medium"
weights = "ggml-tiny.en.bin"

def run(p):
    subprocess.run(p.split(" "))


eps = json.load(open("entitled-opinions.json", "r"))
for ts, ep in eps.items():
    t = unicodedata.normalize("NFKD", ep["title"])

    txf = f"./episodes/{ts}/transcript-{model}"
    if os.path.exists(txf + ".vtt"):
        print("Skipping", t)
        continue

    os.makedirs(f"./episodes/{ts}", exist_ok=True)

    src = f'./episodes/{ts}/audio.mp3'
    if not os.path.exists(src):
        print("Requesting", t)
        audio = requests.get(ep["url"])

        print("Writing", t)
        with open(src, 'wb') as f:
            f.write(audio.content)

    tgt = src.replace('mp3', 'wav')
    if not os.path.exists(tgt):
        print("Re-encoding", t)
        run(f"ffmpeg -y -i {src} -acodec pcm_s16le -ac 1 -ar 16000 {tgt}")

    print("Transcribing", t)
    run(f"{wcpp}/main -f {tgt} --model {wcpp}/models/ggml-{model}.en.bin --output-vtt --output-file {txf}")
