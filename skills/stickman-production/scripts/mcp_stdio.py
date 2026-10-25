"""Small sequential stdio MCP adapter; configured command, no shell evaluation."""
import json,os,queue,subprocess,threading,time
from pathlib import Path

class MCP:
    def __init__(self,command,workspace,log_name,timeout=90,extra_env=None):
        self.workspace=Path(workspace).resolve();self.timeout=timeout;self.sequence=0;self.messages=queue.Queue()
        command=[arg.replace('{workspace}',str(self.workspace)) for arg in command]
        logs=self.workspace/'logs';logs.mkdir(parents=True,exist_ok=True)
        self.log=(logs/log_name).open('a',encoding='utf-8')
        env=dict(os.environ,**(extra_env or {}))
        try:
            self.process=subprocess.Popen(command,cwd=self.workspace,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,
                text=True,encoding='utf-8',env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        except BaseException:self.log.close();raise
        self.reader=threading.Thread(target=self._read,daemon=True);self.reader.start()
        try:
            self.request('initialize',{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'stickman-production','version':'0.1.0'}})
            self._send({'jsonrpc':'2.0','method':'notifications/initialized'})
        except BaseException:self.close();raise
    def _read(self):
        try:
            for line in self.process.stdout:
                try:self.messages.put(json.loads(line))
                except ValueError:pass
        finally:self.messages.put(None)
    def _send(self,value):
        self.process.stdin.write(json.dumps(value)+'\n');self.process.stdin.flush()
    def request(self,method,params):
        self.sequence+=1;request_id=self.sequence;deadline=time.monotonic()+self.timeout
        self._send({'jsonrpc':'2.0','id':request_id,'method':method,'params':params})
        while True:
            remaining=deadline-time.monotonic()
            if remaining<=0:raise TimeoutError(method)
            try:reply=self.messages.get(timeout=remaining)
            except queue.Empty:raise TimeoutError(method)
            if reply is None:raise RuntimeError('MCP process ended; inspect its local log')
            if reply.get('id')!=request_id:continue
            if 'error' in reply:raise RuntimeError(reply['error'])
            return reply['result']
    def call(self,tool,**arguments):
        result=self.request('tools/call',{'name':tool,'arguments':arguments})
        if result.get('isError'):raise RuntimeError(result)
        if result.get('structuredContent') is not None:return result['structuredContent']
        texts=[q['text'] for q in result.get('content',[]) if q['type']=='text']
        if len(texts)==1:
            try:return json.loads(texts[0])
            except ValueError:return texts[0]
        return texts
    def close(self):
        try:
            if self.process.stdin and not self.process.stdin.closed:self.process.stdin.close()
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
        finally:
            self.reader.join(timeout=1)
            self.process.stdout.close()
            self.log.close()
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
