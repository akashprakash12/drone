"""Local bridge: n8n launch/stop/reset plus browser-reported SIMULATED detections."""
import json, pathlib, threading, datetime
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit
ROOT = pathlib.Path(__file__).resolve().parent
TOKEN = json.loads((ROOT/'automation_config.json').read_text(encoding='utf-8'))['token']
lock = threading.Lock()
state = {'command_id': 0, 'command': 'reset', 'mission_id': 'MISSION-000', 'mission_status': 'standby', 'detections': []}
def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def send_json(self,code,obj):
        raw=json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/api/status':
            with lock: result={k:v for k,v in state.items() if k!='detections'}
            return self.send_json(200,result)
        if path=='/api/detections':
            with lock: result={'mission_id':state['mission_id'],'status':state['mission_status'],'detections':list(state['detections']),'count':len(state['detections']),'simulated':True}
            return self.send_json(200,result)
        if path in ('/automation_config.json','/server.py') or path.startswith('/n8n_'):
            return self.send_json(404,{'error':'Not found'})
        return super().do_GET()
    def do_POST(self):
        path=urlsplit(self.path).path
        if path not in ('/api/launch','/api/stop','/api/reset','/api/detections'):
            return self.send_json(404,{'error':'Unknown API route'})
        if path=='/api/detections':
            # Browser same-origin reports only. n8n should use GET for this endpoint.
            origin=self.headers.get('Origin','')
            host=self.headers.get('Host','')
            if origin and origin not in ('http://'+host,'https://'+host):
                return self.send_json(403,{'error':'Cross-origin report rejected'})
        elif self.headers.get('X-Demo-Token','')!=TOKEN:
            return self.send_json(403,{'error':'Invalid automation token'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<=size<=8192: return self.send_json(413,{'error':'Invalid request size'})
            raw=self.rfile.read(size)
            payload=json.loads(raw) if raw else {}
            if not isinstance(payload,dict): raise ValueError('Expected object')
        except (ValueError, OSError, json.JSONDecodeError):
            return self.send_json(400,{'error':'Invalid JSON'})
        with lock:
            if path=='/api/detections':
                event=payload.get('event')
                if event=='launch':
                    state['mission_id']='MISSION-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                    state['detections']=[]
                    state['mission_status']='flying'
                elif event=='detection':
                    name=str(payload.get('object','')).upper()
                    if name not in ('BUILDING','VEHICLE','TREE','PERSON'):
                        return self.send_json(400,{'error':'Unknown simulated object'})
                    confidence=payload.get('confidence')
                    if not isinstance(confidence,(int,float)) or not 0<=confidence<=1:
                        return self.send_json(400,{'error':'Invalid confidence'})
                    object_id=str(payload.get('object_id') or payload.get('person_id') or name)[:80]
                    model=str(payload.get('model') or '')[:120]
                    if not any(x['object_id']==object_id for x in state['detections']):
                        state['detections'].append({'object':name,'object_id':object_id,'person_id':str(payload.get('person_id') or ''),'model':model,'confidence':confidence,'timestamp':stamp(),'simulated':True})
                elif event in ('complete','stop','reset'):
                    state['mission_status']=event
                    if event=='reset': state['detections']=[]
                else: return self.send_json(400,{'error':'Unknown report event'})
                result={'ok':True,'mission_id':state['mission_id'],'count':len(state['detections'])}
            else:
                command=path.rsplit('/',1)[-1]
                state['command_id']+=1
                state['command']=command
                result={'ok':True,'command_id':state['command_id'],'command':command}
                print('N8N COMMAND:',result,flush=True)
        return self.send_json(200,result)
if __name__=='__main__':
    server=ThreadingHTTPServer(('0.0.0.0',8000),Handler)
    print('Dashboard: http://localhost:8000')
    print('Detection report: http://localhost:8000/api/detections')
    print('n8n Docker host URL: http://host.docker.internal:8000')
    print('Keep this terminal open; restrict port 8000 to trusted local access.')
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
