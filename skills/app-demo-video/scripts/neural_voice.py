# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["kokoro-onnx==0.4.9"]
# ///
"""Generate all narration takes with a single, local Kokoro session."""
import json, sys, wave
from pathlib import Path
import numpy as np
from kokoro_onnx import Kokoro
def main(job):
    data=json.loads(job.read_text()); s=data['settings']
    assets=Path(s.get('model_dir','~/.local/share/argstack/voice-models/kokoro-v1')).expanduser()
    model=Kokoro(str(assets/'kokoro-v1.0.int8.onnx'),str(assets/'voices-v1.0.bin'))
    speed=float(s.get('speed',1.0))
    if not .8<=speed<=1.2: raise ValueError('Use speed 0.8–1.2 and write lines that fit the scene.')
    for i,text in enumerate(data['lines'],1):
        if not text.strip():continue
        audio,rate=model.create(text,voice=s.get('voice','af_heart'),speed=speed,lang=s.get('lang','en-us'))
        if not len(audio) or not np.isfinite(audio).all():raise ValueError(f'Invalid audio in shot {i}')
        with wave.open(str(job.parent/f'line-{i}.wav'),'wb') as w:
            w.setparams((1,2,rate,0,'NONE','not compressed'));w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
if __name__=='__main__':main(Path(sys.argv[1]))
