"""Portable timing, manifest and delivery primitives; Python standard library."""
import hashlib,json,math,re
from pathlib import Path

def read_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def inside(root,relative):
    root=Path(root).resolve();path=(root/relative).resolve()
    if not path.is_relative_to(root):raise ValueError('Media/output path escapes the episode workspace')
    return path

def validate(data):
    if data.get('schema_version')!=1:raise ValueError('Unsupported episode schema version')
    identity=data['identity'];fmt=data['format']
    for key in ['number','version']:
        if type(identity[key]) is not int or identity[key]<1:raise ValueError('Identity numbers must be positive integers')
    for key in ['slug','language']:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',identity[key]):raise ValueError('Invalid slug/language')
    for key in ['width','height','fps','duration_frames']:
        if type(fmt[key]) is not int or fmt[key]<=0:raise ValueError('Format values must be positive integers')
    cursor=0;ids=set()
    for shot in data['shots']:
        if shot['id'] in ids:raise ValueError('Duplicate shot ID')
        ids.add(shot['id'])
        if type(shot['start_frame']) is not int or type(shot['end_frame']) is not int:raise ValueError('Cuts require integer frame bounds')
        if shot['start_frame']!=cursor or shot['end_frame']<=cursor:raise ValueError('Picture shots must cover consecutive frames')
        cursor=shot['end_frame']
    if cursor!=fmt['duration_frames']:raise ValueError('Picture coverage differs from duration')
    known=set(data.get('cast',{}));line_ids=set()
    for line in data.get('lines',[]):
        if line['id'] in line_ids or line['speaker'] not in known:raise ValueError('Invalid line ID/speaker')
        line_ids.add(line['id'])
        if not line['text'].strip():raise ValueError('Empty dialogue')
    for cue in data.get('captions',[]):
        if not 0<=cue['start']<cue['end']<=cursor/fmt['fps']+.0001:raise ValueError('Invalid caption bounds')
    return data

def delivery_name(data):
    i=data['identity'];return f'{i["number"]:04}_{i["slug"]}_{i["language"]}_v{i["version"]:02}.mp4'

def clock(takes,lead=0.0,tail=.5):
    """Actual take durations plus deliberate gaps, never implicit voice speed-up."""
    if not all(math.isfinite(t) and t>=0 for t in [lead,tail]):raise ValueError('Invalid lead/tail')
    cursor=lead;lines=[]
    for take in takes:
        duration=float(take['duration']);gap=float(take.get('gap_after',.25))
        if not math.isfinite(duration) or duration<=0 or not math.isfinite(gap) or gap<0:raise ValueError('Invalid duration or gap')
        lines.append(dict(take,start=cursor,end=cursor+duration));cursor+=duration+gap
    end=lines[-1]['end'] if lines else lead
    return {'lines':lines,'duration':end+tail,'speed':1}

class TimeMap:
    def __init__(self,points):
        self.points=[tuple(map(float,p)) for p in points]
        if len(self.points)<2:raise ValueError('Two anchors required')
        for a,b in zip(self.points,self.points[1:]):
            if not all(math.isfinite(x) for x in a+b) or not(a[0]<b[0] and a[1]<b[1]):raise ValueError('Both clocks must increase strictly')
    def at(self,t,inverse=False):
        p=[(y,x) for x,y in self.points] if inverse else self.points
        if not p[0][0]<=t<=p[-1][0]:raise ValueError('Time outside anchors')
        for (a,x),(b,y) in zip(p,p[1:]):
            if a<=t<=b:return x+(t-a)/(b-a)*(y-x)
        raise ValueError('Unmapped time')
    def cut_frames(self,seconds,fps):
        result=[round(self.at(t)*fps) for t in seconds]
        if any(a>=b for a,b in zip(result,result[1:])):raise ValueError('Retiming collapsed a picture shot; re-plan cuts')
        return result

def sha256(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def archive(source,folder,data):
    """Idempotent delivery; a changed export must get a new revision."""
    import shutil
    source=Path(source);folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    target=folder/delivery_name(data);digest=sha256(source)
    if target.exists() and sha256(target)!=digest:raise FileExistsError('Preserve delivery; increment its language revision')
    registry=folder/'index.json';items=read_json(registry) if registry.exists() else []
    key=lambda q:(q['number'],q.get('language','en'),q['version'])
    entry=dict(data['identity'],file=target.name,sha256=digest,approved_by_user=False)
    for old in items:
        if key(old)==key(entry) and (old['file']!=target.name or old['sha256']!=digest):raise FileExistsError('Delivery identity already belongs to another export')
    shutil.copy2(source,target)
    items=[q for q in items if key(q)!=key(entry)]+[entry];write_json(registry,items)
    return target
