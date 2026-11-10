"""Build shot-timed narration offline using the installed macOS speech engine."""
from pathlib import Path
import json, math, shutil, subprocess, wave

RATE = 48000

def stamp(samples):
    ms = round(samples * 1000 / RATE)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'

def generate(shots, settings, tmp, delivery):
    say = shutil.which('say')
    engine=settings.get('engine','macos')
    if engine not in ('macos','kokoro'): raise ValueError('Unknown voiceover engine')
    if engine=='kokoro':
        job=tmp/'voice-job.json'
        job.write_text(json.dumps({'settings':settings,'lines':[s.get('spoken',s['caption']).strip() for s in shots]}))
        subprocess.run(['uv','run','--python','3.12','--script',str(Path(__file__).with_name('neural_voice.py')),str(job)],check=True)
    if engine=='macos' and not say:
        raise ValueError('Local voiceover requires macOS say; supply a narration audio file on other hosts.')
    voice = settings.get('voice', 'Samantha')
    speed = settings.get('words_per_minute', 170)
    if not isinstance(speed, int) or not 90 <= speed <= 240:
        raise ValueError('words_per_minute must be 90–240')
    transcript = ['WEBVTT', '']; elapsed = 0
    raw = tmp/'voice-track.wav'
    with wave.open(str(raw), 'wb') as track:
        track.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        for i, shot in enumerate(shots, 1):
            budget = round(float(shot['duration']) * 30) * (RATE//30)
            text = shot.get('spoken', shot['caption']).strip()
            if not text:
                track.writeframes(b'\0\0' * budget); elapsed += budget; continue
            delay = float(shot.get('voice_start', 0.28))
            if not math.isfinite(delay) or delay < 0: raise ValueError(f'Invalid voice_start in shot {i}')
            offset = round(delay * RATE)
            line = tmp/f'line-{i}.txt'; line.write_text(text)
            aiff = tmp/f'line-{i}.aiff'
            if engine=='kokoro': aiff=tmp/f'line-{i}.wav'
            else: subprocess.run([say, '-v', voice, '-r', str(speed), '-f', str(line), '-o', str(aiff)],check=True)
            pcm = subprocess.check_output(['ffmpeg','-nostdin','-loglevel','error','-i',str(aiff),
                '-ac','1','-ar',str(RATE),'-c:a','pcm_s16le','-f','s16le','pipe:1'])
            length = len(pcm)//2; tail = budget-offset-length
            if not length or tail < RATE//10:
                raise ValueError(f'Shot {i}: voice needs {delay+length/RATE+.1:.2f}s, shot has {budget/RATE:.2f}s. Shorten the line or extend the footage.')
            track.writeframes(b'\0\0'*offset + pcm + b'\0\0'*tail)
            transcript.extend([stamp(elapsed+offset)+' --> '+stamp(elapsed+offset+length),text,''])
            elapsed += budget
    if len(transcript)==2:raise ValueError('Voiceover enabled but no spoken lines')
    (delivery/'voiceover.vtt').write_text('\n'.join(transcript)+'\n')
    mix = tmp/'voice-mix.wav'
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',str(raw),'-af',
        'loudnorm=I=-16:LRA=7:TP=-1.5','-ar',str(RATE),'-c:a','pcm_s16le',str(mix)],check=True)
    return mix
