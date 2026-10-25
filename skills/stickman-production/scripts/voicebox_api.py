"""Voicebox adapter with request provenance and bounded generation waits."""
import json,time,urllib.request
from core import inside,read_json,write_json

class Voicebox:
    def __init__(self,url,timeout=90):self.url=url.rstrip('/');self.timeout=timeout
    def json(self,route,data=None):
        request=urllib.request.Request(self.url+route,data=None if data is None else json.dumps(data).encode('utf-8'),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=self.timeout) as response:return json.load(response)
    def generate(self,root,line,voice):
        if not voice.get('profile_id'):raise ValueError('Select a real profile in the local config before generation')
        stem=line['id']
        if not stem.replace('-','').isalnum():raise ValueError('Use alphanumeric/hyphen line IDs')
        folder=inside(root,'audio');folder.mkdir(parents=True,exist_ok=True)
        request=dict(profile_id=voice['profile_id'],engine=voice['engine'],language=voice['language'],text=line['text'],
            seed=line.get('seed',42),personality=False,normalize=True)
        request_path=folder/(stem+'-request.json');target=folder/(stem+'.wav');job_path=folder/(stem+'-job.json')
        if request_path.exists() and read_json(request_path)!=request:raise FileExistsError('Take changed; create a new take ID or revision')
        if target.exists():return target
        write_json(request_path,request)
        job=read_json(job_path) if job_path.exists() else self.json('/generate',request)
        write_json(job_path,job);generation_id=job.get('id') or job.get('generation_id')
        if not generation_id:raise RuntimeError('Voicebox did not return a generation ID')
        deadline=time.monotonic()+self.timeout
        while time.monotonic()<deadline:
            history=self.json('/history/'+generation_id);write_json(folder/(stem+'-history.json'),history)
            state=history.get('status')
            if state=='completed':
                with urllib.request.urlopen(self.url+'/audio/'+generation_id,timeout=self.timeout) as response:payload=response.read()
                if payload[:4]!=b'RIFF':raise ValueError('Expected a WAV response')
                target.write_bytes(payload);return target
            if state in ['failed','cancelled']:raise RuntimeError(history)
            time.sleep(1)
        raise TimeoutError('Generation deadline reached; job preserved for later inspection')
