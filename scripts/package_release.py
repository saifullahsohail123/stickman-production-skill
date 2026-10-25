"""Audit public source and build a stable source-only ZIP; no publishing."""
import argparse,hashlib,io,json,re,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.venv','work','dist','__pycache__'}
SPECIAL={'LICENSE','VERSION','.gitignore'}
EXTENSIONS={'.py','.md','.json','.yaml','.yml','.txt'}

def sources():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in SKIP for x in p.relative_to(ROOT).parts)
                  and not p.name.endswith(('.local.json','.pyc','.log')))

def audit(files):
    issues=[]
    for path in files:
        name=path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in EXTENSIONS and path.name not in SPECIAL:issues.append(name+': unexpected non-source file');continue
        text=path.read_text(encoding='utf-8')
        patterns=[r'[A-Za-z]:[\\/](?:Users|Self-learning-Projects)[\\/]',r'sk-[A-Za-z0-9]{24,}',
                  r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b']
        for pattern in patterns:
            if re.search(pattern,text,re.I):issues.append(name+': possible private identifier/path/key')
    for required in ['README.md','LICENSE','VERSION','skills/stickman-production/SKILL.md']:
        if not (ROOT/required).exists():issues.append('Missing '+required)
    if issues:raise ValueError('\n'.join(issues))

def build(check=False):
    files=sources();audit(files);version=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
    manifest={'version':version,'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    if check:print(f'Public source audit passed: {len(files)} files');return
    blob=io.BytesIO()
    with zipfile.ZipFile(blob,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,payload in [(p.relative_to(ROOT).as_posix(),p.read_bytes()) for p in files]+[('release-manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())]:
            info=zipfile.ZipInfo('stickman-production-skill/'+name,date_time=(2026,10,25,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            archive.writestr(info,payload,compresslevel=9)
    dist=ROOT/'dist';dist.mkdir(exist_ok=True);target=dist/f'stickman-production-skill-{version}.zip';payload=blob.getvalue()
    if target.exists() and target.read_bytes()!=payload:raise FileExistsError('Existing release differs; increment VERSION')
    target.write_bytes(payload);print(target);print(hashlib.sha256(payload).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');build(parser.parse_args().check)
