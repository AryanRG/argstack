# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow==12.0.0"]
# ///
"""Render a JSON edit list of recorded app clips. Requires ffmpeg and ffprobe."""
import argparse, json, math, shutil, subprocess, tempfile
from pathlib import Path
from voiceover import generate
from PIL import Image, ImageDraw, ImageFont
def ff(*args):
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y',*map(str,args)],check=True)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-of','json','-show_streams','-show_format',path]))
def font(size,heavy=False):
    names=(['/System/Library/Fonts/Supplemental/Arial Bold.ttf','DejaVuSans-Bold.ttf'] if heavy else ['/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf'])
    for name in names:
        try:return ImageFont.truetype(name,size)
        except OSError:pass
    raise ValueError('Install Arial or DejaVu Sans for readable captions')
def drawtext(d,xy,text,size,color,width,bold=False):
    f=font(size,bold)
    if not text.strip() or '\n' in text or d.textlength(text,font=f)>width:raise ValueError('Shorten this label to fit: '+text)
    d.text(xy,text,font=f,fill=color,anchor='lm')
def timestamp(frames):
    ms=round(frames*1000/30);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
def render(manifest,out):
    m=json.loads(manifest.read_text());shots=m['shots'];base=manifest.parent;out=out.resolve()
    if not shots or len(shots)>30:raise ValueError('Expected 1–30 shots')
    if out.exists():raise ValueError('Choose a new output directory')
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as td:
        tmp=Path(td);deliver=tmp/'delivery';deliver.mkdir();elapsed=0;subs=['WEBVTT',''];frames=[]
        for i,s in enumerate(shots,1):
            clip=(base/s['clip']).resolve();pr=probe(clip)
            if not any(st['codec_type']=='video' for st in pr['streams']):raise ValueError('No video: '+str(clip))
            start=float(s.get('start',0));n=round(float(s['duration'])*30)
            if not math.isfinite(start) or start<0 or n<30 or start+n/30>float(pr['format']['duration'])+0.03:raise ValueError(f'Shot {i} outside footage')
            if len(s['caption'].split())/ (n/30)>3.5:raise ValueError(f'Shot {i}: caption needs more reading time')
            bg=Image.new('RGB',(1920,1080),'#172622');d=ImageDraw.Draw(bg)
            drawtext(d,(96,40),m['brand'],28,'#ebf2df',650,True)
            drawtext(d,(840,40),m['title'],24,'#d8dfcf',840)
            drawtext(d,(1720,40),f'{i:02} / {len(shots):02}',21,'#d6e79e',175)
            d.rounded_rectangle((91,79,1829,953),radius=4,fill='#899586')
            drawtext(d,(96,986),s['label'].upper(),20,'#d6e79e',1730,True)
            drawtext(d,(96,1030),s['caption'],39,'#fffaf0',1730)
            d.rectangle((0,1073,1919,1079),fill='#394d43');d.rectangle((0,1073,round(1919*i/len(shots)),1079),fill='#c7dd8c')
            bg.save(tmp/'mat.png')
            vf='[1:v]setpts=PTS-STARTPTS,fps=30:start_time=0,scale=1728:864:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1728:864:(ow-iw)/2:(oh-ih)/2:color=0x18251f,setsar=1[v];[0:v][v]overlay=96:84:shortest=1,format=yuv420p'
            seg=tmp/f'seg{i}.mp4'
            ff('-loop','1','-framerate','30','-i',tmp/'mat.png','-ss',start,'-i',clip,'-filter_complex',vf,'-frames:v',n,'-an','-c:v','libx264','-preset','veryfast','-crf','17',seg)
            if int(probe(seg)['streams'][0]['nb_frames'])!=n:raise ValueError(f'Shot {i} is shorter than its edit')
            pic=tmp/f'shot{i}.jpg';ff('-ss',max(0,n/30-0.5),'-i',seg,'-frames:v',1,pic);frames.append(pic)
            subs.extend([timestamp(elapsed)+' --> '+timestamp(elapsed+n),s['caption'],'']);elapsed+=n
        playlist=tmp/'edit.txt';playlist.write_text(''.join(f"file 'seg{i}.mp4'\n" for i in range(1,len(shots)+1)))
        args=['-f','concat','-safe','1','-i',playlist]
        if 'voiceover' in m and m.get('narration'): raise ValueError('Choose generated voiceover or supplied narration, not both')
        if 'voiceover' in m or m.get('narration'):
            audio=generate(shots,m['voiceover'],tmp,deliver) if 'voiceover' in m else (base/m['narration']).resolve()
            pr=probe(audio)
            if not any(st['codec_type']=='audio' for st in pr['streams']) or float(pr['format']['duration'])>elapsed/30+.03:raise ValueError('Narration missing audio or exceeds edit duration')
            args+=['-i',audio,'-map','0:v','-map','1:a:0','-c:a','aac','-b:a','160k']
        ff(*args,'-c:v','copy','-movflags','+faststart',deliver/'demo.mp4')
        (deliver/'captions.vtt').write_text('\n'.join(subs)+'\n');shutil.copyfile(frames[-1],deliver/'poster.jpg')
        sheet=Image.new('RGB',(480*min(len(frames),3),270*math.ceil(len(frames)/3)),'#172622')
        for j,p in enumerate(frames):
            with Image.open(p) as img:sheet.paste(img.resize((480,270),Image.Resampling.LANCZOS),((j%3)*480,(j//3)*270))
        sheet.save(deliver/'contact-sheet.jpg',quality=95);deliver.rename(out)
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('manifest',type=Path);a.add_argument('output',type=Path);args=a.parse_args();render(args.manifest.resolve(),args.output)
