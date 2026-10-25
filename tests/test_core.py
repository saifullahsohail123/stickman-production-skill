import array,copy,json,math,sys,tempfile,unittest,wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/stickman-production/scripts'))
from core import TimeMap,archive,clock,inside,read_json,sha256,validate,write_json
from audio_tools import trim_wav
from mcp_stdio import MCP

class CoreTests(unittest.TestCase):
    def episode(self):return read_json(ROOT/'skills/stickman-production/assets/episode.example.json')
    def test_real_durations_and_deliberate_gaps(self):
        result=clock([{'duration':2.13,'gap_after':.4},{'duration':1.27}],lead=.2,tail=.5)
        self.assertAlmostEqual(result['lines'][1]['start'],2.73)
        self.assertAlmostEqual(result['duration'],4.5)
        self.assertEqual(result['speed'],1)
    def test_invalid_clock(self):
        for takes in [[{'duration':0}],[{'duration':2,'gap_after':-.2}],[{'duration':float('nan')}]]:
            with self.assertRaises(ValueError):clock(takes)
        with self.assertRaises(ValueError):clock([],lead=float('inf'))
    def test_two_clocks_are_invertible(self):
        mapping=TimeMap([(0,0),(2,3.2),(3,4),(6,8.4)])
        for t in [0,.7,2,2.6,5.1,6]:self.assertAlmostEqual(mapping.at(mapping.at(t),inverse=True),t)
    def test_collapsed_or_reversed_cuts_rejected(self):
        with self.assertRaises(ValueError):TimeMap([(0,0),(1,2),(2,1)])
        with self.assertRaises(ValueError):TimeMap([(0,0),(1,1)]).cut_frames([0,.001,1],24)
    def test_integer_picture_coverage(self):
        data=self.episode();validate(data)
        data['shots'][0]['start_frame']=1
        with self.assertRaises(ValueError):validate(data)
        data=self.episode();data['shots'][0]['end_frame']=71
        with self.assertRaises(ValueError):validate(data)
    def test_unknown_speaker_rejected(self):
        data=self.episode();data['lines']=[{'id':'one','speaker':'other','text':'Hello'}]
        with self.assertRaises(ValueError):validate(data)
    def test_unicode_roundtrip_and_workspace_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=inside(root,'words.json');value={'hi':'छोटी सी चुटकी','ur':'ایک چھوٹی سی چٹکی'}
            write_json(path,value);self.assertEqual(read_json(path),value)
            with self.assertRaises(ValueError):inside(root,'../outside.json')
    def test_language_variants_and_immutable_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source.mp4';source.write_bytes(b'original')
            data=self.episode();english=archive(source,root/'deliveries',data)
            hindi=copy.deepcopy(data);hindi['identity']['language']='hi'
            archive(source,root/'deliveries',hindi)
            self.assertEqual(len(read_json(root/'deliveries/index.json')),2)
            source.write_bytes(b'changed')
            with self.assertRaises(FileExistsError):archive(source,root/'deliveries',data)
            self.assertEqual(english.read_bytes(),b'original')
            source.write_bytes(b'original');renamed=copy.deepcopy(data);renamed['identity']['slug']='renamed'
            with self.assertRaises(FileExistsError):archive(source,root/'deliveries',renamed)
    def test_trim_preserves_pcm_and_channels(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source.wav';target=root/'edit.wav';rate=16000
            frames=[(0,0)]*1600+[(int(7000*math.sin(i*.1)),int(3000*math.cos(i*.1))) for i in range(3200)]+[(0,0)]*1600
            pcm=array.array('h',[x for pair in frames for x in pair])
            if sys.byteorder!='little':pcm.byteswap()
            payload=pcm.tobytes()
            with wave.open(str(source),'wb') as output:output.setparams((2,2,rate,0,'NONE','not compressed'));output.writeframes(payload)
            result=trim_wav(source,target)
            with wave.open(str(target),'rb') as audio:
                edit=audio.readframes(audio.getnframes());self.assertEqual((audio.getnchannels(),audio.getframerate()),(2,rate))
            lo=round(result['trim_start']*rate)*4;hi=round(result['trim_end']*rate)*4
            self.assertEqual(edit,payload[lo:hi]);self.assertEqual(result['speech_speed'],1)
    def test_silent_take_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'silence.wav'
            with wave.open(str(path),'wb') as output:output.setparams((1,2,16000,0,'NONE','not compressed'));output.writeframes(b'\0'*3200)
            with self.assertRaises(ValueError):trim_wav(path,Path(temp)/'out.wav')
    def test_mcp_named_arguments_and_protocol_noise(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);server=root/'server.py'
            server.write_text('import sys,json\nprint("startup noise",flush=True)\nfor line in sys.stdin:\n r=json.loads(line)\n if "id" not in r:continue\n value={} if r["method"]=="initialize" else {"structuredContent":r["params"]["arguments"]}\n print(json.dumps({"jsonrpc":"2.0","id":r["id"],"result":value}),flush=True)\n',encoding='utf-8')
            with MCP([sys.executable,str(server)],root,'mock.log',timeout=3) as client:
                self.assertEqual(client.call('project_create',name='demo'),{'name':'demo'})
    def test_mcp_eof_does_not_hang(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(RuntimeError):MCP([sys.executable,'-c','pass'],temp,'eof.log',timeout=3)

if __name__=='__main__':unittest.main()
